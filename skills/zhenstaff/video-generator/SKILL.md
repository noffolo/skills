---
name: video-generator
description: Automated text-to-video pipeline with multi-provider TTS/ASR support - OpenAI, Azure, Aliyun, Tencent | 多厂商 TTS/ASR 支持的自动化文本转视频系统
tags: [video-generation, remotion, openai, azure, aliyun, tencent, tts, whisper, automation, ai-video, short-video, text-to-video, multi-provider]
repository: https://github.com/ZhenRobotics/openclaw-video-generator
homepage: https://github.com/ZhenRobotics/openclaw-video-generator#readme
requires:
  api_keys:
    - name: OPENAI_API_KEY
      description: OpenAI API key for TTS and Whisper services (default provider - required unless using Azure/Aliyun/Tencent) | OpenAI API 密钥（默认提供商 - 除非使用 Azure/阿里云/腾讯云，否则必需）
      url: https://platform.openai.com/api-keys
      optional: false
    - name: ALIYUN_ACCESS_KEY_ID
      description: Aliyun AccessKey ID (optional, alternative provider) | 阿里云 AccessKey ID（可选，备选提供商）
      url: https://ram.console.aliyun.com/manage/ak
      optional: true
    - name: ALIYUN_ACCESS_KEY_SECRET
      description: Aliyun AccessKey Secret (required if using Aliyun) | 阿里云 AccessKey Secret（使用阿里云时必需）
      optional: true
    - name: ALIYUN_APP_KEY
      description: Aliyun NLS App Key (required if using Aliyun TTS/ASR) | 阿里云 NLS 应用密钥（使用阿里云时必需）
      url: https://ram.console.aliyun.com/manage/ak
      optional: true
    - name: AZURE_SPEECH_KEY
      description: Azure Speech Service key (optional, alternative provider) | Azure 语音服务密钥（可选，备选提供商）
      url: https://portal.azure.com/
      optional: true
    - name: AZURE_SPEECH_REGION
      description: Azure Speech Service region (required if using Azure) | Azure 语音服务区域（使用 Azure 时必需）
      optional: true
    - name: TENCENT_SECRET_ID
      description: Tencent Cloud Secret ID (optional, alternative provider) | 腾讯云 Secret ID（可选，备选提供商）
      url: https://console.cloud.tencent.com/cam/capi
      optional: true
    - name: TENCENT_SECRET_KEY
      description: Tencent Cloud Secret Key (required if using Tencent) | 腾讯云 Secret Key（使用腾讯云时必需）
      optional: true
    - name: TENCENT_APP_ID
      description: Tencent Cloud App ID (required if using Tencent) | 腾讯云应用 ID（使用腾讯云时必需）
      optional: true
  tools:
    - node>=18
    - npm
    - ffmpeg
    - python3
    - jq
  packages:
    - name: openclaw-video-generator
      source: npm
      version: ">=1.6.0"
      verified_repo: https://github.com/ZhenRobotics/openclaw-video-generator
      verified_commit: 75df997  # v1.5.1 - Compatibility & Documentation Improvements
install:
  commands:
    - npm install -g openclaw-video-generator@latest
  verify:
    - openclaw-video-generator --version
  notes: |
    Requires at least one TTS/ASR provider API key.
    Set OPENAI_API_KEY for default provider, or configure alternative providers.
---

# 🎬 Video Generator Skill

Automated text-to-video generation system that transforms text scripts into professional short videos with AI-powered voiceover, precise timing, and cyber-wireframe visuals.

## 🔒 Security & Trust

This skill is **safe and verified**:
- ✅ All code runs **locally** on your machine
- ✅ **No external servers** (except OpenAI API for TTS/Whisper)
- ✅ Source code is **open source** and auditable
- ✅ Uses official **npm package** (openclaw-video-generator)
- ✅ **Verified repository**: github.com/ZhenRobotics/openclaw-video-generator
- ✅ **No data collection** - all processing is local

**Required API Access**:
- OpenAI API key (for TTS and Whisper) - you maintain control

## 📦 Installation

### Prerequisites Check

Before installation, verify you have:
```bash
# Check Node.js (requires >= 18)
node --version

# Check npm
npm --version

# Check ffmpeg (required for video processing)
ffmpeg -version
```

If missing, install:
```bash
# Ubuntu/Debian
sudo apt install nodejs npm ffmpeg

# macOS
brew install node ffmpeg
```

### Installation Methods

Both methods are fully supported. Choose based on your needs:

| Feature | npm Global Install | Git Clone Local Install |
|---------|-------------------|------------------------|
| **Difficulty** | ⭐ Simple (one command) | ⭐⭐ Requires clone + npm install |
| **Updates** | `npm update -g` | `git pull && npm install` |
| **Use Case** | End users, quick start | Developers, code customization |
| **API Keys** | System environment variables | Project .env file (recommended) |
| **Disk Usage** | Small (single global copy) | Each project has its own copy |
| **Recommended For** | Terminal users, AI agents | Developers, teams |

**Method 1: npm Package (Quick Start)**

✅ **Pros**: Simple installation, global access, easy updates
⚠️ **Note**: Requires system-level environment variable configuration

```bash
# Install from verified npm registry
npm install -g openclaw-video-generator

# Configure API Key (choose one):
# Option A: Environment variable (recommended)
export OPENAI_API_KEY="sk-..."
# Add to ~/.bashrc (Linux) or ~/.zshrc (macOS)

# Option B: Pass via command line
openclaw-video-generator generate "your text" --api-key "sk-..."

# Verify installation
openclaw-video --version
```

**Method 2: From Source (Developer Recommended)**

✅ **Pros**: Can modify code, project-local .env, easier debugging
⚠️ **Note**: Requires git clone and manual dependency installation

```bash
# Clone from verified repository
git clone https://github.com/ZhenRobotics/openclaw-video-generator.git ~/openclaw-video-generator

# Verify commit (security check)
cd ~/openclaw-video-generator
git rev-parse HEAD  # Should match verified commit: ac3c568

# Install dependencies
npm install

# Configure .env file (project-level, more secure)
cp .env.example .env
nano .env  # Add your API keys here

# Build (if needed)
npm run build
```

**macOS Users - Special Notes**:

If you encounter permission issues with npm global install:

```bash
# Solution A: Use sudo (simple but requires password)
sudo npm install -g openclaw-video-generator

# Solution B: Configure npm to user directory (recommended, permanent fix)
mkdir -p ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.zshrc
source ~/.zshrc
npm install -g openclaw-video-generator
```

For macOS users, we **recommend Method 2 (Git Clone)** because:
- ✅ Clearer paths, no global install permissions needed
- ✅ Easier .env file management
- ✅ Better for debugging
- ✅ Avoids zsh/bash environment variable confusion

> 💬 **Need Help with Deployment?** Contact our official maintenance partner: **专注人工智能的黄纪恩学长**（闲鱼 Xianyu）for technical support and troubleshooting.

### API Key Configuration

**IMPORTANT**: Store API key securely in `.env` file (never hardcode in scripts)

```bash
cd ~/openclaw-video-generator
cat > .env << 'EOF'
# OpenAI API Configuration
OPENAI_API_KEY="sk-your-key-here"
OPENAI_API_BASE="https://api.openai.com/v1"
EOF

# Secure the file
chmod 600 .env
```

### Verify Installation

```bash
cd ~/openclaw-video-generator
./scripts/test-providers.sh
```

Expected output:
```
✅ TTS: 1 provider(s) configured (openai)
✅ ASR: 1 provider(s) configured (openai)
```

---

## 🚀 Usage

### When to Use This Skill

**AUTO-TRIGGER** when user mentions:
- Keywords: `video`, `generate video`, `create video`, `生成视频`
- Provides a text script for video conversion
- Wants text-to-video conversion

**EXAMPLES**:
- "Generate video: AI makes development easier"
- "Create a video about AI tools"
- "Make a short video with this script..."

**DO NOT USE** for:
- Video editing or clipping
- Video playback or format conversion only

---

## 🎯 Core Features

- 🎤 **Multi-Provider TTS** - OpenAI, Azure, Aliyun, Tencent (auto-fallback)
- ⏱️ **Timestamp Extraction** - Precise speech-to-text segmentation
- 🎬 **Scene Detection** - 6 intelligent scene types
- 🎨 **Video Rendering** - Remotion with cyber-wireframe style
- 🖼️ **Background Videos** - Custom backgrounds with opacity control
- 🔒 **Secure** - Local processing, no data sent to third parties

---

## 💻 Agent Usage Guide

### CRITICAL SECURITY NOTES

1. **Project Location**: Use existing install at `~/openclaw-video-generator/`
2. **Never**: Clone new repos without user confirmation
3. **Always**: Verify `.env` file exists before running commands
4. **Check**: Tools availability (node, npm, ffmpeg) before execution

### Primary Command: Generate Video

**Standard Generation**:
```bash
cd ~/openclaw-video-generator && \
./scripts/script-to-video.sh <script-file> \
  --voice nova \
  --speed 1.15
```

**With Background Video**:
```bash
cd ~/openclaw-video-generator && \
./scripts/script-to-video.sh <script-file> \
  --voice nova \
  --speed 1.15 \
  --bg-video "backgrounds/tech/video.mp4" \
  --bg-opacity 0.6 \
  --bg-overlay "rgba(10,10,15,0.4)"
```

**Example Flow**:

User: "Generate video: AI makes development easier"

Agent:
1. Check if project exists: `ls ~/openclaw-video-generator`
2. Create script file:
   ```bash
   cat > ~/openclaw-video-generator/scripts/user-script.txt << 'EOF'
   AI makes development easier
   EOF
   ```
3. Execute:
   ```bash
   cd ~/openclaw-video-generator && \
   ./scripts/script-to-video.sh scripts/user-script.txt
   ```
4. Show output: `~/openclaw-video-generator/out/user-script.mp4`

### Provider Configuration

**Multi-Provider Support** (v1.2.0+):

The system supports automatic fallback across providers:
- OpenAI (default)
- Azure (enterprise)
- Aliyun (China)
- Tencent (China)

Configure in `.env`:
```bash
# Provider priority (tries left to right)
TTS_PROVIDERS="openai,azure,aliyun,tencent"
ASR_PROVIDERS="openai,azure,aliyun,tencent"
```

Check configuration:
```bash
cd ~/openclaw-video-generator && ./scripts/test-providers.sh
```

---

## ⚙️ Configuration Options

### TTS Voices

**OpenAI**:
- `nova` - Warm, energetic (recommended for short videos)
- `alloy` - Neutral
- `echo` - Clear, male
- `shimmer` - Soft, female

**Azure** (if configured):
- `zh-CN-XiaoxiaoNeural` - Female, general
- `zh-CN-YunxiNeural` - Male, warm
- `zh-CN-XiaoyiNeural` - Female, sweet

### Speech Speed
- Range: 0.25 - 4.0
- Recommended: 1.15 (fast-paced)
- Default: 1.0

### Background Video Options (v1.2.0+)
- `--bg-video <path>` - Background video file
- `--bg-opacity <0-1>` - Opacity (0=invisible, 1=fully visible)
- `--bg-overlay <rgba>` - Overlay color for text clarity

**Recommended Settings**:
| Content Type | Opacity | Overlay |
|--------------|---------|---------|
| Text-focused | 0.3-0.4 | `rgba(10,10,15,0.6)` |
| Balanced | 0.5-0.6 | `rgba(10,10,15,0.4)` |
| Background-focused | 0.7-1.0 | `rgba(10,10,15,0.25)` |

---

## 📊 Video Specifications

- **Resolution**: 1080 x 1920 (vertical, optimized for shorts)
- **Frame Rate**: 30 fps
- **Format**: MP4 (H.264 + AAC)
- **Style**: Cyber-wireframe with neon colors
- **Duration**: Auto-calculated from script length

---

## 🎨 Scene Types (Auto-Detected)

| Type | Visual Effect | Trigger |
|------|---------------|---------|
| **title** | Glitch + spring scale | First segment |
| **emphasis** | Pop-up zoom | Contains numbers/percentages |
| **pain** | Shake + red warning | Problems, pain points |
| **content** | Smooth fade-in | Regular content |
| **circle** | Rotating ring | Listed points |
| **end** | Slide-up fade-out | Last segment |

---

## 💰 Cost Estimation

Per 15-second video: **~$0.003** (< 1 cent):
- OpenAI TTS: ~$0.001
- OpenAI Whisper: ~$0.0015
- Remotion rendering: Free (local)

---

## 🔧 Troubleshooting

### Issue 1: Project Not Found

```bash
# Check installation
ls ~/openclaw-video-generator

# If missing, install via npm (safe)
npm install -g openclaw-video-generator

# Or clone from verified source
git clone https://github.com/ZhenRobotics/openclaw-video-generator.git ~/openclaw-video-generator
cd ~/openclaw-video-generator && npm install
```

### Issue 2: API Key Error

**Error**: `Missing OPENAI_API_KEY` or `model_not_found`

**Solution**:
1. Verify `.env` file exists:
   ```bash
   cat ~/openclaw-video-generator/.env
   ```
2. If missing, create it:
   ```bash
   cd ~/openclaw-video-generator
   echo 'OPENAI_API_KEY="sk-your-key-here"' > .env
   chmod 600 .env
   ```
3. Ensure API key has TTS + Whisper access
4. Verify account has sufficient balance (min $5)

### Issue 3: Provider Failures

**Error**: "All providers failed"

**Solution**:
```bash
# Check provider configuration
cd ~/openclaw-video-generator && ./scripts/test-providers.sh

# Configure additional providers
cat >> .env << 'EOF'
# Azure (optional fallback)
AZURE_SPEECH_KEY="your-azure-key"
AZURE_SPEECH_REGION="eastasia"
EOF
```

### Issue 4: Network/Geographic Restrictions

**Error**: `SSL_connect: 连接被对方重置`

**Solution**: Configure alternative providers (Azure, Aliyun, Tencent) in `.env`

See: `MULTI_PROVIDER_SETUP.md` for detailed configuration

---

## 📚 Documentation

- **Full Guide**: `~/openclaw-video-generator/README.md`
- **Multi-Provider Setup**: `~/openclaw-video-generator/MULTI_PROVIDER_SETUP.md`
- **GitHub**: https://github.com/ZhenRobotics/openclaw-video-generator
- **Issues**: https://github.com/ZhenRobotics/openclaw-video-generator/issues

---

## 🎯 Agent Behavior Guidelines

**DO**:
- ✅ Verify project exists before executing commands
- ✅ Check `.env` configuration before API calls
- ✅ Use existing project directory (`~/openclaw-video-generator/`)
- ✅ Provide clear progress feedback
- ✅ Show output file location after completion
- ✅ Handle errors gracefully with actionable solutions

**DON'T**:
- ❌ Clone repositories without user confirmation
- ❌ Create new Remotion projects (use existing)
- ❌ Hardcode API keys in commands
- ❌ Ignore security warnings
- ❌ Run untrusted scripts

---

## 📊 Tech Stack

- **Remotion**: React-based video framework
- **OpenAI**: TTS + Whisper APIs
- **Azure/Aliyun/Tencent**: Alternative providers
- **TypeScript**: Type-safe development
- **Node.js**: Runtime (v18+)
- **FFmpeg**: Video processing

---

## 🆕 Version History

### v1.2.0 (2026-03-07) - Current
- ✨ Background video support
- 🌐 Multi-provider architecture (OpenAI, Azure, Aliyun, Tencent)
- 🔄 Automatic provider fallback
- 🔒 Enhanced security (proper .env handling)

### v1.1.0 (2026-03-05)
- ✨ Custom color support
- 📦 npm package published
- 🔐 Removed hardcoded API keys

### v1.0.0 (2026-03-03)
- ✨ Initial release

---

## 🔒 Security & Privacy

**Data Processing**:
- ✅ All video rendering is **local**
- ✅ Audio processing is **local**
- ⚠️ TTS/ASR uses OpenAI API (text/audio sent to OpenAI)

**API Key Safety**:
- ✅ Stored in `.env` file (not in code)
- ✅ File permissions: 600 (owner read/write only)
- ✅ Never committed to git (.gitignore)

**Verification**:
- npm package: https://www.npmjs.com/package/openclaw-video-generator
- GitHub repo: https://github.com/ZhenRobotics/openclaw-video-generator
- Verified commit: `e0fb35f`

---

**Project Status**: ✅ Production Ready & Verified

**License**: MIT

**Author**: @ZhenStaff

**Support**: https://github.com/ZhenRobotics/openclaw-video-generator/issues

**ClawHub**: https://clawhub.ai/ZhenStaff/video-generator
