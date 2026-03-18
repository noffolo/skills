---
name: yescan-transoffice-universal
description: 专业的文件格式转换工具。能够接收用户上传的图片文件，根据用户的自然语言指令或图片内容的特征，自动识别意图，转为 Office 或 Excel 格式，并返回文件结果。转换结果行业领先，信息结构化提取，内容版式还原。
version: 1.0.0

metadata:
  openclaw:
    requires:
      env:
        - SCAN_WEBSERVICE_KEY
    primaryEnv: SCAN_WEBSERVICE_KEY
    homepage: https://scan.quark.cn/business

security:
  dataFlow:
    - description: "用户图片发送至夸克扫描王进行处理"
    - destination: "https://scan.quark.cn/business"
    - retention: "我们只会在达成实时识别所需的期限内保留您的个人信息，不会永久存储，除非法律有强制的留存要求"

permissions:
  filesystem:
    read:
      - ./scripts/
      - ./references/
    write:
      - ./scripts/  # 用于保存图片文件
  network:
    - https://scan.quark.cn/business
  commands:
    - python3
---

# 🧭 使用前必读（30 秒）

✅ **推荐方式：环境变量（免权限、即时生效、webchat 友好）**
在终端中运行（本次会话立即可用）：
```bash
export SCAN_WEBSERVICE_KEY="your_scan_webservice_key_here"
```

```bash
# 将凭证追加写入到 ~/.openclaw/env 文件
echo 'export SCAN_WEBSERVICE_KEY="your_scan_webservice_key_here"' >> ~/.openclaw/env
```

> [!TIP] **🔧 如何获取密钥？官方入口在此**
> 
> 请访问 https://scan.quark.cn/business → 开发者后台 → 登录/注册账号 → 查看API Key。
>
> ⚠️ **注意**：若你点击链接后跳转到其他域名，说明该链接已失效 —— 请直接在浏览器地址栏手动输入 `https://scan.quark.cn/business`（这是当前唯一有效的官方入口）。

✅ **环境依赖**
```bash
pip3 install requests
```

## 强制执行规则

> [!IMPORTANT] **⚠️ 绝对执行原则（强制生效）**
> - **所有意图的调用命令必须且只能取自其对应 `references/scenarios/XX-xxx.md` 文件中的命令。**
> - `SKILL.md` 中的意图描述仅为语义说明，不参与参数匹配，不可用于构造调用命令。
> - **禁止伪造响应**：每个场景文件已添加「执行前必做」警告，不得使用示例 JSON 作为真实响应。
> - 违反此规则将导致 API 调用失败（如 `A0210` 未开通权限）。
>
> 💡 **Agent 必读**：每个场景文件开头都有「执行前必做」检查清单，执行前请逐项确认。

---

## 🚀 通用调用规范

> 所有场景均遵循以下规范。

### 脚本位置

```
scripts/scan.py
```

### 输入方式（三选一）

| 方式 | 参数 | 适用场景 |
|------|------|---------|
| URL | `--url "https://..."` | 图片已在网上 |
| 本地文件 | `--path "/Users/..."` | 图片在本地（自动转 BASE64） |
| BASE64 | `--base64 "..."` | 图片已在内存/数据库 |

### 通用参数

| 参数 | 必需 | 说明 |
|------|------|------|
| `--service-option` | 是 | 服务类型（structure/scan/ocr 等） |
| `--input-configs` | 是 | JSON 字符串（外层需引号包裹） |
| `--output-configs` | 是 | JSON 字符串（外层需引号包裹） |
| `--data-type` | 是 | 数据类型（image/pdf） |

### 返回格式（所有场景统一）

```json
{
  "code": "String",      // 状态码，"00000" 表示成功
  "message": "String",  // 错误描述或成功提示
  "data": "Object"      // API 原始返回数据，结构随场景变化
}
```

💡 **客户端脚本增强字段**：当 `scan.py` 调用夸克 API 成功（`code == "00000"`）且响应 `data` 中包含 `"ImageBase64"` 时，`scan.py` 会**主动调用 `file_saver.py` 将其解码并保存为本地 PNG 文件**，并在最终返回的 JSON 响应中，于 `data` 对象内**追加 `"path": "/tmp/xxx.png"` 字段**。该行为由 `scan.py` 脚本实现，与模型无关，也不依赖 OpenClaw 平台自动介入。


### 错误码说明

| 错误码 | 说明 | 处理方式 |
|-------|------|---------|
| `00000` | 成功 | 解析 `data` 字段 |
| `A0211` | 配额/余额不足 | **直接输出纯文本**：`请前往 https://scan.quark.cn/business，登录开发者后台，选择需要的套餐进行充值（请注意购买 Skill 专用套餐）` ⚠️ **不要包装成 JSON，不要总结** |
| `HTTP_ERROR` | HTTP 请求失败 | 检查网络连接或 API 服务状态 |
| `CONFIG_ERROR` | 配置错误 | 检查 `SCAN_WEBSERVICE_KEY` 环境变量是否正确 |
| `TIMEOUT` | 请求超时 | 检查网络后重试 |
| `NETWORK_ERROR` | 网络错误 | 检查网络连接 |
| `JSON_PARSE_ERROR` | 响应解析失败 | 联系技术支持或检查 API 返回原始内容 |
| `URL_VALIDATION_ERROR` | URL 格式验证失败 | 检查 URL 是否正确（需以 http:// 或 https:// 开头） |
| `BASE64_DECODE_ERROR` | BASE64 解码失败 | 检查 BASE64 字符串是否完整、合法 |
| `BASE64_FORMAT_ERROR` | BASE64 格式错误 | 检查 Data URL 格式是否正确 |
| `FILE_ERROR` | 本地文件验证失败 | 检查文件是否存在、格式是否支持、大小是否超限 |
| `FILE_READ_ERROR` | 文件读取失败 | 检查文件权限或磁盘空间 |
| `INVALID_INPUT` | 输入参数错误 | 确保只提供了一个输入参数（URL/路径/BASE64 三选一） |
| `INVALID_JSON` | JSON 配置格式错误 | 检查 `--input-configs` 或 `--output-configs` 是否为合法 JSON 字符串 |

---

## 🎯 意图路由（when to use）

> [!IMPORTANT] **⚠️ 全局流程控制**
> - **单一意图原则**：每次请求只执行一个意图类型，命中即执行
> - **接口返回即结束**：无论接口返回成功还是失败，都直接展示给用户
> - **不继续判断**：执行完一个意图后，**不再尝试其他意图**，不重试、不切换
> - **等待新指令**：任务完成后等待用户发起新的请求

> **AGENT 执行流程**：根据用户指令关键词匹配意图类型 → 点击链接获取完整执行策略（调用命令 + 返回结构 + 示例）→ 执行后直接返回结果

---

### 📋 意图类型与 API 场景映射

> 💡 **编号说明**：意图编号 (1-2) 为内部逻辑序号，场景编号 (31-32) 对应夸克 API 场景 ID，保持独立便于未来扩展。

| 逻辑序号 | 意图类型 | API 场景 | 场景文件                                                                                |
|------|---------|--------|-------------------------------------------------------------------------------------|
| 前置 | 环境变量检查 | 自动检查   | [00-auth-check.md](references/scenarios/00-auth-check.md)                           |
| 1    | 图片转 Excel | 31     | [31-image-to-excel.md](references/scenarios/31-image-to-excel.md)                       |
| 2    | 图片转 Word| 32     | [32-image-to-word.md](references/scenarios/32-image-to-word.md)               |
---

### 🔍 意图匹配规则

**⚠️ 前置检查：环境变量**（自动执行，非意图）
- 在调用任何场景前，**自动检查** `SCAN_WEBSERVICE_KEY` 是否已配置
- 若未配置，直接提示用户获取密钥，**不执行任何 API 调用**
- 检查逻辑参考：[00-auth-check.md](references/scenarios/00-auth-check.md)

**逻辑序号 1 - 图片转 Excel**（API 场景 31）
- 当用户请求将包含表格、数据、报表的图片、截图或扫描件转换为Excel (.xlsx/.xls) 文件，触发此意图。
- [⚠️ 获取执行策略](references/scenarios/31-image-to-excel.md)

**逻辑序号 2 - 图片转 Word**（API 场景 32）
- 当用户请求将图片、截图、照片或扫描件转换为Word 文档 触发此意图。
- [⚠️ 获取执行策略](references/scenarios/32-image-to-word.md)

---

### ⚠️ 匹配顺序说明

1. **前置检查**：调用任何场景前，自动检查 `SCAN_WEBSERVICE_KEY` 环境变量
2. **顺序匹配**：按逻辑序号升序匹配（1 → 2 ），命中即止
---

## ⛔ 不适用场景（When Not to Use）

> 本技能**不支持**以下场景，请勿尝试：

| 不支持的场景 | 原因 | 建议替代方案 |
|------------|------|------------|
| **视频处理** | 仅支持单张静态图片 | 先提取视频帧，再逐帧处理 |
| **批量处理** | 每次调用仅限单张图片 | 如需批量，请循环调用或联系管理员 |
| **实时摄像头流** | 非实时流处理架构 | 使用专用视频处理服务 |
| **超大图片（>5MB）** | API 限制 | 先压缩或裁剪后再处理 |
| **非图片格式** | 仅支持 jpg/jpeg/png/gif/bmp/webp/tiff/wbmp | 先转换为支持的图片格式 |

---

## 💡 示例参考

> 每个意图场景的完整调用示例已在对应场景文件中提供，请直接查阅：
> - 各场景调用命令 + 响应结构 + 完整示例：`references/scenarios/XX-xxx.md`
> - 通用参数规范：见上文「🚀 通用调用规范」章节

---

## ⚠️ 重要注意事项

1. **JSON 格式**: `--input-configs` 和 `--output-configs` 必须是 **JSON 字符串**
    - ✅ 正确：`--input-configs '{"function_option": "..."}'`
    - ❌ 错误：`--input-configs {"function_option": "..."}`

2. **安全与配额**: 严禁泄露 API Key，注意 `A0211` 配额限制

3. **图片大小**: 本地文件最大 5MB，支持 jpg/jpeg/png/gif/bmp/webp/tiff/wbmp/webp 格式

---

## 🔗 相关资源

- [夸克扫描王开放平台](https://scan.quark.cn/business)
- [API 通用规范](references/API.md)（可选参考）
- [场景文件目录](references/scenarios/)

---

## 📁 文件结构

> **环境依赖**: Python 3.9+，运行前执行 `pip3 install requests`

- `SKILL.md` —  本文档（意图分析 + 通用规范）
- `scripts/scan.py` —  主执行脚本（Python 3.9+，需 `requests` 库）
- `scripts/file_saver.py` —  文件保存工具（Python 3.9+）
- `scripts/outputs/` —  **输出目录（自动创建）**
   - `documents/` — Word/Excel 转换结果（`.docx` / `.xlsx`）
- `references/scenarios/` — 场景策略目录
   - `00-auth-check.md` — 环境变量检查
   - `31-image-to-excel.md` — 场景 31 [图片转 Excel]
   - `32-image-to-word.md` — 场景 32 [图片转 Word]

