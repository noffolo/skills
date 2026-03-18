---
name: llm-proxy
description: LLM API 代理服务管理工具。支持多 Provider 转发（百炼/OpenRouter/NVIDIA）、内容安全审计、健康监控。使用场景：(1)启动/停止/重启代理服务 (2)查看代理状态和统计 (3)查看实时日志 (4)配置内容过滤规则。
---

# LLM Proxy 管理工具

本地 LLM API 代理服务，提供多 Provider 转发、内容安全审计等功能。

## 功能特性

- 🔄 **多 Provider 转发** - 百炼、OpenRouter、NVIDIA NIM
- 🔒 **内容安全审计** - 两层审核机制（恶意指令 + 敏感内容）
- 📊 **请求统计** - 实时统计请求数、错误率、告警数
- 📝 **日志记录** - 所有请求 JSONL 格式存档

## 快速开始

### 查看代理状态

```bash
llm-proxy-ctl.sh status
```

### 启动代理

```bash
llm-proxy-ctl.sh start
```

### 停止代理

```bash
llm-proxy-ctl.sh stop
```

### 重启代理

```bash
llm-proxy-ctl.sh restart
```

### 查看实时日志

```bash
llm-proxy-ctl.sh logs
```

## Provider 配置

代理支持以下 Provider 路径前缀：

| 前缀 | 目标 API |
|------|----------|
| `/bailian` | 阿里云百炼 `https://coding.dashscope.aliyuncs.com/v1` |
| `/openrouter` | OpenRouter `https://openrouter.ai/api/v1` |
| `/nvd` | NVIDIA NIM `https://integrate.api.nvidia.com/v1` |

### 使用示例

```bash
# 通过代理调用百炼 API
curl http://127.0.0.1:18888/bailian/chat/completions \
  -H "Authorization: Bearer $BAILIAN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "qwen-plus", "messages": [{"role": "user", "content": "Hello"}]}'

# 通过代理调用 OpenRouter
curl http://127.0.0.1:18888/openrouter/chat/completions \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "anthropic/claude-3-opus", "messages": [{"role": "user", "content": "Hello"}]}'

# 通过代理调用 NVIDIA NIM
curl http://127.0.0.1:18888/nvd/chat/completions \
  -H "Authorization: Bearer $NVIDIA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "meta/llama-3.1-8b-instruct", "messages": [{"role": "user", "content": "Hello"}]}'
```

## 健康检查

### HTTP 端点

```bash
# 健康状态
curl http://127.0.0.1:18888/health

# 统计数据
curl http://127.0.0.1:18888/stats
```

### 健康检查响应

```json
{
  "status": "ok",
  "stats": {
    "total_requests": 1234,
    "total_responses": 1200,
    "blocked": 5,
    "warnings": 12,
    "errors": 34
  },
  "uptime": 3600,
  "rules_loaded": {
    "layer1": 6,
    "layer2": 3,
    "whitelist": 2
  }
}
```

## 内容安全审计

### 两层审核机制

**第一层：恶意指令检测**
- 危险系统命令（rm -rf /、mkfs、dd 等）
- 提权操作（sudo su、chmod u+s）
- SQL 注入/删除
- 数据外泄（curl -d @、nc -e）
- 后门/反弹 shell

**第二层：敏感内容检测**
- 个人身份信息（身份证、手机号、邮箱）
- 银行卡/信用卡号
- 敏感关键词

### 规则配置

规则文件：`{baseDir}/scripts/content-filter-rules.json`

```json
{
  "layer1_malicious": {
    "enabled": true,
    "rules": [
      {
        "id": "CMD-001",
        "name": "危险系统命令",
        "severity": "critical",
        "patterns": ["rm\\s+-rf\\s+[/~]", "mkfs\\.", "dd\\s+if=.*of=/dev/"]
      }
    ]
  },
  "layer2_sensitive": {
    "enabled": true,
    "rules": [...]
  },
  "whitelist": ["已授权的.*操作"]
}
```

## 日志文件

| 文件 | 内容 |
|------|------|
| `~/.openclaw/logs/llm-proxy/proxy-YYYY-MM-DD.jsonl` | 请求日志 |
| `~/.openclaw/logs/llm-proxy/service.log` | 服务日志 |

### 日志格式

```json
{
  "timestamp": "2026-03-17T12:34:56.789",
  "request_id": "abc12345",
  "provider": "bailian",
  "path": "/chat/completions",
  "status": 200,
  "duration_ms": 1234,
  "alerts": [],
  "request_size": 256,
  "response_size": 1024
}
```

## 常见问题

### 端口被占用

```bash
# 查看占用端口的进程
lsof -i :18888

# 终止进程
kill -9 <PID>

# 或重启代理（会自动清理）
llm-proxy-ctl.sh restart
```

### 代理无响应

```bash
# 检查健康状态
curl http://127.0.0.1:18888/health

# 重启代理
llm-proxy-ctl.sh restart
```

### 查看错误日志

```bash
tail -100 ~/.openclaw/logs/llm-proxy/service.log
```

## 核心文件

| 文件 | 说明 |
|------|------|
| `{baseDir}/scripts/llm-proxy.py` | 代理主程序 |
| `{baseDir}/scripts/llm-proxy-ctl.sh` | 启动控制脚本 |
| `{baseDir}/scripts/content-filter-rules.json` | 内容过滤规则 |

---

**注意**: 代理服务需要 Python 3.6+ 和网络连接。
