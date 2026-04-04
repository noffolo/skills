# 环境配置指南

## 1. 安装依赖

```bash
npm install puppeteer
```

Puppeteer 会自动下载 Chromium。Linux 服务器可能需要额外系统库：

```bash
# Ubuntu/Debian
apt-get install -y libgbm-dev libasound2 libatk-bridge2.0-0 libatk1.0-0 \
  libcups2 libdrm2 libglib2.0-0 libnss3 libx11-6 libxcomposite1 \
  libxdamage1 libxext6 libxfixes3 libxrandr2 libxss1
```

脚本已内置 `--no-sandbox` 参数，无需额外配置。

---

## 2. 安装中文字体（避免封面图乱码）

脚本使用 **Noto Sans SC** 字体渲染中文，路径固定为 `~/.fonts/NotoSansSC-*.otf`。

### macOS

```bash
brew install font-noto-sans-cjk
```

### Ubuntu/Debian

```bash
apt-get install -y fonts-noto-cjk
```

### 手动安装（服务器/Docker）

```bash
mkdir -p ~/.fonts
wget -O ~/.fonts/NotoSansSC-Regular.otf \
  "https://github.com/notofonts/noto-cjk/raw/main/Sans/OTF/SimplifiedChinese/NotoSansCJKsc-Regular.otf"
wget -O ~/.fonts/NotoSansSC-Bold.otf \
  "https://github.com/notofonts/noto-cjk/raw/main/Sans/OTF/SimplifiedChinese/NotoSansCJKsc-Bold.otf"
fc-cache -f -v
```

> 如需修改字体路径，编辑 `scripts/xhs_publisher.js` 中的 `fontFace` 部分。

---

## 3. 小红书登录

首次使用需登录，之后 session 自动保存在 `~/.openclaw-sessions/xiaohongshu/`，有效期约7天。

**登录方式：手机号 + 验证码**

告诉 Agent「帮我登录小红书」，Agent 会：
1. 打开登录页，自动发送验证码到你的手机
2. 提示你回复6位验证码
3. 登录成功后自动保存 session

Session 保存后无需每次登录，直到过期为止。

---

## 4. 验证安装

```bash
node -e "
const { generateCoverImage } = require('./scripts/xhs_publisher.js');
generateCoverImage('测试标题', '第一行副标题\n第二行副标题\n第三行副标题', '/tmp/test_cover.png')
  .then(p => console.log('✅ 封面图生成成功:', p))
  .catch(e => console.error('❌ 失败:', e.message));
"
```

生成的 `/tmp/test_cover.png` 应为 1080×1440px，中文正常显示即为成功。
