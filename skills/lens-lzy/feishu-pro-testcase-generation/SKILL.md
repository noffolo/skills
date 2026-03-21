---
name: feishu-testcase-writer
description: Read Feishu/Lark requirement documents from online doc links, decompose modules and business rules into review-ready QA test cases, and save the output into a new Feishu cloud doc. Use when Codex needs to help testers draft structured test cases in the team's approved style for list pages, detail pages, field rules, calculations, permissions, status flows, save/confirm/audit checks, and evidence placeholders.
---

# Feishu Testcase Writer

## Overview

Turn a Feishu requirement doc link into a structured QA testcase document that matches the team's reviewed style: hierarchical headings, page-by-page decomposition, field-level rules, logic validation, and explicit placeholders for execution evidence.

Read [references/reviewed-style.md](references/reviewed-style.md) before drafting. Read [references/doc-template.md](references/doc-template.md) when you are about to write the final Feishu doc.

## Workflow

### 1. Confirm scope from the requirement link

- Accept a Feishu or Lark online requirement doc link as the primary source.
- If multiple links are provided, treat the first requirement link as the main source and use the rest as supplements.
- Read the document first. Do not ask the user to paste the full content unless the link is inaccessible.
- If the user names a specific module, generate only that module's testcases.
- If the document is long, extract:
  - feature/module names
  - menu path or entry path
  - user roles and organization scope
  - list page behavior
  - detail page fields and tabs
  - data sources and downstream dependencies
  - formulas, linkage rules, and recalculation rules
  - state transitions and button visibility
  - save, confirm, audit, reverse-audit, void, and duplicate-check rules
  - open questions or requirement conflicts

### 2. Discover available Feishu tools before acting

- Prefer tool discovery over hard-coding tool names.
- Look for tools that can do the following:
  - open or fetch a Feishu/Lark doc from a link
  - read structured document blocks or export document content
  - create a new Feishu cloud doc
  - append blocks, headings, callouts, code blocks, tables, and images
  - optionally create the doc inside a specified folder or space
- If tool names are explicit in the environment, use them.
- If no Feishu-reading tool is available, tell the user what is missing and ask for pasted content instead of inventing access.
- If no Feishu-writing tool is available, output the finished Markdown content directly and state that saving to Feishu could not be completed.

### 3. Rebuild the requirement as a testcase tree

Draft the testcase structure in the same decomposition style used by the reviewed samples:

- Start from menu/module level.
- Break each module into:
  - list page
  - detail page
  - process validation
  - logic validation
- Under list pages, cover:
  - displayed columns
  - filter/search conditions
  - default sorting
  - operation buttons
  - organization or permission filtering
- Under detail pages, break down by:
  - header fields
  - detail grids/tabs
  - calculated fields
  - linked or derived fields
  - import/export or batch behavior if present
- For each field or rule, capture only the dimensions that are supported by the requirement:
  - label and location
  - required/optional
  - editable/read-only
  - control type
  - default value
  - value range, length, precision, format, enum
  - data source
  - linkage or refresh rule
  - formula or derivation
  - permission limit
  - boundary and abnormal cases

### 4. Write only executable testcase content

- Do not fabricate execution results, screenshots, validation data, or SQL.
- Default output mode is `testcase-design`, not `test-execution-result`.
- Preserve the reviewed document style by adding empty evidence sections where appropriate:
  - `测试结果：待执行`
  - `验证数据：待补充`
  - `相应SQL：待补充`
- If the user later provides execution evidence, update the same document instead of generating fake evidence.
- Every testcase item must be concrete. Avoid vague phrases such as “验证成功” or “正常显示”.
- When the requirement states a formula, copy the formula in normalized plain language and explain what inputs drive it.
- When the requirement is ambiguous, add a separate `需求确认项` section instead of guessing.

### 5. Use the reviewed heading style for the final document

Match the team's preferred document shape:

- top title with date and requirement name
- source requirement link near the top
- one first-level heading per module, for example `1. 饲料厂差价调整`
- tester name only when the user provides it or it is already in the source
- menu path when available
- second-level headings such as `1.1 列表页`, `1.2 详情页`, `1.3 逻辑校验`
- deeper levels for fields, rules, and branches, for example `2.2.1.3 组织`
- highlight key rules using callouts or block quotes instead of burying them in paragraphs
- use screenshots only when available from the source or from later execution evidence

Follow [references/doc-template.md](references/doc-template.md) for the default scaffold.

### 6. Save into a new Feishu cloud doc

- Create a new Feishu doc after the testcase content is complete.
- Default title format:
  - `{YYYYMMDD}-{需求简称}-测试用例`
- If the user provides a target folder or space, save there.
- If the user does not provide a folder and the tool requires one, ask only for that missing destination.
- Write the content as structured headings and blocks, not as one giant pasted paragraph.
- After writing, return:
  - the new Feishu doc title
  - the new Feishu doc link if available
  - a short summary of what was covered
  - any `需求确认项`

## Quality Gate

Before finalizing, verify all of the following:

- The output is based only on the requirement source and standard QA coverage heuristics.
- Every major module is decomposed into pages, fields, and logic checks rather than a flat list.
- Each important field includes the non-obvious rules that make it testable.
- Logic validation covers the actual lifecycle mentioned by the requirement.
- Permission, organization, and state-dependent behavior are not omitted.
- The doc contains no invented screenshots, SQL, query results, or execution conclusions.
- Open questions are isolated in `需求确认项`.

## Output Rules

- Prefer Chinese unless the user explicitly asks for English.
- Prefer headings and short rule bullets over large Markdown tables.
- Use tables only for compact matrices such as enum values, permission combinations, or ambiguity lists.
- Keep numbering stable and hierarchical.
- When a rule repeats across similar branches, reference the earlier numbered subsection instead of duplicating the full text.
- When the source requirement is weak, generate the smallest defensible testcase set and clearly label missing inputs.

## Minimal fallback

If the Feishu link cannot be read but the user still wants immediate help:

1. Ask for the requirement content or screenshots.
2. Continue using the same reviewed-style testcase structure.
3. Make it explicit that the source switched from online doc reading to user-pasted content.
