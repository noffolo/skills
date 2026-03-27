#!/usr/bin/env python3
"""On-chain Settlement Predictor v1.2.0"""
from __future__ import annotations
import argparse, json, logging, os, sys, time, urllib.request, urllib.parse
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime, timezone
from threading import Lock
from typing import Optional
logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")
try:
    from web3 import Web3
    from web3.exceptions import BlockNotFound, TransactionNotFound
except ImportError:
    print("ERROR: web3 not installed. Run: pip install web3>=6.0.0", file=sys.stderr); sys.exit(1)
# All keys are OPTIONAL.
ETHERSCAN_API_KEY = os.environ.get("ETHERSCAN_API_KEY", "")
TENDERLY_API_KEY  = os.environ.get("TENDERLY_API_KEY",  "")
TENDERLY_BASE = "https://api.tenderly.co/api/v1"
@dataclass
class ChainConfig:
    name: str; rpc_url: str; fallbacks: list = field(default_factory=list)
    chain_id: int = 1; explorer_api: str = ""; explorer_fallbacks: list = field(default_factory=list)
    def get_w3(self):
        for url in [self.rpc_url] + self.fallbacks:
            try:
                w3 = Web3(Web3.HTTPProvider(url, request_kwargs={"timeout": 10}))
                if w3.is_connected(): return w3
            except: pass
        raise ConnectionError(f"No RPC for {self.name}")
    def eu(self, module, action, params=None):
        base = self.explorer_fallbacks[0] if self.explorer_fallbacks else self.explorer_api
        if not base: return ""
        q = urllib.parse.urlencode({"chainid": self.chain_id, "module": module, "action": action, "apikey": ETHERSCAN_API_KEY})
        if params: q += "&" + urllib.parse.urlencode(params)
        return f"{base}?{q}"
CHAINS = {
    "ethereum":  ChainConfig(name="Ethereum",  chain_id=1,  rpc_url="https://eth.llamarpc.com",    fallbacks=["https://rpc.ankr.com/eth","https://ethereum.publicnode.com","https://rpc.mevblocker.io"],       explorer_api="https://api.etherscan.io/v2/api", explorer_fallbacks=["https://api.routescan.io/v2/network/mainnet/evm/1/etherscan"]),
    "arbitrum":  ChainConfig(name="Arbitrum One", chain_id=42161, rpc_url="https://arb1.arbitrum.io/rpc", fallbacks=["https://rpc.ankr.com/arbitrum","https://arbitrum.publicnode.com"], explorer_api="https://api.arbiscan.io/api", explorer_fallbacks=["https://api.routescan.io/v2/network/mainnet/evm/42161/etherscan"]),
    "optimism":  ChainConfig(name="Optimism",  chain_id=10,  rpc_url="https://mainnet.optimism.io", fallbacks=["https://rpc.ankr.com/optimism","https://optimism.publicnode.com"], explorer_api="https://api-optimistic.etherscan.io/api", explorer_fallbacks=["https://api.routescan.io/v2/network/mainnet/evm/10/etherscan"]),
    "base":      ChainConfig(name="Base",      chain_id=8453, rpc_url="https://mainnet.base.org",   fallbacks=["https://rpc.ankr.com/base","https://base.publicnode.com"],   explorer_api="https://api.basescan.org/api"),
    "polygon":   ChainConfig(name="Polygon",   chain_id=137, rpc_url="https://polygon-rpc.com",    fallbacks=["https://rpc.ankr.com/polygon","https://polygon.publicnode.com"], explorer_api="https://api.polygonscan.com/api"),
}
_HF = os.path.join(os.path.expanduser("~/.cache"), "settlement-predictor", "gas-history.json")
_HL = Lock(); _MH = 60
def _lh():
    if not os.path.exists(_HF): return {}
    try:
        with open(_HF) as f: raw = json.load(f)
        return {k: deque(maxlen=_MH, iterable=v) for k, v in raw.items()}
    except: return {}
def _sh(h):
    try:
        os.makedirs(os.path.dirname(_HF), exist_ok=True)
        with open(_HF, "w") as f: json.dump({k: list(v) for k, v in h.items()}, f)
    except: pass
_P = _lh(); _GH = _P
for c in list(CHAINS.keys()):
    if c not in _GH: _GH[c] = deque(maxlen=_MH)
_BH = _GH.get("_btc", deque(maxlen=_MH))
if "_btc" not in _GH: _GH["_btc"] = _BH
def _rg(chain, std, fst):
    with _HL:
        if chain not in _GH: _GH[chain] = deque(maxlen=_MH)
        _GH[chain].append({"ts": time.time(), "s": std, "f": fst}); _sh(_GH)
def _rb(sat):
    with _HL: _BH.append({"ts": time.time(), "v": sat}); _GH["_btc"] = _BH; _sh(_GH)
def _at(h):
    if len(h) < 3: return {"dp": len(h), "tr": "unknown", "ch": "unknown", "sg": "insufficient_data", "rs": f"Need>=3 (have {len(h)})"}
    r = list(h)[-20:]; n = len(r); xv = list(range(n)); yv = [float(s.get("v", s.get("s", 0))) for s in r]
    xm = sum(xv)/n; ym = sum(yv)/n; num = sum((xv[i]-xm)*(yv[i]-ym) for i in range(n)); den = sum((xv[i]-xm)**2 for i in range(n))
    slope = num/den if den else 0.0; y0, y1 = yv[0], yv[-1]; chg = ((y1-y0)/y0)*100 if y0 > 0 else 0.0; avg = sum(yv)/n
    if abs(chg) < 2: tr, ch, sg = "stable", "横盘整理", "hold"
    elif slope > 0:
        if chg > 10: tr, ch, sg = "rising_fast", "上涨通道", "gas_up"
        elif chg > 3: tr, ch, sg = "rising", "温和上涨", "caution"
        else: tr, ch, sg = "slight_rise", "轻微上涨", "hold"
    else:
        if chg < -10: tr, ch, sg = "falling_fast", "快速回落", "good_time_to_send"
        elif chg < -3: tr, ch, sg = "falling", "回落通道", "caution"
        else: tr, ch, sg = "slight_fall", "轻微回落", "good_time_to_send"
    vol = None
    if len(r) >= 4:
        chgs = [(yv[i]-yv[i-1])/max(yv[i-1],0.001)*100 for i in range(1,len(yv))]
        vol = (sum((c-sum(chgs)/len(chgs))**2 for c in chgs)/len(chgs))**0.5
    d0, d1 = r[0]["ts"], r[-1]["ts"]
    recs = {"good_time_to_send": "现在是Gas低点，适合发送交易", "gas_up": "Gas正在快速上涨，建议尽早发送", "caution": "Gas趋势不明，建议关注实时数据", "hold": "Gas基本稳定，可以择机发送", "insufficient_data": "数据不足，建议多次查询后判断"}
    return {"dp": n, "dur": round((d1-d0)/60,1), "tr": tr, "ch": ch, "sg": sg, "slope": round(slope/max(avg,0.001)*100,4) if avg>0 else 0, "chg": round(chg,2), "avg": round(avg,4), "frm": y0, "to": y1, "vol": round(vol,2) if vol else None, "rec": recs.get(sg,"")}
def _rcall(url):
    time.sleep(0.25)
    try:
        req = urllib.request.Request(url); resp = urllib.request.urlopen(req, timeout=15)
        d = json.loads(resp.read())
        if d.get("status") == "0" and d.get("message") != "No transactions found": return {"error": d.get("message")}
        return d
    except Exception as e: return {"error": str(e)}
def _tend(url, payload):
    try:
        req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers={"X-Access-Key": TENDERLY_API_KEY, "Content-Type": "application/json"})
        return json.loads(urllib.request.urlopen(req, timeout=30).read())
    except Exception as e: return {"error": str(e)}
def _w2g(w): return w/1e9
def _g2w(g): return int(g*1e9)
def _w2e(w): return w/1e18
def _bgr(w3, n):
    try: b = w3.eth.get_block(n); return b.gasUsed/b.gasLimit if b.gasLimit > 0 else 0.0
    except: return 0.0
def _pcg(w3):
    try: p = w3.eth.get_block("pending"); return p.gasUsed/p.gasLimit if p.gasLimit > 0 else 0.5
    except: return 0.5
def _gt(w3):
    try:
        lt = w3.eth.block_number
        r_ = sum(_bgr(w3,lt-i) for i in range(1,4))/3; o_ = sum(_bgr(w3,lt-i) for i in range(4,8))/4
        return "rising" if r_ > o_*1.1 else ("falling" if r_ < o_*0.9 else "stable")
    except: return "unknown"
def _bf(w3):
    try: return _w2g(w3.eth.fee_history(1,"latest",[])["baseFeePerGas"][0])
    except: return 30.0
GM = {"instant":1.5,"fast":1.25,"standard":1.05,"slow":0.95}
BT = {"ethereum":12.0,"arbitrum":0.25,"optimism":2.0,"base":2.0,"polygon":2.0}
HR = {0:0.85,1:0.80,2:0.75,3:0.78,4:0.82,5:0.88,6:0.95,7:1.10,8:1.25,9:1.35,10:1.30,11:1.20,12:1.15,13:1.18,14:1.22,15:1.28,16:1.20,17:1.15,18:1.20,19:1.25,20:1.15,21:1.05,22:0.98,23:0.92}
MB = "https://mempool.space/api"; MB1 = "https://mempool.space/api/v1"
BH = {0:0.80,1:0.75,2:0.70,3:0.72,4:0.75,5:0.80,6:0.88,7:1.05,8:1.20,9:1.30,10:1.25,11:1.18,12:1.12,13:1.10,14:1.15,15:1.20,16:1.18,17:1.22,18:1.28,19:1.25,20:1.15,21:1.08,22:0.98,23:0.88}
UV2="0x7a250d5630b4cf539739df2c5dacb4c659f2488d".lower()
UV3="0xe592427a0aece92de3edee1f18e0157c05861564".lower()
SUS="0xd9e1ce17f2641f24ae83637ab66a2cca9c378b9f".lower()
ERC20ABI=json.loads('[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"}]')
def get_gas_prediction(chain):
    if chain not in CHAINS: return {"error": f"Unsupported chain: {chain}"}
    w3 = CHAINS[chain].get_w3(); bf = _bf(w3); cg = _pcg(w3); tr = _gt(w3); bt = BT.get(chain,12.0)
    tiers = {}
    for t, m in GM.items():
        g = round(bf*m, 2); b = int({"instant":1,"fast":3,"standard":6,"slow":12}[t]*bt)
        tiers[t] = {"gwei": g, "desc": f"{t.upper()} - ~{b}s on {CHAINS[chain].name}"}
    r = {"chain": chain, "chain_name": CHAINS[chain].name, "base_fee_gwei": round(bf,2), "congestion_pct": round(cg*100,1), "trend": tr, "gas_tiers": tiers, "block_time_seconds": bt, "ts": datetime.now(timezone.utc).isoformat().replace("+00:00","Z")}
    _rg(chain, tiers.get("standard",{}).get("gwei",bf), tiers.get("fast",{}).get("gwei",bf))
    with _HL: h = _GH.get(chain)
    if h and len(h) >= 3: r["trend_analysis"] = _at(h)
    return r
def predict_settlement_time(chain, gp):
    if chain not in CHAINS: return {"error": f"Unsupported chain: {chain}"}
    w3 = CHAINS[chain].get_w3(); bt = BT.get(chain,12.0); bf = _bf(w3); pm = gp-bf; ratio = pm/max(bf,0.001)
    if pm <= 0 or ratio < 0.1: t,b,p = "unlikely",999,0.1
    elif ratio < 0.2: t,b,p = "unlikely",12,0.3
    elif ratio < 0.5: t,b,p = "standard",6,0.75
    elif ratio < 1.0: t,b,p = "fast",3,0.90
    else: t,b,p = "instant",1,0.97
    return {"chain":chain,"gas_price_gwei":gp,"base_fee_gwei":round(bf,4),"premium_pct":round(ratio*100,2),"estimated_blocks":b,"estimated_eta_sec":round(b*bt,1),"inclusion_prob":round(min(p,0.99),3),"tier":t,"hint":"Higher gas = faster. 10-20% above base_fee = safe margin.","ts":datetime.now(timezone.utc).isoformat().replace("+00:00","Z")}
def get_optimal_window(chain, urgency):
    if chain not in CHAINS: return {"error": f"Unsupported chain: {chain}"}
    if urgency not in ("low","medium","high"): return {"error": "urgency must be: low, medium, or high"}
    try: w3 = CHAINS[chain].get_w3(); bf = _bf(w3); bt = BT.get(chain,12.0)
    except Exception as e: return {"error": f"Failed: {e}"}
    ch = datetime.now(timezone.utc).hour; cp = HR.get(ch,1.0); cg = round(bf*cp,4)
    bh = min(range(24), key=lambda h: HR.get(h,1.0)); bp = HR.get(bh,1.0); bg = round(bf*bp,4)
    sv = max(0,(cg-bg)/max(cg,0.001)*100)
    if urgency == "high": rec = "send immediately" if cp < 1.15 else "now is elevated"; w = 0; gt = round(bf*1.3,2)
    elif urgency == "medium": rec = f"wait ~{(bh-ch)%24}h" if sv > 5 else "within 1-2h"; w = 0 if sv <= 5 else ((bh-ch)%24)*60; gt = round(bf*(1.1 if sv<=5 else bp),2)
    else: rec = f"wait ~{(bh-ch)%24}h" if sv > 8 else "within 2-4h"; w = 0 if sv <= 8 else ((bh-ch)%24)*60; gt = round(bf*(1.05 if sv<=8 else bp),2)
    return {"chain":chain,"urgency":urgency,"recommended_action":rec,"wait_minutes":max(0,w),"expected_savings_pct":max(0,sv),"gas_target_gwei":gt,"next_window_utc":f"{bh:02d}:00","current_hour_utc":f"{ch:02d}:00","current_gas_index":round(cp,2),"best_gas_index":round(bp,2),"block_time_seconds":bt,"ts":datetime.now(timezone.utc).isoformat().replace("+00:00","Z")}
def analyze_pending_pool(chain, pool, direction, amount_usd):
    if chain not in CHAINS: return {"error": f"Unsupported chain: {chain}"}
    if direction not in ("buy","sell"): return {"error": "direction must be: buy or sell"}
    if amount_usd <= 0: return {"error": "amount_usd must be positive"}
    try: w3 = CHAINS[chain].get_w3(); bf = _bf(w3)
    except Exception as e: return {"error": f"Failed: {e}"}
    try: Web3.to_checksum_address(pool)
    except: return {"error": f"Invalid pool address: {pool}"}
    pl = pool.lower()
    if direction == "buy" and amount_usd > 5000: sr = "high"
    elif direction == "buy" and amount_usd > 1000: sr = "medium"
    elif direction == "sell" and amount_usd > 5000: sr = "medium"
    else: sr = "low"
    sl = 0.5 if sr == "high" else (0.3 if sr == "medium" else 0.1)
    warnings = []
    if sr in ("high","medium"): warnings.append("三明治攻击风险 - 建议增加滑点容忍度")
    if amount_usd > 10000: warnings.append("大额交易考虑使用Flashbots/MEV保护RPC")
    if pl in (UV2,SUS): warnings.append("UniswapV2/SushiSwap - 滑点建议0.5%-1.0%")
    elif pl == UV3: warnings.append("Uniswap V3 - 滑点建议0.3%-1.0%，无常损失需注意")
    return {"chain":chain,"pool_address":pool,"direction":direction,"amount_usd":amount_usd,"base_fee_gwei":round(bf,4),"sandwich_risk":sr,"slippage_recommended":sl,"warnings":warnings if warnings else ["✅ 风险较低"],"safety_tips":["Use MEV-protected RPC","Set slippage 0.5-1.0% for large trades."],"ts":datetime.now(timezone.utc).isoformat().replace("+00:00","Z")}
def _hr(raw):
    rl = raw.lower(); m = {"insufficient funds":"余额不足","execution reverted":"交易回滚","nonce too low":"Nonce错误","replacement underpriced":"替换费用过低","insufficient a amount":"代币A不足","insufficient b amount":"代币B不足","insufficient balance":"余额不足","expired":"交易过期","slippage":"滑点超限","unauthorized":"未授权"}
    for k, d in m.items():
        if k in rl: return f"⚠️ {d} | {raw[:80]}"
    return f"⚠️ 交易回滚 | {raw[:80]}"
def track_transaction(chain, tx_hash):
    if chain not in CHAINS: return {"error": f"Unsupported chain: {chain}"}
    try: w3 = CHAINS[chain].get_w3(); Web3.to_checksum_address(tx_hash[:42])
    except Exception as e: return {"error": f"Invalid tx_hash: {e}"}
    receipt = None; tx_ts = None; confirmed = False; confirmations = 0
    try:
        receipt = w3.eth.get_transaction_receipt(tx_hash); confirmed = receipt.status == 1; bn = receipt.blockNumber
        try: tip = w3.eth.block_number; confirmations = tip - bn + 1
        except: confirmations = 1
        try: blk = w3.eth.get_block(bn); tx_ts = datetime.utcfromtimestamp(blk.timestamp).isoformat()+"Z"
        except: pass
    except TransactionNotFound: confirmed = False; confirmations = 0
    except Exception as e: return {"error": f"Failed: {e}"}
    rr = None
    if receipt and receipt.status == 0:
        rr = "⚠️ 交易失败（status=0）"
        if ETHERSCAN_API_KEY:
            cfg = CHAINS.get(chain)
            if cfg:
                url = cfg.eu("transaction","gettxreceiptstatus",{"txhash":tx_hash})
                if url:
                    d = _rcall(url)
                    if "result" in d and d["result"]: rr = _hr(d["result"])
    gu = receipt.gasUsed if receipt else None; eg = receipt.effectiveGasPrice if receipt else None
    return {"chain":chain,"tx_hash":tx_hash,"confirmed":confirmed,"status":"confirmed ✅" if confirmed else ("failed ❌" if receipt and receipt.status==0 else "pending ⏳"),"block_number":receipt.blockNumber if receipt else None,"confirmations":confirmations,"timestamp":tx_ts,"gas_used":int(gu) if gu else None,"effective_gas_price_gwei":round(_w2g(int(eg)),4) if eg else None,"tx_fee_eth":round(_w2e(int((gu or 0)*(eg or 0))),8) if gu and eg else None,"revert_reason":rr,"ts":datetime.now(timezone.utc).isoformat().replace("+00:00","Z")}
def verify_contract(chain, addr):
    if chain not in CHAINS: return {"error": f"Unsupported chain: {chain}"}
    if not ETHERSCAN_API_KEY: return {"error":"ETHERSCAN_API_KEY required","hint":"Set env var","free_alts":["https://www.contractreader.io/","https://sourcify.dev/"]}
    cfg = CHAINS[chain]; url = cfg.eu("contract","getsourcecode",{"address":addr})
    if not url: return {"error": f"No explorer API for {chain}"}
    info = _rcall(url)
    if "result" in info and info["result"]:
        src = info["result"][0]; v = bool(src.get("SourceCode","").strip() not in ("","1")); risks = []
        if not v: risks.append("合约未开源 - 无法验证代码安全性")
        if src.get("Proxy","0") == "1": risks.append(f"代理合约: {src.get('Implementation','')}")
        if "selfdestruct" in src.get("SourceCode","").lower(): risks.append("⚠️ selfdestruct")
        try: ca = Web3.to_checksum_address(addr)
        except: ca = addr
        return {"chain":chain,"contract_address":ca,"verified":v,"contract_name":src.get("ContractName",""),"compiler_version":src.get("CompilerVersion",""),"optimization":src.get("OptimizationUsed",""),"license":src.get("LicenseType","Unknown"),"is_proxy":src.get("Proxy","0")=="1","risks":risks if risks else ["✅ 未检测到明显风险"],"hint":"建议使用Tenderly进行完整交易模拟"}
    return {"error": info.get("message","Failed to fetch")}
def get_token_info(chain, addr):
    if chain not in CHAINS: return {"error": f"Unsupported chain: {chain}"}
    try: w3 = CHAINS[chain].get_w3(); ca = Web3.to_checksum_address(addr)
    except Exception as e: return {"error": f"Invalid address: {e}"}
    r = {"chain":chain,"token_address":ca}
    try:
        c = w3.eth.contract(address=ca, abi=ERC20ABI)
        r["name"] = c.functions.name().call(); r["symbol"] = c.functions.symbol().call(); r["decimals"] = c.functions.decimals().call(); total = c.functions.totalSupply().call()
        r["total_supply"] = total; r["total_supply_formatted"] = total/(10**r["decimals"])
    except: pass
    if ETHERSCAN_API_KEY and CHAINS[chain].explorer_api:
        cfg = CHAINS[chain]; eb = cfg.explorer_api.split("/api")[0]
        hu = _rcall(f"{eb}/api?module=token&action=tokenholdercount&contractaddress={ca}&apikey={ETHERSCAN_API_KEY}")
        if "result" in hu:
            try: r["holder_count"] = int(hu["result"])
            except: r["holder_count"] = hu.get("result")
    return {"chain":chain,"token_address":ca,"name":r.get("name","Unknown"),"symbol":r.get("symbol","???"),"decimals":r.get("decimals",18),"total_supply":r.get("total_supply"),"total_supply_formatted":r.get("total_supply_formatted"),"holder_count":r.get("holder_count","N/A (requires Etherscan Pro)"),"source":"on-chain" if not ETHERSCAN_API_KEY else "on-chain + Etherscan API","ts":datetime.now(timezone.utc).isoformat().replace("+00:00","Z")}
def get_internal_txs(chain, tx_hash):
    if chain not in CHAINS: return {"error": f"Unsupported chain: {chain}"}
    if not ETHERSCAN_API_KEY: return {"error":"ETHERSCAN_API_KEY required","hint":"Set env var"}
    cfg = CHAINS[chain]; url = cfg.eu("transaction","txlistinternal",{"txhash":tx_hash})
    if not url: return {"error": f"No explorer API for {chain}"}
    d = _rcall(url)
    if "result" in d:
        txs = d["result"]
        if not txs: return {"chain":chain,"tx_hash":tx_hash,"internal_txs":[],"count":0}
        parsed = []
        for tx in (txs if isinstance(txs,list) else [txs]):
            if isinstance(tx,dict): parsed.append({"from":tx.get("from",""),"to":tx.get("to",""),"value_eth":_w2e(int(tx.get("value",0))),"type":tx.get("type","CALL"),"error":tx.get("isError","0")=="1"})
        return {"chain":chain,"tx_hash":tx_hash,"internal_txs":parsed,"count":len(parsed),"ts":datetime.now(timezone.utc).isoformat().replace("+00:00","Z")}
    return {"error": d.get("message","Failed to fetch")}
def simulate_transaction(chain, from_addr, to_addr, value_eth, calldata, gas_limit):
    if chain not in CHAINS: return {"error": f"Unsupported chain: {chain}"}
    if not TENDERLY_API_KEY: return {"error":"TENDERLY_API_KEY required for simulation","hint":"Sign up free at https://dashboard.tenderly.co/"}
    cfg = CHAINS[chain]
    try:
        w3 = CHAINS[chain].get_w3()
        fa = Web3.to_checksum_address(from_addr) if from_addr and from_addr != "0x0000000000000000000000000000000000000000" else None
        ta = Web3.to_checksum_address(to_addr); vwei = _g2w(value_eth*1e9) if value_eth > 0 else 0
        nonce = w3.eth.get_transaction_count(fa) if fa else 0; gl = gas_limit if gas_limit else 8000000
        payload = {"network_id":str(cfg.chain_id),"from":fa or "0x0000000000000000000000000000000000000000","to":ta,"input":calldata,"gas":gl,"gas_price":str(int(w3.eth.gas_price*1.1)),"value":str(vwei),"nonce":nonce,"simulation_type":{"type":"full"}}
        res = _tend(f"{TENDERLY_BASE}/simulate", payload)
        if "error" in res: return {"error": res["error"]}
        sim = res.get("simulation",{}); exe = sim.get("execution",{}); gu = exe.get("gas_used",0); st = exe.get("status","unknown")
        return {"chain":chain,"from":fa or "0x000...","to":ta,"value_eth":value_eth,"status":st,"gas_used":gu,"gas_limit":gl,"simulation_source":"tenderly","ts":datetime.now(timezone.utc).isoformat().replace("+00:00","Z")}
    except Exception as e: return {"error": f"Simulation failed: {e}"}
def _mg(path):
    url = f"{MB}{path}"
    try: req = urllib.request.Request(url); return json.loads(urllib.request.urlopen(req, timeout=15).read().decode())
    except Exception as e: return {"error": str(e)}
def _mv(path):
    url = f"{MB1}{path}"
    try: req = urllib.request.Request(url); return json.loads(urllib.request.urlopen(req, timeout=15).read().decode())
    except Exception as e: return {"error": str(e)}
def get_btc_fee_estimate(urgency="medium"):
    fees = _mv("/fees/recommended")
    if "error" in fees: return fees
    mp = _mg("/mempool"); mc = mp.get("count","unknown") if isinstance(mp,dict) else "unknown"
    cg = "high" if isinstance(mp,dict) and mp.get("count",0)>100000 else ("medium" if isinstance(mp,dict) and mp.get("count",0)>30000 else "low") if isinstance(mp,dict) else "unknown"
    fs = fees.get("fastestFee",10); hh = fees.get("halfHourFee",5); hr_ = fees.get("hourFee",3); ec = fees.get("economyFee",2); mn = fees.get("minimumFee",1)
    tiers = {"instant":round(fs*1.5),"fast":fs,"standard":hh,"slow":hr_,"economy":ec,"minimum":mn}
    um = {"high":"fast","medium":"standard","low":"slow"}; rt = um.get(urgency,"standard"); rs = tiers.get(rt,hh)
    tb = {"instant":1,"fast":1,"standard":3,"slow":6,"economy":24,"minimum":144}
    def cost(s,vb=225): return round(s*vb/100,2)
    result = {"chain":"bitcoin","chain_id":0,"unit":"sat/vB","mempool_count":mc,"congestion":cg,"hour_utc":datetime.now(timezone.utc).hour,"tiers":{k:{"sat_vb":tiers[k],"blocks":tb[k],"eta":["~10","~30","~60","~4h","~24h"][[1,3,6,24,144].index(tb[k])] if tb[k] in [1,3,6,24,144] else "~10","cost_btc":cost(tiers[k])} for k in tiers},"recommended":{"tier":rt,"sat_vb":rs,"blocks":tb.get(rt,3),"eta":"~30" if rt=="standard" else "~10","cost_btc":cost(rs),"cost_usd":None},"raw_api":fees,"ts":datetime.now(timezone.utc).isoformat().replace("+00:00","Z")}
    _rb(rs)
    if _BH and len(_BH) >= 3: result["trend_analysis"] = _at(_BH)
    return result
def predict_btc_settlement(sat, urgency="medium"):
    fees = _mv("/fees/recommended")
    if "error" in fees: return fees
    fs = fees.get("fastestFee",10); hh = fees.get("halfHourFee",5); hr_ = fees.get("hourFee",3); mn = fees.get("minimumFee",1)
    if sat >= fs: t,b,p,eta = "fast",1,"~10 min",0.95
    elif sat >= hh: t,b,p,eta = "standard",3,"~30 min",0.90
    elif sat >= hr_: t,b,p,eta = "slow",6,"~60 min",0.80
    elif sat >= 2: t,b,p,eta = "economy",24,"~4 hours",0.65
    elif sat >= mn: t,b,p,eta = "minimum",72,"~12 hours",0.50
    else: t,b,p,eta = "rejected",None,"likely dropped",0.05
    return {"chain":"bitcoin","sat_per_vb":sat,"tier":t,"urgency":urgency,"estimated_blocks":b,"estimated_eta":eta,"inclusion_prob":p,"confidence":"high" if sat>=fs else ("medium" if sat>=hh else "low"),"typical_tx_cost_btc":round(sat*225/100000000,8),"typical_tx_cost_sat":int(sat*225),"hint":"Higher sat/vB = faster confirmation.","ts":datetime.now(timezone.utc).isoformat().replace("+00:00","Z")}
def get_optimal_btc_window(urgency="medium"):
    fees = _mv("/fees/recommended")
    if "error" in fees: return fees
    now_utc = datetime.now= datetime.now(timezone.utc); ch = now_utc.hour
    bh = min(range(24), key=lambda h: BH.get(h, 1.0)); bp = BH.get(bh, 1.0)
    tier_name = {"high":"fast","medium":"standard","low":"slow"}.get(urgency,"standard")
    current_sat = fees.get("halfHourFee",5) if tier_name in ("standard","slow") else fees.get("fastestFee",10)
    sorted_hours = sorted([{"h":h,"v":BH.get(h,1.0)} for h in range(24)], key=lambda x: x["v"])
    cheapest = sorted_hours[0]
    return {"chain":"bitcoin","urgency":urgency,"tier":tier_name,"current_hour_utc":ch,"recommended":{"hour_utc":cheapest["h"],"hours_ahead":(cheapest["h"]-ch)%24,"label":f"{cheapest['h']:02d}:00 UTC","est_sat_vb":max(1,int(cheapest["v"]*current_sat)),"savings_vs_now":max(0,current_sat-max(1,int(cheapest["v"]*current_sat)))},"top_3_cheapest":[{"hour":f"{w['h']:02d}:00","sat_vb":max(1,int(w['v']*current_sat)),"hours_ahead":(w['h']-ch)%24} for w in sorted_hours[:3]],"mempool_base_fee":fees,"ts":datetime.now(timezone.utc).isoformat().replace("+00:00","Z")}
def track_btc_transaction(tx_hash):
    tx = _mg(f"/tx/{tx_hash}")
    if "error" in tx: return tx
    st = tx.get("status",{}); confirmed = st.get("confirmed",False); bh = st.get("block_height")
    if confirmed and bh:
        try: tip = _mg("/blocks/tip/height"); conf = tip-bh+1 if isinstance(tip,int) else tx.get("confirmations",1)
        except: conf = tx.get("confirmations",1)
    else: conf,bh = 0,None
    fr = None
    if not confirmed and tx.get("fee") and tx.get("vin") and tx.get("vout"):
        try: vb = tx.get("virtual_size",tx.get("size",225)); fr = round(tx.get("fee")/vb,2) if vb>0 else None
        except: pass
    return {"chain":"bitcoin","tx_hash":tx_hash,"confirmed":confirmed,"status":f"confirmed in block {bh}" if confirmed else "unconfirmed - in mempool","block_height":bh,"confirmations":conf,"fee_sat":tx.get("fee"),"fee_rate_sat_vb":fr,"size_bytes":tx.get("size",0),"vsize":tx.get("virtual_size",tx.get("size",0)),"num_inputs":len(tx.get("vin",[])),"num_outputs":len(tx.get("vout",[])),"total_in_sat":sum(v.get("prevout",{}).get("value",0) for v in tx.get("vin",[]) if v.get("prevout")),"total_out_sat":sum(v.get("value",0) for v in tx.get("vout",[])),"ts":datetime.now(timezone.utc).isoformat().replace("+00:00","Z")}
def analyze_btc_trend():
    btc_data = get_btc_fee_estimate("medium")
    if "error" in btc_data: return btc_data
    with _HL: h = _BH
    ta = _at(h) if h and len(h)>=3 else {"dp":len(h) if h else 0,"tr":"unknown","ch":"unknown","sg":"insufficient_data","rs":"Need>=3 pts"}
    return {"chain":"bitcoin","sat_vb":btc_data.get("recommended",{}).get("sat_vb"),"congestion":btc_data.get("congestion"),"trend_analysis":ta,"ts":datetime.now(timezone.utc).isoformat().replace("+00:00","Z")}
def main():
    p = argparse.ArgumentParser(description="On-chain Settlement Predictor v1.2.0")
    sub = p.add_subparsers(dest="cmd", required=True)
    def sa(sp): sp.add_argument("-c","--chain",default="ethereum",choices=list(CHAINS.keys())); sp.add_argument("-f","--format",default="json",choices=["json","table"])
    def ap(name,help_,extra=None):
        pp = sub.add_parser(name,help=help_); sa(pp)
        if extra: extra(pp)
        return pp
    ap("get-gas-prediction","Get current gas tiers")
    p2 = sub.add_parser("predict-settlement",help="Predict settlement time"); sa(p2); p2.add_argument("-g","--gas-price",type=float,required=True)
    p3 = sub.add_parser("get-optimal-window",help="Find optimal time window"); sa(p3); p3.add_argument("-u","--urgency",default="medium",choices=["low","medium","high"])
    p4 = sub.add_parser("analyze-pending-pool",help="Analyze pending pool for sandwich risk"); sa(p4)
    p4.add_argument("-p","--pool",required=True); p4.add_argument("-d","--direction",required=True,choices=["buy","sell"]); p4.add_argument("-a","--amount",type=float,required=True)
    p5 = sub.add_parser("track-tx",help="Track transaction"); sa(p5); p5.add_argument("-t","--tx",required=True)
    p6 = sub.add_parser("verify-contract",help="Verify contract"); sa(p6); p6.add_argument("-a","--address",required=True)
    p7 = sub.add_parser("get-token-info",help="Get token info"); sa(p7); p7.add_argument("-a","--address",required=True)
    p8 = sub.add_parser("get-internal-txs",help="Get internal txs"); sa(p8); p8.add_argument("-t","--tx",required=True)
    p9 = sub.add_parser("simulate-tx",help="Simulate tx"); sa(p9); p9.add_argument("--from",default="0x0000000000000000000000000000000000000000"); p9.add_argument("-t","--to",required=True); p9.add_argument("-v","--value",type=float,default=0.0); p9.add_argument("-d","--data",default="0x"); p9.add_argument("--gas",type=int)
    p10 = sub.add_parser("btc-fee-estimate",help="BTC fee estimate"); p10.add_argument("-u","--urgency",default="medium",choices=["low","medium","high"])
    p11 = sub.add_parser("btc-predict-settlement",help="Predict BTC settlement"); p11.add_argument("-s","--sat",type=float,required=True); p11.add_argument("-u","--urgency",default="medium",choices=["low","medium","high"])
    p12 = sub.add_parser("btc-optimal-window",help="BTC optimal window"); p12.add_argument("-u","--urgency",default="medium",choices=["low","medium","high"])
    p13 = sub.add_parser("track-btc-tx",help="Track BTC tx"); p13.add_argument("-t","--tx",required=True)
    p14 = sub.add_parser("analyze-gas-trend",help="Analyze gas trend"); p14.add_argument("-c","--chain",default="ethereum",choices=list(CHAINS.keys()))
    sub.add_parser("analyze-btc-trend",help="Analyze BTC fee trend")
    args = p.parse_args()
    result = None
    if args.cmd == "get-gas-prediction": result = get_gas_prediction(args.chain)
    elif args.cmd == "predict-settlement": result = predict_settlement_time(args.chain, args.gas_price)
    elif args.cmd == "get-optimal-window": result = get_optimal_window(args.chain, args.urgency)
    elif args.cmd == "analyze-pending-pool": result = analyze_pending_pool(args.chain, args.pool, args.direction, args.amount)
    elif args.cmd == "track-tx": result = track_transaction(args.chain, args.tx)
    elif args.cmd == "verify-contract": result = verify_contract(args.chain, args.address)
    elif args.cmd == "get-token-info": result = get_token_info(args.chain, args.address)
    elif args.cmd == "get-internal-txs": result = get_internal_txs(args.chain, args.tx)
    elif args.cmd == "simulate-tx": result = simulate_transaction(args.chain, args.from_, args.to, args.value, args.data, args.gas)
    elif args.cmd == "btc-fee-estimate": result = get_btc_fee_estimate(args.urgency)
    elif args.cmd == "btc-predict-settlement": result = predict_btc_settlement(args.sat, args.urgency)
    elif args.cmd == "btc-optimal-window": result = get_optimal_btc_window(args.urgency)
    elif args.cmd == "track-btc-tx": result = track_btc_transaction(args.tx)
    elif args.cmd == "analyze-gas-trend":
        g = get_gas_prediction(args.chain)
        if "error" in g: result = g
        else:
            with _HL: h = _GH.get(args.chain)
            ta = _at(h) if h and len(h)>=3 else {"dp":len(h) if h else 0,"tr":"unknown","ch":"unknown","sg":"insufficient_data","rs":"Need>=3 pts"}
            result = {"chain":args.chain,"sat_vb":g.get("base_fee_gwei"),"trend_analysis":ta,"ts":datetime.now(timezone.utc).isoformat().replace("+00:00","Z")}
    elif args.cmd == "analyze-btc-trend": result = analyze_btc_trend()
    if result: print(json.dumps(result, indent=2, ensure_ascii=False))
if __name__ == "__main__": main()
