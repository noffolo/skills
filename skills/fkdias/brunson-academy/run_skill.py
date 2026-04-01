#!/usr/bin/env python3
"""
OpenClaw Skill Wrapper for Brunson Academy
"""
import sys
import os
from pathlib import Path
import json

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from brunson_academy import BrunsonAcademy

def parse_openclaw_input():
    """
    Parse input from OpenClaw skill call
    
    Expected format: /brunson [command] [args...]
    """
    if len(sys.argv) < 2:
        return "help", []
    
    # Join all args and parse
    full_input = " ".join(sys.argv[1:])
    
    # Check if it's a command
    if full_input.startswith("/brunson "):
        full_input = full_input[len("/brunson "):]
    
    # Split into command and args
    parts = full_input.split()
    if not parts:
        return "help", []
    
    command = parts[0]
    args = parts[1:] if len(parts) > 1 else []
    
    return command, args

def main():
    """Main entry point for OpenClaw skill"""
    academy = BrunsonAcademy()
    
    # Parse input
    command, args = parse_openclaw_input()
    
    # Handle command
    try:
        result = academy.handle_command(command, args)
        
        # Output for OpenClaw
        output = {
            "success": True,
            "command": command,
            "result": result,
            "metadata": {
                "skill": "brunson-academy",
                "version": "0.1.0",
                "phase": 1
            }
        }
        
        # Print as JSON for OpenClaw
        try:
            print(json.dumps(output, ensure_ascii=False))
        except UnicodeEncodeError:
            # Remove emojis for Windows compatibility
            import re
            clean_result = re.sub(r'[^\x00-\x7F]+', '', result)
            output["result"] = clean_result
            print(json.dumps(output, ensure_ascii=False))
        
    except Exception as e:
        # Error handling
        error_output = {
            "success": False,
            "command": command,
            "error": str(e),
            "metadata": {
                "skill": "brunson-academy",
                "version": "0.1.0"
            }
        }
        print(json.dumps(error_output, ensure_ascii=False))
        sys.exit(1)

if __name__ == "__main__":
    main()