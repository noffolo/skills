---
name: wechat-mp-xk
description: 微信公众号发布工具 - 安全版，支持 Knowledge-Base 主题、分步流程、一键发布
version: 1.2.0
author: 九章快手团队
license: MIT
tags:
  - wechat
  - mp
  - publish
  - markdown
  - knowledge-base
  - security
metadata:
  openclaw:
    emoji: "📱"
    category: social
---

# 微信公众号发布工具 - wechat-mp-xk

**安全版 - 一键将 Markdown 文章发布到微信公众号草稿箱**

## ⚠️ 配置提示

**重要：** 本工具使用环境变量管理敏感信息，请勿在代码中硬编码 AppID/Secret！

## ✨ 功能特点

- 🔒 **安全配置** - 环境变量管理敏感信息
- 📱 **一键发布** - Markdown → 公众号草稿箱
- 🎨 **Knowledge-Base 主题** - 简约专业排版
- 🔧 **分步流程** - 灵活控制每个环节
- 🖼️ **自动图片** - 自动上传封面图
- 📝 **Front Matter** - 支持元数据配置

## 🚀 快速开始

### 安装

```bash
# 通过 ClawHub 安装
clawhub install wechat-mp-xk

# 或从 GitHub 克隆
git clone https://github.com/xingkongqy/wechat-mp-xk.git
cd wechat-mp-xk
```

### 配置（重要！）

**方式 1：环境变量（推荐）**

```bash
# 临时配置（当前终端有效）
export WX_APPID="your_appid"
export WX_SECRET="your_secret"

# 永久配置（添加到 ~/.bashrc）
echo 'export WX_APPID="your_appid"' >> ~/.bashrc
echo 'export WX_SECRET="your_secret"' >> ~/.bashrc
source ~/.bashrc
```

**方式 2：.env 文件**

```bash
# 复制示例文件
cp .env.example .env

# 编辑 .env 文件，填入真实值
# ⚠️ 不要将 .env 提交到 Git！
```

### 一键发布

```bash
python3 wxgzh_step_by_step.py article article.md \
  --cover cover.jpg \
  --title "文章标题" \
  --author "作者名"
```

## 📋 分步流程

### Step 1: Markdown 转 HTML

```bash
python3 wxgzh_step_by_step.py md2html article.md --output-dir .wxgzh
```

### Step 2: 修复 HTML

```bash
python3 wxgzh_step_by_step.py fix .wxgzh/article.html
```

### Step 3: 上传封面图

```bash
python3 wxgzh_step_by_step.py cover \
  --cover cover.jpg \
  --output .wxgzh/cover.json
```

### Step 4: 发布到草稿箱

```bash
python3 wxgzh_step_by_step.py publish \
  --article .wxgzh/article.html \
  --cover cover.jpg \
  --title "文章标题"
```

## 🎨 Knowledge-Base 主题

| 元素 | 样式 |
|------|------|
| **一级标题** | 28px，底部细线分割 |
| **二级标题** | 22px，浅灰背景条 |
| **三级标题** | 18px，底部奶黄色高亮 |
| **正文** | 16px，行距 1.75 |
| **加粗** | 黄色高光笔效果 |
| **引用块** | 浅灰背景，左侧边框 |
| **表格** | 数据库风格 |

## 🔒 安全最佳实践

### ❌ 不要

- 在代码中硬编码 AppID/Secret
- 将 .env 文件提交到 Git
- 在日志中打印敏感信息
- 通过 URL 传递敏感参数

### ✅ 要

- 使用环境变量
- 使用密钥管理服务
- 定期轮换密钥（90 天）
- 限制文件权限（chmod 600）

## 📁 文件结构

```
wechat-mp-xk/
├── wxgzh_step_by_step.py    # 主程序（分步流程）
├── publish_kb_theme.py       # Knowledge-Base 主题版
├── wechat_mp.py              # 核心 API 模块
├── wechat_style_template.py  # 排版模板
├── README.md                 # 使用文档
├── SECURITY.md               # 安全说明
├── .env.example              # 环境变量示例
├── .gitignore                # Git 忽略配置
└── tests/
    └── test_publish.py       # 测试用例
```

## ⚠️ 注意事项

1. **IP 白名单** - 服务器 IP 需在公众号后台配置
2. **作者名限制** - 最多 20 字节（中文约 6-7 字）
3. **标题限制** - 最多 64 字节
4. **Token 缓存** - 自动缓存到 /tmp/wechat_token.json

## 📝 使用示例

### 示例 1：一键发布

```bash
# 配置环境变量
export WX_APPID="your_appid"
export WX_SECRET="your_secret"

# 发布文章
python3 wxgzh_step_by_step.py article article.md \
  --cover cover.jpg \
  --title "文章标题"
```

### 示例 2：分步发布

```bash
# Step 1: 转换
python3 wxgzh_step_by_step.py md2html article.md -o .wxgzh

# Step 2: 修复
python3 wxgzh_step_by_step.py fix .wxgzh/article.html

# Step 3: 封面
python3 wxgzh_step_by_step.py cover --cover cover.jpg -o .wxgzh/cover.json

# Step 4: 发布
python3 wxgzh_step_by_step.py publish --article .wxgzh/article.html --cover cover.jpg
```

## 🧪 测试

```bash
# 运行测试
python3 -m pytest tests/
```

## 📄 License

MIT License

Copyright (c) 2026 九章快手团队

---

**版本：** v1.1.0  
**创建时间：** 2026-03-20  
**作者：** 九章快手团队
