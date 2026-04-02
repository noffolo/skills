# Speech Synthesizer | 语音合成器 🔊

> 文字转语音，支持微软神经网络 TTS（免费离线）和 OpenAI 兼容 API

![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Windows%20%7C%20macOS-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)

## 功能特性

- 🔊 **edge-tts** — 微软神经网络 TTS，免费离线，高音质
- 🌐 **API 模式** — 支持 OpenAI 兼容 API
- 🇨🇳 **中文支持** — 晓晓、云希、云扬等多种中文声音
- ⚡ **离线可用** — edge-tts 无需 API Key

## 快速开始

### 1. 安装依赖

```bash
cd ~/.openclaw/workspace/skills/audio-tts
pip install -r requirements.txt
```

### 2. 运行

```bash
# edge-tts（默认，免费）
python3 scripts/tts_simple.py "你好，这是语音合成测试"

# 英文声音
python3 scripts/tts_simple.py "Hello world" --voice en-US-Jenny

# API 模式
python3 scripts/tts_simple.py "Hello" --engine api \
    --api-url https://api.openai.com/v1 \
    --api-key your-key
```

## 输出目录

```
~/.openclaw/workspace/projects/tts/output/
```

## 文档

详见 [SKILL.md](SKILL.md)
