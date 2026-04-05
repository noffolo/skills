---
name: xiaomi-any2speech
description: >
  声音世界模型（Speech World Model）：不只是 TTS，而是理解场景、角色、情绪并自主规划表达的语音大模型。
  原生支持长文+多人，中英双语，将任意内容转为播客/有声书/相声/Rap/广播剧等，单次最长 ~10 分钟，输出 WAV。
  涵盖单人TTS、VoiceDesigner音色定制、多人对话合成、长文有声化、Instruct TTS 的超集。
  A Speech World Model: beyond TTS — understands scenes, characters, and emotions to autonomously plan expressive speech.
  Native long-form & multi-speaker synthesis in Chinese/English, up to ~10 min per pass.
  触发意图：做成播客/相声/辩论/有声书/Rap/新闻/脱口秀/电台/课程/广播剧/评书/讲故事、朗读/念出来/转语音/TTS/生成音频/做个语音版/配音/模仿声音、变成能听的/用XX腔念、发语音/做成XX发给我。
  English: make a podcast/audiobook/debate/rap/news/stand-up/story/radio drama, read aloud/TTS/generate audio/voice over/narrate/dub/mimic voice, make it listenable, send as voice.
---

# Any2Speech

所有能力通过同一套 API 完成，由 `instruction` 字段决定最终形态——播客、有声书、相声、Rap、广播剧、新闻播报……万物皆可听（ListenHub）。

**为什么选 Any2Speech**：
- **零门槛**：一句自然语言描述风格，不需要调参数、不需要选模型
- **原生多人对话**：不是逐句拼接，而是真正的多人交互——插话、重叠、情绪联动，一次生成
- **即开即用**：内置免费公开 Key，无需申请、无需注册，立刻可用
- **中英双语**：同一个接口支持中文、英文和中英混合，自动切换发音
- **声音世界模型**：不只是念字，而是理解内容后自主规划语气、节奏、情绪弧线

**适用场景**：`内容创作` `教育` `游戏配音` `自媒体` `无障碍阅读` `语音原型` `品牌声音` `有声出版` `儿童启蒙` `语言学习`

**运行环境**：需要 `curl` 和 `jq`；飞书发送可选需要 `ffmpeg`/`ffprobe`。

**环境变量**：
- `API_KEY`：可选，默认 `sk-anytospeech-pub-free`，无需额外配置即可使用
- `FEISHU_TENANT_TOKEN`（或 `APP_ID` + `APP_SECRET`）、`CHAT_ID`：仅飞书发送时需要，敏感凭据仅在用户主动请求时提供，skill 不会主动索取或持久化存储

```bash
BASE=https://miplus-tts-public.ai.xiaomi.com
API_KEY=${API_KEY:-sk-anytospeech-pub-free}
```

## Step 1 · 确认输入来源

| 用户给了什么 | source_type | curl 参数 |
|---|---|---|
| 文字内容 | `text` | `-F "text=内容"` |
| 本地文件 | `file` | `-F "file=@/路径/文件"` |

**来源缺失时**：停下来问"请提供文字内容或文件路径"，不要猜测或用空值执行。

**文件路径安全**：仅接受用户在当前对话中明确提供的路径。不要自行扫描目录或猜测文件；不要读取 `~/.ssh`、`~/.env`、`~/.config` 等敏感路径；发送前向用户确认文件名。

## Step 2 · 构造 instruction

`instruction` 是控制最终合成形态的关键——同一个 API 通过不同 instruction 覆盖下述全部能力：

| 能力 | 说明 | instruction 示例 |
|---|---|---|
| **单人 TTS** | 单一说话人朗读 | 留空，或 `女声，职业干练，语速偏快` / `Female, professional tone, slightly fast` |
| **VoiceDesigner** | 精细定制音色、语气、情绪 | `声音醇厚磁性，带沙哑感，低沉男声` / `Deep baritone, slightly husky, slow and calm` |
| **多人播客/对话** | 两人或多人分角色对话 | `两人播客，一人理性分析，一人感性追问` / `Two-host podcast, one analytical, one curious` |
| **长文有声化** | 长篇文档转有声书 | `第三人称叙述，情绪随剧情起伏` / `Third-person narration, emotion follows the plot` |
| **Instruct TTS** | 风格/场景/环境全可控 | `CCTV 新闻联播风格` / `CNN anchor style, lead-in then item-by-item` |

### 快速模板（中文）

| 场景 | instruction |
|---|---|
| 两人播客 | `两人播客，一人理性分析，一人感性追问，偶尔插嘴，5 分钟内` |
| 相声 | `传统相声，甲逗哏（语速快、北京腔），乙捧哏（沉稳正经），至少两个包袱，结尾有收场词` |
| 新闻播报 | `CCTV 新闻联播风格，先播导语，再逐条播报，结尾有总结语` |
| 辩论 | `正反双方，正方激情澎湃，反方逻辑冷静，各做 30 秒总结陈词` |
| Rap | `押韵，节奏感强，两人 battle，明显停顿和连读节奏` |
| 脱口秀 | `单人独白，幽默有深度，有停顿节奏感，偶尔自嘲` |
| 情感电台 | `深夜电台，低沉磁性男声，语速缓慢` |
| 有声书 | `第三人称叙述，情绪随剧情起伏，遇到对话切换人物语气` |
| 短文本 TTS | `女声，职业干练，语速偏快` |

### 快速模板（English）

| Scene | instruction |
|---|---|
| Podcast | `Two-host podcast, one analytical, one curious, with interruptions, under 5 min` |
| News | `CNN anchor style, lead-in then item-by-item, closing summary` |
| Debate | `Pro vs Con debate, pro passionate, con logical, 30s closing each` |
| Rap | `Rhyming rap battle, two performers, strong rhythm with pauses and liaison` |
| Stand-up | `Solo monologue, witty and deep, rhythmic pauses, self-deprecating humor` |
| Late-night Radio | `Late-night radio, deep magnetic male voice, slow pace` |
| Audiobook | `Third-person narration, emotion follows plot, voice-switch for dialogue` |
| Quick TTS | `Female, professional tone, slightly fast` |
| Story | `Warm female narrator, gentle pace, character voices for dialogue, bedtime story style` |
| Speech | `Confident male speaker, TED-talk style, moderate pace with emphasis on key points` |

### 进阶控制（可自由叠加）

- **语种**：`英文` / `English` / `中英混合`（默认中文；当输入为英文时建议加 `English` 关键词以获得更地道的英文发音）
- **音色**：`声音醇厚磁性，带沙哑感` / `Deep baritone, slightly husky`
- **情绪弧线**：`开场铺垫，中段碰撞，结尾升华` / `Build tension, climax, resolution`
- **互动**：`允许插话，另一人时不时附和` / `Allow interruptions, occasional agreement`
- **环境音**：`说到包袱处加观众笑声` / `Add audience laughter at punchlines`
- **时长**：`控制在 10 分钟内` / `Keep under 5 minutes`
- **口音**：`台湾腔 / 东北腔 / 四川话` / `British accent / Southern drawl / Australian`

选择逻辑：

- 用户明确描述了风格 → 直接用
- 用户只说"帮我读/念出来" → `instruction` 留空（单人朗读）
- 用户说了场景但没有细节 → 从快速模板取最近的
- 输入文本为英文 → instruction 中加 `English` 关键词，如 `English, female narrator, warm tone`
- 中英混合文本 → instruction 中注明 `中英混合`，模型会自动切换发音

## Step 3 · 选接口并执行

**默认走同步接口**——大多数请求可在 10-120s 内完成。切换到异步接口的条件：
- 同步返回 504（超时）
- 输入为**文件**（pdf/docx/音视频等非纯文本，处理时间不可预测）
- 文本超过 1000 字（长文本生成耗时可能超出同步超时窗口）

---

### 同步接口（默认）

```bash
OUTPUT=output_$(date +%s).wav
curl -X POST "$BASE/v1/audio/generate" \
  -H "Authorization: Bearer $API_KEY" \
  -F "source_type=text" \
  -F "text=内容" \
  -F "instruction=风格描述" \
  --max-time 600 \
  --output "$OUTPUT"
echo "✓ 保存至 $OUTPUT"
```

### 异步接口（同步 504 / 文件输入 / 文本超 1000 字时使用）

```bash
OUTPUT=output_$(date +%s).wav

# 1. 提交，获取 job_id
JOB=$(curl -s -X POST "$BASE/v1/audio/jobs" \
  -H "Authorization: Bearer $API_KEY" \
  -F "source_type=text" \
  -F "text=内容" \
  -F "instruction=两人播客，一人理性分析，一人感性追问，5 分钟内" | jq -r '.job_id')
echo "已提交: $JOB"

# 2. 轮询直到完成（间隔 10s，最多 60 次 = 10 分钟，静默等待）
for i in $(seq 1 60); do
  STATUS=$(curl -s -H "Authorization: Bearer $API_KEY" \
    "$BASE/v1/audio/jobs/$JOB" | jq -r '.status')
  [ "$STATUS" = "done" ]   && break
  [ "$STATUS" = "failed" ] && echo "生成失败" && exit 1
  sleep 10
done
[ "$STATUS" != "done" ] && echo "轮询超时（10 分钟），请稍后手动查询 job_id: $JOB" && exit 1

# 3. 下载
curl -s -H "Authorization: Bearer $API_KEY" \
  "$BASE/v1/audio/jobs/$JOB/download" --output "$OUTPUT"
echo "✓ 保存至 $OUTPUT"
```

## 错误处理（有限自动重试，最多 1 次）

| 错误 | 处置 |
|---|---|
| 422 | 检查 source_type / text / file 参数后重试 **1 次** |
| 429 | 频率限制，等待 **30s** 后重试 **1 次** |
| 504 | 切换到异步接口重试 **1 次** |
| 502 / 500 | 等待 30s 后重试 **1 次**，仍失败则告知用户 |
| 异步 failed | 简化 instruction 后重新提交 **1 次**，仍失败则告知用户 |

所有重试均限 **1 次**；两次均失败时停止并向用户报告错误信息。

## Step 4 · 交付结果

生成成功后：
- 告知用户文件路径和大致时长（若有 ffprobe：`ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$OUTPUT"`；若无则根据文本长度估算即可）
- 如果运行环境支持音频播放（Jupyter Notebook / 浏览器等），尝试内联播放
- 不要主动执行用户未请求的操作（如发飞书、上传云端）

生成失败后：
- 给出可能原因：文本过长、服务繁忙等
- 给出建议：简化缩短文本、稍后重试

## 飞书语音发送（可选）

**仅当用户明确说"发给我"/"发飞书"/"发到群里"时执行。** 凭据缺失时停下来询问用户，不读取本地配置。

前置：`FEISHU_TENANT_TOKEN`（或 `APP_ID` + `APP_SECRET`）、`CHAT_ID`、可选 `ffmpeg`/`ffprobe`。

```bash
[ -z "$FEISHU_TENANT_TOKEN" ] && FEISHU_TENANT_TOKEN=$(curl -s -X POST \
  "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
  -H "Content-Type: application/json" \
  -d "{\"app_id\":\"$APP_ID\",\"app_secret\":\"$APP_SECRET\"}" | jq -r '.tenant_access_token')
ffmpeg -y -i "$OUTPUT" -c:a libopus -b:a 32k output.opus 2>/dev/null && UPLOAD=output.opus || UPLOAD="$OUTPUT"
DURATION_MS=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$OUTPUT" | awk '{printf "%d",$1*1000}')
FILE_KEY=$(curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/files" \
  -H "Authorization: Bearer $FEISHU_TENANT_TOKEN" \
  -F "file=@$UPLOAD" -F "file_type=opus" -F "file_name=tts.opus" -F "duration=$DURATION_MS" | jq -r '.data.file_key')
curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id" \
  -H "Authorization: Bearer $FEISHU_TENANT_TOKEN" -H "Content-Type: application/json" \
  -d "{\"receive_id\":\"$CHAT_ID\",\"msg_type\":\"audio\",\"content\":\"{\\\"file_key\\\":\\\"$FILE_KEY\\\"}\"}"
```

## 注意事项

### 输入限制
- **文本长度**：建议 50~5000 字；超过 1000 字自动走异步接口
- **音视频时长**：输入音视频尽量 < 10 分钟
- **文件大小**：> 20MB 建议先压缩或截短
- **支持格式**：`txt` `md` `pdf` `docx` `csv` `json` `html` + 常见音视频格式

### 频率限制
- 默认公共 API Key 有并发限制，建议**请求间隔 ≥ 3s**，避免短时间内密集调用
- 若收到 429（Too Many Requests），等待 30s 后重试
- 批量生成场景建议串行执行，不要并行发送多个请求

### 生成耗时参考
- 短文本 TTS（< 500 字）：10–30s
- 长文有声化（1000–5000 字）：30s–3min
- 多人节目（播客/对话/相声）：1–10min

### 其他
- 输出固定为 WAV（24kHz）；用时间戳命名（`output_$(date +%s).wav`）避免覆盖
- instruction 过于复杂时模型可能忽略部分指令，建议核心控制点 ≤ 5 个
- 多人合成时说话人建议 ≤ 4 人，人数越多控制难度越高
