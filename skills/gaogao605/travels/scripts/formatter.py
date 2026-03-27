#!/usr/bin/env python3
"""
分贝通机票助手 - 格式化输出模块
固化展示逻辑，确保输出格式一致
"""

# ============================================================
# 展示配置（可调整）
# ============================================================

# 航班列表展示数量
FLIGHT_LIST_LIMIT = 5

# 每个航班展示的舱位数量
SEAT_LIST_LIMIT = 5

# ============================================================
# 航班列表格式化
# ============================================================

def format_flight_list(flights, direction="去程"):
    """
    格式化航班列表展示
    
    Args:
        flights: 航班列表数据
        direction: 方向（去程/返程）
    
    Returns:
        格式化后的Markdown文本
    """
    lines = []
    
    lines.append(f"## ✈️ {direction}航班\n")
    lines.append(f"找到 **{len(flights)}** 个航班\n")
    
    lines.append("| 序号 | 航班 | 时间 | 航线 | 机型 | 最低价 |")
    lines.append("|:---:|------|------|------|------|-----:|")
    
    for idx, f in enumerate(flights[:FLIGHT_LIST_LIMIT], 1):
        flight_no = f.get("flight_no", "-")
        airline = f.get("airline_name", "-")
        dep_time = f.get("dep_time", "-")
        arr_time = f.get("arr_time", "-")
        dep_port = f.get("starting_airport_short", "-")
        arr_port = f.get("destination_airport_short", "-")
        plane = f.get("plane_type_short", "-")
        price = int(f.get("min_price", 0))
        
        lines.append(f"| {idx} | {flight_no} {airline} | {dep_time}-{arr_time} | {dep_port}→{arr_port} | {plane} | ¥{price} |")
    
    lines.append("")
    lines.append("---")
    lines.append("💡 回复航班序号查看舱位价格，如 **1**")
    
    return "\n".join(lines)


# ============================================================
# 舱位价格格式化
# ============================================================

def format_seat_list(flight_info, seats):
    """
    格式化舱位价格展示
    
    Args:
        flight_info: 航班基本信息
        seats: 舱位列表数据
    
    Returns:
        格式化后的Markdown文本
    """
    lines = []
    
    # 航班信息头部
    flight_no = flight_info.get("flight_no", "-")
    airline = flight_info.get("airline_name", "-")
    dep_time = flight_info.get("dep_time", "-")
    arr_time = flight_info.get("arr_time", "-")
    dep_port = flight_info.get("starting_airport", "-")
    arr_port = flight_info.get("destination_airport", "-")
    plane = flight_info.get("plane_type", "-")
    meal = flight_info.get("meal", "-")
    
    lines.append(f"## ✈️ {flight_no} {airline}\n")
    lines.append(f"📅 时间：{dep_time} - {arr_time}")
    lines.append(f"📍 航线：{dep_port} → {arr_port}")
    lines.append(f"🛫 机型：{plane}")
    lines.append(f"🍽️ 餐食：{meal}")
    lines.append("")
    lines.append("---\n")
    
    # 舱位列表
    lines.append("### 舱位价格\n")
    lines.append("| 序号 | 舱位 | 折扣 | 票价 | 机建 | 燃油 | 总价 | 余座 |")
    lines.append("|:---:|:---:|:---:|---:|---:|---:|---:|:---:|")
    
    for idx, seat in enumerate(seats[:SEAT_LIST_LIMIT], 1):
        cabin_name = seat.get("seat_msg", "-")
        cabin_code = seat.get("cabin", "-")
        discount = int(seat.get("discount", 0) * 100)
        price = int(seat.get("par_price", 0))
        tax = 50  # 机建费固定
        fuel = 20  # 燃油费固定
        total = int(seat.get("settle_price", 0)) + tax + fuel
        status = seat.get("seat_status", "-")
        
        # 余座状态
        if status == "A":
            status_display = "充足"
        elif status.isdigit():
            status_display = f"余{status}座"
        else:
            status_display = status
        
        lines.append(f"| {idx} | {cabin_name}({cabin_code}) | {discount}% | ¥{price} | ¥{tax} | ¥{fuel} | ¥{total} | {status_display} |")
    
    lines.append("")
    lines.append("---")
    lines.append("💡 回复 **舱位序号** 预订，如 **1**")
    
    return "\n".join(lines)


# ============================================================
# 机票订单创建结果格式化
# ============================================================

def format_order_result(order_data, flight_info, seat_info):
    """
    格式化机票订单创建结果展示
    
    Args:
        order_data: 订单数据（包含order_id, pay_url）
        flight_info: 航班信息
        seat_info: 舱位信息
    
    Returns:
        格式化后的Markdown文本
    """
    lines = []
    
    order_id = order_data.get("order_id", "-")
    pay_url = order_data.get("pay_url", "-")
    pay_deadline = order_data.get("pay_deadline", "-")
    
    # 航班信息
    flight_no = flight_info.get("flight_no", "-")
    airline = flight_info.get("airline_name", "-")
    plane = flight_info.get("plane_type", "-")
    dep_date = flight_info.get("date", "-")
    dep_time = flight_info.get("dep_time", "-")
    arr_time = flight_info.get("arr_time", "-")
    dep_port = flight_info.get("starting_airport", "-")
    arr_port = flight_info.get("destination_airport", "-")
    
    # 舱位信息
    cabin_name = seat_info.get("seat_msg", "-")
    cabin_code = seat_info.get("cabin", "-")
    discount = int(seat_info.get("discount", 0) * 100)
    price = int(seat_info.get("settle_price", 0))
    tax = 50
    fuel = 20
    total = price + tax + fuel
    
    lines.append("## ✅ 机票订单创建成功！\n")
    
    # 订单基本信息
    lines.append(f"**订单号**：{order_id}")
    lines.append(f"**支付截止**：{pay_deadline}")
    lines.append("")
    
    lines.append("### ✈️ 航班信息")
    lines.append(f"- **航班**：{flight_no} {airline}")
    lines.append(f"- **机型**：{plane}")
    lines.append(f"- **时间**：{dep_date} {dep_time}-{arr_time}")
    lines.append(f"- **航线**：{dep_port} → {arr_port}")
    lines.append("")
    
    lines.append("### 💺 舱位信息")
    lines.append(f"- **舱位**：{cabin_name}（{cabin_code}舱）")
    lines.append(f"- **折扣**：{discount}%")
    lines.append(f"- **票价**：¥{price} + ¥{tax}机建 + ¥{fuel}燃油 = **¥{total}**")
    lines.append("")
    
    # 行李额（如果有）
    baggage = seat_info.get("baggage", {})
    if baggage:
        lines.append("### 🧳 行李额")
        checkin = baggage.get("checkInBaggage", {})
        carryon = baggage.get("carryOnBaggage", {})
        
        if checkin.get("flag"):
            lines.append(f"- **托运行李**：免费{checkin.get('weight', '-')}KG，不限件数")
            lines.append(f"  单件尺寸上限：{checkin.get('size', '-')}")
        
        if carryon.get("flag"):
            lines.append(f"- **手提行李**：免费{carryon.get('weight', '-')}KG，每人{carryon.get('piece', '-')}件")
            lines.append(f"  单件尺寸上限：{carryon.get('size', '-')}")
        
        lines.append("")
    
    # 支付按钮
    if pay_url:
        lines.append(f"**[立即支付]({pay_url})**")
    
    lines.append("")
    lines.append("---")
    lines.append("⚠️ 请尽快完成支付，超时订单将自动取消！")
    
    return "\n".join(lines)


# ============================================================
# 行李额格式化
# ============================================================

def format_baggage_info(baggage_data):
    """
    格式化行李额展示
    
    Args:
        baggage_data: 行李额数据
    
    Returns:
        格式化后的Markdown文本
    """
    lines = []
    
    lines.append("## 🧳 行李额信息\n")
    
    # 托运行李
    checkin = baggage_data.get("checkInBaggage", {})
    if checkin.get("flag"):
        lines.append("### 托运行李")
        lines.append(f"- **免费额度**：{checkin.get('weight', '-')}KG，不限件数")
        lines.append(f"- **单件尺寸上限**：{checkin.get('size', '-')}")
        lines.append(f"- **说明**：{checkin.get('context', '-')}")
        lines.append("")
    
    # 手提行李
    carryon = baggage_data.get("carryOnBaggage", {})
    if carryon.get("flag"):
        lines.append("### 手提行李")
        lines.append(f"- **免费额度**：{carryon.get('weight', '-')}KG，每人{carryon.get('piece', '-')}件")
        lines.append(f"- **单件尺寸上限**：{carryon.get('size', '-')}")
        lines.append(f"- **说明**：{carryon.get('context', '-')}")
        lines.append("")
    
    # 备注
    remark = baggage_data.get("remark", "")
    if remark:
        lines.append(f"📝 {remark}")
    
    return "\n".join(lines)


# ============================================================
# 退改规则格式化
# ============================================================

def format_refund_rule(rule_data):
    """
    格式化退改规则展示
    
    Args:
        rule_data: 退改规则数据
    
    Returns:
        格式化后的Markdown文本
    """
    lines = []
    
    lines.append("## 📋 退改规则\n")
    
    # 退票规则
    refund = rule_data.get("refund", {})
    if refund:
        lines.append("### 退票规则")
        lines.append(f"- **规则**：{refund.get('rule', '-')}")
        lines.append(f"- **费用**：{refund.get('fee', '-')}")
        lines.append("")
    
    # 改签规则
    change = rule_data.get("change", {})
    if change:
        lines.append("### 改签规则")
        lines.append(f"- **规则**：{change.get('rule', '-')}")
        lines.append(f"- **费用**：{change.get('fee', '-')}")
        lines.append("")
    
    return "\n".join(lines)


# ============================================================
# 订单状态格式化
# ============================================================

def format_order_status(order_data):
    """
    格式化订单状态展示
    
    Args:
        order_data: 订单数据
    
    Returns:
        格式化后的Markdown文本
    """
    lines = []
    
    order_id = order_data.get("order_id", "-")
    status = order_data.get("status", "-")
    
    # 航班信息
    flight = order_data.get("flight", {})
    flight_no = flight.get("flight_no", "-")
    dep_time = flight.get("dep_time", "-")
    arr_time = flight.get("arr_time", "-")
    
    # 乘客信息
    passenger = order_data.get("passenger", {})
    passenger_name = passenger.get("name", "-")
    
    # 价格信息
    price = order_data.get("price", 0)
    
    lines.append("## 📋 订单详情\n")
    lines.append(f"**订单号**：{order_id}")
    lines.append(f"**状态**：{status}")
    lines.append("")
    
    lines.append("### ✈️ 航班信息")
    lines.append(f"- **航班**：{flight_no}")
    lines.append(f"- **时间**：{dep_time} - {arr_time}")
    lines.append("")
    
    lines.append("### 👤 乘客信息")
    lines.append(f"- **姓名**：{passenger_name}")
    lines.append("")
    
    lines.append("### 💰 价格信息")
    lines.append(f"- **总价**：¥{price}")
    
    return "\n".join(lines)