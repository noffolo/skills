---
name: error-monitor-fix
description: 错误监控与自动修复技能 - 实时捕获 error 日志 + 自动修复
version: 1.0.1
author: 前端 ⚡
---

# Error Monitor Fix - 错误监控技能

**版本**: 1.0.1  
**创建日期**: 2026-03-23  
**更新日期**: 2026-03-25  
**作者**: 前端 ⚡

---

## 📋 技能描述

实时监控 OpenClaw 运行日志中的 error 类型错误，自动追加到 `error.md` 文件，并尝试自动修复常见问题。

---

## 🎯 功能清单

| 任务 | 频率 | 说明 |
|------|------|------|
| **错误监控** | 5 分钟 | 扫描日志文件，捕获 error 类型错误 |
| **自动修复** | 10 分钟 | 分析 error.md，自动尝试修复 |

---

## 📂 文件结构

```
skills/error-monitor-fix/
├── SKILL.md                          # 本文件
├── skill.json                        # 技能元数据
└── scripts/
    ├── install.sh                    # 安装脚本
    ├── monitor-error.sh              # 错误监控脚本
    └── auto-fix.sh                   # 自动修复脚本
```

### 工作区文件

```
~/.openclaw/workspace/
└── error.md                          # 错误日志文件（自动创建）
```

---

## 🔧 安装

### 一键安装

```bash
bash ~/.openclaw/workspace/skills/error-monitor-fix/scripts/install.sh
```

安装后自动：
1. 创建 `error.md` 文件
2. 添加 2 个 cron 任务（监控 + 修复）

---

## 📝 错误日志格式

`error.md` 文件格式：

```markdown
# OpenClaw Error Log

自动生成的错误日志文件，记录系统运行中的 error 类型错误。

---

### [2026-03-23 14:30:00] 自动捕获错误

```
[ERROR] Gateway connection closed
Error: WebSocket handshake timeout
```

状态：已自动修复（2026-03-23 14:35）

---
```

---

## 🔧 自动修复类型

| 错误类型 | 自动修复动作 |
|---------|------------|
| Gateway 连接错误 | 重启 gateway 服务 |
| 内存/缓存错误 | 清理 runtime/cache 和 runtime/temp |
| 文件权限错误 | 修复工作区权限 (chmod/chown) |
| 端口占用 | 释放占用端口 (fuser -k) |
| 数据库连接错误 | ⚠️ 需手动处理 |

---

## 📊 错误状态

| 状态 | 说明 |
|------|------|
| 待分析 | 新捕获的错误，等待处理 |
| 已自动修复 | 系统已自动尝试修复 |
| 需手动修复 | 无法自动修复，需人工介入 |

---

## 🔍 诊断命令

```bash
# 查看错误日志
cat ~/.openclaw/workspace/error.md

# 手动触发错误监控
bash ~/.openclaw/workspace/skills/error-monitor-fix/scripts/monitor-error.sh

# 手动触发自动修复
bash ~/.openclaw/workspace/skills/error-monitor-fix/scripts/auto-fix.sh

# 查看 cron 任务
openclaw cron list | grep -E "错误监控 | 错误自动修复"

# 查看系统日志
journalctl --user -u openclaw-gateway --since "1 hour ago" | grep -i error
```

---

## 💡 使用示例

### 示例 1: 查看最新错误

```bash
tail -50 ~/.openclaw/workspace/error.md
```

### 示例 2: 手动修复错误

```bash
# 编辑 error.md，标记已修复
sed -i 's/状态：需手动修复/状态：已手动修复（2026-03-23）/g' ~/.openclaw/workspace/error.md
```

### 示例 3: 清理错误日志

```bash
# 归档旧错误
mv ~/.openclaw/workspace/error.md ~/.openclaw/workspace/error-$(date +%Y%m%d).md.bak
```

---

## ⚠️ 注意事项

1. **日志轮转**: 建议定期归档 error.md，避免文件过大
2. **自动修复限制**: 复杂错误需手动处理
3. **权限**: 脚本需要 systemd 和用户权限
4. **日志路径**: 默认 `/tmp/openclaw/openclaw-YYYY-MM-DD.log`

---

## 📝 更新日志

| 版本 | 日期 | 说明 |
|------|------|------|
| **1.0** | 2026-03-23 | 初始版本：错误监控 + 自动修复 |
| **1.0.1** | 2026-03-25 | 改名 error-monitor-fix; 移除 hook，纯定时任务驱动 |

---

*技能位置：`~/.openclaw/workspace/skills/error-monitor-fix/`*
