#!/usr/bin/env python3
"""
Version Manager for Trading Assistant
版本管理工具 - 统一更新项目中的所有版本号

Usage / 用法:
    python version_manager.py <new_version>
    
Example / 示例:
    python version_manager.py 1.4.0
"""

import sys
import os
import re
from pathlib import Path

# Files that contain version numbers / 包含版本号的文件
VERSION_FILES = {
    'pyproject.toml': [
        (r'^version = "[\d.]+"', 'version = "{version}"'),
    ],
    'cli.py': [
        (r'VERSION = "[\d.]+"', 'VERSION = "{version}"'),
    ],
    'README.md': [
        (r'\*\*Version\*\*: v[\d.]+', '**Version**: v{version}'),
    ],
    'CHANGELOG.md': [
        (r'## \[(\d+\.\d+\.\d+)\]', None),  # Just check, don't replace
    ],
    'docs/CLI.md': [
        (r'Version: [\d.]+', 'Version: {version}'),
    ],
}

def get_current_version():
    """Get current version from pyproject.toml"""
    pyproject = Path('pyproject.toml')
    if not pyproject.exists():
        print("❌ pyproject.toml not found")
        sys.exit(1)
    
    content = pyproject.read_text()
    match = re.search(r'^version = "([\d.]+)"', content, re.MULTILINE)
    if not match:
        print("❌ Version not found in pyproject.toml")
        sys.exit(1)
    
    return match.group(1)

def update_version(new_version):
    """Update version in all files"""
    print(f"📝 Updating version to v{new_version}...\n")
    
    updated_files = []
    
    for file_path, patterns in VERSION_FILES.items():
        path = Path(file_path)
        if not path.exists():
            print(f"⚠️  Skipping {file_path} (not found)")
            continue
        
        content = path.read_text()
        original_content = content
        changes_made = False
        
        for pattern, replacement in patterns:
            if replacement is None:
                # Just check if pattern exists
                if re.search(pattern, content, re.MULTILINE):
                    print(f"✓ Found version pattern in {file_path}")
                continue
            
            new_pattern = replacement.format(version=new_version)
            new_content = re.sub(pattern, new_pattern, content, flags=re.MULTILINE)
            
            if new_content != content:
                changes_made = True
                print(f"✓ Updated {file_path}")
                content = new_content
        
        if changes_made:
            path.write_text(content)
            updated_files.append(file_path)
    
    # Update CHANGELOG - add new version section
    changelog = Path('CHANGELOG.md')
    if changelog.exists():
        content = changelog.read_text()
        # Check if new version section already exists
        if f'## [{new_version}]' not in content:
            # Add new version section after the header
            header_match = re.search(r'(## \[\d+\.\d+\.\d+\] - \d{4}-\d{2}-\d{2})', content)
            if header_match:
                insert_pos = header_match.start()
                today = Path.cwd().stat().st_mtime
                from datetime import datetime
                today_str = datetime.now().strftime('%Y-%m-%d')
                new_section = f"\n## [{new_version}] - {today_str}\n\n### 🆕 Coming Soon\n\n- Details TBD\n\n"
                content = content[:insert_pos] + new_section + content[insert_pos:]
                changelog.write_text(content)
                print(f"✓ Updated CHANGELOG.md with new version section")
                updated_files.append('CHANGELOG.md')
    
    print(f"\n✅ Version updated to v{new_version}!")
    print(f"📝 Modified files: {len(updated_files)}")
    for f in updated_files:
        print(f"   - {f}")
    
    return updated_files

def main():
    if len(sys.argv) != 2:
        print(__doc__)
        current = get_current_version()
        print(f"\nCurrent version: v{current}")
        sys.exit(1)
    
    new_version = sys.argv[1]
    
    # Validate version format
    if not re.match(r'^\d+\.\d+\.\d+$', new_version):
        print("❌ Invalid version format. Use semantic versioning: X.Y.Z (e.g., 1.4.0)")
        sys.exit(1)
    
    current_version = get_current_version()
    print(f"Current version: v{current_version}")
    print(f"New version: v{new_version}\n")
    
    if current_version == new_version:
        print("⚠️  Version is already up to date!")
        sys.exit(0)
    
    update_version(new_version)
    
    print("\n💡 Next steps:")
    print("   1. git add -A")
    print(f"   2. git commit -m 'chore: Bump version to {new_version}'")
    print("   3. git push origin main")
    print(f"   4. git tag v{new_version}")
    print(f"   5. git push origin v{new_version}")

if __name__ == '__main__':
    main()
