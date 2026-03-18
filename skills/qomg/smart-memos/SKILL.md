---
name: smart-memos
description: |
  智能备忘录管理系统，支持从 macOS 备忘录导入（PDF/Markdown/HTML/TXT/JSON）、
  智能自动分类、语义搜索、快速记录、编辑修改和归档管理。
  
  使用场景：
  - 用户说"帮我记录备忘录"、"记个笔记"、"添加备忘"
  - 用户说"搜索备忘录"、"查找笔记"、"回忆一下"
  - 用户说"导入备忘录"、"从备忘录导入"、"导出备忘录"
  - 用户说"查看分类"、"备忘录统计"、"整理备忘录"
  - 用户说"编辑备忘录"、"修改备忘录"、"更新备忘录"
  - 用户需要管理个人笔记、待办事项、灵感记录
---

# 智能备忘录系统 (Smart Memos)

智能备忘录管理系统，支持多种格式导入、自动分类、语义搜索、快速记录和编辑修改。

## 功能特性

- 📥 **多格式导入**: PDF, Markdown, HTML, TXT, JSON
- 🏷️ **智能分类**: 自动分类到工作、学习、生活等 12+ 类别
- 🔍 **语义搜索**: 关键词搜索，支持分类筛选
- ⚡ **快速记录**: CLI 和 API 快速添加
- ✏️ **编辑修改**: 支持修改标题、内容、分类、标签
- 🗂️ **归档管理**: 支持删除和归档
- 📊 **统计分析**: 分类统计和趋势分析
- 🔖 **标签支持**: Markdown 导入时自动识别 `#标签`

## 使用方法

### 快速记录

```python
from scripts.memos import SmartMemoSystem

memos = SmartMemoSystem()
memo_id = memos.add_memo(
    title="会议记录",
    content="下午3点项目进度会议",
    category="工作",
    tags=["会议", "项目"]
)
```

### 搜索备忘录

```python
# 关键词搜索
results = memos.search_memos("会议")

# 分类筛选
results = memos.search_memos("项目", category="工作")
```

### 编辑备忘录

```python
# 更新备忘录
memos.update_memo(
    memo_id=1,
    title="新标题",
    content="新内容",
    category="工作",
    tags=["标签1", "标签2"]
)
```

### 导入备忘录

```python
# 从 PDF 导入
count = memos.import_from_notes_app("~/Downloads/备忘录.pdf")

# 从 Markdown 导入（自动识别 #标签）
count = memos.import_from_notes_app("~/Downloads/笔记.md")
```

### 删除/归档

```python
# 删除备忘录
memos.delete_memo(memo_id)

# 归档备忘录
memos.archive_memo(memo_id)
```

## 自动分类规则

| 分类 | 关键词 | 权重 |
|------|--------|------|
| 工作 | 会议、项目、任务、deadline、进度、客户、需求 | 1.5x |
| 学习 | 教程、课程、学习、笔记、阅读、书籍、知识 | 1.5x |
| 生活 | 购物、超市、买菜、做饭、家务、缴费、快递 | 1.0x |
| 旅行 | 机票、酒店、景点、攻略、行程、旅游、签证 | 1.5x |
| 财务 | 收入、支出、预算、投资、理财、股票、基金 | 1.5x |
| 灵感 | 想法、创意、灵感、构思、设计、方案、计划 | 1.0x |
| 待办 | todo、待办、待处理、待确认、提醒、记得 | 2.0x |
| 联系人 | 电话、邮箱、地址、联系人、名片、微信 | 1.5x |
| 技术 | 代码、编程、开发、API、框架、工具、Git | 1.5x |
| 娱乐 | 电影、音乐、游戏、综艺、追剧、推荐 | 1.0x |
| 健康 | 医院、医生、健康、体检、药品、运动 | 1.5x |
| 美食 | 餐厅、菜谱、食物、美食、烹饪、料理 | 1.0x |

## CLI 使用

脚本支持命令行操作：

```bash
# 添加备忘录
python scripts/memos.py add "标题" "内容" [分类] [标签]

# 列出备忘录（显示ID）
python scripts/memos.py list [分类] [数量]

# 查看详情
python scripts/memos.py view <ID>

# 编辑备忘录
python scripts/memos.py edit <ID> --title "新标题" --content "新内容" --category "分类" --tags "标签1,标签2"

# 搜索备忘录
python scripts/memos.py search "关键词" [分类]

# 导入文件（支持 #标签）
python scripts/memos.py import <文件路径>

# 删除/归档
python scripts/memos.py delete <ID>
python scripts/memos.py archive <ID>

# 统计
python scripts/memos.py categories
python scripts/memos.py stats
```

## Markdown 标签格式

导入 Markdown 文件时，支持 `#标签名` 格式：

```markdown
# 项目会议记录 #工作 #会议

今天下午3点召开项目进度会议 #紧急
- 前端页面开发进度 80% #前端
- 后端API接口已完成 #后端
```

导入后会自动提取标签：`工作, 会议, 紧急, 前端, 后端`

## 数据存储

- 数据库: `~/.qclaw/workspace/memos/memos.db`
- 导出目录: `~/.qclaw/workspace/memos/`

## 依赖

- Python 3.7+
- SQLite3 (内置)
- 可选: `pdfplumber` 或 `PyPDF2` (PDF 导入)

## 版本历史

### v1.2.0
- 新增编辑修改功能
- 优化分类算法（增加权重机制）
- 支持 Markdown 标签导入
- list/search 显示 ID

### v1.1.0
- 新增 PDF 和 Markdown 导入支持
- 优化 PDF 文本提取
- 改进 Markdown 解析

### v1.0.0
- 基础功能：添加、搜索、列表、分类
- 支持从 macOS Notes 导入
- 智能自动分类
- 语义搜索功能
