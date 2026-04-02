---
name: maze-ai
version: 1.0.0
description: "Maze AI"
---

# Maze API 智能助手

## 认证流程

### Step 1: 登录获取身份列表

**⚠️ 不要在 skill 中硬编码账号密码！**

当用户说"登录"时，**必须先询问用户名和密码**，然后用用户提供的凭据登录：

```bash
curl -X POST "https://t.stoooges.cn/api/login" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{ "password": "{用户提供的密码}", "username": "{用户提供的用户名}"}'
```

**重要**：每次登录都要询问用户，不要使用任何默认账号密码。

### Step 2: 切换身份获取专用 Token

```bash
curl -X GET "https://t.stoooges.cn/api/get_login_info?id={identity_id}" \
  -H "accept: application/json" \
  -H "token: {主token}"
```

## 身份 ID 对照表

| ID | 身份代码 | 中文名称 |
|---|---|---|
| 93 | salesvp | 销售合伙人 |
| 1799 | sales | 销售 |
| 2121 | mentorhead | 导师主管 |
| 4831 | plmentor | 规划导师 |
| 5401 | bd | 商务 |
| 5402 | bdhead | 商务主管 |

---

## 销售数据查询 API

### 端点

```
POST https://t.stoooges.cn/api/sales/vp/achievement/categorical_data
```

### 请求示例

```bash
curl -X POST "https://t.stoooges.cn/api/sales/vp/achievement/categorical_data" \
  -H "accept: application/json" \
  -H "token: {身份token}" \
  -H "Content-Type: application/json" \
  -d '{
    "area": "hz",
    "category": 4,
    "endYearMonth": "",
    "startYearMonth": "",
    "type": ""
  }'
```

### 参数说明

#### category（数据类型，必填）

| 值 | 含义 |
|---|---|
| 1 | 线索数 |
| 2 | 签约数 |
| 3 | 签约率 |
| 4 | 签约额 |
| 5 | 到账金额 |

#### type（业务类型，可选）

| 值 | 含义 |
|---|---|
| "" | 全部 |
| u | 美本 |
| uk | 非美本 |
| t | 转学 |
| g | 研究生 |
| o | 单项 |

#### area（区域，可选）

| 值 | 含义 |
|---|---|
| "" | 全部 |
| hz | 杭州 |
| sh | 上海 |
| bj | 北京 |
| xa | 西安 |
| sz | 深圳 |
| cq | 重庆 |
| cd | 成都 |
| cs | 长沙 |
| qd | 青岛 |

#### startYearMonth / endYearMonth（时间范围，可选）

格式：`YYYY-MM-DD`，例如 `2026-03-02`

---

## 使用场景

当用户问以下问题时，自动调用 API 查询：

- "杭州的签约额是多少" → category=4, area=hz
- "美本签约数" → category=2, type=u
- "上海研究生到账金额" → category=5, area=sh, type=g
- "本月的线索数" → category=1 + 时间参数
- "签约率是多少" → category=3

**注意**：查询前确保已切换到正确身份并获取 token。
