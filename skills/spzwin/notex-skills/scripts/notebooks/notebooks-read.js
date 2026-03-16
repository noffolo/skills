#!/usr/bin/env node
/**
 * NoteX Notebook 来源读取脚本（可独立执行）
 *
 * 功能：
 * 1) 获取某个 Notebook 下的来源列表（不含正文）
 * 2) 获取某个来源的正文内容（contentText）
 *
 * ⚠️ 独立执行说明：
 *   本脚本可脱离 AI Agent 直接在命令行运行。
 *   执行前请先阅读 Notebooks 模块的 OpenAPI 接口文档获取完整入参说明：
 *   docs/skills/openapi/notebooks/api-index.md
 *
 * 用法示例：
 *   # 若已设置环境变量 XG_USER_TOKEN，可省略 --key
 *   node docs/skills/scripts/notebooks/notebooks-read.js --mode list --key CWORK_KEY --notebook-id nb_xxx
 *   node docs/skills/scripts/notebooks/notebooks-read.js --mode content --key CWORK_KEY --notebook-id nb_xxx --source-id src_xxx
 */

const PROD_NOTEX_HOST = 'notex.aishuo.co';
const PROD_NOTEX_BASE_URL = 'https://notex.aishuo.co/noteX';

function parseArgs() {
  const args = process.argv.slice(2);
  const result = {};
  for (let i = 0; i < args.length; i += 1) {
    const key = args[i];
    if (!key.startsWith('--')) continue;
    const normalized = key.replace(/^--/, '');
    const next = args[i + 1];
    if (!next || next.startsWith('--')) {
      result[normalized] = 'true';
      continue;
    }
    result[normalized] = next;
    i += 1;
  }
  return result;
}

async function requestJson(url, options = {}) {
  const controller = new AbortController();
  const timeoutMs = options.timeoutMs || 60000;
  const timeout = setTimeout(() => controller.abort(), timeoutMs);

  try {
    const response = await fetch(url, {
      method: options.method || 'GET',
      headers: options.headers || {},
      signal: controller.signal,
    });

    const text = await response.text();
    let payload = {};
    if (text) {
      try {
        payload = JSON.parse(text);
      } catch (error) {
        throw new Error(`响应不是合法 JSON: ${text.slice(0, 200)}`);
      }
    }

    if (!response.ok) {
      const msg = payload.resultMsg || payload.error || response.statusText;
      throw new Error(`HTTP ${response.status}: ${msg}`);
    }

    if (payload && typeof payload === 'object' && 'resultCode' in payload) {
      if (payload.resultCode !== 1) {
        throw new Error(payload.resultMsg || `API error (${payload.resultCode})`);
      }
      return payload.data;
    }

    return payload;
  } finally {
    clearTimeout(timeout);
  }
}

function buildHeaders(args) {
  if (!args['access-token']) {
    throw new Error('缺少 access-token：必须先通过环境变量或 CWork Key 获取 access-token');
  }
  return {
    'Content-Type': 'application/json',
    'access-token': args['access-token'],
  };
}

function normalizeProdBaseUrl(rawBaseUrl) {
  let parsed;
  try {
    parsed = new URL(rawBaseUrl);
  } catch {
    throw new Error(`base-url 非法：${rawBaseUrl}`);
  }

  if (parsed.protocol !== 'https:') {
    throw new Error('base-url 必须使用 https 协议');
  }
  if (parsed.hostname !== PROD_NOTEX_HOST) {
    throw new Error(`base-url 必须使用生产域名 ${PROD_NOTEX_HOST}`);
  }

  const pathname = parsed.pathname.replace(/\/+$/, '');
  if (!pathname || pathname === '/') {
    return `${parsed.origin}/noteX`;
  }
  if (pathname === '/noteX') {
    return `${parsed.origin}${pathname}`;
  }
  if (pathname === '/noteX/openapi') {
    return `${parsed.origin}${pathname}`;
  }
  throw new Error('base-url 路径仅支持 /noteX 或 /noteX/openapi');
}

function getBaseUrl(args) {
  const base = args['base-url'] || process.env.NOTEX_API_BASE_URL || PROD_NOTEX_BASE_URL;
  return normalizeProdBaseUrl(base);
}

function buildApiUrl(baseUrl, apiPath) {
  const normalizedApiPath = apiPath.startsWith('/openapi/') ? apiPath : `/openapi${apiPath.replace(/^\/api/i, '')}`;
  if (/\/noteX\/openapi$/i.test(baseUrl) || /\/openapi$/i.test(baseUrl)) {
    return `${baseUrl}${normalizedApiPath.replace(/^\/openapi/i, '')}`;
  }
  if (/\/noteX$/i.test(baseUrl)) {
    return `${baseUrl}${normalizedApiPath}`;
  }
  throw new Error(`不支持的 base-url: ${baseUrl}`);
}

async function exchangeTokenByKey(cworkKey) {
  const url = `https://cwork-web.mediportal.com.cn/user/login/appkey?appCode=cms_gpt&appKey=${encodeURIComponent(cworkKey)}`;
  const data = await requestJson(url, {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' },
    timeoutMs: 30000,
  });

  if (!data || !data.xgToken) {
    throw new Error('CWork Key 换 token 失败：返回字段不完整');
  }

  return {
    accessToken: data.xgToken,
  };
}

function getEnvAuthContext() {
  const envToken = process.env.XG_USER_TOKEN;
  if (envToken) {
    return { accessToken: envToken };
  }
  return null;
}

async function resolveAuthContext(args) {
  const envAuth = getEnvAuthContext();
  if (envAuth) {
    console.log('[auth] 使用环境变量鉴权 (XG_USER_TOKEN)');
    args['access-token'] = envAuth.accessToken;
    return;
  }

  if (!args.key) {
    throw new Error('缺少鉴权参数：请提供环境变量 (XG_USER_TOKEN) 或 --key（推荐）');
  }

  console.log('[auth] 使用 CWork Key 换取 token...');
  const auth = await exchangeTokenByKey(args.key);

  args['access-token'] = auth.accessToken;
  console.log('[auth] 鉴权成功');
}

async function listSources(args) {
  const notebookId = args['notebook-id'];
  if (!notebookId) {
    throw new Error('list 模式必须提供 --notebook-id');
  }

  const baseUrl = getBaseUrl(args);
  const headers = buildHeaders(args);

  const query = new URLSearchParams();
  if (args['business-type']) query.set('businessType', args['business-type']);
  const queryString = query.toString();
  const url = buildApiUrl(baseUrl, `/api/notebooks/${notebookId}/sources${queryString ? `?${queryString}` : ''}`);

  const data = await requestJson(url, { headers, timeoutMs: 60000 });
  console.log(JSON.stringify(data, null, 2));
}

async function fetchSourceContent(args) {
  const notebookId = args['notebook-id'];
  const sourceId = args['source-id'];
  if (!notebookId || !sourceId) {
    throw new Error('content 模式必须提供 --notebook-id 与 --source-id');
  }

  const baseUrl = getBaseUrl(args);
  const headers = buildHeaders(args);

  const url = buildApiUrl(baseUrl, `/api/notebooks/${notebookId}/sources/${sourceId}/content`);
  const data = await requestJson(url, { headers, timeoutMs: 60000 });
  console.log(JSON.stringify(data, null, 2));
}

function printUsage() {
  console.log(`
用法:
  # 获取 Notebook 下来源列表（不含正文）
  node docs/skills/scripts/notebooks/notebooks-read.js --mode list --key <CWorkKey> --notebook-id <nbId>

  # 获取单个来源正文
  node docs/skills/scripts/notebooks/notebooks-read.js --mode content --key <CWorkKey> --notebook-id <nbId> --source-id <srcId>

可选参数:
  --key <CWorkKey>            CWork Key（推荐；脚本内部自动换取授权）
  --mode <list|content>       list=来源列表，content=获取正文
  --notebook-id <id>          目标 Notebook ID
  --source-id <id>            目标 Source ID（mode=content 必填）
  --business-type <type>      业务类型筛选（mode=list 可选）
  --base-url <url>            生产地址（仅支持 https://notex.aishuo.co/noteX 或 /noteX/openapi）
`);
}

async function main() {
  const args = parseArgs();
  const mode = args.mode;

  if (args.help || !mode) {
    printUsage();
    return;
  }

  if (mode !== 'list' && mode !== 'content') {
    printUsage();
    throw new Error(`不支持的 mode: ${mode}`);
  }

  await resolveAuthContext(args);

  if (mode === 'list') {
    await listSources(args);
    return;
  }

  await fetchSourceContent(args);
}

main().catch((error) => {
  console.error(`❌ ${error.message}`);
  process.exit(1);
});
