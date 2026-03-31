import http from "http";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const PORT = process.env.NUWA_PORT || 3099;
const OPENCLAW_GATEWAY = process.env.OPENCLAW_GATEWAY || "http://localhost:18789";

// Read gateway config
const OPENCLAW_CFG_PATH = path.join(process.env.HOME, ".openclaw", "openclaw.json");
let OPENCLAW_TOKEN = process.env.OPENCLAW_GATEWAY_TOKEN || process.env.OPENCLAW_TOKEN || "";

try {
  const cfg = JSON.parse(fs.readFileSync(OPENCLAW_CFG_PATH, "utf-8"));
  if (!OPENCLAW_TOKEN) OPENCLAW_TOKEN = cfg?.gateway?.auth?.token || "";
  
  // Check (but do NOT auto-modify) chatCompletions endpoint
  const enabled = cfg?.gateway?.http?.endpoints?.chatCompletions?.enabled;
  if (!enabled) {
    console.log("   ⚠️  chatCompletions 端点未启用，语音对话将无法工作");
    console.log("   请手动添加到 ~/.openclaw/openclaw.json 并重启 Gateway:");
    console.log('   { "gateway": { "http": { "endpoints": { "chatCompletions": { "enabled": true } } } } }');
    console.log("   然后运行: openclaw gateway restart\n");
  }
} catch {}

// Demo config for 5-min free trial mode.
// These are NuwaAI-issued public demo keys with limited quota, NOT user credentials.
// They only grant access to the demo avatars below and expire per-session.
const DEMO_CONFIG = {
  zh: {
    apiKey: "sk-ody1Xk9lw_vXkRWEPnaO8OwTFB9gbCnng2EWUl5jNbzolDSlFItc9DvWqrr6RLcL",
    avatarId: "2037840977565188097",
    userId: "81936",
  },
  en: {
    apiKey: "sk-ody1Xk9lw_vXkRWEPnaO8OwTFB9gbCnng2EWUl5jNbzolDSlFItc9DvWqrr6RLcL",
    avatarId: "2037841603867942913",
    userId: "81936",
  },
};

// In-memory config store (persisted to local file)
const CONFIG_FILE = path.join(__dirname, ".nuwa-config.json");
let nuwaConfig = { apiKey: "", avatarId: "", userId: "" };
try {
  nuwaConfig = JSON.parse(fs.readFileSync(CONFIG_FILE, "utf-8"));
} catch {}

function saveConfig() {
  fs.writeFileSync(CONFIG_FILE, JSON.stringify(nuwaConfig, null, 2));
}

const mimeTypes = {
  ".html": "text/html",
  ".js": "application/javascript",
  ".css": "text/css",
  ".json": "application/json",
  ".svg": "image/svg+xml",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".gif": "image/gif",
  ".webp": "image/webp",
  ".ico": "image/x-icon",
};

const server = http.createServer(async (req, res) => {
  // CORS for local dev
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");
  if (req.method === "OPTIONS") { res.writeHead(204); res.end(); return; }

  // API: Health check proxy
  if (req.url === "/api/health" && req.method === "GET") {
    try {
      const headers = {};
      if (OPENCLAW_TOKEN) headers["Authorization"] = `Bearer ${OPENCLAW_TOKEN}`;
      const resp = await fetch(`${OPENCLAW_GATEWAY}/health`, { headers });
      const data = await resp.json();
      res.writeHead(200, { "Content-Type": "application/json" });
      res.end(JSON.stringify(data));
    } catch (e) {
      res.writeHead(200, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ ok: false, error: e.message }));
    }
    return;
  }

  // API: Get/Set NuwaAI config
  if (req.url === "/api/config" && req.method === "GET") {
    res.writeHead(200, { "Content-Type": "application/json" });
    res.end(JSON.stringify({
      avatarId: nuwaConfig.avatarId,
      userId: nuwaConfig.userId,
      hasApiKey: !!nuwaConfig.apiKey,
      gateway: OPENCLAW_GATEWAY,
      configured: !!(nuwaConfig.apiKey && nuwaConfig.avatarId && nuwaConfig.userId),
    }));
    return;
  }

  if (req.url === "/api/config" && req.method === "POST") {
    let body = "";
    for await (const chunk of req) body += chunk;
    try {
      const { apiKey, avatarId, userId } = JSON.parse(body);
      if (apiKey !== undefined) nuwaConfig.apiKey = apiKey;
      if (avatarId !== undefined) nuwaConfig.avatarId = avatarId;
      if (userId !== undefined) nuwaConfig.userId = userId;
      saveConfig();
      res.writeHead(200, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ ok: true, configured: !!(nuwaConfig.apiKey && nuwaConfig.avatarId && nuwaConfig.userId) }));
    } catch (e) {
      res.writeHead(400, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ error: e.message }));
    }
    return;
  }

  // API: Get demo/trial config
  if (req.url?.startsWith("/api/demo") && req.method === "GET") {
    const url = new URL(req.url, `http://${req.headers.host}`);
    const lang = url.searchParams.get("lang") === "en" ? "en" : "zh";
    const demo = DEMO_CONFIG[lang];

    // /api/demo — just config info
    if (url.pathname === "/api/demo") {
      res.writeHead(200, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ avatarId: demo.avatarId, userId: demo.userId }));
      return;
    }

    // /api/demo/token — get access token
    if (url.pathname === "/api/demo/token") {
      try {
        const resp = await fetch("https://api.nuwaai.com/web/apiKey/auth", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ secretKey: demo.apiKey }),
        });
        const data = await resp.json();
        res.writeHead(200, { "Content-Type": "application/json" });
        res.end(JSON.stringify({ ...data, avatarId: demo.avatarId }));
      } catch (e) {
        res.writeHead(500, { "Content-Type": "application/json" });
        res.end(JSON.stringify({ code: -1, msg: e.message }));
      }
      return;
    }
  }

  // API: Get NuwaAI access token
  if (req.url === "/api/token" && req.method === "GET") {
    if (!nuwaConfig.apiKey) {
      res.writeHead(200, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ code: -1, msg: "API Key 未配置" }));
      return;
    }
    try {
      const resp = await fetch("https://api.nuwaai.com/web/apiKey/auth", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ secretKey: nuwaConfig.apiKey }),
      });
      const data = await resp.json();
      res.writeHead(200, { "Content-Type": "application/json" });
      res.end(JSON.stringify(data));
    } catch (e) {
      res.writeHead(500, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ code: -1, msg: e.message }));
    }
    return;
  }

  // API: Chat with OpenClaw (non-streaming fallback)
  if (req.url === "/api/chat" && req.method === "POST") {
    let body = "";
    for await (const chunk of req) body += chunk;
    try {
      const { message } = JSON.parse(body);
      const headers = { "Content-Type": "application/json" };
      if (OPENCLAW_TOKEN) headers["Authorization"] = `Bearer ${OPENCLAW_TOKEN}`;
      headers["x-openclaw-session-key"] = "agent:main:nuwa-human";

      const resp = await fetch(`${OPENCLAW_GATEWAY}/v1/chat/completions`, {
        method: "POST",
        headers,
        body: JSON.stringify({
          model: "openclaw:main",
          messages: [{ role: "user", content: message }],
        }),
      });
      const data = await resp.json();
      const reply = data.choices?.[0]?.message?.content || data.error?.message || "...";
      res.writeHead(200, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ reply }));
    } catch (e) {
      res.writeHead(500, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ error: e.message }));
    }
    return;
  }

  // API: Chat with OpenClaw (streaming SSE)
  if (req.url === "/api/chat/stream" && req.method === "POST") {
    let body = "";
    for await (const chunk of req) body += chunk;
    try {
      const { message } = JSON.parse(body);
      const headers = { "Content-Type": "application/json" };
      if (OPENCLAW_TOKEN) headers["Authorization"] = `Bearer ${OPENCLAW_TOKEN}`;
      headers["x-openclaw-session-key"] = "agent:main:nuwa-human";

      const resp = await fetch(`${OPENCLAW_GATEWAY}/v1/chat/completions`, {
        method: "POST",
        headers,
        body: JSON.stringify({
          model: "openclaw:main",
          messages: [{ role: "user", content: message }],
          stream: true,
        }),
      });

      if (!resp.ok) {
        const errText = await resp.text();
        res.writeHead(resp.status, { "Content-Type": "text/event-stream", "Cache-Control": "no-cache", "Connection": "keep-alive" });
        res.write(`data: ${JSON.stringify({ error: errText })}\n\n`);
        res.end();
        return;
      }

      res.writeHead(200, {
        "Content-Type": "text/event-stream",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "X-Accel-Buffering": "no",
      });

      const reader = resp.body.getReader();
      const decoder = new TextDecoder();
      let buffer = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        buffer += decoder.decode(value, { stream: true });

        const lines = buffer.split("\n");
        buffer = lines.pop() || "";

        for (const line of lines) {
          const trimmed = line.trim();
          if (!trimmed || !trimmed.startsWith("data: ")) continue;
          const data = trimmed.slice(6);
          if (data === "[DONE]") {
            res.write("data: [DONE]\n\n");
            continue;
          }
          try {
            const parsed = JSON.parse(data);
            const content = parsed.choices?.[0]?.delta?.content;
            if (content) {
              res.write(`data: ${JSON.stringify({ content })}\n\n`);
            }
          } catch {}
        }
      }
      res.end();
    } catch (e) {
      if (!res.headersSent) {
        res.writeHead(500, { "Content-Type": "text/event-stream" });
      }
      res.write(`data: ${JSON.stringify({ error: e.message })}\n\n`);
      res.end();
    }
    return;
  }

  // Static files
  let filePath = req.url === "/" ? "/index.html" : req.url.split("?")[0];
  const publicDir = path.join(__dirname, "public");
  filePath = path.resolve(publicDir, "." + filePath);

  // Path traversal protection
  if (!filePath.startsWith(publicDir)) {
    res.writeHead(403);
    res.end("Forbidden");
    return;
  }

  const ext = path.extname(filePath);
  const contentType = mimeTypes[ext] || "application/octet-stream";

  try {
    const content = fs.readFileSync(filePath);
    res.writeHead(200, { "Content-Type": contentType });
    res.end(content);
  } catch {
    res.writeHead(404);
    res.end("Not found");
  }
});

const BIND = process.env.NUWA_BIND || "127.0.0.1";
server.listen(PORT, BIND, () => {
  console.log(`\n🦞 Claw Body — 龙虾真身已启动`);
  console.log(`   打开浏览器: http://localhost:${PORT}`);
  console.log(`   OpenClaw Gateway: ${OPENCLAW_GATEWAY}`);
  if (nuwaConfig.avatarId) {
    console.log(`   形象 ID: ${nuwaConfig.avatarId}`);
  } else {
    console.log(`   ⚠️  首次使用，请在网页中配置你的龙虾形象`);
  }
  console.log();
});

// Graceful shutdown
function shutdown() {
  console.log("\n🦞 Claw Body — 正在关闭...");
  server.close(() => process.exit(0));
  setTimeout(() => process.exit(1), 3000);
}
process.on("SIGTERM", shutdown);
process.on("SIGINT", shutdown);
