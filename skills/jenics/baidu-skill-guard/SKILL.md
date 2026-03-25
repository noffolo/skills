---
name: baidu-skill-guard
version: 1.0.8
description: Intercepts all skill install requests. MUST be used before installing any skill from ClawdHub, GitHub, 百度 AppBuilder 平台, or other sources. Run security check API to get risk rating. Triggers on install, add, enable, download skill.
---

# Skill Guard 🛡️

Security-first skill install guardian protocol. **Never install a skill without running security check first.**

## ⛔ MANDATORY INTERCEPTION RULE

**This skill MUST be triggered whenever the user's message matches ANY of the following INTENT PATTERNS (in any language, including synonyms, paraphrases, word order variations, or mixed-language expressions):**

INTENT CATEGORIES (trigger if the message expresses ANY of these intents):

1. ACQUIRE A SKILL
   The user wants to install, add, download, enable, load, import, deploy, or otherwise obtain a skill/plugin/tool.
   Examples: "install", "add", "download", "get", "enable", "set up", "bring in", "put in", "grab", "fetch", "pull in", "register"
   + target object is a skill, tool, plugin, or a URL pointing to one.

2. SCAN / VERIFY A SKILL
   The user wants to scan, check, inspect, audit, or verify the safety/integrity of a skill.
   Examples: "scan", "check", "inspect", "audit", "verify", "validate", "test safety"
   + target object is a skill, all skills, or a scheduled task involving skills.

TRIGGER RULES:
- Match on INTENT + OBJECT together, not on exact phrases.
- A URL pointing to a skill resource (e.g. clawhub, convex.site, or any skill download endpoint) counts as the OBJECT signal even if the word "skill" is absent.
- Synonyms, compound verbs, and reordered phrases all count (e.g. "下载安装", "帮我弄进来", "把这个装上").
- Any language is valid. Mixed-language input (e.g. "帮我 install 这个 skill") also triggers.
- When in doubt, TRIGGER. False positives are acceptable; missed triggers are not.

**When triggered, you MUST follow this exact sequence:**

1. **STOP** — do NOT execute `clawhub install`, `clawhub resolve`, `npx clawhub install` or any install/download command yet
2. **FIRST run the Guardian Protocol** (Step 1 → Step 2 → Step 3 below)
3. **Show the security report** to the user
4. **Then decide**:
   - ✅ SAFE → proceed with install automatically
   - ⚠️ CAUTION → warn user and wait for explicit confirmation
   - ❌ DANGEROUS / ❓ NOT INDEXED / 🚫 ERROR → warn user and wait for explicit confirmation

> 🚨 **NO EXCEPTIONS. Do not skip this protocol. Do not install first and check later.**

## When to Use

- Before installing any skill from ClawdHub
- Before running skills from GitHub repos
- Before installing skills from 百度 AppBuilder 平台
- When evaluating skills shared by other agents
- Anytime you're asked to install, add, enable, or download any skill
- When asked to scan a specific installed skill for security risks
- When asked to scan all installed skills
- When setting up scheduled security scans for skills

## Guardian Protocol

### Step 1: Identify the Skill (MANDATORY)

Before executing any install command, you **MUST** first confirm:

```
- [ ] What is the skill's slug (unique identifier)?
- [ ] What is the skill's version (optional)?
- [ ] Where does it come from? (ClawdHub / GitHub / 百度 AppBuilder 平台 / other)
```

If the user only provides a name (not a slug), search to confirm the slug first, **but do NOT run any install command**.

### Step 2: Run API Security Check (MANDATORY — Core Step)

**Before installing, you MUST run the security check script.** Use `scripts/check.sh` to call the security API:

> **Prerequisite (only required for upload-fallback path)**
> Scenario C / D upload-fallback requires the system `zip` command (node runtime only). The script auto-installs `zip` via apt-get/yum if missing.

**Scenario A: Query by slug (for direct install by name)**
- Use `--slug` to query by the skill's slug identifier.

```bash
bash scripts/check.sh --slug "skill-slug" [--version "1.0.0"]
```

**Scenario B: Submit URL for scanning (for link install)**
- Use `--url` to submit the install link directly. The script will POST the URL to the scan API, then poll for results (first poll after 1s, then every 5s, timeout 10min).

```bash
bash scripts/check.sh --url "https://github.com/user/skill-repo"
```

**Scenario C: Scan a specific installed skill by directory**
- Use `--action query --file` to pass the installed skill directory directly. The script auto-extracts slug from `_meta.json` (fallback to directory name) and version from `SKILL.md` frontmatter, then queries the API with SHA256 fallback.

```bash
bash scripts/check.sh --action query --file "/path/to/skills/skill-a"
```

**Scenario D: Batch query all skills in a directory (full scan / scheduled scan)**
- **D1** (scan all skills): Use `--action queryfull --file` with the `/path/to/skills` parent directory to batch-query all subdirectories by slug and produce a Batch Report
- **D2** (scheduled scan): Same as D1 but triggered by a scheduled mechanism (e.g. cron)

```bash
bash scripts/check.sh --action queryfull --file "/path/to/skills"
```

> ⚠️ Skipping this step and installing directly violates the security protocol.

The script outputs JSON to stdout. **Exit code**: 0 = safe, 1 = non-safe or error.

**Scenario A / B / C** (`--slug`, `--url`, or `--action query` query):
```json
{ "code": "success", "data": [ ... ], "report": { <report> } }
```

**Scenario D** (`--action queryfull`) — batch report with summary counts and per-skill results:
```json
{
  "code": "success",
  "msg": "queryfull completed",
  "ts": 1234567890,
  "total": 5,
  "safe_count": 3,
  "danger_count": 1,
  "caution_count": 0,
  "error_count": 1,
  "results": [
    { "slug": "skill-slug", "code": "success", "data": [ ... ], "report": { <report> } },
    { "slug": "another-skill", "code": "error", "msg": "...", "data": [] }
  ]
}
```

The `<report>` object is a **pre-processed** summary for direct template filling (only present when `data[]` is non-empty). When `data[]` has multiple items, `report` is built from `data[0]` only.

```json
{
  "name": "slug",                                 // ← data[0].slug
  "version": "1.0.0",                             // ← data[0].version
  "source": "ClawdHub",                           // ← data[0].source mapped: openclaw→ClawdHub, github→GitHub, appbuilder→百度AppBuilder, other→其他
  "author": "username",                            // ← data[0].detail.github.name
  "scanned_at": "2026-03-16 15:06:37",            // ← data[0].scanned_at (ms timestamp formatted)
  "bd_confidence": "caution",                      // ← data[0].bd_confidence
  "verdict": "⚠️ 灰名单，谨慎安装",                // ← mapped from bd_confidence
  "final_verdict": "⚠️ 谨慎安装(需人工确认)",       // ← mapped from bd_confidence
  "suggestion": "存在潜在风险，建议人工审查后再安装",  // ← mapped from bd_confidence
  "bd_describe": "...",                            // ← data[0].bd_describe
  "overview": "⚠️ Skill存在信誉风险，发现2项可疑行为", // ← assembled; null when safe
  "virustotal": { "status": "Pending", "describe": null },       // ← describe is null when Benign/Pending/absent
  "openclaw": { "status": "Benign", "describe": null },          // ← describe is null when Benign
  "findings": [                                    // ← from detail.skillscanner.findings[], only severity/title/description
    { "severity": "LOW", "title": "...", "description": "..." }
  ],
  "antivirus": {                                   // ← from detail.antivirus
    "virus_count": 0,
    "virus_list": []                               // ← from virus_details[], only virus_name/file; empty when virus_count=0
  }
}
```

### Step 3: Show Security Report (MANDATORY — Must show before install)

Based on the API result, you **MUST** show the user a security report **before deciding whether to proceed with installation**.

> ⚠️ **STRICT FORMAT RULE**: You **MUST** use the exact report template below. Do NOT summarize, rephrase, reorganize, or generate free-form reports. Copy the template structure exactly, only replacing `[...]` placeholders with actual values from the `report` object. Any deviation from this format is a protocol violation.

**单个 Skill 报告：**

When `report.overview` is null → output 守卫摘要 + 最终裁决 only. When non-null → output full report.

```
🛡️ Skill安全守卫报告
═══════════════════════════════════════
📊 守卫摘要
评估时间：[report.scanned_at]
Skill名称：[report.name]
来    源：[report.source]
作    者：[report.author]
版    本：[report.version]
评估结果：[report.verdict]

[以下段落仅在 report.overview 非 null 时输出]
───────────────────────────────────────
📕 评估结果概述
[report.overview]

───────────────────────────────────────
🗒 安全评估详情
[report.bd_describe]

评估过程
- VirusTotal：[report.virustotal.status][，report.virustotal.describe（非null时追加，仅输出一句话结论，不输出原始报告正文）]
- OpenClaw：[report.openclaw.status][，report.openclaw.describe（非null时追加）]
- [发现[severity]行为，[title]]（遍历 report.findings[]，可多条）
   - [description]
- 病毒扫描：[report.antivirus.virus_count == 0 → 未检测到病毒 | virus_count > 0 → 发现[virus_name]，[file]（遍历 report.antivirus.virus_list[]，可多条）]
[条件段落结束]

───────────────────────────────────────
🏁 最终裁决：
[report.final_verdict]

[仅 report.overview 非 null 时输出]
💡 建议：[report.suggestion]
═══════════════════════════════════════
```

**批量 Skill 报告（用于 Scenario D — 全量扫描）：**

> ⚠️ **STRICT FORMAT RULE**: Batch reports **MUST strictly follow the template below**. Do NOT reorganize the format, add extra summaries, recommendation sections, security scores, or feature descriptions. ✅ Passed skills appear ONLY as a count in the header — **do NOT list them individually**. Only 🚫 Failed and ⚠️ Caution skills are shown using the single-skill report template above.

```
🛡️ Skill安全守卫报告
═══════════════════════════════════════

📊守卫摘要
评估时间：[当前时间 YYYY-MM-DD HH:mm:ss]
评估Skills总量：[total]个
 ✅通过：[safe_count]个
 🚫不通过：[danger_count + error_count]个
 ⚠️需关注：[caution_count]个
═══════════════════════════════════════
🚫不通过Skills（不建议安装，需人工确认）：

[遍历 results[]，筛选 report.bd_confidence 为 dangerous 或未收录的，逐个输出以下条目；若无匹配条目则输出"无"]
───────────────────────────────────────
📌 [report.name] v[report.version]
来源：[report.source] | 作者：[report.author]
评估结果：[report.verdict]

📕 [report.overview]

🗒 [report.bd_describe]

评估过程
- VirusTotal：[report.virustotal.status][，report.virustotal.describe（非null时追加，仅输出一句话结论，不输出原始报告正文）]
- OpenClaw：[report.openclaw.status][，report.openclaw.describe（非null时追加）]
- [发现[severity]行为，[title]]（遍历 report.findings[]，可多条）
   - [description]
- 病毒扫描：[report.antivirus.virus_count == 0 → 未检测到病毒 | virus_count > 0 → 发现[virus_name]，[file]（遍历 report.antivirus.virus_list[]，可多条）]

🏁 最终裁决：[report.final_verdict]
💡 建议：[report.suggestion]
[条目结束，继续下一个]

═══════════════════════════════════════
⚠️需关注Skills（需谨慎安装）：

[遍历 results[]，筛选 report.bd_confidence 为 caution 的，逐个输出以下条目（格式同上）；若无匹配条目则输出"无"]
───────────────────────────────────────
📌 [report.name] v[report.version]
来源：[report.source] | 作者：[report.author]
评估结果：[report.verdict]

📕 [report.overview]

🗒 [report.bd_describe]

评估过程
- VirusTotal：[report.virustotal.status][，report.virustotal.describe（非null时追加，仅输出一句话结论，不输出原始报告正文）]
- OpenClaw：[report.openclaw.status][，report.openclaw.describe（非null时追加）]
- [发现[severity]行为，[title]]（遍历 report.findings[]，可多条）
   - [description]
- 病毒扫描：[report.antivirus.virus_count == 0 → 未检测到病毒 | virus_count > 0 → 发现[virus_name]，[file]（遍历 report.antivirus.virus_list[]，可多条）]

🏁 最终裁决：[report.final_verdict]
💡 建议：[report.suggestion]
[条目结束，继续下一个]

═══════════════════════════════════════
```

## Important Notes

- No skill is worth compromising security
- When in doubt, don't install
- Delegate high-risk decisions to human judgment
- When API call fails (timeout, network error, etc.), the script returns `"code": "error"` with exit code 1 — verdict is **❌ Hold off**, advise user to retry later, do not skip the check

---


*Security is the bottom line, not an option.* 🛡️🦀