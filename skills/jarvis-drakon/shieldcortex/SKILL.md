---
name: shieldcortex
description: >
  Persistent memory and security system for AI agents (ShieldCortex product).
  Use when: developing ShieldCortex features, writing ShieldCortex content/blogs,
  managing the ShieldCortex npm package or ClawHub skill, or answering questions
  about ShieldCortex capabilities. Covers memory persistence, semantic search,
  knowledge graphs, and the 6-layer security pipeline.
  Do NOT use when: the task is about OpenClaw's built-in memory search, general
  security auditing (use iron-dome), or unrelated products.
---

# ShieldCortex — Persistent Memory & Security for AI Agents

Give your AI agent a brain that persists between sessions — and protect it from memory poisoning attacks.

## Description

ShieldCortex is a complete memory system with built-in security. It gives AI agents persistent, intelligent memory with semantic search, knowledge graphs, decay-based forgetting, and contradiction detection. Every memory write passes through a 6-layer defence pipeline that blocks prompt injection, credential leaks, and poisoning attacks.

**Use when:**
- You want your agent to remember things between sessions (decisions, preferences, architecture, context)
- You need semantic search across past memories (not just keyword matching)
- You want automatic memory consolidation, decay, and cleanup
- You want knowledge graph extraction from memories (entities, relationships)
- You need to protect memory from prompt injection or poisoning attacks
- You want credential leak detection in memory writes
- You want to audit what's been stored in and retrieved from memory
- You want to scan agent instruction files (SKILL.md, .cursorrules, CLAUDE.md) for hidden threats

**Do NOT use when:**
- You only need simple key-value storage (use a config file)
- You want ephemeral session-only context (use the agent's built-in context window)
- You need a vector database for RAG pipelines (ShieldCortex is agent memory, not document retrieval)

## Prerequisites

- Node.js >= 18
- npm or pnpm

## Install

```bash
npm install -g shieldcortex
```

For OpenClaw integration (installs the cortex-memory hook):

```bash
npx shieldcortex openclaw install
```

For Claude Code / VS Code / Cursor MCP integration:

```bash
npx shieldcortex install
```

## Quick Start

### As an OpenClaw hook (automatic)

After `npx shieldcortex openclaw install`, the hook activates on next restart:

- **Auto-saves** important session context on compaction
- **Injects** relevant past memories on session start
- **"remember this: ..."** keyword trigger saves memories inline

### CLI Commands

```bash
# Check status
npx shieldcortex status

# Scan content for threats
npx shieldcortex scan "some text to check"

# Full security audit of your agent environment
npx shieldcortex audit

# Scan all installed skills/instruction files for hidden threats
npx shieldcortex scan-skills

# Scan a single skill file
npx shieldcortex scan-skill ./path/to/SKILL.md

# Build knowledge graph from existing memories
npx shieldcortex graph backfill

# Start the visual dashboard
npx shieldcortex --dashboard
```

### As a Library (programmatic)

```javascript
import {
  addMemory,
  getMemoryById,
  runDefencePipeline,
  scanSkill,
  extractFromMemory,
  consolidate,
  initDatabase
} from 'shieldcortex';

// Initialize
initDatabase('/path/to/memories.db');

// Add a memory (automatically passes through defence pipeline)
addMemory({
  title: 'API uses OAuth2',
  content: 'The payment API requires OAuth2 bearer tokens, not API keys',
  category: 'architecture',
  importance: 'high',
  project: 'my-project'
});

// Scan content before processing
const result = runDefencePipeline(untrustedContent, 'Email Import', {
  type: 'external',
  identifier: 'email-scanner'
});

if (result.allowed) {
  // Safe to process
}

// Extract knowledge graph entities
const { entities, triples } = extractFromMemory(
  'Database Migration',
  'We switched from MySQL to PostgreSQL for the auth service',
  'architecture'
);
// entities: [{name: 'MySQL', type: 'service'}, {name: 'PostgreSQL', type: 'service'}, ...]
// triples: [{subject: 'auth service', predicate: 'uses', object: 'PostgreSQL'}, ...]
```

## Memory System Features

| Feature | Description |
|---------|-------------|
| **Persistent Storage** | SQLite-backed, survives restarts and compaction |
| **Semantic Search** | Find memories by meaning, not just keywords |
| **Project Scoping** | Isolate memories per project/workspace |
| **Importance Levels** | Critical, high, normal, low with auto-decay |
| **Categories** | Architecture, decisions, preferences, context, learnings, errors |
| **Decay & Forgetting** | Old, unaccessed memories fade — like a real brain |
| **Consolidation** | Automatic merging of similar/duplicate memories |
| **Contradiction Detection** | Flags when new memories conflict with existing ones |
| **Knowledge Graph** | Extracts entities and relationships from memories |
| **Activation Scoring** | Recently accessed memories get retrieval priority |
| **Salience Scoring** | Important memories surface first in search |

## Security Features

| Layer | Protection |
|-------|-----------|
| **Input Sanitisation** | Strip control characters, null bytes, dangerous formatting |
| **Pattern Detection** | Regex matching for known injection patterns |
| **Anomaly Scoring** | Entropy analysis, behavioural deviation detection |
| **Credential Leak Detection** | Blocks API keys, tokens, private keys (25+ patterns, 11 providers) |
| **Trust Scoring** | Source-based reliability scoring for memory writes |
| **Audit Trail** | Full forensic log of every memory operation |
| **Skill Scanner** | Detect prompt injection in SKILL.md, .cursorrules, CLAUDE.md |

## ShieldCortex Cloud (Optional)

Sync audit data to a team dashboard for cross-project visibility:

```bash
npx shieldcortex config set-api-key <your-key>
```

Free local package is unlimited. Cloud adds team dashboards, audit aggregation, and alerts.

## Links

- **npm:** https://www.npmjs.com/package/shieldcortex
- **GitHub:** https://github.com/Drakon-Systems-Ltd/ShieldCortex
- **Website:** https://shieldcortex.ai
- **Docs:** https://github.com/Drakon-Systems-Ltd/ShieldCortex#readme

## 70 Exported APIs

The library exports 70 named functions and types covering defence, memory, knowledge graph, skill scanning, and audit. Full list in the [CHANGELOG](https://github.com/Drakon-Systems-Ltd/ShieldCortex/blob/main/CHANGELOG.md#2100---2026-02-13).

## v4.x Features (v4.0.0 – v4.4.0)

### Memory Intelligence
| Feature | Description |
|---------|-------------|
| **Memory Types** | `user`, `feedback`, `project`, `reference` — typed memories with validation |
| **Staleness Scoring** | Age-based decay with warnings on old memories |
| **LLM-Powered Reranking** | Hybrid recall: embedding search + LLM reranker for precision |
| **Dream Mode** | Background memory consolidation (`shieldcortex consolidate`) — like sleep for AI |
| **Memory Scopes** | `private` vs `team` for multi-agent deployments |
| **Positive Feedback** | `shieldcortex cortex confirm` — learn from success, not just mistakes |
| **Save Filtering** | Blocks saving derivable info (file paths, git refs) |

### X-Ray Security Scanner (v4.3.0+)

On-demand security scanning for files, directories, plugins, and npm packages:

```bash
# Scan a local file or directory
shieldcortex xray ./path

# Deep scan an npm package (registry + local)
shieldcortex xray some-package --deep

# CI/CD pipeline gate
shieldcortex xray --ci --threshold=HIGH

# Continuous file monitoring
shieldcortex xray --watch

# npm pre-install hook
shieldcortex xray-preinstall
```

**X-Ray detects:**
- `eval`/`exec` and shell execution patterns
- AI directives and prompt injection
- Steganography indicators and obfuscation
- Unicode tricks and homoglyph attacks
- Network beacons and persistence hooks
- Dependency risk scoring
- Typosquat detection (e.g. `axois` → `axios`)
- Suspicious postinstall scripts

**Trust score:** 0–100 with SAFE / LOW / MEDIUM / HIGH / CRITICAL ratings.

**Memory Guard:** Auto-scans content before agent memory writes (via OpenClaw plugin).

Free tier: 5 local scans/day. Pro: unlimited + deep npm registry scan.
