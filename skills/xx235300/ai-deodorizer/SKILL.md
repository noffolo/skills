---
name: ai-deodorizer
version: 1.0.0
description: |
  Remove signs of AI-generated writing from text, making it sound more natural and human-written.
  Based on 25 AI writing pattern detectors + two-round rewriting strategy + Soul injection principles.
  Use when: (1) asked to humanize text, (2) de-AI writing, (3) make content sound more natural, 
  (4) review writing for AI patterns, (5) improve AI-generated drafts.
  Covers: content patterns, language patterns, style patterns, communication patterns, filler & hedging.
author: xx235300
homepage: https://github.com/xx235300/ai-deodorizer
source: https://github.com/xx235300/ai-deodorizer
tags:
  - text-processing
  - writing-improvement
  - ai-detection
  - nlp
  - chinese
allowed-tools:
  - Read
  - Write
  - Edit
---

# Ai-Deodorizer: Remove AI Writing Patterns

> Author: xx235300 | License: MIT | Based on Wikipedia "Signs of AI writing"

## Overview

Ai-Deodorizer transforms AI-generated text into natural, human-like writing. It uses a **two-round rewriting strategy**:

1. **Round 1 - Pattern Fix**: Identify and fix 25 common AI writing patterns
2. **Round 2 - Anti-AI Audit**: Ask "what still looks AI?" and fix remaining tells

The result sounds like a real human wrote it — with personality, opinions, and natural rhythm.

## Usage

### Basic Usage

```
Please humanize this text:

[paste your AI-generated text here]
```

### With File Input

```
Please humanize the content of this file: /path/to/file.txt
```

### With Strength Mode

```
Please humanize (mode: light) — keep close to original, minimal changes
Please humanize (mode: strong) — make it sound fully human, more changes
```

## Key Features

- **25 AI Pattern Detectors** across 5 categories
- **Two-Round Rewriting** — pattern fix + anti-AI audit
- **Soul Injection** — adds human voice, not just cleaning
- **Chinese Language Support** — built-in Chinese AI vocabulary table

## Supported Pattern Categories

### Content Patterns (6 types)
Significance inflation, notability name-dropping, superficial -ing analyses, promotional language, vague attributions, formulaic challenges

### Language Patterns (6 types)
AI vocabulary, copula avoidance, negative parallelisms, rule of three abuse, synonym cycling, false ranges

### Style Patterns (6 types)
Em dash overuse, boldface overuse, inline-header lists, title case headings, emoji abuse, curly quotes

### Communication Patterns (3 types)
Chatbot artifacts, cutoff disclaimers, sycophantic tone

### Filler & Hedging (4 types)
Filler phrases, over-hedging, generic positive conclusions, zombie templates

## Soul Injection Principles

Good writing has a human behind it. Beyond cleaning patterns:

- **Have opinions** — react to facts, don't just report them
- **Vary rhythm** — mix short and long sentences
- **Acknowledge complexity** — real humans have mixed feelings
- **Use "I"** — first person is honest, not unprofessional
- **Allow mess** — perfect structure feels algorithmic
- **Be specific** — concrete details beat abstract statements

## Environment Setup

This skill requires a compatible LLM API. Set the following environment variables:

- `MINIMAX_API_KEY` — Your API key (required)
- `API_BASE` — API base URL (optional, defaults to MiniMax endpoint)
- `MODEL` — Model name (optional, defaults to MiniMax-M2.7)

## Disclaimer

**Disclaimer**:
This project is 99% AI-generated. The AI's owner has no programming background. Please evaluate the project's feasibility before use.
