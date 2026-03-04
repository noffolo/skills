---
name: drip-billing
description: Track AI agent usage and costs with Drip metered billing.
license: MIT
compatibility: Requires Node.js 18+, npm, and DRIP_API_KEY. Optional: DRIP_BASE_URL, DRIP_WORKFLOW_ID. (Node 24.x if developing the Drip monorepo)
provenance:
  npmPackage: https://www.npmjs.com/package/@drip-sdk/node
  sourceRepository: https://github.com/MichaelLevin5908/drip
credentials:
  primary: DRIP_API_KEY
  keyTypes:
    - prefix: "pk_live_"
      scope: "Usage tracking, customers, billing, analytics, sessions"
      recommended: true
    - prefix: "pk_test_"
      scope: "Same as pk_live_ but on testnet"
      recommended: true
    - prefix: "sk_live_"
      scope: "Full API access — all endpoints including webhooks, key management, feature flags"
      recommended: false
    - prefix: "sk_test_"
      scope: "Same as sk_live_ but on testnet"
      recommended: false
  leastPrivilege: "Use pk_ (public) keys for usage tracking and billing. Only use sk_ (secret) keys if you need webhook management, API key rotation, or feature flags. Never expose sk_ keys to untrusted agents, client apps, or third-party runtimes."
requiredEnvVars:
  - name: DRIP_API_KEY
    description: "Required API key from the Drip dashboard. Use a public key (pk_live_... or pk_test_...) for usage tracking. Only use a secret key (sk_live_... or sk_test_...) for trusted server-side admin operations."
    required: true
  - name: DRIP_BASE_URL
    description: Optional trusted Drip API base URL used for telemetry emission.
    required: false
  - name: DRIP_WORKFLOW_ID
    description: Optional workflow identifier for run telemetry.
    required: false
dataSent:
  - "Usage quantities (meter name + numeric quantity)"
  - "Customer identifiers (customerId, externalCustomerId)"
  - "Run lifecycle events (start, end, status, duration)"
  - "Sanitized metadata for diagnostics (for example model family, tool name, status code, latency, hashed IDs)"
dataNotSent:
  - "Raw prompts, completions, or model outputs"
  - "Environment variables, secrets, or credentials"
  - "Raw request/response bodies, file contents, or source code"
securityNotes:
  - "Never include PII, secrets, passwords, API keys, or raw user content in metadata fields"
  - "Use a strict metadata allowlist and redaction policy before emitting telemetry"
  - "Prefer pk_ (public) keys which cannot manage webhooks, rotate API keys, or toggle feature flags"
  - "Never provide sk_ (secret) keys to untrusted agents, browsers, mobile clients, or third-party execution environments"
  - "Verify the @drip-sdk/node package on npm before installing: https://www.npmjs.com/package/@drip-sdk/node"
metadata:
  author: drip
  version: "1.2"
---

# Drip Billing Integration

Track usage and costs for AI agents, LLM calls, tool invocations, and any metered workload.

## When to Use This Skill

- Recording LLM usage quantities (for example total tokens per call)
- Tracking tool/function call costs
- Logging agent execution traces
- Metering API requests for billing
- Attributing costs to customers or workflows

## Security & Data Privacy

**Key scoping (least privilege):**
- Use **`pk_` (public) keys** for usage tracking, customer management, and billing. This is sufficient for all skill operations.
- Only use **`sk_` (secret) keys** if you need admin operations: webhook management, API key rotation, or feature flags.
- Never provide `sk_` keys to untrusted agents, browser/mobile clients, or third-party hosted runtimes.
- Public keys (`pk_`) cannot manage webhooks, rotate API keys, or toggle feature flags — this limits blast radius if the key is compromised.

**Metadata safety:**
- Include only minimal non-sensitive operational context in metadata.
- Never include PII, secrets, passwords, API keys, raw user prompts, model outputs, or full request/response bodies.
- Use a strict allowlist and redaction policy before telemetry writes.
- Prefer hashes/IDs (for example `queryHash`) instead of raw user text.

**What data is transmitted:**
- Usage quantities (meter name + numeric value)
- Customer identifiers
- Run lifecycle events (start/end, status, duration)
- Sanitized metadata you explicitly provide (model family, tool name, status code, latency, hashed IDs)

**What is NOT transmitted:**
- Raw prompts, completions, or model outputs
- Environment variables or secrets
- File contents or source code

## Installation

```bash
npm install @drip-sdk/node
```

## Provenance & Install Policy

- Install from the official npm package only: `@drip-sdk/node`.
- Prefer pinned versions in project manifests and lockfiles.
- Do not run remote package execution flows (`npx <package>`) in this skill.
- Before supplying credentials, verify package source and published version:
  - npm: https://www.npmjs.com/package/@drip-sdk/node
  - source: https://github.com/MichaelLevin5908/drip
  - sdk source (node): https://github.com/MichaelLevin5908/drip-sdk
  - sdk source (python): https://github.com/MichaelLevin5908/drip-sdk-python

## Environment Setup

```bash
# Recommended: public key — sufficient for all usage tracking and billing
export DRIP_API_KEY=pk_live_...

# Get a free api key from the Drip website: https://drippay.dev/

# Optional: trusted API base URL override
# export DRIP_BASE_URL=https://api.drippay.dev/v1

# Optional: workflow grouping default for run telemetry
# export DRIP_WORKFLOW_ID=research-agent

# Only if you need admin operations (webhooks, key management, feature flags):
# export DRIP_API_KEY=sk_live_...
```

## Telemetry Safety Contract

- Send only metadata needed for billing and diagnostics.
- Do not send raw prompts, raw model outputs, raw query text, full request/response bodies, or credentials.
- Prefer stable identifiers and hashes (for example `queryHash`) over raw user content.
- Emit telemetry only to a trusted `DRIP_BASE_URL`.
- Before enabling auto-tracking in production, verify the installed handler/middleware implementation still sanitizes metadata (allowlist filtering, key redaction, non-primitive dropping, string truncation).
- LangChain auto-tracking emits counts and hashes (for example `promptCount`, `queryHash`) instead of raw prompt/query/output previews.
- Always pass explicit `metadataAllowlist` and `redactMetadataKeys` values for high-sensitivity workloads; do not rely only on defaults.

## Quick Start

### 1. Initialize the SDK

```typescript
import { Drip } from '@drip-sdk/node';

// Reads DRIP_API_KEY from environment automatically (pk_live_... recommended)
const drip = new Drip({
  apiKey: process.env.DRIP_API_KEY,
  baseUrl: process.env.DRIP_BASE_URL,
});
```

### 2. Track Usage (Simple)

```typescript
await drip.trackUsage({
  customerId: 'customer_123',
  meter: 'llm_tokens',
  quantity: 1500,
  // metadata is optional — only include operational context, never PII or secrets
  metadata: { model: 'gpt-4' }
});
```

### 3. Record Agent Runs (Complete Execution)

```typescript
await drip.recordRun({
  customerId: 'cus_123',
  workflow: 'research-agent',
  events: [
    { eventType: 'llm.call', model: 'gpt-4', quantity: 1700, units: 'tokens' },
    { eventType: 'tool.call', name: 'web-search', duration: 1500 },
    { eventType: 'llm.call', model: 'gpt-4', quantity: 1000, units: 'tokens' },
  ],
  status: 'COMPLETED',
});
```

### 4. Streaming Execution (Real-Time)

```typescript
// Start the run
const run = await drip.startRun({
  customerId: 'cus_123',
  workflowId: process.env.DRIP_WORKFLOW_ID ?? 'document-processor',
});

// Log each step as it happens
await drip.emitEvent({
  runId: run.id,
  eventType: 'llm.call',
  model: 'gpt-4',
  quantity: 1700,
  units: 'tokens',
});

await drip.emitEvent({
  runId: run.id,
  eventType: 'tool.call',
  name: 'web-search',
  duration: 1500,
});

// Complete the run
await drip.endRun(run.id, { status: 'COMPLETED' });
```

## Event Types

| Event Type | Description | Key Fields |
|------------|-------------|------------|
| `llm.call` | LLM API call | `model`, `quantity`, `units` |
| `tool.call` | Tool invocation | `name`, `duration`, `status` |
| `agent.plan` | Planning step | `description` |
| `agent.execute` | Execution step | `description`, `metadata` |
| `error` | Error occurred | `description`, `metadata` |

## Common Patterns

### Wrap Tool Calls

```typescript
async function trackedToolCall<T>(runId: string, toolName: string, fn: () => Promise<T>): Promise<T> {
  const start = Date.now();
  try {
    const result = await fn();
    await drip.emitEvent({
      runId,
      eventType: 'tool.call',
      name: toolName,
      duration: Date.now() - start,
      status: 'success',
    });
    return result;
  } catch (error: unknown) {
    const message = error instanceof Error ? error.message : 'Unknown error';
    await drip.emitEvent({
      runId,
      eventType: 'tool.call',
      name: toolName,
      duration: Date.now() - start,
      status: 'error',
      // Only include the error message — never include stack traces, env vars, or user data
      metadata: { error: message },
    });
    throw error;
  }
}
```

### LangChain Auto-Tracking

```typescript
import { DripCallbackHandler } from '@drip-sdk/node/langchain';

const handler = new DripCallbackHandler({
  apiKey: process.env.DRIP_API_KEY,
  baseUrl: process.env.DRIP_BASE_URL,
  customerId: 'cus_123',
  workflow: process.env.DRIP_WORKFLOW_ID ?? 'research-agent',
  metadata: { integration: 'langchain' },
  metadataAllowlist: ['integration', 'model', 'latencyMs', 'promptCount', 'queryHash', 'statusCode'],
  redactMetadataKeys: ['prompt', 'input', 'output', 'response', 'apiKey', 'token', 'authorization'],
});

// All LLM calls and tool usage automatically tracked
const result = await agent.invoke(
  { input: 'Research the latest AI news' },
  { callbacks: [handler] }
);
```

## API Reference

See [references/API.md](references/API.md) for complete SDK documentation.
