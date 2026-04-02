---
name: webcam
description: 摄像头 Skill Server API。用于查询当前 Skill 已绑定的设备列表、触发截图、查询某设备事件、获取最近事件、读取事件图片、查看设备在线状态和电量。当用户要求查看当前可操作设备、拍一张当前画面、查询某天事件、查看最近事件、查看事件图片、查询在线状态或电量时使用。
metadata: {"openclaw":{"requires":{"env":["TIVS_CLI_ID","TIVS_API_KEY"]},"primaryEnv":"TIVS_API_KEY"}}
---

# Web Camera Skill

通过 Skill Server 查询和操作当前 Skill 已绑定的摄像头设备。本版尽量保持简单，只覆盖设备列表、截图、事件、在线状态和电量相关接口。

## 何时使用

- 用户要查看当前 Skill 能操作哪些摄像头
- 用户要看某个设备当前截图或实时画面
- 用户要查某个设备某一天或某个时间段的事件
- 用户要看最近一个事件或某个事件的图片
- 用户要确认设备是否在线
- 用户要查询设备电量

## 基础配置

### Base URL

所有请求都使用：

```text
https://skill.webcamapp.cc
```

### 环境变量

- `TIVS_CLI_ID`：Skill Server 分配的 `cli_id`
- `TIVS_API_KEY`：Skill Server 分配的 `cli_api_key`

### 公共请求头

本版文档统一只使用 Header 鉴权，请求头写法如下：

```http
X-Client-ID: $TIVS_CLI_ID
X-Api-Key: $TIVS_API_KEY
Content-Type: application/json
```

补充说明：

- 不要在聊天内容中回显 `TIVS_API_KEY` 的真实值
- 除非接口明确是 `GET` 且无请求体，否则默认按 JSON 请求发送
- 统一按 Header 方式调用

### 设备管理站点

如果需要管理已授权设备，或排查为什么设备列表为空，可参考设备管理站点：

```text
https://skill.webcamapp.cc/icam365/api-key-device?xxx
```

这个页面用于管理 `api_key` 已关联的设备，不是接口 Base URL。

## 通用响应

成功或失败都使用统一响应信封：

```json
{
  "requestId": "req_xxx",
  "code": "ok",
  "msg": "ok",
  "data": {}
}
```

读取结果时优先关注 `data` 字段。

## 接口列表

### 1. 获取设备列表

```http
GET /api/v1/skill/devices
```

用途：

- 列出当前 Skill 已绑定、可操作的设备
- 当用户只知道设备名称，需要先确认设备范围时优先调用

返回要点：

- `data.items[].deviceId`
- `data.items[].deviceName`
- `data.items[].deviceProductKey`
- `data.items[].productKey`
- `data.items[].online`
- `data.items[].connectWay`
- `data.items[].isOwner`
- `data.items[].extend.bindTime`
- `data.items[].appId`
- `data.items[].pkgName`
- `data.items[].userId`

### 2. 截图 / 获取实时画面

```http
POST /api/v1/skill/device/snapshot
```

请求体：

```json
{
  "deviceId": "dev-001"
}
```

说明：

- 请求体字段必须使用 `deviceId`
- `deviceId` 为空时会返回 `bad_request`
- 适合“拍一张”“看当前画面”“帮我截个图”这类请求

返回要点：

- `data.deviceId`
- `data.status`
- `data.imageUrl`

### 3. 获取某一天或某时间段事件

```http
GET /api/v1/skill/device/events
```

查询参数：

- `device_id`：必填
- `start_time`：可选，Unix 秒时间戳
- `end_time`：可选，Unix 秒时间戳
- `tag`：可选，可重复传多个
- `tags`：可选，作为 `tag` 的兼容写法
- `limit`：可选，整数，需大于等于 `0`
- `offset`：可选，整数，需大于等于 `0`

说明：

- 如果传时间范围，建议 `start_time` 和 `end_time` 一起传
- 如果同时传 `start_time` 和 `end_time`，必须满足 `start_time < end_time`
- 适合“今天发生了什么”“查某天事件”“只看某类事件”这类请求

返回要点：

- `data.items[].id`
- `data.items[].tag`
- `data.items[].time`
- `data.items[].deviceId`
- `data.items[].detailDescription`

### 4. 获取最近一个事件

```http
GET /api/v1/skill/device/events/latest
```

查询参数：

- `device_id`：必填
- `start_time`：可选，Unix 秒时间戳
- `end_time`：可选，Unix 秒时间戳

说明：

- 适合“最近一次发生了什么”“最新事件是什么”
- 返回的是单条事件，不是列表

返回要点：

- `data.id`
- `data.tag`
- `data.time`
- `data.deviceId`
- `data.detailDescription`
- `data.image`

### 5. 获取某个事件的图片

```http
GET /api/v1/skill/device/events/image
```

查询参数：

- `event_id`：必填

说明：

- 适合“给我看这条事件的图片”
- `event_id` 必须使用系统已经返回过的事件 ID，不要自己拼

返回要点：

- `data.id`
- `data.tag`
- `data.time`
- `data.deviceId`
- `data.detailDescription`
- `data.image`

### 6. 获取设备在线状态

```http
GET /api/v1/skill/device/online
```

查询参数：

- `device_id`：必填

返回要点：

- `data.deviceId`
- `data.isOnline`
- `data.isAlive`

说明：

- 适合“设备在线吗”“设备还活着吗”
- 返回字段较简单，按接口实际值直接解释即可

### 7. 获取设备电量

```http
GET /api/v1/skill/device/battery
```

查询参数：

- `device_id`：必填
- `start_time`：必填，Unix 秒时间戳
- `end_time`：必填，Unix 秒时间戳

说明：

- 必须满足 `start_time < end_time`
- 适合“查最近一段时间电量”这类请求

返回要点：

- `data.deviceId`
- `data.qoe`

## 使用约束

- Query 参数统一使用 `snake_case`，例如 `device_id`、`start_time`、`event_id`
- 截图接口请求体使用 `camelCase`，字段名固定为 `deviceId`
- 响应字段以实际返回为准，常见为 `camelCase`
- `limit` 和 `offset` 不能是负数
- 对于事件图片和最近事件，优先使用接口返回的 `image`
- 不要臆造不存在的接口路径，也不要把 `devices` 和 `device` 写混
- 如果需要按设备名操作，先通过设备列表确认目标设备，再继续调用后续接口

## 常见场景

### 查看当前有哪些设备

1. 调用 `GET /api/v1/skill/devices`
2. 把结果整理成可读设备清单

### 看某个设备当前画面

1. 先确认 `deviceId`
2. 调用 `POST /api/v1/skill/device/snapshot`
3. 返回截图结果中的 `imageUrl`

### 查看某个设备今天发生了什么

1. 先确认 `device_id`
2. 将“今天”换算成明确时间范围
3. 调用 `GET /api/v1/skill/device/events`
4. 按时间整理并总结事件

### 查看最近一个事件

1. 调用 `GET /api/v1/skill/device/events/latest`
2. 输出事件摘要和图片

## 错误处理

- 缺少 `TIVS_CLI_ID` 或 `TIVS_API_KEY`：明确提示缺少环境变量，不要伪造请求
- `deviceId` 或 `device_id` 缺失：提示用户补充目标设备
- `event_id` 缺失：提示用户先提供事件 ID，或先查询事件列表
- 时间参数非法或顺序错误：提示用户改为合法的 Unix 秒时间戳，并满足 `start_time < end_time`
- 设备列表为空：直接说明当前 Skill 下没有可操作设备，并提示用户检查设备管理站点
- 接口返回未知字段结构：只解释已确认字段，不要臆造含义

## 明确禁止

- 不要回显 `TIVS_API_KEY` 原文
- 不要把设备管理站点当成 API 接口
- 不要输出未经整理的长段原始 JSON 作为默认回答
