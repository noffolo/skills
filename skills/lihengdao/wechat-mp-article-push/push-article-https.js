#!/usr/bin/env node
/**
 * 推送到公众号。 HTML、config.json 和 此脚本 push-article-https.js 应该在同一个目录。HTML在其他路径时请先复制到本目录。执行时只传 HTML 文件名：
 *
 * 用法：node push-article-https.js <HTML 文件名> 
 * 示例：node push-article-https.js 我的文章.html
 *
 * 标题从 HTML 的 <title>…</title> 取。
 */

const https = require('https');
const http = require('http');
const fs = require('fs');
const path = require('path');
const { URL } = require('url');

const DEFAULT_API = 'https://api.pcloud.ac.cn/openClawService';
const DIR = __dirname;

function readJson(name) {
  const p = path.join(DIR, name);
  if (!fs.existsSync(p)) throw new Error('缺少: ' + p);
  return JSON.parse(fs.readFileSync(p, 'utf8').trim());
}

function titleFromHtml(html) {
  const m = html.match(/<title[^>]*>([\s\S]*?)<\/title>/i);
  const raw = m ? m[1].replace(/<[^>]+>/g, '').trim() : '';
  return raw || '未命名';
}

function postJson(urlStr, body, timeoutMs = 120000) {
  const payload = JSON.stringify(body);
  const u = new URL(urlStr);
  const lib = u.protocol === 'https:' ? https : http;
  const port = u.port || (u.protocol === 'https:' ? 443 : 80);

  return new Promise((resolve, reject) => {
    const req = lib.request(
      {
        hostname: u.hostname,
        port,
        path: u.pathname + u.search,
        method: 'POST',
        headers: {
          'Content-Type': 'application/json; charset=utf-8',
          'Content-Length': Buffer.byteLength(payload, 'utf8'),
        },
      },
      (res) => {
        const chunks = [];
        res.on('data', (c) => chunks.push(c));
        res.on('end', () => {
          const raw = Buffer.concat(chunks).toString('utf8');
          let json;
          try {
            json = JSON.parse(raw);
          } catch (_) {}
          resolve({ statusCode: res.statusCode, raw, json });
        });
      }
    );
    const t = setTimeout(() => req.destroy(new Error('超时')), timeoutMs);
    req.on('error', (e) => {
      clearTimeout(t);
      reject(e);
    });
    req.on('close', () => clearTimeout(t));
    req.write(payload);
    req.end();
  });
}

async function main() {
  const htmlArg = process.argv[2];
  if (!htmlArg || !htmlArg.trim()) {
    throw new Error('请传入 HTML 文件名（与脚本同目录）。例如: node push-article-https.js 我的文章.html');
  }
  // 只从脚本同目录读，只取文件名，避免路径导致失败
  const fileName = path.basename(htmlArg.trim());
  const htmlPath = path.join(DIR, fileName);

  const cfg = readJson('config.json');
  if (!fs.existsSync(htmlPath)) throw new Error('同目录下找不到: ' + fileName + '（请把 HTML 放在脚本所在目录）');
  const content = fs.readFileSync(htmlPath, 'utf8');
  if (!content.trim()) throw new Error('文件为空: ' + htmlPath);

  const title = titleFromHtml(content);
  if (!cfg.openId || String(cfg.openId).includes('XXXX')) {
    throw new Error('config.json 里 openId 无效，请用向导生成的配置');
  }

  const apiBase = cfg.apiBase || DEFAULT_API;
  const body = {
    action: 'sendToWechat',
    openId: cfg.openId,
    title: title.slice(0, 64),
    content,
    sendMode: 'draft',
  };
  if (cfg.pushMode === 'custom' && cfg.accountId != null && cfg.accountId !== '') {
    body.accountId = cfg.accountId;
  }

  console.error('推送中…', apiBase, '| 标题', title.slice(0, 30) + (title.length > 30 ? '…' : ''), '| 正文长度', content.length);
  const res = await postJson(apiBase, body);
  console.log(
    JSON.stringify(
      { ok: res.statusCode >= 200 && res.statusCode < 300, statusCode: res.statusCode, data: res.json !== undefined ? res.json : res.raw },
      null,
      2
    )
  );
  if (res.statusCode < 200 || res.statusCode >= 300) process.exit(1);
}

main().catch((e) => {
  console.error(e.message || e);
  process.exit(1);
});
