# 求职自动投递技能

## 功能概述
自动管理求职流程，包括简历管理、求职信模板、职位平台管理、自动投递记录、Gmail 集成追踪。

## 触发条件
用户提到"求职"、"投简历"、"找工作"、"job"、"简历"时自动激活。

## 技能能力

### 1. 简历管理
- 上传/更新简历 (PDF/DOCX)
- 维护多版本简历（不同岗位方向）
- 提取简历关键信息

### 2. 求职信模板
- 创建针对不同岗位的求职信模板
- 变量替换：姓名、职位、公司名、JD等
- 自动生成定制化求职信

### 3. 职位平台管理
- 记录投递的职位平台（BOSS直聘、拉勾、猎聘、智联招聘等）
- 记录投递状态：已投递、待回复、已面试、已拒绝、已offer

### 4. 投递记录追踪
- 记录投递时间、公司、岗位、薪资、状态
- Gmail 标签自动分类（按公司或状态）

### 5. 自动投递 (通过 Gmail)
- 使用 Gmail 发送求职邮件
- 自动抄送投递记录到指定邮箱
- 自动打标签分类

## 文件结构
```
job-hunter/
├── SKILL.md
├── scripts/
│   ├── send_application.py    # 发送求职邮件
│   ├── track_applications.py  # 追踪投递状态
│   └── gmail_labels.py        # Gmail 标签管理
├── templates/
│   ├── cover_letter_general.md
│   ├── cover_letter_tech.md
│   └── cover_letter_sales.md
├── data/
│   ├── resume.json            # 简历信息
│   ├── applications.json      # 投递记录
│   └── platforms.json         # 平台配置
```

## 配置项
- GMAIL_API_KEY: Maton Gmail API Key（自动继承）
- RESUME_PATH: 简历文件路径
- DEFAULT_EMAIL_SIGNATURE: 默认邮件签名

## 使用示例
- "帮我投个简历" → 交互式投递流程
- "查看投递记录" → 列出所有投递
- "更新简历" → 上传新简历
- "生成求职信" → 创建定制求职信