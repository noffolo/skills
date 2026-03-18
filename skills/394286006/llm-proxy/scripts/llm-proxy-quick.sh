#!/bin/bash
# LLM Proxy 快捷命令 - 用于 skill 调用

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CTL_SCRIPT="$SCRIPT_DIR/llm-proxy-ctl.sh"

case "$1" in
  status|start|stop|restart|logs)
    bash "$CTL_SCRIPT" "$1"
    ;;
  health)
    curl -s http://127.0.0.1:18888/health | python3 -m json.tool
    ;;
  stats)
    curl -s http://127.0.0.1:18888/stats | python3 -m json.tool
    ;;
  *)
    echo "用法: $0 {status|start|stop|restart|logs|health|stats}"
    ;;
esac
