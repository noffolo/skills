# LLM Proxy Skill - 使用方式

## 安装

### 方式一：从 ClawHub 安装

```bash
# 安装 ClawHub CLI
npm i -g clawhub

# 安装 skill
clawhub install llm-proxy
```

### 方式二：手动安装

```bash
# 复制到 OpenClaw skills 目录
cp -r llm-proxy ~/.openclaw/skills/

# 或复制到当前工作目录
cp -r llm-proxy ./skills/
```

## 启动服务

```bash
# 进入 skill 目录
cd ~/.openclaw/skills/llm-proxy/scripts

# 启动代理
./llm-proxy-ctl.sh start
```

## 使用代理

代理启动后，通过 `http://127.0.0.1:18888` 访问：

### 百炼 API

```bash
curl http://127.0.0.1:18888/bailian/chat/completions \
  -H "Authorization: Bearer $BAILIAN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen-plus",
    "messages": [{"role": "user", "content": "你好"}]
  }'
```

### OpenRouter API

```bash
curl http://127.0.0.1:18888/openrouter/chat/completions \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "anthropic/claude-3-opus",
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

### NVIDIA NIM API

```bash
curl http://127.0.0.1:18888/nvd/chat/completions \
  -H "Authorization: Bearer $NVIDIA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "meta/llama-3.1-8b-instruct",
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

## 配置 OpenClaw 使用代理

在 `~/.openclaw/openclaw.json` 中配置：

```json5
{
  models: {
    // 百炼模型通过代理
    "bailian/qwen-plus": {
      endpoint: "http://127.0.0.1:18888/bailian"
    },
    // OpenRouter 模型通过代理
    "openrouter/claude-3-opus": {
      endpoint: "http://127.0.0.1:18888/openrouter"
    },
    // NVIDIA 模型通过代理
    "nvd/llama-3.1-8b": {
      endpoint: "http://127.0.0.1:18888/nvd"
    }
  }
}
```

## 管理命令

```bash
# 查看状态
./llm-proxy-ctl.sh status

# 健康检查
curl http://127.0.0.1:18888/health

# 查看统计
curl http://127.0.0.1:18888/stats

# 查看日志
./llm-proxy-ctl.sh logs

# 重启代理
./llm-proxy-ctl.sh restart

# 停止代理
./llm-proxy-ctl.sh stop
```

## 环境变量

```bash
# 自定义端口（默认 18888）
export LLM_PROXY_PORT=18888

# 自定义规则文件
export RULES_FILE=/path/to/custom-rules.json
```

## 查看日志

```bash
# 实时日志
tail -f ~/.openclaw/logs/llm-proxy/service.log

# 请求日志
cat ~/.openclaw/logs/llm-proxy/proxy-$(date +%Y-%m-%d).jsonl | jq

# 错误请求
cat ~/.openclaw/logs/llm-proxy/proxy-*.jsonl | jq 'select(.status >= 400)'
```
