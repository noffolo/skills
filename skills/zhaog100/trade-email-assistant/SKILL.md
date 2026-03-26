# Trade Email Assistant - 外贸邮件 AI 助手

## 概述
自动化外贸邮件管理：IMAP 拉取、关键词分类、AI 智能回复生成。脚本处理数据，Agent 驱动 AI 决策。

## 触发词
- `查邮件` / `check email` / `unread emails` — 拉取未读邮件
- `邮件摘要` / `email summary` — 查看今日统计
- `回复 #UID` / `reply #UID` — 生成回复草稿
- `发邮件` / `send email` — 发送邮件
- `询盘` / `inquiry` — 询盘相关操作

## 工作流

### 1. 查邮件
```bash
cd ~/.openclaw/workspace/skills/trade-email-assistant
bash scripts/check-emails.sh | python3 scripts/classify-email.py
```

**Agent 操作**：
- 展示分类结果给用户
- 如有 `unclassified`，读取每封邮件的 `subject` + `body_preview` 进行语义分析，输出分类
- 如有 P0 询盘（`priority=0`），立即通知用户
- 更新 SQLite：`UPDATE email_index SET category=?, priority=?, classified_method='agent_ai', classified_at=datetime('now') WHERE message_id=?`

### 2. 回复邮件
用户说"回复 #8450"时：

**Agent 操作**：
1. 从 SQLite 读取邮件：`SELECT * FROM email_index WHERE gmail_uid='8450'`
2. 拉取完整邮件：`bash scripts/check-emails.sh --max 50` 找到对应 UID 的 body_text
3. 根据分类加载知识库：
   - `inquiry` → `knowledge/trade/email-templates.md` + `incoterms-2020.md`
   - `order` → `knowledge/trade/export-process.md`
   - `logistics` → `knowledge/trade/export-process.md`
4. 生成中英双语回复草稿，用 `[待填]` 标记需人工补充的信息
5. 展示草稿给用户确认
6. 用户确认后：`bash scripts/send-email.sh --to "..." --subject "..." --body-file /tmp/reply.txt --in-reply-to "..." --send`

### 3. 邮件摘要
```bash
bash scripts/email-summary.sh
```

### 4. 发送邮件
```bash
# 预览（默认）
python3 scripts/send-email.py --to "user@example.com" --subject "主题" --body "内容" --dry-run

# 实际发送
python3 scripts/send-email.py --to "user@example.com" --subject "主题" --body-file /tmp/email.txt --send
```

## AI 分类指导
对 `unclassified` 邮件，Agent 应分析邮件内容判断类别：
- **inquiry** (P0): 询问产品、价格、样品、合作意向
- **order** (P1): 下单、付款、发票确认
- **logistics** (P2): 运输、跟踪、清关、物流查询
- **platform** (P3): 电商平台、账号、Listing、评价
- **other** (P4): 其他

## 回复草稿要求
- 语言：中英双语（English + 中文对照）
- 语气：专业、礼貌、热情
- 必须包含：公司介绍、产品优势、价格范围（[待填]）、交期
- Incoterms 2020 术语（如涉及）
- `[待填]` 标记需人工补充的具体信息

## 数据库位置
`data/email-index.db`（SQLite，WAL 模式）

## 配置
`config/email-config.json` — IMAP/SMTP 参数、分类阈值、通知时间

## 安全
- 默认 `--dry-run`，需 `--send` 确认才发送
- IMAP PEEK 不标记已读
- 密码从 `~/.openclaw/secrets/gmail.env` 读取
