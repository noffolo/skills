---
name: freeads-snap-ad
description: "🎬 AI 高端广告视频生成器 - 将产品照片转化为 8 秒专业广告视频（含 BGM、Slogan、音效、丰富运镜）。使用 Atlas Cloud API 调用 Veo 3.1 生成视频。触发词：随手拍广告、生成广告视频、产品广告。核心输出：视频文件 URL。"
version: 3.0.0
author: lipeng0820
metadata:
  category: media-generation
  platforms:
    - codeflicker
    - openclaw
    - claude-code
  required-env:
    - ATLASCLOUD_API_KEY
  estimated-cost: "$0.80-1.60 per video"
---

# FreeAds 随手拍广告 - AI 高端广告视频生成器 🎬

> **这是一个视频生成器，不是文案/方案生成器！**
> 
> **最终产出：8 秒 MP4 广告视频（含 BGM、Slogan、音效、丰富运镜）**
> 
> 📦 快速安装：`clawhub install lipeng0820/freeads-snap-ad`

---

## 🚨🚨🚨 核心定位（AI 助手必读）🚨🚨🚨

### 这个 Skill 是什么？

**✅ 是：AI 高端商业广告视频生成器**
- 输入：产品照片（随手拍）
- 输出：**8 秒 MP4 高端广告视频**
- 特点：**必须有 BGM、Slogan、音效、丰富运镜**
- 调用：Atlas Cloud Veo 3.1 API (`google/veo3.1/image-to-video`)

**❌ 不是：广告文案/方案生成器**
- 分镜脚本只是中间步骤，用于生成视频提示词
- 最终产出**必须是视频**，不是文案、方案、设计稿

### 视频质量要求（必须满足）：

| 要素 | 要求 |
|------|------|
| **BGM** | 必须有背景音乐，与产品调性匹配 |
| **Slogan** | 必须在视频中展示品牌/产品 Slogan |
| **音效** | 必须有环境音效增强沉浸感 |
| **运镜** | 必须有丰富运镜（推轨、摇移、特写等） |
| **商业感** | 必须有高端商业广告的质感 |

### 禁止输出以下内容作为最终结果：
- ❌ "📸 功能简介... Slogan & 广告文案..."
- ❌ 广告方案文档
- ❌ 设计建议
- ❌ 简单平移的产品展示
- ❌ 没有 BGM 的静默视频

---

## 🔧 使用的模型（Atlas Cloud）

| 功能 | 模型 ID | 说明 |
|------|---------|------|
| **智能抠图** | `google/nano-banana-2/edit` | 提取产品主体，生成白底图 |
| **分镜脚本生成** | `zai-org/glm-5-turbo` | 分析产品，生成英文视频 prompt |
| **视频生成** | `google/veo3.1/image-to-video` | 生成 8 秒高端广告视频 |

**⚠️ 注意：Atlas Cloud 没有 Gemini 模型，使用 `zai-org/glm-5-turbo` 替代！**

---

## 🚨 执行规则（违反即失败）🚨

**禁止说以下任何借口：**
- ❌ "Atlas Cloud 没有视频生成模型" - **Veo 3.1 就是视频模型！**
- ❌ "API 计费系统不可用" - **直接调用 API**
- ❌ "模型不可用" - **用备选模型 `zai-org/glm-5-turbo`**

**必须执行的 API 调用：**
```python
# 1. 抠图 - 使用 Nano Banana 2
POST https://api.atlascloud.ai/api/v1/model/generateImage
{
    "model": "google/nano-banana-2/edit",
    "prompt": "Remove background, keep product only, white background",
    "image_url": "用户上传的图片URL"
}

# 2. 生成分镜脚本 - 使用 GLM-5-Turbo（不是 Gemini！）
POST https://api.atlascloud.ai/v1/chat/completions
{
    "model": "zai-org/glm-5-turbo",  # 注意：不是 gemini-3.1-pro！
    "messages": [...]
}

# 3. 视频生成 - 使用 Veo 3.1
POST https://api.atlascloud.ai/api/v1/model/generateVideo
{
    "model": "google/veo3.1/image-to-video",
    "prompt": "分镜脚本生成的英文 prompt",
    "image_url": "抠图后的白底图URL",
    "durationSeconds": 8,
    "withAudio": true  # 必须启用音频！
}
```

---

## 工作流程（简化版，不收集 LOGO）

**输入** → **处理** → **输出**

```
用户产品图片 → 上传 → 抠图提取主体（白底图）→ 分析产品生成分镜脚本 → Veo 3.1 生成视频 → 视频 URL
```

| 步骤 | 操作 | API/模型 | 输出 |
|------|------|---------|------|
| 1 | 上传图片 | `uploadMedia` | 图片 URL |
| 2 | **抠图**（必须） | `google/nano-banana-2/edit` | 白底产品图 URL |
| 3 | 产品分析+分镜脚本 | `zai-org/glm-5-turbo` | 英文视频 prompt |
| 4 | 费用预估 | - | 显示费用，用户确认 |
| 5 | **生成视频**（核心） | `google/veo3.1/image-to-video` | **视频 URL** ← 最终产出 |

**⚠️ 重要变更：**
- **不收集 LOGO**：避免 LOGO 图片干扰产品识别
- **只用产品图**：仅使用用户上传的产品随手拍进行处理
- **必须先抠图**：提取产品主体，生成干净的白底图后再生成视频

---

## API Key 配置

在首次使用前，配置 Atlas Cloud API Key：

```bash
# 在 ~/.zshrc 或 ~/.bashrc 中添加
export ATLASCLOUD_API_KEY="your-api-key"
```

如果环境变量未设置，询问用户：

> 请提供您的 Atlas Cloud API Key（可在 https://console.atlascloud.ai/ 获取）。

---

## 完整工作流程

### Step 1: 获取用户图片

请用户提供产品图片（随手拍），支持：
- 直接粘贴图片
- 提供本地文件路径
- 提供图片 URL

**⚠️ 不要询问 LOGO！只使用用户上传的产品图片！**

---

### Step 2: 上传图片到 Atlas Cloud

```python
import requests
import os

api_key = os.environ.get("ATLASCLOUD_API_KEY")

# 上传本地图片
upload_response = requests.post(
    "https://api.atlascloud.ai/api/v1/model/uploadMedia",
    headers={"Authorization": f"Bearer {api_key}"},
    files={"file": open("product_photo.jpg", "rb")}
)
image_url = upload_response.json().get("url")
print(f"图片已上传: {image_url}")
```

---

### Step 3: 使用 Nano Banana 2 抠图（必须执行）

**⚠️ 此步骤必须执行，不能跳过！**

```python
import requests
import time

def remove_background(image_url: str, api_key: str) -> str:
    """
    使用 Nano Banana 2 抠图，提取产品主体
    """
    prompt = """Remove the background COMPLETELY and extract the product only.

REQUIREMENTS:
- Keep ONLY the main product, remove ALL background elements
- Remove any table, surface, other objects, hands, shadows from background
- Maintain EXACT product shape, proportions, colors, textures
- Keep all product details crisp and sharp
- Preserve any text, labels, logos ON the product itself

OUTPUT:
- Pure white (#FFFFFF) background
- Product centered with professional studio lighting
- Clean, precise edges
- Subtle soft shadow for depth

The product must look like a professional e-commerce photo."""

    response = requests.post(
        "https://api.atlascloud.ai/api/v1/model/generateImage",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": "google/nano-banana-2/edit",
            "prompt": prompt,
            "image_url": image_url,
            "output_format": "png"
        }
    )
    
    prediction_id = response.json().get("predictionId")
    
    # 轮询获取结果
    while True:
        result = requests.get(
            f"https://api.atlascloud.ai/api/v1/model/getResult?predictionId={prediction_id}",
            headers={"Authorization": f"Bearer {api_key}"}
        ).json()
        
        if result.get("status") == "completed":
            return result.get("output")
        elif result.get("status") == "failed":
            raise Exception(f"抠图失败: {result.get('error')}")
        
        time.sleep(2)

# 使用示例
white_bg_image_url = remove_background(image_url, api_key)
print(f"白底图生成完成: {white_bg_image_url}")
```

---

### Step 4: 使用 GLM-5-Turbo 分析产品并生成分镜脚本

**⚠️ 使用 `zai-org/glm-5-turbo`，不是 `gemini-3.1-pro`！**

```python
from openai import OpenAI

client = OpenAI(
    api_key=api_key,
    base_url="https://api.atlascloud.ai/v1"
)

# 生成分镜脚本（不是简单文案！）
response = client.chat.completions.create(
    model="zai-org/glm-5-turbo",  # 注意：不是 gemini！
    messages=[
        {
            "role": "system",
            "content": """You are a world-class commercial video director. Analyze the product image and create a CINEMATIC video prompt for Veo 3.1.

Your prompt MUST create a HIGH-END COMMERCIAL with:

1. **DYNAMIC CAMERA MOVEMENTS** (CRITICAL):
   - Opening: Dramatic reveal (dolly in from black, or light sweep)
   - Middle: Smooth orbital rotation around product
   - Close-up: Detailed texture/feature shots
   - Ending: Pull back to hero shot
   
2. **PROFESSIONAL LIGHTING**:
   - Dramatic studio lighting with key, fill, and rim lights
   - Light rays, lens flares, or sparkle effects
   - Reflections on glossy surfaces
   
3. **AUDIO ELEMENTS** (MUST SPECIFY):
   - Epic/emotional background music matching product type
   - Subtle sound effects (whoosh, impact, shimmer)
   - Professional audio atmosphere
   
4. **SLOGAN/TEXT OVERLAY**:
   - Suggest a short, powerful slogan to appear in video
   - Specify when text should appear and fade
   
5. **VISUAL EFFECTS**:
   - Particle effects, light leaks, or subtle motion graphics
   - Premium color grading (cinematic, warm/cool tone)
   - Depth of field effects

Output format (in English):
SLOGAN: [2-5 word powerful slogan]
PROMPT: [Detailed video prompt for Veo 3.1, 150-250 words, describing camera movements, lighting, effects, and audio in detail]"""
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {"url": white_bg_image_url}
                },
                {
                    "type": "text",
                    "text": "Analyze this product and create a cinematic video prompt. The video MUST feel like a high-end TV commercial with BGM, sound effects, and dynamic camera movements."
                }
            ]
        }
    ],
    max_tokens=1024
)

video_script = response.choices[0].message.content
print(video_script)
```

---

### Step 5: 费用预估

**费用参考：**

| 步骤 | 模型 | 费用估算 |
|------|------|----------|
| 智能抠图 | Nano Banana 2 | $0.02 - $0.05 |
| 分镜脚本 | GLM-5-Turbo | $0.01 - $0.02 |
| 视频生成 (8秒含音频) | Veo 3.1 I2V | $0.72 - $1.60 |
| **总计** | - | **$0.75 - $1.67** |

向用户展示费用预估后，等待用户确认再继续。

---

### Step 6: 使用 Veo 3.1 生成高端广告视频（核心步骤）

**⚠️ 这是最关键的步骤！必须生成有 BGM、音效、丰富运镜的高端广告！**

```python
def generate_commercial_video(
    image_url: str,
    video_prompt: str,
    api_key: str,
    duration: int = 8
) -> str:
    """
    使用 Veo 3.1 生成高端商业广告视频
    """
    # 增强 prompt，确保视频有商业广告质感
    enhanced_prompt = f"""{video_prompt}

MANDATORY COMMERCIAL QUALITY REQUIREMENTS:

CAMERA WORK:
- Cinematic camera movements: dolly, crane, orbital, push-in
- Smooth transitions between shots
- Professional depth of field with bokeh
- Multiple angle changes for dynamic feel

AUDIO (CRITICAL - Must have audio!):
- Epic/emotional background music matching the product mood
- Subtle sound effects: whoosh on camera moves, impact on reveals
- Professional audio mixing and atmosphere
- Music should build and peak at product reveal

VISUAL QUALITY:
- High-end commercial color grading
- Dramatic lighting with rim lights and lens flares  
- Premium visual effects: light rays, particles, reflections
- Text/slogan overlay with elegant animation

PRODUCT PRESENTATION:
- Hero product must be the star
- Maintain exact product appearance throughout
- Professional studio quality
- Luxurious, aspirational feel

This must look like a Super Bowl commercial, not a simple product video."""

    response = requests.post(
        "https://api.atlascloud.ai/api/v1/model/generateVideo",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": "google/veo3.1/image-to-video",
            "prompt": enhanced_prompt,
            "image_url": image_url,
            "durationSeconds": duration,
            "resolution": "1080p",
            "aspectRatio": "16:9",
            "withAudio": True  # 必须启用音频！
        }
    )
    
    prediction_id = response.json().get("predictionId")
    print(f"视频生成中，任务ID: {prediction_id}")
    print("预计需要 2-3 分钟，请耐心等待...")
    
    # 轮询获取结果
    while True:
        result = requests.get(
            f"https://api.atlascloud.ai/api/v1/model/getResult?predictionId={prediction_id}",
            headers={"Authorization": f"Bearer {api_key}"}
        ).json()
        
        if result.get("status") == "completed":
            return result.get("output")
        elif result.get("status") == "failed":
            raise Exception(f"视频生成失败: {result.get('error')}")
        
        print("视频生成中，请稍候...")
        time.sleep(10)

# 使用示例
video_url = generate_commercial_video(
    image_url=white_bg_image_url,
    video_prompt=video_script,  # 从 Step 4 获得的分镜脚本
    api_key=api_key,
    duration=8
)
print(f"\n✅ 广告视频生成完成！\n🎬 视频链接: {video_url}")
```

---

## 正确的最终输出格式

```
✅ 广告视频生成完成！

🎬 视频链接: https://atlas-media.oss-xxx.aliyuncs.com/videos/xxxxx.mp4

📋 生成摘要
| 步骤 | 状态 | 结果 |
|------|------|------|
| 1. 上传图片 | ✅ | 完成 |
| 2. Nano Banana 2 抠图 | ✅ | 白底图生成成功 |
| 3. 分镜脚本生成 | ✅ | GLM-5-Turbo 完成 |
| 4. Veo 3.1 视频生成 | ✅ | 8秒视频完成 |

📝 Slogan: [生成的 Slogan]

💰 实际费用
- 智能抠图: ~$0.03
- 分镜脚本: ~$0.02
- 视频生成 (8秒): ~$1.20
- **总计: ~$1.25**

视频已生成，可直接下载使用！🎉
```

---

## 注意事项

1. **不收集 LOGO** - 避免 LOGO 图片干扰产品识别，只使用用户上传的产品图
2. **必须先抠图** - 提取产品主体，去除背景杂物
3. **使用 GLM-5-Turbo** - Atlas Cloud 没有 Gemini，用 `zai-org/glm-5-turbo` 替代
4. **视频必须有音频** - `withAudio: true` 确保有 BGM 和音效
5. **商业质感** - Prompt 中明确要求高端商业广告效果

---

## 故障排查

### 常见问题

1. **"Gemini 模型不可用"**
   - 原因：Atlas Cloud 没有 Gemini 模型
   - 解决：使用 `zai-org/glm-5-turbo` 替代

2. **视频没有 BGM/音效**
   - 原因：未启用 `withAudio`
   - 解决：确保请求中 `"withAudio": true`

3. **视频只是简单产品旋转，没有商业感**
   - 原因：Prompt 不够详细
   - 解决：使用增强的 prompt，明确要求运镜、灯光、特效

4. **产品识别错误（如圣诞帽识别为跑鞋）**
   - 原因：LOGO 图片干扰了产品识别
   - 解决：不收集 LOGO，只用产品图

5. **API Key 无效**
   - 检查环境变量是否正确设置
   - 确认 API Key 未过期

---

## 支持文件

- **`references/atlas-cloud-api.md`** - Atlas Cloud API 详细文档

---

## 版本历史

- **v3.0.0** - 重大更新
  - 移除 LOGO 收集功能，避免干扰产品识别
  - 模型从 `gemini-3.1-pro` 改为 `zai-org/glm-5-turbo`
  - 增强视频 prompt，要求 BGM、Slogan、音效、丰富运镜
  - 简化工作流程
  - 作者更正为 `lipeng0820`
