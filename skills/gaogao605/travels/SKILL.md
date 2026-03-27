---
name: fbt-travel
description: 分贝通旅行助手 - 一站式酒店预订、机票预订服务。支持酒店搜索、房型查询、预订下单；航班搜索、舱位查询、机票预订、改期、退票。
version: 1.0.0
metadata: {"openclaw": {"emoji": "🧳", "category": "travel", "tags": ["分贝通", "酒店", "机票", "航班", "预订", "旅行"], "requires": {"bins": ["python3"]}, "required": true}}
---
# 分贝通旅行助手

一站式企业差旅服务，整合酒店预订和机票预订功能。

---

## 🔐 鉴权流程（必须先完成）

**重要**：使用任何功能前，用户必须先完成鉴权流程。鉴权成功后获得的凭证会自动保存在 `~/.fbt-auth.json` 文件中，新会话会自动沿用。

### 鉴权步骤

**步骤 1：发送验证码**
```
用户: 分贝通登录
AI: 请输入您的手机号

用户: 13800138000
AI: ✅ 验证码已发送，请在5分钟内输入
```

**步骤 2：验证并获取凭证**
```
用户: 1234
AI: 🎉 认证成功！现在可以使用分贝通旅行服务了
```

### 鉴权命令

```bash
# 发送验证码
python3 scripts/auth.py send <手机号>

# 验证验证码
python3 scripts/auth.py verify <手机号> <验证码>

# 查看鉴权状态
python3 scripts/auth.py status
```

---

## 🏨 酒店服务

### 1. 搜索酒店

**触发词**：订酒店、搜酒店、找酒店 + 城市/关键词

**执行命令**：
```bash
python3 scripts/hotel_api.py search <城市> <关键词> [入住日期] [退房日期]
```

**示例**：
```bash
python3 scripts/hotel_api.py search 北京市 三元桥附近 2026-03-26 2026-03-27
```

### 2. 查看房型价格

**触发词**：回复酒店序号（如"1"）

**执行命令**：
```bash
python3 scripts/hotel_api.py price <酒店ID> <入住日期> <退房日期>
```

### 3. 查看酒店详情和评论

**触发词**：回复"序号-详情"（如"1-详情"）

**执行命令**：
```bash
python3 scripts/hotel_api.py detail <酒店ID>
python3 scripts/hotel_api.py comment <酒店ID>
```

### 4. 创建酒店订单

**触发词**：回复"房型序号-产品序号"（如"1-1"）+ 提供入住人信息

**执行命令**：
```bash
python3 scripts/hotel_api.py order <酒店ID> <房型ID> <产品ID> <入住日期> <退房日期> <总价> <入住人姓名> <入住人手机号>
```

### 5. 查询/取消酒店订单

**触发词**：查看订单、取消订单

**执行命令**：
```bash
python3 scripts/hotel_api.py query_order <订单ID>
python3 scripts/hotel_api.py cancel_order <订单ID> [取消原因]
```

---

## ✈️ 机票服务

### 1. 搜索航班

**触发词**：某地到某地航班、查机票、搜航班 + 日期

**执行命令**：
```bash
python3 scripts/flight_search.py <出发城市> <到达城市> <日期>
```

**示例**：
```bash
python3 scripts/flight_search.py 北京 上海 2026-04-02
```

### 2. 查看舱位价格

**触发词**：查看航班详情、这个航班的舱位

**执行命令**：
```bash
python3 scripts/flight_price.py <出发机场三字码> <到达机场三字码> <日期> <航班号>
```

**示例**：
```bash
python3 scripts/flight_price.py PEK SHA 2026-04-02 CA1501
```

### 3. 查看退改规则（可选）

**触发词**：退改规则、行李额、这个舱位的政策

**执行命令**：
```bash
python3 scripts/flight_guest_rule.py <舱位编号>
```

### 4. 创建机票订单

**触发词**：订这个、预订、下单 + 乘客信息

**执行命令**：
```bash
python3 scripts/flight_order.py <舱位编号> <乘客姓名> <乘客手机号> <乘客证件号>
```

**示例**：
```bash
python3 scripts/flight_order.py 1 "张三" "13800138000" "110101199001011234"
```

### 5. 查询/取消机票订单

**执行命令**：
```bash
python3 scripts/flight_order_detail.py <订单ID>
python3 scripts/flight_cancel.py <订单ID>
```

### 6. 改期

**触发词**：改期、改签、换航班

**执行命令**：
```bash
# 搜索可改期的航班
python3 scripts/flight_endorse_search.py <订单ID> <改期日期>

# 查看改期价格
python3 scripts/flight_endorse_price.py <订单ID> <改期日期> <新航班号>

# 提交改期申请
python3 scripts/flight_endorse_apply.py <舱位编号> <订单ID>
```

### 7. 退票

**触发词**：退票

**执行命令**：
```bash
# 查询退票费
python3 scripts/flight_refund_fee.py <订单ID>

# 提交退票申请（需用户确认退票费）
python3 scripts/flight_refund_apply.py <订单ID> <退票金额>
```

---

## 📋 完整示例

### 酒店预订流程

```
用户: 预订北京三元桥附近的酒店 明日入住

AI: [展示酒店列表表格]
    回复序号查看房型价格

用户: 3

AI: [展示房型和价格表格]
    回复"房型序号-产品序号"预订

用户: 1-1 郜文彬 1348879748

AI: ✅ 订单创建成功！
    订单号: xxx
    [支付链接]
```

### 机票预订流程

```
用户: 4月2日北京到上海的航班

AI: [展示航班列表表格]
    回复航班号查看舱位

用户: CA1501

AI: [展示舱位价格表格]
    回复"舱位编号"预订

用户: 订第1个 张三 13800138000 110101199001011234

AI: ✅ 订单创建成功！
    订单号: xxx
    [支付链接]
```

---

## ⚠️ 重要注意事项

1. **PII 安全**：乘客姓名、手机号、证件号等个人信息仅在预订时发送至服务，不会在日志中暴露

2. **日期格式**：所有日期均为 YYYY-MM-DD

3. **强制确认**：
   - 下单时必须索取乘客/入住人信息
   - 退票时必须让用户确认退票费用

4. **数据准确性**：展示结果必须基于脚本输出的原始数据，不得修改或编造

5. **统一鉴权**：酒店和机票共用同一套鉴权系统，一次登录即可使用所有服务

---

## 📁 文件结构

```
fbt-travel/
├── SKILL.md                    # 技能说明文档
├── skill.json                  # 技能元数据
├── scripts/
│   ├── auth.py                 # 统一鉴权
│   ├── common.py               # 公共函数
│   ├── hotel_api.py            # 酒店API封装
│   ├── flight_search.py        # 航班搜索
│   ├── flight_price.py         # 舱位价格
│   ├── flight_order.py         # 机票下单
│   ├── flight_order_detail.py  # 订单详情
│   ├── flight_cancel.py        # 取消订单
│   ├── flight_endorse_*.py     # 改期相关
│   └── flight_refund_*.py      # 退票相关
└── references/
    └── HOTEL_API.md            # 酒店API规范
```

---

## 📝 格式化输出模块

**文件位置**：`scripts/formatter.py`

### 展示配置

| 配置项 | 默认值 | 说明 |
|-------|-------|------|
| FLIGHT_LIST_LIMIT | 5 | 航班列表展示数量 |
| SEAT_LIST_LIMIT | 5 | 每个航班展示的舱位数量 |

### 格式化函数

```python
from scripts.formatter import (
    format_flight_list,     # 航班列表格式化
    format_seat_list,       # 舱位价格格式化
    format_order_result,    # 订单创建结果格式化
    format_baggage_info,    # 行李额格式化
    format_refund_rule,     # 退改规则格式化
    format_order_status     # 订单状态格式化
)
```

### 展示字段规范

**航班列表必须包含**：
- 序号、航班号、航司、时间、航线、机型、最低价

**舱位价格必须包含**：
- 序号、舱位名称、舱位代码、折扣、票价、机建、燃油、总价、余座

**订单详情必须包含**：
- 订单号、航班信息、舱位信息
- 票价明细（票价+机建+燃油）
- **行李额**（托运+手提）
- **[立即支付]** 按钮

---

## 版本历史

| 版本 | 日期 | 变更说明 |
|-----|------|---------|
| 1.1.0 | 2026-03-25 | 新增格式化输出模块，固化展示逻辑 |
| 1.0.0 | 2026-03-25 | 合并酒店和机票技能包，统一鉴权流程 |