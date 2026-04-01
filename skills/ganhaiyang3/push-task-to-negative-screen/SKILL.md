---
name: today-task
description: 通用任务结果推送器，当任务完成后将结果推送到负一屏。使用统一的标准数据格式，支持各种类型的任务结果推送。
trigger: 当用户说"任务完成，推送到负一屏"、"推送任务结果"、"发送到负一屏"或任何任务完成后需要推送结果到负一屏的场景
config:
  required:
    - authCode: "授权码，从负一屏获取，用于身份验证"
    - pushServiceUrl: "推送服务URL，config.json中有默认值"
  optional:
    - timeout: "超时时间（秒），默认30"
    - max_content_length: "最大内容长度，默认5000"
    - auto_generate_id: "是否自动生成任务ID，默认true"
    - default_result: "默认任务结果，默认'任务已完成'"
    - log_level: "日志级别，默认'INFO'"
    - save_records: "是否保存推送记录，默认true"
    - records_dir: "记录目录，默认'push_records'"
    - max_records: "最大记录数，默认100"
---

# Today Task
## 技能概述
这是一个通用的任务结果推送器，专门用于在任务完成后将结果推送到负一屏。使用统一的标准数据格式，支持各种类型的任务结果推送。

## 🔒 安全说明
本技能已通过安全审查，不包含恶意代码。所有网络请求仅发送到用户配置的指定URL，不收集或传输敏感信息。详细安全声明请查看 [SECURITY.md](./SECURITY.md)。

## ⚙️ 配置要求（必需）
**本技能需要以下配置才能正常工作：**

### 1. 授权码 (authCode) - **必需**
- **用途**：用于身份验证，确保只有授权用户可以向负一屏推送内容
- **获取方式**：
  1. 从手机桌面右滑进入负一屏
  2. 点击左上角头像
  3. 进入"我的"页面，点击右上角设置图标
  4. 选择"动态管理"
  5. 点击"关联账号"
  6. 找到"Claw智能体"并点击获取授权码

### 2. 推送URL (pushServiceUrl) - **必需**
- **用途**：指定推送服务的目标地址
- **默认值**：config.json中有默认值
- **众测URL**：`https://distribution-drcn.ai.dbankcloud.cn/distribution/message/cloud/claw/msg/upload?ver=15.0.22.599`
- **正式环境URL**：`https://distribution-drcn.ai.dbankcloud.cn/distribution/message/cloud/claw/msg/upload?ver=15.0.22.300`

### 🔧 配置方式
本技能使用**混合配置系统**，支持灵活的配置优先级：

#### 配置优先级规则
1. **优先使用 OpenClaw 全局配置**
2. **如果没有设置，则使用本地 config.json 中的配置**
3. **如果都没有设置，技能将无法正常工作**

#### OpenClaw 全局配置命令
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

#### 本地配置文件 (config.json)
其他配置项在技能目录的 `config.json` 文件中设置：
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
  "pushServiceUrl": "https://distribution-drcn.ai.dbankcloud.cn/distribution/message/cloud/claw/msg/upload?ver=15.0.22.200"
}
```

**注意**：如果缺少必需的授权码或推送URL配置，技能将无法正常工作并会显示明确的错误信息。

## 💾 数据存储说明
**本技能会在本地创建以下目录用于运行记录：**

### 📁 日志目录 (`logs/`)
- **用途**：运行监控和故障排查
- **内容**：包含脱敏的运行信息（授权码显示为 `Twe7***` 格式）
- **控制**：通过 `log_level` 配置项控制详细程度

### 📁 推送记录目录 (`push_records/`)
- **用途**：历史记录和审计追踪
- **内容**：任务推送响应数据
- **控制**：
  - 通过 `save_records` 配置项控制是否保存（默认：`true`）
  - 通过 `max_records` 配置项控制最大记录数（默认：`100`）
  - 通过 `records_dir` 配置项指定目录位置

### 🔐 隐私保护措施
1. **敏感信息脱敏**：授权码等敏感信息在日志中仅显示部分字符
2. **用户完全控制**：可关闭记录保存功能
3. **本地存储**：所有文件仅存储在用户本地设备
4. **定期清理**：建议定期清理或通过配置限制文件数量

**用户责任**：请定期检查和管理这些本地文件，确保符合您的隐私要求。

## 🎯 设计理念
- **统一格式**：使用标准化的数据格式，不区分任务类型
- **简单直接**：专注于任务结果的格式化和推送
- **灵活通用**：支持任何类型的任务结果
- **易于集成**：提供简单的API接口

## 📋 触发条件
- "任务完成，推送到负一屏"
- "推送任务结果"
- "发送到负一屏"
- 任何任务完成后需要推送结果到负一屏的场景

## 🔄 工作流程
1. **任务完成**：其他技能或任务执行完成
2. **结果收集**：收集任务执行结果数据
3. **格式转换**：将任务结果转换为标准格式
4. **数据验证**：验证数据完整性和格式
5. **执行推送**：推送到负一屏系统
6. **结果反馈**：返回推送状态和记录

## 📊 标准数据格式
### 推送数据格式
```json
{
  "authCode": "string",           // 授权码，负一屏上对openclaw进行账号关联之后生成的授权码
  "msgContent": [                 // MsgContent数组，消息内容
    {
      "scheduleTaskId": "string", // 任务ID，必填，对于周期性任务此ID需要保持一致
      "scheduleTaskName": "string", // 任务名称，必填，如"生成日报任务、生成新闻任务"
      "summary": "string",        // 任务摘要，必填，说明具体是什么任务，以及任务的执行状态，比如 "生成新闻早报任务已完成"、"生成新闻早报任务异常"
      "result": "string",         // 任务执行结果，必填，说明是已成功完成了，还是异常中断了
      "content": "string",        // 任务的执行结果具体内容，markdown格式的长文本数据，必填
      "source": "string",         // 来源，人工是openclaw的任务，则值为OpenClaw，必填
      "taskFinishTime": "number"  // 任务完成的时间戳，秒的时间戳，必填
    }
  ]
}
  }
}
```

### 内容格式规范
任务的执行结果具体内容使用markdown格式，遵循以下样式规范：

1. **主标题文本**
   - font size: Subtitle_L (Bold) = 18
   - color: font_primary = #000000 90%
   - 行高：默认

2. **一级文本**
   - font size: Body_L (Bold) = 16
   - color: font_primary = #000000 90%
   - 行高：22

3. **二级文本**
   - font size: Body_M (Bold) = 14
   - color: font_primary = #000000 90%
   - 行高：22

4. **段落文本**
   - font size: Body_M (regular) = 14
   - color: font_secondary = #000000 60%
   - 行高：22

5. **分割线**
   - 使用控件：Divider

6. **AI生成注释文本**
   - font size: 10 medium
   - color: font_fourth #000000 20%
   - 行高：默认

## 📁 输入要求
### 任务结果数据格式
```json
{
  "task_id": "string",           // 任务ID（必填）
  "task_name": "string",         // 任务名称（必填）
  "task_result": "string",       // 任务执行结果描述（必填）
  "task_content": "string",      // 任务详细内容，markdown格式（必填）
  "schedule_task_id": "string",  // 周期性任务ID（必填，非周期性任务时等于task_id）
  "auth_code": "string"          // 授权码（可选，可在配置中设置）
}
```

### 简化输入格式
```json
// 格式1：完整格式
{
  "task_id": "news_20240327_1001",
  "task_name": "今日新闻汇总",
  "task_result": "任务已完成",
  "task_content": "# 今日新闻汇总\n\n## 热点新闻\n\n1. OpenAI发布新一代模型...",
  "schedule_task_id": "news_20240327_1001",
  "auth_code": "asdf166553"
}
```

## 🛠️ 推送流程
1. **数据接收**：接收任务结果数据
2. **格式标准化**：转换为标准pushData格式
3. **数据验证**：验证必需字段
4. **授权码处理**：使用配置的授权码或数据中的授权码
5. **推送执行**：调用负一屏API推送数据
6. **结果处理**：处理推送结果并保存记录

## 📝 输出格式
### 成功响应
```json
{
  "success": true,
  "message": "任务结果推送成功",
  "task_id": "news_20240327_1001",
  "task_name": "今日新闻汇总",
  "push_time": "2024-03-27 10:15:30",
  "record_id": "push_20240327_101530",
  "hiboard_response": {
    "code": "0000000000",
    "desc": "成功"
  }
}
```

### 错误响应
```json
{
  "success": false,
  "message": "错误描述",
  "task_id": "news_20240327_1001",
  "task_name": "今日新闻汇总",
  "error_type": "validation|format|network|system|auth|service",
  "push_time": "2024-03-27 10:15:30",
  "suggestion": "建议的解决方案"
}
```

## 🚨 错误码处理指南

系统提供了详细的错误码处理功能，当推送失败时会返回具体的错误信息和解决方案。

### 常见错误码及解决方案

#### 1. 错误码: 0000900034 - 授权码无效或未关联
**问题描述**: 授权码无效或用户未在负一屏关联账号
**解决方案**:
1. 从手机桌面右滑进入负一屏
2. 点击左上角头像
3. 进入"我的"页面，点击右上角设置图标
4. 选择"动态管理"
5. 点击"关联账号"
6. 找到"Claw智能体"并点击获取授权码

#### 2. 错误码: 0200100004 - 负一屏云推送服务异常
**问题描述**: 负一屏云推送到服务动态云有报错，需要检查返回的desc字段

##### CP错误码: 82600017 - 设备未联网或未登录华为账号
**解决方案**:
1. 检查设备Wi-Fi或移动数据是否已连接
2. 打开"设置"应用
3. 进入"华为账号"或"帐号中心"
4. 确保已登录华为账号
5. 如未登录，请使用华为账号登录

##### CP错误码: 82600013 - 服务动态推送开关已关闭
**解决方案**:
1. 从手机桌面右滑进入负一屏
2. 点击左上角头像
3. 进入"我的"页面，点击右上角设置图标
4. 选择"动态管理"
5. 找到"AI任务完成通知"
6. 打开"场景开关"和"服务提供方开关"

##### CP错误码: 82600005 - 服务动态云服务异常
**解决方案**:
1. 等待几分钟后重试
2. 如问题持续，可能是服务端维护
3. 可稍后再试或联系技术支持

### 错误信息格式
错误信息会包含详细的结构化内容：
- 错误代码和描述
- 问题分析
- 具体解决方案
- 操作步骤
- 技术支持信息

### 示例错误信息
```
错误代码: 0000900034
错误描述: 授权码无效

[问题分析] 授权码无效或未关联

[解决方案] 请您到负一屏 -> 我的页 -> 动态管理 -> 关联账号 -> 点击Claw智能体去获取授权码

[操作步骤]
1. 从手机桌面右滑进入负一屏
2. 点击左上角头像
3. 进入"我的"页面，点击右上角设置图标
4. 选择"动态管理"
5. 点击"关联账号"
6. 找到"Claw智能体"并点击获取授权码

[技术支持]
- 如问题无法解决，请记录错误代码并提供给技术支持
- 错误发生时间: 2026-03-30 17:10:00
```

## 🔗 与其他技能配合
### 典型工作流
```
1. 执行某个任务（如查询新闻、检查天气、生成报告等）
2. 任务完成后，生成markdown格式的结果
3. 调用本技能推送结果到负一屏
4. 用户可以在负一屏查看任务结果
```

### 集成示例
```python
# 在其他技能中调用本技能
def complete_task_and_push(task_name, task_content, task_result="任务已完成"):
    # 1. 准备任务数据
    task_data = {
        "task_id": f"{task_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "task_name": task_name,
        "task_result": task_result,
        "task_content": task_content
    }
    
    # 2. 调用推送技能
    push_result = push_to_negative_screen(task_data)
    
    return push_result
```

## 🚀 使用示例

### 基本使用
```
# 任务完成后
任务完成，推送到负一屏
```

### 在脚本中使用
```bash
# 推送任务结果
python scripts/task_push.py --data task_result.json

# 使用配置文件中的授权码
python scripts/task_push.py --data task_result.json --config config.json

# 直接传递markdown内容
python scripts/task_push.py --name "新闻汇总" --content "# 新闻汇总\n\n今日热点..." --result "已完成"
```

### 在OpenClaw技能中集成
```python
# 在技能脚本中调用
from task_pusher import TaskPusher

def skill_main():
    # ... 执行任务逻辑 ...
    
    # 生成markdown格式的结果
    markdown_content = generate_markdown_result(data)
    
    # 任务完成后推送结果
    pusher = TaskPusher()
    result = pusher.push({
        "task_id": f"task_{int(time.time())}",
        "task_name": "AI新闻汇总",
        "task_result": "任务已完成",
        "task_content": markdown_content
    })
    
    return result
```

## ⚙️ 配置说明 - 混合配置系统

本技能使用混合配置系统，支持灵活的配置优先级：

### 配置优先级规则
1. **auth_code (授权码)**：
   - 优先使用 OpenClaw 全局配置
   - 如果没有设置，则使用本地配置（如果存在）
   - 如果都没有设置，则提示用户配置

2. **pushServiceUrl (推送URL)**：
   - 优先使用 OpenClaw 全局配置
   - 如果没有设置，则使用本地 config.json 中的 `pushServiceUrl` 配置
   - 如果都没有设置，则提示用户配置

3. **其他配置项**：使用本地 config.json 中的配置

### 配置加载顺序
1. 首先加载本地 config.json 文件中的基础配置
2. 然后检查 OpenClaw 全局配置
3. 根据优先级规则合并配置
4. 验证必需配置是否完整

### OpenClaw 全局配置命令

#### 1. 设置授权码
```bash
openclaw config set skills.entries.today-task.config.authCode YOUR_AUTH_CODE
```

#### 2. 设置推送URL
```bash
openclaw config set skills.entries.today-task.config.pushServiceUrl YOUR_PUSH_URL
```

#### 3. 查看技能配置
```bash
openclaw config get skills.entries.today-task
```

#### 4. 删除配置
```bash
# 删除授权码配置
openclaw config unset skills.entries.today-task.config.authCode

# 删除推送URL配置
openclaw config unset skills.entries.today-task.config.pushServiceUrl
```

### 配置示例
```bash
# 设置授权码
openclaw config set skills.entries.today-task.config.authCode KzLEP2FjYPg1

# 设置推送URL
openclaw config set skills.entries.today-task.config.pushServiceUrl https://distribution-drcn.ai.dbankcloud.cn/distribution/message/cloud/claw/msg/upload?ver=15.0.22.599
```

### 本地配置文件 (config.json)

其他配置项在技能目录的 `config.json` 文件中设置：

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

**配置优先级说明**：
1. **auth_code (授权码)**：优先使用 OpenClaw 全局配置，如果没有则使用本地配置
2. **pushServiceUrl (推送URL)**：优先使用 OpenClaw 全局配置，如果没有则使用本地 config.json 中的配置
3. **其他配置项**：使用本地 config.json 中的配置

### 🔑 授权码获取说明
**授权码是必填字段**，用于验证推送权限。如果未设置授权码或授权码无效，推送将失败。

**获取步骤**：
1. 从手机桌面右滑进入负一屏
2. 点击左上角头像
3. 进入"我的"页面，点击右上角设置图标
4. 选择"动态管理"
5. 点击"关联账号"
6. 找到"Claw智能体"并点击获取授权码

**推送URL说明**：
- 测试URL: `https://distribution-drcn.ai.dbankcloud.cn/distribution/message/cloud/claw/msg/upload?ver=15.0.22.599`
- 众测URL: `https://hiboardnjdev.hwcloudtest.cn:8081/distribution/message/cloud/claw/msg/upload?ver=15.0.22.200`
- 现网URL: `https://hiboardnjdev.hwcloudtest.cn:8081/distribution/message/cloud/claw/msg/upload?ver=15.0.22.300`

### 🔄 自动检测授权码功能
当用户在对话中提供授权码时，系统会自动检测并提示使用OpenClaw配置命令。

**支持格式**：
- "我的授权码是 aqvIVhhWz7ir"
- "使用授权码 FrF2e6Pwqvpz"
- "授权码: NWrU7qbN8vvx"
- "auth: HO4hza2l9MYy"

**工作原理**：
1. 系统会分析用户输入，检测是否符合授权码格式
2. 检测到授权码后，生成OpenClaw配置命令
3. 提示用户使用命令设置配置
4. 设置完成后，技能将使用新的授权码

**使用示例**：
```
用户：我的授权码是 aqvIVhhWz7ir
系统：检测到授权码: aqvi***
请使用以下OpenClaw命令设置授权码:
openclaw config set skills.entries.today-task.config.authCode aqvIVhhWz7ir
```

### 🔑 授权码获取说明
**授权码是必填字段**，用于验证推送权限。如果未设置授权码或授权码无效，推送将失败并显示以下提示：

```
📱 请您到负一屏 -> 我的页 -> 动态管理 -> 关联账号 -> 点击Claw智能体去获取授权码
```

**获取步骤**：
1. 打开负一屏应用
2. 进入"我的"页面
3. 找到"动态管理"
4. 点击"关联账号"
5. 找到"Claw智能体"并点击获取授权码

**常见授权码错误**：
- `0000900034` - 授权码无效
- `The authCode is invalid` - 授权码无效
- 授权码未设置 - 配置文件中缺少auth_code字段

### 🔄 自动更新授权码功能
**新增功能**：当用户在对话中提供授权码时，系统会自动检测并更新到配置文件中。

**支持格式**：
- "我的授权码是 aqvIVhhWz7ir"
- "使用授权码 FrF2e6Pwqvpz"
- "授权码: NWrU7qbN8vvx"
- "auth: HO4hza2l9MYy"

**工作原理**：
1. 系统会分析用户输入，检测是否符合授权码格式
2. 检测到授权码后，自动更新到配置文件
3. 更新完成后会显示确认信息
4. 后续推送将使用新的授权码

**授权码格式要求**：
- 长度：10-20个字符
- 组成：字母、数字，可能包含下划线或连字符
- 示例：`aqvIVhhWz7ir`, `FrF2e6Pwqvpz`, `NWrU7qbN8vvx`

**使用示例**：
```
用户：我的授权码是 aqvIVhhWz7ir
系统：✅ 检测到授权码，已更新到配置文件
```

### 配置验证
配置验证失败时会显示以下提示：
```
配置中缺少必需字段: auth_code, hiboards_url
请使用以下方式设置配置:
1. auth_code (授权码): 使用OpenClaw全局配置命令设置
   命令: openclaw config set skills.entries.today-task.config.authCode YOUR_AUTH_CODE
2. hiboards_url (推送URL): 使用OpenClaw全局配置命令设置
   命令: openclaw config set skills.entries.today-task.config.pushServiceUrl YOUR_PUSH_URL

其他配置项请在技能目录的config.json文件中设置。
```

## 📁 文件结构
```
push-task-to-negative-screen/
├── SKILL.md                    # 技能定义
├── README.md                   # 使用说明
├── config.json                 # 配置文件示例
├── scripts/
│   ├── task_push.py           # 主推送脚本
│   ├── task_pusher.py         # 推送器类
│   ├── config.py              # 配置管理
│   ├── logger.py              # 日志工具
│   ├── hiboards_client.py     # 负一屏客户端
│   └── simple_test.py         # 测试脚本
└── push_records/              # 推送记录目录（自动创建）
```

## 💡 设计优势
1. **格式统一**：所有任务使用相同的推送格式
2. **简单易用**：接口简单，易于集成
3. **灵活性强**：支持任何类型的任务结果
4. **配置方便**：支持配置文件
5. **错误处理完善**：详细的错误信息和建议
6. **记录完整**：保存完整的推送记录

## 🎨 Markdown内容生成建议
### 最佳实践
1. **使用标题层级**：合理使用#、##、###等标题
2. **列表展示**：使用-或*表示列表项
3. **代码块**：使用```包裹代码
4. **表格**：使用markdown表格格式
5. **分割线**：使用---作为分割线

### 示例模板
```markdown
# 任务名称

## 执行结果
✅ 任务已完成

## 详细内容
- 项目1: 结果描述
- 项目2: 结果描述
- 项目3: 结果描述

## 关键指标
| 指标 | 数值 | 状态 |
|------|------|------|
| 完成率 | 100% | ✅ |
| 用时 | 5分钟 | ⏱️ |

---

*生成时间: 2026-03-30 10:30:00*
```
