---
name: jisu-idcardrecognition
description: 使用极速数据身份证识别 API，对身份证等证件图片进行 OCR 识别，返回姓名、证件号等信息。
metadata: { "openclaw": { "emoji": "🪪", "requires": { "bins": ["python3"], "env": ["JISU_API_KEY"] }, "primaryEnv": "JISU_API_KEY" } }
---

## 极速数据身份证识别（Jisu IDCardRecognition）

基于 [身份证识别 API](https://www.jisuapi.com/api/idcardrecognition/) 的 OpenClaw 技能，支持对多种证件图片进行 OCR 识别，例如：

- 一代/二代身份证（正反面）
- 驾照、行驶证、军官证
- 港澳台通行证、护照、户口本、居住证等

核心接口为：

- `/idcardrecognition/recognize`：证件图片识别
- `/idcardrecognition/type`：获取支持的证件类型列表（`typeid` 与 `typename`）

使用前需要在极速数据官网申请服务，文档见：[https://www.jisuapi.com/api/idcardrecognition/](https://www.jisuapi.com/api/idcardrecognition/)

## 环境变量配置

```bash
# Linux / macOS
export JISU_API_KEY="your_appkey_here"

# Windows PowerShell
$env:JISU_API_KEY="your_appkey_here"
```

## 脚本路径

脚本文件：`skills/idcardrecognition/idcardrecognition.py`

## 使用方式与请求参数

当前脚本封装了 `/idcardrecognition/recognize` 接口，统一通过一段 JSON 调用。

### 1. 从本地图片识别证件（推荐）

```bash
python3 skills/idcardrecognition/idcardrecognition.py '{"path":"11.jpg","typeid":2}'
```

- `path`：本地证件图片路径（脚本会读取并转为 base64）；
- `typeid`：证件类型 ID（必填），可通过 `/idcardrecognition/type` 接口获取。

### 2. 直接传 base64 图片内容

如果前置流程已经将图片转为 base64，可以直接传 `pic` 字段：

```bash
python3 skills/idcardrecognition/idcardrecognition.py '{
  "pic": "<base64_string>",
  "typeid": 2
}'
```

> 注意：`pic` 只需要纯 base64 内容，不要带 `data:image/...;base64,` 前缀。

### 3. 请求参数说明

| 字段名 | 类型   | 必填 | 说明 |
|--------|--------|------|------|
| path   | string | 二选一 | 本地图片路径，脚本会自动读取并转为 base64 |
| image  | string | 二选一 | `path` 的别名 |
| file   | string | 二选一 | `path` 的别名 |
| pic    | string | 二选一 | 已是 base64 的图片内容（不带前缀） |
| typeid | int    | 是   | 证件类型 ID，参考 `/idcardrecognition/type` 返回 |

`typeid` 必填；`path/image/file` 与 `pic` 至少提供一个，同时存在时优先使用 `pic`。

## 返回结果说明

原始接口返回结构示例（节选，参考官网文档）：

```json
{
  "status": 0,
  "msg": "ok",
  "result": {
    "name": "李先生",
    "sex": "男",
    "nation": "汉",
    "birth": "1999-01-22",
    "address": "浙江省杭州市西湖区益乐路39号",
    "number": "411725199901220124",
    "portrait": "/9j/4AAQSkZJRgABAQ1qLt/Wiiigdz/9k=",
    "issueorg": "杭州市公安局西湖分局",
    "startdate": "2019-01-22",
    "enddate": "2029-01-22",
    "retain": ""
  }
}
```

本技能会直接输出 `result` 对象，例如：

```json
{
  "name": "李先生",
  "sex": "男",
  "nation": "汉",
  "birth": "1999-01-22",
  "address": "浙江省杭州市西湖区益乐路39号",
  "number": "411725199901220124",
  "portrait": "/9j/4AAQSkZJRgABAQ1qLt/Wiiigdz/9k=",
  "issueorg": "杭州市公安局西湖分局",
  "startdate": "2019-01-22",
  "enddate": "2029-01-22",
  "retain": ""
}
```

当出现业务错误（如图片为空、格式错误、大小超限等）时，统一包装为：

```json
{
  "error": "api_error",
  "code": 201,
  "message": "图片为空"
}
```

网络或解析错误则返回：

```json
{
  "error": "request_failed" | "http_error" | "invalid_json",
  "message": "...",
  "status_code": 500
}
```

## 常见错误码

来源于 [身份证识别文档](https://www.jisuapi.com/api/idcardrecognition/)：

| 代号 | 说明               |
|------|--------------------|
| 201  | 图片为空           |
| 202  | 图片格式错误       |
| 203  | 证件类型不存在     |
| 204  | 图片大小超过限制   |
| 208  | 识别失败           |
| 210  | 没有信息           |

系统错误码 101–108 与其它极速数据接口一致。

## 在 OpenClaw 中的推荐用法

1. 用户上传一张身份证或其它证件照片，提问「帮我识别姓名和证件号」。  
2. 代理先通过 `/idcardrecognition/type` 确认所需证件的 `typeid`，例如二代身份证正面是 `2`，然后将图片保存为本地文件路径或转为 base64。  
3. 调用：`python3 skills/idcardrecognition/idcardrecognition.py '{"path":"11.jpg","typeid":2}'`，从返回结果中读取 `name/sex/birth/address/number` 等字段，用自然语言总结，并视场景进行适度脱敏与隐私保护。  

