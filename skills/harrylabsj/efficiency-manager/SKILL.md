---
name: efficiency-manager
description: Track events, analyze efficiency, generate daily/weekly/monthly reports with suggestions. All data stored locally.
triggers:
  - 效率
  - 效率日报
  - 效率周报
  - 效率月报
  - 效率分析
  - 效率报告
  - 时间管理
  - 事情安排
  - 时间规划
  - 做什么效率高
  - efficiency
  - efficiency report
  - time analysis
---

# Efficiency Manager

Track your daily activities, analyze efficiency, and get actionable insights.

## Overview

Efficiency Manager helps you:
- Track events with description, category, and time
- Analyze your efficiency per category (vs. your best & global average)
- Generate daily, weekly, and monthly efficiency reports
- Get suggestions to improve your productivity
- Optimize your schedule based on your best time slots

## Features

- **Event Tracking**: Record what you did, when, and for how long
- **Efficiency Analysis**: Compare your performance vs. best & average
- **Time Insights**: Learn when you're most productive for each category
- **Reports**: Daily, weekly, and monthly efficiency reports
- **Smart Scheduling**: Get suggestions on what to do when

## Installation

```bash
clawhub install efficiency-manager
```

## Usage

### Record Events

```bash
# Quick add
efficiency add "写代码" --category work --from 09:00 --to 11:00

# With notes
efficiency add "看书" --category study --from 14:00 --to 15:30 --notes "阅读《深度工作》"

# Interactive mode
efficiency add
```

### View Reports

```bash
# Daily report (default: today)
efficiency report today
efficiency report 2026-03-21

# Weekly report
efficiency report week
efficiency report week 2026-03-15

# Monthly report
efficiency report month
efficiency report month 2026-03
```

### Analyze Efficiency

```bash
# Analyze specific category
efficiency analyze work
efficiency analyze study

# Analyze all
efficiency analyze --all
```

### Smart Planning

```bash
# Get schedule suggestions
efficiency plan "写代码2h" "开会1h" "健身1h"
```

### Configuration

```bash
# Show config
efficiency config

# Set preferences
efficiency config set dayStart 06:00
efficiency config set reportTime 22:00
```

### List Events

```bash
# List recent events
efficiency list

# List events by date
efficiency list --date 2026-03-21

# List by category
efficiency list --category work
```

### Delete Events

```bash
# Delete by ID
efficiency delete <event-id>

# Delete all (with confirmation)
efficiency delete --all
```

## Categories

| Category | Chinese | Best Duration |
|----------|---------|---------------|
| work | 工作 | 1.8h |
| study | 学习 | 1.0h |
| exercise | 运动 | 0.75h |
| social | 社交 | 1.5h |
| rest | 休息 | 0.5h |
| entertainment | 娱乐 | 1.2h |
| chores | 家务 | 1.0h |
| other | 其他 | 1.0h |

## Time Slots

- **Morning**: 06:00 - 12:00
- **Afternoon**: 12:00 - 18:00
- **Evening**: 18:00 - 22:00
- **Night**: 22:00 - 06:00

## Data Storage

All data is stored locally:
- Events: `~/.openclaw/efficiency-manager/data/events.json`
- Config: `~/.openclaw/efficiency-manager/config.json`

## Requirements

- Node.js 18+
- OpenClaw installed

## Version

1.0.0