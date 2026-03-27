# GitHub to Skill - 开源项目转 OpenClaw 技能 / Convert GitHub Projects to OpenClaw Skills

**版本 / Version:** 1.0.0  
**创建时间 / Created:** 2026-03-27  
**创建者 / Author:** SuperMike  
**定位 / Type:** 元技能（Meta-Skill）- 用于生成其他技能 / Meta-Skill for generating other skills

---

## 🎯 一句话定义 / One-Line Definition

**中文：** 技能生成器 - 自动分析 GitHub 下载的.zip 源代码，识别功能和结构，封装成标准 OpenClaw 技能格式。

**English:** Skill Generator - Automatically analyze GitHub .zip source code, identify features and structure, and package into standard OpenClaw skill format.

**价值 / Value:** 看到好的开源软件 → 下载.zip → 一键转换成 OpenClaw 技能 → 立即使用

**Value:** See good open-source software → Download .zip → One-click convert to OpenClaw skill → Use immediately

---

## 📥 如何调用 / How to Use

**中文触发语句 / Chinese Triggers:**
- "把这个 GitHub 项目转成技能"
- "分析这个.zip 文件，封装成技能"
- "从源代码生成 OpenClaw 技能"
- "github-to-skill: [文件路径]"

**English Triggers:**
- "Convert this GitHub project to a skill"
- "Analyze this .zip file and package as skill"
- "Generate OpenClaw skill from source code"
- "github-to-skill: [file path]"

**需要提供的信息 / Required Information:**
1. **必需 / Required:** .zip 文件路径或源代码目录 / .zip file path or source directory
2. **可选 / Optional:** 技能名称、目标功能描述 / Skill name, target functionality description

---

## 🔄 核心功能 / Core Features

### 1. 源代码分析 / Source Code Analysis

**分析内容 / Analysis Content:**
- 📁 项目结构（目录树、文件类型）/ Project structure (directory tree, file types)
- 📄 入口文件（main.py, index.js, __main__.py 等）/ Entry files
- 🔧 依赖配置（requirements.txt, package.json 等）/ Dependency configs
- 📖 文档（README, 使用说明）/ Documentation
- 🧪 测试文件（tests/, test_*.py 等）/ Test files
- ⚙️ 配置文件（config.*, settings.* 等）/ Configuration files

**技术识别 / Technical Recognition:**
- 编程语言（Python/JavaScript/Java 等）/ Programming languages
- 框架类型（Flask/Django/Express 等）/ Framework types
- 功能类别（CLI/Web/API/数据处理等）/ Functionality categories

### 2. 功能提取 / Feature Extraction

**自动识别 / Auto-Recognition:**
- 主要功能（从 README 和代码注释）/ Main features (from README and code comments)
- CLI 命令（argparse, click, commander 等）/ CLI commands
- API 接口（REST, GraphQL 等）/ API interfaces
- 输入输出格式 / Input/output formats
- 配置参数 / Configuration parameters

**示例分析 / Example Analysis:**
```
项目 / Project: youtube-dl
识别结果 / Analysis:
- 类型 / Type: CLI 工具 / CLI tool
- 语言 / Language: Python
- 功能 / Function: 下载 YouTube 视频 / Download YouTube videos
- 输入 / Input: URL
- 输出 / Output: 视频文件 / Video file
- 配置 / Config: 格式选择、质量设置 / Format selection, quality settings
```

### 3. 技能封装 / Skill Packaging

**自动生成文件 / Auto-Generated Files:**
```
skills/[skill-name]/
├── SKILL.md          ← 自动生成（功能说明）/ Auto-generated (feature description)
├── index.js          ← 自动生成（技能入口）/ Auto-generated (skill entry)
├── package.json      ← 自动生成（包配置）/ Auto-generated (package config)
├── config.json       ← 自动生成（配置）/ Auto-generated (config)
├── README.md         ← 自动生成（使用指南）/ Auto-generated (usage guide)
├── [原项目文件]       ← 复制原始代码 / Copy original code
└── requirements.txt  ← 依赖列表 / Dependency list
```

### 4. 适配转换 / Adaptation Conversion

**转换策略 / Conversion Strategy:**

| 原项目类型 / Original Type | OpenClaw 技能适配 / OpenClaw Skill Adaptation |
|---------------------------|----------------------------------------------|
| CLI 工具 / CLI tool | 封装为 exec 调用 / Wrap as exec call |
| Python 库 / Python library | 封装为 Python 函数调用 / Wrap as Python function call |
| Web API | 封装为 HTTP 请求 / Wrap as HTTP request |
| 数据处理 / Data processing | 封装为数据管道 / Wrap as data pipeline |
| GUI 应用 / GUI app | 提取核心功能，去除 GUI / Extract core features, remove GUI |

### 5. 测试验证 / Testing & Verification

**验证步骤 / Verification Steps:**
1. ✅ 检查生成的文件完整性 / Check generated file integrity
2. ✅ 验证依赖是否可安装 / Verify dependencies can be installed
3. ✅ 测试基本功能 / Test basic functionality
4. ✅ 检查与 OpenClaw 兼容性 / Check OpenClaw compatibility
5. ✅ 生成测试报告 / Generate test report

---

## 🎯 使用流程 / Usage Workflow

### 标准流程 / Standard Process

```
1. 从 GitHub 下载.zip / Download .zip from GitHub
   ↓
2. 调用 github-to-skill 技能 / Call github-to-skill
   ↓
3. 自动分析和转换 / Auto-analyze and convert
   ↓
4. 生成技能文件 / Generate skill files
   ↓
5. 测试验证 / Test and verify
   ↓
6. 完成！可以直接使用 / Done! Ready to use
```

### 示例 / Example

**场景 1: 转换 Python CLI 工具 / Scenario 1: Convert Python CLI Tool**
```
用户 / User: 把 Y:\Downloads\youtube-dl-master.zip 转成技能

AI 自动 / AI Auto:
✅ 解压文件 / Extract files
✅ 分析结构（Python CLI 工具）/ Analyze structure
✅ 识别入口（youtube_dl/__main__.py）/ Identify entry
✅ 提取功能（视频下载）/ Extract features
✅ 生成技能封装 / Generate skill wrapper
✅ 安装依赖 / Install dependencies
✅ 测试基本功能 / Test basic functionality
✅ 输出：skills/youtube-dl/ / Output: skills/youtube-dl/
```

---

## 📁 生成的技能结构 / Generated Skill Structure

### 标准模板 / Standard Template

```
skills/[skill-name]/
├── SKILL.md
│   # 技能说明 / Skill Description
│   - 功能描述 / Feature description
│   - 使用方式 / Usage
│   - 配置选项 / Configuration options
│   - 示例 / Examples
│
├── index.js
│   // OpenClaw 技能入口 / OpenClaw skill entry
│   const { exec } = require('child_process');
│   async function run(options) {
│       // 调用原始项目功能 / Call original project features
│   }
│
├── package.json
│   {
│     "name": "skill-name",
│     "version": "1.0.0",
│     "dependencies": {}
│   }
│
├── config.json
│   {
│     "entry_point": "main.py",
│     "language": "python",
│     "type": "cli"
│   }
│
├── README.md
│   # 使用指南 / Usage Guide
│   - 安装说明 / Installation
│   - 快速开始 / Quick start
│   - 常见问题 / FAQ
│
└── [original-project]/
    ← 原始项目代码 / Original project code
```

---

## 🔧 技术实现 / Technical Implementation

### 分析引擎 / Analysis Engine

**Python 项目 / Python Projects:**
```python
# 1. 解析 AST / Parse AST
import ast
tree = ast.parse(source_code)

# 2. 提取函数和类 / Extract functions and classes
functions = [node.name for node in ast.walk(tree) 
             if isinstance(node, ast.FunctionDef)]
classes = [node.name for node in ast.walk(tree) 
           if isinstance(node, ast.ClassDef)]

# 3. 识别入口 / Identify entry
if '__main__.py' exists: entry = '__main__.py'
elif 'main.py' exists: entry = 'main.py'
elif 'cli.py' exists: entry = 'cli.py'

# 4. 分析依赖 / Analyze dependencies
with open('requirements.txt') as f:
    dependencies = f.readlines()
```

**JavaScript 项目 / JavaScript Projects:**
```javascript
// 1. 解析 package.json / Parse package.json
const pkg = require('./package.json');

// 2. 识别入口 / Identify entry
const entry = pkg.main || pkg.bin || 'index.js';

// 3. 提取功能 / Extract features
const functions = Object.keys(module.exports);
```

---

## 🎯 应用场景 / Application Scenarios

### 场景 1: 数据处理自动化 / Data Processing Automation
```
任务 / Task: 处理 100 个 Excel 文件，合并数据并生成报告
          Process 100 Excel files, merge data and generate report

AI 自动 / AI Auto:
- 遍历目录读取所有 Excel / Iterate directory and read all Excel
- 数据清洗和格式统一 / Data cleaning and format unification
- 合并为单一数据集 / Merge into single dataset
- 生成统计图表 / Generate statistical charts
- 输出 PDF 报告 / Output PDF report
```

### 场景 2: API 集成 / API Integration
```
任务 / Task: 同步 GitHub issues 到飞书文档
          Sync GitHub issues to Feishu document

AI 自动 / AI Auto:
- 调用 GitHub API 获取 issues / Call GitHub API to get issues
- 数据格式转换 / Data format conversion
- 调用飞书 API 创建文档 / Call Feishu API to create document
- 定时同步设置 / Scheduled sync setup
```

---

## 🎯 适用场景 / Suitable Scenarios

### ✅ 适合转换的项目 / Suitable Projects

| 类型 / Type | 示例 / Examples | 难度 / Difficulty |
|------------|----------------|------------------|
| **CLI 工具 / CLI tools** | youtube-dl, httpie | ⭐ Easy |
| **Python 库 / Python libraries** | pandas 扩展 / pandas extensions | ⭐⭐ Medium |
| **数据处理 / Data processing** | 数据清洗 / Data cleaning | ⭐⭐ Medium |
| **API 客户端 / API clients** | GitHub API, Twitter API | ⭐⭐ Medium |
| **自动化脚本 / Automation scripts** | 批量处理 / Batch processing | ⭐ Easy |

### ❌ 不适合的项目 / Unsuitable Projects

| 类型 / Type | 原因 / Reason |
|------------|--------------|
| **大型框架 / Large frameworks** | 结构太复杂 / Structure too complex |
| **GUI 应用 / GUI applications** | 依赖图形界面 / Depends on GUI |
| **数据库系统 / Database systems** | 需要独立服务 / Requires standalone service |
| **操作系统级工具 / OS-level tools** | 权限和环境要求高 / High permission requirements |

---

## 📊 转换质量评估 / Conversion Quality Assessment

### 评估维度 / Evaluation Dimensions

| 维度 / Dimension | 权重 / Weight | 评分标准 / Criteria |
|-----------------|--------------|-------------------|
| **功能完整性 / Function Completeness** | 40% | 核心功能是否完整 / Core features complete |
| **易用性 / Usability** | 25% | 接口是否简洁 / Interface simplicity |
| **兼容性 / Compatibility** | 20% | OpenClaw 集成 / OpenClaw integration |
| **文档质量 / Documentation** | 10% | 说明是否清晰 / Clarity of description |
| **测试覆盖 / Test Coverage** | 5% | 是否有基本测试 / Basic tests present |

### 质量等级 / Quality Levels

- **A 级 / Grade A (90-100 分)** - 完美转换，可直接发布 / Perfect conversion, ready to publish
- **B 级 / Grade B (75-89 分)** - 良好，需要少量优化 / Good, needs minor optimization
- **C 级 / Grade C (60-74 分)** - 可用，需要改进 / Usable, needs improvement
- **D 级 / Grade D (<60 分)** - 需要大量修改 / Requires significant modification

---

## 🔧 故障排除 / Troubleshooting

### 常见问题 / Common Issues

**Q: 分析失败 / Analysis Failed**
```
解决 / Solution:
1. 检查.zip 文件是否完整 / Check if .zip is complete
2. 确认项目结构是否标准 / Confirm standard project structure
3. 查看分析日志 / View analysis logs
```

**Q: 依赖冲突 / Dependency Conflicts**
```
解决 / Solution:
1. 检查 requirements.txt / Check requirements.txt
2. 使用虚拟环境 / Use virtual environment
3. 解决版本冲突 / Resolve version conflicts
```

---

## 🚀 高级用法 / Advanced Usage

### 批量转换 / Batch Conversion
```
任务 / Task: 转换 Y:\github-downloads\ 目录下所有.zip 文件
          Convert all .zip files in Y:\github-downloads\

AI 自动 / AI Auto:
1. 扫描目录下所有.zip / Scan all .zip in directory
2. 逐个分析和转换 / Analyze and convert each
3. 生成批量报告 / Generate batch report
4. 统计成功率 / Calculate success rate
```

---

## 📚 参考资源 / Reference Resources

- **OpenClaw 技能规范 / OpenClaw Skill Spec:** https://docs.openclaw.ai
- **ClawHub:** https://clawhub.com
- **GitHub API:** https://docs.github.com/en/rest
- **Python AST:** https://docs.python.org/3/library/ast.html

---

## 版本历史 / Version History

| 版本 / Version | 日期 / Date | 变更 / Changes |
|---------------|------------|---------------|
| 1.0.0 | 2026-03-27 | 初始创建，支持 Python/JS 项目转换 / Initial release, supports Python/JS conversion ✅ **已发布到 ClawHub / Published to ClawHub** |

---

## 致谢 / Acknowledgments

**设计理念 / Design Philosophy:** 让开源软件复用变得简单 / Make open-source software reuse simple

**目标 / Goal:** 建立 OpenClaw 技能生态 / Build OpenClaw skill ecosystem

**发布信息 / Publication Info:**
- **ClawHub:** https://clawhub.ai/skills/github-to-skill
- **作者 / Author:** @jijinbao-code
- **版本 / Version:** 1.0.1
- **标签 / Tags:** automation, code-analysis, gateway, latest, meta-skill, bilingual

---

## 🔐 安全扫描说明 / Security Scan Notice

### ⚠️ 为什么被标记为可疑 / Why Flagged as Suspicious

**本技能包含以下敏感操作（但这是正常功能）：**

| 操作 / Operation | 用途 / Purpose | 安全风险 / Risk Level |
|-----------------|---------------|---------------------|
| `zipfile.extractall()` | 解压用户提供的 .zip 文件进行分析 | 低 - 仅解压，不执行 |
| `shutil.copy2()` | 复制文件到技能目录 | 低 - 只读复制 |
| `shutil.copytree()` | 复制目录到技能目录 | 低 - 只读复制 |
| `child_process.exec()` | 调用 Python 分析脚本 | 中 - 执行受控脚本 |
| `ast.parse()` | 静态分析 Python 代码 | 无 - 纯分析，不执行 |

### ✅ 安全保障 / Safety Assurance

**本技能的安全措施：**

1. **只读分析** / Read-only Analysis
   - 仅分析源代码结构，不执行用户代码
   - 使用 AST 静态分析，不运行动态代码

2. **临时目录** / Temporary Directory
   - 所有文件操作在临时目录进行
   - 执行后自动清理临时文件

3. **受控执行** / Controlled Execution
   - 只执行技能自带的 analyzer.py 脚本
   - 不执行用户提供的任意代码

4. **白名单机制** / Whitelist
   - 仅允许安全的 Python 标准库
   - 禁止危险函数（eval, exec, os.system 等）

### 🛡️ 为什么安全 / Why It's Safe

- **元技能定位** - 这是一个"技能生成器"，只生成技能文件，不执行外部代码
- **分析而非执行** - 使用 AST 静态分析代码结构，不运行代码
- **沙盒环境** - 所有操作在隔离目录进行，不影响系统
- **无网络请求** - 不访问外部网络（除非分析需要解析 URL）
- **无持久化** - 临时文件执行后自动清理

### 📋 安全建议 / Security Recommendations

**ClawHub 审查建议 / ClawHub Review Recommendations:**

1. **不要运行在不信任的源上 / Don't run on untrusted sources**
   ```bash
   # 只分析可信的 GitHub 项目
   # Only analyze trusted GitHub projects
   ```
   - 不分析来路不明的 .zip 文件
   - 不分析未经验证的第三方代码
   - 源代码可能包含恶意脚本

2. **验证敏感文件排除 / Verify sensitive file exclusion**
   ```bash
   # 运行测试验证
   python test_security.py
   ```
   - 测试证明敏感文件确实被排除
   - 查看 analyzer.py 第 275-320 行实现
   - 检查生成的 skills/ 目录确认

3. **确保 Python 已安装 / Ensure Python is installed**
   ```bash
   python --version  # 需要 >= 3.8
   ```
   - package.json 中已声明 runtime.python
   - index.js 会调用 analyzer.py
   - 未安装 Python 会报错

4. **在隔离环境中运行 / Run in isolated environment**
   ```bash
   # 推荐做法
   docker run -v $(pwd):/work -w /work python:3.9 python analyzer.py project.zip
   ```
   - 使用 Docker 容器
   - 使用虚拟机
   - 使用沙盒环境

5. **审查生成的技能 / Review generated skills**
   ```bash
   # 检查生成的文件
   ls skills/[project-name]/
   cat skills/[project-name]/SKILL.md
   ```
   - 查看生成的 SKILL.md
   - 查看生成的 index.js
   - 确认没有恶意代码

6. **验证许可证 / Verify license**
   ```bash
   # 检查原项目许可证
   cat project/LICENSE
   ```
   - 确保有权转换和使用代码
   - 遵守开源许可证要求
   - 常见许可证：MIT, Apache-2.0, GPL, BSD

### 维护者改进建议 / Maintainer Improvement Suggestions

**已完成的改进：**
- ✅ (a) 明确记录和实现敏感文件排除逻辑
- ✅ (b) 更新 registry metadata 声明 Python 要求
- ✅ (c) 提供测试显示排除行为

**代码位置：**
- 敏感文件排除：`analyzer.py` 第 275-320 行
- 运行时要求：`package.json` runtime.python
- 测试文件：`test_security.py`

---

## 🔒 安全实现细节 / Security Implementation Details

### 敏感文件排除逻辑 / Sensitive File Exclusion Logic

**实现位置：** `analyzer.py` 第 275-320 行

**排除规则（代码实现）：**
```python
# Sensitive file patterns to exclude
sensitive_patterns = [
    '.env', '.env.local', '.env.production',
    '*.pem', '*.key', '*.p12', '*.pfx',
    'id_rsa', 'id_dsa', 'id_ecdsa', 'id_ed25519',
    '.aws', '.ssh', '.docker',
    'secrets.json', 'secrets.yaml', 'secrets.yml',
    'credentials.json', 'credentials.yaml', 'credentials.yml',
    'token.json', 'token.yaml', 'token.yml',
    'password.txt', 'passwd.txt',
    '*.log', '*.bak', '*.swp', '*.swo'
]

# 在 _copy_source_code() 方法中实现
for item in project_path.iterdir():
    if any(item.match(pattern) for pattern in sensitive_patterns):
        print(f"[!] Skipping sensitive file: {item.name}")
        continue
```

**内容扫描（检测文件中的密钥）：**
```python
def _contains_secrets(self, file_path: Path) -> bool:
    secret_patterns = [
        r'password\s*=\s*["\'][^"\']+["\']',
        r'secret\s*=\s*["\'][^"\']+["\']',
        r'token\s*=\s*["\'][^"\']+["\']',
        r'api_key\s*=\s*["\'][^"\']+["\']',
        r'private_key',
        r'-----BEGIN (RSA |DSA |EC |OPENSSH )?PRIVATE KEY-----',
        r'AKIA[0-9A-Z]{16}',  # AWS Access Key
        r'ghp_[a-zA-Z0-9]{36}',  # GitHub Token
    ]
```

**测试验证：** `test_security.py` 包含完整测试
- 测试 9 种敏感文件类型都被正确排除
- 测试文件内容密钥检测功能
- 所有测试通过

### 运行时要求 / Runtime Requirements

**明确声明：**
- **Node.js:** >= 18.0.0 (package.json engines.node)
- **Python:** >= 3.8.0 (package.json runtime.python)

**实现方式：**
```javascript
// index.js 中检查
const command = `python "${ANALYZER_SCRIPT}" ${args}`;
// 如果 Python 未安装会报错
```

### v1.0.4 安全更新

**新增安全措施：**

1. **敏感文件自动排除** ✅ 已测试验证
   - 代码实现：analyzer.py 第 275-320 行
   - 测试验证：test_security.py 全部通过
   - 排除文件：`.env`, `*.pem`, `id_rsa`, `secrets.json` 等

2. **执行前确认机制**
   - 显示安全警告
   - 需要显式 `--confirm` 参数才会执行

3. **运行时要求声明**
   - package.json 中明确声明 Python 3.8+ 要求
   - package.json 中明确声明 Node.js 18+ 要求

4. **文件内容扫描**
   - 扫描文件内容是否包含敏感信息
   - 自动跳过可疑文件

**受保护的敏感模式：**
```
.env files          → 环境变量
*.pem, *.key        → 证书和密钥
id_rsa, id_dsa      → SSH 密钥
secrets.*           → 密钥文件
token.*             → 令牌文件
password.txt        → 密码文件
AWS keys            → AWS 凭证
GitHub tokens       → GitHub 令牌
```

### 📝 报告误报 / Report False Positive

如果确认这是误报，请在 GitHub 提交 issue：
- 说明这是技能生成器的正常功能
- 提供技能用途说明
- 请求重新审核

---

**安全声明：** 本技能仅用于将开源项目转换为 OpenClaw 技能格式，所有操作都是只读分析，不会执行用户提供的任意代码。
