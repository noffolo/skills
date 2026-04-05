---
name: daxiapi
version: 2.1.0
description: 大虾皮(daxiapi.com)金融数据API接口，获取A股市场宽度、行业相对强度、市场估值水平、个股动量排名，帮助进行自下向上选股。系统理论来自马克米勒维尼的VCP、欧奈尔的RPS、Wyckoff与价格行为学理论。此skill应在用户请求股票数据、市场分析、板块热度、个股动量等金融数据时触发。
metadata:
  category: 金融分析
  tags: [大虾皮, daxiapi, 金融分析, 股票, 市场热力图, 动量, 估值, 风格轮动]
  compatibility: [Linux, macOS, Windows]
---

# 大虾皮 API Skill

大虾皮(daxiapi.com)提供专业的A股量化数据API服务，本skill指导如何正确调用这些接口。

## 使用前提
可以先安装 `daxiapi-cli` 命令行工具，安装后可直接在终端调用：

```bash
npx daxiapi-cli@latest {command_args}
```
如果电脑没有安装 `Nodejs` 环境，可以使用HTTP工具来发送请求，具体参考 [使用方式](#使用方式) 部分。

## 关于数据更新

- 数据更新频率：每日收盘后开始更新，一般在17:00之前更新完K线、热力图和个股数据，在20:30更新市场恐慌指数等汇总信息

## 关于第三方API说明：
- 免费使用,无需VIP Token
- 数据更新频率高(实时或准实时)
- **可作为大虾皮API的补充数据源，必要的时候优先获取三方API的数据**
- 注意请求频率限制和数据缓存

## 核心概念

### 动量与形态指标

| 指标 | 全称 | 说明 |
|------|------|------|
| **CS** | Close-Short MA | 短期动量，股价与EMA20的乖离率。公式：`(ln(Close) - ln(EMA(ln(Close),20))) × 100`。入场阈值5-15，止损阈值<-5 |
| **SM** | Short-Medium MA | 中期动量，EMA20与EMA60的乖离率。值>0表示多头排列 |
| **ML** | Medium-Long MA | 长期动量，EMA60与EMA120的乖离率 |
| **RPS** | Relative Price Strength | 欧奈尔股价相对强度，全市场排名百分比。RPS>80为强势股 |
| **SCTR** | StockCharts Technical Rank | 技术排名，如60代表强于市场60%的股票 |

### Wyckoff与价格行为形态

| 形态 | 说明 |
|------|------|
| **VCP** | 波动收缩模式，供应吸收后可能上涨 |
| **SOS** | 强势走势行为（Sign of Strength） |
| **LPS** | 最后支撑点（Last Point of Support），突破后可买入 |
| **Spring** | 弹簧形态，假破位后快速回升 |
| **信号K** | 价格行为学入场信号，突破小区间 |

### 市场温度指标

| 指标 | 定义 | 关键阈值 |
|------|------|----------|
| **估值温度** | 市盈率历史百分位（0-100） | <20低估，>70高估 |
| **恐贪指数** | 市场贪婪恐惧程度（0-100） | 0-10极度恐惧（底部），90-100极度贪婪（顶部） |
| **趋势温度** | 股价高于MA60的占比（0-100） | <20低迷，>80过热 |
| **动量温度** | 动量中位数历史百分位 | <20超跌，>80高潮将至 |

### 风格轮动指标

| 指标 | 计算方式 | 解读 |
|------|----------|------|
| **大小盘波动差值** | 中证2000涨幅 - 沪深300涨幅 | >0小盘强，<0大盘强；±10%注意均值回归 |

## 认证方式

API支持两种认证方式：

### 1. X-API-Token 方式（推荐给VIP用户）

在请求头中添加 `X-API-Token`：

```javascript
fetch('/coze/get_index_k', {
    headers: { 'X-API-Token': 'your_32_char_token' }
})
```

**限流规则：**
- 每日上限：1000次
- 每分钟上限：10次
- 超限时返回 429 状态码

### 2. 固定Key方式（内部使用）

```javascript
// 方式：Bearer Token
headers: { 'Authorization': 'Bearer YOUR_ACCESS_TOKEN' }
```

## 使用方式

API 支持两种调用方式：

### 方式一：CLI 命令行工具（推荐）

使用 `daxiapi-cli` 命令行工具，安装后可直接在终端调用：

```bash
# 安装
npm install -g daxiapi-cli

# 配置Token
daxiapi config set token YOUR_API_TOKEN

# 使用示例
daxiapi market              # 市场概览
daxiapi market -d           # 市场温度
daxiapi sector              # 板块热力图
daxiapi stock 000001        # 查询个股
daxiapi search 三一重工     # 搜索股票

# 简写形式
dxp market                  # 使用 dxp 别名
```

**CLI 命令说明：**

| 命令 | 说明 |
|------|------|
| `daxiapi config set token <token>` | 设置API Token |
| `daxiapi config get` | 查看当前配置 |
| `daxiapi market` | 市场概览（指数、涨跌分布） |
| `daxiapi market -d` | 市场温度分析 |
| `daxiapi sector` | 板块热力图 |
| `daxiapi stock <codes>` | 查询个股（多个用逗号分隔） |
| `daxiapi kline <code>` | 获取个股K线数据 |
| `daxiapi search <keyword>` | 搜索股票/行业 |

**K线命令详解：**

```bash
# 获取日线数据（默认300条）
daxiapi kline 600519

# 获取最近500条日线
daxiapi kline 600519 -l 500

# 获取周线数据
daxiapi kline 600519 -t week

# 获取月线数据
daxiapi kline 600519 -t month

# 输出JSON格式
daxiapi kline 600519 -j

# 简单输出格式
daxiapi kline 600519 -s
```

### 方式二：HTTP 请求

直接调用 API 接口：

```javascript
// JavaScript Fetch
const response = await fetch('https://daxiapi.com/coze/get_index_k', {
    method: 'GET',
    headers: { 'X-API-Token': 'your_api_token' }
});
const data = await response.json();
```

```bash
# cURL
curl -H "X-API-Token: your_api_token" https://daxiapi.com/coze/get_market_data
```

## Token 保存与使用指南

**重要：** 调用API前，必须先确认用户是否已提供有效的 API Token。

### Token 获取方式
用户需要在 daxiapi.com 用户中心页面申请 API Token（仅限VIP用户）。

### AI 使用 Token 的推荐方式

#### 方式一：环境变量（推荐）
将 token 存储在环境变量中，代码中通过 `process.env` 读取：

```javascript
// .env 文件
DAXIAPI_TOKEN=your_32_char_token_here

// 代码中使用
const token = process.env.DAXIAPI_TOKEN;
fetch('/coze/get_index_k', {
    headers: { 'X-API-Token': token }
});
```

#### 方式二：配置文件
创建独立的配置文件（需加入 .gitignore）：

```javascript
// config/api.js
module.exports = {
    daxiapi: {
        token: 'your_32_char_token_here',
        baseUrl: 'https://daxiapi.com'
    }
};
```

#### 方式三：临时使用（仅限对话上下文）
若用户在对话中直接提供 token，AI 可临时用于测试，但需提醒用户：
- 不要在公开代码仓库中提交 token
- Token 泄露后应立即重新申请

### AI 调用流程

1. **首次使用**：询问用户是否有 API Token
   - 有 → 使用用户提供的 token
   - 无 → 提示用户去 daxiapi.com 申请

2. **存储 token**：根据项目类型选择存储方式
   - Node.js 项目 → 使用 `.env` 文件
   - Python 项目 → 使用 `.env` 或 `config.py`
   - 临时测试 → 在对话上下文中使用

3. **调用 API**：在请求头中携带 `X-API-Token`

### 安全提醒

- 永远不要在前端 JavaScript 代码中硬编码 token
- `.env` 文件必须加入 `.gitignore`
- Token 泄露后应立即在用户中心重新申请

## 市场分析框架

详细分析方法请参阅以下文档：

### 综合分析
详细分析方法请参阅 `references/market-analysis.md`，包括：
- CS指标阈值判断与市场宽度分析四维度
- 大小盘风格轮动分析方法
- 估值温度、恐贪指数、趋势温度、动量温度解读
- 个股技术面分析（动量/成交量/形态/步骤）
- 个股基本面分析（估值/财务/市值）
- 综合评估报告输出规范

### 市场风格分析
大小盘风格轮动的详细分析方法请参阅 `references/market-style-analysis.md`，包括：
- 大小盘波动差值指标详解
- 均值回归信号判断
- 运动方向分析方法
- 机构vs游资活跃度判断
- 完整分析框架与实战案例

### 市场温度分析
市场温度指标的详细解读方法请参阅 `references/market-temp-analysis.md`，包括：
- 估值温度、恐贪指数、趋势温度、动量温度四大指标详解
- 各指标的阈值判断与投资建议
- 完整分析流程与输出规范
- 实战案例与注意事项

### 行业热力图分析
行业板块热力图的详细解读方法请参阅 `references/sector-heatmap-analysis.md`，包括：
- 四维度分析方法（延续扩散、领涨、上升、反转）
- 完整输出规范与报告格式
- CS动量指标判断规则
- 重要要求与语言规范
- 实战案例与注意事项

## 可用API列表

详细API参数说明请参阅 `references/api-reference.md`。

### 市场数据类
| API路径 | 方法 | 功能描述 |
|---------|------|----------|
| `/coze/get_index_k` | GET | 获取上证指数K线数据 |
| `/coze/get_market_data` | GET | 获取市场整体数据（指数、涨跌分布、宽度） |
| `/coze/get_market_degree` | GET | 获取市场温度（冷热判断） |
| `/coze/get_market_style` | GET | 获取大小盘风格数据 |
| `/api/xingtai/high_60d.json` | GET | 获取带量创60日新高的股票 |
| `/coze/get_market_temp` | POST | 获取市场温度表格（估值/恐贪/情绪） |
| `/coze/get_market_value_data` | GET | 获取指数估值数据（PE/PB/温度） |
| `/coze/get_market_end_news` | GET | 获取收盘新闻 |

### 板块/概念类
| API路径 | 方法 | 功能描述 |
|---------|------|----------|
| `/coze/get_sector_data` | POST | 获取行业板块热力图 |
| `/coze/get_sector_rank_stock` | POST | 获取行业内个股排名 |
| `/coze/get_gn_table` | POST | 获取概念板块数据 |
| `/coze/get_gainian_stock` | POST | 获取概念内个股数据 |

### 个股查询类
| API路径 | 方法 | 功能描述 |
|---------|------|----------|
| `/coze/get_stock_data` | POST | 获取个股详细信息（动量、形态、估值） |
| `/coze/query_stock_data` | POST | 根据关键字查询股票/行业代码 |

### 第三方API
除了大虾皮官方API外,还可以使用以下第三方API获取补充数据,详细接口说明请参阅 `references/api-reference.md` 的"第三方API接口"章节。

#### 东方财富API
| 接口 | 功能描述 |
|------|----------|
| 指数行情数据 | 获取多个指数的实时行情,包括涨跌家数 |
| K线数据 | 获取股票、指数、ETF的K线历史数据 |
| 涨停股票池 | 获取当日涨停股票列表,包括连板数、封单金额 |
| 跌停股票池 | 获取当日跌停股票列表 |
| 炸板股票池 | 获取当日炸板股票列表 |
| 股指期货数据 | 获取IH、IC、IF、IM等期货合约数据 |

**涨跌停数据获取：**

涨跌停数据使用东方财富API获取，详细接口说明请参阅 `references/api-reference.md` 的"第三方API接口 - 东方财富API"章节。

- **涨停股票池**：获取当日涨停股票列表，包括连板数、封单金额、涨停原因等
- **跌停股票池**：获取当日跌停股票列表
- **炸板股票池**：获取当日炸板（涨停后打开）股票列表

这些接口免费使用，无需VIP Token，数据实时更新。

#### 集思录API
| 接口 | 功能描述 |
|------|----------|
| 可转债指数报价 | 获取可转债市场整体数据,包括等权指数、平均溢价率、市场温度 |

#### 同花顺API
| 接口 | 功能描述 |
|------|----------|
| 市场成交额数据 | 获取市场成交额历史数据,支持日线和分钟线 |

**第三方API特点:**
- 免费使用,无需VIP Token
- 数据更新频率高(实时或准实时)
- **可作为大虾皮API的补充数据源，必要的时候优先获取三方API的数据**
- 注意请求频率限制和数据缓存

### K线数据类
| API路径 | 方法 | 功能描述 |
|---------|------|----------|
| `/coze/get_index_k` | GET | 获取上证指数K线数据（需要VIP Token） |
| 腾讯财经API | GET | 免费获取个股K线数据，支持前复权 |
| 东方财富API | GET | 免费获取个股K线数据（备选数据源） |

**K线数据获取方式：**

1. **CLI方式（推荐）**：使用 `daxiapi kline <code>` 命令，自动选择最优数据源
2. **腾讯财经API**：直接调用腾讯接口，数据更稳定
3. **东方财富API**：备选数据源，当腾讯接口失败时自动切换

**数据源详解：**

首选：腾讯财经API
```bash
# 单只股票实时行情
curl -sL 'https://qt.gtimg.cn/q=sh600547' | iconv -f gbk -t utf-8

# K线数据（前复权）
# 格式：https://proxy.finance.qq.com/ifzqgtimg/appstock/app/newfqkline/get?_var=&param={市场代码}{股票代码},{类型},,,{条数},qfq
# 市场代码：sh(上海)、sz(深圳)
# 类型：day(日线)、week(周线)、month(月线)
curl 'https://proxy.finance.qq.com/ifzqgtimg/appstock/app/newfqkline/get?_var=&param=sh600519,day,,,300,qfq&r=0.123'
```

备选：东方财富API
```bash
# K线数据
# secid: 1.{代码}(上海)、0.{代码}(深圳)
# klt: 101(日线)、102(周线)、103(月线)
curl 'https://push2his.eastmoney.com/api/qt/stock/kline/get?secid=1.600519&klt=101&fqt=1&lmt=300'
```

**返回字段说明：**
- `date`: 交易日期
- `open`: 开盘价
- `close`: 收盘价
- `high`: 最高价
- `low`: 最低价
- `volume`: 成交量（手）
- `amount`: 成交额（万元）

## 响应格式

所有API返回统一格式：

```json
{
    "errCode": 0,
    "errMsg": "OK",
    "data": { ... }
}
```

**错误码说明：**
- `0` - 成功
- `401` - 认证失败（Token无效或非VIP）
- `404` - API不存在
- `429` - 请求频率超限
- `500` - 服务器错误

## 注意事项

1. **Token安全**：API Token应在服务端使用，避免在前端代码中暴露
2. **限流策略**：高频请求会触发限流，建议合理控制请求频率
3. **数据延迟**：部分数据可能存在延迟，不构成投资建议
4. **接口限制**：每天1000次，每分钟10次
