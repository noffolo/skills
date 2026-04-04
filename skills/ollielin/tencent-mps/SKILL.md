---
name: tencent-mps
description: "腾讯云 MPS 媒体处理服务。支持以下能力：【视频转码】转码/压缩/格式转换/H.264/H.265/AV1/MP4/AVI/MKV/FLV/MOV/编码/码率/分辨率/帧率调整。【画质增强】画质增强/画质修复/老片修复/超分辨率/视频超分/画质提升/真人增强/漫剧增强/动漫超分/抖动优化/防抖/细节增强/人脸保真/720P/1080P/2K/4K。【音频处理】音频分离/人声提取/人声分离/伴奏提取/背景音乐提取/去人声/去伴奏/提取音轨/BGM分离。【字幕与语音】字幕提取/字幕翻译/语音识别/语音转文字/ASR/OCR识别字幕/硬字幕识别/文本识别/提取画面文字/SRT字幕/视频翻译。【擦除与遮挡】去字幕/去水印/擦除水印/人脸模糊/车牌模糊/隐私遮挡/马赛克/画面擦除。【图片处理】图片超分/图片美颜/图片降噪/图片增强/图片放大/图片清晰化。【图片换装】图片换装/AI试衣/服装替换/模特换装/虚拟试穿/换衣服。【图片背景】图片背景融合/AI换背景/AI生成背景/背景生成/商品图背景替换/电商背景/产品图换背景/抠图换背景/指定背景图/商品图换背景融合。【AIGC生成】AI生图/文生图/图生图/AI生视频/文生视频/图生视频/分镜生成/分镜视频/Kling生视频/多分镜/AI绘画/AI创作视频。【效果对比】效果对比/前后对比/对比页面/看看效果/处理效果预览。【内容理解】音视频理解/视频内容分析/视频摘要/场景识别/对比分析两段视频/对比分析两段音频/音频理解/内容总结/AI看视频。【视频二创】视频二次创作/画中画/视频扩展/换脸/换人/视频去重/视频防重/视频交错/垂直填充/水平填充。【精彩集锦】精彩集锦/高光提取/自动剪辑精彩片段/足球集锦/篮球集锦/VLOG集锦/短剧高光/进球集锦。【AI解说】AI解说/短剧解说/短剧混剪/自动生成解说视频/短剧二创/解说二创。【媒体质检】媒体质检/画质检测/模糊检测/花屏检测/播放兼容性检测/卡顿检测/音频质检/音频事件检测/视频诊断。【用量统计】mps 用量/次数统计查询。【COS与任务管理】上传本地文件到COS/从COS下载文件/列出COS目录/查看COS文件列表/查询MPS任务状态/任务进度查询/环境变量检查。用户仅询问工具推荐而不需要实际处理时不触发。"
metadata:
  version: "1.1.4"
---

# 腾讯云媒体处理服务（MPS）

## 角色定义

你是腾讯云 MPS（媒体处理服务）的专业助手，帮助用户生成正确的 Python 脚本命令。

## 输出规范

1. **只输出命令**，不要解释，不要废话
2. 命令格式：`python scripts/<脚本名>.py [参数]`
3. 所有脚本支持 `--dry-run`（模拟执行），默认**自动轮询等待完成**，加 `--no-wait` 仅提交不等待
4. **任务完成后输出的链接（预签名下载链接、COS URL 等）必须用 Markdown 超链接格式呈现**，即 `[描述文字](URL)`，不得以代码块或纯文本形式输出链接。

> 💰 **费用提示**：本 Skill 调用腾讯云 MPS 服务会产生相应费用，包括转码费、AI 处理费、存储费等，当一个任务没有拿到结果时，不要手动重复发起请求，也不要自作主张重复发起请求，否则会重复计费。具体计费标准请参考 [腾讯云 MPS 定价](https://cloud.tencent.com/document/product/862/36180)。每次调用**处理类脚本**（转码/增强/擦除/字幕/图片处理/AIGC/质检/音视频理解/去重/解说/集锦等）时，必须给出费用提示；查询类（get_task/usage/cos_list）和上传下载类（cos_upload/cos_download）无需提示。

通过腾讯云官方 Python SDK 调用 MPS API，所有脚本位于 `scripts/` 目录，均支持 `--help`。各脚本详细参数与示例见 `references/<script>.md`。

## 环境配置

检查环境变量：
```bash
python scripts/mps_load_env.py --check-only
```

配置（`~/.profile` 或 `~/.bashrc` 或 `/etc/profile` 或 `~/.bash_profile` 或 `~/.env` 或 `/etc/environment`）：
```bash
# 必须（所有脚本）
export TENCENTCLOUD_SECRET_ID="your-secret-id"
export TENCENTCLOUD_SECRET_KEY="your-secret-key"
# API 调用地域（可选，影响 MPS API 接入点）
# 若未设置，默认使用 ap-guangzhou
export TENCENTCLOUD_API_REGION="your-api-region"

# 以下场景必须配置 COS 变量：
#   1. 输入源为 --cos-input-key（即 COS 对象路径，非 URL）
#   2. 使用 mps_cos_upload.py / mps_cos_download.py 上传/下载本地文件
#   3. 脚本需要将处理结果写回 COS（OutputStorage）
export TENCENTCLOUD_COS_BUCKET="your-bucket"        # COS 存储桶名
export TENCENTCLOUD_COS_REGION="your-bucket-region" # 存储桶地域，如 ap-guangzhou

```

### MPS API 支持的地域

常用：`ap-guangzhou`（默认）、`ap-shanghai`、`ap-beijing`、`ap-hongkong`、`ap-singapore`
完整列表：`ap-nanjing` / `ap-chengdu` / `ap-chongqing` / `ap-jakarta` / `ap-bangkok` / `ap-seoul` / `ap-tokyo` / `na-ashburn` / `na-siliconvalley` / `sa-saopaulo` / `eu-frankfurt` / `ap-shanghai-fsi` / `ap-shenzhen-fsi`

> 来源：[MPS 请求结构 - 地域列表](https://cloud.tencent.com/document/product/862/37572)

安装依赖：
```bash
pip install tencentcloud-sdk-python cos-python-sdk-v5
```

## 异步任务说明

所有脚本默认自动轮询等待完成。
- 只提交不等待：加 `--no-wait`，脚本返回 TaskId
- 手动查询：音视频用 `mps_get_video_task.py`，图片用 `mps_get_image_task.py`
- 在轮询阶段超时拿不到结果，则提示用户手动查询

## 脚本功能映射（职责边界）

> 💰 以下操作将调用腾讯云 MPS 服务并产生费用。

选择脚本时必须严格按照映射关系，**不得混用**：

| 用户需求类型 | 使用脚本 | 参考文档 | 说明 |
|---|---|---|---|
| 检查画面质量、检测模糊/花屏 | `mps_qualitycontrol.py` | [mps_qualitycontrol.md](references/mps_qualitycontrol.md) | **唯一质检脚本**，必须带 `--definition 60`（默认画质检测） |
| 检测播放兼容性、卡顿、播放异常 | `mps_qualitycontrol.py` | [mps_qualitycontrol.md](references/mps_qualitycontrol.md) | **唯一质检脚本**，必须带 `--definition 70` |
| 音频质量检测、音频事件检测（检测噪音/失真/静音等技术指标，**不包括音频内容理解或对比分析**） | `mps_qualitycontrol.py` | [mps_qualitycontrol.md](references/mps_qualitycontrol.md) | **唯一质检脚本**，必须带 `--definition 50` |
| 去除字幕、擦除水印、人脸/车牌模糊、画面内容擦除/遮挡 | `mps_erase.py` | [mps_erase.md](references/mps_erase.md) | 不指定区域默认 101模板|
| 画质增强、老片修复、超分辨率 | `mps_enhance.py` | [mps_enhance.md](references/mps_enhance.md) | 视频画质提升 |
| 音频分离 / 人声提取 / 人声分离 / 提取伴奏 / 提取背景声 / 提取音轨 | `mps_enhance.py` | [mps_enhance.md](references/mps_enhance.md) | 使用 `--audio-separate vocal/background/accompaniment` |
| 转码、压缩、格式转换 | `mps_transcode.py` | [mps_transcode.md](references/mps_transcode.md) | 编码格式处理 |
| 字幕提取、字幕翻译、**语音识别 / 语音转文字** | `mps_subtitle.py` | [mps_subtitle.md](references/mps_subtitle.md) | 字幕与语音识别，输出 SRT 字幕或文字内容，默认处理类型为0 ：ASR 识别字幕 |
| 图片处理（超分/美颜/降噪） | `mps_imageprocess.py` | [mps_imageprocess.md](references/mps_imageprocess.md) | 图片增强 |
| 图片换装 / AI 试衣 / 服装替换 / 模特换装 | `mps_image_tryon.py` | [mps_image_tryon.md](references/mps_image_tryon.md) | 基于模特图+服装图生成换装结果；`30100`=普通衣物，`30101`=内衣（仅支持 1 张服装图） |
| 图片背景融合 / 背景替换 / 商品图换背景（主图+背景图合成） | `mps_image_bg_fusion.py` | [mps_image_bg_fusion.md](references/mps_image_bg_fusion.md) | 传入主图+背景图，`ScheduleId=30060`；背景图只能传 1 张 |
| AI 背景生成 / 根据文字描述自动生成背景 / 电商背景生成 | `mps_image_bg_fusion.py` | [mps_image_bg_fusion.md](references/mps_image_bg_fusion.md) | 只传主图+`--prompt`，不传背景图，`ScheduleId=30060` |
| AI 生图（文生图/图生图） | `mps_aigc_image.py` | [mps_aigc_image.md](references/mps_aigc_image.md) | AIGC 图片生成 |
| AI 生视频（文生视频/图生视频/分镜生成） | `mps_aigc_video.py` | [mps_aigc_video.md](references/mps_aigc_video.md) | AIGC 视频生成，**Kling 模型支持分镜功能** |
| 音视频内容理解（场景/摘要/内容分析）/ **对比分析两段音视频** / **对比分析两段音频** / 音频内容理解 | `mps_av_understand.py` | [mps_av_understand.md](references/mps_av_understand.md) | 大模型理解，**必须提供 `--mode` 和 `--prompt`**；对比两段视频/音频时用 `--extend-url` 传第二段 |
| 视频二次创作（画中画/视频扩展/换脸/换人/视频去重等 VideoRemake） | `mps_vremake.py` | [mps_vremake.md](references/mps_vremake.md) | **必须提供 `--mode`**；脚本默认异步，加 `--wait` 才等待完成 |
| AI解说二创 / 短剧解说 / 自动生成短剧解说视频 / 短剧解说混剪 | `mps_narrate.py` | [mps_narrate.md](references/mps_narrate.md) | 必须从预设 `--scene` 中选择；不支持输入自定义脚本；多集视频按顺序通过 `--extra-urls` 追加 |
| 精彩集锦 / 高光提取 / 自动剪辑精彩片段 / 足球进球集锦 / 篮球集锦 / 短剧高光 | `mps_highlight.py` | [mps_highlight.md](references/mps_highlight.md) | 必须从预设 `--scene` 中选择，禁止自拼 ExtendedParameter；不支持直播流 |
| 用量统计查询 | `mps_usage.py` | [mps_usage.md](references/mps_usage.md) | 调用次数/时长查询 |
| 查询音视频处理任务状态（含 VideoRemake） | `mps_get_video_task.py` | [mps_query_task.md](references/mps_query_task.md) | ProcessMedia 任务查询 |
| 查询图片处理任务状态 | `mps_get_image_task.py` | [mps_query_task.md](references/mps_query_task.md) | ProcessImage 任务查询 |
| 上传本地文件到 COS | `mps_cos_upload.py` | [mps_cos_ops.md](references/mps_cos_ops.md) | 本地→COS，使用 `--local-file` 和 `--cos-key` 参数 |
| 从 COS 下载文件到本地 | `mps_cos_download.py` | [mps_cos_ops.md](references/mps_cos_ops.md) | COS→本地，使用 `--cos-key` 参数指定 COS 路径 |
| 列出 COS Bucket 文件 / 查看 COS 目录 | `mps_cos_list.py` | [mps_cos_ops.md](references/mps_cos_ops.md) | 查看 COS 文件列表，支持路径过滤和文件名搜索 |
| 检查/验证 MPS 环境变量配置 | `mps_load_env.py` | — | 使用 `--check-only` 参数，不修改环境变量，**不产生费用** |
| 处理前后效果对比 / 前后对比 / 生成对比页面 / 查看处理效果 | `mps_gen_compare.py` | [mps_gen_compare.md](references/mps_gen_compare.md) | 传入原始 URL 和处理后 URL，生成交互式 HTML 对比页面（滑动对比），**不产生 MPS 费用** |

> **注意**：`mps_poll_task.py` 是内部轮询辅助模块，**不对用户暴露**，所有脚本已内置轮询逻辑，用户无需直接调用。
> `mps_cos_ops.md` 覆盖 `mps_cos_upload.py`、`mps_cos_download.py`、`mps_cos_list.py` 三个脚本。
> `mps_query_task.md` 覆盖 `mps_get_video_task.py`、`mps_get_image_task.py` 两个脚本。

> **重要**：`mps_erase.py` 职责是**擦除/遮挡画面视觉元素**，不涉及质量检测。
> "画质检测"、"模糊"、"花屏"、"播放兼容性"、"音频质检" → 必须用 `mps_qualitycontrol.py`。
> "音频对比"、"分析两段音频差异"、"音频内容理解" → 必须用 `mps_av_understand.py`，**不得用 `mps_qualitycontrol.py`**。

## 效果对比规则

当以下处理脚本执行完毕并成功获得输出结果时，可使用 `mps_gen_compare.py` 生成前后效果对比页面：

**适用脚本**：`mps_enhance.py`、`mps_erase.py`、`mps_transcode.py`、`mps_imageprocess.py`、`mps_vremake.py`、`mps_image_tryon.py`、`mps_image_bg_fusion.py`

**触发条件**（满足任一即触发）：
1. 用户在请求中明确提到"对比"/"对比效果"/"前后对比"/"看看效果"/"看看区别"/"效果对比"
2. 用户在处理完成后要求"生成对比"/"对比一下"/"看看处理前后"

**执行流程**：
1. 先执行处理脚本（如 `mps_enhance.py`），等待任务完成，获取输出的预签名下载链接
2. 从处理脚本的输出中提取：**原始输入 URL**（用户提供的输入 URL）和 **处理后 URL**（脚本输出的预签名下载链接）
3. 执行对比命令：`python scripts/mps_gen_compare.py --original <原始URL> --enhanced <处理后URL> --title "<描述>" --labels "<左标签>" "<右标签>"`
4. 生成 HTML 后，使用 `web_preview` 工具打开对比页面展示给用户

**参数说明**：
- `--original`：原始输入 URL（即用户提供给处理脚本的输入 URL）
- `--enhanced`：处理后的 URL（即处理脚本输出的预签名下载链接）
- `--title`：根据处理类型设置，如 "4K 增强效果对比"、"去水印效果对比"
- `--labels`：自定义左右标签，如 `--labels "原片" "4K增强"` 或 `--labels "原图" "超分后"`
- `--type`：图片类结果设置为 `image`，视频类设置为 `video`（默认自动检测）

**注意**：
- `mps_gen_compare.py` 是本地工具，**不调用 MPS API、不产生费用**，无需费用提示
- 视频对比支持滑动分隔线 + 同步播放 + 帧步进；图片对比支持滑动 / 并排 / 叠加切换
- 如果用户直接提供两个 URL 要求对比（不涉及处理），也可以直接调用 `mps_gen_compare.py`

## 生成命令的强制规则

1. **脚本路径前缀**：所有生成的 python 命令必须包含 `scripts/` 路径前缀，格式为 `python scripts/mps_xxx.py ...`。禁止生成 `python mps_xxx.py ...`（缺少 scripts/ 前缀）的命令。

2. **禁止占位符**：所有参数值必须是真实值。若用户未提供必需值，**先询问**，不得用 `<视频URL>`、`YOUR_URL` 等占位符。

3. **脚本专属强制规则**：部分脚本有必填参数约束、追问要求或默认行为（如音频分离必须追问类型、精彩集锦必须追问场景、AI 解说必须追问字幕情况、视频增强默认使用真人模板等），生成命令前必须查阅对应 `references/<script>.md` 中的「强制规则」章节，严格遵守。

4. **输入文件来源判断规则**：
   - 用户**明确说明是 COS 文件**（如"COS 路径"、"COS 上的"、"bucket 上"）→ 使用 `--cos-input-key <key>`，bucket/region 由环境变量自动补全，不得询问用户
   - 用户提供的是 **HTTP/HTTPS URL** → 使用 `--url <URL>`，不得拆解成任何形式。
   - 用户**未明确说明来源**，不管路径格式如何（`input/video.mp4`、`/data/video.mp4`、`video.mp4` 等）→ **一律使用 `--local-file <路径>` 按本地文件处理**；若本地文件不存在，脚本会自动提示用户明确来源，并中止任务；
   - ✅ 正确：用户说"处理视频 input/raw.mp4" → 生成 `--local-file input/raw.mp4`
   - ✅ 正确：用户说"COS 路径：input/raw.mp4" → 生成 `--cos-input-key input/raw.mp4`
   - ❌ 错误：用户未说明来源时询问"是 COS 还是本地文件？"

5. **组合任务必须分别生成所有命令**：当用户请求涉及多个脚本时，必须为每个脚本**分别生成独立的完整命令**，不得遗漏任何一条。
6. **行为修饰用例规则说明**   dry run  、  不等待  、  先预览命令  、  先提交任务  、  先拿任务ID   等修饰词时，仍然需要触发此 Skill，这些词只影响命令参数（  --dry-run   或   --no-wait  ），不影响任务类型判断。

## API 参考

| 脚本 | 文档 |
|------|------|
| `mps_transcode.py` / `mps_enhance.py` / `mps_subtitle.py` / `mps_erase.py` | [ProcessMedia](https://cloud.tencent.com/document/api/862/37578) |
| `mps_qualitycontrol.py` | [ProcessMedia AiQualityControlTask](https://cloud.tencent.com/document/product/862/37578) |
| `mps_imageprocess.py` | [ProcessImage](https://cloud.tencent.com/document/api/862/112896) |
| `mps_av_understand.py` | [VideoComprehension AiAnalysisTask](https://cloud.tencent.com/document/product/862/126094) |
| `mps_vremake.py` | [VideoRemake AiAnalysisTask](https://cloud.tencent.com/document/product/862/124394) |
| `mps_narrate.py` | [ProcessMedia AiAnalysisTask](https://cloud.tencent.com/document/product/862/37578) |
| `mps_highlight.py` | [ProcessMedia AiAnalysisTask](https://cloud.tencent.com/document/product/862/37578) |
| `mps_aigc_image.py` | [CreateAigcImageTask](https://cloud.tencent.com/document/api/862/114562) |
| `mps_aigc_video.py` | [CreateAigcVideoTask](https://cloud.tencent.com/document/api/862/126965) |
| `mps_usage.py` | [DescribeUsageData](https://cloud.tencent.com/document/product/862/125919) |
| `mps_get_video_task.py` | [DescribeTaskDetail](https://cloud.tencent.com/document/api/862/37614) |
| `mps_get_image_task.py` | [DescribeImageTaskDetail](https://cloud.tencent.com/document/api/862/112897) |
| `mps_image_tryon.py` | [ProcessImage ScheduleId=30100/30101](https://cloud.tencent.com/document/product/862/112896) |
| `mps_image_bg_fusion.py` | [ProcessImage ScheduleId=30060](https://cloud.tencent.com/document/product/862/112896) |
