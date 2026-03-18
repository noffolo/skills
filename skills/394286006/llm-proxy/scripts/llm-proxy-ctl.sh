#!/bin/bash
# LLM Proxy 启动脚本 - 无限自动重启版

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROXY_SCRIPT="$SCRIPT_DIR/llm-proxy.py"
PROXY_PORT=18888
PID_FILE="/tmp/llm-proxy.pid"
LOG_FILE="$HOME/.openclaw/logs/llm-proxy/service.log"
RESTART_DELAY=2

# 等待网络就绪（开机时网络可能还没启动）
wait_for_network() {
    local max_wait=${1:-90}  # 默认最多等待90秒
    local waited=0
    local targets=("https://www.baidu.com" "https://www.aliyun.com" "https://www.apple.com")

    echo "⏳ 检查网络连接 (最多等待${max_wait}秒)..."
    while [ $waited -lt $max_wait ]; do
        for target in "${targets[@]}"; do
            if curl -s --max-time 3 "$target" >/dev/null 2>&1; then
                echo "✅ 网络就绪 (耗时 ${waited}秒, 目标: $target)"
                return 0
            fi
        done
        sleep 3
        waited=$((waited + 3))
        if [ $((waited % 15)) -eq 0 ]; then
            echo "  → 仍在等待网络... (${waited}/${max_wait}秒)"
        fi
    done
    echo "⚠️ 网络检查超时 (${max_wait}秒)，继续启动（可能无法连接上游API）"
    return 1
}

start() {
    # 检查是否已在运行（先检查健康端点）
    if curl -s --max-time 3 http://127.0.0.1:$PROXY_PORT/health > /dev/null 2>&1; then
        echo "✅ 代理已在运行"
        curl -s http://127.0.0.1:$PROXY_PORT/health | python3 -m json.tool
        return 0
    fi

    # 检查端口是否被占用（但不立即杀进程）
    if is_port_in_use $PROXY_PORT; then
        echo "⚠️ 端口 $PROXY_PORT 被占用，清理中..."
        local port_pids
        port_pids=$(/usr/sbin/lsof -ti ":$PROXY_PORT" 2>/dev/null)
        if [ -n "$port_pids" ]; then
            echo "   占用进程: $port_pids"
            for pid in $port_pids; do
                echo "   → 终止 PID: $pid"
                kill -TERM "$pid" 2>/dev/null
            done
            sleep 2
        fi
    fi

    # 清理残留进程（先尝试优雅终止）
    local proxy_pids
    proxy_pids=$(pgrep -f "llm-proxy.py" 2>/dev/null)
    if [ -n "$proxy_pids" ]; then
        echo "🧹 清理残留进程: $proxy_pids"
        for pid in $proxy_pids; do
            kill -TERM "$pid" 2>/dev/null
        done
        sleep 2
    fi

    # 强制清理仍在运行的进程
    pkill -9 -f "llm-proxy" 2>/dev/null
    sleep 1

    # 等待网络就绪
    wait_for_network 30

    echo "🚀 启动 LLM Proxy..."
    mkdir -p "$(dirname "$LOG_FILE")"

    # 直接后台启动，使用 -u 禁用缓冲（解决 nohup 无响应问题）
    python3 -u "$PROXY_SCRIPT" >> "$LOG_FILE" 2>&1 &
    echo $! > "$PID_FILE"
    echo "✅ 代理 PID: $(cat "$PID_FILE")"

    sleep 3
    if curl -s --max-time 5 http://127.0.0.1:$PROXY_PORT/health > /dev/null 2>&1; then
        echo "✅ 健康检查通过"
        curl -s http://127.0.0.1:$PROXY_PORT/health | python3 -m json.tool
    else
        echo "⚠️ 启动可能失败，检查日志: $LOG_FILE"
    fi
}

kill_by_port() {
    local port=$1
    local pids

    # 方法1: 使用 lsof 查找占用端口的进程
    pids=$(lsof -ti ":$port" 2>/dev/null)

    if [ -n "$pids" ]; then
        echo "🔍 发现占用端口 $port 的进程: $pids"
        for pid in $pids; do
            echo "  → 终止 PID: $pid"
            kill -9 "$pid" 2>/dev/null
        done
        return 0
    fi

    return 1
}

# 检查端口是否被占用
is_port_in_use() {
    local port=$1
    lsof -ti ":$port" >/dev/null 2>&1
    return $?
}

# 等待端口完全释放（循环杀进程直到端口可用）
wait_for_port_release() {
    local port=$1
    local max_attempts=${2:-15}  # 默认最多尝试15次
    local attempt=0

    echo "⏳ 等待端口 $port 释放..."

    while [ $attempt -lt $max_attempts ]; do
        if ! is_port_in_use "$port"; then
            echo "✅ 端口 $port 已释放"
            return 0
        fi

        attempt=$((attempt + 1))
        # 随机等待 2-6 秒，避免竞争
        local wait_interval=$(( RANDOM % 5 + 2 ))
        echo "  → 端口仍被占用 (尝试 $attempt/$max_attempts)，等待 ${wait_interval}s 后重试..."

        # 杀掉占用端口的进程
        kill_by_port "$port" 2>/dev/null

        # 同时清理所有 llm-proxy 相关进程
        pkill -9 -f "llm-proxy.py" 2>/dev/null

        sleep $wait_interval
    done

    echo "❌ 端口 $port 释放超时 (已尝试 $max_attempts 次)"
    return 1
}

stop() {
    echo "🛑 停止 LLM Proxy..."

    # 1. 尝试通过 PID 文件停止守护进程（包括其子进程）
    if [ -f "$PID_FILE" ]; then
        local pid=$(cat "$PID_FILE")
        echo "🛑 停止守护进程 (PID: $pid)..."
        # 杀整个进程组
        kill -9 -- -"$pid" 2>/dev/null || kill -9 "$pid" 2>/dev/null
        sleep 1
    fi

    # 2. 清理所有 llm-proxy 相关进程
    echo "🧹 清理所有 llm-proxy 进程..."
    pkill -9 -f "llm-proxy" 2>/dev/null

    # 3. 等待端口释放
    sleep 2

    # 4. 清理临时文件
    rm -f "$PID_FILE"
    rm -f /tmp/llm-proxy-wrapper.sh

    echo "✅ 已完全停止"
}

status() {
    if curl -s --max-time 2 http://127.0.0.1:18888/health > /dev/null 2>&1; then
        echo "✅ 代理运行中"
        curl -s http://127.0.0.1:18888/health | python3 -m json.tool
    else
        echo "❌ 代理无响应"
        if [ -f "$PID_FILE" ] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
            echo "⚠️ 守护进程在运行 (PID: $(cat "$PID_FILE")), 但代理无响应"
        else
            echo "❌ 守护进程也未运行"
        fi
    fi
}

logs() {
    tail -f "$LOG_FILE"
}

case "$1" in
    start) start ;;
    stop) stop ;;
    restart) stop; sleep 1; start ;;
    status) status ;;
    logs) logs ;;
    *) echo "用法: $0 {start|stop|restart|status|logs}" ;;
esac
