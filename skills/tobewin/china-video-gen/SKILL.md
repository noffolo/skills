---
name: china-video-gen
description: 国内可用的 AI 视频生成技能。Use when the user wants to create a video from text — generates script, images (via china-image-gen), voiceover (via china-tts), and merges everything into an MP4 using ffmpeg. No time limit (unlike 15s AI video models), full control over pacing and content. Automatically checks and installs dependencies (ffmpeg, china-image-gen, china-tts). Domestic-friendly, no VPN required.
version: 1.0.0
license: MIT-0
metadata: {"openclaw": {"emoji": "🎬", "requires": {"bins": ["curl", "python3"], "env": ["SILICONFLOW_API_KEY"]}, "primaryEnv": "SILICONFLOW_API_KEY"}}
---

# 国内 AI 视频生成 China Video Gen

将文字描述转化为完整视频：自动生成分镜脚本 → 图片序列 → 配音 → 合成 MP4。
无时长限制，完全可控，国内直连，无需翻墙。

依赖说明 → `references/dependencies.md`
ffmpeg 合成参数 → `references/ffmpeg.md`
分镜设计指南 → `references/storyboard.md`

## 触发时机

- "帮我做一个30秒的[产品]宣传视频"
- "生成一个介绍[主题]的短视频"
- "做一个[品牌]的广告视频"
- "把这段文字做成视频"
- "生成适合小红书/抖音发布的视频"

---

## Step 0：环境检查

**每次执行前必须先检查依赖，缺失则提示用户手动安装。**

### 检查 ffmpeg

```bash
if command -v ffmpeg &> /dev/null; then
  echo "✅ ffmpeg 已安装: $(ffmpeg -version 2>&1 | head -1)"
else
  echo "❌ ffmpeg 未安装，请手动安装："
  echo ""
  echo "  macOS:   brew install ffmpeg"
  echo "  Ubuntu:  sudo apt install ffmpeg"
  echo "  CentOS:  sudo yum install ffmpeg"
  echo "  Windows: 从 https://ffmpeg.org/download.html 下载并添加到 PATH"
  echo ""
  echo "安装完成后重新运行本技能。"
  exit 1
fi
```

### 检查 china-image-gen

```bash
# 检查 skill 是否已安装
SKILL_PATHS=(
  "$HOME/.openclaw/skills/china-image-gen"
  "$HOME/.config/openclaw/skills/china-image-gen"
  "./skills/china-image-gen"
)

IMAGEGEN_FOUND=false
for p in "${SKILL_PATHS[@]}"; do
  if [ -f "$p/SKILL.md" ]; then
    IMAGEGEN_FOUND=true
    break
  fi
done

if [ "$IMAGEGEN_FOUND" = false ]; then
  echo "⚠️  china-image-gen 未安装"
  echo "请在 OpenClaw 中执行：clawhub install china-image-gen"
  echo "或访问：https://clawhub.ai/ToBeWin/china-image-gen"
  echo ""
  echo "china-image-gen 是文生图技能，用于生成视频中的每一帧图片。"
  echo "安装完成后重新运行本技能。"
  exit 1
fi
echo "✅ china-image-gen 已安装"
```

### 检查 china-tts

```bash
SKILL_PATHS=(
  "$HOME/.openclaw/skills/china-tts"
  "$HOME/.config/openclaw/skills/china-tts"
  "./skills/china-tts"
)

TTS_FOUND=false
for p in "${SKILL_PATHS[@]}"; do
  if [ -f "$p/SKILL.md" ]; then
    TTS_FOUND=true
    break
  fi
done

if [ "$TTS_FOUND" = false ]; then
  echo "⚠️  china-tts 未安装"
  echo "请在 OpenClaw 中执行：clawhub install china-tts"
  echo "或访问：https://clawhub.ai/ToBeWin/china-tts"
  echo ""
  echo "china-tts 是文字转语音技能，用于生成视频的解说词音频。"
  echo "安装完成后重新运行本技能。"
  exit 1
fi
echo "✅ china-tts 已安装"
```

### 检查 API Key

```bash
if [ -z "$SILICONFLOW_API_KEY" ]; then
  echo "❌ 缺少 SILICONFLOW_API_KEY"
  echo ""
  echo "请配置硅基流动 API Key："
  echo "  1. 访问 cloud.siliconflow.cn 注册账号（国内直连）"
  echo "  2. 进入「API密钥」页面创建 Key"
  echo "  3. 执行：export SILICONFLOW_API_KEY='sk-xxxxxxxx'"
  echo "  4. 或写入 ~/.openclaw/.env 文件"
  echo ""
  echo "新用户有免费额度，支付宝/微信充值，最低10元"
  exit 1
fi
echo "✅ API Key 已配置"
```

---

## Step 1：理解用户需求

从用户描述中提取关键信息：

```
视频主题：产品宣传 / 知识科普 / 品牌故事 / 教程演示 / 其他
目标时长：15秒 / 30秒 / 60秒 / 更长（无限制）
画面风格：写实 / 插画 / 科技感 / 温暖 / 商务
音色选择：见 references/dependencies.md 音色列表
目标平台：小红书(1:1或3:4) / 抖音(9:16) / B站/YouTube(16:9) / 通用(16:9)
语言：中文 / 英文 / 中英混合
```

---

## Step 2：生成分镜脚本

根据用户需求，设计分镜脚本。每个分镜包含：

```
分镜N：
  时长：X 秒
  画面描述（英文 prompt，用于 FLUX 文生图）
  解说词（中文，用于 TTS 配音）
  运镜效果：静止 / Ken Burns 缩放 / 平移
  转场效果：淡入淡出 / 擦除 / 无
```

### 时长分配原则

```
总时长 30秒，建议分镜数量：5-8个
  开场：2-3秒（Logo/主题/吸引眼球）
  主体：每个分镜3-5秒
  结尾：2-3秒（CTA/联系方式/品牌）

总时长 60秒，建议分镜数量：10-15个
  节奏：前10秒最关键，必须抓住注意力

字数与时长对照（TTS朗读速度约4字/秒）：
  3秒 ≈ 12字
  5秒 ≈ 20字
  10秒 ≈ 40字
```

### 分镜脚本示例（30秒产品宣传）

```
分镜1（3秒）：
  画面：A sleek product on a clean white background, dramatic lighting, commercial photography style, 8k
  解说：每个人都需要的神器，今天终于来了
  运镜：Ken Burns 轻微放大
  转场：淡入

分镜2（5秒）：
  画面：Close-up of product features, modern minimalist style, professional product photography
  解说：[产品名]，突破传统，三大核心功能让你爱不释手
  运镜：静止
  转场：淡出淡入

分镜3（5秒）：
  画面：Happy person using the product in daily life, warm natural lighting, lifestyle photography
  解说：无论工作还是生活，它都是你最可靠的伙伴
  运镜：左移平移
  转场：淡出淡入

分镜4（5秒）：
  画面：Product detail shots showing quality craftsmanship, macro photography, bokeh background
  解说：精选材料，严苛工艺，每一处细节都是品质的体现
  运镜：静止
  转场：淡出淡入

分镜5（5秒）：
  画面：Multiple color options displayed elegantly, e-commerce style photography, white background
  解说：五种配色，总有一款适合你
  运镜：静止
  转场：淡出淡入

分镜6（4秒）：
  画面：Brand logo and product name on elegant dark background, luxury brand style
  解说：现在下单，享受限时优惠，扫码立即购买
  运镜：静止
  转场：淡入淡出
```

---

## Step 3：生成图片序列

调用 china-image-gen skill，为每个分镜生成对应图片。

### 分辨率与比例

```
小红书(1:1)：1024x1024
小红书(3:4)：768x1024
抖音/竖版(9:16)：720x1280
B站/横版(16:9)：1280x720
```

### 图片生成（对每个分镜执行）

```bash
# 创建工作目录
OUTPUT_DIR="${OPENCLAW_WORKSPACE:-$PWD}/video_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$OUTPUT_DIR/frames"
mkdir -p "$OUTPUT_DIR/audio"

# 生成分镜图片（以分镜1为例）
curl -s -X POST "https://api.siliconflow.cn/v1/images/generations" \
  -H "Authorization: Bearer $SILICONFLOW_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"model\": \"black-forest-labs/FLUX.1-schnell\",
    \"prompt\": \"{分镜N的英文画面描述}\",
    \"image_size\": \"{目标分辨率}\",
    \"num_inference_steps\": 20
  }" | python3 -c "
import sys, json, urllib.request
data = json.load(sys.stdin)
url = data['images'][0]['url']
urllib.request.urlretrieve(url, '$OUTPUT_DIR/frames/frame_01.jpg')
print('✅ 分镜1 图片已下载')
"
```

⚠️ 图片 URL 有效期1小时，必须立即下载。

### 批量生成脚本

```bash
# 所有分镜批量生成
PROMPTS=(
  "分镜1的英文prompt"
  "分镜2的英文prompt"
  "分镜3的英文prompt"
)
DURATIONS=(3 5 5 5 5 4)  # 每个分镜的秒数

for i in "${!PROMPTS[@]}"; do
  n=$(printf "%02d" $((i+1)))
  echo "正在生成第$((i+1))个分镜图片..."
  RESPONSE=$(curl -s -X POST "https://api.siliconflow.cn/v1/images/generations" \
    -H "Authorization: Bearer $SILICONFLOW_API_KEY" \
    -H "Content-Type: application/json" \
    -d "{
      \"model\": \"black-forest-labs/FLUX.1-schnell\",
      \"prompt\": \"${PROMPTS[$i]}\",
      \"image_size\": \"1280x720\",
      \"num_inference_steps\": 20
    }")
  URL=$(echo "$RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin)['images'][0]['url'])")
  curl -s -o "$OUTPUT_DIR/frames/frame_${n}.jpg" "$URL"
  echo "✅ 分镜$((i+1)) 完成"
  sleep 1  # 避免频率限制
done
```

---

## Step 4：生成配音音频

调用 china-tts skill，将所有解说词合并为一个音频文件。

```bash
# 合并所有解说词文本
VOICEOVER="分镜1解说词。分镜2解说词。分镜3解说词。分镜4解说词。分镜5解说词。分镜6解说词。"

# 调用硅基流动 TTS
curl --location 'https://api.siliconflow.cn/v1/audio/speech' \
  --header "Authorization: Bearer $SILICONFLOW_API_KEY" \
  --header 'Content-Type: application/json' \
  --data "{
    \"model\": \"FunAudioLLM/CosyVoice2-0.5B\",
    \"input\": \"$VOICEOVER\",
    \"voice\": \"FunAudioLLM/CosyVoice2-0.5B:claire\",
    \"response_format\": \"mp3\",
    \"speed\": 1.0
  }" \
  --output "$OUTPUT_DIR/audio/voiceover.mp3"

echo "✅ 配音生成完成：$OUTPUT_DIR/audio/voiceover.mp3"
```

---

## Step 5：合成视频

使用 ffmpeg 将图片序列和音频合成为 MP4 视频。

### 方案A：简单合成（静止图片+音频）

```bash
# 生成图片时长配置文件
DURATIONS=(3 5 5 5 5 4)
> "$OUTPUT_DIR/concat.txt"
for i in "${!DURATIONS[@]}"; do
  n=$(printf "%02d" $((i+1)))
  echo "file 'frames/frame_${n}.jpg'" >> "$OUTPUT_DIR/concat.txt"
  echo "duration ${DURATIONS[$i]}" >> "$OUTPUT_DIR/concat.txt"
done
# 最后一帧重复一次（ffmpeg concat 需要）
echo "file 'frames/frame_$(printf "%02d" ${#DURATIONS[@]}).jpg'" >> "$OUTPUT_DIR/concat.txt"

# 合成视频
cd "$OUTPUT_DIR"
ffmpeg -y \
  -f concat -safe 0 -i concat.txt \
  -i audio/voiceover.mp3 \
  -c:v libx264 -pix_fmt yuv420p \
  -c:a aac -shortest \
  -vf "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2" \
  output.mp4

echo "✅ 视频合成完成：$OUTPUT_DIR/output.mp4"
```

### 方案B：Ken Burns 效果（推荐，更有质感）

```bash
# 为每张图片添加缓慢缩放效果（模拟镜头推进）
cd "$OUTPUT_DIR"
DURATIONS=(3 5 5 5 5 4)

for i in "${!DURATIONS[@]}"; do
  n=$(printf "%02d" $((i+1)))
  d=${DURATIONS[$i]}
  fps=25
  frames=$((d * fps))

  ffmpeg -y -loop 1 -i "frames/frame_${n}.jpg" \
    -vf "scale=8000:-1,zoompan=z='min(zoom+0.0015,1.3)':d=${frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1280x720,fps=${fps}" \
    -t "$d" -c:v libx264 -pix_fmt yuv420p \
    "frames/clip_${n}.mp4"
  echo "✅ 分镜$((i+1)) Ken Burns 效果完成"
done

# 合并所有片段
> concat_clips.txt
for i in "${!DURATIONS[@]}"; do
  n=$(printf "%02d" $((i+1)))
  echo "file 'frames/clip_${n}.mp4'" >> concat_clips.txt
done

ffmpeg -y -f concat -safe 0 -i concat_clips.txt \
  -i audio/voiceover.mp3 \
  -c:v libx264 -c:a aac -shortest \
  output.mp4

echo "✅ 视频合成完成（Ken Burns效果）：$OUTPUT_DIR/output.mp4"
```

### 方案C：淡入淡出转场

```bash
# 两张图片之间添加0.5秒淡入淡出转场
# 使用 xfade filter
ffmpeg -y \
  -i frames/clip_01.mp4 \
  -i frames/clip_02.mp4 \
  -filter_complex \
    "[0][1]xfade=transition=fade:duration=0.5:offset=2.5[v01];
     [v01][2]xfade=transition=fade:duration=0.5:offset=7[vout]" \
  -map "[vout]" -i audio/voiceover.mp3 \
  -c:v libx264 -c:a aac -shortest \
  output.mp4
```

---

## Step 6：输出结果

```
🎬 视频生成完成
━━━━━━━━━━━━━━━━━━━━
视频文件：{工作区}/video_20260321_143052/output.mp4
总时长：约 XX 秒
分镜数：X 张
画面比例：16:9（1280x720）
配音音色：claire（温柔女声）

文件结构：
  video_20260321_143052/
  ├── output.mp4          ← 最终视频
  ├── frames/             ← 各分镜图片
  │   ├── frame_01.jpg
  │   └── ...
  ├── audio/
  │   └── voiceover.mp3  ← 配音文件
  └── concat.txt          ← 合成配置

播放：
  macOS:  open output.mp4
  Linux:  vlc output.mp4 / mpv output.mp4

估算成本：
  图片（FLUX schnell）：约 ¥{N×0.07}
  配音（CosyVoice2）：  约 ¥{字节数×单价}
  合计：约 ¥X
```

---

## 视频类型预设

### 产品宣传（30秒，16:9）

```
分镜数：6个
图片模型：FLUX.1-dev（高质量）
音色：alex（沉稳男声）或 claire（温柔女声）
效果：Ken Burns
转场：淡入淡出
```

### 知识科普（60秒，16:9）

```
分镜数：12个
图片模型：FLUX.1-schnell（快速）
音色：anna（沉稳女声）
效果：静止图片
转场：无
```

### 小红书竖版（30秒，3:4）

```
分辨率：768x1024
分镜数：6个
图片模型：Kolors（中文理解最好）
音色：diana（欢快女声）
效果：Ken Burns
```

### 抖音竖版（15秒，9:16）

```
分辨率：720x1280
分镜数：4个（节奏快）
图片模型：FLUX.1-schnell
音色：bella（激情女声）
效果：Ken Burns
```

---

## 注意事项

- 图片 URL 有效期仅1小时，生成后立即下载
- Ken Burns 效果处理较慢，每张图约需10-30秒
- 视频文件保存至 OpenClaw 工作区，长期保留
- 建议先用 FLUX.1-schnell 快速预览，满意后换 FLUX.1-dev 出高质量版
- 不要在短时间内大批量请求，避免触发 API 限速
