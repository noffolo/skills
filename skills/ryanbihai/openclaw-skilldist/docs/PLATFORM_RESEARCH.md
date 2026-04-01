# 平台自动化调研报告（实测版）

> 生成时间：2026-03-31  
> 调研范围：COZE、腾讯元器、阿里百炼、SkillzWave（基于实际 API 测试）

---

## 一、平台概览（实测结果）

| 平台 | 自动化可能性 | API 开放程度 | 审核机制 | 推荐方案 |
|------|-------------|-------------|---------|---------|
| **ClawHub** | ✅ 全自动 | 高（官方 CLI） | 无 | 直接使用 |
| **GitHub** | ✅ 全自动 | 高（Git API） | 无 | 直接使用 |
| **SkillsMP** | ✅ 全自动 | 高（GitHub 同步） | 无 | 直接使用 |
| **SkillzWave** | ❌ 不可行 | 低（仅手动页面） | 人工审核 | 生成提交文本 |
| **COZE** | ⚠️ 部分 | 中（REST API 存在） | 人工审核 | API 创建 Bot + 手动提交市场 |
| **腾讯元器** | ⚠️ 部分 | 中（需进一步测试） | 人工审核 | 生成提交文本 |
| **阿里百炼** | ⚠️ 部分 | 中（需 Token） | 人工审核 | 生成提交文本 |

---

## 二、平台详细分析（实测）

### 2.1 COZE/扣子 🔍

**平台地址：** https://www.coze.cn/store/market/bot

**实测结果：**
- ✅ API 端点确认：`https://api.coze.cn`（可访问）
- ✅ 官方文档：`https://www.coze.cn/docs/developer_guides/api_overview`
- ⚠️ API 路径 `/v2/bots` 不存在，需查阅完整文档确认正确端点
- ⚠️ 发布到商店需要人工审核，无法绕过

**API 自动化能力：**
- 可通过 API 创建/更新 Bot
- 需 Personal Access Token（不是 API Key）
- 无法通过 API 直接提交到商店市场

**所需 Token：**
- `COZE_TOKEN` - 从 https://www.coze.cn/settings/api 获取
- Token 类型：Personal Access Token

**提交方式：**
1. 通过 API 创建 Bot（开发者测试）
2. 手动在 https://www.coze.cn/store/market/bot 提交审核

**难度：** ⭐⭐⭐ 中等

---

### 2.2 腾讯元器 🔍

**平台地址：** https://yuanqi.tencent.com/market

**实测结果：**
- ⚠️ 主站可访问，但 API 文档被屏蔽
- 平台主要面向微信小程序生态
- 智能体发布需要腾讯账号 + 人工审核

**API 自动化能力：**
- 有基础 API 支持（需进一步测试）
- 发布到市场需要手动操作控制台

**所需 Token：**
- `YUANQI_TOKEN` - 腾讯云 API Key

**难度：** ⭐⭐⭐⭐ 较高

---

### 2.3 阿里百炼 🔍

**平台地址：** https://bailian.console.aliyun.com/model-market

**实测结果：**
- ⚠️ 页面访问被拒绝
- 阿里云 AI 服务平台
- 智能体/Dataset 发布需要人工操作

**API 自动化能力：**
- 有阿里云 API 支持（需 Token）
- 智能体发布需要控制台操作

**所需 Token：**
- `BAILIAN_TOKEN` - 阿里云 API Key

**难度：** ⭐⭐⭐⭐ 较高

---

### 2.4 SkillzWave 🔍

**平台地址：** https://skillzwave.ai/submit/

**实测结果：**
- ✅ 主站可访问（44,000+ skills）
- ❌ 未发现公开 API
- ⚠️ 需要 GitHub OAuth 登录
- 提交表单：https://skillzwave.ai/submit/
- GitHub: https://github.com/SpillwaveSolutions
- CLI: `skilz` CLI（安装 via `npm install -g skilz`）

**API 自动化能力：**
- ❌ 无公开 API
- ⚠️ GitHub OAuth 需要浏览器交互
- 只能生成标准提交文本

**提交信息需求：**
- GitHub 仓库 URL
- Skill 描述
- 截图/预览
- 分类标签
- 开发者联系信息

**难度：** ⭐⭐ 较低（但无自动化可能）

---

## 三、自动化架构设计

### 3.1 Token 安全存储

```
用户本地文件系统（绝对不上传）
    │
    ├── skill-publisher/
    │   ├── .env                    ← Token 存储位置（已在 .gitignore）
    │   │   ├── GITHUB_TOKEN=xxx
    │   │   ├── CLAWHUB_TOKEN=xxx
    │   │   ├── COZE_TOKEN=xxx
    │   │   ├── YUANQI_TOKEN=xxx
    │   │   └── BAILIAN_TOKEN=xxx
    │   └── .gitignore             ← 确保 .env 忽略

Token 安全原则：
1. 绝不写入 Git 提交
2. 交互式输入（密码模式）
3. 本地 .env 文件存储
4. 按需授权（只申请必要权限）
```

### 3.2 分层发布策略

```
┌─────────────────────────────────────────┐
│  交互式 Token 配置（setup_tokens.py）     │
│  • 按平台逐一询问 Token                  │
│  • 安全输入（密码模式）                  │
│  • 本地 .env 保存                        │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│  自动发布层（可全自动）                   │
│  ✅ ClawHub  - npx clawhub publish      │
│  ✅ GitHub   - git push                 │
│  ✅ SkillsMP - GitHub 触发同步           │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│  半自动层（API 创建 + 手动提交）         │
│  ⚠️ COZE      - API 创建 Bot            │
│  ⚠️ 腾讯元器  - API 创建技能             │
│  ⚠️ 阿里百炼  - API 调用                │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│  生成提交文本层                          │
│  📝 SkillzWave - 完整提交表单           │
│  📝 COZE       - Bot 配置信息            │
│  📝 腾讯元器   - 技能描述+链接           │
│  📝 阿里百炼   - 智能体信息+链接         │
└─────────────────────────────────────────┘
```

---

## 四、平台 API 自动化可能性总结

| 平台 | API 自动化 | 绕过审核 | 推荐程度 | 说明 |
|------|-----------|---------|---------|------|
| ClawHub | ✅ 完全 | N/A | ⭐⭐⭐⭐⭐ | 官方 CLI 支持 |
| GitHub | ✅ 完全 | N/A | ⭐⭐⭐⭐⭐ | REST/Git API |
| SkillsMP | ✅ 完全 | N/A | ⭐⭐⭐⭐ | GitHub 自动同步 |
| SkillzWave | ❌ 不可能 | ❌ | ⭐⭐ | 无公开 API，只有手动页面 |
| COZE | ⚠️ 部分 | ❌ | ⭐⭐⭐ | API 存在，需手动提交市场 |
| 元器 | ⚠️ 部分 | ❌ | ⭐⭐ | 主要靠手动 |
| 百炼 | ⚠️ 部分 | ❌ | ⭐⭐ | 主要靠手动 |

**结论：**
- **可全自动（3个）：** ClawHub、GitHub、SkillsMP → 直接集成
- **需生成提交文本（4个）：** SkillzWave、COZE、元器、百炼 → 生成标准文本 + 链接

---

## 五、Token 获取指南

### GitHub
1. https://github.com/settings/tokens
2. Generate new token (classic)
3. 勾选 `repo` 权限
4. 复制 Token

### ClawHub
1. https://clawhub.ai
2. 登录 → 个人设置
3. 复制 API Token

### COZE/扣子
1. https://www.coze.cn/settings/api
2. 需申请开发者权限
3. 创建 Personal Access Token

### 腾讯元器
1. https://yuanqi.tencent.com
2. 登录腾讯账号
3. 个人中心 → API 密钥

### 阿里百炼
1. https://bailian.console.aliyun.com
2. 登录阿里云账号
3. API Key 管理

---

## 六、后续优化建议

### 短期（1 周）
1. 实现 COZE API 集成（创建 Bot）
2. 测试腾讯元器 API
3. 完善提交文本生成器

### 中期（1 个月）
1. 研究 SkillzWave 是否有隐藏 API
2. 申请 COZE 开发者认证
3. 实现阿里百炼 API 集成

### 长期（3 个月）
1. 争取获得各平台官方合作
2. 实现完整的端到端自动化
3. 考虑构建统一的 Skill 发布标准

---

*本报告基于 2026-03-31 的实测调研，各平台政策可能随时变化。*
