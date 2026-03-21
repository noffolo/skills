---
name: 软著材料生成
description: >
  创建生成软著材料生成任务：传入系统名称与接收邮箱，调用后端 API 创建任务并返回 taskId。
  适用于将“创建任务”能力封装成可复用脚本，供自动化/工作流/平台集成调用。
---

## 何时使用

- 需要通过脚本创建软著材料生成任务，并传递 **系统名称** 与 **邮箱**。
- 需要将该能力发布到 ClawHub，供外部复用。

## 输入

- `SYSTEM_NAME` / `--system-name`：系统名称（必填）
- `NOTIFY_EMAIL` / `--notify-email`：接收邮箱（必填）
- `ACCESS_TOKEN` / `--access-token`：可选，会作为 Header `access_token` 传入（用于同一会话下创建任务）

## 输出

- 成功：打印接口返回 JSON（包含 `taskId` 等字段）
- 失败：返回非 0 退出码，并打印错误信息

## 使用方式

### Python（推荐，跨平台）

```bash
python scripts/create_task.py \
  --system-name "农业机械化信息网平台" \
  --notify-email "user@example.com"
```

## 发布到 ClawHub

在包含 `SKILL.md` 的目录执行（示例）：

```bash
clawhub publish . --slug code-right-create-task --name "Code-Right: Create Task" --version 0.1.0
```

