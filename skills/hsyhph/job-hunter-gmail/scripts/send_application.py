#!/usr/bin/env python3
"""
求职邮件自动发送脚本
通过 Gmail (Maton) 发送求职申请
"""
import requests
import json
import os
import sys
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from pathlib import Path

# 配置
MATON_API_KEY = os.environ.get("MATON_API_KEY", "TpAggeUoPNsXeQchTqBRHm5K3-oVN22ckuq5aFQ52xFGofH7DRo1YhPM_z21FXKmZJ9wu1qKAAPVSy5GLvx2zMVNWHVdeluoVbU")
MATON_BASE_URL = "https://gateway.maton.ai/google-mail/gmail/v1/users/me"

HEADERS = {
    "Authorization": f"Bearer {MATON_API_KEY}",
    "Content-Type": "application/json"
}

# 数据目录
DATA_DIR = Path(__file__).parent.parent / "data"


def load_resume():
    """加载简历信息"""
    resume_file = DATA_DIR / "resume.json"
    if resume_file.exists():
        return json.loads(resume_file.read_text(encoding="utf-8"))
    return {}


def load_applications():
    """加载投递记录"""
    apps_file = DATA_DIR / "applications.json"
    if apps_file.exists():
        return json.loads(apps_file.read_text(encoding="utf-8"))
    return {"applications": []}


def save_application(app_data):
    """保存投递记录"""
    apps = load_applications()
    apps["applications"].append(app_data)
    apps_file = DATA_DIR / "applications.json"
    apps_file.write_text(json.dumps(apps, ensure_ascii=False, indent=2), encoding="utf-8")


def create_label(name):
    """创建 Gmail 标签"""
    url = f"{MATON_BASE_URL}/labels"
    data = {"name": name}
    response = requests.post(url, headers=HEADERS, json=data)
    return response.json()


def send_email(to, subject, body, attachments=None):
    """发送求职邮件"""
    # 构建 MIME 邮件
    msg = MIMEMultipart("alternative")
    msg["to"] = to
    msg["subject"] = subject
    
    # 添加纯文本和 HTML 版本
    text_part = MIMEText(body, "plain", "utf-8")
    html_part = MIMEText(body.replace("\n", "<br>"), "html", "utf-8")
    msg.attach(text_part)
    msg.attach(html_part)
    
    # 添加附件（简历）
    if attachments:
        for att_path in attachments:
            if Path(att_path).exists():
                with open(att_path, "rb") as f:
                    att = MIMEApplication(f.read())
                    att.add_header("Content-Disposition", "attachment", 
                                   filename=Path(att_path).name)
                    msg.attach(att)
    
    # Base64url 编码
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode("utf-8").rstrip("=")
    
    url = f"{MATON_BASE_URL}/messages/send"
    data = {"raw": raw}
    response = requests.post(url, headers=HEADERS, json=data)
    return response.json()


def generate_cover_letter(company, position, template_name="general"):
    """生成求职信"""
    resume = load_resume()
    
    templates = {
        "general": """{name} 求职信 - {position}

尊敬的 {company} 招聘负责人：

您好！我是 {name}，{title}，拥有 {experience} 工作经验。偶然间看到贵公司 {position} 的招聘信息，深感机遇难逢，特此投递简历申请该职位。

{highlights}

我具备以下优势：
{skills}

期待能与您进一步沟通，共同探讨该岗位的合作可能性。

此致
敬礼

{name}
{phone}
{email}
{date}""",
        
        "tech": """{name} 技术岗位求职信 - {position}

尊敬的 {company} 技术团队：

您好！我是 {name}，{title}，{experience}。看到贵公司招聘 {position} 岗位，深感兴奋，特此申请。

技术优势：
{tech_skills}

项目经验：
{projects}

我热衷于技术研发，期待能加入贵公司技术团队，共同打造优秀产品。

此致
敬礼

{name}
{phone}
{email}
{date}"""
    }
    
    template = templates.get(template_name, templates["general"])
    
    # 变量替换
    replacements = {
        "name": resume.get("name", "应聘者"),
        "title": resume.get("title", "求职者"),
        "experience": resume.get("experience", "相关经验"),
        "company": company,
        "position": position,
        "phone": resume.get("phone", ""),
        "email": resume.get("email", ""),
        "date": __import__("datetime").datetime.now().strftime("%Y-%m-%d"),
        "highlights": resume.get("highlights", ""),
        "skills": resume.get("skills", ""),
        "tech_skills": resume.get("tech_skills", ""),
        "projects": resume.get("projects", ""),
    }
    
    return template.format(**replacements)


def send_application(company, position, hr_email, template="general", resume_path=None):
    """发送求职申请"""
    resume = load_resume()
    
    # 生成求职信
    body = generate_cover_letter(company, position, template)
    subject = f"应聘 {position} - {resume.get('name', '求职者')}"
    
    # 准备附件
    attachments = []
    if resume_path:
        attachments.append(resume_path)
    elif resume.get("resume_file"):
        attachments.append(resume.get("resume_file"))
    
    # 发送邮件
    result = send_email(hr_email, subject, body, attachments)
    
    # 保存投递记录
    app_data = {
        "id": result.get("id", ""),
        "company": company,
        "position": position,
        "hr_email": hr_email,
        "template": template,
        "status": "sent",
        "sent_at": __import__("datetime").datetime.now().isoformat(),
        "gmail_id": result.get("id", "")
    }
    save_application(app_data)
    
    return result


def list_applications():
    """列出所有投递记录"""
    return load_applications()


def main():
    if len(sys.argv) < 2:
        print("求职投递工具")
        print("=" * 40)
        print("用法:")
        print("  python send_application.py send <公司> <岗位> <HR邮箱> [模板]  # 发送申请")
        print("  python send_application.py list                                      # 投递记录")
        print("  python send_application.py cover <公司> <岗位> [模板]             # 生成求职信预览")
        print("  python send_application.py label <标签名>                          # 创建Gmail标签")
        return
    
    command = sys.argv[1]
    
    try:
        if command == "send":
            if len(sys.argv) < 5:
                print("用法: send <公司> <岗位> <HR邮箱> [模板]") 
                return
            company = sys.argv[2]
            position = sys.argv[3]
            hr_email = sys.argv[4]
            template = sys.argv[5] if len(sys.argv) > 5 else "general"
            result = send_application(company, position, hr_email, template)
            print(json.dumps(result, indent=2, ensure_ascii=False))
            
        elif command == "list":
            result = list_applications()
            print(json.dumps(result, indent=2, ensure_ascii=False))
            
        elif command == "cover":
            if len(sys.argv) < 4:
                print("用法: cover <公司> <岗位> [模板]") 
                return
            company = sys.argv[2]
            position = sys.argv[3]
            template = sys.argv[4] if len(sys.argv) > 4 else "general"
            body = generate_cover_letter(company, position, template)
            print(body)
            
        elif command == "label":
            if len(sys.argv) < 3:
                print("用法: label <标签名>") 
                return
            label_name = sys.argv[2]
            result = create_label(label_name)
            print(json.dumps(result, indent=2, ensure_ascii=False))
            
        else:
            print(f"未知命令: {command}")
            
    except Exception as e:
        print(f"错误: {e}")


if __name__ == "__main__":
    main()