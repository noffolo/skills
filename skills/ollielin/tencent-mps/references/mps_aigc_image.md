# AIGC 生图参数与示例 — `mps_aigc_image.py`

**功能**：AI 生成图片，支持文生图、图生图，支持 Hunyuan/GEM/Qwen 模型。
> ⚠️ 生成的图片默认存储 12 小时，请尽快下载使用。

## 参数说明

| 参数 | 说明 |
|------|------|
| `--prompt` | 图片描述文本（最多 1000 字符，未传参考图时必填）|
| `--model` | 模型：`Hunyuan`（默认）/ `GEM` / `Qwen` |
| `--model-version` | 模型版本，如 GEM `2.5` / `3.0` |
| `--negative-prompt` | 负向提示词 |
| `--enhance-prompt` | 开启提示词增强 |
| `--image-url` | 参考图 URL（可多次指定，GEM 支持最多 3 张）|
| `--image-ref-type` | 参考图类型（与 `--image-url` 一一对应）：`asset`（内容参考）/ `style`（风格参考）|
| `--image-cos-bucket` | 参考图所在 COS Bucket（可多次指定，与 `--image-url` 互斥）|
| `--image-cos-region` | 参考图所在 COS Region（可多次指定）|
| `--image-cos-key` | 参考图的 COS Key（可多次指定）|
| `--additional-parameters` | 附加参数（JSON 字符串，模型专属扩展参数）|
| `--aspect-ratio` | 宽高比（如 `16:9`、`1:1`）。支持：`1:1`, `3:2`, `2:3`, `3:4`, `4:3`, `4:5`, `5:4`, `9:16`, `16:9`, `21:9` |
| `--resolution` | 分辨率：`720P` / `1080P` / `2K` / `4K` |
| `--no-wait` | 只提交任务，不等待结果 |
| `--task-id` | 查询已有任务结果 |
| `--cos-bucket-name` | 结果存储 COS Bucket（不配置则使用 MPS 临时存储 12 小时）|
| `--cos-bucket-region` | 结果存储 COS 区域 |
| `--cos-bucket-path` | 结果存储 COS 路径前缀，默认 `/output/aigc-image/` |
| `--download-dir` | 任务完成后将生成图片下载到指定本地目录（默认仅打印预签名 URL）|
| `--operator` | 操作者名称（可选）|
| `--poll-interval` | 轮询间隔（秒），默认 5 |
| `--max-wait` | 最长等待时间（秒），默认 300 |
| `--verbose` / `-v` | 输出详细信息 |
| `--region` | MPS 服务区域（优先读取 `TENCENTCLOUD_API_REGION` 环境变量，默认 `ap-guangzhou`）|
| `--dry-run` | 只打印参数，不调用 API |

## 强制规则

- **AIGC 脚本不支持 `--cos-object` 参数**，禁止使用。COS 参考图必须用专属参数：
  - `--image-cos-bucket` + `--image-cos-region` + `--image-cos-key`（可多次指定）
- 用户提供 bucket/region/key 时，必须完整传入这三个参数，不得省略。

```bash
# COS 图生图（明确指定 bucket/region/key）
python scripts/mps_aigc_image.py --prompt "城市夜景" \
    --image-cos-bucket mps-test-1234567 \
    --image-cos-region ap-guangzhou \
    --image-cos-key input/ref.jpg
```

## 示例命令

```bash
# 文生图（Hunyuan 默认）
python scripts/mps_aigc_image.py --prompt "一只可爱的橘猫在阳光下打盹"

# GEM 3.0 + 反向提示词 + 16:9 + 2K
python scripts/mps_aigc_image.py --prompt "赛博朋克城市夜景" --model GEM --model-version 3.0 \
    --negative-prompt "人物" --aspect-ratio 16:9 --resolution 2K

# 图生图（参考图片 + 描述）
python scripts/mps_aigc_image.py --prompt "将这张照片变成油画风格" \
    --image-url https://example.com/photo.jpg

# GEM 多图参考（支持 asset/style 参考类型）
python scripts/mps_aigc_image.py --prompt "融合这些元素" --model GEM \
    --image-url https://example.com/img1.jpg --image-ref-type asset \
    --image-url https://example.com/img2.jpg --image-ref-type style

# 仅提交任务不等待
python scripts/mps_aigc_image.py --prompt "产品海报" --no-wait

# 查询任务结果
python scripts/mps_aigc_image.py --task-id abc123def456-aigc-image-20260328112000
```

