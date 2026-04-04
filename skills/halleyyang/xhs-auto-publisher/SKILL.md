---
name: xhs-publisher
description: 小红书通用自动发帖技能。全流程自动化：AI生成帖子内容 → 生成封面图（6套风格模板）→ Puppeteer自动发布到小红书创作者中心。适合运营任意垂直领域小红书账号（科技、生活、美食、旅行、节日、知识分享等）。当用户需要自动发小红书帖子、生成封面图、或定时发帖时使用。
---

# xhs-publisher · 小红书通用发帖技能

AI 生成内容 → 自动生成封面图 → 一键发布到小红书。支持任意主题，不限领域。

## 前置条件

- **Node.js** ≥ 18，依赖已预装（`scripts/node_modules/`）
- **中文字体**：封面图渲染需要 Noto Sans SC，见 [references/setup.md](references/setup.md)
- **小红书账号**：首次使用需手机号 + 验证码登录，之后 session 自动持久化（有效期约 7 天）

## 核心文件

| 文件 | 说明 |
|------|------|
| `scripts/xhs_publisher.js` | 主脚本，导出 `generateCoverImage`, `publishPost`, `loginWithPhone`, `checkContentSafety` 等 |
| `references/posting-guide.md` | 帖子写作规范、话题标签策略、封面模板说明 |
| `references/setup.md` | 环境配置、字体安装、依赖安装指南 |

## 对话流程

### 发帖请求

当用户说「帮我发一篇关于 XX 的小红书」时，按以下步骤执行：

1. **生成帖子内容**：根据主题生成标题（≤20字）、正文（200-400字）、话题（3-5个）
2. **生成封面图**：调用 `generateCoverImage`，副标题用 `\n` 换行
3. **展示给用户确认**：将封面图和帖子文字发给用户预览
4. **发布**：用户确认后调用 `publishPost` 发布

> ⚠️ 发布前必须让用户确认内容，不要跳过预览步骤直接发布。

### 登录引导话术

Session 失效时，引导用户提供手机号：

> 「需要重新登录小红书，请告诉我注册手机号，我来帮你发验证码。」

## 内容安全规范

脚本内置 `checkContentSafety()` 安全检查，发布前自动拦截违规内容。

### 🚫 会被拦截的内容

| 类型 | 示例 | 原因 |
|------|------|------|
| 人身攻击 | `智障` `脑残` `去死` | 直接违规 |
| 煽动对立 | `你支持谁？` `谁更有理？` | 平台判定站队煽动 |
| 强烈倾向性定性 | `全是他的错` `活该` `咎由自取` | 不当言论风险 |
| 未证实指控 | `故意侵权` `明知故犯` | 名誉侵权风险 |

### ✅ 争议话题写法原则

陈述事实 + 开放提问，不站队、不定性。结尾用「你怎么看？」而非「你支持谁？」。

## API 参考

### `generateCoverImage(title, subtitle, outputPath, footer?)`

生成封面图（PNG，1080×1440px）。

```js
const { generateCoverImage } = require('./scripts/xhs_publisher.js');

await generateCoverImage(
  '清明节，比你想的更厚重',            // 标题（≤20字）
  '它不只是扫墓\n藏着2500年的家国情怀\n今天聊聊它真正的故事',  // 副标题（\n 换行）
  '/tmp/xhs_cover.png',               // 输出路径（绝对路径）
  '知识分享'                           // 可选，底部署名
);
```

模板根据标题 hash 自动选择（同一标题始终对应同一套模板）。

---

### `publishPost(options)`

发布帖子到小红书创作者中心。

```js
const { publishPost } = require('./scripts/xhs_publisher.js');

await publishPost({
  title: '清明节，比你想的更厚重',      // 必填，≤20字
  content: '很多人以为清明只是...',     // 必填，正文（纯文本，不含话题标签）
  topics: ['传统文化', '清明节', '历史故事'],  // 必填，3-5个话题
  imagePath: '/tmp/xhs_cover.png',     // 必填，封面图绝对路径

  // session 失效时传入以下两项，触发自动登录
  phone: '13812345678',                // 可选，手机号
  askCodeFn: async (prompt) => {       // 可选，向用户索取验证码的异步函数
    return await askUser(prompt);      // 返回6位验证码字符串
  },
});
```

**返回值**：`Promise<boolean>` — `true` 表示发布成功。

---

### `loginWithPhone(page, phone, askCodeFn)`

手动触发手机号登录（通常由 `publishPost` 内部自动调用）。

```js
const puppeteer = require('puppeteer');
const { loginWithPhone } = require('./scripts/xhs_publisher.js');

const browser = await puppeteer.launch({ headless: true, args: ['--no-sandbox'] });
const page = await browser.newPage();

await loginWithPhone(page, '13812345678', async (prompt) => {
  return await askUser(prompt); // 返回6位验证码
});
```

---

### `checkContentSafety(title, content)`

独立调用安全检查（`publishPost` 内部已自动调用，一般无需手动调用）。

```js
const { checkContentSafety } = require('./scripts/xhs_publisher.js');

const result = checkContentSafety('标题', '正文内容');
if (!result.safe) {
  console.error('内容不安全:', result.reason);
}
```

## 封面图模板

| 编号 | 名称 | 背景色 | 风格 | 适合内容 |
|------|------|--------|------|----------|
| 0 | 珊瑚红·撞色 | #FF5A5F / #FFF8F0 | 上下分割，大字冲击 | 热点、节日、话题性内容 |
| 1 | 奶油白·极简 | #FAFAF8 | 白底黑字，高级留白 | 知识、观点、深度内容 |
| 2 | 墨绿·自然风 | #2D4A3E | 文艺清新 | 人文、生活、旅行、历史 |
| 3 | 深蓝·知性风 | #0F2342 渐变 | 沉稳理性 | 科普、职场、财经 |
| 4 | 柠黄·活力风 | #F9E84E | 明亮年轻 | 美食、穿搭、娱乐 |
| 5 | 丁香紫·治愈风 | #EDE0F5 渐变 | 圆润柔和，卡片设计 | 情感、心理、治愈系 |

## 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `XHS_PROFILE_DIR` | Puppeteer 用户数据目录（含 session cookie） | `~/.openclaw-sessions/xiaohongshu` |

## 常见问题排查

| 现象 | 排查方法 |
|------|----------|
| 封面图中文乱码 | 检查 Noto Sans SC 字体是否安装，见 [references/setup.md](references/setup.md) |
| 发布按钮未找到 | 自动截图 `xhs_pre_publish.png` 保存到 workspace，检查页面状态 |
| 话题未正确插入 | 话题面板弹出较慢时自动用 Enter 兜底，不影响发布；可在发布后手动补充话题 |
| Session 过期 | 重新调用 `loginWithPhone` 或在 `publishPost` 传入 `phone` + `askCodeFn` |
| 登录失败/验证码错误 | 调试截图保存于 `/tmp/xhs_login_debug.png`、`/tmp/xhs_after_login.png` |
