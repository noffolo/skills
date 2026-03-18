# Smart Memos

智能备忘录管理系统 - 一个支持多格式导入、智能分类、语义搜索和编辑修改的备忘录工具。

## 安装

### 方式一：作为 OpenClaw Skill 安装

1. 下载 `smart-memos.skill` 文件
2. 在 OpenClaw 中安装 Skill
3. 即可通过 AI 助手使用

### 方式二：独立使用

```bash
# 克隆或下载代码
cd smart-memos/scripts

# 运行（无需安装依赖，纯 Python 标准库）
python memos.py
```

## 依赖

- Python 3.7+
- SQLite3（Python 内置）

### 可选依赖（PDF 导入）

```bash
# 推荐：pdfplumber（效果更好）
pip install pdfplumber

# 或：PyPDF2
pip install PyPDF2

# 或：系统命令 pdftotext（macOS）
brew install poppler
```

## 快速开始

```bash
# 添加备忘录
python memos.py add "会议记录" "下午3点项目进度会议" "工作"

# 列出备忘录
python memos.py list

# 查看详情
python memos.py view 1

# 编辑备忘录
python memos.py edit 1 --title "新项目会议" --tags "紧急"

# 搜索
python memos.py search "会议"
```

## 功能特性

- 📥 多格式导入（PDF/Markdown/HTML/TXT/JSON）
- 🏷️ 智能自动分类（12+ 类别）
- 🔍 语义搜索
- ✏️ 编辑修改
- 🔖 标签支持
- 🗂️ 归档管理

## 文档

详见 `SKILL.md`

## 许可证

MIT
