---
name: douyin-download-transcribe
description: 抖音视频免费下载 + 本地转录（中英双语）。分享链接直接解析，Whisper 本地转文字，无需登录无需 API KEY。
metadata:
  {
    "openclaw":
      {
        "emoji": "🎬",
        "requires":
          {
            "bins": ["ffmpeg", "whisper"],
          },
        "install":
          [
            {
              "id": "clawhub-full-package",
              "kind": "clawhub-package",
              "label": "本 skill 已包含完整 MCP 服务器，无需额外安装",
            },
          ],
      },
  }
---

# 抖音视频免费下载 + 本地转录（中英双语）

## 功能特点

- ✅ **无需登录** — 分享链接直接解析
- ✅ **无需 API KEY** — 纯本地解析
- ✅ **无水印下载** — 自动替换域名去水印
- ✅ **Whisper 本地转文字** — 中英文支持，GPU 加速
- ✅ **支持 Mac/ Linux** — Python 3.11+

## 安装（一键）

```bash
# 进入技能目录，运行安装脚本
cd ~/.openclaw/workspace/skills/douyin-download-transcribe/douyin-mcp
chmod +x setup.sh
./setup.sh
```

安装脚本会自动：
1. 创建 Python 虚拟环境并安装依赖
2. 安装 ffmpeg（如需要）
3. 安装 OpenAI Whisper CLI
4. 配置 mcporter（添加 `douyin-analyzer` MCP 服务器）

安装完成后**重启 OpenClaw** 生效。

## 验证安装

```bash
mcporter list | grep douyin
# 应该看到：douyin-analyzer (3 tools)
```

## 使用方式

### 方式一：MCP 调用（推荐，自动解析 + 下载 + 转录）

```
mcporter call douyin-analyzer.analyze_douyin_video share_link="https://v.douyin.com/xxx"
```

### 方式二：逐个工具调用

```bash
# 获取视频信息
mcporter call douyin-analyzer.parse_douyin_video_info share_link="https://v.douyin.com/xxx"

# 获取无水印下载链接
mcporter call douyin-analyzer.get_douyin_download_link share_link="https://v.douyin.com/xxx"
```

### 方式三：给我发分享链接（最简单）

直接转发抖音视频链接给我，我说"分析一下"，自动完成：
1. 解析视频信息
2. 下载无水印视频
3. Whisper 转文字（中/英）
4. 内容总结

## 解析原理

三层降级策略，保证高可用：

| 层 | 方法 | 说明 |
|----|------|------|
| 第一层 | `iesdouyin.com` 官方 API | 直接请求 JSON，替换 `playwm`→`play` 去水印 |
| 第二层 | 第三方解析 API | `liuxingw.com/api/douyin/api.php` |
| 第三层 | Playwright 浏览器 | 模拟手机访问分享链接，提取 `<video>` 标签 |

**无水印原理：** `playwm` = 带水印，`play` = 无水印。CDN 上是同一文件，水印是播放端渲染的。

## Whisper 转录命令（GPU 加速）

```bash
# Mac M系列 GPU 加速（推荐）
whisper /path/to/audio.mp3 \
  --model small \
  --language Chinese \
  --device mps \
  --fp16 True \
  --output_format txt \
  --output_dir /tmp/

# CPU 备用
whisper /path/to/audio.mp3 --model small --language Chinese
```

## 文件说明

```
douyin-mcp/
├── server.py          # MCP 服务器核心代码
├── requirements.txt   # Python 依赖
├── setup.sh           # 一键安装脚本
└── .venv/            # Python 虚拟环境（安装后生成）
```

## 已知问题

- 部分极新视频或私有视频可能解析失败
- Whisper 转录效果取决于音频质量
- 建议使用 `small` 模型（速度/精度平衡）

## 排错指南

**症状：MCP 调用返回"无法获取视频信息"**

可能原因：
1. **Playwright 浏览器未安装** → `playwright install chromium`
2. **旧版 server.py 未包含修复** → 确认 server.py 中使用了 `page.evaluate('el => el.src')` 而非 `getAttribute('src')`
3. **asyncio 冲突** → 确认 server.py 导入了 `nest_asyncio` 并调用了 `nest_asyncio.apply()`
4. **share_url 未传递** → `get_video_info(video_id, share_url)` 需要传入第二个参数

快速验证：
```bash
# 直接测试 Python 模块
cd ~/.openclaw/workspace/skills/douyin-download-transcribe/douyin-mcp
source .venv/bin/activate
python3 -c "
from server import DouyinParser
info = DouyinParser.get_video_info('7623273111479893349', 'https://v.douyin.com/你的链接/')
print(info)
"
```

**症状：analyze 成功但 transcript 为 null**

检查 whisper 是否可用：
```bash
whisper --version   # 或
~/.openclaw/workspace/skills/douyin-download-transcribe/douyin-mcp/.venv/bin/whisper --version
```
