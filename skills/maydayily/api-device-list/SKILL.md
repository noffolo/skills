---
name: api-device-list
description: "调用 ai-open-gateway 的设备列表查询接口 POST /api/device/list，获取当前用户绑定的所有设备信息。Use when: 需要查看绑定了哪些设备、获取设备 MAC 地址、确认设备是否已绑定。⚠️ 需设置 AI_GATEWAY_API_KEY。"
metadata:
  openclaw:
    requires:
      bins: ["python3"]
      env: ["AI_GATEWAY_API_KEY"]
    primaryEnv: "AI_GATEWAY_API_KEY"
---

# 设备列表查询接口

`POST /api/device/list` 用于查询当前认证用户绑定的所有设备列表。该接口无需请求体，设备列表由 api_key 自动关联。

## ⚠️ 展示规则（MUST 严格遵守）

脚本输出 JSON 格式的结构化数据，这是预期行为。以下展示规则是给 agent 的格式化指令：agent MUST 解析脚本输出的 JSON，按下述规则转换为用户友好的格式后再展示，MUST NOT 直接展示原始 JSON。

1. 当 `code == 0` 且 `data` 非空时，以表格展示：

| MAC 地址 | 设备名称 |
|----------|----------|
| aabbccddeeff | 客厅摄像机 |

关键规则：device_id MUST 去掉 `xxxxS_` 前缀再展示为 MAC 地址。表头 MUST 写"MAC 地址"，不要写"设备 ID"。

2. 当 `data` 为空数组时，回复："当前账户下没有绑定任何设备。"
3. 当 `code != 0` 时，回复："接口调用失败，错误码 {code}，原因：{message}"

## 前置依赖

脚本依赖 httpx。如果未安装，脚本会提示 `python3 -m pip install httpx`。

## 配置声明

本 skill 依赖以下配置项，agent 和用户 MUST 在运行前确认已正确配置。

### 必需配置

| 配置项 | 传递方式 | 说明 |
|--------|----------|------|
| AI_GATEWAY_API_KEY | 环境变量（推荐）、`~/.openclaw/.env`（fallback）、命令行 `--api-key` | API 密钥，用于接口鉴权。脚本按此优先级自动获取 |

### 可选配置

| 配置项 | 传递方式 | 默认值 | 说明 |
|--------|----------|--------|------|
| AI_GATEWAY_HOST | 环境变量、`~/.openclaw/.env` | `https://ai-open-gateway.closeli.cn` | 网关地址 |
| AI_GATEWAY_VERIFY_SSL | 环境变量 | true | 设为 false 可禁用 TLS 证书验证（仅限开发环境） |
| AI_GATEWAY_NO_ENV_FILE | 环境变量 | false | 设为 true 可禁用 `~/.openclaw/.env` fallback 读取（生产环境推荐） |

### Fallback 配置路径

脚本默认会读取 `~/.openclaw/.env` 文件作为 fallback 配置源。该文件为所有 skill 共享，格式为 `KEY=VALUE`（每行一条）。生产环境 MUST 设置 `AI_GATEWAY_NO_ENV_FILE=true` 禁用此 fallback，改为通过环境变量直接传递所有配置。

## 安全注意事项

- 共享凭证文件 `~/.openclaw/.env` 可被同一用户下所有 skill 读取。生产环境 MUST 通过环境变量传递 API_KEY，MUST NOT 依赖共享凭证文件
- TLS 证书验证默认启用，MUST NOT 在生产环境禁用（禁用会导致中间人攻击风险，攻击者可截获 API_KEY 和设备数据）
- 使用前 MUST 确认 AI_GATEWAY_HOST 指向可信域名
- MUST 使用最小权限的 API_KEY，避免复用高权限凭证。本 skill 仅需设备列表查询权限

## 网络访问声明

本 skill 仅访问以下端点（均为 AI_GATEWAY_HOST 下的路径）：

| 端点 | 方法 | 用途 |
|------|------|------|
| /api/device/list | POST | 查询用户绑定的设备列表 |

脚本不访问任何其他网络资源。

## 快速开始

```bash
python3 list_devices.py
```

## 认证方式

使用 Bearer Token 认证，脚本自动在请求头中携带 `Authorization: Bearer <api_key>`。

## 请求格式

### 请求头

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| Content-Type | string | 是 | `application/json` |
| Authorization | string | 是 | `Bearer <api_key>`，32 位十六进制字符串 |

### 请求体

无需请求体。

## 响应格式

```json
{
  "code": 0,
  "message": "success",
  "request_id": "<32位请求追踪ID>",
  "data": [
    {
      "device_id": "xxxxS_aabbccddeeff",
      "device_name": "客厅摄像机"
    }
  ]
}
```

### data 字段（设备数组）

| 参数名 | 类型 | 说明 |
|--------|------|------|
| device_id | string | 设备 ID，格式: `xxxxS_<mac地址>`，后续接口均使用此格式 |
| device_name | string | 设备名称，用户自定义的设备别名 |

## 错误码

| 错误码 | HTTP 状态码 | 说明 |
|--------|------------|------|
| 1001 | 401 | 未提供 api_key（缺少 Authorization 头或格式不正确） |
| 1002 | 401 | api_key 无效或已禁用 |
| 3001 | 502 | 网关内部服务调用失败 |
| 3004 | 502 | 网关内部服务调用失败 |
| 5000 | 500 | 内部错误 |

## 注意事项

- device_id 格式为 `xxxxS_<mac>`，是后续所有设备相关接口的标识符
- 全局请求超时为 120 秒
