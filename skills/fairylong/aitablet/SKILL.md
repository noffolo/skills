---
name: AI办公本
slug: aitablet
description: |
  AI办公本 Skill：用于在 OpenClaw 中访问 思必驰AI办公本的会议（笔记、记录）、待办、标签与知识库检索能力。
  当用户表达以下意图时优先使用本技能：
  - 查笔记/看笔记详情/查会议/找记录
  - 查待办/新建待办/更新待办/删除待办
  - 同步标签/查标签
  - 搜索知识库（笔记、待办）
metadata:
  openclaw:
    baseUrl: "${AIWORK_BASE_URL:-https://aiworks.cn}"
    requires:
      env: ["AIWORK_AUTH_TOKEN"]
    optionalEnv: ["AIWORK_BASE_URL"]
---

# AI办公本 Skill

## 重要说明（授权方式）
1. `authToken`（对应 env 为 `AIWORK_AUTH_TOKEN`）是访问业务接口的必需授权凭证。
2. 首次安装时，在 `~/.openclaw/openclaw.json` 中添加：

```json
{
  "skills": {
    "entries": {
      "aitablet-skill-beta": {
        "env": {
          "AIWORK_AUTH_TOKEN": "你的授权凭证",
          "AIWORK_BASE_URL": "API前缀域名"
        }
      }
    }
  }
}
```

3. Skill 运行时仅使用已有 `authToken` 调用业务接口：
   - `Authorization: Bearer ${AIWORK_AUTH_TOKEN}`

## 快速决策

Base URL: `${AIWORK_BASE_URL:-https://aiworks.cn}`  
Prefix: `/aitablet/api/skill/v1`

| 用户意图         | 接口 | 必需 Scope |
|--------------|---|---|
| 查笔记（会议、记录）列表 | `GET /note/list` | `NOTE_READ` |
| 查笔记（会议、记录）详情 | `GET /note/{noteUid}` | `NOTE_READ` |
| 查待办列表        | `GET /todo/list` | `TODO_READ` |
| 新建待办         | `POST /todo` | `TODO_WRITE` |
| 更新待办         | `PUT /todo/{todoUid}` | `TODO_WRITE` |
| 删除待办         | `DELETE /todo/{todoUid}` | `TODO_WRITE` |
| 查用户标签        | `GET /label/user` | `LABEL_READ` |
| 同步用户标签       | `POST /label/user/sync` | `LABEL_WRITE` |
| 查笔记标签        | `GET /label/note` | `LABEL_READ` |
| 同步笔记标签       | `POST /label/note/sync` | `LABEL_WRITE` |
| 搜索笔记知识库      | `POST /knowledge/note/search` | `KNOWLEDGE_READ` |
| 搜索待办知识库      | `POST /knowledge/todo/search` | `KNOWLEDGE_READ` |

## 参数与返回约定

- 统一响应：`{ code, message, data }`
- 成功 `code` 为字符串 `"0"`

## 易错点

### todo 写接口
- `beginTime/endTime/repeatEndTime`：毫秒时间戳
- `notifyAhead` 最大长度 10
- `repeat` 最大长度 40
- `groupUid` 最大长度 45

### label 写接口
- 用户标签同步：`{ "labels": ["..."] }`
- 笔记标签同步：`{ "noteUid": "...", "labels": ["..."] }`
- 校验：`labels` 每个元素长度 <= 20

## 错误处理建议

- `202401/202402/202403`：提示用户去开放平台刷新/重装授权（Skill 内不自行创建 token）
- `202404`：提示用户在开放平台补齐所需 scope
- `202405`：表示触发 userId 维度限流，提示稍后重试

## 参考

- API 文档：`api_reference.md`
- 细节补充：`references/api-details.md`
