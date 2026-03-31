---
name: jiuma-free-meta-human
description: 九马AI免费数字人视频生成技能。使用九马AI API进行文本到数字人视频的生成，支持选择不同数字人形象和音色。当用户需要根据文本生成数字人视频时使用此技能。
---

# jiuma-free-meta-human Skill

这是一个免费的数字人视频生成工具，基于九马（Jiuma）平台。输入文本内容、数字人ID和音色ID，即可自动生成口型同步的数字人视频，生成时间通常在30分钟以内。

## 功能特性

- 📝 **文本转视频**：输入文字内容，自动生成数字人视频
- 👥 **多样数字人**：支持公共数字人和私有数字人形象
- 🎵 **多种音色**：提供丰富的声音选项
- 🎬 **口型同步**：自动实现唇形与语音的精准同步
- ⏱️ **快速生成**：视频生成时间在30分钟以内

## 安装要求

1. **Python版本**：3.10 或更高版本
2. **依赖库**：`requests` 库

## 配置文件

### 数字人ID参考（meta-human.json）
包含可用的公共数字人形象ID，用户也可以使用自己在九马官网的私有数字人ID。

### 音色ID参考（voice.json）
包含可用的公共音色ID，用户也可以使用自己在九马官网的私有音色ID。

## 参数说明

| 参数名              | 类型     | 是否必需 | 描述         |
|------------------|--------|--|----------------|
| `text`           | string | 是 | 文本内容，10-100字之间 |
| `human_id`       | string | 是 | 数字人ID（整数类型）    |
| `voice_id`       | string | 是 | 音色ID（整数类型）     |
| `human_video_id` | int    | 否 | 任务ID                |
| `access_key`     | string | 否 | 九马官网访问秘钥        |

## 使用指南

当用户需要生成数字人视频时，按照以下步骤操作：

### 1. 收集用户信息

**文本内容**：
- 提示用户输入10-100字之间的文本内容
- 示例：`text="大家好，我是AI助手，很高兴为您服务。"`

**数字人ID**：
- 提示用户输入数字人ID
- 选项：
  - 公共数字人ID（参考 meta-human.json）
  - 私有数字人ID（九马官网获取）
- 示例：`human_id=12345`

**音色ID**：
- 提示用户输入音色ID
- 选项：
  - 公共音色ID（参考 voice.json）
  - 私有音色ID（九马官网获取）
- 示例：`voice_id=67890`

**九马官网访问秘钥**
- 当用户使用私有音色ID或私有数字人ID时, 提示用户输入九马官网访问秘钥
- 实例：`access_key="12x54r0e993f9-u0fUZEoLFTWUt94b2eMrMWKppcNskEzu"`

### 2. 资源查找提示

如果用户不知道可用的数字人或音色ID，提供以下帮助：
- 引导用户查看 `meta-human.json` 和 `voice.json` 文件
- 提示访问九马官网获取私有资源
- 提供常见组合的示例
- 使用了私有ID就引导用户填写秘钥 `access_key`

### 3. 执行生成

- **公共id生成数字人**
```bash
# OpenClaw中使用
# 提交数字人生成任务
python3 ./skills/jiuma-free-meta-human/generate_video.py --action "create" --text "{{.text}}" --human_id {{.human_id}} --voice_id {{.voice_id}}

```
- **私有id生成数字人**
```bash
# OpenClaw中使用
# 提交数字人生成任务
python3 ./skills/jiuma-free-meta-human/generate_video.py --action "create" --text "{{.text}}" --human_id {{.human_id}} --voice_id {{.voice_id}} --access_key "{{.access_key}}"
```
- **查询公共id生成数字人的任务状态**
```bash
# OpenClaw中使用
# 查询任务状态, 建议10-15分钟后查询
 python3 ./skills/jiuma-free-meta-human/generate_video.py --action "check" --human_video_id {{.human_video_id}}
```

- **查询私有id生成数字人的任务状态**
```bash
# OpenClaw中使用
# 查询任务状态, 建议10-15分钟后查询
 python3 ./skills/jiuma-free-meta-human/generate_video.py --action "check" --human_video_id {{.human_video_id}} --access_key "{{.access_key}}"
```

## API说明

### 公共id生成数字人
- **URL**: `POST https://api.jiuma.com/DigitalHumanVideo/createDigitalHumanVideo`
- **参数**:
  - `action`: 操作类型, create表示创建任务; check表示查询任务
  - `text`: 文本内容
  - `human_id`: 数字人ID
  - `voice_id`: 音色ID
- **响应结果**:
  - `code`: 状态码, 200表示成功; 500表示失败
  - `error`: 错误信息
  - `human_video_id`: 任务ID

### 私有id生成数字人
- **URL**: `POST https://api.jiuma.com/DigitalHumanVideo/createDigitalHumanVideo`
- **参数**:
  - `action`: 操作类型, create表示创建任务; check表示查询任务
  - `text`: 文本内容
  - `human_id`: 数字人ID
  - `voice_id`: 音色ID
  - `access_key`: 九马官网访问秘钥
- **响应结果**:
  - `code`: 状态码, 200表示成功; 500表示失败
  - `error`: 错误信息
  - `human_video_id`: 任务ID

### 查询公共id生成数字人的任务状态
- **URL**: `POST https://api.jiuma.com/DigitalHumanVideo/digitalHumanVideoInfo`
- **参数**:
  - `action`: 操作类型, create表示创建任务; check表示查询任务
  - `human_video_id`: 任务ID
- **响应结果**:
  - `code`: 状态码, 200表示成功; 500表示失败
  - `message`: 返回信息
  - `status`: 任务状态; 17: "远程调度制作失败" | 13: "视频制作中" | 21: "已完成"
  - `video_url`: 视频下载链接

### 查询私有id生成数字人的任务状态
- **URL**: `POST https://api.jiuma.com/DigitalHumanVideo/digitalHumanVideoInfo`
- **参数**:
  - `action`: 操作类型, create表示创建任务; check表示查询任务
  - `human_video_id`: 任务ID
  - `access_key`: 九马官网访问秘钥
- **响应结果**:
  - `code`: 状态码, 200表示成功; 500表示失败
  - `message`: 返回信息
  - `status`: 任务状态; 17: "远程调度制作失败" | 13: "视频制作中" | 21: "已完成"
  - `video_url`: 视频下载链接

## 交互流程优化

### 智能引导
1. **第一步**：询问用户需要生成的文本内容
2. **第二步**：询问数字人ID，同时提供获取方式
3. **第三步**：询问音色ID，提供参考选项
4. **第四步**：确认所有参数，开始生成

### 错误预防
- 文本字数检查（10-100字）
- ID格式验证（确保是整数）
- 生成前二次确认

## 最佳实践

### 推荐配置
- **短视频制作**：使用30-50字文本
- **公共数字人**：优先使用已验证的公共ID
- **常用音色**：选择清晰度高的音色

### 注意事项
1. 生成过程可能需要30分钟左右，请耐心等待
2. 确保网络连接稳定
3. 生成结果会自动保存到指定目录
4. 如需中断生成，请使用适当的中断方式

## 故障排除

| 问题 | 可能原因 | 解决方案 |
|------|----------|----------|
| 文本字数不足 | 文本少于10字 | 添加更多内容 |
| ID格式错误 | 非整数或格式不正确 | 检查ID格式 |
| 生成超时 | 网络或服务器问题 | 稍后重试 |
| 音视频不同步 | 文本过长或特殊字符 | 简化文本内容 |

## 扩展功能建议

未来可考虑添加：
- 批量生成支持
- 自定义背景功能
- 多语言支持
- 视频格式选择
