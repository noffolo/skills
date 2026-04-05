# 历史日K行情数据

> 分类: 股票行情数据 | 目录: `股票行情数据` | 索引见 `SKILL.md`


### 描述

获取个股历史日线行情数据，可指定股票代码和起止日期，按日期倒序排序

### 请求参数

| 名称 | 类型 | 必填 | 默认值 | 说明 |
|:---|:---|:---|:---|:---|
| `interfaceId` | `str` | 是 | "G2" | 接口ID |
| `stockCodes` | `str` | 是 | - | 支持查询单只股票和多只股票（单次查询不超过20个），如果是多只，以逗号隔开；示例：'000001',<br>'600519' |
| `startDate` | `str` | 否 | - | 开始日期 startDate和endDate区间不能超过一年，如超过数据会截断，如果都为空，<br>则查询最新交易日，示例：2023-01-01 |
| `endDate` | `str` | 否 | - | 结束日期 startDate和endDate区间不能超过一年，如超过数据会截断，如果都为空，<br>则查询最新交易日，示例：2023-12-31 |

### 返回参数

ResultData.data 为 List，元素为历史日K行情列表

| 名称 | 类型 | 是否必返回 | 说明 |
|:---|:---|:---|:---|
| `stockCode` | `str` | 否 | 股票代码 |
| `stockName` | `str` | 否 | 股票名称 |
| `tradeDate` | `str` | 否 | 交易日 |
| `newPrice` | `float` | 否 | 最新价 |
| `maxPrice` | `float` | 否 | 最高价 |
| `minPrice` | `float` | 否 | 最低价 |
| `openPrice` | `float` | 否 | 开盘价 |
| `yesterdayClosePrice` | `float` | 否 | 昨收价 |
| `chg` | `float` | 否 | 涨跌幅 |
| `chgMoney` | `float` | 否 | 涨跌额 |
| `volume` | `int` | 否 | 成交量 |
| `tradeMoney` | `float` | 否 | 成交额 |

### 调用示例

```python
from equal_data import EqualDataApi  
api = EqualDataApi('your API_KEY') 
# 调用接口
data = api.query_equal_data(
    interfaceId="G2",
    stockCodes=None,  # str  # 默认: 
    startDate=None,  # str  # 默认: 
    endDate=None,  # str  # 默认: 
)
```


