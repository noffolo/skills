# 更新日志

本文档记录 `wechat-mp-article-push` 技能的所有重要变更。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/),
版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

 

## [2.0.X] - 2026-03-19

### 🚀 版本升级

- 版本号升级至 2.0.0
- 移除 package.json 和 .npmignore（脚本零依赖，无需 npm 管理）
- SKILL.md 文件路径表合并至顶部，增加「作用」列
- SKILL.md 向导流程描述更清晰（AI → 用户 → 扫码 → 选择 → 复制）
- SKILL.md 移除底部重复的文件一览表
- README.md 措辞微调（快速推送→一键推送，配置说明细化）
- 2.0.15 支持更好看的公众号生成效果；支持小红书图文卡片；


---

## [1.0.0] - 2026-03-19

### 🎉 首次发布

#### 新增
- ✨ 初始版本发布
- 📝 完整的技能说明文档(SKILL.md)
- 🎨 公众号 HTML 文章格式规范(design.md)
- 🔧 文章推送脚本(push-article-https.js)
- ⚙️ 配置文件示例(config.example.json)
- 📖 README.md 文档
- 📋 CHANGELOG.md 变更日志

#### 功能特性
- 支持通过配置向导配置公众号
- 生成符合公众号规范的 HTML 文章
- 推送文章到公众号


#### 文档
- 详细的配置说明
- HTML 格式规范指南
- 推送接口说明
- 使用示例

---
 
## 版本说明

- **Major (主版本号)**: 不兼容的 API 变更
- **Minor (次版本号)**: 向后兼容的功能新增
- **Patch (修订号)**: 向后兼容的 bug 修复
