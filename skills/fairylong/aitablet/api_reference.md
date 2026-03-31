# AI办公本 OpenClaw Skill API 参考文档

## 1. 概述

### 1.1 接口基础信息

| 项目 | 说明 |
|---|---|
| 协议 | HTTP/HTTPS |
| 统一前缀 | `/aitablet/api/skill/v1` |
| 数据格式 | `application/json; charset=UTF-8` |
| 鉴权方式 | `Authorization: Bearer {AIWORK_AUTH_TOKEN}`（受保护接口） |

### 1.2 通用响应结构

```json
{
  "code": "0",
  "message": "success",
  "data": {}
}
```

- `code`：`"0"` 表示成功，其他为业务错误码。
- `message`：错误或成功消息。
- `data`：返回数据，可能是对象、数组或 `null`。

### 1.3 授权与 Scope

当前系统使用以下 Scope（大写）：

- `NOTE_READ`
- `TODO_READ`
- `TODO_WRITE`
- `LABEL_READ`
- `LABEL_WRITE`
- `KNOWLEDGE_READ`

> 说明：本文件为 Skill 运行时接口文档，不包含开放平台侧的 3 个授权管理接口。
> `AIWORK_AUTH_TOKEN` 由开放平台在安装 Skill 时下发给 OpenClaw，用户可在安装时选择 scope，并支持永久授权。

---

## 2. 笔记接口

> 需要 Scope：`NOTE_READ`

### 2.1 查询笔记列表

- **GET** `/aitablet/api/skill/v1/note/list`
- Header：`Authorization: Bearer {AIWORK_AUTH_TOKEN}`

查询参数：

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| pageNum | Integer | 否 | 默认 1 |
| pageSize | Integer | 否 | 默认 10，范围 1~100 |
| orderBy | String | 否 | `createTime` / `updateTime` |
| startTime | String | 否 | 格式 `yyyy-MM-dd HH:mm:ss` |
| endTime | String | 否 | 格式 `yyyy-MM-dd HH:mm:ss` |
| keyword | String | 否 | 标题关键字 |

### 2.2 查询笔记详情

- **GET** `/aitablet/api/skill/v1/note/{noteUid}`
- Header：`Authorization: Bearer {AIWORK_AUTH_TOKEN}`

返回核心字段（`SkillNoteVO`）：

- `noteUid`, `title`, `createTime`, `updateTime`, `labels`
- `type`, `groupName`, `version`, `top`, `encryptType`
- `asrContent`, `summaryContent`, `insightContent`, `ocrContent`

---

## 3. 待办接口

### 3.1 查询待办列表

- **GET** `/aitablet/api/skill/v1/todo/list`
- Scope：`TODO_READ`
- Header：`Authorization: Bearer {AIWORK_AUTH_TOKEN}`

查询参数：

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| status | Integer | 否 | `null`全部，`0`未完成，`1`已完成 |
| beginTime | Long | 否 | 开始时间（毫秒时间戳） |
| endTime | Long | 否 | 结束时间（毫秒时间戳） |
| pageNum | Integer | 否 | 页码 |
| pageSize | Integer | 否 | 每页大小 |


### 3.2 创建待办

- **POST** `/aitablet/api/skill/v1/todo`
- Scope：`TODO_WRITE`
- Header：`Authorization: Bearer {AIWORK_AUTH_TOKEN}`

请求体（`SkillTodoForm`）：

```json
{
  "todo": "完成周报",
  "beginTime": 1761922800000,
  "endTime": 1761926400000,
  "label": "工作",
  "important": true,
  "done": false,
  "notifyAhead": "30m",
  "repeat": "weekly",
  "repeatEndTime": 1764601200000,
  "repeatCount": 10,
  "groupUid": "1000002643-DEFAULT"
}
```

字段校验：

- `notifyAhead` 最大长度 10
- `repeat` 最大长度 40
- `groupUid` 最大长度 45

### 3.3 更新待办

- **PUT** `/aitablet/api/skill/v1/todo/{todoUid}`
- Scope：`TODO_WRITE`
- Header：`Authorization: Bearer {AIWORK_AUTH_TOKEN}`
- 请求体同 `SkillTodoForm`

### 3.4 删除待办

- **DELETE** `/aitablet/api/skill/v1/todo/{todoUid}`
- Scope：`TODO_WRITE`
- Header：`Authorization: Bearer {AIWORK_AUTH_TOKEN}`

### 3.5 待办返回字段（`SkillTodoVO`）

时间字段已统一为毫秒时间戳：

- `beginTime`, `endTime`, `repeatEndTime`
- `syncTime`, `finishTime`, `createTime`, `updateTime`

其他字段：

- `uid`, `todo`, `label`, `important`, `done`, `notifyAhead`, `repeat`, `repeatCount`, `groupUid`

---

## 4. 标签接口

### 4.1 查询用户标签

- **GET** `/aitablet/api/skill/v1/label/user`
- Scope：`LABEL_READ`
- Header：`Authorization: Bearer {AIWORK_AUTH_TOKEN}`

响应：

```json
{
  "code": "0",
  "message": "success",
  "data": {
    "labels": ["工作", "学习"]
  }
}
```

### 4.2 同步用户标签

- **POST** `/aitablet/api/skill/v1/label/user/sync`
- Scope：`LABEL_WRITE`
- Header：`Authorization: Bearer {AIWORK_AUTH_TOKEN}`

请求体：

```json
{
  "labels": ["工作", "学习"]
}
```

校验规则：`labels` 中每个字符串长度不能超过 20。

### 4.3 查询笔记标签

- **GET** `/aitablet/api/skill/v1/label/note`
- Scope：`LABEL_READ`
- Header：`Authorization: Bearer {AIWORK_AUTH_TOKEN}`
- 参数：`noteUids`（可多值）

### 4.4 同步笔记标签

- **POST** `/aitablet/api/skill/v1/label/note/sync`
- Scope：`LABEL_WRITE`
- Header：`Authorization: Bearer {AIWORK_AUTH_TOKEN}`

请求体：

```json
{
  "noteUid": "100882c4-f07b-47fd-8e5e-0fcb29fa2f5f",
  "labels": ["复盘", "重点"]
}
```

---

## 5. 知识库检索接口

> 需要 Scope：`KNOWLEDGE_READ`

### 5.1 搜索笔记知识库

- **POST** `/aitablet/api/skill/v1/knowledge/note/search`
- Header：`Authorization: Bearer {AIWORK_AUTH_TOKEN}`

### 5.2 搜索待办知识库

- **POST** `/aitablet/api/skill/v1/knowledge/todo/search`
- Header：`Authorization: Bearer {AIWORK_AUTH_TOKEN}`

请求体（`SkillKnowledgeSearchForm`）：

```json
{
  "query": "本周项目进度",
  "startTime": 1761609600000,
  "endTime": 1762214400000,
  "topN": 10
}
```

- `query` 必填，不能为空。
- `topN` 默认 10。

响应对象（`SkillKnowledgeVO`）：

- `uid`, `title`, `score`, `createTime`, `type`（`note` / `todo`）
- `contentFragments[]`：`content`, `score`, `fragmentType`

---

## 6. 错误码（关键）

### 6.1 授权相关（2024xx）

| code | message | 含义 |
|---|---|---|
| 202400 | 授权凭证为空 | 未提供 Authorization |
| 202401 | 授权凭证不存在 | token 不存在 |
| 202402 | 授权凭证已过期 | token 过期 |
| 202403 | 授权凭证已失效 | token 状态失效 |
| 202404 | 授权范围不足 | 缺少所需 scope |
| 202405 | Too many requests, please retry later | 触发 userId 维度限流 |

### 6.2 参数/业务相关（示例）

| code | message | 含义 |
|---|---|---|
| 201600 | 参数错误 | 通用参数校验失败 |
| 201602 | 待办不存在或无权限 | `todoUid` 不存在或无权访问 |
| 201613 | 内部服务异常 | 标签同步内部异常（如入库异常） |

---

## 7. 调用建议

1. Skill 运行时直接使用安装时下发的授权码，不在 Skill 内创建/删除授权。
2. 受保护接口统一携带 `Authorization: Bearer {AIWORK_AUTH_TOKEN}`。
3. 对 202401/202402/202403 提示用户在开放平台刷新或重装授权。
4. 对 202404 提示用户在开放平台补齐所需 scope。
5. 对 `todo` 与 `label` 写接口做好幂等重试与参数长度校验。
6. 对 `202405`，提示稍后重试，避免高频并发调用。


## 4. 调用建议

1. Skill 运行时仅使用安装时下发的 `AIWORK_AUTH_TOKEN`。  
2. 受保护接口统一携带 `Authorization: Bearer {AIWORK_AUTH_TOKEN}`。  
3. 对 `202401/202402/202403`，提示用户刷新/重装授权。  
4. 对 `202404`，提示用户补齐 scope。  
