# LLM Proxy 故障排查指南

## 常见问题

### 1. 端口被占用

**症状**:
```
[ERROR] 端口 18888 已被占用
```

**解决方案**:
```bash
# 查看占用进程
lsof -i :18888

# 终止进程
kill -9 <PID>

# 或使用控制脚本
llm-proxy-ctl.sh restart
```

### 2. 代理无响应

**检查步骤**:
```bash
# 1. 检查健康端点
curl -s --max-time 5 http://127.0.0.1:18888/health

# 2. 检查进程
pgrep -f llm-proxy.py

# 3. 检查端口
lsof -i :18888

# 4. 查看日志
tail -50 ~/.openclaw/logs/llm-proxy/service.log
```

### 3. 上游 API 连接失败

**症状**:
```json
{"error": "连接失败: [Errno 61] Connection refused"}
```

**检查**:
```bash
# 检查网络
curl -s https://www.baidu.com

# 检查 NVIDIA NIM API
curl -s https://integrate.api.nvidia.com/v1/models \
  -H "Authorization: Bearer $NVIDIA_API_KEY"
```

### 4. 内容过滤误报

**调整规则**:

编辑 `{baseDir}/scripts/content-filter-rules.json`:

```json
{
  "whitelist": [
    "已授权的.*操作",
    "测试环境.*命令"
  ]
}
```

重启代理生效：
```bash
llm-proxy-ctl.sh restart
```

## 日志分析

### 查看请求日志

```bash
# 今日日志
cat ~/.openclaw/logs/llm-proxy/proxy-$(date +%Y-%m-%d).jsonl | jq

# 错误请求
cat ~/.openclaw/logs/llm-proxy/proxy-*.jsonl | jq 'select(.status >= 400)'

# 告警请求
cat ~/.openclaw/logs/llm-proxy/proxy-*.jsonl | jq 'select(.alerts | length > 0)'
```

### 统计分析

```bash
# 请求量统计
cat ~/.openclaw/logs/llm-proxy/proxy-*.jsonl | jq -r '.provider' | sort | uniq -c

# 错误率
cat ~/.openclaw/logs/llm-proxy/proxy-*.jsonl | jq -r '.status' | \
  awk '{if($1>=400)err++;total++} END{print "错误率:", err/total*100 "%"}'

# 平均响应时间
cat ~/.openclaw/logs/llm-proxy/proxy-*.jsonl | jq '.duration_ms' | \
  awk '{sum+=$1;count++} END{print "平均:", sum/count, "ms"}'
```

## 性能调优

### 增加并发

编辑 `{baseDir}/scripts/llm-proxy.py`:
```python
MAX_THREADS = 100  # 默认 50
```

### 调整超时

```python
READ_TIMEOUT = 120  # 默认 60 秒
```

### 日志轮转

添加 crontab:
```bash
# 每周清理 30 天前的日志
0 3 * * 0 find ~/.openclaw/logs/llm-proxy -name "*.jsonl" -mtime +30 -delete
```
