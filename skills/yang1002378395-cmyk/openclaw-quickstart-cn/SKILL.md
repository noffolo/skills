# OpenClaw 快速启动指南

中文用户 5 分钟上手 OpenClaw 的完整指南。

## 何时使用

- 刚安装 OpenClaw，不知道从哪里开始
- 想快速配置国产 AI 模型（DeepSeek/智谱/通义）
- 需要一个清晰的入门流程

## 使用方法

1. 确认 OpenClaw 已安装：`openclaw --version`
2. 按下面的步骤依次执行

## 步骤 1：检查环境

```bash
openclaw status
```

如果显示 Gateway 未运行，执行：

```bash
openclaw gateway start
```

## 步骤 2：配置 AI 模型

OpenClaw 支持多种 AI 模型。推荐中文用户使用国产模型：

### DeepSeek（推荐）

1. 访问 https://platform.deepseek.com 获取 API Key
2. 配置：

```bash
openclaw config set model deepseek-chat
openclaw config set providers.deepseek.apiKey sk-xxxxx
```

### 智谱 GLM

1. 访问 https://open.bigmodel.cn 获取 API Key
2. 配置：

```bash
openclaw config set model glm-4
openclaw config set providers.zhipu.apiKey xxxx.xxxx
```

### 阿里通义

1. 访问 https://dashscope.console.aliyun.com 获取 API Key
2. 配置：

```bash
openclaw config set model qwen-turbo
openclaw config set providers.dashscope.apiKey sk-xxxxx
```

## 步骤 3：测试连接

```bash
openclaw chat
```

输入任意问题，如果收到回复说明配置成功！

## 步骤 4：连接通讯平台（可选）

### 微信/Telegram/WhatsApp

```bash
openclaw channel add telegram --token YOUR_BOT_TOKEN
```

按提示完成配置。

## 步骤 5：安装 Skills（可选）

Skills 是 OpenClaw 的技能扩展：

```bash
# 搜索 skills
npx clawhub@latest search "关键词"

# 安装 skill
npx clawhub@latest install <skill-name>
```

## 常见问题

### Q: Gateway 启动失败？

检查端口占用：

```bash
lsof -i :3434
```

### Q: AI 模型连接失败？

1. 检查 API Key 是否正确
2. 确认账户有余额
3. 检查网络连接（部分模型需要代理）

### Q: 如何切换模型？

```bash
openclaw config set model <model-name>
```

## 获取帮助

- 文档：https://docs.openclaw.ai
- 社区：https://discord.com/invite/clawd
- GitHub：https://github.com/openclaw/openclaw

---

**需要安装服务？** 搜索 `openclaw-cn-installer` 获取专业安装支持。
