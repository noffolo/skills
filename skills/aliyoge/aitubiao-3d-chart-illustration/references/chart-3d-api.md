# Chart 3D Illustration API Reference

> **重要**：所有非流式响应都包裹在 `{ "code": 0, "msg": "ok", "data": { ... } }` 结构中。
> 下面的响应示例展示的是 `data` 字段内的业务数据。
> **即使 HTTP 状态码为 200，也必须检查 `code` 字段是否为 0。非 0 表示业务错误（如 AI贝不足）。**

## 1. Create 3D Illustration (一站式)

**Endpoint**: `POST {BASE_URL}/api/v1/agent/chart/create-3d-illustration`

一次调用完成：数据解析 → 图表渲染 → 截图 → 3D插图生成 → 保存到用户文件

**Headers**:
```
Authorization: Bearer {API_KEY}
Content-Type: application/json
```

**Request Body**:
```json
{
  "data": [["月份", "销售额"], ["1月", 1000], ["2月", 1500], ["3月", 2000]],
  "chartType": "basic-column",
  "style": "黄金材质",
  "chartTitle": "季度销售趋势"
}
```

| Field | Type | Required | Max Length | Description |
|-------|------|----------|-----------|-------------|
| data | (string\|number)[][] | Yes | - | 二维数组格式数据，第一行为表头，后续为数据行。数值型单元格用 number，文本用 string |
| chartType | string | Yes | - | 图表类型，见下方支持列表 |
| style | string | No | 500 | 内置风格名称（如 `gold`, `crystal`）或自定义描述（如"赛博朋克"），见下方内置风格列表 |
| chartTitle | string | No | 100 | 图表标题文字 |

**Response** (data 字段内容):
```json
{
  "success": true,
  "imageUrl": "https://oss.xxx/image/user/chart-3d-1711344000-abc.png",
  "chartType": "basic-column",
  "processingTime": "45000ms"
}
```

| Field | Type | Description |
|-------|------|-------------|
| success | boolean | 是否生成成功 |
| imageUrl | string | 3D插图图片 URL（已保存到用户文件） |
| chartType | string | 使用的图表类型 |
| processingTime | string | 总处理时间 |
| errorCode | string | 错误分类码，`chart_type_incompatible` 表示图表类型与数据不兼容 |
| error | string | 失败时的错误信息 |
| compatibleChartTypes | string[] | 当图表类型不兼容时，返回与数据兼容的3D图表类型列表 |

**注意**:
- 图表渲染 + 3D转换通常需要 30-120 秒，请设置足够的超时时间（建议 180s）。
- `imageUrl` 指向的图片已自动保存到用户的上传文件中。

**图表类型不兼容响应** (success=false, errorCode="chart_type_incompatible"):

当用户指定的图表类型与数据不兼容时，API 不会静默替换类型，而是返回错误和兼容的图表类型列表：
```json
{
  "code": 0,
  "msg": "ok",
  "data": {
    "success": false,
    "chartType": "basic-line",
    "errorCode": "chart_type_incompatible",
    "error": "Chart type \"basic-line\" requires the first column to contain time values (e.g., years, months, dates, quarters), but the column header \"品类\" and data values do not appear to be time-related.",
    "compatibleChartTypes": ["basic-column", "basic-pie", "funnel"]
  }
}
```

**业务错误响应** (code ≠ 0):
```json
{
  "code": 90001,
  "msg": "exp.shell.SHELL_NOT_ENOUGH"
}
```

| 错误码 | 含义 | 处理方式 |
|--------|------|---------|
| 90001 | AI贝不足 | 展示余额信息，建议充值或升级会员 |
| 14301 | 图片存储容量不足 | 用户图片存储空间已满，建议删除旧图片或升级会员 |

## 2. Get User Quota (通用配额查询)

**Endpoint**: `GET {BASE_URL}/api/v1/agent/quota`

查询用户当前 AI贝余额和所有 AI 功能的 AI贝消耗量。建议在生成3D插图前调用此接口预检。

**Headers**:
```
Authorization: Bearer {API_KEY}
```

**Response** (data 字段内容):
```json
{
  "shellBalance": 100,
  "shellLeft": 80,
  "shellNum": 20,
  "projectsUsed": 5,
  "projectsLimit": 50,
  "projectsRemaining": 45,
  "features": {
    "chart3dIllustrationCreate": { "key": "chart3dIllustrationCreate", "cost": 5, "unit": "次", "label": "图表3D插图", "billingModel": "per-request" },
    "chartProject": { "key": "chartProject", "cost": 10, "unit": "次", "label": "图表项目创建", "billingModel": "per-request" },
    "..."
  }
}
```

> **图表3D插图创建**：使用 `features.chart3dIllustrationCreate` 的 cost 计算费用（billingModel 为 per-request，总费用 = cost）。

## Supported Chart Types (11 types)

| chartType | 中文名称 | 数据结构 | 数据行数 | 数据要求 | 推荐场景 |
|-----------|---------|---------|---------|---------|---------|
| `basic-line` | 基础折线图 | 1列时间 + 1-8列数值 | 2-120行 | 数值或比率 | 时间序列/趋势数据 |
| `cascaded-area` | 层叠面积图 | 1列时间 + 1-8列数值 | 2-120行 | 数值或比率 | 多系列趋势对比 |
| `stacked-area` | 堆叠面积图 | 1列时间 + 1-12列数值 | 2-120行 | 数值或比率 | 累计趋势可视化 |
| `basic-pie` | 饼图 | 1列分类 + 1列数值 | 2-12行 | 比率(总和≈100%) | 占比/分布数据 |
| `basic-column` | 基础柱状图 | 1列分类 + 1列数值 | 2-120行 | 数值或比率 | 分类对比 |
| `check-in-bubble` | 打卡气泡图 | 1列维度 + 2-48列数值 | 2-48行 | 数值或比率 | 频次/热度数据 |
| `funnel` | 漏斗图 | 1列阶段名 + 1列数值 | 2-12行 | 数值或比率 | 转化率/流程数据 |
| `donut-progress` | 圆环进度图 | 1列名称 + 1列数值 | 仅1行 | 比率(0-100) | 占比/完成度 |
| `bar-progress` | 条形进度图 | 1列名称 + 1列数值 | 仅1行 | 比率(0-100) | 单指标进度 |
| `word-cloud` | 词云图 | 1列关键词 + 1列数值 | 12-120行 | 纯数值 | 关键词频率 |
| `liquid` | 水波图 | 1列名称 + 1列数值 | 1-48行 | 比率(0-100) | 单指标比率 |

## 3D Built-in Styles (内置风格)

`style` 字段支持两种用法：

### 1. 内置风格名称（推荐）

传入以下名称，系统自动解析为优化过的详细提示词。名称不区分大小写（`Gold`、`gold`、`GOLD` 均可）：

| style 值 | 效果描述 |
|----------|---------|
| `water` | 纯净水/液体质感 |
| `dollar` | 美元钞票材质 |
| `gold` | 真实黄金材质 |
| `chip` | 电脑芯片/电路板风格 |
| `fuzzy` | 毛茸茸/长毛毯质感 |
| `plants` | 灌木丛/绿植风格 |
| `steel` | 不锈钢金属质感 |
| `glass` | 多彩玻璃质感 |
| `watermelon` | 西瓜切片材质 |
| `bread` | 面包切片材质 |
| `crystal` | 水晶质感 |
| `container` | 集装箱风格 |
| `wood` | 橡木木纹质感 |

### 2. 自定义风格描述

传入任意文本描述（如 `"赛博朋克"`, `"黏土风"`, `"水彩风格"`），系统直接使用该描述作为风格提示词。
