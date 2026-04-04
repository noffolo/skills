# AIGC 生视频参数与示例 — `mps_aigc_video.py`

**功能**：AI 生成视频，支持文生视频、图生视频、分镜生成，支持 Hunyuan/Hailuo/Kling/Vidu/OS/GV 模型。
> ⚠️ 生成的视频默认存储 12 小时，请尽快下载使用。

## 参数说明

| 参数 | 说明 |
|------|------|
| `--prompt` | 视频描述文本（最多 2000 字符，未传图片时必填）|
| `--model` | 模型：`Hunyuan`（默认）/ `Hailuo` / `Kling` / `Vidu` / `OS` / `GV` |
| `--model-version` | 模型版本，如 Kling `2.5`/`O1`，Hailuo `2.3`，Vidu `q2-pro` |
| `--scene-type` | 场景类型：`motion_control`（Kling 动作控制）/ `land2port`（明眸横转竖）/ `template_effect`（Vidu 特效模板）|
| `--multi-shot` | **Kling 专属**。启用分镜功能 |
| `--multi-prompts-json` | **Kling 专属**。多分镜配置（JSON 数组），每个分镜含 `index`、`prompt`、`duration`。限制：1-6 个分镜，每个提示词最长 512 字符，所有时长之和必须等于总时长 |
| `--negative-prompt` | 负向提示词 |
| `--enhance-prompt` | 开启提示词增强 |
| `--image-url` | 参考图（首帧）URL（单张，图生视频时使用）|
| `--last-image-url` | 参考图（尾帧）URL（部分模型支持，需同时传 `--image-url`）|
| `--image-cos-bucket` | 首帧图片所在 COS Bucket（与 `--image-url` 互斥）|
| `--image-cos-region` | 首帧图片所在 COS Region |
| `--image-cos-key` | 首帧图片的 COS Key |
| `--last-image-cos-bucket` | 尾帧图片所在 COS Bucket |
| `--last-image-cos-region` | 尾帧图片所在 COS Region |
| `--last-image-cos-key` | 尾帧图片的 COS Key |
| `--ref-image-url` | 多图参考 URL（可多次指定，GV/Vidu 支持，最多 3 张）|
| `--ref-image-type` | 多图参考类型（与 `--ref-image-url` 一一对应）：`asset`（内容参考）/ `style`（风格参考）|
| `--ref-image-cos-bucket` | 多图参考所在 COS Bucket（可多次指定）|
| `--ref-image-cos-region` | 多图参考所在 COS Region（可多次指定）|
| `--ref-image-cos-key` | 多图参考的 COS Key（可多次指定）|
| `--duration` | 视频时长（秒）。各模型支持范围：<br>- Hunyuan: 5s（默认）<br>- Hailuo: 6s（默认）/ 10s<br>- Kling: 5s / 10s（默认）<br>- Vidu: 4s / 8s（默认）<br>- OS: 5s（默认）/ 10s<br>- GV: 5s（默认）/ 10s |
| `--resolution` | 分辨率：`720P` / `1080P` / `2K` / `4K` |
| `--aspect-ratio` | 宽高比（如 `16:9`, `9:16`, `1:1`, `4:3`, `3:4`）|
| `--no-logo` | 去除水印（Hailuo/Kling/Vidu 支持）|
| `--enable-bgm` | 启用背景音乐（部分模型版本支持）|
| `--enable-audio` | 是否为视频生成音频（GV/OS 支持，可选值: `true`/`false`）|
| `--ref-video-url` | 参考视频 URL（仅 Kling O1 支持）|
| `--ref-video-type` | 参考视频类型：`feature`（特征参考）/ `base`（待编辑视频，默认）|
| `--keep-original-sound` | 保留原声：`yes` / `no` |
| `--ref-video-cos-bucket` | 参考视频所在 COS Bucket（可多次指定）|
| `--ref-video-cos-region` | 参考视频所在 COS Region（可多次指定）|
| `--ref-video-cos-key` | 参考视频的 COS Key（可多次指定）|
| `--off-peak` | 错峰模式（仅 Vidu），任务 48 小时内生成 |
| `--additional-params` | JSON 格式附加参数，用于传递模型专属扩展参数（如 Kling 相机控制）|
| `--no-wait` | 只提交任务，不等待结果 |
| `--task-id` | 查询已有任务结果 |
| `--cos-bucket-name` | 结果存储 COS Bucket（不配置则使用 MPS 临时存储 12 小时）|
| `--cos-bucket-region` | 结果存储 COS 区域 |
| `--cos-bucket-path` | 结果存储 COS 路径前缀，默认 `/output/aigc-video/` |
| `--download-dir` | 任务完成后将生成视频下载到指定本地目录（默认仅打印预签名 URL）|
| `--operator` | 操作者名称（可选）|
| `--poll-interval` | 轮询间隔（秒），默认 10 |
| `--max-wait` | 最长等待时间（秒），默认 1800 |
| `--verbose` / `-v` | 输出详细信息 |
| `--region` | MPS 服务区域（优先读取 `TENCENTCLOUD_API_REGION` 环境变量，默认 `ap-guangzhou`）|
| `--dry-run` | 只打印参数，不调用 API |

## 强制规则

- **AIGC 脚本不支持 `--cos-object` 参数**，禁止使用。COS 输入必须用专属参数：
  - 首帧图片：`--image-cos-bucket` + `--image-cos-region` + `--image-cos-key`
  - 尾帧图片：`--last-image-cos-bucket` + `--last-image-cos-region` + `--last-image-cos-key`
  - 多图参考：`--ref-image-cos-bucket` + `--ref-image-cos-region` + `--ref-image-cos-key`
  - 参考视频：`--ref-video-cos-bucket` + `--ref-video-cos-region` + `--ref-video-cos-key`
- 用户提供 bucket/region/key 时，必须完整传入这三个参数，不得省略。

```bash
# COS 图生视频（明确指定 bucket/region/key）
python scripts/mps_aigc_video.py --prompt "花朵随风摇曳" \
    --image-cos-bucket mps-test-1234567 \
    --image-cos-region ap-guangzhou \
    --image-cos-key input/scene.jpg
```

## 分镜功能说明（Kling 专属）

### 单分镜模式（系统自动拆分）
```bash
python scripts/mps_aigc_video.py --prompt "旅行日记，记录美好瞬间" --model Kling --multi-shot
```

### 多分镜模式（自定义每个分镜）
```bash
python scripts/mps_aigc_video.py --model Kling --multi-shot --duration 12 \
    --multi-prompts-json '[
      {"index": 1, "prompt": "日出时分，从酒店窗户看城市天际线", "duration": "3"},
      {"index": 2, "prompt": "在咖啡馆享用早餐，窗外街道行人", "duration": "4"},
      {"index": 3, "prompt": "公园里散步，阳光透过树叶", "duration": "5"}
    ]'
```

**校验规则**：分镜数量 1-6 个；每个提示词最长 512 字符；每个时长 ≥ 1 秒；所有时长之和必须等于总时长。

## 示例命令

```bash
# 文生视频（Hunyuan 默认）
python scripts/mps_aigc_video.py --prompt "一只猫在阳光下伸懒腰"

# Kling 2.5 + 10秒 + 1080P + 16:9 + 去水印 + BGM
python scripts/mps_aigc_video.py --prompt "赛博朋克城市" --model Kling --model-version 2.5 \
    --duration 10 --resolution 1080P --aspect-ratio 16:9 --no-logo --enable-bgm

# 图生视频（首帧图片 + 描述）
python scripts/mps_aigc_video.py --prompt "让画面动起来" \
    --image-url https://example.com/photo.jpg

# 首尾帧生视频（GV 模型）
python scripts/mps_aigc_video.py --prompt "过渡动画" --model GV \
    --image-url https://example.com/start.jpg --last-image-url https://example.com/end.jpg

# GV 多图参考生视频（支持 asset/style 参考类型）
python scripts/mps_aigc_video.py --prompt "融合风格生成视频" --model GV \
    --ref-image-url https://example.com/img1.jpg --ref-image-type asset \
    --ref-image-url https://example.com/img2.jpg --ref-image-type style

# Kling O1 参考视频 + 保留原声
python scripts/mps_aigc_video.py --prompt "将视频风格化" --model Kling --model-version O1 \
    --ref-video-url https://example.com/video.mp4 --ref-video-type base --keep-original-sound yes

# Vidu 错峰模式
python scripts/mps_aigc_video.py --prompt "自然风景" --model Vidu --off-peak

# 仅提交任务不等待
python scripts/mps_aigc_video.py --prompt "宣传片" --no-wait

# 查询任务结果
python scripts/mps_aigc_video.py --task-id abc123def456-aigc-video-20260328112000
```
