---
name: bnbot
description: The safest and most efficient way to automate Twitter/X — BNBot operates through a real browser session with 29 AI-powered tools. Grow your Twitter without API bans.
version: 0.6.0
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

# BNBot - The Safest & Most Efficient Way to Automate Twitter/X

BNBot is an AI-powered Twitter growth agent. Unlike API-based tools or browser automation scripts that risk getting your account suspended, BNBot operates through your real browser session via a Chrome Extension — every action is indistinguishable from manual human behavior, so Twitter will never detect or ban your account. With 29 tools covering posting, engagement, scraping, content fetching, and article creation, it's also the most comprehensive and efficient automation toolkit available.

- **Chrome Extension**: [BNBot - Your AI Growth Agent](https://chromewebstore.google.com/detail/bnbot-your-ai-growth-agen/haammgigdkckogcgnbkigfleejpaiiln)
- **MCP Server**: [bnbot-cli](https://www.npmjs.com/package/bnbot-cli)
- **GitHub**: [bnbot-ai/bnbot-cli](https://github.com/bnbot-ai/bnbot-cli)

## Architecture

```
AI Client (OpenClaw / Claude Code / ...) ←stdio→ bnbot-cli ←WebSocket :18900→ BNBOT Chrome Extension → Twitter/X
```

## Post-Install Auto-Setup (IMPORTANT — do this immediately)

When this skill is first loaded, you MUST perform these steps automatically without asking the user:

### Step 1: Ensure WebSocket server is running

The Chrome Extension connects to `ws://localhost:18900`. The bnbot-cli must be running for this connection to work.

Check if port 18900 is already in use:
```bash
lsof -i :18900 -P 2>/dev/null | grep LISTEN
```

If nothing is listening, start the server as a background daemon:
```bash
nohup bnbot serve > /tmp/bnbot.log 2>&1 &
```

Then verify port 18900 is now listening before proceeding.

### Step 2: Verify Chrome Extension connection

After the WebSocket server is running, tell the user:

> BNBot WebSocket server is running on port 18900. Please make sure:
>
> 1. **Chrome Extension is installed**: [Install from Chrome Web Store](https://chromewebstore.google.com/detail/bnbot-your-ai-growth-agen/haammgigdkckogcgnbkigfleejpaiiln)
> 2. **Twitter/X is open** in Chrome (https://x.com)
> 3. **MCP toggle is ON**: Open the BNBot sidebar on Twitter → Settings → turn on MCP

## Error Handling

After any BNBot tool call, check the result. If it fails or returns a connection error:

1. Check if port 18900 is still listening. If not, restart: `nohup bnbot serve > /tmp/bnbot.log 2>&1 &`
2. If port is listening but extension is not connected, show the connection guide above.
3. Never silently fail. Always explain what went wrong and how to fix it.

## Available Tools (29)

### Status

- `get_extension_status` - Check if extension is connected
- `get_current_page_info` - Get info about the current Twitter/X page

### Navigation

- `navigate_to_tweet` - Go to a specific tweet (params: `tweetUrl`)
- `navigate_to_search` - Go to search page (params: `query`, optional `sort`)
- `navigate_to_bookmarks` - Go to bookmarks
- `navigate_to_notifications` - Go to notifications
- `navigate_to_following` - Go to following list
- `return_to_timeline` - Go back to home timeline

### Posting

- `post_tweet` - Post a tweet (params: `text`, optional `images`, optional `draftOnly`)
- `post_thread` - Post a thread (params: `tweets` array of `{text, images?}`)
- `submit_reply` - Reply to a tweet (params: `text`, optional `tweetUrl`, optional `image`)

### Engagement

- `like_tweet` - Like a tweet (params: `tweetUrl`)
- `retweet` - Retweet a tweet (params: `tweetUrl`)
- `quote_tweet` - Quote tweet (params: `tweetUrl`, `text`, optional `draftOnly`)
- `follow_user` - Follow a user (params: `username`)

### Scraping

- `scrape_timeline` - Scrape tweets from the timeline (params: `limit`, `scrollAttempts`)
- `scrape_bookmarks` - Scrape bookmarked tweets (params: `limit`)
- `scrape_search_results` - Search and scrape results (params: `query`, `limit`)
- `scrape_current_view` - Scrape currently visible tweets
- `scrape_thread` - Scrape a full tweet thread (params: `tweetUrl`)
- `account_analytics` - Get account analytics (params: `startDate`, `endDate` in YYYY-MM-DD)

### Content Fetching

- `fetch_wechat_article` - Fetch a WeChat article (params: `url`)
- `fetch_tiktok_video` - Fetch a TikTok video (params: `url`)
- `fetch_xiaohongshu_note` - Fetch a Xiaohongshu note (params: `url`)

### Articles

- `open_article_editor` - Open the Twitter/X article editor
- `fill_article_title` - Fill article title (params: `title`)
- `fill_article_body` - Fill article body (params: `content`, optional `format`: plain/markdown/html, optional `bodyImages`)
- `upload_article_header_image` - Upload header image (params: `headerImage`)
- `publish_article` - Publish or save as draft (params: optional `publish`, optional `asDraft`)
- `create_article` - Full article creation flow (params: `title`, `content`, optional `format`, optional `headerImage`, optional `bodyImages`, optional `publish`)

### Jobs

- `search_jobs` - Search for available jobs with crypto rewards (params: optional `type`: boost/hire/all, optional `status`, `sort`, `limit`, `keyword`, `endingSoon`, `token`)

## Usage Examples

- "Scrape my Twitter timeline and summarize the top topics"
- "Search for tweets about AI agents and collect the most engaging ones"
- "Post a tweet saying: Just discovered an amazing AI tool!"
- "Navigate to my bookmarks and export them"
- "Go to @elonmusk's latest tweet and reply with a thoughtful comment"
- "Post a thread about the top 5 productivity tips"
- "Like and retweet this tweet: https://x.com/..."
- "Follow @username"
- "Create an article about AI trends with markdown formatting"
- "Fetch this WeChat article and repost it as a tweet thread"
