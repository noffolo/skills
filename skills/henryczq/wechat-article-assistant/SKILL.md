---
name: wechat-article-assistant
description: 多个微信公众号文章同步和下载助手。通过本地 Python 脚本完成微信公众号后台登录、登录态保存、公众号搜索与管理、文章同步、文章详情抓取与导出。用于需要登录公众号平台、同步公众号最新文章、查询文章列表、抓取单篇文章详情、排查登录或代理问题的场景。
---

# WeChat Article Assistant

用这个 Skill 处理 5 类事：

1. 登录微信公众号后台并保存登录态
2. 搜索 / 添加 / 删除公众号
3. 同步公众号文章列表到本地
4. 抓取单篇公众号文章详情
5. 排查登录、代理、环境问题

## 主入口

统一使用：

```bash
python scripts/wechat_article_assistant.py --help
```

## 核心规则

### 1. 登录优先用一体化等待模式

优先使用：

```bash
python scripts/wechat_article_assistant.py login-start --wait true ...
```

正常情况下会：生成二维码 → 发回当前会话 → 后端等待扫码 → 登录成功后通知。

如果二维码自动发送失败，当前实现会降级处理：

- 先保留二维码会话 `sid`
- 直接返回 `qr_path` 与 `resume_command`
- 不继续无意义地长等待
- 外层补发二维码后，再执行：

```bash
python scripts/wechat_article_assistant.py login-wait --sid 'SID' --json
```

不要优先设计成“用户扫码后再手动回来汇报”。

### 2. 登录二维码回传必须带 channel / target / account

从 Inbound Context 读取：

- `channel` ← `channel`
- `target` ← `chat_id`
- `account` ← `account_id`

示例：

```bash
python scripts/wechat_article_assistant.py login-start \
  --channel "${channel}" \
  --target "${target}" \
  --account "${account}" \
  --wait true \
  --json
```

只要 `account_id` 存在，就传 `--account`。不要省略。

### 3. 文章抓取代理和同步代理是两回事

分别由：

- `apply_article_fetch`
- `apply_sync`

控制。不要混用判断。

### 4. 同步代理按网关模式理解，不按标准 CONNECT 代理理解

代理地址应当是这种：

```text
https://your-gateway.example.com
```

运行时会拼成：

```text
https://your-gateway.example.com/?url=https://mp.weixin.qq.com/...
```

同步和文章抓取现在都优先按这种 gateway 风格处理。

**不要把它当成标准 HTTP/HTTPS CONNECT 代理。**

### 5. 文章详情优先用短链接

抓详情时优先归一化成：

```text
https://mp.weixin.qq.com/s/...
```

不要优先依赖长 query 链接。

## 常用命令

### 检查登录状态

```bash
python scripts/wechat_article_assistant.py login-info --validate true --json
```

### 查看代理配置

```bash
python scripts/wechat_article_assistant.py proxy-show --json
```

### 同步全部公众号

```bash
python scripts/wechat_article_assistant.py sync-all --interval-seconds 180 --json
```

### 同步单个公众号

```bash
python scripts/wechat_article_assistant.py sync --fakeid "FAKEID" --json
```

### 查看同步日志

```bash
python scripts/wechat_article_assistant.py sync-logs --limit 20 --json
```

### 抓单篇文章详情

```bash
python scripts/wechat_article_assistant.py article-detail \
  --link "https://mp.weixin.qq.com/s/xxxxxxxx" \
  --json
```

## 默认排查顺序

用户说“报错 / 失败 / 不工作 / 登录异常 / 同步异常”时，默认先做只读排查：

```bash
python scripts/wechat_article_assistant.py env-check --json
python scripts/wechat_article_assistant.py doctor --json
python scripts/wechat_article_assistant.py login-info --validate true --json
python scripts/wechat_article_assistant.py proxy-show --json
```

默认先解释原因，不要擅自改代码、改配置、装依赖，除非用户明确要求修复。

## 同步失败时怎么判断

先看错误类型：

- `invalid session`：优先怀疑公众号后台登录态失效
- `代理连接失败`：优先怀疑网关地址、回源能力或错误地走到了标准代理分支
- `微信接口返回非 JSON`：优先怀疑网关返回了错误页/拦截页

如果 sync 返回里已经带了 `data.request_debug`，优先看：

- `mode`：`gateway` / `direct`
- `request_url`
- `curl`

## 登录状态判断

当前 Skill 的登录检查已经在 sync 前做显式校验。

期望行为：

- 如果后台首页看起来不像已登录页面，就尽早报重新登录
- 不要等到 `appmsgpublish` 再返回 `invalid session`

## 什么时候读附加参考

遇到这些情况，再读 `references/operations.md`：

- 需要完整命令配方
- 需要代理 / 网关配置示例
- 需要 Windows Python 别名排查
- 需要环境依赖排查清单
- 需要 OpenClaw cron 建议
- 需要理解 sync debug 输出

更底层的实现细节再看：

- `references/interface-reference.md`
- `references/design.md`
- `references/sqlite-schema.md`

只有在继续做产品规划、范围评审或长期演进设计时，再看仓库级文档：

- `docs/wechat-article-assistant-requirements-functional-spec.md`
