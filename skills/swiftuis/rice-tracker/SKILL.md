---
name: rice-tracker
description: >
  大米消耗采购提醒系统。记录每个买家的购买信息，自动计算预计吃完日期，
  支持工作日/周末/每日消耗频率，到期自动提醒采购。
  适用于：大米卖家追踪客户库存、团购组织者管理库存、家庭食材管理。
  Keywords: 大米, 库存管理, 采购提醒, 消耗追踪
version: 1.0.0
homepage: https://clawhub.com/skills/rice-tracker
author: 你的名字
tags: [实用工具, 库存管理, 自动提醒]
---

# 🍚 大米消耗采购提醒系统

记录每个买家的大米购买与消耗，自动计算预计吃完日期，快到期时自动提醒采购。

## 功能特性

- ✅ 添加买家记录（姓名、手机号、购买日期、斤数、人口、消耗频率）
- ✅ 消耗频率：每天都吃 / 只工作日吃 / 只周末吃
- ✅ 自动计算预计吃完日期（剩余天数）
- ✅ 状态标签：已耗尽（红）/ 即将耗尽（橙）/ 充足（绿）
- ✅ 删除记录
- ✅ **每日 20:00 自动检查并推送提醒**（集成 OpenClaw cron）
- ✅ 手机/电脑 Web 界面访问

## 使用方式

### 📋 常用操作（告诉 AI 即可）

| 操作 | 示例 |
|:---|:---|
| 添加客户记录 | "张三，2026-03-27，买了40斤，家里3口人，每人每天0.4斤，工作日吃" |
| 记录客户吃完了 | "李四今天买新大米了，30斤" |
| 查看状态 | "查看大米库存" |
| 删除客户记录 | "删除张三的记录" |
| 测试提醒 | "运行一次大米检查" |

### 🌐 Web 界面

```bash
python3 ~/.openclaw/workspace/skills/rice-tracker/scripts/app.py
```

- **电脑浏览器**：`http://localhost:5001`
- **手机浏览器**：`http://<本机IP>:5001`

### 🔔 自动提醒

每天 20:00（Asia/Shanghai）自动检查，有提醒会自动推送。

## 文件结构

```
rice-tracker/
├── SKILL.md
└── scripts/
    ├── app.py              # Flask Web 主程序
    └── check_alerts.py     # 每日检查脚本
```

## 数据文件

```
~/.openclaw/workspace/rice-shop-records.json
```

## 自动设置

安装本技能后，运行以下命令完成初始化：

```bash
# 1. 安装依赖（Flask 已内置）
pip3 install flask --break-system-packages  # 如提示未安装

# 2. 启动 Web 服务（后台运行）
nohup python3 ~/.openclaw/workspace/skills/rice-tracker/scripts/app.py \
  > ~/.openclaw/workspace/skills/rice-tracker/app.log 2>&1 &

# 3. 测试提醒脚本
python3 ~/.openclaw/workspace/skills/rice-tracker/scripts/check_alerts.py
```

## 定时提醒配置

如 cron 未自动设置，手动添加：

```bash
# 每天 20:00 自动检查并推送提醒
openclaw cron add --name "大米库存每日检查" \
  --schedule "0 20 * * *" \
  --timezone "Asia/Shanghai" \
  --message "请运行以下命令检查大米库存：\npython3 ~/.openclaw/workspace/skills/rice-tracker/scripts/check_alerts.py\n运行后将结果整理成消息发送给我，告诉我哪些客户需要采购提醒。" \
  --channel webchat
```
