---
name: wechat-fetch
description: |
  微信公众号文章抓取工具。使用 OpenClaw 持久化浏览器上下文，复用已登录 Cookie，支持无头模式，稳定可靠。
author: 小明
version: 2.0.1
keywords:
  - wechat
  - 微信
  - article
  - 文章
  - 抓取
  - scraper
  - mp.weixin.qq.com
  - markdown
  - playwright
  - persistent-context
requires:
  bins: playwright
---

# WeChat Fetch - 微信文章抓取工具

使用 Playwright 持久化浏览器上下文抓取微信公众号文章，自动复用已登录 Cookie，无需每次扫码登录。

## 特性

- ✅ **稳定可靠** - 使用真实浏览器登录态，不会被反爬拦截
- ✅ **无头模式** - 可以在后台运行，无需图形界面
- ✅ **自动复用 Cookie** - 复用 OpenClaw 浏览器的已登录会话
- ✅ **支持多种格式** - Markdown/HTML/JSON/TXT
- ✅ **Cookie 自动监控** - 定时检查 Cookie 状态，过期自动提醒

## 使用方法

### 基本用法

```bash
python3 scripts/wechat_fetch.py "https://mp.weixin.qq.com/s/xxxxx" -o ./article.md
```

### 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `url` | 微信文章 URL（必需） | - |
| `-o, --output` | 输出文件路径 | - |
| `-t, --timeout` | 超时时间（秒） | 30 |

## Cookie 管理

### 首次登录

使用 `headless=False` 打开浏览器，访问微信文章并扫码登录。

### Cookie 监控

```bash
# 手动检查
python3 scripts/wechat_cookie_monitor.py --check

# 定时任务（每 12 小时）
0 */12 * * * python3 scripts/wechat_cookie_monitor.py --check
```

### Cookie 有效期

- **有效期**: 约 4 天
- **检查频率**: 每 12 小时
- **预警时间**: 剩余 1 天
- **过期处理**: 扫码登录更新

## 更新日志

### v2.0.1 (2026-03-20)
- ✅ 修复 SKILL.md，移除私有仓库链接
- ✅ 使用持久化浏览器上下文
- ✅ 复用已登录 Cookie
- ✅ 添加 Cookie 自动监控
- ✅ 支持无头模式

## 相关资源

- [Cookie 监控文档](COOKIE_MONITOR_README.md)
- [Playwright 文档](https://playwright.dev/python/)

## 许可证

MIT License
