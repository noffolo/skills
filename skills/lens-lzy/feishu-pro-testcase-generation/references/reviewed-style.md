# Reviewed Style Notes

This reference captures the shared characteristics observed from the three approved sample files:

- `/Users/liuzy53/Downloads/20250320-猪场管家【饲料考核】-测试结果.pdf`
- `/Users/liuzy53/Downloads/whiteboard_exported_image (1).pdf`
- `/Users/liuzy53/Downloads/whiteboard_exported_image.pdf`

Use these rules to keep the generated testcase document aligned with the team's expectations.

## 1. Overall structure is hierarchical, not spreadsheet-first

The approved samples use a layered heading tree instead of a flat testcase table:

- module or menu
- list page
- detail page
- field or tab
- sub-rule
- lifecycle or logic validation

Example pattern:

```text
2. 饲料厂差价调整
2.1 列表页
2.2 详情页
2.2.1 表头
2.2.1.3 组织
2.2.1.3.1 默认为当前组织
2.3 逻辑校验
2.3.1 保存时重复校验
```

Do not collapse everything into one table unless the user explicitly asks for table output.

## 2. Test design starts from a mind-map style decomposition

The whiteboard samples show the real thinking pattern before the final document is written:

- start from the feature root
- split by page area and business area
- keep breaking down until the leaf node is directly testable
- annotate special rules, risks, and requirement changes near the leaf node

This means the skill should internally think in a tree before writing the document.

## 3. Coverage is field-deep, not page-shallow

For each important field or grid column, the reviewed samples tend to capture several of these dimensions:

- required or optional
- editable or read-only
- default value
- data source
- precision, length, format, enum, or unit
- formula or system derivation
- permission limit
- visibility condition
- linked recalculation behavior

When the requirement includes formulas or derived values, include the derivation logic explicitly.

## 4. Coverage is split into UI, business rule, and lifecycle checks

The approved samples repeatedly include:

- list page coverage
- detail page coverage
- process validation
- logic validation

Common logic validation items:

- save duplicate check
- save required-field check
- confirm recalculation
- audit validation
- reverse-audit validation
- void validation
- button visibility by state

Do not stop at field attributes. Always add lifecycle checks when the requirement mentions document states or approval steps.

## 5. Critical rules are surfaced as callouts

Important business rules are called out instead of hidden inside long paragraphs. Use one of:

- Feishu callout block
- block quote
- short, isolated rule bullets

Examples of rules worth surfacing:

- allowed organization level
- repeated-creation rule
- recalculation trigger
- data-source restriction
- formula summary

## 6. Evidence is expected, but must not be fabricated

The approved result document contains sections like:

- `测试结果`
- `验证数据`
- `相应SQL`
- screenshots near the relevant section

When generating pre-execution testcases, preserve these sections as placeholders:

- `测试结果：待执行`
- `验证数据：待补充`
- `相应SQL：待补充`

Never claim an execution result without real evidence.

## 7. Ambiguity should be isolated, not silently guessed

The whiteboard samples contain highlighted notes for uncertain or changing rules. Reflect that behavior by adding a final `需求确认项` section whenever the source is incomplete or contradictory.

Recommended columns:

| 序号 | 疑问点 | 待确认内容 | 影响范围 |
| --- | --- | --- | --- |
| 1 | 组织选择范围 | 是否允许选择到片区/分公司/种猪场 | 详情页字段与权限 |

## 8. Team quality bar

Treat the draft as review-ready only if it meets all of these:

- It is traceable to the source requirement.
- It is structured enough that a tester can execute directly from the headings.
- It captures field rules, business rules, and lifecycle rules together.
- It does not use empty wording such as “校验通过” or “功能正常”.
- It does not invent test results.
