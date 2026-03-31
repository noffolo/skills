# Google

## 常用模式

### 网页搜索
```bash
opencli-rs google search "OpenClaw"
```

### 新闻搜索
```bash
opencli-rs google news --query "OpenClaw" --limit 10
```

### 搜索建议
```bash
opencli-rs google suggest --query "openclaw"
```

### 趋势
```bash
opencli-rs google trends --limit 10
```

## 最小说明

- Google 相关新闻、趋势等结果形态变化较快，返回内容受当下搜索结果影响。
- 若结果异常卡住，常见原因是浏览器链路或扩展连接状态异常。
