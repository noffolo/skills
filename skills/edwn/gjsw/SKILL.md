---
name: gjsw
description: 国家税务总局 12366 纳税服务平台自动登录技能。当用户要求登录12366、国家税务总局、纳税服务平台时触发，会要求用户输入账号密码，然后自动打开Chrome浏览器完成登录。
user-invocable: true
metadata:
  openclaw:
    emoji: "🔐"
    requires:
      bins:
        - python3
        - google-chrome
      env: []  # 移除环境变量依赖，改为交互式输入
    interactive: true  # 标记为交互式技能
    interactive_prompts:
      username: "请输入您的12366登录账号（手机号/用户名）："
      password: "请输入您的登录密码（输入时不可见）："
    login_url: "https://12366.chinatax.gov.cn/usercenter/login/page"
---

# 国家税务总局 12366 纳税服务平台自动登录

该技能使用 Playwright + ddddocr 实现自动识别验证码并登录国家税务总局 12366 纳税服务平台。登录成功后，Chrome 浏览器将保持打开状态，并保留登录会话。

## 使用方式

1. **触发技能**：用户说"登录12366"、"打开国家税务总局"、"登录纳税服务平台"等
2. **输入凭证**：OpenClaw 会询问账号和密码
3. **自动登录**：自动打开 Chrome 浏览器，识别验证码并完成登录

## 功能特性

- **交互式登录**：无需预设环境变量，按需输入账号密码
- **自动登录**：通过用户名、密码和图形验证码自动登录
- **验证码识别**：使用 OCR 自动识别图形验证码
- **会话持久化**：登录信息保存在 `./chrome_profile` 目录，下次运行无需重复登录
- **多平台支持**：在 macOS、Linux、Windows 上均可运行（需安装 Chrome）

## 前置要求

### 1. 安装系统依赖

- **Python 3.8+** 及以下 Python 包：
  ```bash
  pip install playwright ddddocr
  playwright install chromium