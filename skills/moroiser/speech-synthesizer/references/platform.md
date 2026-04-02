# Audio TTS Skill - 平台笔记

## 测试环境

- OS: Linux (通用)
- TTS: edge-tts 7.x
- Python: 3.12

## edge-tts vs 其他 TTS

| 方案 | 成本 | 音质 | 中文支持 | 离线 | API Key |
|------|------|------|---------|------|---------|
| edge-tts | 免费 | 高 | 很好 | 部分 | 不需要 |
| OpenAI TTS | 按量计费 | 很高 | 一般 | 否 | 需要 |
| pyttsx3 | 免费 | 低 | 一般 | 是 | 不需要 |

## 平台兼容性

- **Linux**: ✅ 完全支持
- **Windows**: ✅ 完全支持
- **macOS**: ✅ 完全支持

## 已知限制

- edge-tts 依赖微软服务，需要能访问 `edge.microsoft.com`
- 部分声音在不同地区可能不可用
