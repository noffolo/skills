# GET https://sg-al-cwork-web.mediportal.com.cn/open-api/llm-cost/user-usage

## 作用

查询指定用户在指定日期范围内的 AI 使用明细：总费用、总 Token、按产品（含嵌套模型）的明细。不传 `personId` 时表示**当前登录用户**；不传日期时默认**当天**（以服务端为准）。

**鉴权类型**

- `appKey`

**Headers**

- `appKey`：应用密钥（环境变量见脚本说明）

**Query 参数**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `personId` | integer (int64) | 否 | 用户 ID；不传则当前登录用户 |
| `startTime` | string | 否 | 开始日期 `YYYY-MM-DD`，默认当天 |
| `endTime` | string | 否 | 结束日期 `YYYY-MM-DD`，默认当天 |

## 请求 Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "personId": { "type": "integer" },
    "startTime": { "type": "string", "pattern": "^\\d{4}-\\d{2}-\\d{2}$" },
    "endTime": { "type": "string", "pattern": "^\\d{4}-\\d{2}-\\d{2}$" }
  }
}
```

## 响应 Schema

统一为 `Result<T>`；成功时 `data` 内含查询条件、汇总与产品/模型明细（结构以联调为准，与 OpenAPI 示例一致）。

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "resultCode": { "type": "integer" },
    "resultMsg": { "type": ["string", "null"] },
    "data": {
      "type": "object",
      "description": "含 query、summary、products 等明细结构"
    }
  }
}
```

### `data` 典型层级（用于向用户排版）

实际字段名以响应 JSON 为准；Agent 解析后按 **总览 → 产品 → 模型** 输出：

| 层级 | 含义 | 应呈现内容（有则列） |
|------|------|----------------------|
| **总览** | `summary` 或与 `data` 顶层等价汇总 | 查询范围内**用户整体**：输入 Token 合计、输出 Token 合计、费用合计等 |
| **产品** | `products[]` 中每一项 | **产品名称/标识**；该产品**小计**：输入 Token、输出 Token、费用等 |
| **模型** | 每个产品下的模型列表（如 `models`、`modelList` 或嵌套在 product 内） | **模型名**；该模型**输入 Token**、**输出 Token**（及其它返回字段） |

脚本 `user-usage.py` 会对 `data` 递归处理：凡**字段名**含 `token` 的数值，会额外生成 `字段名Display` 字符串（`≥1000` → `K`，`≥1_000_000` → `M`）。展示给用户时优先用 `*Display`。

加 `--format markdown` 时，成功时仅打印 **Markdown 表格**（与 `SKILL.md` 层级一致）；失败或非成功 `resultCode` 时仍打印 JSON 便于排错。

**顺序**：先输出总览 → 再 `products[0]` 的产品小计 + 其下各模型 → 再 `products[1]` … 以此类推。

## 脚本映射

- `../../scripts/llm-cost/user-usage.py`
