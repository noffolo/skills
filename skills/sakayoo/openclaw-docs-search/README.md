# OpenClaw Docs Search

Code-enhanced publish package for ClawHub / OpenClaw skill distribution.

## Summary

OpenClaw Docs Search helps the agent search OpenClaw official documentation and return concise Markdown results. This package includes both the skill instructions and the supporting TypeScript / JavaScript implementation used for official-search querying, document fetching, content extraction, and Markdown conversion.

## Included Files

- `SKILL.md` — skill metadata and runtime instructions
- `src/search.ts` — source implementation
- `dist/search.js` — compiled runtime build
- `package.json` / `package-lock.json` — dependency manifest
- `tsconfig.json` — TypeScript build configuration

## What This Skill Does

- Searches OpenClaw official docs through the official search endpoint
- Prefers English queries for higher search precision
- Fetches a specific documentation page on demand
- Extracts the `#content-area` main article region
- Converts noisy HTML into compact Markdown for LLM consumption

## Intended Use

- Answer questions about OpenClaw setup, configuration, CLI, channels, gateway, diagnostics, and skills
- Retrieve specific documentation pages on demand
- Reduce token usage compared with loading full documentation pages

## Safety Notes

- This skill is intended for public documentation lookup only
- It does not request secrets, credentials, or local private files
- It avoids bulk site mirroring and is designed for on-demand retrieval
