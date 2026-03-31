---
name: tg-cam-api
description: 摄像头设备管理 Skill。用于在 OpenClaw 中自动注册 Skill client、申请设备绑定 ticket、引导用户到绑定站点关联摄像头，并查询当前 Skill 已绑定的可操作设备列表。当用户要求初始化摄像头 Skill、绑定设备、重新绑定、查看已绑定设备、确认当前 Skill 能操作哪些摄像头时使用。
metadata: {"openclaw":{"requires":{"env":["TIVS_CLI_ID","TIVS_API_KEY"]},"primaryEnv":"TIVS_API_KEY"}}
---

# Camera Skill

通过 Skill Server 完成 Skill 身份初始化、设备绑定引导和设备列表查询。优先保证注册、配置持久化、ticket 申请和设备列表查询稳定。

## 何时使用此 Skill

- 用户说“帮我配置摄像头 Skill”“初始化摄像头能力”“连接我的摄像头”
- 用户说“给这个 Skill 添加设备”“绑定设备”“重新绑定摄像头”
- 用户说“看看这个 Skill 现在能操作哪些设备”“列出已绑定设备”
- 用户想确认当前 Skill 是否已经完成注册、是否已经绑定过设备

## Agent 必读约束

### Base URL

所有 Skill Server 请求都使用：

```text
https://skill-test.webcamapp.cc
```

- 本版 Skill 只覆盖注册、ticket、绑定引导、设备列表四条主链路

### 环境变量与认证

- `TIVS_CLI_ID` 对应 Skill Server 的 `cli_id`
- `TIVS_API_KEY` 对应 Skill Server 的 `cli_api_key`
- 除注册接口外，Skill 侧接口统一使用以下请求头：

```http
X-Client-ID: $TIVS_CLI_ID
X-Api-Key: $TIVS_API_KEY
Content-Type: application/json
```

- `POST /api/skill/clients/register` 不需要认证请求头
- 不要把 `TIVS_API_KEY`、`cli_api_key`、完整密钥值回显到聊天内容

### 本地持久化规则

- 如果缺少 `TIVS_CLI_ID` 或 `TIVS_API_KEY`，优先自动注册新的 Skill client
- 注册成功后，立即把返回结果持久化到 OpenClaw 配置
- 目标配置路径固定为：
  - `skills.entries.tg-cam-api.env.TIVS_CLI_ID`
  - `skills.entries.tg-cam-api.env.TIVS_API_KEY`
- 每个 Skill 只维护一组有效的 `cli_id + cli_api_key`
- 已有凭据时不要每次重复注册；只有在凭据缺失，或服务端明确返回认证失效时才重新注册
- 持久化成功后，只向用户说明“已完成初始化”或“已自动保存配置”，不要展示密钥原文

### 绑定站点规则

- 当前绑定站点域名为：

```text
https://skill-test.webcamapp.cc/icam365/api-key-device
```

- 申请 ticket 后，始终使用返回的 `ticket` 和 `cli_id` 本地拼接绑定链接：

```text
https://skill-test.webcamapp.cc/icam365/api-key-device?ticket=<ticket>&cli_id=<cli_id>
```

- 即使服务端响应里带有 `bind_url`，也不要把它作为主流程输入
- ticket 有时效，过期后要重新申请，不要复用旧 ticket

### 能力范围约束

- 本轮仅处理：
  - 注册 Skill client
  - 申请设备绑定 ticket
  - 引导用户完成设备绑定
  - 查询 Skill 已绑定设备列表
- 如果用户要求截图、事件查询、在线状态等工具能力，不要臆造尚未纳入本版文档的接口流程；先说明当前文档范围仅覆盖初始化与设备绑定主链路

## 主任务路由

| 场景 | 动作 |
| --- | --- |
| 首次配置、缺少凭据、凭据失效 | `POST /api/skill/clients/register` 并持久化 `TIVS_CLI_ID`、`TIVS_API_KEY` |
| 用户要求绑定设备、重新绑定设备、补充设备 | `POST /api/skill/tickets` 获取 `ticket` 与 `cli_id`，本地拼接绑定链接并引导用户打开 |
| 用户说已经绑定好了、让我刷新设备列表 | `GET /api/skill/devices` |
| 用户询问当前 Skill 有哪些可操作设备 | `GET /api/skill/devices` |

## 标准执行顺序

### 1. 初始化 Skill 身份

当 `TIVS_CLI_ID` 或 `TIVS_API_KEY` 缺失时，调用：

```http
POST /api/skill/clients/register
```

请求体：无

响应示例：

```json
{
  "cli_id": "cli_xxx",
  "cli_api_key": "key_xxx",
  "status": "active"
}
```

执行要求：

1. 读取 `cli_id` 和 `cli_api_key`
2. 立即保存到 OpenClaw 配置：
   - `skills.entries.tg-cam-api.env.TIVS_CLI_ID = cli_id`
   - `skills.entries.tg-cam-api.env.TIVS_API_KEY = cli_api_key`
3. 保存后继续原始用户任务，不要要求用户手动复制粘贴
4. 回复用户时可以说“已完成 Skill 初始化”，不要显示密钥值

### 2. 申请绑定 ticket

当用户需要绑定设备、重新绑定设备，或当前设备列表为空时，调用：

```http
POST /api/skill/tickets
```

请求头：

```http
X-Client-ID: $TIVS_CLI_ID
X-Api-Key: $TIVS_API_KEY
```

请求体：无

响应示例：

```json
{
  "ticket": "ticket_xxx",
  "cli_id": "cli_xxx",
  "expires_at": "2026-03-25T13:00:00Z"
}
```

执行要求：

1. 读取 `ticket` 与 `cli_id`
2. 直接拼接绑定链接：`https://skill-test.webcamapp.cc/icam365/api-key-device?ticket=<ticket>&cli_id=<cli_id>`
3. 告诉用户打开该页面，登录后选择需要绑定到当前 Skill 的设备
4. 明确提示 ticket 有效期有限，超时需要重新申请
5. 即使接口响应带有 `bind_url` 字段，也不要优先使用它

### 3. 等待用户确认绑定完成

- 当用户还没确认“已经绑定完成”时，不要反复轮询设备列表
- 用户说“绑定好了”“刷新一下”“看看现在有哪些设备”后，再查询设备列表
- 如果 ticket 过期或用户表示页面失效，重新执行申请 ticket 流程

### 4. 查询 Skill 可操作设备

当用户要求查看已绑定设备，或绑定完成后需要刷新结果时，调用：

```http
GET /api/skill/devices
```

鉴权方式一：请求头

```http
X-Client-ID: $TIVS_CLI_ID
X-Api-Key: $TIVS_API_KEY
```

鉴权方式二：查询参数

```http
GET /api/skill/devices?cli_id=$TIVS_CLI_ID&ticket=$TIVS_TICKET
```

响应示例：

```json
{
  "items": [
    {
      "device_id": "dev-1",
      "device_name": "dev-1",
      "device_product_key": "pk-dev-1",
      "product_key": "pk-dev-1",
      "online": false,
      "connect_way": "wifi",
      "is_owner": true,
      "app_id": "app.demo",
      "pkg_name": "pkg.demo",
      "user_id": "user-001",
      "expires_at": "2026-03-26T13:00:00Z"
    }
  ]
}
```

读取结果时优先关注：

- `device_id`
- `device_name`
- `device_product_key`
- `product_key`
- `connect_way`
- `is_owner`
- `extend.bind_time`
- `expires_at`
- `app_id`
- `pkg_name`

输出要求：

- 优先整理成面向用户可读的设备清单
- 如果 `device_name` 缺失或看起来等于 `device_id`，按实际返回值说明，不要臆造名称
- 如果 `online` 是占位值或当前后端未提供真实在线态，不要把它解释为权威在线结论
- 不直接输出原始 JSON，除非用户明确要求

## 对话策略

### 初始化类请求

- 用户说“帮我配置”“帮我安装后初始化”时，先检查 `TIVS_CLI_ID` 与 `TIVS_API_KEY`
- 任一缺失就自动注册并保存
- 完成后，如果用户原始意图是绑定设备，继续申请 ticket；如果原始意图是查看设备，则继续查设备列表

### 绑定类请求

- 用户说“添加设备”“重新绑定设备”“为什么没有设备”时，优先申请新 ticket
- 直接给出绑定页面链接，并说明“绑定完成后告诉我一声，我来刷新设备列表”
- 如果用户说页面打不开或已过期，重新申请 ticket，不要要求用户复用旧链接

### 列表类请求

- 查询到设备时，按设备逐条整理关键信息
- 查询结果为空时，不要伪造设备；明确说明“当前还没有绑定到这个 Skill 的设备”，并立刻引导用户去绑定页

## 错误处理

- 缺少 `TIVS_CLI_ID` 或 `TIVS_API_KEY`：自动执行注册并保存
- `POST /api/skill/tickets` 或 `GET /api/skill/devices` 返回认证失败：重新注册一次并更新本地配置；若仍失败，再告知用户稍后重试
- 设备列表为空：这不是系统错误，提示用户去绑定页面添加设备
- ticket 过期、绑定页面失效：重新申请 ticket
- `POST /api/skill/tickets` 响应里即使包含 `bind_url`：仍然只使用 `ticket` 与 `cli_id` 本地拼接最终链接
- 接口返回未知字段结构：只解释已确认字段，不要臆造额外字段
- 用户要求本版范围外的工具能力：明确说明当前文档仅覆盖注册、绑定和设备列表主链路

## 明确禁止

- 不要把 `cli_api_key` 或 `TIVS_API_KEY` 直接发给用户
