#!/bin/bash
# MiniMax Token Plan 余额查询
# 认证：使用环境变量 MINIMAX_API_KEY（通过 openclaw config set 配置）
# 用法: bash query.sh [api_key]

AUTH_VALUE="${1:-$MINIMAX_API_KEY}"

if [[ -z "$AUTH_VALUE" ]]; then
    echo "错误：未找到 API Key"
    echo ""
    echo "首次使用请先获取 API Key："
    echo ""
    echo "1. 登录 https://platform.minimaxi.com"
    echo "2. 进入 用户中心 → 接口密钥"
    echo "3. 创建 Token Plan Key"
    echo "4. 复制 Key 后直接粘贴给我"
    echo ""
    echo "获取后选择："
    echo "  - 单次查询：只查一次，不保存"
    echo "  - 保存到本地：保存 Key，以后直接查询"
    exit 1
fi

URL="https://www.minimaxi.com/v1/api/openplatform/coding_plan/remains"

RESULT=$(curl -s -X GET "$URL" \
    -H "Authorization: Bearer $AUTH_VALUE" \
    -H "Content-Type: application/json")

echo "$RESULT"
