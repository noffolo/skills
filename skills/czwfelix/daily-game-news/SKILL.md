# Daily-Game-News Skill

每日游戏资讯自动抓取与报告生成技能。

## 功能描述

1. 根据配置文件抓取多个游戏资讯网站的文章
2. 自动分类到 7 个大类（头条要闻、新品动态、厂商动态、行业数据、值得关注、投融资、其他）
3. 生成格式化报告并发送给用户
4. 同时生成 Word 文档存档

## 触发条件

- 定时任务：每天北京时间 10:00 自动执行
- 手动触发：用户提及 "每日游戏资讯"、"游戏新闻报告"、"Daily Game News"

## 配置文件

位置：`/home/admin/.openclaw/workspace/configs/news-crawler-config.json`

## 输出

1. **飞书消息**: 格式化报告直接发送给用户
2. **Word 文档 (.docx)**: 存储在 `/home/admin/.openclaw/workspace/reports/daily-game-news/`
3. **文本文件 (.txt)**: 保留用于兼容，同目录

## 使用示例

```bash
# 手动触发（使用虚拟环境）
cd ~/.openclaw/workspace/skills/daily-game-news
source .venv/bin/activate
python scripts/crawler.py

# 或使用 uv
uv run --with python-docx scripts/crawler.py

# 获取今日报告
获取今日游戏资讯报告

# 获取历史报告
获取 2026-03-07 游戏资讯报告