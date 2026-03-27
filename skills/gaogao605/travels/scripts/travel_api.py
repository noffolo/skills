#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分贝通旅行助手 - 统一API入口
版本: 1.0.0 | 最后更新: 2026-03-25

整合酒店和机票服务，提供一站式差旅预订体验。
"""
import sys
import os

# 添加脚本目录到路径
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPTS_DIR)


def print_usage():
    """打印使用说明"""
    print("""
================================================================================
分贝通旅行助手 v1.0.0
================================================================================

【鉴权】
  python3 travel_api.py auth send <手机号>          发送验证码
  python3 travel_api.py auth verify <手机号> <验证码> 验证并获取凭证
  python3 travel_api.py auth status                 查看鉴权状态

【酒店服务】
  python3 travel_api.py hotel search <城市> <关键词> [入住] [退房]
  python3 travel_api.py hotel price <酒店ID> <入住> <退房>
  python3 travel_api.py hotel detail <酒店ID>
  python3 travel_api.py hotel comment <酒店ID>
  python3 travel_api.py hotel order <酒店ID> <房型ID> <产品ID> <入住> <退房> <总价> <姓名> <手机>
  python3 travel_api.py hotel query <订单ID>
  python3 travel_api.py hotel cancel <订单ID> [原因]

【机票服务】
  python3 travel_api.py flight search <出发城市> <到达城市> <日期>
  python3 travel_api.py flight price <出发机场> <到达机场> <日期> <航班号>
  python3 travel_api.py flight order <舱位编号> <姓名> <手机> <证件号>
  python3 travel_api.py flight query <订单ID>
  python3 travel_api.py flight cancel <订单ID>
  python3 travel_api.py flight endorse <订单ID> <改期日期>
  python3 travel_api.py flight refund <订单ID>

================================================================================
""")


def main():
    if len(sys.argv) < 2:
        print_usage()
        return

    service = sys.argv[1].lower()

    if service == "auth":
        # 鉴权服务
        if len(sys.argv) < 3:
            print("用法: travel_api.py auth [send|verify|status]")
            return
        os.system(f"python3 {SCRIPTS_DIR}/auth.py {' '.join(sys.argv[2:])}")

    elif service == "hotel":
        # 酒店服务
        if len(sys.argv) < 3:
            print("用法: travel_api.py hotel [search|price|detail|comment|order|query|cancel]")
            return
        os.system(f"python3 {SCRIPTS_DIR}/hotel_api.py {' '.join(sys.argv[2:])}")

    elif service == "flight":
        # 机票服务
        if len(sys.argv) < 3:
            print("用法: travel_api.py flight [search|price|order|query|cancel|endorse|refund]")
            return
        
        action = sys.argv[2].lower()
        args = sys.argv[3:]
        
        if action == "search":
            os.system(f"python3 {SCRIPTS_DIR}/flight_search.py {' '.join(args)}")
        elif action == "price":
            os.system(f"python3 {SCRIPTS_DIR}/flight_price.py {' '.join(args)}")
        elif action == "order":
            os.system(f"python3 {SCRIPTS_DIR}/flight_order.py {' '.join(args)}")
        elif action == "query":
            os.system(f"python3 {SCRIPTS_DIR}/flight_order_detail.py {' '.join(args)}")
        elif action == "cancel":
            os.system(f"python3 {SCRIPTS_DIR}/flight_cancel.py {' '.join(args)}")
        elif action == "endorse":
            if len(args) >= 2:
                os.system(f"python3 {SCRIPTS_DIR}/flight_endorse_search.py {' '.join(args)}")
        elif action == "refund":
            if len(args) >= 1:
                os.system(f"python3 {SCRIPTS_DIR}/flight_refund_fee.py {' '.join(args)}")
        else:
            print(f"未知的机票操作: {action}")

    else:
        print(f"未知的服务类型: {service}")
        print("支持的服务: auth, hotel, flight")


if __name__ == "__main__":
    main()