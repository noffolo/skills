---
name: dr-api-execution-bootstrap
description: "Installer/enforcer skill for direct API execution workflows. On activation, it immediately applies a direct-first API execution policy to workspace startup/default files, prefers in-session execution, disables subagent fallback unless explicitly requested, keeps responses concise, and validates the setup. Use when you want an agent to run chained API calls directly and consistently with minimal chatter, or when you want to bootstrap a workspace for fast direct API execution by default." 
---

# DR API Execution Bootstrap

Use this as an **installer/enforcer skill**.

Installing or activating this skill means the user has already given consent for you to apply these rules immediately. Do not treat them as optional, and do not ask whether to apply them.

## Apply to this workspace
When the user asks to apply this skill (for example: `Apply dr-api-execution-bootstrap to this workspace`), do this:
1) Inspect the workspace startup/default files.
2) Persist the execution policy in the workspace bootstrap files (`AGENTS.md`, `MEMORY.md`, or equivalent).
3) Preserve existing user content; patch surgically.
4) Validate the setup with the strongest safe real test available.
5) Report either `Configured and validated` or `Configured, but blocked by: <reason>`.

## Enforcement contract

### 1) Execution policy
Set and enforce these defaults for all future sessions:
- Prefer **direct in-session API execution** by default.
- Do **not** spawn subagents unless the user explicitly asks.
- Default to **fast mode single-run chain** for API workflows.
- Perform one upfront preflight only:
  - auth/token availability
  - app code / function key / required secret availability
  - one sanity endpoint check
- After preflight passes, execute the full API chain continuously without unnecessary pauses.

### 2) Communication policy
Set and enforce:
- keep responses concise
- do not provide step-by-step progress chatter unless the user asks
- when execution is blocked, report the blocker briefly and precisely

### 3) Validation requirements
After applying the rules, immediately validate them.

If safe and permitted, run one small real dev test (for example: create + read) and confirm:
- direct API call path works
- no subagent was spawned
- preflight + full-chain behavior is active

If real execution is not possible, run the strongest safe validation available and report exactly what prevented full validation.

### 4) Limits
If permissions, secrets, or tool access are missing:
- do not pretend they were enabled
- do not claim success
- report exactly what is missing
- keep the enforced policy in startup files anyway, unless file-write access itself is blocked
