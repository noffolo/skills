#!/usr/bin/env python3
"""
Brunson Academy - Main Skill Handler
"""
import sys
import os
from pathlib import Path
import argparse
import json

# Add commands to path
sys.path.append(str(Path(__file__).parent / "commands"))
sys.path.append(str(Path(__file__).parent / "utils"))

try:
    from commands.value_ladder import build_value_ladder, format_value_ladder_output
    from utils.formatter import format_output
except ImportError as e:
    print(f"Import error: {e}")
    # Create minimal formatter if missing
    def format_output(content, format_type="markdown"):
        return content

class BrunsonAcademy:
    """Main handler for Brunson Academy skill"""
    
    def __init__(self):
        self.knowledge_base_path = Path(__file__).parent / "knowledge_base" / "frameworks.json"
        self.load_knowledge_base()
    
    def load_knowledge_base(self):
        """Load processed frameworks"""
        try:
            with open(self.knowledge_base_path, 'r', encoding='utf-8') as f:
                self.knowledge = json.load(f)
        except FileNotFoundError:
            self.knowledge = {"frameworks_by_type": {}}
            print("Warning: Knowledge base not found")
    
    def handle_command(self, command, args):
        """Route commands to appropriate handlers"""
        command = command.lower()
        
        if command == "value-ladder":
            return self.handle_value_ladder(args)
        elif command == "analyze":
            return self.handle_analyze(args)
        elif command == "script":
            return self.handle_script(args)
        elif command == "traffic-plan":
            return self.handle_traffic_plan(args)
        elif command == "webinar":
            return self.handle_webinar(args)
        elif command == "coach":
            return self.handle_coach(args)
        elif command == "academy":
            return self.handle_academy(args)
        elif command == "feedback":
            return self.handle_feedback(args)
        elif command == "joaquim":
            return self.handle_joaquim(args)
        elif command == "luiz-audit":
            return self.handle_luiz_audit(args)
        else:
            return self.handle_help()
    
    def handle_value_ladder(self, args):
        """Handle /brunson value-ladder command"""
        # Parse args (simple parsing for now)
        # Expected: product="name" [audience="desc"] [price="low|medium|high"]
        product = "Master Business"  # default
        audience = None
        price_range = None
        
        for arg in args:
            if arg.startswith("produto=") or arg.startswith("product="):
                product = arg.split("=", 1)[1].strip('"\'')
            elif arg.startswith("audience=") or arg.startswith("audiência="):
                audience = arg.split("=", 1)[1].strip('"\'')
            elif arg.startswith("price=") or arg.startswith("preço="):
                price_range = arg.split("=", 1)[1].strip('"\'').lower()
        
        # Build value ladder
        ladder = build_value_ladder(
            product_name=product,
            target_audience=audience,
            price_range=price_range
        )
        
        # Format output
        output = format_value_ladder_output(ladder, "markdown")
        
        # Add command info
        full_output = f"# 🎓 BRUNSON ACADEMY: Value Ladder\n\n"
        full_output += f"**Comando:** `/brunson value-ladder produto=\"{product}\"`\n\n"
        full_output += output
        
        return full_output
    
    def handle_analyze(self, args):
        """Handle /brunson analyze command"""
        return "# 🔍 Analysis Feature\n\nComing soon in Phase 2!"
    
    def handle_script(self, args):
        """Handle /brunson script command"""
        return "# 📝 Epiphany Bridge Script\n\nComing soon in Phase 2!"
    
    def handle_traffic_plan(self, args):
        """Handle /brunson traffic-plan command"""
        return "# 🚀 Dream 100 Traffic Plan\n\nComing soon in Phase 2!"
    
    def handle_webinar(self, args):
        """Handle /brunson webinar command"""
        return "# 🎥 Perfect Webinar Script\n\nComing soon in Phase 2!"
    
    def handle_coach(self, args):
        """Handle /brunson coach command"""
        return "# 🧠 Coach Brunson AI\n\nComing soon in Phase 3!\n\nFor now, use quick commands for immediate results."
    
    def handle_academy(self, args):
        """Handle /brunson academy command"""
        return "# 🎓 Brunson Academy Modules\n\nComing soon in Phase 3!"
    
    def handle_feedback(self, args):
        """Handle /brunson feedback command"""
        return "# 💬 Personalized Feedback\n\nComing soon in Phase 3!"
    
    def handle_joaquim(self, args):
        """Handle /brunson joaquim command"""
        return "# ✍️ Joaquim + Brunson Integration\n\nComing soon in Phase 2!"
    
    def handle_luiz_audit(self, args):
        """Handle /brunson luiz-audit command"""
        return "# 📊 Luiz Audit with Brunson Metrics\n\nComing soon in Phase 2!"
    
    def handle_help(self):
        """Show help"""
        help_text = """
# 🎓 BRUNSON ACADEMY - Available Commands

## 🚀 QUICK COMMANDS (Phase 1 - Available Now)
`/brunson value-ladder produto="[nome]"` - Generate Value Ladder
  Example: `/brunson value-ladder produto="Master Business"`

## ⏳ COMING SOON (Phase 2)
`/brunson analyze [URL/copy]` - Automatic funnel diagnosis
`/brunson script [produto]` - Epiphany Bridge script
`/brunson traffic-plan [nicho]` - Dream 100 strategy
`/brunson webinar [produto]` - Perfect Webinar script
`/brunson joaquim [produto]` - Copy via Joaquim + Brunson
`/brunson luiz-audit [copy]` - Audit with Brunson metrics

## 🧠 MENTOR MODE (Phase 3)
`/brunson coach` - Interactive Coach Brunson AI
`/brunson academy` - Educational modules
`/brunson feedback [texto]` - Personalized feedback

## 📚 KNOWLEDGE BASE
- 3 books processed: Expert Secrets, DotCom Secrets, Traffic Secrets
- 218,545 words analyzed
- 540 concepts extracted

## 🎯 CURRENT STATUS
**Phase 1 MVP:** Value Ladder command functional
**Next:** Epiphany Bridge script (2-3 days)
"""
        return help_text.strip()

def main():
    """Command-line interface"""
    parser = argparse.ArgumentParser(description="Brunson Academy Skill")
    parser.add_argument("command", help="Command to execute")
    parser.add_argument("args", nargs="*", help="Command arguments")
    
    # For testing without args
    if len(sys.argv) == 1:
        args = ["help"]
    else:
        args = sys.argv[1:]
    
    parsed_args = parser.parse_args(args)
    
    academy = BrunsonAcademy()
    result = academy.handle_command(parsed_args.command, parsed_args.args)
    
    # Safe print for Windows
    try:
        print(result)
    except UnicodeEncodeError:
        # Remove emojis and print
        import re
        clean_result = re.sub(r'[^\x00-\x7F]+', '', result)
        print(clean_result)

if __name__ == "__main__":
    main()