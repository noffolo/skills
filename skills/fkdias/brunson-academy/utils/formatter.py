#!/usr/bin/env python3
"""
Output formatting utilities
"""
import json

def format_output(content, format_type="markdown"):
    """Format content for output"""
    if format_type == "markdown":
        return content
    elif format_type == "json":
        try:
            return json.dumps(content, indent=2, ensure_ascii=False)
        except:
            return str(content)
    elif format_type == "text":
        # Simple text formatting
        if isinstance(content, dict):
            return dict_to_text(content)
        else:
            return str(content)
    else:
        return str(content)

def dict_to_text(data, indent=0):
    """Convert dict to readable text"""
    lines = []
    for key, value in data.items():
        if isinstance(value, dict):
            lines.append("  " * indent + f"{key}:")
            lines.append(dict_to_text(value, indent + 1))
        elif isinstance(value, list):
            lines.append("  " * indent + f"{key}:")
            for item in value:
                if isinstance(item, dict):
                    lines.append(dict_to_text(item, indent + 1))
                else:
                    lines.append("  " * (indent + 1) + f"- {item}")
        else:
            lines.append("  " * indent + f"{key}: {value}")
    return "\n".join(lines)

def split_long_message(text, max_length=4000):
    """
    Split long messages for platforms with length limits
    
    Args:
        text: Message text
        max_length: Maximum length per chunk
    
    Returns:
        list: Chunks of text
    """
    if len(text) <= max_length:
        return [text]
    
    # Try to split at markdown sections
    chunks = []
    current_chunk = ""
    
    lines = text.split('\n')
    for line in lines:
        # If adding this line would exceed limit, start new chunk
        if len(current_chunk) + len(line) + 1 > max_length and current_chunk:
            chunks.append(current_chunk.strip())
            current_chunk = line
        else:
            if current_chunk:
                current_chunk += '\n' + line
            else:
                current_chunk = line
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks

def add_telegram_formatting(text):
    """
    Add Telegram-friendly formatting
    
    Args:
        text: Plain text
    
    Returns:
        str: Formatted text with markdown
    """
    # Simple markdown formatting
    lines = text.split('\n')
    formatted_lines = []
    
    for line in lines:
        # Headers
        if line.startswith('# '):
            formatted_lines.append(f"*{line[2:]}*")
        elif line.startswith('## '):
            formatted_lines.append(f"**{line[3:]}**")
        elif line.startswith('### '):
            formatted_lines.append(f"__{line[4:]}__")
        else:
            formatted_lines.append(line)
    
    return '\n'.join(formatted_lines)