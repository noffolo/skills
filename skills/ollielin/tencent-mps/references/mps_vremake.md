# 视频二次创作参数与示例 — `mps_vremake.py`

**功能**：视频二次创作（VideoRemake），支持画中画、视频扩展、换脸、换人、**视频去重**等多种模式。**视频去重也是视频二次创作的一种方式**，用户说"视频去重"时同样使用本脚本。
> **核心机制**：`AiAnalysisTask.Definition=29` + `ExtendedParameter(vremake.mode + 模式参数)`。
> 脚本**默认异步**（只提交任务返回 TaskId），加 `--wait` 才等待完成。

## 支持模式（含视频去重）

| 模式 | 说明 |
|------|------|
| `PicInPic` | 画中画（原视频缩小嵌入新背景）|
| `BackgroundExtend` | 视频扩展（在场景切换处插入扩展画面）|
| `VerticalExtend` | 垂直填充（上下填充）|
| `HorizontalExtend` | 水平填充（左右填充）|
| `AB` | 视频交错 |
| `SwapFace` | 换脸 |
| `SwapCharacter` | 换人 |

## 参数说明

| 参数 | 说明 |
|------|------|
| `--local-file` | 本地文件路径，自动上传到 COS 后处理（与 `--cos-input-*` 互斥）|
| `--url` | 视频 URL（HTTP/HTTPS），与 `--task-id` 互斥 |
| `--cos-input-key` | COS 输入文件的 Key（如 `/input/video.mp4`，推荐使用）|
| `--cos-input-bucket` | 输入文件所在 COS Bucket 名称（默认使用环境变量）|
| `--cos-input-region` | 输入文件所在 COS Region（如 `ap-guangzhou`）|
| `--task-id` | 查询已有任务结果，跳过创建 |
| `--mode` | **必填**。二次创作模式（含视频去重，见上表）|
| `--wait` | 等待任务完成后退出（默认只提交，异步）|
| `--llm-prompt` | 大模型提示词（生成背景**图片**，适用 PicInPic/AB）|
| `--llm-video-prompt` | 大模型提示词（生成背景**视频**，优先于 `--llm-prompt`）|
| `--min-scene-secs` | [BackgroundExtend] 插入扩展画面最小间隔（秒，默认 2.0）|
| `--random-move` | [PicInPic] 随机移动画中画位置 |
| `--random-cut` | 随机裁剪 |
| `--random-speed` | 随机加速 |
| `--random-flip` | 随机镜像（`true`/`false`，默认 `true`）|
| `--append-image` | [VerticalExtend/HorizontalExtend] 在视频开头/结尾插入图片（1.5秒）|
| `--append-image-prompt` | 开头/结尾图片生成提示词 |
| `--ext-mode` | [HorizontalExtend/AB] 扩展模式 `1`/`2`/`3` |
| `--src-faces` | [SwapFace] 原视频人脸 URL 列表（与 `--dst-faces` 一一对应，最多 6 张）|
| `--dst-faces` | [SwapFace] 目标人脸 URL 列表 |
| `--src-character` | [SwapCharacter] 原视频人物 URL（正面全身图）|
| `--dst-character` | [SwapCharacter] 目标人物 URL（正面全身图）|
| `--custom-json` | 自定义 vremake 扩展参数 JSON（与 `--mode` 自动合并）|
| `--json` | JSON 格式输出 |
| `--output-dir` | 将结果 JSON 保存到指定目录 |
| `--download-dir` | 任务完成后将输出视频下载到指定本地目录（默认仅打印预签名 URL）|
| `--definition` | AiAnalysisTask 模板 ID（默认 `29`）|
| `--region` | 处理地域（优先读取 `TENCENTCLOUD_API_REGION` 环境变量，默认 `ap-guangzhou`） |
| `--dry-run` | 只打印参数预览，不调用 API |

**SwapFace 限制**：视频分辨率 ≤ 4K；单张图片 < 10MB（jpg/png）；人脸总数 ≤ 6 张。
**SwapCharacter 限制**：视频时长 ≤ 20 分钟；需正面全身图。

## 示例命令

```bash
# 画中画去重（等待结果）
python scripts/mps_vremake.py --url https://example.com/video.mp4 --mode PicInPic --wait

# 视频扩展去重（COS 输入）
python scripts/mps_vremake.py --cos-input-key /input/video.mp4 --mode BackgroundExtend --wait

# 画中画 + LLM 提示词（背景图片）
python scripts/mps_vremake.py --url https://example.com/video.mp4 \
    --mode PicInPic --llm-prompt "生成一个唯美的自然风景背景图片" --wait

# 垂直填充 + LLM 提示词（背景视频）
python scripts/mps_vremake.py --url https://example.com/video.mp4 \
    --mode VerticalExtend --llm-video-prompt "随机生成一个自然风景视频" --wait

# 换脸模式（--src-faces 和 --dst-faces 一一对应）
python scripts/mps_vremake.py --url https://example.com/video.mp4 \
    --mode SwapFace \
    --src-faces https://example.com/src1.png https://example.com/src2.png \
    --dst-faces https://example.com/dst1.jpg https://example.com/dst2.jpg \
    --wait

# 换人模式（正面全身图）
python scripts/mps_vremake.py --url https://example.com/video.mp4 \
    --mode SwapCharacter \
    --src-character https://example.com/src_fullbody.png \
    --dst-character https://example.com/dst_fullbody.png \
    --wait

# 异步提交（默认，不加 --wait）
python scripts/mps_vremake.py --url https://example.com/video.mp4 --mode PicInPic

# 查询已有任务结果
python scripts/mps_vremake.py --task-id 2600011633-WorkflowTask-xxxxx

# dry-run 预览
python scripts/mps_vremake.py --url https://example.com/video.mp4 \
    --mode BackgroundExtend --min-scene-secs 3.0 --dry-run
```
