# 查询任务参数与示例

覆盖脚本：`mps_get_video_task.py`、`mps_get_image_task.py`

## 查询音视频任务 — `mps_get_video_task.py`

适用于 `ProcessMedia` 提交的任务（TaskId 格式：`1234567890-WorkflowTask-xxxxxx`）

### 参数说明

| 参数 | 说明 |
|------|------|
| `--task-id` | 任务 ID（必填）|
| `--verbose` / `-v` | 输出完整 JSON 响应（含所有子任务详情）|
| `--json` | 只输出原始 JSON，不打印格式化摘要 |
| `--region` | MPS 服务区域（优先读取 `TENCENTCLOUD_API_REGION` 环境变量，默认 `ap-guangzhou`）|

### 示例命令

```bash
# 查询任务状态（简洁输出）
python scripts/mps_get_video_task.py --task-id 1234567890-WorkflowTask-80108cc3380155d98b2e3573a48a

# 详细输出（含子任务信息）
python scripts/mps_get_video_task.py --task-id 1234567890-WorkflowTask-80108cc3380155d98b2e3573a48a --verbose

# JSON 格式输出（便于程序解析）
python scripts/mps_get_video_task.py --task-id 1234567890-WorkflowTask-80108cc3380155d98b2e3573a48a --json

# 指定地域
python scripts/mps_get_video_task.py --task-id 1234567890-WorkflowTask-80108cc3380155d98b2e3573a48a --region ap-beijing
```

---

## 查询图片任务 — `mps_get_image_task.py`

适用于 `ProcessImage` 提交的任务

### 参数说明

| 参数 | 说明 |
|------|------|
| `--task-id` | 任务 ID（必填）|
| `--verbose` / `-v` | 输出完整 JSON 响应 |
| `--json` | 只输出原始 JSON |
| `--region` | MPS 服务区域（优先读取 `TENCENTCLOUD_API_REGION` 环境变量，默认 `ap-guangzhou`）|

### 示例命令

```bash
# 查询任务状态（简洁输出）
python scripts/mps_get_image_task.py --task-id 1234567890-ImageTask-80108cc3380155d98b2e3573a48a

# 详细输出（含子任务信息）
python scripts/mps_get_image_task.py --task-id 1234567890-ImageTask-80108cc3380155d98b2e3573a48a --verbose

# JSON 格式输出
python scripts/mps_get_image_task.py --task-id 1234567890-ImageTask-80108cc3380155d98b2e3573a48a --json

# 指定地域
python scripts/mps_get_image_task.py --task-id 1234567890-ImageTask-80108cc3380155d98b2e3573a48a --region ap-beijing
```
