---
name: ai-image-generator
description: |
  AI 图片与视频异步生成技能，调用 AI Artist API 根据文本提示词生成图片或视频，自动轮询直到任务完成。

  ⚠️ 使用前必须设置环境变量 AI_ARTIST_TOKEN 为你自己的 API Key！
  获取 API Key：访问 https://staging.kocgo.vip/index 注册登录后创建。

  支持图片模型：SEEDREAM5_0（默认高质量图片）、NANO_BANANA_2（轻量快速）。
  支持视频模型：SEEDANCE_1_5_PRO（文生视频，支持音频）、SORA2（文生视频或首尾帧图生视频，支持 firstImageUrl/lastImageUrl）。

  触发场景：
  - 用户要求生成图片，如"生成一匹狼"、"画一只猫"、"风景画"、"帮我画"等。
  - 用户要求生成视频，如"生成视频"、"用 SORA2 生成"、"文生视频"、"图生视频"、"生成一段...的视频"等。
  - 用户指定模型：SEEDREAM5_0、NANO_BANANA_2、SEEDANCE_1_5_PRO、SORA2。
---

# AI Image Generator

异步生成 AI 图片与视频的技能。

## ⚠️ 首次使用必读

### 1. 获取 API Key

访问 [https://staging.kocgo.vip/index](https://staging.kocgo.vip/index) 注册并登录，然后创建你的 API Key。

### 2. 设置环境变量

**在使用前，你必须先设置自己的 API Key：**

```bash
# Linux/macOS/Git Bash (Windows)
export AI_ARTIST_TOKEN="sk-your_api_key_here"

# Windows PowerShell
$env:AI_ARTIST_TOKEN="sk-your_api_key_here"
```

### 3. 验证配置

**验证配置是否正确：**

```bash
python3 scripts/test_config.py
```

详细配置说明请查看下方"环境配置"章节。

## 快速开始

```bash
python3 scripts/generate_image.py "提示词"
```

## 在对话中直接返回图片

### 方式 1: Markdown 图片语法（推荐）

生成图片后，直接在回复中使用 Markdown 语法：

```markdown
![描述](图片URL)
```

**平台支持情况：**
- ✅ WebChat、Discord、Telegram：完全支持
- ✅ 飞书：支持（需公开 URL）
- ❌ WhatsApp：不支持

### 方式 2: 下载后发送（需要 message 工具）

使用 `--download` 参数下载图片，然后通过 message 工具发送：

```bash
python3 scripts/generate_image.py "风景画" --download
```

然后在代码中读取图片并发送：

```python
from scripts.generate_image import generate_image
import base64

result = generate_image(prompt="风景画", download=True)
if result and result["status"] == "SUCCESS":
    # 方式 A: 使用 data URI
    image_uri = result["data_uri"]  # data:image/png;base64,...
    
    # 方式 B: 读取本地文件
    with open(result["local_path"], "rb") as f:
        image_data = f.read()
        base64_data = base64.b64encode(image_data).decode()
```

## 参数说明

### 通用参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `prompt` | 必填 | 生成提示词（图片或视频描述）|
| `--model` | `SEEDREAM5_0` | 生成模型，可选: `SEEDREAM5_0`、`NANO_BANANA_2`、`SEEDANCE_1_5_PRO` |
| `--interval` | `5` | 轮询间隔(秒) |

### 图片专属参数（SEEDREAM5_0 / NANO_BANANA_2）

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--quality` | `2K` | 图片质量 (2K/4K) |
| `--size` | 模型默认值 | 图片尺寸。SEEDREAM5_0: `2048x2048`，NANO_BANANA_2: `1:1` |
| `--download` | - | 下载图片到本地 |
| `--output-dir` | `workspace/images` | 图片保存目录 |
| `--markdown-output` | - | 以 Markdown 格式输出图片链接 |

### 视频专属参数（SEEDANCE_1_5_PRO）

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--ratio` | `16:9` | 画面比例，如 `16:9`、`9:16`、`1:1` |
| `--resolution` | `720p` | 视频分辨率，如 `720p`、`1080p` |
| `--duration` | `10` | 视频时长（秒）|

## 支持的模型

### 图片模型

| 模型 | methodType | 默认尺寸 | 特点 |
|------|-----------|---------|------|
| `SEEDREAM5_0` | `4` | `2048x2048` | 默认模型，高质量，尺寸格式: WxH |
| `NANO_BANANA_2` | `5` | `1:1` | 轻量快速，尺寸格式: 比例 (如 1:1, 16:9) |

### 视频模型

| 模型 | methodType | 默认比例 | 默认分辨率 | 默认时长 | 特点 |
|------|-----------|---------|-----------|---------|------|
| `SEEDANCE_1_5_PRO` | `2` | `16:9` | `720p` | 10s | 文生视频，支持音频生成 |
| `SORA2` | `11` | `16:9` | `720p` | 4s | 图生视频，支持首尾帧控制（FIRST&LAST）|

## 使用示例

```bash
# 基础用法 - 默认模型 SEEDREAM5_0
python3 scripts/generate_image.py "一匹狼"

# 使用 NANO_BANANA_2 模型
python3 scripts/generate_image.py "生成一只狗" --model NANO_BANANA_2

# NANO_BANANA_2 指定尺寸比例
python3 scripts/generate_image.py "风景画" --model NANO_BANANA_2 --size "16:9"

# 下载图片
python3 scripts/generate_image.py "风景画" --download

# 高质量生成（SEEDREAM5_0）
python3 scripts/generate_image.py "风景画" --quality "4K" --size "4096x4096"

# 直接输出 Markdown 图片链接
python3 scripts/generate_image.py "一只可爱的猫" --markdown-output

# 生成视频 - 默认 16:9 / 720p / 10s
python3 scripts/generate_image.py "小骏马祝福大家新年快乐" --model SEEDANCE_1_5_PRO

# 生成视频 - 指定比例和分辨率
python3 scripts/generate_image.py "海边日落风景" --model SEEDANCE_1_5_PRO --ratio "9:16" --resolution "1080p"

# 生成视频 - 指定时长
python3 scripts/generate_image.py "一只猫在玩耍" --model SEEDANCE_1_5_PRO --duration 5

# SORA2 - 纯文生视频
python3 scripts/generate_image.py "一匹小马在奔跑" --model SORA2

# SORA2 - 首帧图生视频（FIRST&LAST 模式）
python3 scripts/generate_image.py "一匹小马在奔跑" --model SORA2 --first-image-url "https://example.com/horse.jpg"

# SORA2 - 指定比例、分辨率、时长
python3 scripts/generate_image.py "一匹小马在奔跑" --model SORA2 --ratio "16:9" --resolution "720p" --duration 4

# SORA2 - 不生成音频
python3 scripts/generate_image.py "风景" --model SORA2 --no-audio
```

## 程序化调用

```python
from scripts.generate_image import generate_image, generate_video

# 图片 - 默认 SEEDREAM5_0
result = generate_image(prompt="一只可爱的猫咪")

# 图片 - NANO_BANANA_2
result = generate_image(prompt="生成一只狗", model="NANO_BANANA_2")

# 图片 - 下载到本地
result = generate_image(prompt="风景画", model="SEEDREAM5_0", download=True, output_dir="./images")

if result and result["status"] == "SUCCESS":
    print(f"图片链接: {result['url']}")
    print(f"本地路径: {result.get('local_path')}")

# 视频 - 默认参数
result = generate_video(prompt="小骏马祝福大家新年快乐")

# 视频 - 指定比例、分辨率、时长
result = generate_video(
    prompt="海边日落风景",
    model="SEEDANCE_1_5_PRO",
    ratio="9:16",
    resolution="1080p",
    duration=5
)

# SORA2 - 纯文生视频
result = generate_video(
    prompt="一匹小马在奔跑",
    model="SORA2"
)

# SORA2 - 首尾帧控制
result = generate_video(
    prompt="一匹小马在奔跑",
    model="SORA2",
    first_image_url="https://example.com/horse.jpg",
    generate_audio=True,
    scale_factor=0.5,
    ratio="16:9",
    resolution="720p",
    duration=4
)

if result and result["status"] == "SUCCESS":
    print(f"视频链接: {result['url']}")
```

## 返回字段

| 字段 | 说明 |
|------|------|
| `status` | SUCCESS / FAILED / TIMEOUT |
| `url` | 图片URL |
| `message` | 状态描述 |
| `local_path` | 本地保存路径（需 --download） |
| `data_uri` | Base64 Data URI（需 --download） |
| `image_data` | 原始图片字节（需 --download） |

## 环境配置

### 必需配置 - API Key

**重要：使用前必须设置你自己的 API Key！**

#### 获取 API Key

1. 访问 [https://staging.kocgo.vip/index](https://staging.kocgo.vip/index)
2. 注册并登录账号
3. 在控制台创建你的 API Key
4. 复制生成的 API Key（格式：`sk-xxxxxx...`）

#### 方式 1：使用 .env 文件（推荐）

1. 复制 `.env.example` 为 `.env`：
   ```bash
   cp .env.example .env
   ```

2. 编辑 `.env` 文件，填入你的 API Key：
   ```bash
   AI_ARTIST_TOKEN=sk-your_api_key_here
   ```

3. 在运行脚本前加载环境变量：
   ```bash
   # Linux/macOS/Git Bash
   source .env

   # 或使用 export
   export $(cat .env | xargs)
   ```

#### 方式 2：直接设置环境变量

##### Linux / macOS / Git Bash (Windows)

```bash
export AI_ARTIST_TOKEN="sk-your_api_key_here"
```

为了永久生效，将上述命令添加到 `~/.bashrc` 或 `~/.zshrc` 文件中。

##### Windows PowerShell

```powershell
$env:AI_ARTIST_TOKEN="sk-your_api_key_here"
```

永久设置（系统级）：
```powershell
[System.Environment]::SetEnvironmentVariable('AI_ARTIST_TOKEN', 'sk-your_api_key_here', 'User')
```

##### Windows CMD

```cmd
set AI_ARTIST_TOKEN=sk-your_api_key_here
```

#### 验证配置

运行以下命令验证 API Key 是否设置成功：

```bash
# Linux/macOS/Git Bash
echo $AI_ARTIST_TOKEN

# Windows PowerShell
echo $env:AI_ARTIST_TOKEN

# Windows CMD
echo %AI_ARTIST_TOKEN%
```

如果输出为空或显示默认值，说明环境变量未正确设置。

#### 测试配置（推荐）

运行配置测试脚本，验证 API Key 是否正确设置：

```bash
python3 scripts/test_config.py
```

该脚本会检查：
- API Key 是否已设置
- 是否使用了默认 Key（需要替换为你自己的）
- 配置是否可以正常使用

### 可选配置 - 飞书通知

```bash
export FEISHU_WEBHOOK_URL="https://open.feishu.cn/open-apis/bot/v2/hook/xxx"
```

## 相关文件

- `scripts/generate_image.py` - 主脚本
- `references/api.md` - API 详细文档
