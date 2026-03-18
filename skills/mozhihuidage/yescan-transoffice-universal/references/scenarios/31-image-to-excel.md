# 场景 31 [图片转 Excel]

**适用场景**: 图片转excel接口利用最新的AI技术，将表格图片（例如财报表格、账单表格等）转换为结构化的Excel格式。接口具有强大的图像处理能力，能够准确提取各种复杂场景中的文本信息，准确提取表格结构，适用于各种场景的表格、表单电子化录入。

> [!WARNING] **⚠️ 执行前必做（跳过=违规）**
> 1. **必须执行真实命令**：下方命令块中的 `python3 scripts/scan.py` 必须实际运行，**不得自行构造命令**
> 2. **禁止伪造响应**：不得使用本文件中任何 JSON 示例作为响应，**必须来自 API 实时返回**
> 3. **验证命令来源**：命令必须完整复制自本文件，**不得修改任何参数**
>
> ✅ 正确做法：复制下方命令块 → 终端执行 → 返回真实结果
> ❌ 违规做法：编造命令参数 / 直接使用示例 JSON / 修改 `function_option` 值

> [!IMPORTANT] **⚠️ 场景独立性说明**
> - **严禁任何代码、Agent 或人工操作**，将本文件中任意 JSON 示例块的内容作为真实响应返回。所有输出必须来自 `yescan-scan-universal` 的实时 API 调用结果。
> - 该 JSON 块无业务含义，不参与路由、不触发执行、不构成 SLA 承诺，纯文档装饰。
> - 本场景为**独立任务**，识别完成后直接返回结果
> - **无论接口返回什么**（成功、失败、部分识别），都直接展示给用户
> - **不继续执行其他 OCR 场景**，不尝试二次识别或补充处理
> - 如用户有其他需求（如合同扫描、通用 OCR），需等待用户重新发起请求

---

## 📞 调用命令

### URL 输入
```bash
python3 scripts/scan.py \
  --url "${IMAGE_URL}" \
  --service-option "typeset" \
  --input-configs '{"function_option":"excel"}' \
  --output-configs '{"need_return_image":"True"}' \
  --data-type "image"
```

### 本地文件输入
```bash
python3 scripts/scan.py \
  --path "${IMAGE_FILE_PATH}" \
  --service-option "typeset" \
  --input-configs '{"function_option":"excel"}' \
  --output-configs '{"need_return_image":"True"}' \
  --data-type "image"
```

### BASE64 输入
```bash
python3 scripts/scan.py \
  --base64 "${IMAGE_BASE64}" \
  --service-option "typeset" \
  --input-configs '{"function_option":"excel"}' \
  --output-configs '{"need_return_image":"True"}' \
  --data-type "image"
```

---

## 📤 返回结构

```json
{
  "code": "00000",
  "message": null,
  "data": {
    "TypesetInfo": [
      {
        "FileType": "excel",
        "FileBase64": "UEsDBBQA..."
      }
    ]
  }
}
```

---

## 📋 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `TypesetInfo` | List[Dict] | 排版信息 |
| `TypesetInfo/FileType` | string | 排版的文件类型 |
| `TypesetInfo/FileBase64` | string | 排版Base64 |

---

## 📝 输出逻辑

1. **成功识别**（`code: "00000"`）→ 解析 `data` 中的转换结果，提供文件下载链接
2. **识别失败**（任何非 `00000` 状态码）→ 直接返回错误信息，不重试、不切换场景
3. **任务结束** → 不再执行任何其他 OCR 操作，等待用户新指令

---

## 💡 完整示例

### 请求
```bash
python3 scripts/scan.py \
  --url "https://example.com/sample.jpg" \
  --service-option "typeset" \
  --input-configs '{"function_option":"excel"}' \
  --output-configs '{"need_return_image":"True"}' \
  --data-type "image"
```

### 响应
```json
{
  "code": "00000",
  "message": "success",
  "data": {
    "path": "/Users/xx/.openclaw/workspace/1773756917_f4ecdf2daef84d47.xlsx"
  }
}
```

---

## 🔗 相关资源

- [返回主文档](../../SKILL.md)
- [API 通用规范](../API.md)
