# Audio TTS Skill 部署指南

---

## 系统要求

### 软件
- **Python**: 3.8+
- **网络**: 首次运行需要网络以下载 edge-tts 数据（之后可离线）

### 操作系统
- Linux / Windows / macOS 皆可

---

## 快速部署

### Linux / macOS

```bash
cd ~/.openclaw/workspace/skills/audio-tts
pip install -r requirements.txt
python3 scripts/tts_simple.py "测试语音"
```

### Windows

```powershell
cd $env:USERPROFILE\.openclaw\workspace\skills\audio-tts
pip install -r requirements.txt
python scripts/tts_simple.py "测试语音"
```

---

## 依赖说明

### edge-tts

微软神经网络 TTS，特点：
- 免费使用
- 无需 API Key
- 音质好，支持中文
- 需要网络下载初期数据

### openai (API 模式)

当 edge-tts 不满足需求时，可使用 OpenAI 兼容 API：

```bash
export TTS_API_URL=https://api.openai.com/v1
export TTS_API_KEY=sk-your-key
python3 scripts/tts_simple.py "Hello" --engine api
```

---

## 故障排查

### edge-tts 无法连接

检查网络连接：
```bash
curl -I https://www.bing.com
```

如有代理干扰：
```bash
unset all_proxy ALL_PROXY http_proxy https_proxy
```

### 无声音输出

- 检查输出文件是否生成
- 确认音频播放器可用：`mpg123 output.mp3` 或浏览器打开

### 中文声音不自然

推荐使用 `zh-CN-Xiaoxiao`（晓晓），是中文效果最好的声音之一。
