# GET https://sg-al-cwork-web.mediportal.com.cn/open-api/cwork-user/searchEmpByName

## 作用

按姓名模糊搜索内部员工（及文档所述外部联系人），用于在**查询他人 AI 费用**前解析 **`personId`**。本 Skill 能力二要求用户只输入姓名，Agent 通过本接口取得 `personId` 后再调用 `llm-cost/user-usage`。

**鉴权类型**

- `appKey`

**Headers**

- `appKey`：应用密钥（环境变量见脚本说明）
- `Content-Type`：GET 无 Body，可不传或按网关要求

**Query 参数**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `searchKey` | string | 是 | 搜索关键词，按姓名模糊搜索 |

## 请求 Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["searchKey"],
  "properties": {
    "searchKey": { "type": "string", "description": "姓名模糊搜索" }
  }
}
```

## 响应 Schema

统一为 `Result<T>`；成功时 `data` 为 `SearchAddressbookVO`，`personId` 位于 `data.inside.empList[]` 元素中。详见基础服务文档。

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "resultCode": { "type": "integer" },
    "resultMsg": { "type": ["string", "null"] },
    "data": {
      "type": "object",
      "description": "SearchAddressbookVO，inside.empList[].personId 为 Long"
    }
  }
}
```

## 脚本映射

- `../../scripts/cwork-user/search-emp-by-name.py`
