# NoteX 首页链接（带 token）

## 作用

生成带 token 的 NoteX 首页链接：
```
https://notex.aishuo.co/?token=xxx
```

## 说明

- 该能力不新增业务 API。
- token 来源：环境变量 `XG_USER_TOKEN` / 上下文 `token|xgToken|access-token` / CWork Key 换取。
- 仅此场景允许返回带 token 的完整 URL。

## 脚本映射

- `../../scripts/open-link/notex-open-link.js`
