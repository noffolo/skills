---
name: bnbot
description: The safest and most efficient way to automate Twitter/X — BNBot operates through a real browser session with 29 AI-powered tools. Grow your Twitter without API bans.
version: 1.3.0
homepage: https://github.com/bnbot-ai/bnbot-cli
metadata:
  openclaw:
    emoji: "\U0001F916"
    os: [darwin, linux, windows]
    requires:
      bins: [bnbot-cli]
    install:
      - id: node
        kind: node
        package: bnbot-cli
        bins: [bnbot-cli]
        label: Install bnbot-cli (npm)
---

# BNBot - Control Twitter/X via AI

BNBot operates through a real browser session via Chrome Extension. 29 CLI tools for posting, engagement, scraping, content fetching, and articles.

- **Chrome Extension**: [Install](https://chromewebstore.google.com/detail/bnbot-your-ai-growth-agen/haammgigdkckogcgnbkigfleejpaiiln)
- **npm**: [bnbot-cli](https://www.npmjs.com/package/bnbot-cli)

## First-time setup (run once after install)

After `bnbot-cli` is installed, start the WebSocket daemon:

```bash
nohup bnbot serve > /tmp/bnbot.log 2>&1 &
sleep 1
lsof -i :18900 -P 2>/dev/null | grep LISTEN
```

Confirm port 18900 is LISTEN before proceeding.

## Before using any bnbot tool

Check if the daemon is still running:

```bash
lsof -i :18900 -P 2>/dev/null | grep LISTEN
```

If empty, restart it:

```bash
nohup bnbot serve > /tmp/bnbot.log 2>&1 &
```

## How to use tools

All tools are executed via the `bnbot` CLI:

```bash
bnbot get-extension-status
bnbot post-tweet --text "Hello world!"
bnbot scrape-timeline --limit 10
```

Output is JSON.

**Auto-thread for multiple images**: When `post-tweet` receives more than 4 images (Twitter's limit), it automatically splits into a thread — first tweet gets the text + first 4 images, subsequent tweets get remaining images in batches of 4. You don't need to manually use `post-thread` for this.

When scraping content from Xiaohongshu or other platforms with many images (e.g. 10), just pass all images to `post-tweet` and it handles the splitting automatically.

## If extension is not connected

If `bnbot get-extension-status` shows `connected: false`, tell the user:

> Chrome Extension is not connected. Please:
> 1. Install extension: https://chromewebstore.google.com/detail/bnbot-your-ai-growth-agen/haammgigdkckogcgnbkigfleejpaiiln
> 2. Open https://x.com in Chrome
> 3. Open BNBot sidebar → Settings → turn on MCP

## Available CLI commands

### Status
- `bnbot get-extension-status` — Check if extension is connected
- `bnbot get-current-page-info` — Get current Twitter/X page info

### Navigation
- `bnbot navigate-to-tweet --tweetUrl <url>`
- `bnbot navigate-to-search --query "..." [--sort ...]`
- `bnbot navigate-to-bookmarks`
- `bnbot navigate-to-notifications`
- `bnbot navigate-to-following`
- `bnbot return-to-timeline`

### Posting
- `bnbot post-tweet --text "..."`
- `bnbot post-thread --tweets '[{"text":"..."},{"text":"..."}]'`
- `bnbot submit-reply --text "..." [--tweetUrl <url>]`
- `bnbot quote-tweet --tweetUrl <url> --text "..."`

### Engagement
- `bnbot like-tweet [--tweetUrl <url>]`
- `bnbot retweet [--tweetUrl <url>]`
- `bnbot follow-user --username <handle>`

### Scraping
- `bnbot scrape-timeline --limit <n> --scrollAttempts <n>`
- `bnbot scrape-bookmarks --limit <n>`
- `bnbot scrape-search-results --query "..." --limit <n>`
- `bnbot scrape-current-view`
- `bnbot scrape-thread --tweetUrl <url>`
- `bnbot account-analytics --startDate YYYY-MM-DD --endDate YYYY-MM-DD`

### Content Fetching
- `bnbot fetch-wechat-article --url <url>`
- `bnbot fetch-tiktok-video --url <url>`
- `bnbot fetch-xiaohongshu-note --url <url>`

### Articles
- `bnbot open-article-editor`
- `bnbot fill-article-title --title "..."`
- `bnbot fill-article-body --content "..." [--format markdown]`
- `bnbot upload-article-header-image --headerImage <path>`
- `bnbot publish-article [--publish true]`
- `bnbot create-article --title "..." --content "..." [--format markdown]`

### Jobs
- `bnbot search-jobs [--type boost] [--limit 10]`
