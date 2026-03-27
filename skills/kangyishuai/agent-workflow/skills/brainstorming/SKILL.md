---
name: brainstorming
description: "Use before starting any significant task — creating features, writing content, designing solutions, planning projects, or making changes. Explores user intent, requirements, and design through collaborative dialogue before taking action. Trigger when a new task is described or when the scope of work is unclear. Do not trigger when the user is asking a simple question, giving feedback mid-task, or when a design has already been approved."
---

# Brainstorming Ideas Into Designs

Help turn ideas into fully formed designs and specs through natural collaborative dialogue.

Start by understanding the current project context, then ask questions one at a time to refine the idea. Once you understand what you're building, present the design and get user approval.

<HARD-GATE>
Do NOT invoke any execution skill, take any implementation action, or start producing deliverables until you have presented a design and the user has approved it. This applies to EVERY task regardless of perceived simplicity.
</HARD-GATE>

## Anti-Pattern: "This Is Too Simple To Need A Design"

Every task goes through this process. A short document, a minor change, a config tweak — all of them. "Simple" tasks are where unexamined assumptions cause the most wasted work. The design can be short (a few sentences for truly simple tasks), but you MUST present it and get approval.

## Checklist

You MUST create a task for each of these items and complete them in order:

1. **Explore project context** — check existing files, docs, prior work
2. **Ask clarifying questions** — one at a time, understand purpose/constraints/success criteria
3. **Propose 2-3 approaches** — with trade-offs and your recommendation
4. **Present design** — in sections scaled to their complexity, get user approval after each section
5. **Write design doc** — save to `docs/specs/YYYY-MM-DD-<topic>-design.md`
6. **Spec self-review** — quick inline check for placeholders, contradictions, ambiguity, scope (see below)
7. **User reviews written spec** — ask user to review the spec file before proceeding
8. **Transition to execution** — invoke `agent-workflow:writing-plans` skill to create an execution plan

## Process Flow

```dot
digraph brainstorming {
    "Explore project context" [shape=box];
    "Ask clarifying questions" [shape=box];
    "Propose 2-3 approaches" [shape=box];
    "Present design sections" [shape=box];
    "User approves design?" [shape=diamond];
    "Write design doc" [shape=box];
    "Spec self-review\n(fix inline)" [shape=box];
    "User reviews spec?" [shape=diamond];
    "Invoke writing-plans skill" [shape=doublecircle];

    "Explore project context" -> "Ask clarifying questions";
    "Ask clarifying questions" -> "Propose 2-3 approaches";
    "Propose 2-3 approaches" -> "Present design sections";
    "Present design sections" -> "User approves design?";
    "User approves design?" -> "Present design sections" [label="no, revise"];
    "User approves design?" -> "Write design doc" [label="yes"];
    "Write design doc" -> "Spec self-review\n(fix inline)";
    "Spec self-review\n(fix inline)" -> "User reviews spec?";
    "User reviews spec?" -> "Invoke writing-plans skill" [label="approved"];
    "User reviews spec?" -> "Write design doc" [label="needs changes"];
}
```

## Clarifying Questions

Ask one question at a time. Do NOT ask multiple questions in one message.

**Good questions:**
- "What problem does this solve for the user?"
- "What does success look like for this?"
- "Are there any constraints I should know about?"
- "Who is the audience for this?"

**Bad questions:**
- "What's the goal, what are the constraints, and who uses this?" (too many at once)

## Proposing Approaches

After gathering enough context, propose 2-3 distinct approaches:

```
Approach 1: [Name]
- How it works: ...
- Trade-offs: ...

Approach 2: [Name]
- How it works: ...
- Trade-offs: ...

My recommendation: Approach N, because ...
```

Don't just list options — give a recommendation with reasoning.

## Spec Self-Review

After writing the spec, check it yourself before asking the user to review:

1. **Completeness** — Does every stated goal have a corresponding section?
2. **Placeholder scan** — Any "TBD", "TODO", "fill in later"? Fix them.
3. **Contradiction check** — Do any two sections conflict?
4. **Scope check** — Is anything in the spec out of scope for this task?

Fix issues inline. Then ask user to review.

## Transition to Execution

After user approves the spec:

```
Spec approved. Ready to create an execution plan.

Invoking agent-workflow:writing-plans to break this into actionable steps.
```

## Common Mistakes

**Skipping the design for "simple" tasks**
- Problem: Unexamined assumptions cause rework
- Fix: Always present a design, even if brief

**Asking multiple questions at once**
- Problem: Overwhelming, hard to answer
- Fix: One question per message

**Presenting a design without trade-offs**
- Problem: User can't make informed choice
- Fix: Always include trade-offs and a recommendation

**Starting execution before approval**
- Problem: Wasted work if direction changes
- Fix: Hard gate — no action before approval
