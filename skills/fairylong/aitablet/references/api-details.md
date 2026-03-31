# API Details

## 1) 通用响应

```json
{
  "code": "0",
  "message": "success",
  "data": {}
}
```

- 成功：`code == "0"`
- 失败：`code != "0"`

## 2) 授权说明（Skill 运行时）

- Skill 运行时只消费已有 `AIWORK_AUTH_TOKEN`。
- Skill 不调用开放平台侧的授权管理接口。
- token 在安装 Skill 时由平台下发给 OpenClaw。

## 3) 关键错误码

| code | message | 说明 |
|---|---|---|
| 202400 | Authorization token is required | 未传 Authorization |
| 202401 | Authorization token is invalid | token 无效 |
| 202402 | Authorization token has expired | token 过期 |
| 202403 | Authorization token is disabled | token 失效 |
| 202404 | Authorization scope is insufficient | scope 不匹配 |
| 202405 | Too many requests, please retry later | 触发 userId 维度限流 |
| 201600 | 参数非法 | 请求参数不合法 |
| 201602 | 记录不存在 | todo 不存在或无权限 |
| 201613 | 内部服务异常 | 服务内部异常 |

## 4) Scope 速查

| Scope | 能力 |
|---|---|
| NOTE_READ | 读笔记 |
| TODO_READ | 读待办 |
| TODO_WRITE | 写待办 |
| LABEL_READ | 读标签 |
| LABEL_WRITE | 写标签 |
| KNOWLEDGE_READ | 知识库检索 |

## 5) 时间字段规范

- Todo 相关时间统一为 Unix 毫秒时间戳（`Long`）。
- `beginTime/endTime/repeatEndTime/syncTime/finishTime/createTime/updateTime` 均为毫秒格式。

## 6) 校验规则

- `SkillLabelForm.labels`：每个元素长度 <= 20
- `SkillTodoForm.notifyAhead`：长度 <= 10
- `SkillTodoForm.repeat`：长度 <= 40
- `SkillTodoForm.groupUid`：长度 <= 45
