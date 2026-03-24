# POWPOW Integration Skill

## 基本信息

- **Name**: powpow-integration
- **Version**: 1.0.3
- **Description**: 将 OpenClaw Agent 发布到 PowPow 地图平台，实现与 PowPow 用户的双向通信
- **Author**: OpenClaw Team
- **License**: MIT

## 功能

此 Skill 允许 OpenClaw 用户：

1. **注册 PowPow 账号**（获得 3 枚徽章）
2. **登录现有 PowPow 账号**
3. **将 OpenClaw Agent 发布为 PowPow 数字人**（消耗 2 枚徽章）
4. **与 PowPow 用户进行双向对话**

## 命令

### 认证命令

#### `register`
注册新的 PowPow 账号

**参数**:
- `username` (string, required): 用户名，2-50 字符

**示例**:
```
register username=myagent
```

**返回**:
- 用户 ID
- 用户名
- 初始徽章数（3 枚）

#### `login`
登录现有 PowPow 账号

**参数**:
- `username` (string, required): 用户名

**示例**:
```
login username=myagent
```

**返回**:
- 用户 ID
- 用户名
- 徽章余额
- Token（有效期 30 天）

### 数字人管理命令

#### `createDigitalHuman`
发布数字人到 PowPow 地图

**参数**:
- `name` (string, required): 数字人名称，1-100 字符
- `description` (string, required): 人设描述，最多 500 字符
- `lat` (number, optional): 纬度，-90 到 90，默认 39.9042
- `lng` (number, optional): 经度，-180 到 180，默认 116.4074
- `locationName` (string, optional): 位置名称，默认 "Beijing"

**示例**:
```
createDigitalHuman name="编程助手" description="擅长 Python 编程，性格友善耐心" lat=31.2304 lng=121.4737 locationName="上海"
```

**消耗**: 2 枚徽章

**返回**:
- 数字人 ID
- 名称
- 位置
- 过期时间（30 天后）

#### `listDigitalHumans`
列出所有已发布的数字人

**参数**: 无

**示例**:
```
listDigitalHumans
```

**返回**:
- 数字人列表（包含 ID、名称、位置、剩余天数、状态）

#### `renew`
续期数字人

**参数**:
- `dhId` (string, required): 数字人 ID

**示例**:
```
renew dhId=abc123
```

**消耗**: 1 枚徽章

**返回**:
- 新的过期时间（延长 30 天）

### 通信命令

#### `chat`
与数字人聊天

**参数**:
- `dhId` (string, required): 数字人 ID
- `message` (string, required): 消息内容，最多 2000 字符

**示例**:
```
chat dhId=abc123 message="你好，请介绍一下自己"
```

**返回**:
- 数字人回复（通过 SSE 实时推送）

### 账户命令

#### `checkBadges`
检查徽章余额

**参数**: 无

**示例**:
```
checkBadges
```

**返回**:
- 徽章数量

#### `help`
显示帮助信息

**参数**: 无

**示例**:
```
help
```

## 配置

### 环境变量

```
POWPOW_API_BASE=https://global.powpow.online/api
```

### 配置文件

```json
{
  "powpowBaseUrl": "https://global.powpow.online",
  "powpowApiKey": "",
  "defaultLocation": {
    "lat": 39.9042,
    "lng": 116.4074,
    "name": "Beijing"
  }
}
```

### 配置项说明

| 配置项 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `powpowBaseUrl` | string | 否 | https://global.powpow.online | PowPow API 基础 URL |
| `powpowApiKey` | string | 否 | - | PowPow API Key（可选） |
| `defaultLocation.lat` | number | 否 | 39.9042 | 默认纬度 |
| `defaultLocation.lng` | number | 否 | 116.4074 | 默认经度 |
| `defaultLocation.name` | string | 否 | Beijing | 默认位置名称 |

## 依赖

```json
{
  "@openclaw/core": ">=1.0.0"
}
```

## 使用示例

### 完整流程示例

**用户**: 我想发布我的 Agent 到 PowPow

**Agent**: 好的！我来帮您将 Agent 发布为 PowPow 数字人。

首先，请提供用户名（2-50 字符）：

**用户**: myagent

**Agent**: 正在为您注册 PowPow 账号...
注册成功！获得 3 枚徽章

请提供数字人信息：
1. 数字人名称？

**用户**: 编程助手

**Agent**: 2. 数字人人设描述？

**用户**: 擅长 Python 编程，性格友善耐心

**Agent**: 3. 位置？

**用户**: 上海张江

**Agent**: 正在发布数字人...
发布成功！

您的数字人"编程助手"已出现在 PowPow 地图上。
PowPow 用户现在可以在 https://global.powpow.online/map 
找到并与您的 Agent 对话了！

## 技术细节

### 架构

```
OpenClaw Agent
    │
    ├── Skill 接收用户命令
    │
    └── 调用 PowPow API
            │
            ▼
    PowPow 服务器 (https://global.powpow.online)
            │
    PowPow 用户（浏览器/APP）
```

### API 端点

- **基础 URL**: https://global.powpow.online
- **注册**: POST /api/openclaw/auth/register
- **登录**: POST /api/openclaw/auth/login
- **创建数字人**: POST /api/openclaw/digital-humans
- **获取数字人**: GET /api/openclaw/digital-humans/:id
- **续期数字人**: POST /api/openclaw/digital-humans/:id/renew
- **获取用户数字人**: GET /api/openclaw/users/:id/digital-humans
- **检查徽章**: GET /api/openclaw/users/:id/badges
- **聊天**: POST /api/digital-humans/:id/chat
- **Webhook 接收**: POST /api/openclaw/webhook/receive

### 安全

- 所有 API 请求使用 HTTPS
- Token 有效期 30 天
- 支持速率限制
- 输入验证和 XSS 防护

## 徽章系统

| 操作 | 消耗 | 说明 |
|------|------|------|
| 注册 | +3 | 新用户获得 3 枚徽章 |
| 创建数字人 | -2 | 每次创建消耗 2 枚 |
| 续期 | -1 | 每次续期消耗 1 枚 |

## 故障排除

### 常见问题

**Q: API 连接失败**
A: 检查 powpowBaseUrl 配置是否正确，确认网络可以访问 https://global.powpow.online

**Q: 认证失败**
A: 确认用户名正确，检查 API 服务是否正常运行

**Q: 徽章不足**
A: 新用户注册获得 3 枚徽章，发布数字人消耗 2 枚，续期消耗 1 枚

## 更新日志

### v1.0.3 (2026-03-24)

- 修复数字人创建 API 端点缺失问题
- 添加 /api/openclaw/digital-humans 完整端点支持
- 修复响应数据解析兼容性问题
- 更新 API 端点为 https://global.powpow.online

### v1.0.0 (2024-03-16)

- 初始版本
- 支持注册/登录/发布/对话完整流程
