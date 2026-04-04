# figma-to-mobile

Convert Figma designs to production-ready mobile UI code.

Supports: Android XML · Jetpack Compose · SwiftUI · UIKit

## Install

### Claude Code

Copy the `figma-to-mobile` folder into your project:
```
your-project/.claude/skills/figma-to-mobile/
```

### GitHub Copilot

Copy the `figma-to-mobile` folder into your project:
```
your-project/.agents/skills/figma-to-mobile/
```

### OpenClaw

Place in your workspace skills directory or install via ClawHub:
```bash
clawhub install figma-to-mobile
```

## Setup

1. Get a Figma Personal Access Token:
   - Figma → Avatar → Settings → Security → Personal Access Tokens
   - Generate a new token (starts with `figd_`)

2. Set the environment variable:
   ```bash
   # macOS/Linux
   export FIGMA_TOKEN="figd_your_token_here"

   # Windows PowerShell
   $env:FIGMA_TOKEN = "figd_your_token_here"
   ```

## Usage

Paste a Figma design link in your AI assistant's chat:

> Convert this to Android XML: https://www.figma.com/design/xxx/Project?node-id=100-200

The agent will:
1. Fetch the design data from Figma API
2. Ask clarifying questions (platform, list vs static, etc.)
3. Generate production-ready code files
4. Iterate based on your feedback

## What's in the box

```
figma-to-mobile/
├── SKILL.md              # Agent instructions (the brain)
├── scripts/
│   └── figma_fetch.py    # Figma API data fetcher
└── references/
    ├── xml-patterns.md       # Android XML mapping rules
    ├── compose-patterns.md   # Jetpack Compose mapping rules
    ├── swiftui-patterns.md   # SwiftUI mapping rules
    └── uikit-patterns.md     # UIKit mapping rules
```

## Requirements

- Python 3.8+ with `requests` package
- Figma Personal Access Token
