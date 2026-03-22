# 学术论文评审 Skill

[English](README.md)

这是一个可复用的 agent skill，用于对**中国管理类硕士论文**进行多轮评审。

## 概述

本仓库封装了一份可复用的论文评审 skill，适用于以下 agent / prompt 生态：

- OpenCode
- OpenClaw
- Claude Code
- 其他支持 Markdown 技能文件的系统

该 skill 主要面向**中国管理类硕士论文**，尤其适用于：

- **MBA**
- **MEM**
- **MPA**

同时也可用于其他结构相近的专业型、应用型硕士论文，例如管理学、公共管理、工程管理等方向。

它采用 **3 轮评审策略**：

1. 宏观结构审查
2. 分章节深度审查
3. 跨章节一致性审查

输出风格为**严格但可执行**的中文修改意见。

## 多轮审阅支持

支持，而且这是这份 skill 的核心能力之一。

- **第 1 轮：** 宏观结构与整体逻辑审查
- **第 2 轮：** 分章节深度审查
- **第 3 轮：** 跨章节一致性审查
- **迭代复审：** 如果目录中已有 `review_results.md`，skill 会把之前的问题作为核查对象，判断是已修改、部分修改还是未修改

因此它不仅适合第一次通读评审，也适合**论文修改后的连续复审、多轮迭代审阅**。

## 文件说明

- `SKILL.md` — 标准主入口技能文件，带有元数据 frontmatter
- `skill.json` — 发布用元数据文件
- `.gitignore` — 本地输出与临时文件忽略规则

## 适用场景

该 skill 适用于能够加载 Markdown 技能文件、提示词文件、命令文件或工作流说明文件的 agent 系统。

推荐适用范围：

- MBA 论文
- MEM 论文
- MPA 论文
- 其他管理学、公共管理、工程管理及结构相近的应用型硕士论文

典型用途：

- 审阅 `.docx` 论文初稿
- 对修改后的论文进行复审
- 生成结构化的 `review_results.md`

## 使用方式

由于不同 agent 框架的技能目录结构不同，可以采用以下方式：

### 方式 1：直接使用文件

直接让你的 agent 系统读取 `SKILL.md`。

### 方式 2：复制到技能目录

将整个文件夹复制到目标框架的本地 skills / prompts 目录，并按该框架的约定注册使用。

#### Claude Code

个人目录安装：

```bash
mkdir -p ~/.claude/skills/academic-thesis-review
cp -r . ~/.claude/skills/academic-thesis-review
```

项目内安装：

```bash
mkdir -p .claude/skills/academic-thesis-review
cp -r . .claude/skills/academic-thesis-review
```

#### OpenClaw

建议的全局安装方式：

```bash
mkdir -p ~/.openclaw/skills/academic-thesis-review
cp -r . ~/.openclaw/skills/academic-thesis-review
```

#### OpenCode / 兼容 Prompt Loader

将 `SKILL.md` 作为导入的 Markdown 技能文件使用。

### 方式 3：引用 GitHub 仓库

将该目录上传到 GitHub 后，可在支持远程仓库或远程 Markdown 资源的 agent 平台中直接引用。

## 建议触发语句

- 审阅论文
- review thesis
- 论文评审
- 帮我看看论文
- 修改后再看看

## 输入要求

- `.docx` 格式论文文件
- 可用的 Python 环境（用于提取正文文本）
- 可选：已有的 `review_results.md`，用于触发迭代审阅模式

## 输出结果

- Markdown 评审报告
- 推荐输出文件名：`review_results.md`

## 仓库信息

- GitHub 作者主页：https://github.com/wmpluto
- 仓库地址：`https://github.com/wmpluto/academic-thesis-review-skill`
- 首页 / 文档地址：`https://github.com/wmpluto/academic-thesis-review-skill`

## 发布说明

- `SKILL.md` 是当前包的标准主文件，更适合遵循 Agent Skills 风格的生态。
- 在 Windows 下，`SKILL.md` 与 `skill.md` 这种仅大小写不同的双文件名无法稳定共存，因此本包统一使用 `SKILL.md`。
- `skill.json` 是通用发布元数据，不代表所有平台都强制要求该文件。
- 如果未来你有单独的文档站点，可以再把首页地址替换成独立 URL。

## 备注

- 如果后续要适配某个特定平台的严格 manifest 格式，建议新增对应文件，而不是替换 `SKILL.md`。
