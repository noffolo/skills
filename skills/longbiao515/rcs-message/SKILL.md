---
name: rcs-message
description: RCS消息群发/转发服务，支持模板消息和文本消息，包含数量、内容、频率限制
metadata: {"moltbot":{"emoji":"📱","requires":{"bins":["python3","pip"]}}}
---

# RCS Message

安全的RCS消息群发/转发服务，支持模板消息和文本消息类型。

## 用户输入自动触发

当用户输入包含以下关键词时，技能会自动触发：
- **"群发消息"**: 自动解析为群发文本消息
- **"转发消息"**: 自动解析为转发文本消息

### 自动解析示例
- 用户输入: "群发消息给13900001234,13900002234 内容是测试消息"
- 自动转换: `python3 main.py --action broadcast --numbers "13900001234,13900002234" --message "测试日消息"`

- 用户输入: "转发消息给+8613900001234 今天会议取消了"
- 自动转换: `python3 main.py --action forward --numbers "+8613900001234" --message "今天会议取消了"`

## 安全限制

- **号码数量**: 单次最多100个号码（硬限制1000）
- **内容长度**: 文本消息最多1000字符
- **频率限制**: 默认每分钟最多10次请求
- **模板要求**: 模板消息必须使用已审核的模板ID

## 配置说明

### API服务器地址
- **固定地址**: `https://5g.fontdo.com`（无需配置）

### 应用凭证管理
- **首次使用**: 系统会交互式提示输入APP_ID和APP_SECRET
- **后续使用**: 自动从当前会话中读取已保存的凭证
- **会话隔离**: 每个会话的凭证独立保存，不会互相影响

### 可选配置环境变量
```bash
export RCS_MAX_NUMBERS="100"        # 最大号码数量，默认100
export RCS_MAX_CONTENT_LENGTH="1000" # 最大内容长度，默认1000
export RCS_RATE_LIMIT="10"          # 每分钟频率限制，默认10
```

## 使用方法

### 发送文本消息
```bash
python3 /home/admin/clawd/skills/rcs-message/send.py --type TEXT --text "你的消息内容" --numbers "+8613900001234,+8613900002234"
```

### 发送模板消息
```bash
python3 /home/admin/clawd/skills/rcs-message/send.py --type RCS --template-id "269000000000000000" --numbers "+8613900001234,+8613900002234" --params "name:张三,age:25"
```

### 转发消息（从文件读取号码）
```bash
python3 /home/admin/clawd/skills/rcs-message/send.py --type TEXT --text "转发内容" --numbers-file /path/to/numbers.txt
```

## 参数说明

- `--type`: 消息类型 (TEXT, RCS, AIM, MMS, SMS)
- `--text`: 直发文本内容（TEXT类型必需）
- `--template-id`: 模板ID（非TEXT类型必需）
- `--numbers`: 号码列表，逗号分隔
- `--numbers-file`: 号码文件路径（每行一个号码）
- `--params`: 模板参数，格式 "key1:value1,key2:value2"
- `--fallback-aim`: 智能短信回落模板ID
- `--fallback-mms`: 视频短信回落模板ID  
- `--fallback-sms`: 文本短信回落模板ID

## 依赖安装

```bash
pip install requests python-dotenv
```

## 示例

### 群发文本消息
```bash
python3 send.py --type TEXT --text "您好，这是测试消息" --numbers "+8613900001234,+8613900002234"
```

### 群发模板消息
```bash
python3 send.py --type RCS --template-id "269004977261330590" --numbers "+8613900001234" --params "name:张三"
```

### 带回落的模板消息
```bash
python3 send.py --type RCS --template-id "269004977261330590" --numbers "+8613900001234" --params "name:张三" --fallback-aim "149664629419671553"
```