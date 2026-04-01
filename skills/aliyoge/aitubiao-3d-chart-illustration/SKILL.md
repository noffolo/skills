---
name: aitubiao-3d-illustration
version: 0.0.2
description: AI图表3D插图生成。根据用户数据和指定图表类型，生成3D风格化数据可视化插画。当用户想要将图表转为3D插画、创建3D风格图表时使用，触发词包括"3D图表"、"3D插图"、"图表转3D"、"3D illustration"、"3d chart"、"stylize chart"等。
---

# AI 图表3D插图生成

根据用户提供的数据和指定的图表类型，生成3D风格化数据可视化插画。

## 强制规则

**以下规则必须严格执行，不得跳过、变通或使用替代方案：**

1. **认证优先**：在执行任何操作之前，必须先检查凭证状态。认证未通过时，禁止执行任何后续步骤。
2. **按顺序执行**：工作流程的 5 个步骤必须按顺序执行，禁止跳步。
3. **费用确认前禁止调用生成接口**：必须成功查询配额、计算费用、并获得用户明确确认后，才能调用 `create-3d-illustration` 接口。
4. **仅通过 API 生成3D插图**：禁止使用本地工具（Blender、Three.js、matplotlib 等）生成3D可视化。无论 API 因何种原因失败，都**绝对禁止使用本地工具**，没有任何例外。API 失败时正确做法是停止并告知用户，不是寻找替代方案。
5. **401/403 立即停止**：任何步骤中收到 HTTP 401/403，立即停止并引导用户前往 [API Key 管理页面](https://app.aitubiao.com/setting/api-keys) 检查或重新创建 API Key。401/403 不是超时，禁止重试。
6. **超时/500 重试规则**：最多重试 3 次（间隔 5 秒），仍失败则停止并告知用户。

**⚠️ 以下想法是错误的，如果你发现自己在这样想，请立即停止：**
- ❌ "API 不可用，我可以用本地工具生成3D可视化作为替代" → 违反规则 4
- ❌ "至少让用户看到一些3D效果" → 本技能唯一输出方式是 aitubiao API
- ❌ "401 可能是暂时性的，重试几次" → 401 是认证失败，重试无意义，按规则 5 处理

## 认证

在调用任何 API 之前，先检查凭证状态。

### 检查凭证

读取凭证文件，判断认证状态：

```bash
cat ~/.aitubiao/credentials 2>/dev/null
```

根据结果判断：
- **文件不存在或为空** → 执行下方"配置凭证"流程
- **`API_KEY` 为空** → 执行下方"配置凭证"流程
- **`API_KEY` 不以 `sk_v1_` 开头** → 告知用户"当前 API Key 已失效，请前往 [API Key 管理页面](https://app.aitubiao.com/setting/api-keys) 重新创建一个 API Key"
- **`API_KEY` 格式正确** → 认证通过

认证通过后，加载环境变量：
```bash
source ~/.aitubiao/credentials
export BASE_URL="${BASE_URL:-https://api.aitubiao.com}"
```

### 配置凭证

1. 向用户索要 API Key（格式：`sk_v1_...`）。如果没有，引导用户前往 [API Key 管理页面](https://app.aitubiao.com/setting/api-keys) 创建一个新的 API Key，然后将创建好的 Key 粘贴回来。
2. 保存凭证：
```bash
mkdir -p ~/.aitubiao
cat > ~/.aitubiao/credentials << EOF
API_KEY=<用户提供的key>
BASE_URL=https://api.aitubiao.com
EOF
chmod 600 ~/.aitubiao/credentials
```
3. 重新读取文件验证配置是否成功。

凭证保存在 `~/.aitubiao/credentials`，跨会话持久生效。

## 服务架构

所有 API 使用统一的服务地址：

| 默认地址 | API前缀 | 认证方式 |
|---------|---------|---------|
| `https://api.aitubiao.com/` | `/api/v1/agent` | `Authorization: Bearer <API_KEY>` |

**重要**：所有非流式响应都包裹在统一格式中：
```json
{ "code": 0, "msg": "ok", "data": { ... } }
```
实际业务数据在 `data` 字段内。**即使 HTTP 状态码为 200，也必须检查 `code` 字段是否为 0，非 0 表示业务错误。**

## 支持的图表类型

仅以下 11 种图表类型支持转换为3D插图，详细的数据结构要求见 [chart-3d-api.md](references/chart-3d-api.md)。

`basic-line` | `cascaded-area` | `stacked-area` | `basic-pie` | `basic-column` | `check-in-bubble` | `funnel` | `donut-progress` | `bar-progress` | `word-cloud` | `liquid`

### 数据格式注意事项

- **比率值使用百分制**：如完成度75%必须传 `75`，禁止传 `0.75`
- **饼图特殊要求**：所有数值之和必须在99.5%-100%之间
- **时间序列图表**（basic-line、cascaded-area、stacked-area）：第一列必须是时间
- **圆环进度图和条形进度图**：仅支持1行数据

## 工作流程

**每一步必须在前一步完成后才能开始。禁止跳步。**

### 第一步：认证（前置条件：无）

运行检查凭证流程。认证未通过时按"认证"章节流程处理。

**认证未通过时，停止。不要读取用户数据，不要做任何分析。**

### 第二步：识别数据并选择图表类型（前置条件：第一步认证通过）

#### 2.1 获取数据

判断用户如何提供数据：

- **直接粘贴文本**：解析为二维数组格式 `(string|number)[][]`，第一行为表头。
- **本地文件**（CSV/TXT）：用 Read 工具读取，然后解析为二维数组。
- **Excel 文件**（.xlsx/.xls）：使用 xlsx skill 或 Read 工具读取，禁止手动编写 Python 脚本解析 XML。

**数据格式要求**：
API 接受 `data` 字段为 JSON 二维数组，第一行为表头，后续为数据行。数值类型的单元格应为 `number`，文本类型应为 `string`。

示例：
```json
[
  ["月份", "销售额", "利润"],
  ["1月", 1000, 200],
  ["2月", 1500, 350],
  ["3月", 2000, 500]
]
```

#### 2.2 确认图表类型

向用户展示解析后的数据（表格形式），并确认：
- 数据是否正确？
- 选择哪种图表类型？（展示上方支持的11种类型供选择）

如果用户不确定图表类型，根据数据特点推荐：
- **时间序列数据** → `basic-line`（折线图）或 `cascaded-area`（面积图）
- **分类占比数据** → `basic-pie`（饼图）或 `donut-progress`（圆环图）
- **分类对比数据** → `basic-column`（柱状图）
- **层级/流程数据** → `funnel`（漏斗图）
- **单个进度指标** → `bar-progress`（条形进度）或 `liquid`（水波图）

#### 2.3 选择3D风格（可选）

询问用户是否有特殊的3D风格要求。内置风格名称（直接传名称，系统自动解析为详细提示词，不区分大小写）：

`water` | `dollar` | `gold` | `chip` | `fuzzy` | `plants` | `steel` | `glass` | `watermelon` | `bread` | `crystal` | `container` | `wood`

用户也可以输入自定义风格描述（如"赛博朋克"、"黏土风"），系统直接使用。完整风格说明见 [chart-3d-api.md](references/chart-3d-api.md)。

### 第三步：检查配额并确认费用（前置条件：第二步数据和图表类型已确认）

在生成3D插图前，**必须**检查用户的 AI贝余额，并向用户确认费用后才能继续。

收到 401/403 按强制规则 5 处理。超时/500 按强制规则 6 处理。

#### 3.1 查询配额

```bash
curl -s --max-time 10 -X GET "${BASE_URL}/api/v1/agent/quota" \
  -H "Authorization: Bearer ${API_KEY}"
```

#### 3.2 计算总费用

使用 `features.chart3dIllustrationCreate` 的 cost 计算费用（billingModel 为 per-request，总费用 = cost）。

#### 3.3 向用户确认费用

**必须在调用生成接口前向用户展示费用确认信息，并等待用户确认后才能继续**：

```
本次操作将消耗 {cost} 个 AI贝（图表3D插图，按次计费）
当前余额: {shellBalance} 个 AI贝
操作后余额: {shellBalance - cost} 个 AI贝

是否继续？
```

- 如果 `shellBalance < cost`：告知用户当前 AI贝余额不足，需前往 aitubiao 网站购买会员或充值后再继续，**不要继续**

### 第四步：生成3D插图（前置条件：第三步用户已确认费用）

**只有用户明确确认费用后才能执行此步骤。**

**注意**：图表渲染 + 3D转换可能需要 60-120 秒，需设置足够的超时时间。

```bash
curl -s --max-time 180 -X POST "${BASE_URL}/api/v1/agent/chart/create-3d-illustration" \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "data": [["月份","销售额"],["1月",1000],["2月",1500],["3月",2000]],
    "chartType": "<图表类型>",
    "style": "<可选：3D风格描述>",
    "chartTitle": "<可选：图表标题>"
  }'
```

响应格式（需解析 `data` 字段）：
```json
{
  "code": 0,
  "msg": "ok",
  "data": {
    "success": true,
    "imageUrl": "https://oss.xxx/image/user/chart-3d-xxx.png",
    "chartType": "basic-column",
    "processingTime": "45000ms"
  }
}
```

完整请求/响应格式详见 [chart-3d-api.md](references/chart-3d-api.md)。

#### 4.1 图表类型不兼容处理

当返回 `data.errorCode === "chart_type_incompatible"` 时：
1. 向用户展示 `error` 中的不兼容原因
2. 展示 `compatibleChartTypes` 中可用的图表类型供选择
3. 用户选择新类型后，重新执行第四步

响应格式详见 [chart-3d-api.md](references/chart-3d-api.md)。

### 第五步：返回结果（前置条件：第四步生成成功）

向用户提供：
- 3D插图图片 URL（从 `data.imageUrl` 获取）
- 摘要：图表类型、处理时间
- 如有图片展示能力，直接展示3D插图图片

## 错误处理

| HTTP 状态码 | 处理方式 |
|------------|---------|
| 401/403 | 按强制规则 5：立即停止，引导用户前往 [API Key 管理页面](https://app.aitubiao.com/setting/api-keys) 检查 |
| 429 | 等待 30 秒后重试一次 |
| 500 | 按强制规则 6：重试最多 3 次 |

当 `code` 不为 0 时为业务错误（如 90001=AI贝不足，14301=存储容量不足），完整错误码说明见 [chart-3d-api.md](references/chart-3d-api.md)。

## API 参考

详细的接口规格说明见 [chart-3d-api.md](references/chart-3d-api.md)。
