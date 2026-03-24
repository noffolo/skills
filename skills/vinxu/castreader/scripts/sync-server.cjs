#!/usr/bin/env node
/**
 * CastReader Library Sync Server
 * Receives book content from the Chrome Extension and writes to ~/castreader-library/
 * Port: 18790 (localhost only)
 */

const http = require('http');
const fs = require('fs');
const path = require('path');
const os = require('os');

const PORT = parseInt(process.env.SYNC_SERVER_PORT || '18790', 10);
const LIBRARY_ROOT = process.env.LIBRARY_ROOT || path.join(os.homedir(), 'castreader-library');

// Ensure library root exists
fs.mkdirSync(path.join(LIBRARY_ROOT, 'books'), { recursive: true });

function safePath(requestPath) {
  const resolved = path.resolve(LIBRARY_ROOT, requestPath);
  if (!resolved.startsWith(LIBRARY_ROOT)) {
    return null;
  }
  return resolved;
}

function readBody(req) {
  return new Promise((resolve, reject) => {
    const chunks = [];
    req.on('data', (chunk) => chunks.push(chunk));
    req.on('end', () => {
      try {
        resolve(JSON.parse(Buffer.concat(chunks).toString()));
      } catch (e) {
        reject(new Error('Invalid JSON'));
      }
    });
    req.on('error', reject);
  });
}

function respond(res, status, data) {
  res.writeHead(status, {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
  });
  res.end(JSON.stringify(data));
}

const server = http.createServer(async (req, res) => {
  // CORS preflight
  if (req.method === 'OPTIONS') {
    respond(res, 200, { ok: true });
    return;
  }

  const url = new URL(req.url, `http://localhost:${PORT}`);

  try {
    if (req.method === 'GET' && url.pathname === '/health') {
      respond(res, 200, { status: 'ok', libraryRoot: LIBRARY_ROOT });
      return;
    }

    if (req.method === 'POST' && url.pathname === '/save') {
      const body = await readBody(req);
      if (!body.path || body.content === undefined) {
        respond(res, 400, { error: 'Missing path or content' });
        return;
      }

      const filePath = safePath(body.path);
      if (!filePath) {
        respond(res, 403, { error: 'Path outside library root' });
        return;
      }

      fs.mkdirSync(path.dirname(filePath), { recursive: true });
      fs.writeFileSync(filePath, body.content, 'utf-8');
      console.log(`[save] ${body.path} (${body.content.length} chars)`);
      respond(res, 200, { ok: true, path: body.path });
      return;
    }

    if (req.method === 'POST' && url.pathname === '/read') {
      const body = await readBody(req);
      if (!body.path) {
        respond(res, 400, { error: 'Missing path' });
        return;
      }

      const filePath = safePath(body.path);
      if (!filePath) {
        respond(res, 403, { error: 'Path outside library root' });
        return;
      }

      if (!fs.existsSync(filePath)) {
        respond(res, 404, { error: 'File not found' });
        return;
      }

      const content = fs.readFileSync(filePath, 'utf-8');
      respond(res, 200, { ok: true, content });
      return;
    }

    if (req.method === 'POST' && url.pathname === '/save-batch') {
      const body = await readBody(req);
      if (!Array.isArray(body.files)) {
        respond(res, 400, { error: 'Missing files array' });
        return;
      }

      let saved = 0;
      for (const file of body.files) {
        const filePath = safePath(file.path);
        if (!filePath) continue;
        fs.mkdirSync(path.dirname(filePath), { recursive: true });
        fs.writeFileSync(filePath, file.content, 'utf-8');
        saved++;
      }
      console.log(`[save-batch] ${saved}/${body.files.length} files`);
      respond(res, 200, { ok: true, saved });
      return;
    }

    if (req.method === 'POST' && url.pathname === '/delete-glob') {
      const body = await readBody(req);
      if (!body.dir || !body.pattern) {
        respond(res, 400, { error: 'Missing dir or pattern' });
        return;
      }

      const dirPath = safePath(body.dir);
      if (!dirPath) {
        respond(res, 403, { error: 'Path outside library root' });
        return;
      }

      if (!fs.existsSync(dirPath)) {
        respond(res, 200, { ok: true, deleted: 0 });
        return;
      }

      // Simple glob: only supports "chapter-*.md" style patterns
      const re = new RegExp('^' + body.pattern.replace(/\*/g, '.*') + '$');
      const entries = fs.readdirSync(dirPath);
      let deleted = 0;
      for (const entry of entries) {
        if (re.test(entry)) {
          fs.unlinkSync(path.join(dirPath, entry));
          deleted++;
        }
      }
      console.log(`[delete-glob] ${body.dir}/${body.pattern} → ${deleted} files`);
      respond(res, 200, { ok: true, deleted });
      return;
    }

    if (req.method === 'POST' && url.pathname === '/list-books') {
      const booksDir = path.join(LIBRARY_ROOT, 'books');
      if (!fs.existsSync(booksDir)) {
        respond(res, 200, { books: [] });
        return;
      }

      const entries = fs.readdirSync(booksDir, { withFileTypes: true });
      const books = [];
      for (const entry of entries) {
        if (!entry.isDirectory()) continue;
        const metaPath = path.join(booksDir, entry.name, 'meta.json');
        if (fs.existsSync(metaPath)) {
          try {
            const meta = JSON.parse(fs.readFileSync(metaPath, 'utf-8'));
            books.push({ id: entry.name, ...meta });
          } catch { /* skip corrupted meta */ }
        }
      }
      respond(res, 200, { books });
      return;
    }

    respond(res, 404, { error: 'Not found' });
  } catch (err) {
    console.error(`[error] ${req.method} ${url.pathname}:`, err.message);
    respond(res, 500, { error: err.message });
  }
});

// Increase max payload size (default ~80KB is too small for book batches)
server.maxHeaderSize = 16 * 1024;
server.setTimeout(300000); // 5 min timeout for large saves

// Prevent crash on uncaught errors
process.on('uncaughtException', (err) => {
  console.error('[sync-server] Uncaught exception:', err.message);
});
process.on('unhandledRejection', (err) => {
  console.error('[sync-server] Unhandled rejection:', err);
});

server.listen(PORT, '127.0.0.1', () => {
  console.log(`[CastReader Library Sync] Listening on http://127.0.0.1:${PORT}`);
  console.log(`[CastReader Library Sync] Library root: ${LIBRARY_ROOT}`);
});
