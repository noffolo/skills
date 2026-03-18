# Smart Memos 贡献指南

## 开发环境设置

```bash
# 克隆仓库
git clone <repo-url>
cd smart-memos

# 创建虚拟环境（可选）
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

## 运行测试

```bash
python tests/test_memos.py
```

## 项目结构

```
smart-memos/
├── SKILL.md              # Skill 定义文件（OpenClaw 使用）
├── README.md             # 用户文档
├── package.json          # 项目元数据
├── requirements.txt      # Python 依赖
├── LICENSE               # 许可证
├── scripts/              # 核心代码
│   └── memos.py         # 主程序
└── tests/               # 测试代码
    └── test_memos.py    # 单元测试
```

## 添加新功能

1. 在 `scripts/memos.py` 中添加功能
2. 更新 `SKILL.md` 文档
3. 添加测试用例
4. 更新版本号（`package.json` 和 `SKILL.md`）

## 提交规范

- 使用清晰的提交信息
- 一个功能一个提交
- 确保测试通过

## 发布流程

1. 更新版本号
2. 更新 CHANGELOG
3. 打包：`zip -r smart-memos.skill smart-memos/`
4. 上传到 SkillHub
