# Troubleshooting - Tech Brainstorm

## LLM API errors

### "API key not found"
- Check that `~/.openclaw/secrets/openai_api_key` exists and contains a valid key
- Verify file permissions: `chmod 600 ~/.openclaw/secrets/openai_api_key`
- Or set `llm.api_key_file` in config to a different path

### "Connection refused" / timeout
- Verify `llm.base_url` is reachable
- If using a local LLM (Ollama, LM Studio), ensure the server is running
- Check firewall rules if using a remote endpoint

### "Model not found"
- Verify the model name in `llm.model` is valid for your API provider
- OpenAI: `gpt-4o-mini`, `gpt-4o`, `gpt-4-turbo`
- Ollama: `llama3`, `mistral`, etc.

## Dispatch errors

### Telegram: "bot_token not found"
- Set `bot_token` in the output config, or configure Telegram in `~/.openclaw/openclaw.json`
- Verify `channels.telegram.botToken` exists in OpenClaw config

### Telegram: "chat_id required"
- Set `chat_id` in the telegram_bot output config
- Get your chat ID: message @userinfobot on Telegram

### Nextcloud: "skill not installed"
- Install the nextcloud-files skill: `clawhub install nextcloud-files`
- Or remove the nextcloud output from your config

### Mail: "mail_to required"
- Set `mail_to` in the mail-client output config

## Config errors

### "Config file not found"
- Run `python3 scripts/setup.py` to create the config
- Config location: `~/.openclaw/config/tech-brainstorm/config.json`

### "Invalid JSON"
- Validate your config file: `python3 -m json.tool ~/.openclaw/config/tech-brainstorm/config.json`
- Common issue: trailing commas in JSON

## Research data

### "No research data provided"
- The agent should pass web research as JSON on stdin
- Manual usage: pipe a JSON array of `{"url": "...", "title": "...", "content": "..."}` objects
- Or use `--topic` flag for LLM-only brainstorm (no web sources)

### Empty or low-quality results
- Increase `max_sources` in config
- Change `search_depth` to "deep"
- Provide more specific context with `--context`
