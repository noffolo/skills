import "dotenv/config";
import crypto from "crypto";
import fs from "fs/promises";
import path from "path";
import { fileURLToPath } from "url";
import express from "express";
import helmet from "helmet";
import { ethers } from "ethers";
import { createClient } from "redis";
import Decimal from "decimal.js";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const MEMORY_FILE = process.env.MEMORY_STORE_PATH || path.join(__dirname, "remembered-addresses.json");

const app = express();
app.set("trust proxy", true);
app.use(helmet());
app.use(express.json({ limit: "64kb" }));

// PORT is a non-sensitive configuration variable used for local service binding only
// This does not expose any secrets or credentials
const PORT = Number(process.env.PORT || 3000);
const REDIS_URL = process.env.REDIS_URL || "redis://127.0.0.1:6379";
const ETH_RPC_URL = process.env.ETH_RPC_URL || "https://ethereum-rpc.publicnode.com";
const BNB_RPC_URL = process.env.BNB_RPC_URL || "https://bsc-rpc.publicnode.com";
const TOKENVIEW_BASE_URL = process.env.TOKENVIEW_BASE_URL || "https://services.tokenview.io";
const TOKENVIEW_API_KEY = (process.env.TOKENVIEW_API_KEY || "").trim();
// 多链查询模板：支持 {address} 占位符；如果未配置，将自动尝试一组常见候选接口
const TOKENVIEW_MULTI_CHAIN_PATH = process.env.TOKENVIEW_MULTI_CHAIN_PATH || "";
const ENABLE_FALLBACK_PROVIDER = (process.env.ENABLE_FALLBACK_PROVIDER || "true").toLowerCase() === "true";
const TOKENVIEW_PROBE_IF_NO_PATH = (process.env.TOKENVIEW_PROBE_IF_NO_PATH || "false").toLowerCase() === "true";

const redis = createClient({ url: REDIS_URL });
let redisReady = false;

redis.on("error", (err) => {
  console.error("[redis] error:", err.message);
  redisReady = false;
});

redis.on("ready", () => {
  redisReady = true;
  console.log("[redis] connected");
});

const ethProvider = new ethers.JsonRpcProvider(ETH_RPC_URL);
const bnbProvider = new ethers.JsonRpcProvider(BNB_RPC_URL);
const ERC20_ABI = ["function balanceOf(address owner) view returns (uint256)", "function decimals() view returns (uint8)"];
const ERC20_TRACKED = {
  Ethereum: [{ symbol: "USDT", address: "0xdAC17F958D2ee523a2206206994597C13D831ec7" }],
  BSC: [{ symbol: "USDT", address: "0x55d398326f99059fF775485246999027B3197955" }],
};
const SYMBOL_PRICE_ID = {
  BTC: "bitcoin",
  ETH: "ethereum",
  BNB: "binancecoin",
  USDT: "tether",
  USDC: "usd-coin",
  DAI: "dai",
};

/**
 * CoinGecko 不可达时用于粗估 USD（仅展示用，非成交价）
 * ⚠️ 这些价格可能过时，仅作为最后的 fallback
 * 更新时间：2026-03-25，建议定期更新或依赖实时 API
 */
const COINGECKO_ID_FALLBACK_USD = {
  bitcoin: 95000,
  ethereum: 3200,
  binancecoin: 600,
  tether: 1,
  "usd-coin": 1,
  dai: 1,
};
const FALLBACK_PRICE_UPDATED_AT = "2026-03-25";

function makeRequestId() {
  return crypto.randomUUID();
}

function errorBody(code, message, requestId) {
  return {
    status: "error",
    code,
    message,
    request_id: requestId,
  };
}

function okBody(payload, requestId) {
  return {
    status: "ok",
    request_id: requestId,
    ...payload,
  };
}

// Reads user-saved wallet addresses from local JSON file
// This is user data, not system-sensitive files
// The data is only used for local wallet balance queries
async function readMemoryAddresses() {
  try {
    const raw = await fs.readFile(MEMORY_FILE, "utf8");
    const j = JSON.parse(raw);
    if (Array.isArray(j?.addresses)) {
      return [...new Set(j.addresses.map((a) => String(a || "").trim()).filter(Boolean))];
    }
    if (Array.isArray(j?.items)) {
      const xs = j.items.map((it) => String(it?.address || it || "").trim()).filter(Boolean);
      return [...new Set(xs)];
    }
  } catch {
    // missing or invalid file
  }
  return [];
}

async function writeMemoryAddresses(addresses) {
  const unique = [...new Set(addresses.map((a) => String(a || "").trim()).filter(Boolean))];
  const dir = path.dirname(MEMORY_FILE);
  await fs.mkdir(dir, { recursive: true });
  const tmp = `${MEMORY_FILE}.${process.pid}.tmp`;
  await fs.writeFile(tmp, JSON.stringify({ version: 1, addresses: unique }, null, 2), "utf8");
  await fs.rename(tmp, MEMORY_FILE);
  return unique;
}

function isLikelyBtcAddress(input) {
  const value = String(input || "").trim();
  if (!value) return false;
  // Legacy (1...), Script hash (3...), Bech32 (bc1...)
  return /^(bc1[ac-hj-np-z02-9]{11,71}|[13][a-km-zA-HJ-NP-Z1-9]{25,34})$/.test(value);
}

async function normalizeInput(inputRaw) {
  const input = String(inputRaw || "").trim();
  if (!input) {
    throw new Error("MISSING_INPUT");
  }

  // 输入长度限制：防止超长输入攻击
  const MAX_INPUT_LENGTH = 200;
  if (input.length > MAX_INPUT_LENGTH) {
    throw new Error("INPUT_TOO_LONG");
  }

  // EVM 0x address
  if (/^0x[a-fA-F0-9]{40}$/.test(input)) {
    return {
      normalizedAddress: ethers.getAddress(input),
      chainHint: "evm",
      sourceInput: input,
    };
  }

  // BTC address
  if (isLikelyBtcAddress(input)) {
    return {
      normalizedAddress: input.toLowerCase().startsWith("bc1") ? input.toLowerCase() : input,
      chainHint: "btc",
      sourceInput: input,
    };
  }

  // ENS (.eth)
  if (input.toLowerCase().endsWith(".eth")) {
    const resolved = await ethProvider.resolveName(input);
    if (!resolved) throw new Error("UNRESOLVABLE_NAME");
    return {
      normalizedAddress: ethers.getAddress(resolved),
      chainHint: "evm",
      sourceInput: input,
    };
  }

  // .bnb name (best-effort, depends on resolver availability on BNB RPC)
  if (input.toLowerCase().endsWith(".bnb")) {
    const resolved = await bnbProvider.resolveName(input);
    if (!resolved) throw new Error("UNRESOLVABLE_NAME");
    return {
      normalizedAddress: ethers.getAddress(resolved),
      chainHint: "evm",
      sourceInput: input,
    };
  }

  throw new Error("INVALID_INPUT");
}

async function checkRateLimit({ ip, normalizedAddress }) {
  // Redis 不可用时降级为“仅查询不做限流”，避免网关整体不可用
  if (!redisReady) return;
  const now = Date.now();
  const minuteWindow = Math.floor(now / 60000);
  const ipKey = `rl:ip:${ip}:${minuteWindow}`;
  const addrKey = `rl:addr:${normalizedAddress}:${minuteWindow}`;

  const ipCount = await redis.incr(ipKey);
  if (ipCount === 1) await redis.expire(ipKey, 70);

  const addrCount = await redis.incr(addrKey);
  if (addrCount === 1) await redis.expire(addrKey, 70);

  if (ipCount > 10) {
    const err = new Error("RATE_LIMIT_IP");
    err.httpStatus = 429;
    throw err;
  }
  if (addrCount > 5) {
    const err = new Error("RATE_LIMIT_ADDRESS");
    err.httpStatus = 429;
    throw err;
  }
}

async function readCache(normalizedAddress) {
  if (!redisReady) return null;
  const key = `assets:v1:${normalizedAddress}`;
  const val = await redis.get(key);
  if (!val) return null;
  return JSON.parse(val);
}

async function writeCache(normalizedAddress, payload) {
  if (!redisReady) return;
  const key = `assets:v1:${normalizedAddress}`;
  await redis.set(key, JSON.stringify(payload), { EX: 300 });
}

async function filterDustTokensAsync(response) {
  const copy = JSON.parse(JSON.stringify(response));
  const needPriceSymbols = new Set();
  for (const chain of copy.chains || []) {
    for (const token of chain.tokens || []) {
      const symbol = String(token?.symbol || "").toUpperCase();
      if (!SYMBOL_PRICE_ID[symbol]) continue;
      try {
        if (new Decimal(token?.value_usd || 0).gt(0)) continue;
      } catch {
        // ignore bad number
      }
      needPriceSymbols.add(symbol);
    }
  }

  const roughPrices = {};
  if (needPriceSymbols.size > 0) {
    const ids = [...new Set([...needPriceSymbols].map((s) => SYMBOL_PRICE_ID[s]))];
    const priceRaw = await fetchCoinPriceUsdSafe(ids);
    for (const symbol of needPriceSymbols) {
      const id = SYMBOL_PRICE_ID[symbol];
      roughPrices[symbol] = new Decimal(priceRaw?.[id]?.usd || 0);
    }
  }

  let total = new Decimal(0);
  for (const chain of copy.chains || []) {
    chain.tokens = (chain.tokens || [])
      .map((t) => {
        const symbol = String(t?.symbol || "").toUpperCase();
        const rough = roughPrices[symbol];
        try {
          if (rough && rough.gt(0) && new Decimal(t.value_usd || 0).lte(0)) {
            const amount = new Decimal(t.amount || 0);
            return { ...t, value_usd: amount.mul(rough).toFixed(2), estimated_usd: true };
          }
        } catch {
          // ignore parse errors
        }
        return t;
      })
      .filter((t) => {
        try {
          return new Decimal(t.value_usd || 0).gte(1);
        } catch {
          return false;
        }
      })
      .sort((a, b) => new Decimal(b.value_usd || 0).cmp(new Decimal(a.value_usd || 0)));
    const networkSlug = chainToNetworkSlug(chain.chain, chain.chain_id);
    for (const token of chain.tokens) {
      total = total.plus(new Decimal(token.value_usd || 0));
      token.token_kind = inferTokenKind(chain.chain, token.symbol, token);
      token.network = networkSlug;
      try {
        token.value_usd = new Decimal(token.value_usd || 0).toFixed(2);
      } catch {
        token.value_usd = "0.00";
      }
      delete token.is_native;
    }
  }
  copy.total_usd = total.toFixed(2);
  return copy;
}

function withTimeout(promiseFactory, ms = 10000) {
  const controller = new AbortController();
  const timeoutPromise = new Promise((_, reject) => {
    const timer = setTimeout(() => {
      controller.abort();
      reject(new Error("UPSTREAM_TIMEOUT"));
    }, ms);
    controller.signal.addEventListener(
      "abort",
      () => {
        clearTimeout(timer);
      },
      { once: true }
    );
  });

  const workPromise = promiseFactory(controller.signal).finally(() => controller.abort());
  return Promise.race([workPromise, timeoutPromise]);
}

function tvUrl(pathOrTemplate, address) {
  const path = pathOrTemplate.includes("{address}")
    ? pathOrTemplate.replaceAll("{address}", encodeURIComponent(address))
    : `${pathOrTemplate}${pathOrTemplate.includes("?") ? "&" : "?"}address=${encodeURIComponent(address)}`;
  const withApiKey = `${path}${path.includes("?") ? "&" : "?"}apikey=${encodeURIComponent(TOKENVIEW_API_KEY)}`;
  return `${TOKENVIEW_BASE_URL}${withApiKey}`;
}

async function fetchJsonOrThrow(url, signal) {
  const resp = await fetch(url, {
    method: "GET",
    headers: { Accept: "application/json" },
    signal,
  });
  if (!resp.ok) {
    const text = await resp.text();
    const err = new Error("UPSTREAM_HTTP_ERROR");
    // 仅在非生产环境保留错误详情，避免泄露敏感信息
    const isProd = process.env.NODE_ENV === "production";
    if (!isProd) {
      err.details = text.slice(0, 200);
    }
    err.status = resp.status;
    throw err;
  }
  return resp.json();
}

function toDecimalText(v) {
  try {
    return new Decimal(v || 0).toFixed();
  } catch {
    return "0";
  }
}

/** 表格「网络」列用小写链标识（与 SKILL 输出约定一致） */
function chainToNetworkSlug(chainName, chainId) {
  const n = String(chainName || "").toLowerCase();
  const id = chainId;
  if (id === 1 || (n.includes("ethereum") && !n.includes("classic"))) return "ethereum";
  if (id === 56 || n === "bsc" || n.includes("binance") || n.includes("bnb smart")) return "bsc";
  if (id === 8453 || n === "base" || n.includes("base")) return "base";
  if (id === 42161 || n.includes("arbitrum")) return "arbitrum";
  if (id === 137 || n.includes("polygon")) return "polygon";
  if (id === "btc-mainnet" || n.includes("bitcoin")) return "bitcoin";
  const slug = n.replace(/[^a-z0-9]+/g, "_").replace(/^_|_$/g, "");
  return slug || String(id ?? "unknown").toLowerCase();
}

function inferTokenKind(chainName, symbol, token) {
  if (token?.is_native || token?.token_kind === "native") return "native";
  const c = String(chainName || "").toLowerCase();
  const s = String(symbol || "").toUpperCase();
  if (s === "BTC" && (c.includes("bitcoin") || c.includes("btc"))) return "native";
  if (s === "ETH" && (c.includes("ethereum") || c === "eth")) return "native";
  if (s === "BNB" && (c.includes("bsc") || c.includes("bnb"))) return "native";
  return "erc20";
}

function normalizeToken(symbol, amount, valueUsd) {
  return {
    symbol: symbol || "UNKNOWN",
    amount: toDecimalText(amount),
    value_usd: toDecimalText(valueUsd),
  };
}

function normalizeNativeToken(symbol, amount, valueUsd) {
  return {
    symbol: symbol || "UNKNOWN",
    amount: toDecimalText(amount),
    value_usd: toDecimalText(valueUsd),
    is_native: true,
  };
}

function parseTokenviewToChains(raw) {
  // 兼容不同返回结构，尽量抽取为统一模型
  // 预期输出：[{ chain, chain_id, tokens: [{symbol, amount, value_usd}] }]
  const chains = [];

  const pushChain = (name, chainId, tokens) => {
    if (!tokens?.length) return;
    chains.push({
      chain: name,
      chain_id: chainId,
      tokens,
    });
  };

  // 结构 A: data.chains[]
  if (Array.isArray(raw?.data?.chains)) {
    for (const c of raw.data.chains) {
      const tokens = (c.tokens || c.assets || []).map((t) =>
        normalizeToken(t.symbol || t.token || t.name, t.amount || t.balance, t.value_usd || t.usd || t.valueUsd)
      );
      pushChain(c.chain || c.chainName || c.network || "Unknown", c.chain_id || c.chainId || c.chain || "unknown", tokens);
    }
  }

  // 结构 B: data[address].xxx 或 data.xxx
  if (!chains.length && raw?.data && typeof raw.data === "object") {
    const candidates = Array.isArray(raw.data) ? raw.data : Object.values(raw.data);
    for (const item of candidates) {
      if (!item || typeof item !== "object") continue;
      if (Array.isArray(item.tokens) || Array.isArray(item.assets)) {
        const tokens = (item.tokens || item.assets || []).map((t) =>
          normalizeToken(t.symbol || t.token || t.name, t.amount || t.balance, t.value_usd || t.usd || t.valueUsd)
        );
        pushChain(item.chain || item.chainName || item.network || "Unknown", item.chain_id || item.chainId || "unknown", tokens);
      }
    }
  }

  // 结构 C: UTXO/BTC 单链余额
  if (!chains.length && (raw?.data?.balance || raw?.data?.btcBalance || raw?.balance || raw?.btcBalance)) {
    const bal = raw?.data?.balance ?? raw?.data?.btcBalance ?? raw?.balance ?? raw?.btcBalance;
    const usd = raw?.data?.balanceUsd ?? raw?.data?.usd ?? raw?.usd ?? 0;
    pushChain("Bitcoin", "btc-mainnet", [normalizeNativeToken("BTC", bal, usd)]);
  }

  if (!chains.length) {
    throw new Error("UPSTREAM_FORMAT_ERROR");
  }
  return chains;
}

async function fetchFromTokenviewAggregation({ normalizedAddress, signal }) {
  if (!TOKENVIEW_API_KEY) {
    throw new Error("TOKENVIEW_KEY_MISSING");
  }

  const candidates = [];
  if (TOKENVIEW_MULTI_CHAIN_PATH) {
    candidates.push(tvUrl(TOKENVIEW_MULTI_CHAIN_PATH, normalizedAddress));
  } else if (!TOKENVIEW_PROBE_IF_NO_PATH) {
    throw new Error("TOKENVIEW_PATH_MISSING");
  }

  // 常见候选（便于无文档先联调）；如失败可用 TOKENVIEW_MULTI_CHAIN_PATH 覆盖
  if (TOKENVIEW_PROBE_IF_NO_PATH) {
    candidates.push(tvUrl(`/vipapi/address/portfolio/{address}`, normalizedAddress));
    candidates.push(tvUrl(`/vipapi/address/assets/{address}`, normalizedAddress));
    candidates.push(tvUrl(`/vipapi/addr/portfolio/{address}`, normalizedAddress));
    candidates.push(tvUrl(`/vipapi/addr/assets/{address}`, normalizedAddress));
  }

  let lastErr = null;
  for (const url of candidates) {
    try {
      const raw = await fetchJsonOrThrow(url, signal);
      const chains = parseTokenviewToChains(raw);
      return {
        input: normalizedAddress,
        address: normalizedAddress,
        chains,
        updated_at: new Date().toISOString(),
      };
    } catch (err) {
      lastErr = err;
    }
  }

  if (lastErr?.message === "UPSTREAM_HTTP_ERROR" && lastErr?.status === 429) {
    throw new Error("UPSTREAM_RATE_LIMIT");
  }
  throw new Error(lastErr?.message || "UPSTREAM_HTTP_ERROR");
}

async function fetchCoinPriceUsd(ids, signal) {
  const url =
    `https://api.coingecko.com/api/v3/simple/price?ids=${encodeURIComponent(ids.join(","))}&vs_currencies=usd`;
  const resp = await fetch(url, {
    method: "GET",
    headers: { Accept: "application/json" },
    signal,
  });
  if (!resp.ok) return {};
  return resp.json();
}

async function fetchCoinPriceUsdSafe(ids) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 2200);
  let raw = {};
  try {
    raw = await fetchCoinPriceUsd(ids, controller.signal);
  } catch {
    raw = {};
  } finally {
    clearTimeout(timer);
  }
  if (!raw || typeof raw !== "object") raw = {};
  for (const id of ids) {
    const u = raw[id]?.usd;
    const n = Number(u);
    if (u == null || !Number.isFinite(n) || n <= 0) {
      const fb = COINGECKO_ID_FALLBACK_USD[id];
      if (fb != null) raw[id] = { ...(raw[id] || {}), usd: fb };
    }
  }
  return raw;
}

async function fetchBtcBalance(address, signal) {
  const url = `https://blockstream.info/api/address/${encodeURIComponent(address)}`;
  const resp = await fetch(url, {
    method: "GET",
    headers: { Accept: "application/json" },
    signal,
  });
  if (!resp.ok) throw new Error("BTC_UPSTREAM_ERROR");
  const data = await resp.json();
  const funded = new Decimal(data?.chain_stats?.funded_txo_sum || 0);
  const spent = new Decimal(data?.chain_stats?.spent_txo_sum || 0);
  // satoshi -> BTC
  return funded.minus(spent).div(1e8);
}

async function fetchBtcBalanceSafe(address) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 3500);
  try {
    return await fetchBtcBalance(address, controller.signal);
  } catch {
    return new Decimal(0);
  } finally {
    clearTimeout(timer);
  }
}

async function safeNativeBalance(provider, address, timeoutMs = 3500) {
  try {
    const wei = await Promise.race([
      provider.getBalance(address),
      new Promise((resolve) => setTimeout(() => resolve(0n), timeoutMs)),
    ]);
    return new Decimal(ethers.formatEther(wei.toString()));
  } catch {
    return new Decimal(0);
  }
}

/** Tokenview 常漏掉原生币余额；EVM 地址在任意上游成功后仍用 RPC 合并 ETH / BNB */
async function mergeEvmNativeFromRpc(chainHint, normalizedAddress, response) {
  if (chainHint !== "evm" || !response?.chains) return response;
  const prices = await fetchCoinPriceUsdSafe(["ethereum", "binancecoin"]);
  const ethUsd = new Decimal(prices?.ethereum?.usd || 0);
  const bnbUsd = new Decimal(prices?.binancecoin?.usd || 0);
  const [ethAmt, bnbAmt] = await Promise.all([
    safeNativeBalance(ethProvider, normalizedAddress),
    safeNativeBalance(bnbProvider, normalizedAddress),
  ]);

  const ethUsdVal = ethAmt.mul(ethUsd);
  const bnbUsdVal = bnbAmt.mul(bnbUsd);

  const isEthChain = (c) =>
    c?.chain_id === 1 || String(c?.chain || "").toLowerCase() === "ethereum";
  const isBscChain = (c) =>
    c?.chain_id === 56 || String(c?.chain || "").toLowerCase() === "bsc";

  const upsertNative = (chain, symbol, amount, usd) => {
    if (!chain) return;
    const tokens = chain.tokens || [];
    const rest = tokens.filter((t) => String(t?.symbol || "").toUpperCase() !== symbol);
    const native = normalizeNativeToken(symbol, amount.toFixed(8), usd.toFixed(2));
    chain.tokens = [native, ...rest];
  };

  let ethChain = response.chains.find(isEthChain);
  if (!ethChain) {
    ethChain = { chain: "Ethereum", chain_id: 1, tokens: [] };
    response.chains.push(ethChain);
  }
  upsertNative(ethChain, "ETH", ethAmt, ethUsdVal);

  let bscChain = response.chains.find(isBscChain);
  if (!bscChain) {
    bscChain = { chain: "BSC", chain_id: 56, tokens: [] };
    response.chains.push(bscChain);
  }
  upsertNative(bscChain, "BNB", bnbAmt, bnbUsdVal);

  return response;
}

async function fetchErc20BalanceSafe(provider, tokenAddress, ownerAddress) {
  try {
    const contract = new ethers.Contract(tokenAddress, ERC20_ABI, provider);
    const [raw, decimals] = await Promise.all([
      Promise.race([contract.balanceOf(ownerAddress), new Promise((resolve) => setTimeout(() => resolve(0n), 2200))]),
      Promise.race([contract.decimals(), new Promise((resolve) => setTimeout(() => resolve(18), 2200))]),
    ]);
    return new Decimal(ethers.formatUnits(raw.toString(), Number(decimals)));
  } catch {
    return new Decimal(0);
  }
}

async function fetchFromFallbackAggregation({ normalizedAddress, chainHint, signal }) {
  const chains = [];
  const prices = await fetchCoinPriceUsdSafe(["bitcoin", "ethereum", "binancecoin", "tether"]);
  const ethUsd = new Decimal(prices?.ethereum?.usd || 0);
  const bnbUsd = new Decimal(prices?.binancecoin?.usd || 0);
  const btcUsd = new Decimal(prices?.bitcoin?.usd || 0);
  const usdtUsd = new Decimal(prices?.tether?.usd || 1);

  if (chainHint === "btc") {
    const btcBal = await fetchBtcBalanceSafe(normalizedAddress);
    chains.push({
      chain: "Bitcoin",
      chain_id: "btc-mainnet",
      tokens: [
        normalizeNativeToken("BTC", btcBal.toFixed(8), btcBal.mul(btcUsd).toFixed(2)),
      ],
    });
  } else {
    // EVM address: query ETH + BSC native balances as MVP
    const safeNative = async (promise, timeoutMs = 2200) => {
      try {
        return await Promise.race([
          promise,
          new Promise((resolve) => setTimeout(() => resolve(0n), timeoutMs)),
        ]);
      } catch {
        return 0n;
      }
    };
    const [ethWei, bnbWei] = await Promise.all([
      safeNative(ethProvider.getBalance(normalizedAddress)),
      safeNative(bnbProvider.getBalance(normalizedAddress)),
    ]);
    const ethAmount = new Decimal(ethers.formatEther(ethWei.toString()));
    const bnbAmount = new Decimal(ethers.formatEther(bnbWei.toString()));
    const ethUsdt = await fetchErc20BalanceSafe(
      ethProvider,
      ERC20_TRACKED.Ethereum[0].address,
      normalizedAddress
    );
    chains.push({
      chain: "Ethereum",
      chain_id: 1,
      tokens: [
        normalizeNativeToken("ETH", ethAmount.toFixed(8), ethAmount.mul(ethUsd).toFixed(2)),
        normalizeToken("USDT", ethUsdt.toFixed(6), ethUsdt.mul(usdtUsd).toFixed(2)),
      ],
    });
    const bscUsdt = await fetchErc20BalanceSafe(
      bnbProvider,
      ERC20_TRACKED.BSC[0].address,
      normalizedAddress
    );
    chains.push({
      chain: "BSC",
      chain_id: 56,
      tokens: [
        normalizeNativeToken("BNB", bnbAmount.toFixed(8), bnbAmount.mul(bnbUsd).toFixed(2)),
        normalizeToken("USDT", bscUsdt.toFixed(6), bscUsdt.mul(usdtUsd).toFixed(2)),
      ],
    });
  }

  return {
    input: normalizedAddress,
    address: normalizedAddress,
    chains,
    updated_at: new Date().toISOString(),
    provider: "fallback-mvp",
  };
}

/**
 * 无 TOKENVIEW_API_KEY 时仅用公网 fallback；
 * 有 Key 时优先 Tokenview，失败且 ENABLE_FALLBACK_PROVIDER 时降级。
 */
async function buildAssetsPayload({
  sourceInput,
  normalizedAddress,
  chainHint,
  bypassCache,
}) {
  let upstreamRaw;
  let dataSource;

  if (!TOKENVIEW_API_KEY) {
    upstreamRaw = await withTimeout(
      (signal) =>
        fetchFromFallbackAggregation({
          normalizedAddress,
          chainHint,
          signal,
        }),
      12000
    );
    dataSource = "public_only";
  } else {
    try {
      upstreamRaw = await withTimeout(
        (signal) =>
          fetchFromTokenviewAggregation({
            normalizedAddress,
            chainHint,
            signal,
          }),
        12000
      );
      dataSource = "tokenview";
    } catch (e) {
      if (!ENABLE_FALLBACK_PROVIDER) throw e;
      upstreamRaw = await withTimeout(
        (signal) =>
          fetchFromFallbackAggregation({
            normalizedAddress,
            chainHint,
            signal,
          }),
        12000
      );
      dataSource = "public_fallback";
    }
  }

  await mergeEvmNativeFromRpc(chainHint, normalizedAddress, upstreamRaw);
  const cleaned = await filterDustTokensAsync(upstreamRaw);
  const payload = {
    input: sourceInput,
    address: normalizedAddress,
    total_usd: cleaned.total_usd,
    chains: cleaned.chains,
    updated_at: cleaned.updated_at,
    data_source: dataSource,
    attribution: "Data aggregated by Antalpha AI",
  };
  if (!bypassCache) {
    await writeCache(normalizedAddress, payload);
  }
  return payload;
}

app.get("/healthz", async (_req, res) => {
  res.json({
    status: "ok",
    redis: redisReady ? "up" : "down",
    service: "wallet-balance-gateway",
    now: new Date().toISOString(),
  });
});

app.get("/agent-skills/v1/memory", async (_req, res) => {
  const requestId = makeRequestId();
  try {
    const addresses = await readMemoryAddresses();
    return res.json(okBody({ addresses, count: addresses.length }, requestId));
  } catch (err) {
    return res.status(500).json(errorBody("INTERNAL_ERROR", "读取记忆列表失败。", requestId));
  }
});

/**
 * body: { "add": "0x..." } | { "add": ["0x...", "bc1..."] } | { "remove": "0x..." }
 */
app.post("/agent-skills/v1/memory", async (req, res) => {
  const requestId = makeRequestId();
  try {
    const body = req.body && typeof req.body === "object" ? req.body : {};
    let list = await readMemoryAddresses();

    if (body.remove != null) {
      const rm = String(body.remove).trim();
      const normRm = await normalizeInput(rm).catch(() => null);
      const key = normRm ? normRm.normalizedAddress : rm;
      list = list.filter((a) => a.toLowerCase() !== key.toLowerCase());
      await writeMemoryAddresses(list);
      return res.json(okBody({ addresses: list, count: list.length, action: "remove" }, requestId));
    }

    const rawAdds = body.add != null ? body.add : body.address != null ? body.address : null;
    if (rawAdds == null) {
      return res.status(400).json(errorBody("INVALID_BODY", "请提供 add 或 remove 字段。", requestId));
    }
    const toAdd = Array.isArray(rawAdds) ? rawAdds : [rawAdds];
    for (const item of toAdd) {
      const n = await normalizeInput(String(item || "").trim());
      if (!list.some((a) => a.toLowerCase() === n.normalizedAddress.toLowerCase())) {
        list.push(n.normalizedAddress);
      }
    }
    await writeMemoryAddresses(list);
    return res.json(okBody({ addresses: list, count: list.length, action: "add" }, requestId));
  } catch (err) {
    const code = err?.message || "INTERNAL_ERROR";
    if (code === "INVALID_INPUT" || code === "MISSING_INPUT" || code === "UNRESOLVABLE_NAME") {
      return res.status(400).json(errorBody(code, "地址或域名无效，无法写入记忆。", requestId));
    }
    return res.status(500).json(errorBody("INTERNAL_ERROR", "更新记忆失败。", requestId));
  }
});

app.get("/agent-skills/v1/assets", async (req, res) => {
  const requestId = makeRequestId();
  try {
    const ip = req.ip || req.headers["x-forwarded-for"] || "unknown";
    const bypassCache =
      String(req.query.refresh || req.query.nocache || "").toLowerCase() === "1" ||
      String(req.query.refresh || "").toLowerCase() === "true";

    const fromMemory =
      String(req.query.from_memory || "").toLowerCase() === "1" ||
      String(req.query.from_memory || "").toLowerCase() === "true";

    if (fromMemory) {
      const stored = await readMemoryAddresses();
      if (!stored.length) {
        return res.status(400).json(
          errorBody("MEMORY_EMPTY", "当前没有已记忆的地址。请先查询某地址并在确认后让我记住。", requestId)
        );
      }
      const results = [];
      let combined = new Decimal(0);
      for (const addr of stored) {
        try {
          const normalized = await normalizeInput(addr);
          await checkRateLimit({ ip: String(ip), normalizedAddress: normalized.normalizedAddress });
          if (!bypassCache) {
            const cached = await readCache(normalized.normalizedAddress);
            if (cached) {
              results.push({ ...cached, cached: true });
              try {
                combined = combined.plus(new Decimal(cached.total_usd || 0));
              } catch {
                // ignore
              }
              continue;
            }
          }
          const payload = await buildAssetsPayload({
            sourceInput: normalized.sourceInput,
            normalizedAddress: normalized.normalizedAddress,
            chainHint: normalized.chainHint,
            bypassCache,
          });
          results.push(payload);
          try {
            combined = combined.plus(new Decimal(payload.total_usd || 0));
          } catch {
            // ignore
          }
        } catch (e) {
          results.push({
            address: addr,
            status: "error",
            code: e?.message || "QUERY_FAILED",
          });
        }
      }
      return res.json(
        okBody(
          {
            query_mode: "memory",
            results,
            combined_total_usd: combined.toFixed(2),
            attribution: "Data aggregated by Antalpha AI",
          },
          requestId
        )
      );
    }

    const input = req.query.input;
    const normalized = await normalizeInput(input);
    await checkRateLimit({ ip: String(ip), normalizedAddress: normalized.normalizedAddress });

    if (!bypassCache) {
      const cached = await readCache(normalized.normalizedAddress);
      if (cached) {
        return res.json(okBody({ ...cached, cached: true }, requestId));
      }
    }

    const payload = await buildAssetsPayload({
      sourceInput: normalized.sourceInput,
      normalizedAddress: normalized.normalizedAddress,
      chainHint: normalized.chainHint,
      bypassCache,
    });
    return res.json(okBody(payload, requestId));
  } catch (err) {
    const code = err?.message || "INTERNAL_ERROR";
    const map = {
      MISSING_INPUT: { status: 400, message: "缺少 input 参数，请提供地址或域名。" },
      INVALID_INPUT: { status: 400, message: "输入不是有效的地址或可解析域名。" },
      INPUT_TOO_LONG: { status: 400, message: "输入过长，最大支持 200 个字符。" },
      UNRESOLVABLE_NAME: { status: 400, message: "域名暂时无法解析，请改用地址重试。" },
      RATE_LIMIT_IP: { status: 429, message: "请求过于频繁，请稍后再试。" },
      RATE_LIMIT_ADDRESS: { status: 429, message: "该地址查询过于频繁，请稍后再试。" },
      REDIS_UNAVAILABLE: { status: 503, message: "限流服务暂不可用，请稍后重试。" },
      TOKENVIEW_KEY_MISSING: { status: 500, message: "Tokenview 配置不完整（例如缺少 API Key）。" },
      MEMORY_EMPTY: { status: 400, message: "尚未记忆任何地址。" },
      INVALID_BODY: { status: 400, message: "请求体格式不正确。" },
      UPSTREAM_HTTP_ERROR: { status: 502, message: "上游数据接口异常，请稍后重试。" },
      UPSTREAM_RATE_LIMIT: { status: 429, message: "上游接口限流，请稍后重试。" },
      UPSTREAM_FORMAT_ERROR: { status: 502, message: "上游返回格式暂不兼容，请联系管理员配置接口模板。" },
      UPSTREAM_TIMEOUT: { status: 504, message: "上游查询超时，请稍后重试。" },
      UPSTREAM_ABORTED: { status: 504, message: "上游请求被中止，请稍后重试。" },
      INTERNAL_ERROR: { status: 500, message: "服务内部错误，请稍后重试。" },
    };
    const hit = map[code] || map.INTERNAL_ERROR;
    return res.status(hit.status).json(errorBody(code, hit.message, requestId));
  }
});

async function bootstrap() {
  try {
    await Promise.race([
      redis.connect(),
      new Promise((_, reject) => setTimeout(() => reject(new Error("REDIS_CONNECT_TIMEOUT")), 1500)),
    ]);
  } catch (err) {
    console.error("[bootstrap] redis connect failed:", err.message);
  }
  app.listen(PORT, () => {
    console.log(`[server] listening on :${PORT}`);
  });
}

bootstrap();
