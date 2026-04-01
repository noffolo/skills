#!/bin/bash
# quick-publish.sh - 最简发布命令
# 用法: ./quick-publish.sh <slug>
# 
# 一句话发布！自动检测 Token，只发布已配置的平台

cd "$(dirname "$0")/.." || exit 1
./scripts/publish.sh "$@"
