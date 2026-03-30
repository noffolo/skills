---
name: code-quality-system
description: 完整的代码质量分析系统，包含前后端服务和数据库。一键安装、简单配置即可使用。支持周/月维度分析、AI代码审查、Teams消息通知、邮件报告等功能。
version: 1.0.1
author: OpenClaw
---

# 代码质量分析系统

完整的代码质量分析解决方案，开箱即用。

## 一、快速开始

### 1. 安装技能

```bash
clawhub install code-quality-system
```

### 2. 让 AI 助手帮你初始化

```
请帮我初始化代码质量分析系统
```

AI 助手会自动：
1. 解压前后端代码（backend.zip、frontend.zip）
2. 检查环境（Node.js、PostgreSQL）
3. 安装依赖
4. 初始化数据库
5. 询问配置信息
6. 启动服务

### 3. 你只需要提供三个配置

| 配置项 | 说明 | 示例 |
|--------|------|------|
| 代码仓库目录 | 所有项目已拉取完成的根目录 | `/Users/xxx/projects/` |
| Teams 配置 | Webhook 地址（含 token）和 secret | 在 Teams 群里创建机器人获取 |
| SMTP 配置 | 邮箱发送配置 | QQ邮箱、企业邮箱等 |

### 4. 访问系统

- 前端界面：http://localhost:5173
- 后端 API：http://localhost:3000/api/v1

---

## 二、初始化详细步骤

### 2.1 解压代码

```bash
cd ~/.openclaw/skills/code-quality-system
unzip backend.zip
unzip frontend.zip
```

### 2.2 安装依赖

```bash
cd backend && npm install
cd ../frontend && npm install
```

### 2.3 配置数据库

1. 创建 PostgreSQL 数据库：
```bash
createdb code_quality
```

2. 创建后端环境变量文件 `backend/.env`：
```env
DATABASE_URL="postgresql://postgres:postgres@localhost:5432/code_quality?schema=public"
PORT=3000
NODE_ENV=development
JWT_SECRET=your-secret-key
```

3. 初始化数据库：
```bash
cd backend
npx prisma generate
npx prisma migrate deploy
```

### 2.4 创建主配置文件

创建 `config.json`：
```json
{
  "codebaseDir": "/path/to/your/codebase",
  "teams": {
    "webhookUrl": "https://your-teams-server.com/api/robot/send?access_token=xxx",
    "secret": "your-teams-secret"
  },
  "smtp": {
    "host": "smtp.qq.com",
    "port": 465,
    "secure": true,
    "user": "your-email@qq.com",
    "pass": "your-auth-code",
    "fromName": "代码质量分析助手"
  },
  "emailRecipients": ["recipient@example.com"]
}
```

### 2.5 创建前端环境变量

创建 `frontend/.env`：
```env
VITE_API_BASE_URL=http://localhost:3000/api/v1
```

### 2.6 启动服务

```bash
# 启动后端
cd backend && npm run start:dev

# 启动前端（新终端）
cd frontend && npm run dev
```

---

## 三、配置说明

### 3.1 Teams 配置获取方式

1. 在 360Teams 群里添加"群预警机器人"
2. 开通"对话服务"
3. 复制 **Webhook 地址**（包含 access_token）和 **secret**

**Webhook 地址格式**：
```
https://your-teams-server.com/api/robot/send?access_token=xxxxxxxxx
```

### 3.2 SMTP 配置示例

**QQ邮箱**：
```json
{
  "host": "smtp.qq.com",
  "port": 465,
  "secure": true,
  "user": "your-qq@qq.com",
  "pass": "授权码（不是密码）"
}
```

**企业邮箱**：
```json
{
  "host": "smtp.exmail.qq.com",
  "port": 465,
  "secure": true,
  "user": "your-name@company.com",
  "pass": "邮箱密码"
}
```

---

## 四、使用方法

### 4.1 启动服务

告诉 AI 助手：

```
帮我启动代码质量分析系统
```

### 4.2 执行分析

```
帮我分析本周的代码质量
```

或

```
帮我分析 2026 年 3 月的代码质量
```

### 4.3 AI 助手会自动完成

1. **拉取最新代码** - `git fetch` 所有项目
2. **分析代码变更** - 统计提交、增删行、任务等
3. **AI 质量评分** - 分析代码质量并评分
4. **AI 代码审查** - 识别代码问题
5. **同步数据库** - 写入分析结果
6. **发送通知** - Teams 消息和邮件

### 4.4 配置团队成员

在前端界面的"小组管理"页面添加团队成员：

1. 点击"添加成员"
2. 填写姓名、邮箱、Git 用户名
3. 只有添加的用户才会被统计

---

## 五、分析流程详解

### 5.1 周维度分析

**周期值规则**：使用**周四的日期**（YYYYMMDD）

示例：
- 2026-03-30（周一）→ 周期值 `20260402`（周四）
- 2026-04-01（周三）→ 周期值 `20260402`（周四）

**分支匹配规则**：
- 查找分支名包含周期值的版本分支
- 如 `feature/xxx-20260402`

### 5.2 月维度分析

**周期值规则**：使用月份（YYYYMM）

示例：
- 2026 年 3 月 → 周期值 `202603`
- 2026 年 4 月 → 周期值 `202604`

**统计范围**：该月所有分支的所有提交

---

## 六、功能清单

### 6.1 前端页面

| 页面 | 路由 | 功能 |
|------|------|------|
| 项目概览 | `/projects` | 项目列表、筛选、跳转详情 |
| 项目报告 | `/projects/:id/report` | 项目详细分析报告 |
| 代码审查 | `/projects/:id/code-review` | 代码问题明细 |
| 用户详情 | `/users/:id` | 个人代码评审详情 |
| 小组管理 | `/team` | 团队成员管理 |
| 小组报告 | `/team/report` | 团队整体分析报告 |

### 6.2 后端 API

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/v1/projects` | GET | 项目列表 |
| `/api/v1/users` | GET | 用户列表 |
| `/api/v1/dashboard/overview` | GET | 大盘数据 |
| `/api/v1/projects/:id/report` | GET | 项目报告 |
| `/api/v1/code-review/:id` | GET | 代码审查问题 |
| `/api/v1/teams/user-names` | GET | 团队成员用户名列表 |

---

## 七、文件结构

```
code-quality-system/
├── SKILL.md              # 本文档
├── config.example.json   # 配置模板
├── backend.zip           # 后端代码压缩包
├── frontend.zip          # 前端代码压缩包
├── scripts/              # 分析脚本
│   ├── setup.js          # 安装脚本
│   ├── analyze-code-v2.js
│   ├── sync-to-db.js
│   ├── notify-teams.js
│   └── weekly-analysis.sh
└── references/           # 参考文档
```

---

## 八、技术栈

### 后端
- NestJS 10
- Prisma 5
- PostgreSQL 16

### 前端
- React 18
- TypeScript 5
- Vite 5
- Ant Design 5
- Zustand 4

---

## 九、常见问题

### Q: 如何添加新项目？

A: 项目会自动识别。只要代码目录下有 `.git` 文件夹，就会被扫描到。

### Q: 如何修改分析周期？

A: 在前端页面顶部切换"周/月"维度，选择日期即可。

### Q: 数据可以导出吗？

A: 可以通过 API 导出，或直接查询 PostgreSQL 数据库。

### Q: 支持哪些 Git 平台？

A: 支持 Git、GitLab、GitHub、Gitee 等所有 Git 托管平台。

---

## 十、联系支持

遇到问题？直接告诉 AI 助手：

```
代码质量分析系统启动失败，帮我看看
```

AI 助手会自动诊断并解决问题。