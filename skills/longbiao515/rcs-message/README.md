# RCS Message Skill

**蜂动科技5G消息群发/转发服务**

![RCS Message](https://img.shields.io/badge/RCS-Message-blue?logo=5g)
![Privacy Protected](https://img.shields.io/badge/Privacy-Protected-green)

## 📋 目录
- [功能特性](#-功能特性)
- [安全限制](#-安全限制)
- [安装配置](#-安装配置)
- [使用方法](#-使用方法)
- [隐私保护](#-隐私保护)
- [故障排除](#-故障排除)
- [API文档](#-api文档)

## 🚀 功能特性

### 核心功能
- **群发消息**: 支持批量发送文本消息到多个号码
- **转发消息**: 快速转发现有消息内容
- **多模板类型**: 支持 TEXT、RCS、AIM、MMS、SMS 五种消息类型
- **智能回落**: 自动配置短信回落策略（RCS→AIM→MMS→SMS）
- **自然语言识别**: 自动解析用户输入的"群发消息"、"转发消息"等指令

### 安全特性
- **号码加密**: 敏感信息自动加密（13763363601 → 137******01）
- **链接保护**: URL路径自动隐藏（`/secret-key` → `/****`）
- **频率限制**: 防止滥用，保护API配额
- **数量限制**: 单次最多100个号码，防止误操作
- **内容验证**: 自动检查消息长度和格式

### 用户体验
- **交互式认证**: 首次使用时提示输入凭证
- **会话隔离**: 每个会话独立保存凭证
- **环境变量支持**: 支持预配置环境变量
- **详细反馈**: 清晰的成功/失败提示

## 🔒 安全限制

| 限制类型 | 默认值 | 说明 |
|---------|--------|------|
| 号码数量 | 100个 | 单次发送最多100个号码（API上限1000） |
| 消息长度 | 1000字符 | 文本消息最大长度 |
| 发送频率 | 60秒/次 | 最小发送间隔，防止API限流 |
| 号码格式 | +86开头 | 仅支持中国手机号码格式 |

## ⚙️ 安装配置

### 环境要求
- Python 3.6+
- `requests` 库
- `python-dotenv` 库（可选）

### 依赖安装
```bash
pip install requests python-dotenv
```

### 技能目录结构
```
rcs-message/
├── README.md              # 本文件
├── SKILL.md               # 技能元数据
├── send.py                # 核心发送脚本
├── main.py                # 主入口，处理用户输入
├── handle_user_input.py   # 自然语言解析器
├── privacy_protect.py     # 隐私保护模块
├── check_config.py        # 配置检查工具
├── config.example.json    # 配置文件模板
└── USAGE_EXAMPLES.md      # 使用示例
```

## 📝 使用方法

### 方式一：Moltbot自然语言命令（推荐）
直接在Moltbot中使用自然语言：

```text
群发消息给13763363601,13900001234 内容是会议通知
```

```text
转发消息给+8613763363601 项目进度更新
```

### 方式二：命令行直接调用

#### 基本文本发送
```bash
python3 send.py -n "+8613763363601,+8613900001234" -m "会议通知"
```

#### 模板消息发送
```bash
python3 send.py --type RCS --template-id "269000000000000000" -n "+8613763363601" --params "name:张三,amount:100"
```

#### 带回落策略
```bash
python3 send.py --type RCS --template-id "269000000000000000" -n "+8613763363601" --fallback-aim "149000000000000000" --fallback-sms "短信回落内容"
```

### 方式三：配置环境变量（推荐用于生产环境）

#### 设置环境变量
```bash
# 临时设置（当前会话有效）
export FIVE_G_APP_ID="your-app-id"
export FIVE_G_APP_SECRET="your-app-secret"

# 永久设置（添加到 ~/.bashrc）
echo 'export FIVE_G_APP_ID="your-app-id"' >> ~/.bashrc
echo 'export FIVE_G_APP_SECRET="your-app-secret"' >> ~/.bashrc
source ~/.bashrc
```

#### 使用环境变量发送
```bash
python3 send.py -n "+8613763363601" -m "测试消息"
```

## 🛡️ 隐私保护

### 自动加密规则
- **电话号码**: `13763363601` → `137******01`（保留前三后二）
- **URL路径**: `https://api.example.com/secret-key` → `https://api.example.com/****`
- **API密钥**: 自动检测并隐藏敏感密钥信息
- **任务ID**: `1303321380923182868` → `130******5412451555`

### 隐私保护示例
**输入消息**:
```
联系电话：13763363601，API地址：https://api.5g.fontdo.com/v1/secret-key
```

**输出显示**:
```
联系电话：137******01，API地址：https://api.5g.fontdo.com/****
```

## 🛠️ 故障排除

### 常见问题及解决方案

#### 1. 认证失败 (403错误)
- **原因**: APP_ID 或 APP_SECRET 错误
- **解决**: 
  - 检查凭证是否正确
  - 确认应用状态是否正常
  - 重新获取凭证

#### 2. 频率限制错误
- **原因**: 发送过于频繁
- **解决**: 
  - 等待60秒后再试
  - 调整 `MIN_INTERVAL_SECONDS` 参数

#### 3. 号码格式错误
- **原因**: 号码不符合+86开头的11位数字格式
- **解决**: 
  - 确保号码格式为 `+8613763363601`
  - 或者使用 `13763363601`（自动添加+86前缀）

#### 4. 消息长度超限
- **原因**: 消息超过1000字符
- **解决**: 
  - 缩短消息内容
  - 或修改 `MAX_MESSAGE_LENGTH` 参数

### 调试模式
添加 `--debug` 参数查看详细信息：
```bash
python3 send.py -n "+8613763363601" -m "测试消息" --debug
```

## 📡 API文档

### 固定配置
- **API服务器**: `https://5g.fontdo.com`
- **接口地址**: `/messenger/api/v1/group/send`
- **请求方法**: `POST`

### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| templateType | string | 是 | 消息类型 (TEXT/RCS/AIM/MMS/SMS) |
| text | string | TEXT类型必需 | 直发文本内容 |
| templateId | string | 非TEXT类型必需 | 模板ID |
| numbers | array | 是 | 号码列表（最多1000个） |
| params | array | 动态模板必需 | 模板参数 |
| fallbackAim | object | 可选 | 智能短信回落 |
| fallbackMms | object | 可选 | 视频短信回落 |
| fallbackSms | object | 可选 | 文本短信回落 |

### 鉴权方式
- **AppId**: 应用ID
- **Timestamp**: 当前时间戳（毫秒）
- **Signature**: SHA256签名
  ```
  Signature = SHA256(method + uri + appId + secret + timestamp)
  ```

## 📊 使用示例

### 单号码发送
```bash
python3 send.py -n "+8613763363601" -m "你好，世界！"
```

### 多号码群发
```bash
python3 send.py -n "+8613763363601,+8613900001234,+8613812345678" -m "重要通知：会议改期"
```

### 模板消息
```bash
python3 send.py --type RCS --template-id "269004977261330590" -n "+8613763363601" --params "name:张三,order:12345"
```

### 参数说明
```bash
usage: send.py [-h] -n NUMBERS [-m MESSAGE] [-t {TEXT,RCS,AIM,MMS,SMS}]
               [--template-id TEMPLATE_ID] [--dry-run]

RCS消息群发工具

optional arguments:
  -h, --help            show this help message and exit
  -n NUMBERS, --numbers NUMBERS
                        电话号码列表，用逗号分隔 (例: +8613900001234,+8613900002234)
  -m MESSAGE, --message MESSAGE
                        发送的文本内容 (TEXT类型必需)
  -t {TEXT,RCS,AIM,MMS,SMS}, --type {TEXT,RCS,AIM,MMS,SMS}
                        消息类型，默认TEXT
  --template-id TEMPLATE_ID
                        模板ID (非TEXT类型必需)
  --dry-run             仅验证参数，不实际发送
```

## 📞 技术支持

- **服务商**: 蜂动科技
- **API文档**: https://5g.fontdo.com/docs
- **技术支持**: 联系蜂动科技客服


![alt text](32568a469232de8d310598ebc5ffd245.jpg)

---

**版本**: 1.0.0  
**最后更新**: 2026-03-15  
**作者**: Moltbot Skill Creator