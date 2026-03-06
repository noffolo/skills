---
slug: strike163163-my-browser-control
name: 我的浏览器控制工具
version: 0.1.2
author: strike163163
description: 支持传参的macOS浏览器自动化工具，可打开任意指定网址，支持Safari/Chrome。
tags:
  - browser-automation
  - macos
  - python
---

# 我的浏览器控制工具
本工具支持接收网址参数，可一键打开任意指定网址，适配ClawHub Agent调用。

## 核心功能
- 调用open_website(url)函数，传入任意网址即可打开；
- 支持终端传参（python3 open_website.py 网址）；
- 兼容Safari/Chrome浏览器。

## 使用示例
1. 终端运行：python3 open_website.py https://www.baidu.com
2. Agent调用：发送“打开百度”指令，自动触发函数打开网页。