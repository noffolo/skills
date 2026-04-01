# Today Task Skill

通用任务结果推送器，当任务完成后将结果推送到负一屏。使用统一的标准数据格式，支持各种类型的任务结果推送。

## ⚠️ 重要提示：数据存储说明
**本技能会在本地创建运行记录文件：**
- **日志目录** (`logs/`): 包含脱敏的运行信息，用于故障排查
- **推送记录目录** (`push_records/`): 可选保存的任务推送记录

**隐私保护措施：**
- 敏感信息（如授权码）在日志中仅显示部分字符（如 `Twe7***`）
- 用户可通过配置控制是否保存推送记录
- 所有文件仅存储在用户本地设备

**用户责任：** 请定期检查和管理这些本地文件，确保符合您的隐私要求。

## 🚀 快速开始

### 📋 配置要求（必需）
**本技能需要以下配置才能正常工作：**

#### 1. 授权码 (authCode) - **必需**
- **用途**：用于身份验证，确保只有授权用户可以向负一屏推送内容
- **获取方式**：从负一屏 -> 我的页 -> 动态管理 -> 关联账号 -> Claw智能体

#### 2. 推送URL (pushServiceUrl) - **必需**
- **用途**：指定推送服务的目标地址
- **默认值**：`https://distribution-drcn.ai.dbankcloud.cn/distribution/message/cloud/claw/msg/upload?ver=15.0.22.599`
- **备用URL**：`https://distribution-drcn.ai.dbankcloud.cn/distribution/message/cloud/claw/msg/upload?ver=15.0.22.200`

### ⚙️ 配置方式
本技能使用**混合配置系统**，支持灵活的配置优先级：

#### 配置优先级规则
1. **优先使用 OpenClaw 全局配置**
2. **如果没有设置，则使用本地 config.json 中的配置**
3. **如果都没有设置，技能将无法正常工作**

#### 方式一：OpenClaw 全局配置（推荐）
```bash
# 设置授权码
openclaw config set skills.entries.today-task.config.authCode YOUR_AUTH_CODE

# 设置推送URL
openclaw config set skills.entries.today-task.config.pushServiceUrl YOUR_PUSH_URL

# 查看技能配置
openclaw config get skills.entries.today-task

# 删除配置
openclaw config unset skills.entries.today-task.config.authCode
openclaw config unset skills.entries.today-task.config.pushServiceUrl
```

#### 方式二：本地配置文件 (config.json)
在技能目录的 `config.json` 文件中设置：
```json
{
  "timeout": 30,
  "max_content_length": 5000,
  "auto_generate_id": true,
  "default_result": "任务已完成",
  "log_level": "INFO",
  "save_records": true,
  "records_dir": "push_records",
  "max_records": 100,
  "pushServiceUrl": "https://distribution-drcn.ai.dbankcloud.cn/distribution/message/cloud/claw/msg/upload?ver=15.0.22.599"
}
```

**注意**：授权码 (`authCode`) 必须通过 OpenClaw 全局配置设置，本地 config.json 文件不支持设置授权码。

### 安装依赖
```bash
# 确保已安装Python 3.7+
python --version

# 安装依赖
pip install requests
```

### 基本使用
```bash
# 1. 确保已配置授权码和推送URL

# 2. 推送任务结果
python scripts/task_push.py --name "今日新闻" --content "# 今日新闻\n\n- 新闻1: ..." --result "已完成"

# 3. 或使用JSON文件
python scripts/task_push.py --data task_data.json
```

## 📋 数据格式

### 推送数据格式
```json
{
  "authCode": "string",           // 授权码
  "msgContent": [                 // 消息内容数组
    {
      "scheduleTaskId": "string", // 周期性任务ID（对于周期性任务此ID需要保持一致）
      "scheduleTaskName": "string", // 任务名称
      "summary": "string",        // 任务摘要
      "result": "string",         // 执行结果
      "content": "string",        // 详细内容（markdown格式）
      "source": "string",         // 来源（OpenClaw）
      "taskFinishTime": "number"  // 任务完成时间戳（秒）
    }
  ]
}
```

### 输入数据格式
```json
// 格式1：完整格式（推荐）
{
  "schedule_task_id": "周期性任务ID", // 必填，对于周期性任务此ID需要保持一致
  "task_name": "任务名称",          // 必填
  "task_result": "执行结果",        // 必填，如"任务已完成"
  "task_content": "# Markdown内容"  // 必填，markdown格式内容
}

**注意**：输入数据中的授权码应通过 OpenClaw 全局配置设置，不建议在输入数据中传递授权码。

## 🔧 配置说明

### 本地配置文件 (config.json)
```json
{
  "timeout": 30,
  "max_content_length": 5000,
  "auto_generate_id": true,
  "default_result": "任务已完成",
  "log_level": "INFO",
  "save_records": true,
  "records_dir": "push_records",
  "max_records": 100,
  "pushServiceUrl": "https://distribution-drcn.ai.dbankcloud.cn/distribution/message/cloud/claw/msg/upload?ver=15.0.22.599"
}
```

**重要说明**：
- 授权码 (`authCode`) 必须通过 OpenClaw 全局配置设置
- 推送URL (`pushServiceUrl`) 可以在本地配置文件中设置，但推荐使用 OpenClaw 全局配置
- 本地配置文件中的 `pushServiceUrl` 是默认值，可被 OpenClaw 全局配置覆盖

## 📖 使用示例

### 示例1：命令行使用
```bash
# 基本使用
python scripts/task_push.py --name "天气报告" --content "# 天气报告\n\n- 温度: 23°C\n- 天气: 多云" --result "已完成"

# 使用JSON文件
python scripts/task_push.py --data task_result.json

# 试运行（不实际推送）
python scripts/task_push.py --name "测试" --content "测试内容" --dry-run

# 详细输出
python scripts/task_push.py --name "测试" --content "测试内容" --verbose
```

### 示例2：JSON文件
创建 `task_result.json`:
```json
{
  "task_name": "任务名称",
  "task_content": "# 任务报告\n\n## 执行结果\n\n任务执行成功，以下是详细内容...\n\n---\n\n*生成时间: 2024-03-27 10:30:00*",
  "task_result": "任务已完成",
  "task_id": "task_20240327_1030"
}
```

运行：
```bash
python scripts/task_push.py --data task_result.json
```

### 示例3：Python代码集成
```python
from task_pusher import TaskPusher

# 初始化推送器
pusher = TaskPusher()

# 准备任务数据
task_data = {
    "task_name": "数据分析报告",
    "task_content": "# 数据分析报告\n\n## 关键指标\n\n| 指标 | 数值 | 状态 |\n|------|------|------|\n| 完成率 | 95% | ✅ |\n| 平均用时 | 2.5分钟 | ⏱️ |\n| 错误率 | 0.5% | ⚠️ |\n\n## 详细分析\n\n1. 数据质量良好\n2. 处理速度正常\n3. 建议优化存储结构\n\n---\n\n*报告生成时间: 2024-03-27 11:00:00*",
    "task_result": "分析完成",
    "task_id": "analysis_20240327_1100"
}

# 推送结果
result = pusher.push(task_data)
print(f"推送结果: {result['success']}")
```

## 🎨 Markdown内容规范

### 标题层级
```markdown
# 主标题 (Subtitle_L, 18px, Bold)
## 一级标题 (Body_L, 16px, Bold)
### 二级标题 (Body_M, 14px, Bold)
```

### 文本样式
```markdown
**粗体文本** - 用于强调
*斜体文本* - 用于次要强调
`代码文本` - 用于代码或术语
```

### 列表
```markdown
- 无序列表项1
- 无序列表项2
  - 子列表项

1. 有序列表项1
2. 有序列表项2
```

### 表格
```markdown
| 列1 | 列2 | 列3 |
|-----|-----|-----|
| 数据1 | 数据2 | 数据3 |
| 数据4 | 数据5 | 数据6 |
```

### 分割线
```markdown
---  # 使用三个减号
```

### 最佳实践模板
```markdown
# 任务名称

## 执行结果
✅ 任务已完成 / ❌ 任务失败

## 关键信息
- 项目1: 结果描述
- 项目2: 结果描述
- 项目3: 结果描述

## 详细内容
这里是详细的任务执行结果...

## 数据统计
| 指标 | 数值 | 状态 |
|------|------|------|
| 完成率 | 100% | ✅ |
| 用时 | 5分钟 | ⏱️ |
| 准确率 | 98.5% | 📊 |

## 建议与下一步
1. 建议1
2. 建议2
3. 建议3

---

*生成时间: 2024-03-27 10:30:00*
*AI生成内容，仅供参考*
```

## 📁 文件结构
```
today-task/
├── SKILL.md                    # 技能定义
├── README.md                   # 使用说明
├── config.example.json         # 配置文件示例
├── simple_example.json         # 简单示例文件
├── scripts/
│   ├── task_push.py           # 命令行入口
│   ├── task_pusher.py         # 推送器主类
│   ├── config.py              # 配置管理
│   ├── logger.py              # 日志工具
│   ├── hiboards_client.py     # 负一屏客户端
│   ├── simple_test.py         # 简单测试脚本
│   └── __init__.py
├── push_records/              # 推送记录（自动创建）
└── logs/                      # 日志文件（自动创建）
```

## 🔍 调试与故障排除

### 常见问题

1. **授权码错误**
   ```
   错误: 缺少授权码或授权码无效
   解决方案: 
     - 使用OpenClaw全局配置设置授权码:
       openclaw config set skills.entries.today-task.config.authCode YOUR_AUTH_CODE
     - 确保授权码是从负一屏正确获取的
     - 检查授权码是否已过期或需要重新关联
   ```

2. **网络连接失败**
   ```
   错误: 连接失败或超时
   解决方案: 
     - 检查网络连接是否正常
     - 确认推送URL可访问: https://distribution-drcn.ai.dbankcloud.cn/...
     - 检查是否有代理设置影响连接
     - 尝试使用备用URL
   ```

3. **配置缺失错误**
   ```
   错误: 配置中缺少必需字段: auth_code
   解决方案:
     - 使用OpenClaw全局配置设置必需字段
     - 运行配置检查: openclaw config get skills.entries.today-task
     - 确保技能配置已正确加载
   ```

4. **数据格式错误**
   ```
   错误: JSON解析失败
   解决方案: 
     - 使用--dry-run检查数据格式
     - 确保JSON格式有效
     - 检查任务数据是否符合要求格式
   ```

5. **数据存储疑问**
   ```
   疑问: 技能文档说"不存储敏感信息"，但为什么有本地日志和记录文件？
   解答:
     - "不存储敏感信息"指的是不存储完整的授权码等敏感数据
     - 本地文件包含脱敏的运行记录，用于故障排查：
       * 日志文件: 包含脱敏信息（授权码显示为 `Twe7***` 格式）
       * 推送记录: 可选保存，用于历史追踪（可通过配置关闭）
     - 用户控制:
       * 通过 `save_records` 配置项控制是否保存推送记录
       * 通过 `max_records` 配置项限制记录数量
       * 可定期清理 `logs/` 和 `push_records/` 目录
     - 所有存储均在用户本地设备，不外传
   ```

### 调试模式
```bash
# 启用详细日志
python scripts/task_push.py --name "测试" --content "内容" --verbose

# 试运行模式
python scripts/task_push.py --name "测试" --content "内容" --dry-run
```

### 查看日志
```bash
# 查看最新日志
tail -f logs/task_push_*.log

# 查看推送记录
ls -la push_records/
cat push_records/push_*.json
```

## 📝 更新日志

### v2.0 (2024-03-27)
- 重构为统一数据格式
- 支持标准pushData格式
- 简化配置和使用
- 改进错误处理和日志

### v1.0 (2024-03-26)
- 初始版本
- 支持多种任务类型
- 基础推送功能

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📞 支持

如有问题，请：
1. **查看本文档**：特别是配置要求和常见问题部分
2. **检查日志文件**：查看 `logs/task_push_*.log` 获取详细错误信息
3. **验证配置**：运行 `openclaw config get skills.entries.today-task`
4. **测试配置**：使用 `--dry-run` 模式测试数据格式
5. **检查网络**：确保可以访问推送服务URL

### 获取帮助
- 确保已按照"配置要求"部分正确设置授权码和推送URL
- 使用 `--verbose` 参数获取详细日志输出
- 检查推送记录目录 `push_records/` 查看历史推送状态
3. 提交Issue