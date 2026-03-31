# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**sg-maid-search** is a free AI Agent Skill that lets employers in Singapore query the Sunrise Link domestic maid database through AI agents (Claude, Cursor, GitHub Copilot, etc.). It acts as a lead generation tool — skill handles candidate screening, conversion happens on `sunriselink.sg`.

## Architecture

**Target structure** (minimal, zero-dependency skill package):

```
sg-maid-search/
├── SKILL.md                       # Skill entry point: YAML frontmatter + agent behavior instructions
├── scripts/
│   └── search_maids.mjs         # Query script: Node.js 18+ ESM, no third-party dependencies
├── references/
│   └── field_guide.md             # Field documentation: loaded on-demand by agents
├── README.md
└── LICENSE
```

The skill calls a public API endpoint on the Sunrise Link website: `GET https://www.sunriselink.sg/api/public/v1/helpers` — rate-limited (20 req/IP/min, 10-min cooldown on breach), cached 60s

## Key Design Constraints

**Privacy-first:** Never expose PII fields — name, photo_url, dateOfBirth, placeOfBirth, homeCountryAddress, homeCountryContact, allergies, illnesses, physicalDisabilities, employer feedback, health records. 

**Zero dependencies:** `search_maids.mjs` must use only native Node.js 18+ APIs (`fetch` built-in). No `npm install` required for skill users.

**Only available maids:** API filters `status = 'available'` AND `is_deleted = false` — never expose unavailable or deleted candidates.

## API Query Parameters

`GET /api/public/v1/helpers` accepts the following **URL query string** parameters (all optional):

| Parameter | Type | Example |
|-----------|------|---------|
| `nationality` | string | `Philippines` |
| `religion` | string | `Buddhism` |
| `languages` | string (repeat for multiple) | `languages=English&languages=Tagalog` |
| `minAge` | integer ≥ 0 | `25` |
| `maxAge` | integer ≥ 0 | `40` |
| `minSalary` | number ≥ 0 | `600` |
| `maxSalary` | number ≥ 0 | `700` |
| `hasSgExperience` | `true` \| `false` | `true` |
| `needsInfantCare` | `true` \| `false` | `true` |
| `needsExperiencedInfantCare` | `true` \| `false` | `true` |
| `needsElderlyCare` | `true` \| `false` | `true` |
| `needsExperiencedElderlyCare` | `true` \| `false` | `true` |
| `needsDisabledCare` | `true` \| `false` | `true` |
| `needsCooking` | `true` \| `false` | `true` |
| `needsExperiencedCooking` | `true` \| `false` | `true` |
| `needsHousework` | `true` \| `false` | `true` |

Example request:

```
GET /api/public/v1/helpers?nationality=Philippines&minSalary=600&maxSalary=700&needsInfantCare=true
```

## API Response Structure

```jsonc
{
  "totalFound": 12,          // total matching candidates in database
  "returned": 5,             // number returned
  "candidates": [
    {
      "id": 42,
      "uuid": "a1b2c3d4-...",
      "age": 28,                          // number | null
      "nationality": "Philippines",       // string | null
      "religion": "Christianity",         // string | null
      "salary": 650,                      // number | null (SGD/month)
      "loan": 800,                        // number | null (SGD)
      "loanPeriodMonths": 10,             // number | null
      "educationLevel": "Secondary school", // string | null
      "maritalStatus": "Single",          // string | null
      "monthlyRestDays": 4,              // number | null
      "hasSgExperience": true,            // boolean | null
      "languages": ["English", "Tagalog"],
      "interviewAvailability": "byVideo", // string | null
      "skills": {                         // object | null
        "sgEvaluated": {
          "infantsChildren": { "willingness": true, "experienced": true, "ageRange": "0-6" },
          "elderly":         { "willingness": true, "experienced": false },
          "disabled":        { "willingness": false, "experienced": false },
          "housework":       { "willingness": true, "experienced": true },
          "cooking":         { "willingness": true, "experienced": true, "cuisines": ["Chinese", "Western"] }
        },
        "overseasEvaluated": { /* same structure as sgEvaluated */ }
      },
      "workExperience": [
        { "country": "Malaysia", "workDuties": "infant care, housekeeping", "dateFrom": "2021-01", "dateTo": "2023-06" }
      ],
      "profileUrl": "https://www.sunriselink.sg/helpers/{uuid}?utm_source=agent-skill&utm_medium=skill&utm_campaign=sg-maid-search"
    }
  ]
}
```
