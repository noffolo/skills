---
name: soyoung-clinic-tools
slug: soyoung-clinic-tools
version: 2.1.4
description: 新氧青春诊所工具集，包含预约和项目查询百科、门店搜索等能力 | Soyoung clinic tools
tags: [Soyoung, soyoung, clinic, appointment, medical, beauty, healthcare, 新氧，诊所，预约，医美，整形，hospital]
license: MIT
---

# 新氧青春诊所工具集 Soyoung Clinic Tools — 技能集规格

**Name**: soyoung-clinic-tools  
**Version**: 2.1.4  
**License**: MIT

## Description

新氧青春诊所工具集，包含预约和项目查询百科、门店搜索等能力 | Soyoung clinic tools

## Skills（功能技能）

### 📅 appointment
> [skills/appointment/skill.yaml](skills/appointment/skill.yaml)

支持新氧门店查询、预约时间切片查询、提交/修改/取消/查询预约。

### 💉 project
> [skills/project/skill.yaml](skills/project/skill.yaml)

检索新氧项目知识库（原理、适应症、术后护理等）及 C 端商品价格信息。

## Setup（配置工具）

### 🔐 apikey
> [setup/apikey/skill.yaml](setup/apikey/skill.yaml)

不是用户直接使用的技能，而是 appointment 和 project 的共同前置条件。
负责 API Key 主人绑定、配置、查看、替换、删除，以及主人地理位置信息的保存与查询。
appointment 和 project 均通过 `depends_on: setup/apikey` 声明对其的依赖。

## Requirements

- `python3`（3.8+，必需）
- `bash`（入口兼容壳依赖）
- API Key：打开浏览器访问 `https://www.soyoung.com/loginOpenClaw`，登录后复制 API Key

## Workspace State

| 文件 | 说明 |
|------|------|
| `~/.openclaw/state/soyoung-clinic-tools/workspaces/<workspace_key>/api_key.txt` | 当前 workspace 的 API Key，权限 600 |
| `~/.openclaw/state/soyoung-clinic-tools/workspaces/<workspace_key>/binding.json` | 主人 Open ID、主人名、绑定时间等元信息 |
| `~/.openclaw/state/soyoung-clinic-tools/workspaces/<workspace_key>/location.json` | 主人位置 |
| `~/.openclaw/state/soyoung-clinic-tools/workspaces/<workspace_key>/pending/*.json` | 群聊预约审批单 |

## Security Model

- API Key 只能在与主人私聊中发送和配置
- 非主人群聊发起高风险预约操作时，必须先 `@主人`
- 高风险预约动作只包括：查询我的预约、提交预约、修改预约、取消预约
- 主人确认格式：`确认 #审批单号`
- 主人拒绝格式：`拒绝 #审批单号`

## Uninstall

```bash
# 1. 由主人在私聊中删除当前 workspace 的 API Key
bash ~/.openclaw/skills/soyoung-clinic-tools/setup/apikey/scripts/main.sh --delete-key --confirm --workspace-key <workspace_key> --chat-type direct --chat-id <chat_id> --sender-open-id <owner_open_id>

# 2. 禁用并移除 bootstrap hook
openclaw hooks disable soyoung-clinic-tools
rm -rf ~/.openclaw/hooks/soyoung-clinic-tools/

# 3. 删除 skill 目录
rm -rf ~/.openclaw/skills/soyoung-clinic-tools/
```

## Documentation

- 用户指南：[使用说明.md](使用说明.md)
- 版本历史：[CHANGELOG.md](CHANGELOG.md)
- 后端接口规范：[references/api-spec.md](references/api-spec.md)
