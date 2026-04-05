# Coze API 详细参考文档

**Base URL:** `https://daxiapi.com/coze`

---

## GET 接口

### get_index_k
获取上证指数的K线数据（最近30天）

**请求方式:** `GET`

**请求示例:**
```javascript
fetch('/coze/get_index_k', {
    headers: { 'X-API-Token': 'your_token' }
})
```

**响应字段:**
| 字段 | 说明 |
|------|------|
| name | 指数名称 |
| klines[].date | 日期 |
| klines[].open | 开盘价 |
| klines[].close | 收盘价 |
| klines[].high | 最高价 |
| klines[].low | 最低价 |
| klines[].vol | 成交量 |

---

### get_market_data
获取A股市场主流指数信息，包括名称、涨跌幅、市场宽度等

**请求方式:** `GET`

**响应字段:**
| 字段 | 说明 |
|------|------|
| above_ma200_ratio | 全市场股票在200日均线之上的占比 |
| index[] | 主流指数列表 |
| index[].name | 指数名称 |
| index[].cs | 短期动量CS |
| index[].zdf | 当日涨跌幅(%) |
| index[].zdf5/zdf10/zdf20/zdf30 | 5/10/20/30日涨跌幅 |
| zdfRange | 涨跌幅区间分布 |

---

### get_market_degree
获取A股市场温度，判断市场冷热程度

**请求方式:** `GET`

**用途:** 市场冷清时考虑抄底，过热时考虑卖出

**响应内容:** 包含市场温度、估值指标、抄底信号等综合分析文本

---

### get_market_style
获取大小盘风格数据

**请求方式:** `GET`

**响应字段:**
| 字段 | 说明 |
|------|------|
| 日期 | 交易日期 |
| 大小盘波动差值 | 正值大盘强,负值小盘强 |

---

### get_60d_high_stocks
获取带量创60日新高的股票

**请求方式:** `GET`

**请求路径:** `/api/xingtai/high_60d.json`

**用途:** 筛选出近期突破60日高点且伴随成交量放大的强势股票,捕捉趋势突破机会

**请求示例:**
```javascript
fetch('https://daxiapi.com/api/xingtai/high_60d.json', {
    headers: { 'X-API-Token': 'your_token' }
})
```

**响应字段:**
| 字段 | 说明 |
|------|------|
| data[] | 股票列表 |
| data[].code/stockId | 股票代码 |
| data[].name | 股票名称 |
| data[].close/price | 收盘价 |
| data[].high/low | 最高/最低价 |
| data[].vol/vol1 | 当日/昨日成交量 |
| data[].vcs | 成交量动量(>0为放量) |
| data[].vma5 | 5日均量 |
| data[].cs | 短期动量CS |
| data[].sm | 中期动量SM |
| data[].ml | 长期动量ML |
| data[].rps_score | RPS相对强度 |
| data[].sctr | 技术排名百分比 |
| data[].zdf | 当日涨跌幅 |
| data[].zdf_5d/zdf_10d/zdf_20d/zdf_30d | 5/10/20/30日涨跌幅 |
| data[].ma20/ma50/ma150/ma200 | 各期均线 |
| data[].ema20 | 20日EMA |
| data[].isVCP | 是否VCP形态(1=是) |
| data[].isSOS | 是否SOS强势走势(1=是) |
| data[].isLPS | 是否LPS支撑点(1=是) |
| data[].isSpring | 是否弹簧形态(1=是) |
| data[].isCrossoverBox | 是否突破箱体(1=是) |
| data[].isIB | 是否Inside Bar(1=是) |
| data[].isNR4/isNR7 | 是否振幅收窄4/7天(1=是) |
| data[].isHigh1 | 是否价格行为学高1概念(1=是) |
| data[].isW | 是否W底形态(1=是) |
| data[].tags[] | 标签(Good/LPS/↑TR/H2/Sp) |
| data[].high_52w/low_52w | 52周高低点 |
| data[].pe_ttm | 市盈率TTM |
| data[].shizhi_lt | 流通市值 |
| data[].bkId/bkName | 所属板块代码/名称 |
| data[].rsi | RSI指标 |
| data[].alli_g/alli_r/alli_b | 鳄鱼线绿/红/蓝线 |
| data[].cg/cr/cb | Close与鳄鱼线距离 |
| data[].gr/rb | 鳄鱼线各线距离 |
| dates[] | 日期列表 |
| groups[] | 分组信息 |

**投资价值:**
- 创60日新高代表股票突破近期阻力位,展现强势特征
- 带量突破更加可靠,成交量放大确认资金流入
- 可结合动量指标(CS/SM/ML)和技术形态(VCP/SOS/LPS)筛选优质标的

---

### get_market_end_news
获取收盘新闻信息

**请求方式:** `GET`

**响应字段:**
| 字段 | 说明 |
|------|------|
| title | 新闻标题 |
| summary | 新闻摘要 |
| content | 新闻内容 |
| showTime | 发布时间 |
| uniqueUrl | 新闻链接 |

---

### get_market_value_data
获取市场主流指数估值数据（PE/PB/温度）

**请求方式:** `GET`

**用途:** 评估指数估值水平，指导定投和止盈

**投资建议:**
- 买入：20°C以下慢慢定投，10°C以下加量，5°C以下提升额度
- 卖出：60°C以上关注止盈，80°C以上分批止盈

**响应字段:**
| 字段 | 说明 |
|------|------|
| name | 指数名称 |
| PE | 市盈率 |
| PEPercentile | PE历史分位值 |
| PB | 市净率 |
| PBPercentile | PB历史分位值 |
| wendu | 综合温度（最重要指标） |

---


### get_gn_table
获取概念板块数据（资金流入、涨跌幅、涨幅7%股票个数）

**请求方式:** `POST`

---

### get_jsl_topics
获取集思录热门话题

**请求方式:** `GET`

---

## POST 接口

### get_stock_data
获取A股个股详细信息

**请求方式:** `POST`

**请求参数:**
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| code | string | 是 | 股票代码，多个用逗号分隔，最多20个 |

**请求示例:**
```javascript
fetch('/coze/get_stock_data', {
    method: 'POST',
    headers: {
        'X-API-Token': 'your_token',
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({ code: '000001,600031' })
})
```

**响应字段（重要）:**
| 字段 | 说明 |
|------|------|
| code/stockId | 股票代码 |
| name | 股票名称 |
| close/price | 收盘价 |
| zdf | 当日涨跌幅(%) |
| zdf_5d/zdf_10d/zdf_20d/zdf_30d | 5/10/20/30日涨跌幅 |
| cs | 短期动量（Close与EMA20乖离率） |
| sm | 中期动量（EMA20与EMA60乖离率） |
| ml | 长期动量（EMA60与EMA120乖离率） |
| rps_score | RPS相对强度（>80为强势股） |
| sctr | 技术排名百分比 |
| ma20/ma50/ma150/ma200 | 各期均线 |
| ema20 | 20日EMA |
| isVCP | 是否VCP形态（1=是） |
| isSOS | 是否SOS强势走势（1=是） |
| isLPS | 是否LPS支撑点（1=是） |
| isSpring | 是否弹簧形态（1=是） |
| isCrossoverBox | 是否突破箱体（1=是） |
| isIB | 是否Inside Bar（1=是） |
| isNR4/isNR7 | 是否振幅收窄4/7天（1=是） |
| tags[] | 标签（Good/LPS/↑TR/H2/Sp） |
| vol/vol1 | 当日/昨日成交量 |
| vcs | 成交量动量（>0为放量） |
| vma5 | 5日均量 |
| high_52w/low_52w | 52周高低点 |
| pe_ttm | 市盈率TTM |
| shizhi_lt | 流通市值 |
| bkId/bkName | 所属板块代码/名称 |
| gainian | 所属概念 |

---

### get_sector_data
获取行业板块热力图

**请求方式:** `POST`

**请求参数:**
| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| orderBy | string | 否 | cs | 排序指标：cs/zdf/zdf5/zdf10/zdf20/cs_avg/stock_cs_avg |
| lmt | integer | 否 | 5 | 返回天数 |

**请求示例:**
```javascript
fetch('/coze/get_sector_data', {
    method: 'POST',
    headers: {
        'X-API-Token': 'your_token',
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({ orderBy: 'zdf', lmt: 5 })
})
```

**响应字段:**
| 字段 | 说明 |
|------|------|
| csHeatmap | CS动量热力图（Markdown表格） |
| zdfHeatmap | 当日涨跌幅热力图 |
| crossover | 箱体突破板块信息 |
| topStocksTable | 龙头股表格 |
| cs_gt_ma20_names | CS>CS_MA20的板块名称 |
| cs_gt_5_names | CS>5的板块名称 |

---

### get_sector_rank_stock
获取特定行业的股票排名

**请求方式:** `POST`

**请求参数:**
| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| sectorCode | string | 是 | - | 行业代码（以BK开头） |
| orderBy | string | 否 | cs | 排序指标 |

**orderBy 可选值:**
- `cs` - 短期动量
- `sm` - 中期动量
- `zdf/zdf_5d/zdf_10d/zdf_20d/zdf_30d` - 涨跌幅
- `sctr` - 技术排名
- `cg/cr/cb` - 鳄鱼线乖离率

**请求示例:**
```javascript
fetch('/coze/get_sector_rank_stock', {
    method: 'POST',
    headers: {
        'X-API-Token': 'your_token',
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({ sectorCode: 'BK0477', orderBy: 'cs' })
})
```

---

### get_gainian_stock
根据概念获取股票信息

**请求方式:** `POST`

**请求参数:**
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| gnId | string | 是 | 概念代码 |

**请求示例:**
```javascript
fetch('/coze/get_gainian_stock', {
    method: 'POST',
    headers: {
        'X-API-Token': 'your_token',
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({ gnId: 'GN1234' })
})
```

---

### query_stock_data
根据关键字查询股票/行业代码

**请求方式:** `POST`

**请求参数:**
| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| q | string | 是 | - | 关键字/拼音/代码，多个用逗号分隔，最多10个 |
| type | string | 是 | stock | 类型：stock（个股）/ hy（行业） |

**请求示例:**
```javascript
// 查询个股
fetch('/coze/query_stock_data', {
    method: 'POST',
    headers: {
        'X-API-Token': 'your_token',
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({ q: '三一重工', type: 'stock' })
})

// 查询行业
fetch('/coze/query_stock_data', {
    method: 'POST',
    headers: {
        'X-API-Token': 'your_token',
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({ q: '机械', type: 'hy' })
})
```

**响应字段:**
| 字段 | 说明 |
|------|------|
| code | 股票/行业代码 |
| name | 名称 |
| pinyin | 拼音缩写 |
| type | 类型（stock/hy） |

---

## 错误处理

### 统一响应格式
```json
{
    "errCode": 0,
    "errMsg": "OK",
    "data": { ... }
}
```

### 错误码说明
| 错误码 | 说明 | 处理建议 |
|--------|------|----------|
| 0 | 成功 | - |
| 401 | Token无效或非VIP | 提示用户检查Token或申请VIP |
| 404 | API不存在 | 检查请求路径和方法 |
| 429 | 请求频率超限 | 等待后重试，每分钟限10次，每日限1000次 |
| 500 | 服务器错误 | 联系管理员 |

---

## 使用场景示例

### 场景1：分析市场整体情况
1. 调用 `get_market_data` 获取市场宽度
2. 调用 `get_market_degree` 获取市场温度
3. 调用 `get_market_style` 判断大小盘风格

### 场景2：自下向上选股
1. 调用 `get_sector_data` 找出强势行业
2. 调用 `get_sector_rank_stock` 获取行业内龙头股
3. 调用 `get_stock_data` 分析个股详细指标

### 场景3：查询特定股票
1. 调用 `query_stock_data` 搜索股票代码
2. 调用 `get_stock_data` 获取详细信息

### 场景4：定投决策
1. 调用 `get_market_value_data` 获取指数估值
2. 根据温度值决定定投金额

---

## 第三方API接口

除了大虾皮官方API外,还可以使用以下第三方API获取补充数据。

### 东方财富API

#### 1. 指数行情数据

**接口地址:** `GET https://push2.eastmoney.com/api/qt/ulist/get`

**功能说明:** 获取多个指数的实时行情数据,包括价格、涨跌幅、涨跌家数等信息。

**请求参数:**
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| fields | string | 是 | 返回字段列表,逗号分隔 |
| secids | string | 是 | 证券代码列表,格式: 市场.代码,逗号分隔 |
| ut | string | 是 | 用户token |

**请求示例:**
```bash
curl 'https://push2.eastmoney.com/api/qt/ulist/get?fltt=1&invt=2&fields=f12,f13,f14,f1,f2,f4,f3,f152,f6,f104,f105,f106&secids=1.000001,0.399001&ut=fa5fd1943c7b386f172d6893dbfba10b&pn=1&np=1&pz=20&dect=1&wbp2u=|0|0|0|0|web'
```

**响应字段:**
| 字段 | 说明 |
|------|------|
| f12 | 指数代码 |
| f13 | 市场代码(1=上海,0=深圳) |
| f14 | 指数名称 |
| f2 | 当前价格(实际值需除以100) |
| f3 | 涨跌幅百分比(实际值需除以100) |
| f4 | 涨跌额(实际值需除以100) |
| f6 | 成交额 |
| f104 | 上涨家数 |
| f105 | 下跌家数 |
| f106 | 平盘家数 |

**使用场景:**
- 首页指数行情展示
- 市场温度计算
- 涨跌家数统计

---

#### 2. K线数据

**接口地址:** `GET https://push2his.eastmoney.com/api/qt/stock/kline/get`

**功能说明:** 获取股票、指数、ETF的K线历史数据,支持日线、周线、月线等多种周期。

**请求参数:**
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| klt | string | 是 | K线类型: 101=日线,102=周线,103=月线 |
| secid | string | 是 | 证券代码,格式: 市场.代码(如: 1.000300) |
| fqt | string | 否 | 复权类型: 0=不复权,1=前复权,2=后复权 |
| lmt | number | 否 | 返回数据条数 |

**请求示例:**
```bash
curl 'https://push2his.eastmoney.com/api/qt/stock/kline/get?fields1=f1,f2,f3,f4,f5,f6&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f61&ut=7eea3edcaed734bea9cbfc24409ed989&end=29991010&klt=101&secid=1.000300&fqt=1&lmt=300'
```

**响应字段:**
klines数组中每个元素为逗号分隔的字符串:

| 位置 | 字段 | 说明 |
|------|------|------|
| 0 | date | 日期 |
| 1 | open | 开盘价 |
| 2 | close | 收盘价 |
| 3 | high | 最高价 |
| 4 | low | 最低价 |
| 5 | volume | 成交量(手) |

**使用场景:**
- 国家队ETF成交量统计
- 指数走势分析
- K线图表展示

---

#### 3. 涨停股票池

**接口地址:** `GET https://push2ex.eastmoney.com/getTopicZTPool`

**功能说明:** 获取当日涨停股票列表,包括涨停时间、封单金额、连板数等信息。

**请求参数:**
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| ut | string | 是 | 用户token |
| dpt | string | 是 | 部门代码,默认 wz.ztzt |
| Pageindex | number | 否 | 页码,从0开始 |
| pagesize | number | 否 | 每页数量,默认200 |
| date | string | 是 | 日期,格式: YYYYMMDD |

**请求示例:**
```bash
curl 'https://push2ex.eastmoney.com/getTopicZTPool?ut=7eea3edcaed734bea9cbfc24409ed989&dpt=wz.ztzt&Pageindex=0&pagesize=200&sort=fbt:asc&date=20240101'
```

**响应字段:**
| 字段 | 说明 |
|------|------|
| tc | 涨停总数 |
| qdate | 日期(YYYYMMDD) |
| pool[] | 涨停股票列表 |
| pool[].code | 股票代码 |
| pool[].name | 股票名称 |
| pool[].price | 涨停价 |
| pool[].fbt | 首次涨停时间 |
| pool[].zbc | 炸板次数 |
| pool[].lbc | 连板数 |
| pool[].fund | 封单金额 |
| pool[].reason | 涨停原因 |

**使用场景:**
- 涨跌停分析页面
- 市场情绪监控
- 连板股追踪

---

#### 4. 跌停股票池

**接口地址:** `GET https://push2ex.eastmoney.com/getTopicDTPool`

**功能说明:** 获取当日跌停股票列表,包括跌停时间、封单金额等信息。

**请求参数:**
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| ut | string | 是 | 用户token |
| dpt | string | 是 | 部门代码,默认 wz.ztzt |
| Pageindex | number | 否 | 页码,从0开始 |
| pagesize | number | 否 | 每页数量,默认200 |
| date | string | 是 | 日期,格式: YYYYMMDD |

**请求示例:**
```bash
curl 'https://push2ex.eastmoney.com/getTopicDTPool?ut=7eea3edcaed734bea9cbfc24409ed989&dpt=wz.ztzt&Pageindex=0&pagesize=200&sort=fund:asc&date=20240101'
```

**响应字段:**
| 字段 | 说明 |
|------|------|
| tc | 跌停总数 |
| qdate | 日期(YYYYMMDD) |
| pool[] | 跌停股票列表 |
| pool[].code | 股票代码 |
| pool[].name | 股票名称 |
| pool[].price | 跌停价 |
| pool[].fbt | 首次跌停时间 |
| pool[].fund | 封单金额 |

**使用场景:**
- 涨跌停分析页面
- 市场风险监控

---

#### 5. 炸板股票池

**接口地址:** `GET https://push2ex.eastmoney.com/getTopicZBPool`

**功能说明:** 获取当日炸板(涨停后打开)股票列表。

**请求参数:**
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| ut | string | 是 | 用户token |
| dpt | string | 是 | 部门代码,默认 wz.ztzt |
| Pageindex | number | 否 | 页码,从0开始 |
| pagesize | number | 否 | 每页数量,默认200 |
| date | string | 是 | 日期,格式: YYYYMMDD |

**请求示例:**
```bash
curl 'https://push2ex.eastmoney.com/getTopicZBPool?ut=7eea3edcaed734bea9cbfc24409ed989&dpt=wz.ztzt&Pageindex=0&pagesize=200&sort=fbt:asc&date=20240101'
```

**响应字段:**
| 字段 | 说明 |
|------|------|
| tc | 炸板总数 |
| qdate | 日期(YYYYMMDD) |
| pool[] | 炸板股票列表 |
| pool[].code | 股票代码 |
| pool[].name | 股票名称 |
| pool[].price | 当前价格 |
| pool[].fbt | 首次涨停时间 |
| pool[].zbc | 炸板次数 |

**使用场景:**
- 涨跌停分析页面
- 市场情绪分析

---

#### 6. 股指期货数据

**接口地址:** `GET https://futsseapi.eastmoney.com/list/custom/{codes}`

**功能说明:** 获取股指期货实时行情数据,包括IH、IC、IF、IM等合约。

**请求参数:**
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| callbackName | string | 否 | JSONP回调函数名 |
| orderBy | string | 否 | 排序字段,如 zdf |
| sort | string | 否 | 排序方式: asc/desc |
| pageSize | number | 否 | 每页数量,默认100 |
| pageIndex | number | 否 | 页码,从0开始 |
| token | string | 是 | API token |

**URL路径参数:**
- `{codes}`: 期货合约代码列表,逗号分隔
  - 格式: `220_IHM0,220_IHS1,220_IHM1,220_IHS2`
  - 220_IH: 上证50期货
  - 220_IC: 中证500期货
  - 220_IF: 沪深300期货
  - 220_IM: 中证1000期货
  - M0: 当月合约
  - M1: 下月合约
  - S1: 下季合约
  - S2: 隔季合约

**请求示例:**
```bash
curl 'https://futsseapi.eastmoney.com/list/custom/220_IHM0,220_IHS1,220_IHM1,220_IHS2?orderBy=zdf&sort=asc&pageSize=100&pageIndex=0&token=1101ffec61617c99be287c1bec3085ff'
```

**响应字段:**
| 字段 | 说明 |
|------|------|
| code | 合约代码 |
| name | 合约名称 |
| price | 当前价格 |
| zdf | 涨跌幅百分比 |
| ccl | 持仓量 |
| cclday | 日增仓 |
| jjs | 结算价 |

**使用场景:**
- 股指期货基差分析
- 期现套利参考
- 市场情绪判断

---

### 集思录API

#### 可转债指数报价

**接口地址:** `GET https://www.jisilu.cn/webapi/cb/index_quote/`

**功能说明:** 获取可转债市场整体数据,包括等权指数、平均价格、溢价率、市场温度等。

**请求参数:** 无

**请求示例:**
```bash
curl 'https://www.jisilu.cn/webapi/cb/index_quote/'
```

**响应字段:**
| 字段 | 说明 |
|------|------|
| cur_index | 等权指数 |
| cur_increase_rt | 涨跌幅百分比 |
| turnover_rt | 换手率 |
| avg_price | 平均价格 |
| avg_premium_rt | 平均溢价率 |
| temperature | 市场温度(0-100) |

**使用场景:**
- 可转债估值分析
- 市场温度监控
- 投资时机判断

---

### 同花顺API

#### 市场成交额数据

**接口地址:** `GET https://dq.10jqka.com.cn/fuyao/market_analysis_api/chart/v1/get_chart_data`

**功能说明:** 获取市场成交额历史数据,支持日线和分钟线。

**请求参数:**
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| chart_key | string | 是 | 图表类型: turnover_day=日线,turnover_minute=分钟线 |

**请求示例:**
```bash
curl 'https://dq.10jqka.com.cn/fuyao/market_analysis_api/chart/v1/get_chart_data?chart_key=turnover_day'
```

**响应字段:**
point_list数组中每个元素为数组:

| 位置 | 字段 | 说明 |
|------|------|------|
| 0 | timestamp | 时间戳(毫秒) |
| 1 | turnover | 成交额 |
| 2 | avg_turnover | 平均成交额 |

**使用场景:**
- 市场成交额分析
- 量能趋势判断
- 市场活跃度监控

---

## 第三方API注意事项

### 数据更新频率

| API | 更新频率 | 建议缓存时间 |
|-----|----------|--------------|
| 指数行情 | 实时(3秒) | 10秒 |
| K线数据 | 日终 | 30分钟 |
| 涨跌停数据 | 实时(1分钟) | 5分钟 |
| 股指期货 | 实时(3秒) | 10秒 |
| 可转债指数 | 实时(1分钟) | 10分钟 |
| 市场成交额 | 日终 | 30分钟 |

### 使用限制

1. **Token说明**: 项目中使用的token为公开API的通用token,可能存在以下限制:
   - 请求频率限制
   - 数据延迟
   - 功能限制

2. **建议**: 在生产环境中申请专用的API token

### 市场代码说明

| 代码 | 市场 |
|------|------|
| 1 | 上海证券交易所 |
| 0 | 深圳证券交易所 |
| 116 | 上海科创板 |

### 证券代码格式

- **股票**: `市场.代码`,如 `1.600000`(上海)、`0.000001`(深圳)
- **指数**: `市场.代码`,如 `1.000300`(沪深300)
- **ETF**: `市场.代码`,如 `1.510300`(沪深300ETF)
- **板块**: `90.BKxxxx`,如 `90.BK0001`

### 东方财富接口板块名称和代码

```
// 一级行业
{name: '石油石化', id: 'BK0464'},
    {name: '煤炭', id: 'BK0437'},
    {name: '有色金属', id: 'BK0478'},
    {name: '基础化工', id: 'BK1206'},
    {name: '建筑材料', id: 'BK1208'},
    {name: '公用事业', id: 'BK0427'},
    {name: '钢铁', id: 'BK0479'},
    {name: '综合', id: 'BK1217'},
    {name: '环保', id: 'BK0728'},
    {name: '建筑装饰', id: 'BK1209'},
    {name: '电力设备', id: 'BK1200'},
    {name: '农林牧渔', id: 'BK0433'},
    {name: '机械设备', id: 'BK1205'},
    {name: '电子', id: 'BK1201'},
    {name: '交通运输', id: 'BK1210'},
    {name: '家用电器', id: 'BK0456'},
    {name: '轻工制造', id: 'BK1212'},
    {name: '纺织服饰', id: 'BK0436'},
    {name: '通信', id: 'BK1215'},
    {name: '汽车', id: 'BK1211'},
    {name: '房地产', id: 'BK1202'},
    {name: '国防军工', id: 'BK1204'},
    {name: '医药生物', id: 'BK1216'},
    {name: '商贸零售', id: 'BK1213'},
    {name: '美容护理', id: 'BK1035'},
    {name: '食品饮料', id: 'BK0438'},
    {name: '非银金融', id: 'BK1203'},
    {name: '社会服务', id: 'BK1214'},
    {name: '银行', id: 'BK1283'},
    {name: '计算机', id: 'BK1207'},
    {name: '传媒', id: 'BK0486'},
    // 二级行业
    {name: '油服工程', id: 'BK1275'},
    {name: '油气开采Ⅱ', id: 'BK1276'},
    {name: '贵金属', id: 'BK0732'},
    {name: '焦炭Ⅱ', id: 'BK1249'},
    {name: '玻璃玻纤', id: 'BK0546'},
    {name: '农化制品', id: 'BK0731'},
    {name: '化学原料', id: 'BK1019'},
    {name: '炼化及贸易', id: 'BK1274'},
    {name: '非金属材料Ⅱ', id: 'BK1020'},
    {name: '能源金属', id: 'BK1015'},
    {name: '电网设备', id: 'BK0457'},
    {name: '工业金属', id: 'BK1287'},
    {name: '元件', id: 'BK0459'},
    {name: '冶钢原料', id: 'BK1228'},
    {name: '燃气Ⅱ', id: 'BK1028'},
    {name: '地面兵装Ⅱ', id: 'BK1229'},
    {name: '电力', id: 'BK0428'},
    {name: '种植业', id: 'BK1261'},
    {name: '特钢Ⅱ', id: 'BK1227'},
    {name: '煤炭开采', id: 'BK1250'},
    {name: '化学纤维', id: 'BK0471'},
    {name: '航运港口', id: 'BK0450'},
    {name: '农业综合Ⅱ', id: 'BK1257'},
    {name: '化学制品', id: 'BK0538'},
    {name: '体育Ⅱ', id: 'BK1273'},
    {name: '专业工程', id: 'BK1248'},
    {name: '贸易Ⅱ', id: 'BK0484'},
    {name: '基础建设', id: 'BK1247'},
    {name: '综合Ⅱ', id: 'BK0539'},
    {name: '金属新材料', id: 'BK1288'},
    {name: '普钢', id: 'BK1226'},
    {name: '电子化学品Ⅱ', id: 'BK1039'},
    {name: '环境治理', id: 'BK1235'},
    {name: '水泥', id: 'BK0424'},
    {name: '轨交设备Ⅱ', id: 'BK1236'},
    {name: '小金属', id: 'BK1027'},
    {name: '风电设备', id: 'BK1032'},
    {name: '装修建材', id: 'BK0476'},
    {name: '通信设备', id: 'BK0448'},
    {name: '商用车', id: 'BK1264'},
    {name: '其他家电Ⅱ', id: 'BK1243'},
    {name: '塑料', id: 'BK0454'},
    {name: '动物保健Ⅱ', id: 'BK1254'},
    {name: '工程咨询服务Ⅱ', id: 'BK0726'},
    {name: '光学光电子', id: 'BK1038'},
    {name: '物流', id: 'BK0422'},
    {name: '橡胶', id: 'BK1018'},
    {name: '工程机械', id: 'BK0739'},
    {name: '专用设备', id: 'BK0910'},
    {name: '农产品加工', id: 'BK1256'},
    {name: '房地产服务', id: 'BK1045'},
    {name: '环保设备Ⅱ', id: 'BK1234'},
    {name: '家居用品', id: 'BK0440'},
    {name: '航海装备Ⅱ', id: 'BK1230'},
    {name: '纺织制造', id: 'BK1224'},
    {name: '照明设备Ⅱ', id: 'BK1245'},
    {name: '通用设备', id: 'BK0545'},
    {name: '林业Ⅱ', id: 'BK1255'},
    {name: '小家电', id: 'BK1244'},
    {name: '消费电子', id: 'BK1037'},
    {name: '摩托车及其他', id: 'BK1263'},
    {name: '医药商业', id: 'BK1042'},
    {name: '饰品', id: 'BK0734'},
    {name: '其他电子Ⅱ', id: 'BK1223'},
    {name: '装修装饰Ⅱ', id: 'BK0725'},
    {name: '中药Ⅱ', id: 'BK1040'},
    {name: '个护用品', id: 'BK1251'},
    {name: '厨卫电器', id: 'BK1240'},
    {name: '电池', id: 'BK1033'},
    {name: '家电零部件Ⅱ', id: 'BK1242'},
    {name: '文娱用品', id: 'BK1266'},
    {name: '养殖业', id: 'BK1259'},
    {name: '造纸', id: 'BK1267'},
    {name: '汽车服务', id: 'BK1016'},
    {name: '专业服务', id: 'BK1043'},
    {name: '其他电源设备Ⅱ', id: 'BK1034'},
    {name: '食品加工', id: 'BK1280'},
    {name: '黑色家电', id: 'BK1241'},
    {name: '渔业', id: 'BK1260'},
    {name: '非白酒', id: 'BK1279'},
    {name: '饲料', id: 'BK1258'},
    {name: '汽车零部件', id: 'BK0481'},
    {name: '服装家纺', id: 'BK1225'},
    {name: '专业连锁Ⅱ', id: 'BK1270'},
    {name: '白色家电', id: 'BK1239'},
    {name: '航空装备Ⅱ', id: 'BK1231'},
    {name: '房地产开发', id: 'BK0451'},
    {name: '电机Ⅱ', id: 'BK1030'},
    {name: '一般零售', id: 'BK0482'},
    {name: '乘用车', id: 'BK1262'},
    {name: '医疗器械', id: 'BK1041'},
    {name: '生物制品', id: 'BK1044'},
    {name: '饮料乳品', id: 'BK1282'},
    {name: '光伏设备', id: 'BK1031'},
    {name: '调味发酵品Ⅱ', id: 'BK1278'},
    {name: '铁路公路', id: 'BK0421'},
    {name: '多元金融', id: 'BK0738'},
    {name: '自动化设备', id: 'BK1237'},
    {name: '化学制药', id: 'BK0465'},
    {name: '半导体', id: 'BK1036'},
    {name: '包装印刷', id: 'BK1265'},
    {name: '军工电子Ⅱ', id: 'BK1233'},
    {name: '航天装备Ⅱ', id: 'BK1232'},
    {name: '休闲食品', id: 'BK1281'},
    {name: '计算机设备', id: 'BK0735'},
    {name: '化妆品', id: 'BK1252'},
    {name: '医疗美容', id: 'BK1253'},
    {name: '证券Ⅱ', id: 'BK0473'},
    {name: '房屋建设Ⅱ', id: 'BK1246'},
    {name: '医疗服务', id: 'BK0727'},
    {name: '教育', id: 'BK0740'},
    {name: '银行Ⅱ', id: 'BK0475'},
    {name: '互联网电商', id: 'BK1268'},
    {name: '航空机场', id: 'BK0420'},
    {name: '出版', id: 'BK1218'},
    {name: '通信服务', id: 'BK0736'},
    {name: '酒店餐饮', id: 'BK1271'},
    {name: '白酒Ⅱ', id: 'BK1277'},
    {name: 'IT服务Ⅱ', id: 'BK1238'},
    {name: '保险Ⅱ', id: 'BK0474'},
    {name: '电视广播Ⅱ', id: 'BK1219'},
    {name: '广告营销', id: 'BK1220'},
    {name: '游戏Ⅱ', id: 'BK1046'},
    {name: '软件开发', id: 'BK0737'},
    {name: '旅游及景区', id: 'BK1272'},
    {name: '数字媒体', id: 'BK1221'},
    {name: '旅游零售Ⅱ', id: 'BK1269'},
    {name: '影视院线', id: 'BK1222'}
```
