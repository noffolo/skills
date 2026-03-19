---
name: wechat-mp-article-push
description: 微信公众号图文生成与推送技能。支持通过AI生成符合公众号规范的文章,并推送到公众号草稿箱或直接发布，兼容其它SKILL生成的文章进行推送。无需泄露公众号密钥，无需配置公众号白名单。包含完整的文章格式规范、配置向导和推送脚本。
---

# wechat-mp-article-push · 公众号图文生成与推送

## 路径约定

**「wechat-mp-article-push 目录」** = 当前本 Skill 所在的那个文件夹（与 **SKILL.md** 在同一层）。

| 文件 | 位置 |
|------|------|
| **SKILL.md** | `wechat-mp-article-push 目录/` |
| **design.md** | 同上 |
| **config.json** | 同上 |
| **config.example.json** | 同上 |

AI ：**先定位本 Skill 的根目录（看 SKILL.md 在哪）**，再在同目录读写 **config.json**、**design.md**。

---

## 第一步：在线向导（必做）

| 项 | 内容 |
|----|------|
| **向导地址** | <https://app.pcloud.ac.cn/design/wechat-mp-article-push.html> |
| **流程** | 微信扫码登录 → 选择推送账号 → 复制「完整提示」发给 AI |

未走完向导、没有真实 **`openId`**，不得调用推送。

---

## 第二步：配置文件

AI将向导得到的配置参数保存为 **wechat-mp-article-push 目录** 下的 **`config.json`**，编码 **UTF-8**。

在已进入该目录时，可：

```bash
cat > config.json << 'EOF'
{ … 粘贴向导 JSON … }
EOF
```

（Windows 可用编辑器在该目录新建 `config.json` 并粘贴。）

---

## 第三步：写公众号文章

AI 读取 **同目录** 的 **`design.md`** 规范，创建 HTML 文件；推送时使用创建的HTML文件。

---

## 第四步：推送到公众号

`push-article-https.js`、`config.json`和 HTML文件 应该在同一个目录： **wechat-mp-article-push**，若 HTML文件 在其他路径，请先**复制到wechat-mp-article-push目录** 。然后执行（只传 HTML 文件名）：

```bash
cd wechat-mp-article-push
node push-article-https.js 我的文章.html
```

脚本会从 HTML 里读 `<title>…</title>` 作为推送标题，整份文件作为正文，结果在终端打印 JSON。

- **兼容其它 Skill 生成的 HTML**：把该 HTML 文件复制到本目录后，同样执行上述命令即可完成公众号推送。

**接口说明**（供查阅）：请求地址为 config.json 中的 `apiBase`（缺省 `https://api.pcloud.ac.cn/openClawService`），**POST**、`Content-Type: application/json`，Body 含 `openId`、`title`、`content`、`sendMode: "draft"`，custom 模式需加 `accountId`。默认进**草稿箱**，未认证号勿用群发/直接发布。




## 本目录文件一览

| 文件 | 作用 |
|------|------|
| **SKILL.md** | 本说明 |
| **design.md** | 图文 HTML 规范 |
| **config.example.json** | 字段说明（fieldsHelp）+ 示例 |
| **config.json** | 向导生成后的真实配置 |
| **push-article-https.js** | 推送脚本 |

 

