# 📧 Email Analyzer 技能（固化版）

**创建时间**：2026-03-06  
**固化状态**：🔒 **锁死** - 改动需 Wood 哥书面同意  
**执行者**：湫儿  
**监督人**：Wood 哥  

---

## 📋 技能说明

**用途**：分析、清理 biqiang@126.com 邮箱邮件  
**唯一性**：这是访问 Wood 哥邮箱的**唯一合法方式**  

---

## 🔒 固化配置（禁止修改）

| 配置项 | 值 | 备注 |
|--------|------|------|
| **IMAP 服务器** | `imap.126.com:993` | 126 邮箱 |
| **邮箱账户** | `biqiang@126.com` | Wood 哥邮箱 |
| **授权码** | `WUEw8qhBwjzpUAZW` | ✅ 固化 |
| **SSL 验证** | `ssl=True` | 必须 |
| **超时时间** | `60 秒` | 防超时 |
| **ID 命令** | ASCII only! | ❌ 禁止中文 |
| **抓取方法** | `BODY.PEEK[HEADER.FIELDS]` | ✅ 已验证 |
| **删除方法** | `set_flags + expunge` | ✅ 已验证 |

---

## 🎯 关键词列表（固化）

### 可删除关键词（DELETE_KW）
```python
DELETE_KW = [
    'sale', 'discount', 'promo', 'deal', 'offer', 'clearance',
    'newsletter', 'subscription', 'weekly', 'monthly', 'unsubscribe',
    'notification', 'alert', 'update', 'reminder', 'verification',
    'ecobee', 'rachio', 'nest', 'ring', 'smart home',
    'hoa', 'community', 'meeting', 'election', 'board',
    'temu', 'shein', 'wish', 'aliexpress', 'sponsor', 'ad'
]
```

### 保留关键词（KEEP_KW）
```python
KEEP_KW = [
    'forsyth', 'school', 'lhs', 'teacher', 'student',
    'chase', 'visa', 'statement', 'bank', 'credit card',
    'amazon', 'order', 'shipping', 'tracking', 'delivery',
    'uber', 'lyft', 'flight', 'hotel', 'airline', 'delta',
    'google', 'icloud', 'dropbox', 'onedrive', 'apple',
    'insurance', 'medical', 'health', 'doctor', 'hospital',
    'tax', 'irs', 'government', 'utility', 'power', 'water',
    'receipt', 'invoice', 'warranty', 'contract', 'lease'
]
```

---

## 📋 标准使用流程（6 步法）

### 第 1 步：分析模式
```bash
python3 /Users/lobster/.openclaw/workspace/skills/email-analyzer/analyze.py \
  --start-date "2021-02-26" \
  --end-date "2021-08-26" \
  --mode analyze
```

**输出**：JSON 分析报告（分类统计 + UID 列表）

---

### 第 2 步：等待用户确认
**必须等 Wood 哥回复"删除"或"确认"才能继续！**

汇报格式：
```
📊 邮件分析报告

批次：8
日期范围：2021-02-26 ~ 2021-08-26
总邮件数：1,500 封

建议删除：700 封（46.7%）
- Temu 推广：280 封
- 智能家居通知：150 封
- HOA 社区邮件：120 封
- 其他营销：150 封

建议保留：800 封
- 学校/教育：200 封
- 财务/银行：180 封
- 购物订单：220 封
- 其他重要：200 封

确认后回复"删除"执行删除操作。
```

---

### 第 3 步：备份
```bash
python3 /Users/lobster/.openclaw/workspace/skills/email-analyzer/backup.py \
  --batch 8 \
  --uids-file delete_uids.json \
  --output batch8_delete_final_backup.json
```

---

### 第 4 步：执行删除
```bash
python3 /Users/lobster/.openclaw/workspace/skills/email-analyzer/delete.py \
  --uids-file delete_uids.json \
  --confirm
```

---

### 第 5 步：验证
```bash
python3 /Users/lobster/.openclaw/workspace/skills/email-analyzer/verify.py
```

**输出**：删除前后对比统计

---

### 第 6 步：汇报
```
✅ 批次 8 删除完成！

📊 删除统计：
  批次 8: 700 封 (2021-02-26 ~ 2021-08-26)
  总计：700 封

📈 删除后邮箱状态：
  总邮件数：26,298 封
  未读数：18,500 封

💾 备份文件：
  - batch8_delete_final_backup.json

✅ Wood 哥，清理完成！
```

---

## 🚨 错误处理

### IMAP 连接失败
```
错误："Unsafe Login" 或 "Authentication failed"
处理：
  1. 等待 5 分钟重试
  2. 检查 126 网页版是否能登录
  3. 汇报 Wood 哥：可能需要重新生成授权码
```

### SELECT 失败
```
错误："SELECT failed" 或 "Mailbox not found"
处理：
  1. 等待 24 小时（可能是 126 风控）
  2. 用网页版登录解锁
  3. 重试
```

### ID 命令错误
```
错误：UnicodeEncodeError
处理：确保 ID 命令参数只用 ASCII 英文
```

---

## ⚠️ 使用限制

1. **禁止自动执行**：只有在 Wood 哥明确要求时才运行
2. **禁止修改配置**：授权码、关键词、服务器等都锁死
3. **禁止跳过确认**：删除前必须等 Wood 哥确认
4. **禁止删除备份**：备份文件永久保留

---

## 📁 文件结构

```
/Users/lobster/.openclaw/workspace/skills/email-analyzer/
├── SKILL.md              # 本文档（固化配置）
├── analyze.py            # 分析脚本
├── delete.py             # 删除脚本
├── backup.py             # 备份脚本
├── verify.py             # 验证脚本
└── email_analyzer.py     # 核心模块（IMAP 连接）
```

---

## 📝 变更记录

| 日期 | 变更 | 批准人 |
|------|------|--------|
| 2026-03-06 | 技能创建 | Wood 哥 |

---

**固化完成！🔒**
