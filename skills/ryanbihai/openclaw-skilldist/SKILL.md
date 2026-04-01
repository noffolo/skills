# Skill Publisher - 多平台 Skill 发布助手

> **一句话发布** → `python scripts/publish.sh <slug>`
> 
> 自动发布到 ClawHub、GitHub，为 COZE/元器/百炼 生成提交文本

---

## 🚀 3 步完成发布

### 第 1 步：配置 Token（仅首次需要）

```bash
python scripts/setup_tokens.py
```

按提示输入各平台 Token（已配置的会自动跳过）

### 第 2 步：发布 Skill

```bash
# 发布单个 Skill（推荐）
python scripts/publish.sh my-skill

# 或最简命令
./scripts/quick-publish.sh my-skill
```

**自动完成：**
- ✅ ClawHub（自动）
- ✅ GitHub（自动）
- 📝 SkillzWave/COZE/元器/百炼（生成提交文本）

### 第 3 步：复制手动平台文本

脚本会生成各平台的提交文本，直接复制使用即可。

---

## ✨ 功能特性

| 功能 | 说明 |
|------|------|
| 🔐 **安全 Token 管理** | 本地 `.env` 存储，永不上传 |
| ⚡ **一键发布** | `publish.sh <slug>` 自动处理一切 |
| 🔍 **智能检测** | 只发布已配置 Token 的平台 |
| 📝 **提交文本生成** | 为手动平台生成标准文本 |
| 📊 **状态查看** | `check_status.py` 查看所有平台状态 |

---

## 📁 目录结构

```
skill-publisher/
├── SKILL.md                    ← 你在这里
├── _meta.json
├── .env.example               ← Token 模板
├── scripts/
│   ├── publish.sh             ← ⭐ 主发布脚本
│   ├── quick-publish.sh        ← 最简发布命令
│   ├── setup_tokens.py        ← Token 配置向导
│   ├── check_status.py        ← 平台状态查看
│   └── gen_submission.py      ← 生成手动提交文本
├── docs/
│   └── PLATFORM_RESEARCH.md   ← 平台调研报告
└── data/
    └── platforms.json         ← 平台配置
```

---

## 🎯 快速参考

| 操作 | 命令 |
|------|------|
| **发布 Skill** | `python scripts/publish.sh <slug>` |
| **配置 Token** | `python scripts/setup_tokens.py` |
| **查看状态** | `python scripts/check_status.py all` |
| **生成提交文本** | `python scripts/gen_submission.py <slug>` |
| **查看帮助** | `cat scripts/publish.sh` |

---

## 🔐 Token 安全说明

**安全原则：**
1. Token 只存储在本地 `.env` 文件
2. `.env` 已在 `.gitignore` 中，绝不会提交到 GitHub
3. 所有 API 调用使用 HTTPS 加密传输
4. 按需授权（只申请必要权限）

**Token 获取：**

| 平台 | Token 名称 | 获取地址 |
|------|-----------|---------|
| GitHub | `GITHUB_TOKEN` | https://github.com/settings/tokens |
| ClawHub | `CLAWHUB_TOKEN` | https://clawhub.ai |
| COZE | `COZE_TOKEN` | https://www.coze.cn/settings/api |
| 元器 | `YUANQI_TOKEN` | https://yuanqi.tencent.com |
| 百炼 | `BAILIAN_TOKEN` | https://bailian.console.aliyun.com |

---

## 🏗️ 平台自动化程度

| 平台 | 自动化 | 说明 |
|------|--------|------|
| 🌐 **ClawHub** | ✅ 全自动 | `clawhub publish` |
| 💻 **GitHub** | ✅ 全自动 | Git push |
| 🟢 **SkillsMP** | ✅ 全自动 | GitHub 同步 |
| 🌊 **SkillzWave** | ⏳ 手动 | 生成提交文本 |
| 🤖 **COZE** | ⚠️ 部分 | API + 手动审核 |
| 🟡 **元器** | ⏳ 手动 | 手动提交 |
| 🔵 **百炼** | ⏳ 手动 | 手动提交 |

---

## 🔧 故障排除

### Token 无效
```bash
Error: GitHub API token invalid
```
→ 在 https://github.com/settings/tokens 重新生成 Token

### Skill 目录不存在
```bash
Error: Skill 目录不存在
```
→ 确认 slug 正确：`ls /home/node/.openclaw/workspace/skills/`

### ClawHub 发布失败
```bash
Error: Published failed
```
→ 检查 `CLAWHUB_TOKEN` 是否正确

### 推送被拒绝
```bash
error: src refspec main does not match any
```
→ 确认 Git 已初始化并有提交

---

## 📖 详细文档

- [平台调研报告](./docs/PLATFORM_RESEARCH.md) - 各平台 API 自动化可能性分析
- [ClawHub 官方文档](https://docs.clawhub.ai)
- [GitHub API 文档](https://docs.github.com/rest)

---

*维护者：Ryan BihAI  
版本：2.3.0*
