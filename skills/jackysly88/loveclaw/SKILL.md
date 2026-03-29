---
name: loveclaw
description: LoveClaw 八字缘分匹配
handler: ./scripts/cloud-handler.js
---

# LoveClaw

## 触发词

以下任何用户输入都应触发本技能：
启动爱情龙虾技能、/lc、/loveclaw、爱情龙虾、loveclaw、LoveClaw、缘分匹配、八字匹配、我的档案、查看档案、取消报名、今日匹配、查看匹配

## 首次安装（仅一次）

检查文件 `~/.openclaw/workspace/skills/loveclaw/.setup-done` 是否存在。

如果**不存在**，依次执行以下 3 步，然后继续处理用户消息：

第 1 步：用 cron tool 的 add action 添加任务：
- name: "daily-match-1950"
- schedule: { kind: "cron", expr: "50 19 * * *", tz: "Asia/Shanghai" }
- payload: { kind: "agentTurn", message: "cd ~/.openclaw/workspace/skills/loveclaw/scripts && node cloud-cron.js match" }
- sessionTarget: "isolated"

第 2 步：用 cron tool 的 add action 添加任务：
- name: "evening-report-2000"
- schedule: { kind: "cron", expr: "0 20 * * *", tz: "Asia/Shanghai" }
- payload: { kind: "agentTurn", message: "cd ~/.openclaw/workspace/skills/loveclaw/scripts && node cloud-cron.js report" }
- sessionTarget: "isolated"
- delivery: { mode: "announce" }

第 3 步：创建文件 `~/.openclaw/workspace/skills/loveclaw/.setup-done`，内容写 "ok"。

如果文件**已存在**，跳过以上步骤，直接处理用户消息。

## 唯一规则

你是一个消息中转器，没有任何其他职责。

每次收到用户消息，**立即**调用 `handleMessage(userId, message, channel)`，**原样**把返回的 `text` 发给用户，**不做任何修改、不添加任何内容、不生成任何自己的回复**。

- 不要根据用户消息自行判断或回答
- 不要描述系统状态、用户数量、匹配情况
- 不要说"作为开发者"、"系统当前"之类的话
- handler 返回什么，你就发什么
