---
name: chaoxing
description: 超星学习通自动化 - 登录、查看课程、查看作业。使用 puppeteer-extra + stealth 插件绕过自动化检测。
metadata:
  author: OpenClaw
  version: 1.0.1
  requires: puppeteer-extra, puppeteer-extra-plugin-stealth
---

# 超星学习通自动化 (chaoxing)

登录超星学习通、查看课程列表、查看作业列表及详情。

## 环境准备

```bash
cd ~/.openclaw/workspace
npm install puppeteer-extra puppeteer-extra-plugin-stealth
```

> 需要先在 workspace 下初始化 npm 项目：`npm init -y`

## 核心代码

### 初始化浏览器

```js
const puppeteer = require('puppeteer-extra');
const stealthPlugin = require('puppeteer-extra-plugin-stealth');
puppeteer.use(stealthPlugin());

const browser = await puppeteer.launch({
  headless: true,
  args: [
    '--no-sandbox',
    '--disable-setuid-sandbox',
    '--disable-dev-shm-usage',
    '--no-first-run',
    '--no-zygote',
    '--single-process',
    '--ignore-certificate-errors',
    '--ignore-certificate-errors-spki-list'
  ]
});

const page = await browser.newPage();
await page.setViewport({ width: 1920, height: 1080 });
await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36');
```

### 登录（关键hack）

超星会检测自动化，`page.type()` 会失效，必须用原生 setter：

```js
await page.goto('https://passport2.chaoxing.com/login?fid=&newversion=true&refer=https%3A%2F%2Fi.chaoxing.com', { waitUntil: 'domcontentloaded', timeout: 30000 });
await new Promise(r => setTimeout(r, 3000));

await page.evaluate(() => {
  const cb = document.querySelector('input[type="checkbox"]');
  if (cb && !cb.checked) { cb.checked = true; cb.dispatchEvent(new Event('change',{bubbles:true})); }
});

await page.evaluate(({ phone, pwd }) => {
  const phoneInput = document.getElementById('phone');
  const pwdInput = document.getElementById('pwd');
  const s = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'value').set;
  s.call(phoneInput, phone); phoneInput.dispatchEvent(new Event('input',{bubbles:true}));
  s.call(pwdInput, pwd); pwdInput.dispatchEvent(new Event('input',{bubbles:true}));
}, { phone: 'your phone number', pwd: 'password' });

await new Promise(r => setTimeout(r, 500));
await page.evaluate(() => document.querySelector('.btn-big-blue')?.click());
await new Promise(r => setTimeout(r, 8000)); // 等待登录完成
```

### 进入课程

课程列表在主页面 frame 里：

```js
// 点击"课程" tab
await page.evaluate(() => {
  const allElements = document.querySelectorAll('*');
  for (const el of allElements) {
    if (el.childNodes.length === 1 && el.textContent?.trim() === '课程') {
      el.click();
      break;
    }
  }
});
await new Promise(r => setTimeout(r, 5000));

// 找到课程 frame（含 mycourse/stu 的）
const courseFrame = page.frames().find(f => f.url().includes('mycourse/stu'));

// 从 frame 内提取课程链接（课程名完全匹配）
const courseLink = await courseFrame.evaluate((targetName) => {
  const allEls = document.querySelectorAll('a');
  for (const el of allEls) {
    if (el.textContent?.trim() === targetName) {
      return el.href;
    }
  }
  return null;
}, '目标课程名');
```

### 查看作业

**方式一（推荐）：** 直接访问作业列表 URL（需要先登录并访问课程页建立会话）

每个课程的作业列表 URL 格式：
```
https://mooc1.chaoxing.com/mooc2/work/list?courseId=...&classId=...&cpi=...&enc=...
```

`enc` 参数从课程 frame 内的元素 `data` 属性获取。

```js
// 在作业 frame 里提取所有作业链接（从 data 属性）
const taskData = await hwFrame.evaluate(() => {
  const results = [];
  // 找所有 data 属性含 chaoxing work URL 的元素
  const els = document.querySelectorAll('[data]');
  els.forEach(el => {
    const data = el.getAttribute('data');
    if (data && data.includes('chaoxing.com') && data.includes('/work/')) {
      results.push({
        url: data,                              // 作业详情 URL
        text: el.textContent?.trim().replace(/\s+/g, ' ').substring(0, 60)
      });
    }
  });
  return results;
});
```

**方式二：** 先点"作业"tab，再在作业 frame 里提取

```js
// 点击作业 tab（在 courseFrame 里）
await courseFrame.evaluate(() => {
  const links = Array.from(document.querySelectorAll('a'));
  const hwLink = links.find(l => l.textContent?.trim() === '作业');
  if (hwLink) hwLink.click();
});
await new Promise(r => setTimeout(r, 5000));

// 找作业 frame
const hwFrame = page.frames().find(f => f.url().includes('work/list'));
```

### 判断作业是否已提交

进入作业详情页后，检查页面文本：

```js
await page.goto(taskUrl, { waitUntil: 'domcontentloaded', timeout: 20000 });
await new Promise(r => setTimeout(r, 3000));

const pageText = await page.evaluate(() => document.body.innerText);
const isSubmitted = pageText.includes('My Answer') || pageText.includes('Answer details');
// 未提交页面包含 "Save" / "Submit" / "To be Submitted"
```

### ⚠️ 截止时间字段说明（重要）

超星作业详情页的时间格式为：

```
Time:03-27 15:18to04-01 14:30
```

格式是 `Time:开始时间to截止时间`，两者紧挨着没有空格。

**正确提取截止时间：**

```js
// 格式：Time:03-27 15:18to04-01 14:30
// 开始时间 to 截止时间（无空格），提取 to 后面的 MM-DD HH:mm
const deadlineMatch = pageText.match(/Time:(\d{2}-\d{2} \d{2}:\d{2})to(\d{2}-\d{2} \d{2}:\d{2})/);
if (deadlineMatch) {
  const deadlineStr = deadlineMatch[2]; // "04-01 14:30"
}
```

**已知的坑：**
- `Time:` 行包含开始和截止时间，用 `to` 分隔，开始时间在 `to` 前，截止时间在 `to` 后
- 不要尝试从 `Time:` 以外的地方找截止时间

### 截图并发送

```js
await page.screenshot({ path: '/home/xiaochang/.openclaw/workspace/chaoxing-screenshot.png', timeout: 60000 });
console.log('Current URL:', page.url());
console.log('Page text:', pageText.substring(0, 3000));
await browser.close();
```

## 已知问题

- 超星登录页会检测 `webdriver` 属性，stealth 插件用于绕过
- 如果 `page.type()` 后值被清空，改用原生 setter + dispatchEvent
- **重要：** `goTask(this)` 不带 URL 参数，作业 URL 存储在祖先元素的 `data` 属性里，不要尝试从 `onclick` 参数提取 URL
- **重要：** 不要依赖"作业名称"等特定文字匹配作业列表，用 `data` 属性含 `chaoxing.com` + `/work/` 来找作业链接
- 截图超时问题：设置 `protocolTimeout: 120000`
- 作业列表 page 可能需要等待 5-6 秒才能完整渲染

## 参数速查

| 参数 | 值 |
|------|-----|
| browser.headless | true |
| userAgent | Chrome 120 on Windows 10 |
| 登录页 | `passport2.chaoxing.com/login` |
| 课程 frame | 含 `mycourse/stu` 的 frame |
| 作业列表 URL | `https://mooc1.chaoxing.com/mooc2/work/list?courseId=...&classId=...&cpi=...&enc=...` |
| 作业链接提取 | 找 `[data]` 属性含 `chaoxing.com` 且含 `/work/` 的元素 |
| 提交判断 | 含 `My Answer` / `Answer details` → 已提交 |