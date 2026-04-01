---
name: wifi-troubleshooting
description: 针对无线场景下终端体验差、网卡、无法接入 WiFi 等问题进行排障
version: "1.0"
metadata:
  {
    "H3C":
      {
        "emoji": "📍",
        "requires": { "bins": ["mcporter"], "env": ["CLOUDNET_API_KEY"] },
        "primaryEnv": "CLOUDNET_API_KEY",
        "install":
          [
            {
              "id": "npm",
              "kind": "npm",
              "formula": "mcporter",
              "bins": ["mcporter"],
              "label": "Install mcporter (npm)",
            },
          ],
      },
  }
triggers:
  - "WiFi 问题排查"
  - "无线网络故障"
  - "终端上网慢"
  - "连不上 WiFi"
  - "网络卡顿"
author: H3C
---

# wifi-troubleshooting

针对无线场景下终端体验差、网卡、无法接入 WiFi 等问题进行排障。

## 触发条件

用户询问关于无线终端连接问题，例如：
- "XX 场所的 XX 终端上网很慢"
- "XX 场所的 XX 设备连不上 WiFi"
- "XX 场所的 XX 用户反馈网络卡"

## 前置环境检查

### 安装`mcporter`cli支持及skill支持

- mcporter: `npm install -g mcporter`
- 然后再通过clawhub安装`mcporter`技能

### 配置MCP连接参数

- `CLOUDNET_API_KEY` 必须.  需要用户提供Cloudnet管理平台的API KEY，可通过Cloudnet管理平台（网络管理=>设置=>开放平台）获取
- 可选: `CLOUDNET_BASE_URL` for testing/proxying. 默认使用http://localhost
- 执行```bash
mcporter config add cloudnet-mcp ${CLOUDNET_BASE_URL}/api/sse --header Authorization="Bearer ${CLOUDNET_API_KEY}"
```

## 排障步骤

### 第一步：提取关键信息

从用户问题中提取以下信息：

| 信息 | 说明 | 示例 |
|------|------|------|
| **场所名** | 必填，问题发生的场所 | "总部办公室"、"XX 门店" |
| **终端信息** | 必填，MAC 地址或终端用户名 | MAC: `xxxx-xxxx-xxxx` 或用户名: `zhangsan` |
| **故障时间** | 可选，用户未指定则默认当前时间 | "2026-03-24 10:00:00" |

**重要**：如果场所名和终端信息未提取到，必须让用户补充完整后才能继续下一步。

### 第二步：查询场所 ID

调用 `cloudnet-mcp.getallshopsanddevofuser` 获取用户下所有场所，找到场所名对应的场所 ID。

```bash
mcporter call cloudnet-mcp.getallshopsanddevofuser
```

### 第三步：执行终端诊断

根据提取的终端信息（MAC 或用户名），调用 `executeStaDiagnosis` 进行诊断：

**参数说明**：
- `MAC`: 终端 MAC 地址，格式 `xxxx-xxxx-xxxx`
- `shopId`: 场所 ID（来自第二步），需要转为字符串类型
- `faultTime`: 故障时间，格式 `yyyy-MM-dd HH:mm:ss`，用户未指定则使用当前时间
- `timezone`: 用户时区，默认 `Asia/Shanghai`

```bash
mcporter call cloudnet-mcp.executeStaDiagnosis MAC:"xxxx-xxxx-xxxx" shopId:"场所ID" faultTime:"2026-03-24 10:00:00" timezone:"Asia/Shanghai"
```

### 第四步：分析诊断结果

诊断返回后会包含：
- 终端连接状态
- 信号强度
- 接入 AP 信息
- 可能的根因
- 优化建议

结合诊断结果回答用户问题，并给出具体的解决建议。

## 输出格式

完成排障后，向用户清晰说明：
1. 诊断结果摘要
2. 问题根因分析
3. 建议的解决措施