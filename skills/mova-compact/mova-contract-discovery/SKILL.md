---
name: mova-contract-discovery
description: Browse, search, and run public MOVA contracts from the community marketplace. Trigger when the user asks to find a contract, discover available contracts, search for workflows, or wants to run a public contract from another organization.
license: MIT-0
---

> **Ecosystem Skill** — Supports building and managing the MOVA ecosystem. Requires the `openclaw-mova` plugin.

# MOVA Contract Discovery

Browse the public MOVA contract marketplace — find contracts published by any organization, inspect their stats, and run them directly.

## What this skill does

1. Searches the public contract catalog with optional keyword and execution mode filters
2. Shows contract details: title, version, execution mode, pass rate, total runs
3. Runs any public contract on behalf of the user's org
4. Surfaces HITL gates if the contract requires human decisions

---

## When to trigger

Activate when the user:
- Says "find a contract", "search contracts", "what contracts are available"
- Asks for a specific type of workflow (e.g. "is there a contract for invoice approval?")
- Wants to run a contract that isn't their own
- Asks to browse the MOVA marketplace

---

## Step 1 — Search

Ask:

> "What are you looking for? You can describe a workflow type (e.g. invoice, AML, compliance, credit scoring) or say 'show all' to see everything."

Call tool `mova_discover_contracts` with:
- `keyword`: user's search term (omit if "show all")
- `execution_mode`: only if user specifically wants to filter by mode

Show results as a table:

```
Found N contracts:

#  Title                     Version  Mode           Runs   Pass Rate
1  Invoice Approval Agent    1.0.0    human_gated    142    94%
2  AML Alert Triage          2.1.0    ai_assisted    87     91%
3  Supply Chain Risk Screen  1.2.0    human_gated    34     88%
```

If no results — suggest a broader search or different keyword.

---

## Step 2 — Inspect

If the user wants more detail on a contract, show the full manifest:

```
CONTRACT: Invoice Approval Agent
ID:             ctr-usr-abc123
Owner org:      org-xyz
Version:        1.0.0
Execution mode: human_gated
Description:    Approves invoices over €5,000 with OCR extraction and CFO sign-off gate
Runs:           142 total  •  94% pass rate
Registered:     2026-03-15
```

---

## Step 3 — Run

Ask:

> "Want to run [contract title]? Do you have inputs to provide, or should we start with empty inputs?"

Collect inputs as key-value pairs if needed (ask one at a time).

Call tool `mova_run_contract` with:
- `contract_id`: from the discovery results
- `inputs`: collected or `{}`

**If `status: "waiting_human"`** — the contract has a human gate. Show the analysis and options, then ask the user to choose. Call `mova_hitl_decide` with:
- `contract_id`: same contract_id
- `option`: chosen option
- `reason`: user's reasoning

**If `status: "completed"`** — show verdict and output.

**If `status: "failed"`** — show the error. Suggest checking the contract's required connectors with `mova_list_connectors`.

---

## Step 4 — Check run status

If the user wants to follow up on a previous run:

Call `mova_run_status` with the `run_id`.

---

## Execution mode guide

Show this when the user asks what execution modes mean:

| Mode | What it means |
|---|---|
| `deterministic` | Rule-based, same output for same input every time |
| `bounded_variance` | AI-assisted but constrained to narrow output range |
| `ai_assisted` | AI makes decisions, no mandatory human gate |
| `human_gated` | AI analyzes, human must approve before completion |

---

## Rules

- NEVER run a contract without confirming with the user first: "Run [title]?"
- NEVER invent contract IDs — use only IDs from `mova_discover_contracts` results
- NEVER guess inputs — ask the user, or confirm empty inputs are acceptable
- If the contract has a human gate (`status: "waiting_human"`), always show the analysis before asking for the decision
- `contract_id` for `mova_run_contract` and `mova_hitl_decide` comes from the discovery result, not from the contract title
