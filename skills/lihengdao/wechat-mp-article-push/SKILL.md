---
name: wechat-mp-article-push
description: 微信公众号图文生成与推送技能。支持通过AI生成符合公众号规范的文章,并推送到公众号草稿箱或直接发布，兼容其它SKILL生成的文章进行推送。通过配置向导扫码授权，无需泄露公众号Secret密钥，无需配置公众号IP白名单。
---

# wechat-mp-article-push · 公众号图文生成与推送

## 文件路径与作用

**「wechat-mp-article-push 目录」** = 当前本 Skill 所在的那个文件夹（与 **SKILL.md** 在同一层）。

| 文件 | 位置 | 作用 |
|------|------|------|
| **SKILL.md** | `wechat-mp-article-push 目录/` | 本说明 |
| **design.md** | 同上 | 图文 HTML 规范 |
| **config.json** | 同上 | 配置向导生成后的真实配置 |
| **config.example.json** | 同上 | 字段说明（fieldsHelp）+ 示例 |
| **push-article-https.js** | 同上 | 推送脚本 |
 
---

## 第一步：配置向导

| 项 | 内容 |
|----|------|
| **配置向导地址** | <https://app.pcloud.ac.cn/design/wechat-mp-article-push.html> |
| **流程** | AI发送配置向导给用户 → 用户微信扫码 → 用户选择推送账号 → 用户复制发给AI |

AI检查在 **wechat-mp-article-push 目录** 下是否存在 **`config.json`** 。如果不存在，则无法使用本技能，AI需要发送配置向导地址给用户扫码授权。

---

## 第二步：配置文件

AI将配置向导得到的配置参数保存为 **wechat-mp-article-push 目录** 下的 **`config.json`**，编码 **UTF-8**。

在已进入该目录时，可：

```bash
cat > config.json << 'EOF'
{ … 粘贴配置向导 JSON … }
EOF
```

（Windows 可用编辑器在该目录新建 `config.json` 并粘贴。）

---

## 第三步：写公众号文章

用户发送文章创作要求给AI，AI根据 `design.md` 规范生成 HTML 文件。
- **文章或通用**：默认宽度 677px，适合文章或通用类型
- **图文卡片**：宽度 375px，固定分页比例（默认 3:4），类似小红书图文卡片，适合截图分发至朋友圈、小红书或其它社群
---

## 第四步：推送到公众号

AI 保证 `push-article-https.js`、`config.json`和 HTML文件 应该在同一个目录： **wechat-mp-article-push**。若 HTML文件 在其他路径，AI先**复制到wechat-mp-article-push目录** 。然后执行（只传 HTML 文件名）：

```bash
cd wechat-mp-article-push
node push-article-https.js 我的文章.html
```

脚本会从 HTML 里读 `<title>…</title>` 作为推送标题，整份文件作为正文，结果在终端打印 JSON。

- **兼容其它 Skill 生成的 HTML**：AI把该 HTML 文件复制到本目录后，同样执行上述命令即可完成公众号推送。

**接口说明**（供查阅）：请求地址为 config.json 中的 `apiBase`（缺省 `https://api.pcloud.ac.cn/openClawService`），**POST**、`Content-Type: application/json`，Body 含 `openId`、`title`、`content`、`sendMode: "draft"`，custom 模式需加 `accountId`。默认进**草稿箱**，未认证号勿用群发/直接发布。






 

