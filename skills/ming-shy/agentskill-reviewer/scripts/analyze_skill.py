#!/usr/bin/env python3
"""
Skill 分析辅助脚本
用于解析 SKILL.md 的 YAML frontmatter 和统计信息
"""
import sys
import os
import re
from pathlib import Path
import yaml

def parse_skill_md(skill_path):
    """解析 SKILL.md 文件"""
    skill_md = Path(skill_path) / "SKILL.md"
    
    if not skill_md.exists():
        return {"error": "SKILL.md not found"}
    
    content = skill_md.read_text(encoding='utf-8')
    
    # 解析 YAML frontmatter
    frontmatter_match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', content, re.DOTALL)
    
    if not frontmatter_match:
        return {"error": "No valid YAML frontmatter"}
    
    frontmatter_text = frontmatter_match.group(1)
    body_text = frontmatter_match.group(2)
    
    try:
        frontmatter = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError as e:
        return {"error": f"Invalid YAML: {e}"}
    
    # 统计信息
    body_lines = body_text.strip().split('\n')
    description_length = len(frontmatter.get('description', ''))
    
    # 检查冗余关键词（常见的过度解释）
    redundancy_keywords = [
        r'众所周知',
        r'显而易见',
        r'不言而喻',
        r'大家都知道',
        r'Python\s*是一种编程语言',
        r'Markdown\s*是.*标记语言',
        r'简单来说',
        r'顾名思义',
    ]
    
    redundancy_matches = []
    for i, line in enumerate(body_lines, start=1):
        for pattern in redundancy_keywords:
            if re.search(pattern, line, re.IGNORECASE):
                redundancy_matches.append({
                    "line": i,
                    "content": line.strip(),
                    "pattern": pattern
                })
    
    # 查找 references/ 引用
    reference_links = re.findall(r'\[([^\]]+)\]\(references/([^\)]+)\)', body_text)
    
    return {
        "frontmatter": frontmatter,
        "body_lines": len(body_lines),
        "body_chars": len(body_text),
        "description_length": description_length,
        "redundancy_matches": redundancy_matches,
        "reference_links": reference_links,
    }

def check_directory_structure(skill_path):
    """检查目录结构"""
    skill_dir = Path(skill_path)
    
    structure = {
        "SKILL.md": skill_dir / "SKILL.md",
        "scripts/": skill_dir / "scripts",
        "references/": skill_dir / "references",
        "assets/": skill_dir / "assets",
    }
    
    results = {}
    for name, path in structure.items():
        if path.exists():
            if path.is_file():
                results[name] = {"exists": True, "type": "file"}
            else:
                files = list(path.iterdir())
                results[name] = {"exists": True, "type": "dir", "count": len(files)}
        else:
            results[name] = {"exists": False}
    
    # 检查不应该存在的文件
    unwanted_files = []
    for pattern in ['README.md', 'CHANGELOG.md', 'INSTALLATION.md', 'QUICK_REFERENCE.md']:
        if (skill_dir / pattern).exists():
            unwanted_files.append(pattern)
    
    results["unwanted_files"] = unwanted_files
    
    return results

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: analyze_skill.py <skill-path>")
        sys.exit(1)
    
    skill_path = sys.argv[1]
    
    if not os.path.isdir(skill_path):
        print(f"Error: {skill_path} is not a directory")
        sys.exit(1)
    
    # 解析 SKILL.md
    skill_info = parse_skill_md(skill_path)
    
    # 检查目录结构
    structure_info = check_directory_structure(skill_path)
    
    # 输出 JSON 格式
    import json
    result = {
        "skill_path": skill_path,
        "skill_info": skill_info,
        "structure": structure_info,
    }
    
    print(json.dumps(result, ensure_ascii=False, indent=2))
