# cron-parser

Parse, validate, and explain cron expressions in natural language.

## Usage

```
What does this cron expression mean? [expression]
Parse and explain: [expression]
When does this cron run next? [expression]
Validate this cron: [expression]
```

## Examples

| Expression | Meaning |
|-----------|---------|
| `0 * * * *` | Every hour, at minute 0 |
| `0 9 * * 1-5` | Every weekday at 9am |
| `*/15 * * * *` | Every 15 minutes |
| `0 0 1 * *` | First day of every month at midnight |
| `30 4 * * *` | Every day at 4:30am |

## What it does

- **Parse** — Explains what a cron expression means in plain English
- **Next run** — Shows the next 5 execution times
- **Validate** — Checks if expression is valid
- **Convert** — Shows human-readable format and vice versa

## Notes

- Supports standard 5-field cron (minute, hour, day, month, weekday)
- All standard special characters: `*`, `,`, `-`, `/`
- Uses node-cron internally
