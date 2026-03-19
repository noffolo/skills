# 微信公众号文章推送技能

[![ClawHub](https://img.shields.io/badge/ClawHub-wechat--mp--article-push-blue)](https://clawhub.ai/skills/wechat-mp-article-push)

一个强大的微信公众号文章生成与推送技能。支持通过AI生成符合公众号规范的文章,并推送到公众号草稿箱或直接发布，兼容其它SKILL生成的文章进行推送。无需泄露公众号密钥，无需配置公众号白名单。

## ✨ 功能特性 
 
- 🔒 **安全配置** - 通过在线向导安全配置,无需泄露公众号密钥，无需配置公众号白名单
- 📝 **图文生成** - 按照 design.md 规范自动生成符合公众号格式的 HTML 文章
- 🚀 **快速推送** - 推送文章到公众号，推送成功后有服务通知 

## 📦 快速开始

### 1. 配置公众号

访问配置向导完成公众号配置:

```
https://app.pcloud.ac.cn/design/wechat-mp-article-push.html
```

1. 微信扫码登录
2. 选择要推送的公众号
3. 复制生成的配置文件发给AI

### 2. 保存配置

AI将用户发送的配置保存到技能目录下的 `config.json` 文件中。

### 3. 生成文章

用户发送文章创作要求给AI，AI根据 `design.md` 规范生成 HTML 文件。

### 4. 推送文章

AI调用脚本推送文章到公众号

```bash
cd wechat-mp-article-push
node push-article-https.js 你的文章.html
```

## 📖 详细文档

- **SKILL.md** - 完整技能说明
- **design.md** - 公众号 HTML 文章格式规范
- **config.example.json** - 配置字段说明与示例

## 🎯 使用场景

- 📰 日常公众号文章创作
- 🤖 兼容搭配其它SKILL使用
- 🗓️ 定期内容推送自动化 

## 🔧 配置说明

配置文件 `config.json` 包含以下关键字段:

- `openId` - 微信用户 openId(必填)
- `pushMode` - 推送模式: `default` 或 `custom`
- `accountId` - 公众号账号 ID(custom 模式必填)
 
## 🚨 注意事项

- 未认证公众号只能推送到草稿箱
- 推送前请确保运行了配置向导并复制发给了AI

## 📄 许可证

MIT - 免费使用、修改和分发,无需署名

## 🔗 相关链接

- [ClawHub 技能页面](https://clawhub.ai/skills/wechat-mp-article-push)
- [OpenClaw 官方文档](https://docs.openclaw.ai)

## 👨‍💻 维护者

[@lihengdao](https://clawhub.ai/users/lihengdao)

---

**需要帮助?** 查看 SKILL.md 获取详细使用说明。
