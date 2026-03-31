# PRD Template — English (Comprehensive Edition)

> **Document Type**: Product Requirements Document Template
> **Skill**: PRD-Writer (Global PM Edition)
> **Target Users**: Product Managers, Product Owners, Technical Leads, QA Engineers, and cross-functional stakeholders writing or reviewing PRDs for digital products.
> **Template Version**: 1.0
> **Last Updated**: March 2026

---

## Table of Contents

1. [Chapter 1: Project Overview](#1-project-overview)
2. [Chapter 2: User Analysis](#2-user-analysis)
3. [Chapter 3: Requirements](#3-requirements)
4. [Chapter 4: Success Metrics](#4-success-metrics)
5. [Chapter 5: Acceptance Criteria](#5-acceptance-criteria)
6. [Chapter 6: Technical Constraints](#6-technical-constraints)
7. [Chapter 7: Appendix](#7-appendix)

---

## 1. Project Overview

### Chapter Purpose

The Project Overview chapter establishes the strategic and contextual foundation for the entire document. It answers the questions: *Why are we building this? What problem are we solving? What does success look like, and where do we draw the line?* This chapter is the contract between the product team and every execution team member — engineers, designers, QA engineers, data analysts, and stakeholders — before a single line of code is written or a single pixel is designed.

A well-written Project Overview aligns everyone on *why* the project exists, *what* it aims to achieve, and *what it explicitly does not attempt to do*. Without this shared foundation, teams drift into scope creep, feature debates without resolution criteria, and misalignment between business objectives and implementation details.

**Who benefits from this chapter:**
- **Executives and stakeholders** gain a quick understanding of the project's business rationale and expected outcomes.
- **Engineering teams** understand the technical "why" behind features and can make informed architecture decisions.
- **Designers** understand the user problems they need to solve before wireframing solutions.
- **QA Engineers** use the scope boundaries to define test scope and avoid unplanned testing of out-of-scope features.
- **Data Analysts** understand which metrics matter and can plan data collection instrumentation accordingly.

**Do not skip this chapter.** Even for small features or incremental improvements, a concise Project Overview prevents the most common PRD failures: vague goals, undefined scope, and unmet stakeholder expectations.

---

### Filling Guide

#### 1.1 Background and Problem Statement

**What to write here:** Start with the *current state* — describe the problem, inefficiency, or opportunity that has triggered this project. Be specific. Name the pain point, quantify its impact where possible, and explain *who* is affected. Avoid generic statements like "our users need a better experience." Instead, describe *what is broken*, *for whom*, and *at what frequency or scale*.

**Good patterns to follow:**
- Lead with the pain point before the solution. Describe the problem first.
- Include quantitative evidence where available: error rates, time wasted, revenue lost, user drop-off percentages.
- Reference any prior user research, support ticket analysis, or business data that substantiates the problem.
- Acknowledge if the problem statement is based on hypotheses rather than confirmed data — this builds credibility.

**How much to write:** Aim for 200–400 words. If your background section exceeds 600 words, consider whether you are combining multiple problems or need to split the PRD.

---

#### 1.2 Project Goals

**What to write here:** Translate the problem statement into 3–7 concrete, time-bound goals. Each goal should be *specific* (clear enough that two reasonable people would agree on whether it has been achieved), *measurable* (quantitative target where possible), and *realistic* (within the team's capacity and the system's constraints).

**Goal-setting framework:**
- Each goal should be traceable to a Success Metrics chapter (Chapter 4). If you cannot link a goal to a metric, it is too vague.
- Distinguish between *business goals* (outcomes that matter to the organization) and *product goals* (changes in user behavior that drive those outcomes).
- Set a target timeframe. Goals without a deadline are aspirations, not targets.

**Good patterns to follow:**
- Use the format: "Achieve [X] measured by [Y] by [Z date]."
- Limit to one primary North Star goal and 2–6 supporting goals.
- State goals in positive terms — what you *will* achieve, not what you *will eliminate*.

**Common mistakes to avoid:**
- Listing more than 7 goals — this dilutes focus. Rank them and mark the top 3 as primary.
- Confusing goals with features. A goal is an outcome; a feature is a means to an end.
- Setting goals without baseline data. If you do not know the current state, note this as a gap and estimate conservatively.

---

#### 1.3 Scope Definition

**What to write here:** Define *what is included* and *what is explicitly excluded* from this release or project phase. Scope definition is not optional — it is the most effective tool against scope creep.

**In-Scope items** should include:
- Core feature modules that will be built or significantly changed
- User flows that will be fully functional end-to-end
- Platforms (web, iOS, Android, API) that will be supported in this phase
- Key integrations that are part of this release

**Out-of-Scope items** should include:
- Features discussed in brainstorming but not approved for this phase
- Platforms or devices not supported in this release
- Advanced capabilities deferred to future roadmap items
- Integrations that will come in a later phase

**Good patterns to follow:**
- Be specific, not diplomatic. "User notification center" is vague; "In-app notification center with email and push notification delivery" is clear.
- Use the same granularity for In-Scope and Out-of-Scope. If one side lists "Android app," the other should match.
- Review Out-of-Scope items with engineering and design before publishing to ensure nothing critical was accidentally excluded.

---

#### 1.4 Core Value Proposition

**What to write here:** Write a single sentence — no more than 40 words — that captures the essential value this product delivers to its users. This is not a marketing tagline; it is a precise statement of *what changes for the user* and *why that matters*.

**Good patterns to follow:**
- Name the user role, the action they take, and the outcome they achieve.
- Avoid buzzwords ("revolutionary," "AI-powered," "seamless").
- Test it with this question: Could a product manager, an engineer, and a customer service agent all agree this sentence accurately describes the product?

---

### Template Body

```markdown
# [Product / Feature Name]

## 1. Project Overview

### 1.1 Background and Problem Statement

[Describe the current state of affairs that has triggered this project. Identify:
- The specific pain point or opportunity
- Who is affected (user segment, team, or business function)
- Frequency, scale, or financial impact where available
- Any existing data, research, or evidence substantiating the problem
]

**Key Pain Points:**
- [Pain Point 1 — specific, with quantitative evidence where available]
- [Pain Point 2]
- [Pain Point 3]

### 1.2 Project Goals

| # | Goal | Measurable Target | Target Date | Related Metric |
|---|------|-------------------|-------------|----------------|
| 1 | [Primary goal — the single most important outcome] | [e.g., Reduce X by Y%] | [YYYY-QX or YYYY-MM] | [Chapter 4 metric name] |
| 2 | [Supporting goal] | [Target] | [Date] | [Metric] |
| 3 | [Supporting goal] | [Target] | [Date] | [Metric] |
| 4 | [Supporting goal, if applicable] | [Target] | [Date] | [Metric] |

### 1.3 Scope Definition

#### 1.3.1 In Scope

The following are committed deliverables for this release:

- **[Feature Module A]:** [Brief description of what will be built]
- **[Feature Module B]:** [Brief description]
- **[Feature Module C]:** [Brief description]
- **[Platform / Channel]:** [e.g., Web app (Chrome/Safari/Firefox latest 2 versions); iOS app (14+); Android app (10+)]
- **[Key Integration]:** [e.g., Integration with Salesforce CRM for lead sync]

#### 1.3.2 Out of Scope

The following are explicitly excluded from this release:

- **[Feature or capability]:** [Reason for exclusion]
- **[Feature or capability]:** [Reason]
- **[Platform]:** [Reason]
- **[Integration]:** [Reason]

### 1.4 Core Value Proposition

[Write a single sentence (40 words maximum) that captures:
- The target user role
- The action they take or the change they experience
- The outcome and its significance
Format: "[Product name] enables [user role] to [action], so that [desired outcome]."]
```

---

### Example Content

> **Example Product:** SwiftStock — Real-Time Inventory Visibility System for SMB Retailers
>
> **Context:** SwiftStock is a B2B SaaS platform serving 45,000 small and medium-sized retail sellers. The product connects sellers' inventory databases to a central dashboard, providing real-time stock level visibility, low-stock alerts, and automated reorder triggers. The example below demonstrates how a PM would fill in the Project Overview for a new release focused on "Multi-Warehouse Stock Sync."

---

```markdown
# SwiftStock — Multi-Warehouse Inventory Sync Module

## 1. Project Overview

### 1.1 Background and Problem Statement

SwiftStock's 45,000 active sellers manage inventory across an average of 3.2 warehouse locations per account, with 28% of high-volume sellers operating 5 or more warehouses. Our current architecture treats each warehouse as an independent data silo: inventory counts update locally and sync to the central platform once every 24 hours via overnight batch job.

This creates a well-documented operational crisis. A seller in Portland has 200 units of SKU-A in Warehouse 1 and 0 units in Warehouse 2. A customer in Seattle orders 150 units. The system — operating on yesterday's data — confirms the order. The warehouse team ships 150 units from Warehouse 1. Meanwhile, a second customer in San Francisco orders 80 units of SKU-A before the overnight sync runs. Both orders are confirmed. The warehouse ships from Warehouse 1 (depleting all 200 units), then discovers the shortage when attempting to fulfill the second order. Result: one order is partially or fully canceled.

Quantitatively: 38% of sellers report stockout-related order cancellations at least once per week. Our data shows 12% of all orders are affected, representing approximately $2.1M in annual lost revenue across our seller base. More critically, sellers who experience 3 or more stockout cancellations within 60 days have a 34% higher churn rate than baseline. The problem is not a minor inconvenience — it is a systemic risk to seller retention and platform trust.

**Key Pain Points:**
- **Sellers:** Orders confirmed on out-of-date inventory data result in cancellations, refunds, and damaged customer relationships. Sellers report spending 3–5 hours per week manually reconciling warehouse discrepancies.
- **Buyers (B2B customers of sellers):** Unexpected delays or partial shipments erode trust in the seller's brand, which indirectly damages SwiftStock's reputation as the platform enabling those sellers.
- **SwiftStock Support Team:** Stockout-related support tickets represent 22% of all Tier-1 tickets, consuming an estimated 340 support hours per month.
- **Data Accuracy:** The 24-hour data lag makes any real-time reporting, predictive reordering, or demand forecasting impossible for our sellers.

### 1.2 Project Goals

| # | Goal | Measurable Target | Target Date | Related Metric |
|---|------|-------------------|-------------|----------------|
| 1 | **Primary: Reduce stockout-driven order cancellations** | Decrease stockout-related cancellations by 30% (from 12% to 8.4% of total orders) | 2026-Q3 | Lagging Indicator: Stockout Cancellation Rate |
| 2 | Reduce data sync lag from 24 hours to under 5 minutes for 95% of inventory updates | P95 sync latency < 5 minutes for real-time updates; batch fallback for offline warehouses | 2026-Q3 | Leading Indicator: Inventory Sync Latency (P95) |
| 3 | Increase seller engagement with inventory management tools | Raise weekly active usage of the inventory dashboard from 41% to 65% | 2026-Q4 | Leading Indicator: Weekly Active Dashboard Users |
| 4 | Reduce SwiftStock support tickets related to stockout disputes | Decrease support tickets by 25% (from 340 to 255 hours/month) | 2026-Q4 | Lagging Indicator: Stockout-Related Support Ticket Volume |
| 5 | Enable sellers to set per-warehouse low-stock thresholds | 50% of multi-warehouse sellers configure at least one low-stock alert rule | 2026-Q3 | Leading Indicator: Low-Stock Alert Configuration Rate |

### 1.3 Scope Definition

#### 1.3.1 In Scope

The following are committed deliverables for the Multi-Warehouse Stock Sync Module, Sprint 1:

- **Real-Time Inventory Sync Engine:** WebSocket-based push architecture that propagates inventory updates from warehouse source systems to the central SwiftStock platform within 5 minutes of a change event, with guaranteed delivery and ordered processing.
- **Multi-Warehouse Inventory Dashboard:** New dashboard view that displays stock levels across all warehouses for a given SKU in a single screen, with color-coded availability status (In Stock, Low Stock, Out of Stock) per warehouse.
- **Warehouse-Level Low-Stock Alert Rules:** Sellers can define per-warehouse, per-SKU (or per-category) low-stock threshold rules. Alerts are delivered via in-app notification and optional email digest (configurable frequency: immediate, daily, weekly).
- **Unified Order Inventory Reservation:** When an order is placed, the system evaluates inventory availability across *all* warehouses for that seller's account and reserves inventory from the optimal warehouse (nearest geographic location to shipping address by default, configurable).
- **Cross-Warehouse Transfer Workflow:** Sellers can initiate stock transfers between warehouses directly within SwiftStock, with a two-step confirmation (request → approve) workflow.
- **Salesforce Integration (Phase 1):** One-way sync of inventory availability data to Salesforce CRM, enabling seller sales teams to quote accurate lead times to prospects. Read-only from Salesforce side.
- **Web App (Chrome/Firefox/Safari, latest 2 versions); iOS app (14+); Android app (10+)**

#### 1.3.2 Out of Scope

The following are explicitly excluded from this release:

- **Automated Reorder Suggestions:** AI-driven purchase order generation based on sales velocity and lead times. This requires a separate demand forecasting module, planned for 2027.
- **POS (Point of Sale) Integration:** Direct sync with sellers' physical POS terminals. Requires hardware partnership agreements not yet in place.
- **Multi-Bin Location Tracking:** Tracking inventory at the shelf/bin level within a single warehouse. Our current data model supports warehouse-level only.
- **EDI (Electronic Data Interchange) for Enterprise Sellers:** Large enterprise accounts requiring EDI-based inventory updates. This requires a dedicated enterprise integration layer, scoped for Q4 2026.
- **Windows/macOS Desktop Application:** Only web and mobile (iOS/Android) are in scope for this release.
- **Buyer-Facing Stock Availability API:** External third-party developers cannot yet query inventory levels via API. This is gated behind a future API Gateway project (Q4 2026).

### 1.4 Core Value Proposition

SwiftStock's Multi-Warehouse Sync module enables sellers managing inventory across two or more warehouse locations to see a single, accurate view of their stock levels in real time — eliminating the 24-hour data lag that causes 38% of sellers to experience weekly stockout cancellations, and giving them per-warehouse alert rules to prevent shortages before they result in lost orders.
```

---

## 2. User Analysis

### Chapter Purpose

The User Analysis chapter defines *who* the product is being built for, *what* they need, and *what their journey* looks like from problem awareness to resolution. This chapter is the critical bridge between the strategic context established in Chapter 1 and the concrete requirements defined in Chapter 3. Without a clear understanding of users — their roles, goals, pain points, and the contexts in which they use the product — requirements are built on assumptions, and assumptions are the primary driver of product failures.

This chapter serves multiple audiences within the team:
- **Product Managers** use this chapter to ensure every feature decision is traceable back to a real user need.
- **Designers** build empathy maps, journey maps, and personas from this chapter to inform information architecture, interaction design, and visual hierarchy.
- **Engineers** understand the context in which users operate to make appropriate technical design decisions.
- **QA Engineers** use user stories and journey maps to identify edge-case scenarios and ensure test coverage reflects real-world usage patterns.

---

### Filling Guide

#### 2.1 Target User Personas

**What to write here:** Define the distinct user *roles* that will interact with the product. Create separate persona definitions for each distinct role, even if they share the same user account in the product.

**For each persona, include:**
- **Role title:** The name of the role as it appears in the product and in organizational context.
- **Demographics and background:** Relevant professional context — what team they are on, how large their operation is, what tools they currently use, how tech-savvy they are.
- **Primary goals:** The top 2–3 things this persona is trying to accomplish in their workday that this product enables or improves.
- **Pain points:** The specific frustrations, workarounds, or failure modes they experience today that this product addresses.
- **Technology context:** What devices, browsers, or environments they use the product in.
- **Usage frequency and session patterns:** How often do they use the product? For how long? At what times of day?

**How many personas to include:**
- Include **every distinct role** that appears in the product's workflows. Mark one as **Primary** and others as **Secondary** (or Secondary/Internal for internal stakeholders).

**Common mistakes to avoid:**
- Describing one generic "user" for a product with multiple distinct roles.
- Listing pain points that are actually product feature requests in disguise.
- Assuming all users have the same technology setup.

---

#### 2.2 User Stories

**What to write here:** Translate each persona's goals into structured user stories using the canonical format:

> **As a [role], I want [goal/action] so that [benefit/outcome].**

User stories are not feature descriptions — they express *user intent* and *value*. The "so that" clause is the most important part because it connects the feature to the underlying human need.

**How to write effective user stories:**
- Write from the user's perspective, not the system's.
- Keep stories small and focused. One story per user goal, not one story per feature.
- Each story should be independently testable.
- Assign a MoSCoW priority to each story (P0/Must, P1/Should, P2/Could).

**Common mistakes to avoid:**
- Writing user stories that describe system behavior instead of user intent.
- Writing stories that are too large (epics masquerading as stories).
- Omitting the "so that" clause.

---

#### 2.3 User Journey Map (Optional but Recommended)

**What to write here:** Map the end-to-end journey of the primary persona as they move through the product to accomplish a specific goal. A User Journey Map documents the *stages*, *actions*, *touchpoints*, *emotions*, and *pain points* a user experiences from the moment they become aware of a need to the moment it is resolved.

**When to include it:**
- Include it for **primary persona flows that span multiple touchpoints**.
- Include it when the product involves **multiple systems or channels**.
- Include it when there is a known **high drop-off point** in the current flow.

**Journey map format:**
- List 4–8 stages (a common template: Awareness → Discovery → Evaluation → Action → Resolution → Follow-up).
- For each stage: describe the user's action, the touchpoint or channel, their emotional state, and the pain point if any.
- Identify *moments of truth* — stages where the experience has the highest impact on overall satisfaction.

---

### Template Body

```markdown
## 2. User Analysis

### 2.1 Target User Personas

#### 2.1.1 [Persona Name — Role Title]

| Attribute | Description |
|-----------|-------------|
| **Role** | [Official role title as it appears in the product and organization] |
| **Background** | [Professional context: team size, operation scale, industry experience, current tool stack] |
| **Primary Goals** | 1. [Goal 1 — what this person is trying to accomplish]<br>2. [Goal 2]<br>3. [Goal 3] |
| **Pain Points** | 1. [Pain Point 1 — current frustration or workaround]<br>2. [Pain Point 2]<br>3. [Pain Point 3] |
| **Technology Context** | [Devices, browsers, connectivity, physical environment — e.g., "Mobile-first; uses Android phone on warehouse floor with intermittent cellular signal"] |
| **Usage Frequency** | [e.g., Multiple times daily; checks dashboard every morning; processes orders as they come in] |
| **Persona Type** | **Primary** / Secondary |

#### 2.1.2 [Persona Name — Role Title] (Secondary)

[Same structure as above]

#### 2.1.3 [Additional Personas as Needed]

[Repeat structure as needed]

---

### 2.2 User Stories

#### 2.2.1 [Persona Name] User Stories

| ID | User Story | Priority | Related Requirement |
|----|-----------|----------|---------------------|
| US-[###] | **As a [role],** I want to **[perform an action or achieve a goal]** so that **[desired outcome or business value]**. | P0 / P1 / P2 | [REQ-### from Chapter 3, if applicable] |
| US-[###] | **As a [role],** I want to **[perform an action]** so that **[desired outcome]**. | P0 / P1 / P2 | [REQ-###] |
| US-[###] | **As a [role],** I want to **[perform an action]** so that **[desired outcome]**. | P0 / P1 / P2 | [REQ-###] |

#### 2.2.2 [Persona Name] User Stories

[Repeat structure for each distinct persona]

---

### 2.3 User Journey Map (Optional)

#### 2.3.1 Journey: [Name of the Journey Being Mapped]

> **Journey Goal:** [What the user is trying to accomplish through this journey]

| Stage | User Action | Touchpoint / Channel | Emotional State | Pain Points / Friction | Opportunity |
|-------|-------------|----------------------|-----------------|----------------------|-------------|
| 1. [Awareness] | [What triggers the user to start this journey] | [Channel] | [Emotional state] | [Friction] | [Product opportunity] |
| 2. [Discovery] | [User determines they need to address the issue] | [Touchpoint] | [State] | [Friction] | [Opportunity] |
| 3. [Evaluation] | [User evaluates options] | [Touchpoint] | [State] | [Friction] | [Opportunity] |
| 4. [Action] | [User takes the primary action] | [Touchpoint] | [State] | [Friction] | [Opportunity] |
| 5. [Resolution] | [User confirms the issue is resolved] | [Touchpoint] | [State] | [Friction] | [Opportunity] |
| 6. [Follow-up] | [User verifies or monitors ongoing status] | [Touchpoint] | [State] | [Friction] | [Opportunity] |

**Moments of Truth:**
- [Identify the 1–2 stages where the experience has the highest impact on user satisfaction or frustration]
```

---

### Example Content

> **Example Product:** SwiftStock — Multi-Warehouse Inventory Sync Module (continued)
>
> **Primary Persona:** Marcus Chen, Operations Manager at West Coast Goods (a mid-size retailer with 4 warehouses across California and Oregon, $8M annual revenue on SwiftStock).
>
> **Secondary Persona:** Priya Nair, Account Manager at West Coast Goods (uses SwiftStock to communicate accurate lead times to B2B customers).
>
> **Tertiary Persona:** David Okafor, SwiftStock Customer Success Manager (internal stakeholder who monitors platform health for high-value accounts).

---

```markdown
## 2. User Analysis

### 2.1 Target User Personas

#### 2.1.1 Marcus Chen — Operations Manager (Primary)

| Attribute | Description |
|-----------|-------------|
| **Role** | Operations Manager, West Coast Goods — a mid-size retail distributor with 4 warehouse locations across California and Oregon. Marcus has been in warehouse operations for 12 years, the last 3 managing West Coast Goods' multi-warehouse operation. |
| **Background** | Marcus oversees daily inventory operations across all 4 warehouses, manages a team of 18 warehouse staff, and is the primary SwiftStock user for his organization. West Coast Goods processes an average of 340 orders per day across their warehouses. They have been using SwiftStock for 18 months, initially on the Basic plan (single-warehouse view) and upgraded to Business tier 6 months ago for multi-warehouse visibility. His team uses SwiftStock, NetSuite (ERP), and Google Sheets. |
| **Primary Goals** | 1. **Prevent stockouts before they cause order cancellations** — Marcus's single most important daily responsibility.<br>2. **Reduce manual reconciliation time** — Currently spends 2–3 hours every morning manually comparing NetSuite exports with SwiftStock data.<br>3. **Manage cross-warehouse transfers efficiently** — Needs to initiate and track transfers without relying on phone calls or email threads. |
| **Pain Points** | 1. **Data lag of up to 24 hours** makes Marcus question every stock confirmation. He has lost count of the number of times an order was confirmed by SwiftStock only to discover a warehouse had already depleted that SKU.<br>2. **No visibility into cross-warehouse inventory at order time.** When a customer orders 150 units, Marcus has no quick way to know if another warehouse has surplus stock. He currently calls Warehouse 3 directly — a process that takes 15–30 minutes per order.<br>3. **Low-stock alerts arrive after the stockout has already occurred.** Alerts fire when inventory hits zero, not when it reaches a level that triggers concern.<br>4. **No context for *why* stock moved.** SwiftStock shows current levels but not the reason for a sudden drop. |
| **Technology Context** | Desktop-first (Dell laptop, Windows 11, Chrome 110+). Primary work environment is the office with a 27-inch monitor. Uses iOS SwiftStock app (version 5.2) on iPhone 14 when on the warehouse floor. Stable broadband at office; cellular when mobile. Uses NetSuite for purchase orders, SwiftStock for inventory visibility, Slack for team communication. |
| **Usage Frequency** | Daily active user. Checks the SwiftStock dashboard every morning at 7:30 AM. Accesses the mobile app 4–6 times per day for real-time checks. Attended 2 of 3 available SwiftStock webinar sessions last quarter, indicating proactive engagement. |
| **Persona Type** | **Primary** |

#### 2.1.2 Priya Nair — Account Manager (Secondary)

| Attribute | Description |
|-----------|-------------|
| **Role** | Account Manager, West Coast Goods — manages relationships with 35 B2B customers who purchase wholesale quantities on net-30 terms. Primary point of contact for customer inquiries about order status, lead times, and product availability. |
| **Background** | Priya has been with West Coast Goods for 4 years. Her performance is measured on customer retention (target: 92% annually) and upsell conversion rate (target: 28% quarterly). She relies on Salesforce CRM for account management and SwiftStock for real-time inventory checks. Her biggest fear is quoting a lead time that turns out to be wrong — this has happened 3 times in the past 6 months, costing her 2 accounts that cited "unreliable availability information" as a reason for not renewing. |
| **Primary Goals** | 1. **Quote accurate lead times to B2B customers** based on real-time inventory data, not yesterday's spreadsheet.<br>2. **Proactively notify customers of supply constraints** before they place orders, to preserve trust and enable substitution conversations.<br>3. **Access a shared inventory view within Salesforce** without switching between apps mid-call. |
| **Pain Points** | 1. **Priya cannot see real-time inventory during a customer call.** She has to put customers on hold, log into SwiftStock (30–45 seconds), check the SKU, and call the warehouse manually — all while the customer waits.<br>2. **No visibility into pending replenishments.** When a SKU shows "In Stock," Priya has no way to know if a large outbound shipment is scheduled that will deplete stock before the customer's order arrives.<br>3. **Salesforce and SwiftStock are not integrated.** She manually logs SwiftStock availability notes into Salesforce — adding 5–8 minutes per interaction and frequently skipped under time pressure. |
| **Technology Context** | MacBook Pro (macOS Sonoma 14), works primarily in Salesforce (Chrome) and Slack. iPhone 13 for mobile. Tech-savvy for business applications but not for operations or data systems. |
| **Usage Frequency** | Moderate. Accesses SwiftStock 3–5 times per day, always in the context of a customer call or pre-order check. Would use it more if the workflow were faster and integrated with Salesforce. |
| **Persona Type** | **Secondary** |

#### 2.1.3 David Okafor — SwiftStock Customer Success Manager (Internal / Platform Stakeholder)

| Attribute | Description |
|-----------|-------------|
| **Role** | Customer Success Manager at SwiftStock (internal). Manages a portfolio of 85 high-value accounts (annual contract value > $15K), including West Coast Goods. Responsible for onboarding, adoption monitoring, quarterly business reviews, and churn prevention. |
| **Background** | David has been with SwiftStock for 2 years. Before that, he worked as an operations analyst at a 3PL company. His team uses Gainsight for customer health tracking and Zendesk for support ticket management. He has direct visibility into the 22% of support tickets that are stockout-related — and knows that for accounts like West Coast Goods, each stockout cancellation is a potential churn signal. |
| **Primary Goals** | 1. **Reduce churn risk** for accounts experiencing repeated stockout-related cancellations.<br>2. **Identify adoption gaps early** — accounts not using core features 90 days post-onboarding are at 2.3x higher churn risk.<br>3. **Surface product feedback** from enterprise accounts to inform SwiftStock's roadmap. |
| **Pain Points** | 1. **David has no visibility into real-time stockout events** — he learns about them only through support tickets or quarterly reviews.<br>2. **He cannot proactively demonstrate product value** to accounts during QBRs because SwiftStock does not generate adoption reports tied to business outcomes.<br>3. **Onboarding new multi-warehouse accounts requires extensive manual setup guidance.** |
| **Technology Context** | MacBook Pro, works primarily in Gainsight, Zendesk, and Slack. Has read-only access to aggregated platform analytics through SwiftStock's internal analytics dashboard. |
| **Usage Frequency** | Weekly. Reviews account health dashboards every Monday. Uses Zendesk for daily ticket triage. |
| **Persona Type** | **Secondary (Internal)** |

---

### 2.2 User Stories

#### 2.2.1 Marcus Chen — Operations Manager User Stories

| ID | User Story | Priority | Related Requirement |
|----|-----------|----------|---------------------|
| US-001 | **As an Operations Manager,** I want to see the real-time stock level of any SKU across all my warehouses in a single view, so that I can immediately identify which warehouses have available inventory when an order comes in. | **P0** | REQ-INV-001 |
| US-002 | **As an Operations Manager,** I want to set per-warehouse, per-SKU low-stock alert thresholds, so that I am notified when a SKU falls below my defined reorder point — not after it hits zero and disrupts active orders. | **P0** | REQ-INV-002 |
| US-003 | **As an Operations Manager,** I want to initiate a cross-warehouse stock transfer request from within SwiftStock, so that I can move inventory between warehouses without using phone calls, email, or switching to NetSuite. | **P1** | REQ-INV-003 |
| US-004 | **As an Operations Manager,** I want to see the reason for a recent stock level change (e.g., outbound shipment, return, transfer), so that I can distinguish between actual consumption and data sync errors without manually cross-referencing NetSuite. | **P1** | REQ-INV-004 |
| US-005 | **As an Operations Manager,** I want to receive push notifications on my iPhone when any SKU in my top 20 selling items falls below its alert threshold, so that I can respond to potential stockouts even when I am not at my desk. | **P2** | REQ-INV-005 |
| US-006 | **As an Operations Manager,** I want to view a historical trend of stock levels for any SKU over the past 30 days, so that I can identify slow-moving inventory and adjust reorder quantities proactively. | **P2** | REQ-INV-006 |

#### 2.2.2 Priya Nair — Account Manager User Stories

| ID | User Story | Priority | Related Requirement |
|----|-----------|----------|---------------------|
| US-007 | **As an Account Manager,** I want to check real-time inventory availability for any SKU in under 10 seconds from my laptop, so that I can quote accurate lead times to customers without placing them on hold. | **P0** | REQ-SAL-001 |
| US-008 | **As an Account Manager,** I want to see whether a currently-in-stock SKU has any pending outbound shipments scheduled in the next 48 hours, so that I do not quote availability that will be compromised before the customer's order can be fulfilled. | **P1** | REQ-SAL-001 |
| US-009 | **As an Account Manager,** I want to log availability information directly into Salesforce from the SwiftStock context, so that I do not have to manually type notes and risk skipping this step under time pressure. | **P2** | REQ-SAL-002 |

#### 2.2.3 David Okafor — Customer Success Manager User Stories

| ID | User Story | Priority | Related Requirement |
|----|-----------|----------|---------------------|
| US-010 | **As a Customer Success Manager,** I want to receive an alert when any of my high-value accounts experiences a stockout cancellation, so that I can proactively reach out to the account before they submit a churn-risk signal. | **P0** | REQ-CS-001 |
| US-011 | **As a Customer Success Manager,** I want to view an adoption dashboard that shows which accounts have configured low-stock alerts, so that I can identify accounts at risk of churn due to non-adoption during QBRs. | **P1** | REQ-CS-002 |

---

### 2.3 User Journey Map

#### 2.3.1 Journey: Marcus Chen — Preventing a Stockout Before It Cancels an Order

> **Journey Goal:** Marcus receives an alert that SKU-X is approaching low-stock threshold in Warehouse 2 (Portland), evaluates options across warehouses, initiates a cross-warehouse transfer from Warehouse 1 (Los Angeles), and confirms the transfer before the stockout causes an order cancellation.

| Stage | User Action | Touchpoint / Channel | Emotional State | Pain Points / Friction | Opportunity |
|-------|-------------|----------------------|-----------------|----------------------|-------------|
| 1. **Alert Reception** | Marcus receives an in-app notification on his iPhone: "SKU-4421 is at 45 units in Warehouse 2 — below your threshold of 50 units." | iOS Push Notification / In-app notification | **Alert but not yet stressed** | Current system sends alerts after stock hits zero, not at threshold. Marcus has not yet learned to trust early alerts. | **Onboarding moment:** Consider a "Test Alert" feature during setup to build trust in the threshold system. |
| 2. **Verification** | Marcus opens SwiftStock on his iPhone to verify the current stock level. | SwiftStock iOS App | **Cautiously optimistic** | The mobile app takes 8–12 seconds to load on cellular. In a warehouse with poor connectivity, this is a friction point. | Optimize mobile dashboard load time to under 3 seconds. Show pending outbound on the SKU card without requiring a drill-through. |
| 3. **Evaluation** | Marcus checks Warehouse 1 (Los Angeles) and Warehouse 3 (Sacramento) for available stock. Warehouse 1 has 320 units; Warehouse 3 is 380 miles closer to Portland. | SwiftStock Multi-Warehouse Dashboard | **Confident and in control** | Currently requires opening each warehouse's view separately. No side-by-side comparison. | Build a unified cross-warehouse availability view showing all warehouses on one screen with geographic distance indicators. |
| 4. **Decision** | Marcus decides to initiate a transfer of 100 units from Warehouse 3 (Sacramento) to Warehouse 2 (Portland). | SwiftStock Web App (initiates); Email to carrier (executes) | **Satisfied** | Transfer initiation requires the web app. Marcus cannot initiate from the iPhone where he is standing. | Enable mobile transfer initiation in iOS app. |
| 5. **Confirmation & Monitoring** | Marcus receives email confirmations. He sets a calendar reminder to follow up in 24 hours. | Email; SwiftStock Dashboard | **Relieved** | No automated "transfer received" notification. He must manually check SwiftStock to confirm delivery. | Add push notification for "Transfer Received — Confirm Quantity." |
| 6. **Resolution** | Warehouse 2 receives and confirms the transfer. Stock rises to 145 units. The pending order for 80 units is fulfilled. | SwiftStock iOS App (confirmation) | **Triumphant** | None at this stage. | Capture this as a customer success story for advocacy. |

**Moments of Truth:**
1. **Stage 2–3 (Verification and Evaluation):** The speed and completeness of the cross-warehouse data view determines whether Marcus trusts the system enough to act on alerts. If data is incomplete or slow, he falls back to manual phone calls.
2. **Stage 4 (Decision and Action):** The ability to initiate a transfer from mobile is the key differentiator between a 5-minute resolution and a 45-minute multi-step process.
```

---

## 3. Requirements

### Chapter Purpose

The Requirements chapter is the heart of the PRD — the definitive specification of *what* will be built. It translates the user needs from Chapter 2 into concrete, actionable, and testable functional requirements, organized by priority using the MoSCoW framework (P0/Must Have, P1/Should Have, P2/Could Have). Every requirement in this chapter must be traceable to at least one user story from Chapter 2 and at least one acceptance criterion in Chapter 5.

This chapter also defines **Non-Functional Requirements (NFRs)** — the quality attributes that the system must exhibit: performance, scalability, security, availability, and usability.

**The relationship between this chapter and the rest of the PRD:**
- **From Chapter 2:** Each P0 and P1 functional requirement must map to at least one user story.
- **To Chapter 5:** Each functional requirement must have at least one corresponding acceptance criterion.
- **To Chapter 4:** NFRs directly constrain the success metrics.

---

### Filling Guide

#### 3.1 Functional Requirements

**What to write here:** List every feature to be built, organized by priority (P0, P1, P2) and then by feature module. Each requirement needs a unique identifier, a clear description, and traceability metadata.

**Requirement description template:**
- **What it does:** One sentence describing the functional behavior.
- **Who benefits:** Which persona(s) benefit from this feature.
- **Preconditions:** What must be true before this feature can be used.
- **Main flow:** The primary user journey (3–8 steps).
- **Exception flows:** How the system handles error states, edge cases.
- **Business rules:** Any business logic constraints.
- **Edge cases:** Boundary conditions.

**Common mistakes to avoid:**
- Writing requirements that describe UI behavior instead of user outcomes.
- Writing requirements that are too vague to test.
- Including implementation details. The PRD describes *what* and *why*; engineering determines *how*.
- Failing to specify error handling.

---

#### 3.2 Non-Functional Requirements (NFRs)

**What to write here:** Define the quality attributes the system must satisfy.

**Key NFR categories:**

| NFR Category | What It Measures | Example |
|---|---|---|
| **Performance** | Speed, throughput, latency | API response time P99 < 500ms |
| **Scalability** | Ability to handle growth | Support 1000 concurrent warehouse connections |
| **Availability** | Uptime and resilience | 99.5% uptime |
| **Security** | Authentication, authorization, data protection | All API calls over TLS 1.2+ |
| **Reliability** | Error rates, data integrity | Stock sync error rate < 0.1% per day |
| **Compatibility** | Browser, device, OS support | Chrome 90+, iOS 14+, Android 10+ |
| **Accessibility** | WCAG compliance | WCAG 2.1 AA compliance |

---

#### 3.3 Data Tracking Requirements

**What to write here:** Define the events and parameters the product team needs to collect to measure feature adoption and the success metrics defined in Chapter 4.

**For each tracking event:**
- **Event name:** Descriptive, consistent naming convention
- **Trigger:** When does this event fire?
- **Parameters:** What data is associated with this event? Include the data type.
- **User identity:** Is this event associated with a logged-in user, or anonymous?

---

### Template Body

```markdown
## 3. Requirements

### 3.1 Functional Requirements

#### 3.1.1 Requirement Overview

| ID | Feature Module | Requirement Title | Description | Priority | User Story | Notes |
|----|---------------|-------------------|-------------|----------|------------|-------|
| REQ-[###] | [Module name] | [Short descriptive title] | [One-line summary] | P0 / P1 / P2 | [US-###] | [Optional notes] |

#### MoSCoW Priority Annotation Reference

When filling in the **Priority** and **Notes** columns, use the following standard annotations to ensure consistency across all requirements:

| Priority | Meaning | Annotation Format | Release Guidance |
|----------|---------|-----------------|-----------------|
| **P0 — Must Have** | Core functionality without which the product cannot ship. Failure here blocks launch. | `Must, MVP baseline` | Must ship in Sprint 1. Zero P0 defects allowed at release. |
| **P1 — Should Have** | Important functionality that significantly impacts user experience or business outcomes. Deferring hurts but does not block. | `Should, important but not blocking` | Should ship in Sprint 1. If compressed, defer to Sprint 2 with PM approval. |
| **P2 — Could Have** | Desirable enhancements that improve the product but are not essential. Ship if time and resources permit. | `Could, optional enhancement` | Ship if capacity allows. No delivery commitment. |
| **P3 — Won't Have (This Release)** | Explicitly excluded from this release. May be revisited in future roadmap phases. | `Won't have, future roadmap` | Not in scope. Revisit in next planning cycle. |

**Example — Feature List with Full Priority Annotations:**

| Feature Module | Feature Name | Description | Priority | Notes |
|----------------|-------------|-------------|----------|-------|
| Feedback Submission | Feedback Form | Users can submit text feedback up to 2000 characters and select a problem type from a predefined list | P0 | Must, MVP baseline |
| Feedback Submission | Feedback History | Users can view a list of their previously submitted feedback with status and timestamps | P0 | Must, MVP baseline |
| Admin Management | Feedback List | Customer service team can view, filter, and search all submitted feedback | P1 | Should, important but not blocking |
| Admin Management | Feedback Status Update | Customer service can update feedback status (Open → In Review → Resolved) | P1 | Should, important but not blocking |
| Data Analysis | Analytics Dashboard | Display feedback volume and issue type distribution as charts and tables | P2 | Could, optional enhancement |
| Data Analysis | Export to CSV | Allow admins to export filtered feedback data as a CSV file | P2 | Could, optional enhancement |
| Notifications | Email Notification to Submitter | Send email confirmation to the user after feedback is submitted | P0 | Must, MVP baseline |
| Notifications | Status Change Notification | Notify the user via email when their feedback status is updated | P1 | Should, important but not blocking |
| Attachments | Screenshot Upload | Allow users to upload up to 3 image attachments (JPG/PNG/GIF, max 5MB each) | P1 | Should, important but not blocking |
| Security | Rate Limiting | Limit feedback submissions to 10 per user per hour to prevent abuse | P0 | Must, MVP baseline |
| Security | Input Sanitization | Sanitize all user-submitted text to prevent XSS and injection attacks | P0 | Must, MVP baseline |
| Reporting | Weekly Summary Report | Generate a weekly email digest of feedback volume and top issues for the admin team | P2 | Could, optional enhancement |

#### 3.1.2 P0 — Must Have

##### REQ-[INV-001]: [Requirement Title]

**Feature Module:** [Module Name]
**Priority:** P0
**User Story:** [US-###]
**Owner:** [PM Name] / [Tech Lead Name]
**Status:** [Approved / In Review / Draft]

**What it does:**
[One to three sentences describing the functional behavior this requirement delivers to users.]

**Preconditions:**
- [Condition 1 that must be true before this feature is accessible]
- [Condition 2]
- [Condition 3]

**Main Flow:**
1. [Step 1: User initiates action]
2. [Step 2: System processes request]
3. [Step 3: System delivers result]
4. [Step 4: User confirms or next action is available]

**Exception Flows:**
- **[Exception 1]:** [Description of exception condition] → [How the system handles it]
- **[Exception 2]:** [Description] → [How the system handles it]

**Business Rules:**
- [Rule 1]
- [Rule 2]
- [Rule 3]

**Edge Cases:**
- [Edge case 1 and expected behavior]
- [Edge case 2 and expected behavior]

---

##### [Repeat for each P0 requirement]

#### 3.1.3 P1 — Should Have

[Repeat same structure as P0 section above]

#### 3.1.4 P2 — Could Have

[Repeat same structure as P0 section above]

#### 3.1.5 Won't Have (Explicitly Excluded)

| Item | Reason for Exclusion | Future Roadmap Phase |
|------|---------------------|---------------------|
| [Feature or capability] | [Specific reason] | [Quarter / Release] |
| [Feature] | [Reason] | [Phase] |

---

### 3.2 Non-Functional Requirements

#### 3.2.1 Performance Requirements

| Metric | Requirement | Measurement Method | Notes |
|--------|-------------|-------------------|-------|
| [e.g., API Response Time] | [e.g., P99 < 500ms for all read APIs] | [How and where it is measured] | [Caveats] |
| [e.g., Sync Latency] | [e.g., P95 < 5 minutes for 95% of inventory updates] | [Measurement method] | [Caveats] |
| [e.g., Page Load Time] | [e.g., P95 < 2 seconds for dashboard initial load] | [Measurement method] | [Caveats] |
| [e.g., Concurrent Users] | [e.g., Support 1000 concurrent active sessions] | [Load test methodology] | [Scale trigger] |

#### 3.2.2 Availability Requirements

| Metric | Requirement | Measurement Method | Notes |
|--------|-------------|-------------------|-------|
| [e.g., System Uptime] | [e.g., 99.5% uptime excluding scheduled maintenance] | [Measurement method] | [Maintenance window SLA] |
| [e.g., Recovery Time Objective (RTO)] | [e.g., < 15 minutes for non-catastrophic failures] | [DR test results] | [Definition of "recovered"] |
| [e.g., Recovery Point Objective (RPO)] | [e.g., < 5 minutes of data loss for critical paths] | [Backup and replication lag measurement] | [For inventory sync engine] |

#### 3.2.3 Security Requirements

| Requirement | Specification | Implementation Notes |
|-------------|--------------|---------------------|
| [e.g., Encryption in Transit] | All API calls over TLS 1.2+ | Enforced at CDN and API gateway |
| [e.g., Encryption at Rest] | All PII and financial data encrypted at rest (AES-256) | Database-level encryption enabled |
| [e.g., Authentication] | OAuth 2.0 with PKCE for all user-facing APIs | Existing auth infrastructure |
| [e.g., Role-Based Access Control] | Role permissions enforced at API layer | RBAC matrix defined in Appendix 7.5 |

#### 3.2.4 Scalability Requirements

| Metric | Requirement | Measurement Method |
|--------|-------------|-------------------|
| [e.g., Max Warehouses per Account] | Support up to 50 warehouses per seller account | Database schema limits; load test |
| [e.g., Max SKUs per Warehouse] | Support up to 100,000 active SKUs per warehouse | Load test with synthetic data |

#### 3.2.5 Accessibility Requirements

| Requirement | Specification | Notes |
|-------------|--------------|-------|
| [e.g., WCAG 2.1 AA] | All user-facing interfaces comply with WCAG 2.1 AA | Excluding third-party embedded content |
| [e.g., Keyboard Navigation] | All interactive elements reachable via keyboard alone | Tested with axe-core in CI pipeline |

---

### 3.3 Data Tracking Requirements

| Event Name | Trigger | Parameters | User Identity |
|------------|---------|-----------|---------------|
| `[event_name]` | [When does this event fire] | `warehouse_id` (string), `sku_id` (string), `quantity` (integer) | Logged-in user |
| `[event_name]` | [Trigger] | [Parameters with types] | [Anonymous / Logged-in] |

---

### 3.4 User Interface Requirements

#### 3.4.1 Key Pages and Layouts

| Page / Screen | Description | Key Components | Responsive Behavior |
|---------------|-------------|----------------|--------------------|
| [Page name] | [What this page does — one sentence] | [List of key UI components] | [Responsive behavior] |
| [Page name] | [Description] | [Components] | [Responsive behavior] |

#### 3.4.2 Interaction Specifications

| Interaction | Component | Behavior |
|-------------|-----------|----------|
| [Interaction] | [Component] | [Behavior description] |
```

---

### Example Content

> **Example Product:** SwiftStock — Multi-Warehouse Inventory Sync Module (continued)

---

```markdown
## 3. Requirements

### 3.1 Functional Requirements

#### 3.1.1 Requirement Overview

| ID | Feature Module | Requirement Title | Description | Priority | User Story | Notes |
|----|---------------|-------------------|-------------|----------|------------|-------|
| REQ-INV-001 | Inventory Sync | Real-Time Cross-Warehouse Stock Visibility | Users can view real-time stock levels for any SKU across all warehouses in a single, unified dashboard screen | P0 | US-001 | Web and iOS; Android by Q4 |
| REQ-INV-002 | Alerts | Per-Warehouse Low-Stock Alert Rules | Users can define per-warehouse, per-SKU low-stock threshold rules; alerts fire when stock crosses the threshold | P0 | US-002 | Email and in-app push; SMS in P2 |
| REQ-INV-003 | Transfers | Cross-Warehouse Transfer Workflow | Users can initiate, approve, and confirm stock transfers between warehouses within SwiftStock | P1 | US-003 | Two-step confirmation required |
| REQ-INV-004 | Inventory Events | Stock Level Change Audit Trail | Users can view a timestamped history of all stock movements for any SKU | P1 | US-004 | Read-only; 90-day rolling history |
| REQ-INV-005 | Notifications | Mobile Push Notifications for Priority SKU Alerts | Users receive push notifications when priority SKUs cross their alert thresholds | P2 | US-005 | Requires push notification permission |
| REQ-INV-006 | Analytics | Stock Level Historical Trends | Users can view a 30-day historical trend chart for any SKU at the warehouse level | P2 | US-006 | Line chart with daily data points |
| REQ-SAL-001 | Sales Integration | Real-Time Availability Check (Salesforce Context) | Account managers can check real-time SKU availability from within Salesforce | P0 | US-007, US-008 | Salesforce AppExchange app; Phase 1 |
| REQ-SAL-002 | Salesforce | Availability Logging to Salesforce | Availability check results are automatically logged to Salesforce | P2 | US-009 | Uses Salesforce REST API |
| REQ-CS-001 | Customer Success | Account-Level Stockout Alert (Internal) | CS team receives notification when high-value accounts experience stockout cancellations | P0 | US-010 | Internal tool; Gainsight + Slack integration |
| REQ-CS-002 | Customer Success | Adoption Dashboard for CS Team | CS team can view a dashboard showing alert configuration status by account tier | P1 | US-011 | Internal dashboard (Gainsight custom) |

---

#### 3.1.2 P0 — Must Have

##### REQ-INV-001: Real-Time Cross-Warehouse Stock Visibility

**Feature Module:** Inventory Sync
**Priority:** P0
**User Story:** US-001 — "As an Operations Manager, I want to see the real-time stock level of any SKU across all warehouses in a single view, so that I can immediately identify which warehouses have available inventory when an order comes in."
**Owner:** Elena Rodriguez (PM), Wei Zhang (Tech Lead)
**Status:** Approved

**What it does:**
The Multi-Warehouse Inventory Dashboard displays real-time stock levels for a selected SKU (or a filtered SKU list) across all warehouses connected to the seller's account. Stock levels are refreshed via WebSocket push within 5 minutes of any change event, and users can see at a glance which warehouses have stock, which are low, and which are out of stock.

**Preconditions:**
- The user is authenticated and authorized (has at least Viewer role for the requested warehouses).
- The seller's warehouse connections are in an "Active" state (not "Disconnected" or "Error").
- At least one inventory sync cycle has completed for each warehouse in the view.

**Main Flow:**
1. User navigates to the Inventory section in SwiftStock web or mobile app.
2. User opens the Multi-Warehouse view (toggle or tab — "Single Warehouse" vs "All Warehouses").
3. System displays a table/list of SKUs. For each SKU row, system shows stock levels per warehouse in separate columns.
4. Each stock level cell is color-coded: **Green** (above threshold), **Amber** (below threshold but > 0), **Red** (zero — out of stock), **Gray** (no data / sync error).
5. User can sort by any warehouse column. Default sort: alphabetical by SKU name.
6. User can filter the SKU list by: warehouse, stock status, category, last updated time.
7. User clicks on a SKU row to open the SKU Detail Drawer, showing full stock history and event log.
8. WebSocket connection maintains real-time updates. When a stock level changes, the affected cell updates in real time without a page refresh. A subtle "flash" animation (yellow border, 300ms) indicates the cell has been updated.

**Exception Flows:**
- **Warehouse sync in error state:** If a warehouse's connection is in "Error" state, its column shows "Sync Error" in red with tooltip showing error code and last successful sync timestamp. Stock levels shown for that warehouse are stale (last known value) and labeled "(as of [timestamp])".
- **No warehouses connected:** Empty state with CTA: "Connect your first warehouse" + link to the onboarding wizard.
- **SKU not present in a warehouse:** Cell shows "—" rather than "0," distinguishing "never received here" from "received but now at zero."

**Business Rules:**
- Stock levels reflect "available to promise" (ATP) — net of pending outbound reservations.
- If a transfer is in "In Transit" status, the receiving warehouse's stock does not increment until the transfer is confirmed.
- Warehouse columns are ordered alphabetically by default; user can drag to reorder.
- Maximum 20 warehouses displayed in the table; "Show more" pagination for accounts with > 20 warehouses.

**Edge Cases:**
- **Negative stock:** Display "—" and flag for data reconciliation. No negative numbers displayed.
- **Simultaneous updates to the same SKU in multiple warehouses:** WebSocket events processed in order by event timestamp.
- **SKU deactivated mid-session:** Row removed after 30 seconds with toast: "SKU [name] has been deactivated and removed from your inventory view."

---

##### REQ-INV-002: Per-Warehouse Low-Stock Alert Rules

**Feature Module:** Alerts
**Priority:** P0
**User Story:** US-002 — "As an Operations Manager, I want to set per-warehouse, per-SKU low-stock alert thresholds, so that I am notified when a SKU falls below my defined reorder point — not after it hits zero and disrupts active orders."
**Owner:** Elena Rodriguez (PM), Wei Zhang (Tech Lead)
**Status:** Approved

**What it does:**
Sellers can define low-stock alert rules at three levels: (1) per individual SKU in a specific warehouse, (2) per SKU category in a specific warehouse, and (3) globally per SKU across all warehouses. The most specific rule wins. When stock falls below the configured threshold, an alert is triggered via in-app notification and email digest.

**Preconditions:**
- User has "Admin" or "Manager" role on the warehouse for which they are creating a rule.
- The SKU exists in the seller's product catalog.
- Warehouse connection is in "Active" state.

**Main Flow:**
1. User navigates to Settings → Alert Rules (web) or Profile → Alert Settings (mobile).
2. User clicks "+ Create Alert Rule."
3. User selects the **scope**: "Specific SKU" / "SKU Category" / "All SKUs." If "Specific SKU": user searches for and selects the SKU.
4. User selects the **warehouse** for the rule (or "All Warehouses" for a global rule).
5. User sets the **threshold quantity** (positive integer). Optional: percentage of average weekly sales velocity.
6. User selects **alert channel**: In-App (default), Email (optional), Push Notification (optional — mobile only).
7. User selects **priority**: P0 (Immediate) / P1 (Daily Digest) / P2 (Weekly Digest).
8. User clicks "Save Rule." System validates threshold is a positive integer (≥ 1). Toast confirms rule creation.
9. The rule appears in the Alert Rules list. User can toggle it Active/Inactive at any time.

**Exception Flows:**
- **Threshold of 0:** Validation error: "Threshold must be at least 1 unit." Prevents saving.
- **Duplicate rule:** Warning dialog: "An identical rule already exists. Do you want to update the existing rule instead?" with [Update] / [Cancel].
- **SKU not in catalog:** Error: "SKU [code] not found in your product catalog."
- **Warehouse disconnected:** Rule suspended (not deleted). Banner: "This warehouse is disconnected. Alerts will resume automatically when the connection is restored."

**Business Rules:**
- **Most specific rule wins:** A warehouse-specific rule overrides a global rule for the same SKU.
- **Alert deduplication:** A new alert is triggered only after the SKU has risen above the threshold and crossed below it again.
- **Alert escalation:** If a P0 alert is not acknowledged within 4 hours, it escalates to the next permission level.

**Edge Cases:**
- **SKU deleted from catalog:** All associated alert rules are automatically archived with note: "Rule archived — SKU [name] was removed from your catalog on [date]."
- **Zero stock at rule creation:** If a user creates a rule for a SKU currently at 0 units, the alert fires immediately upon rule creation. Confirmation dialog: "Current stock is 0 units. Creating this rule will trigger an immediate alert. Continue?"

---

#### 3.1.3 P1 — Should Have

##### REQ-INV-003: Cross-Warehouse Transfer Workflow

**Feature Module:** Transfers
**Priority:** P1
**User Story:** US-003 — "As an Operations Manager, I want to initiate a cross-warehouse stock transfer from within SwiftStock, so that I can move inventory between warehouses without using phone calls, email, or switching to NetSuite."
**Owner:** Elena Rodriguez (PM)
**Status:** Approved (Sprint 2)

**What it does:**
A seller can initiate a stock transfer of a specified SKU and quantity from one warehouse (Source) to another warehouse (Destination) directly within SwiftStock. The transfer follows a two-step confirmation workflow: (1) Transfer Request — initiated by a Manager or Admin, and (2) Transfer Confirmation — confirmed by a Manager or Admin at the Destination warehouse after goods are physically received. Stock levels are updated only upon confirmation, not upon request.

**Preconditions:**
- User has "Admin" or "Manager" role on the Source warehouse.
- Source warehouse stock for the specified SKU is greater than or equal to the requested transfer quantity.
- Destination warehouse is in "Active" state.
- Source and Destination warehouses are distinct.

**Main Flow:**
1. User on the Multi-Warehouse Dashboard selects a SKU row and clicks "Transfer."
2. Transfer Request form opens. Fields: SKU (pre-populated or searchable), Source Warehouse, Destination Warehouse, Quantity (positive integer), Notes (optional, max 500 characters).
3. User clicks "Submit Transfer Request."
4. System validates all fields. On success:
   - Transfer is created with status "In Transit."
   - Source warehouse's available stock is immediately decremented by the transfer quantity (ATP logic).
   - A notification is sent to all Managers and Admins at the Destination warehouse.
   - The initiating user receives a confirmation with a Transfer ID (e.g., TRF-2026-04182).
5. Destination warehouse Manager or Admin logs in, navigates to Transfers → Incoming, and confirms receipt.
6. Upon confirmation, Destination warehouse's stock increments by the received quantity.
7. Transfer status updates to "Completed." Both parties receive a completion notification.

**Exception Flows:**
- **Insufficient source stock at time of transfer:** System validates against current available stock. If insufficient, submission is rejected with error: "Only [X] units available in [Source Warehouse]. Please adjust the transfer quantity." The transfer is NOT created. The form remains open with all fields preserved.
- **Destination warehouse disconnected:** System allows the transfer to be created but marks it "Pending — Destination Unreachable." Alert is sent to the user.
- **Transfer cancellation:** An Admin at the Source warehouse can cancel an "In Transit" transfer. Upon cancellation, the reserved stock is returned to the Source warehouse's available pool.

**Business Rules:**
- **Transfer reservation is immediate:** The quantity is reserved in the Source warehouse at the time of request creation.
- **Partial transfer support:** Multiple partial receipts are supported. The transfer remains open until full receipt or manual closure.
- **No inter-company transfers:** Transfers are only supported within the same seller account.

**Edge Cases:**
- **Circular transfer attempt:** System prevents this at the form validation stage. Destination dropdown excludes the selected Source warehouse.
- **Zero-quantity transfer:** Quantity = 0 is rejected at validation.
- **SKU not in destination catalog:** If the SKU is not yet in the Destination warehouse's product catalog, it is automatically added upon transfer confirmation.

---

#### 3.1.4 P2 — Could Have

**REQ-INV-005: Mobile Push Notifications for Priority SKU Alerts**
Triggered when any SKU on the user's "Priority SKU List" (a configurable list of up to 100 SKUs) crosses below its configured alert threshold. Push notification delivers within 10 seconds of the sync event. Requires user to grant push notification permission on iOS/Android.

**REQ-INV-006: Stock Level Historical Trends**
A line chart showing daily stock level snapshots for a selected SKU at a selected warehouse over the past 30 days. Data points are derived from the daily inventory snapshot taken at midnight UTC. Supports zoom (7-day, 14-day, 30-day views) and export to CSV.

---

#### 3.1.5 Won't Have (Explicitly Excluded from This Release)

| Item | Reason for Exclusion | Future Roadmap Phase |
|------|---------------------|---------------------|
| **Automated Reorder Purchase Orders** | Requires integration with supplier portals and PO workflow engine | 2027 Q1 |
| **POS Terminal Integration** | Requires hardware partnership agreements not yet finalized | 2027 Q2 |
| **Multi-Bin Location Tracking within a Warehouse** | Our data model supports warehouse-level only | 2027 Q3 |
| **EDI Integration for Enterprise Sellers** | Requires dedicated enterprise integration layer | 2026 Q4 |
| **Buyer-Facing Inventory API (External)** | Requires API Gateway and developer portal | 2026 Q4 |

---

### 3.2 Non-Functional Requirements

#### 3.2.1 Performance Requirements

| Metric | Requirement | Measurement Method | Notes |
|--------|-------------|-------------------|-------|
| **Inventory Sync Latency (P95)** | 95% of inventory updates propagate from source warehouse to SwiftStock dashboard within 5 minutes of the change event | Measured via WebSocket event timestamps: source event timestamp → dashboard render timestamp. Monitored in Datadog. | Applies only to warehouses with Active sync status. |
| **Multi-Warehouse Dashboard Load Time** | P95 < 2.5 seconds for initial load with up to 20 warehouses and 500 visible SKUs | Synthetic monitoring via Datadog Synthetic Tests; measured at CDN edge | |
| **SKU Detail Drawer Open Time** | P95 < 800ms from click to drawer fully rendered | Real User Monitoring (RUM) via Datadog RUM SDK | Mobile app: P95 < 1.5 seconds |
| **API Response Time (Read APIs)** | P99 < 500ms for all inventory read endpoints under normal load | Measured at API gateway; 30-day rolling average | Normal load defined as < 500 concurrent API requests |
| **API Response Time (Write APIs — Transfer)** | P99 < 1 second for transfer creation and confirmation endpoints | Measured at API gateway | Under normal load |
| **Concurrent Active WebSocket Connections** | Support 1,000 concurrent WebSocket connections per seller account; 10,000 per platform | Load test via k6 with WebSocket simulation | Auto-scaling trigger at 70% of limit |
| **Data Sync Error Rate** | < 0.1% of sync events result in a data error per 24-hour period | Error rate = (sync events with errors / total sync events) measured in Datadog; alerted at > 0.05% | |

#### 3.2.2 Availability Requirements

| Metric | Requirement | Measurement Method | Notes |
|--------|-------------|-------------------|-------|
| **System Uptime** | 99.5% uptime measured monthly, excluding planned maintenance windows | Datadog synthetic monitoring: 1 probe every 60 seconds from 3 global regions. | Planned maintenance windows: max 4 hours/month, announced 72 hours in advance |
| **Inventory Sync Engine Availability** | 99.0% uptime for the sync engine specifically | Custom Datadog monitor on sync worker health | |
| **Recovery Time Objective (RTO)** | < 15 minutes for non-catastrophic failures | Measured from incident detection to service restoration | Tested quarterly via chaos engineering |
| **Recovery Point Objective (RPO)** | < 5 minutes of inventory data loss for critical path events (accounts with ACV > $15K) | Measured as time between last successful sync event and failure | Achieved via real-time replication |
| **Planned Maintenance Windows** | Max 1 window per month, max 4 hours, preferred: Saturday 02:00–06:00 UTC | Communicated via Status Page and in-app banner 72 hours in advance | Emergency maintenance windows excluded from SLA |

#### 3.2.3 Security Requirements

| Requirement | Specification | Implementation Notes |
|-------------|--------------|---------------------|
| **Encryption in Transit** | All API traffic and WebSocket connections over TLS 1.2 or higher | Enforced at Cloudflare CDN and AWS ALB; TLS 1.0 and TLS 1.1 explicitly rejected |
| **Encryption at Rest** | All PII, financial data, and API keys encrypted at rest using AES-256 | AWS RDS encryption enabled; KMS key rotation every 90 days |
| **Authentication** | OAuth 2.0 with PKCE for all user-facing API calls; JWT tokens with 1-hour expiry; refresh token rotation | SwiftStock's existing auth infrastructure |
| **Role-Based Access Control (RBAC)** | Permissions enforced at the API layer; no client-side enforcement accepted | RBAC matrix defined in Appendix 7.5 |
| **Audit Logging** | All write operations logged with: user ID, timestamp, action, before/after state, IP address | Logs stored in AWS CloudWatch Logs; 90-day hot storage; 2-year archive in S3 Glacier |
| **API Rate Limiting** | 1,000 requests per minute per API key for standard accounts; 5,000 req/min for Enterprise accounts | Enforced at API gateway via Redis token bucket; returns HTTP 429 with Retry-After header |
| **Vulnerability Scanning** | Automated DAST scanning on every release; critical findings (CVSS ≥ 9.0) block deployment | Must be remediated within 24 hours |
| **Penetration Testing** | External penetration test annually | Last completed: 2026-01-15; no critical findings |

#### 3.2.4 Scalability Requirements

| Metric | Requirement | Measurement Method |
|--------|-------------|-------------------|
| **Max Warehouses per Account** | Support up to 50 warehouses per seller account | Load tested with 50 warehouses |
| **Max SKUs per Warehouse** | Support up to 100,000 active SKUs per warehouse | Load tested with 100,000 SKU catalog |
| **Max Alert Rules per Account** | Support up to 10,000 alert rules per seller account | Rule evaluation latency P95 < 100ms |
| **Max Concurrent Transfers per Account** | Support up to 200 "In Transit" transfers simultaneously per account | Load tested |

#### 3.2.5 Accessibility Requirements

| Requirement | Specification | Notes |
|-------------|--------------|-------|
| **WCAG 2.1 AA** | All user-facing web interfaces comply with WCAG 2.1 Level AA | Excludes: third-party embedded content (Salesforce side panel) |
| **Keyboard Navigation** | All interactive elements reachable via keyboard alone | Tested with axe-core in CI pipeline |
| **Screen Reader Compatibility** | All UI text readable by NVDA (Windows) and VoiceOver (macOS/iOS) | Primary user flows tested quarterly with accessibility consultant |
| **Color Contrast** | Text contrast ratio ≥ 4.5:1 for body text; ≥ 3:1 for large text and UI components | Enforced via design system tokens |

---

### 3.3 Data Tracking Requirements

| Event Name | Trigger | Parameters | User Identity |
|------------|---------|-----------|---------------|
| `multi_warehouse_view_opened` | User navigates to the multi-warehouse inventory dashboard | `account_id` (string), `user_id` (string), `warehouse_count` (integer), `view_mode` (string: "all" or "single") | Logged-in |
| `sku_row_clicked` | User clicks on a SKU row in the multi-warehouse list | `account_id`, `user_id`, `sku_id`, `sku_name`, `source_page` | Logged-in |
| `alert_rule_created` | User successfully saves a new alert rule | `account_id`, `user_id`, `rule_id`, `sku_id` (string or null), `warehouse_id`, `threshold_qty`, `priority` (P0/P1/P2) | Logged-in |
| `alert_rule_triggered` | System triggers an alert (any priority) | `account_id`, `rule_id`, `sku_id`, `warehouse_id`, `current_stock_qty`, `threshold_qty`, `alert_priority`, `delivery_channel` (in_app/email/push) | System event |
| `alert_triggered_acknowledged` | User opens or dismisses an alert | `account_id`, `user_id`, `rule_id`, `acknowledged_via` (in_app/email/push) | Logged-in |
| `transfer_request_created` | User submits a new transfer request | `account_id`, `user_id`, `transfer_id`, `sku_id`, `source_warehouse_id`, `destination_warehouse_id`, `quantity` | Logged-in |
| `transfer_confirmed` | Destination warehouse admin confirms receipt | `account_id`, `user_id`, `transfer_id`, `requested_qty`, `received_qty`, `discrepancy_flag` | Logged-in |
| `transfer_cancelled` | Source warehouse admin cancels a transfer | `account_id`, `user_id`, `transfer_id`, `reason` (optional) | Logged-in |
| `dashboard_load_time` | Web page fully loaded | `account_id`, `user_id`, `page_name`, `load_time_ms`, `connection_type` (wifi/cellular), `device_type` | Logged-in |
| `stock_level_updated_realtime` | WebSocket delivers a real-time stock update to the dashboard | `account_id`, `warehouse_id`, `sku_id`, `previous_qty`, `new_qty`, `event_type` (shipment/receipt/transfer/adjustment), `latency_ms` | System event |

---

### 3.4 User Interface Requirements

#### 3.4.1 Key Pages and Layouts

| Page / Screen | Description | Key Components | Responsive Behavior |
|---------------|-------------|----------------|--------------------|
| **Multi-Warehouse Inventory Dashboard (Web)** | Primary screen for viewing real-time stock across all warehouses | Warehouse selector (dropdown/multi-select), SKU search bar, filter bar (status/category/last updated), inventory data table with per-warehouse columns, color-coded stock cells, "Transfer" action button per row, pagination (50 SKUs per page) | Desktop-only full layout. Tablet (< 1024px): horizontal scroll enabled. Mobile (< 768px): single-warehouse view with warehouse picker. |
| **SKU Detail Drawer (Web)** | Right-side drawer showing full stock history for a single SKU across all warehouses | SKU header (name, SKU code, category), warehouse-by-warehouse stock cards, event timeline, "Create Alert Rule" CTA, "Initiate Transfer" CTA | Drawer is full-screen on mobile. |
| **Alert Rules Management (Web)** | List of all configured alert rules with edit/toggle/delete actions | Rules table (SKU/category/scope, warehouse, threshold, priority, status), "Create Rule" button, empty state | Desktop-only for Sprint 1. |
| **Transfer Center (Web)** | Central hub for all transfer activity | Tabbed view: Active (In Transit) / Pending Confirmation / Completed / Cancelled; transfer cards | Same responsive logic as dashboard. |
| **Mobile: My Alerts Screen (iOS/Android)** | List of active alerts and alert rule shortcuts | Alert list (sorted by recency), alert card (SKU name, warehouse, current stock vs. threshold), quick-action buttons | Mobile-first layout. Push notification deep-links to this screen. |
| **Salesforce Side Panel (Web)** | In-context availability check accessible from within Salesforce CRM | Search bar (SKU lookup), availability result card, "Log to Salesforce" button | Embedded in Salesforce via AppExchange. |

#### 3.4.2 Interaction Specifications

| Interaction | Component | Behavior |
|-------------|-----------|----------|
| **Click on SKU row** | Inventory list (web) | Opens SKU Detail Drawer from the right edge of the screen. Drawer width: 480px on desktop; full-screen on mobile. |
| **Click on "Transfer" button** | SKU Detail Drawer or inventory row | Opens Transfer Request modal with SKU pre-populated. |
| **Toggle alert rule Active/Inactive** | Alert Rules list | Immediate state change on click. Confirmation toast: "Rule [activated/deactivated]." |
| **Pull-to-refresh on mobile** | My Alerts / Inventory screens | Triggers full data refresh. Pull gesture threshold: 80px. 300ms haptic feedback. |
| **Real-time stock cell update** | Multi-Warehouse Dashboard | Cell flashes yellow (300ms ease-in-out) and updates to new value. No page reload. |
| **Filter change on dashboard** | Filter bar | Filters apply immediately. Loading skeleton replaces table for > 200ms render times. |
```

---

## 4. Success Metrics

### Chapter Purpose

The Success Metrics chapter establishes the quantitative framework for measuring whether the product achieves its stated goals after launch. It answers the question: *How will we know, with data, that this project succeeded or failed?*

Success metrics are decomposed into two complementary categories:

**Leading Indicators** are short-term, observable behavioral signals that precede and predict longer-term outcomes. They answer: *Are users behaving in the ways we designed them to?* Leading indicators change quickly — within days or weeks of launch — and give teams early feedback.

**Lagging Indicators** are the ultimate business outcome metrics. They answer: *Did we achieve the business goals we committed to?* Lagging indicators typically take weeks or months to move.

**The North Star Metric** is the single metric that best represents the product's core value proposition.

---

### Filling Guide

#### 4.1 North Star Metric

**What to write here:** Identify the single metric that most directly measures whether the product delivers its core value proposition.

**How to identify your North Star:**
- Ask: "What user behavior, if it increases, most unambiguously proves that our product is working?"
- Avoid metrics that are easily gamed.
- Avoid metrics that are too far downstream of user behavior.

**What to include for each metric:**
- Metric name, precise definition, target value (with baseline), measurement frequency, data source.

---

#### 4.2 Leading Indicators

**What to write here:** List 4–8 leading indicators. Each indicator needs a name, definition, target, measurement period, and the causal logic explaining *why* this indicator predicts the lagging indicator.

**Good leading indicators share these properties:**
- They are **observable within days of launch**.
- They are **directly controllable** by the product team.
- There is a **plausible causal chain** connecting them to the lagging indicator.

---

#### 4.3 Lagging Indicators

**What to write here:** List 3–6 lagging indicators. Define a measurement start date and period that accounts for seasonality.

---

#### 4.4 Metrics Relationship Map

**What to write here:** Draw the explicit causal chain connecting your leading indicators to your lagging indicators and North Star. This is the logic backbone of your measurement framework.

---

### Template Body

```markdown
## 4. Success Metrics

### 4.1 North Star Metric

| Metric Name | Definition | Baseline | Target | Measurement Frequency | Data Source | Owner |
|-------------|-----------|---------|--------|-----------------------|-------------|-------|
| [Name] | [Precise definition: what it measures, how calculated] | [Current value before launch] | [Target value and date] | [e.g., Weekly] | [e.g., Internal data warehouse / Mixpanel] | [Who is responsible for monitoring this] |

> **Why this is our North Star:** [2–3 sentences explaining why this metric best reflects the product's core value proposition.]

---

### 4.2 Leading Indicators

| # | Metric | Definition | Baseline | Target | Measurement Period | Data Source | Causal Logic |
|---|--------|-----------|---------|--------|--------------------|-------------|-------------|
| L-1 | [Name] | [What it measures — be precise] | [Current value] | [Target] | [e.g., Week 1 post-launch, measured daily] | [Source] | [If L-1 improves, we expect [Lagging Indicator] to improve because [mechanism].] |
| L-2 | [Name] | [Definition] | [Baseline] | [Target] | [Period] | [Source] | [Causal logic] |
| L-3 | [Name] | [Definition] | [Baseline] | [Target] | [Period] | [Source] | [Causal logic] |
| L-4 | [Name] | [Definition] | [Baseline] | [Target] | [Period] | [Source] | [Causal logic] |

---

### 4.3 Lagging Indicators

| # | Metric | Definition | Baseline | Target | Measurement Period | Data Source | Related Goal (Chapter 1) |
|---|--------|-----------|---------|--------|--------------------|-------------|------------------------|
| LA-1 | [Name] | [What it measures — be precise] | [Current value] | [Target] | [Start date + duration] | [Source] | [Chapter 1 Goal #] |
| LA-2 | [Name] | [Definition] | [Baseline] | [Target] | [Period] | [Source] | [Chapter 1 Goal #] |
| LA-3 | [Name] | [Definition] | [Baseline] | [Target] | [Period] | [Source] | [Chapter 1 Goal #] |
| LA-4 | [Name] | [Definition] | [Baseline] | [Target] | [Period] | [Source] | [Chapter 1 Goal #] |

---

### 4.4 Metrics Relationship Map

| Leading Indicator | → Predicts Improvement In | Because of This Mechanism |
|-------------------|--------------------------|--------------------------|
| [L-1] | [Lagging Indicator / North Star] | [Explicit causal mechanism] |
| [L-2] | [Lagging Indicator] | [Mechanism] |
| [L-3] | [Lagging Indicator] | [Mechanism] |
| [Combined: L-2 + L-3] | [Lagging Indicator / North Star] | [When both indicators improve together, they compound the effect] |

**Key Assumptions in this Causal Chain:**
- [Assumption 1]
- [Assumption 2]
- [Assumption 3]

**What Will Invalidate this Chain (Early Warning Signals):**
- [Signal 1]
- [Signal 2]

---

### 4.5 Instrumented Dashboards and Reporting Cadence

| Dashboard | Purpose | Access | Refresh Frequency | Owner |
|-----------|---------|--------|-------------------|-------|
| [Dashboard name] | Tracks all launch metrics in real time | [Who has access] | [Frequency] | [Owner] |

**Review Cadence:**
- **Daily (Weeks 1–2 post-launch):** PM reviews all leading indicators. Any metric below 70% of target triggers investigation.
- **Weekly (Weeks 3–8):** Full product team review of leading indicators and early lagging indicator signals.
- **Monthly (Month 2+):** Executive summary of lagging indicator movement.
- **Quarterly:** Comprehensive post-launch retrospective.

---

### 4.6 Technical Performance Metrics (Aligned with NFRs)

| Metric | Definition | Target | Measurement Method | Alert Threshold |
|--------|------------|--------|-------------------|----------------|
| [e.g., Inventory Sync Latency (P95)] | Time from source warehouse change event to dashboard update | < 5 minutes for 95% of events | [Datadog WebSocket trace] | > 8 minutes triggers PagerDuty alert |
| [e.g., Dashboard Availability] | % of time the dashboard is accessible and responsive | ≥ 99.5% | [Datadog synthetic monitoring] | < 99.0% triggers incident |
| [e.g., Sync Error Rate] | % of daily sync events with data errors | < 0.1% | [Datadog error rate dashboard] | > 0.05% triggers Slack alert to Eng Lead |
```

---

### Example Content

> **Example Product:** SwiftStock — Multi-Warehouse Inventory Sync Module (continued)

---

```markdown
## 4. Success Metrics

### 4.1 North Star Metric

| Metric Name | Definition | Baseline | Target | Measurement Frequency | Data Source | Owner |
|-------------|-----------|---------|--------|-----------------------|-------------|-------|
| **Stockout-Driven Order Cancellation Rate** | Percentage of all confirmed orders that are subsequently partially or fully cancelled because the warehouse cannot fulfill the order due to a stockout that existed at the time of order confirmation | **12.0%** (measured over 90-day pre-launch window: 2025-Q4) | **≤ 8.4%** (30% reduction) by 90 days post-launch (target date: 2026-Q4) | Weekly | SwiftStock Order Management System (OMS); calculated as (cancelled orders due to stockout / total confirmed orders) × 100 | Elena Rodriguez (PM) |

> **Why this is our North Star:** This metric directly measures the core pain point identified in Chapter 1 — the gap between confirmed orders and actual fulfillment capacity due to stale inventory data. It is unambiguous: a cancelled order is a measurable, costly failure. It is not easily gamed. And it directly ties to SwiftStock's value proposition: real-time inventory visibility prevents order cancellations.

---

### 4.2 Leading Indicators

| # | Metric | Definition | Baseline | Target | Measurement Period | Data Source | Causal Logic |
|---|--------|-----------|---------|--------|--------------------|-------------|-------------|
| **L-1** | **Low-Stock Alert Configuration Rate** | Percentage of multi-warehouse seller accounts that have configured at least one active low-stock alert rule, out of all eligible accounts (≥ 2 warehouses, active for > 30 days) | **8%** (measured Feb 2026) | **≥ 50%** within 60 days of launch | Week 1 post-launch, measured weekly | SwiftStock product database | **If more sellers configure alerts → they receive earlier warnings → can take action before stockouts occur → cancellation rate decreases.** |
| **L-2** | **Alert-to-Transfer Action Rate** | Percentage of triggered P0 alerts that result in a transfer request being created within 24 hours of alert receipt | **N/A** (new metric) | **≥ 25%** within 60 days post-launch | Week 1 post-launch, measured weekly | SwiftStock product database | **If alerts are actionable (good timing, clear signal) → sellers will initiate transfers → stock moves from surplus to shortage warehouses → stockout is averted → order is fulfilled.** This is the critical conversion point in our value chain. |
| **L-3** | **Multi-Warehouse Dashboard Weekly Active Users (WAU)** | Number of unique users who access the Multi-Warehouse Inventory Dashboard at least once in a 7-day period, divided by total eligible users | **41%** WAU ratio (measured Feb 2026) | **≥ 65%** WAU ratio within 60 days post-launch | Week 1 post-launch, measured weekly | SwiftStock product analytics (Mixpanel) | **If more operations managers use the real-time dashboard → they catch discrepancies earlier → they act before stockouts → cancellation rate decreases.** |
| **L-4** | **Time to First Transfer (New Users)** | Median time (in days) from a user's first login after launch to the creation of their first transfer request | **N/A** (new metric) | **≤ 14 days** median for accounts who have configured alerts | Measured continuously from Day 1; first analysis at Day 30 | Mixpanel | **Fast time-to-value predicts long-term retention.** |
| **L-5** | **Alert Acknowledgement Rate** | Percentage of triggered P0 alerts that are opened or acknowledged by at least one user within 4 hours of firing | **N/A** (new metric) | **≥ 60%** within 30 days post-launch | Week 1 post-launch, measured daily | Mixpanel | **If alerts are seen → sellers can prevent stockouts. If alerts go unacknowledged, they are warnings to no one.** |

---

### 4.3 Lagging Indicators

| # | Metric | Definition | Baseline | Target | Measurement Period | Data Source | Related Goal (Chapter 1) |
|---|--------|-----------|---------|--------|--------------------|-------------|------------------------|
| **LA-1** | **Stockout-Driven Order Cancellation Rate** | *(This is the North Star — see 4.1)* | 12.0% | ≤ 8.4% | 30 days post-launch onward; reviewed weekly; target assessed at 90 days | SwiftStock OMS | **Goal #1** |
| **LA-2** | **SwiftStock Support Ticket Volume (Stockout-Related)** | Number of Tier-1 support tickets categorized as "Stockout Dispute" per month | **340 hours/month** (average Q4 2025) | **≤ 255 hours/month** (25% reduction) | 60 days post-launch; reviewed monthly | Zendesk ticket data | **Goal #4** |
| **LA-3** | **Seller Churn Rate (Stockout-Attributed)** | Percentage of seller accounts that cancel their subscription within 90 days of experiencing ≥ 3 stockout cancellations | **11.3%** (historical benchmark) | **≤ 9.5%** (20% reduction) | 90 days post-launch; measured quarterly | SwiftStock billing system | **Goal #1 (indirect)** |
| **LA-4** | **Customer Satisfaction Score (Stockout-Related)** | NPS/CSAT score for support interactions tagged "stockout_dispute," measured via post-resolution survey | **NPS: 28** (Q4 2025) | **NPS: ≥ 40** | 60 days post-launch; reviewed monthly | Zendesk NPS survey | **Goal #4 (indirect)** |
| **LA-5** | **Account Revenue at Risk from Stockouts** | Estimated monthly revenue represented by orders partially or fully cancelled due to stockouts | **$175,000/month** (platform-wide extrapolation) | **≤ $122,500/month** (30% reduction) | 90 days post-launch | SwiftStock OMS + billing data | **Goal #1 (financial impact)** |

---

### 4.4 Metrics Relationship Map

| Leading Indicator | → Predicts Improvement In | Because of This Mechanism |
|-------------------|--------------------------|--------------------------|
| **L-1: Alert Configuration Rate** (≥ 50%) | **LA-1: Stockout Cancellation Rate** | Sellers who configure alerts receive early warnings → proactive action → inventory arrives before stockout → cancellation avoided. |
| **L-2: Alert-to-Transfer Action Rate** (≥ 25%) | **LA-1: Stockout Cancellation Rate** | Each transfer created from an alert represents a prevented stockout. This is the most direct leading → lagging link. |
| **L-3: Dashboard WAU Ratio** (≥ 65%) | **LA-1: Cancellation Rate** and **LA-2: Support Tickets** | Managers who check the real-time dashboard catch discrepancies before they become order-impacting events. |
| **L-5: Alert Acknowledgement Rate** (≥ 60%) | **L-2: Alert-to-Transfer Action Rate** | Alerts must be seen before they can be acted upon. If < 60% of P0 alerts are acknowledged within 4 hours, we have a notification delivery problem. |
| **L-1 + L-2 + L-3 combined** | **LA-3: Seller Churn Rate** | Sellers who configure alerts (L-1), act on them (L-2), and regularly use the dashboard (L-3) experience fewer stockouts and fewer support frustrations → higher retention. |

**Key Assumptions in this Causal Chain:**
1. **Alerts fire at the right time.** We assume a stock level crossing below the threshold is an actionable event. *Validation method:* Survey 20 sellers in Week 4: "Were you able to prevent the stockout after receiving this alert?"
2. **Transfer is the right solution.** For single-warehouse sellers, transfers are not possible — only reorders. *Validation method:* Segment L-2 by single vs. multi-warehouse accounts.
3. **Notification delivery is reliable.** *Validation method:* Monitor delivery timestamps vs. firing timestamps in Mixpanel.

**What Will Invalidate this Chain (Early Warning Signals):**
- **If L-5 (Alert Acknowledgement Rate) < 40%:** The bottleneck is notification delivery or timing. Investigate email/push deliverability before assuming the feature is flawed.
- **If L-5 ≥ 60% but L-2 (Alert-to-Transfer Rate) < 15%:** Alerts are seen but not acted upon. The problem is in the transfer workflow — too many steps or insufficient authorization.
- **If L-2 ≥ 25% but LA-1 does not improve by Day 60:** Transfers are created but are not preventing cancellations. Investigate transfer lead time vs. customer cancellation window.

---

### 4.5 Instrumented Dashboards and Reporting Cadence

| Dashboard | Purpose | Access | Refresh Frequency | Owner |
|-----------|---------|--------|-------------------|-------|
| **Multi-Warehouse Launch Dashboard (Datadog + Mixpanel)** | Real-time view of all leading indicators (L-1 through L-5) and technical performance metrics | PM (Elena Rodriguez), Engineering Lead (Wei Zhang), VP Product | Real-time (Datadog); daily refresh (Mixpanel) | Elena Rodriguez |
| **SwiftStock Business Review Dashboard (Looker)** | Monthly view of lagging indicators (LA-1 through LA-5) with trend lines and account-level drill-down | Executive team, CS leadership, PM | Daily refresh; reviewed monthly | David Okafor + Elena Rodriguez |
| **Gainsight Customer Health Dashboard** | Account-level adoption scores, alert configuration status, and churn risk indicators | CS Manager (David Okafor), CSRs | Daily refresh | David Okafor |
| **Salesforce CS Tier-1 Ticket Dashboard (Zendesk)** | Weekly volume and trend of stockout-related support tickets | CS Manager, PM | Daily | CS Manager |

**Review Cadence:**
- **Daily (Weeks 1–2 post-launch):** PM reviews all leading indicators. Any metric below 70% of its 30-day target triggers a same-day investigation.
- **Weekly (Weeks 3–8):** Full product team review. PM shares a written status report in the #multi-warehouse-launch Slack channel.
- **Monthly (Month 2+):** Executive summary of lagging indicator movement. If LA-1 has not moved at least 10% toward target by Day 60, a strategic product review is triggered.
- **Quarterly:** Comprehensive post-launch retrospective.

---

### 4.6 Technical Performance Metrics (Aligned with NFRs from Chapter 3)

| Metric | Definition | Target | Measurement Method | Alert Threshold |
|--------|------------|--------|-------------------|----------------|
| **Inventory Sync Latency (P95)** | 95th percentile time from source warehouse change event to WebSocket push reaching the dashboard | < 5 minutes | Datadog WebSocket trace | > 8 minutes → PagerDuty alert |
| **Dashboard Availability** | % of time Multi-Warehouse Dashboard returns a non-error response within 3 seconds | ≥ 99.5% | Datadog synthetic monitoring | < 99.0% → incident declared |
| **Sync Error Rate** | % of daily sync events resulting in a data error | < 0.1% per 24 hours | Datadog: `sync.events.total` vs `sync.events.error` | > 0.05% → Slack alert to Engineering Lead |
| **Alert Delivery Latency (P95)** | Time from alert trigger to alert received on user's device | < 30 seconds | Mixpanel: delivery receipt timestamp | > 2 minutes → alert to Eng Lead |
| **Transfer API Error Rate** | % of transfer API calls returning HTTP 4xx or 5xx | < 0.5% | Datadog API monitor | > 1% → PagerDuty alert |
```

---

## 5. Acceptance Criteria

### Chapter Purpose

The Acceptance Criteria chapter defines the **Definition of Done** for each requirement using the **Given/When/Then (GWT)** format from Behavior-Driven Development (BDD). Each criterion is a testable statement with three components: **Given** (preconditions that must be true before testing begins), **When** (the specific user action or system event that triggers the test), and **Then** (the concrete, observable result that must occur).

The Given/When/Then format is not a stylistic preference — it is a precision tool. The format's discipline forces the author to be explicit about preconditions, specific about actions, and objectively verifiable about outcomes.

**The relationship between this chapter and the rest of the PRD:**
- **From Chapter 3:** Every functional requirement (REQ-###) must have at least one acceptance criterion.
- **From Chapter 2:** Acceptance criteria should reflect real user flows and edge cases.
- **To QA:** Acceptance criteria translate directly into test cases.
- **To Engineering:** Engineers use these criteria as a checklist during development.

---

### Filling Guide

**The Given/When/Then anatomy:**
- **Given:** Describes the *initial state* of the system — user authentication state, pre-existing data, prior user actions.
- **When:** Describes the *trigger* — the single, specific action or event. The When clause should describe one action at a time.
- **Then:** Describes the *observable outcome* — the specific changes in the system's state, UI, or data. Outcomes must be objectively verifiable.

**Criteria quality checklist:**
- [ ] The Given clause establishes a specific, reproducible state.
- [ ] The When clause describes a single action — not a sequence of multiple steps.
- [ ] The Then clause describes an objectively observable outcome.
- [ ] Each criterion is *independent* — it can be executed in isolation.
- [ ] Each criterion maps to a specific requirement ID (REQ-###).
- [ ] Each criterion can be automated.

**Common mistakes to avoid:**
- Writing criteria that describe UI implementation rather than user outcomes.
- Writing criteria that are too vague to be tested.
- Omitting negative criteria (what happens with invalid input).
- Writing criteria that assume perfect network conditions.

---

### Template Body

```markdown
## 5. Acceptance Criteria

> **How to Read This Chapter:** Each section corresponds to a requirement (REQ-###) from Chapter 3. Acceptance criteria are written in Given/When/Then format. Each criterion is independently executable and objectively verifiable. QA Engineers should be able to use these criteria directly as test case specifications without additional clarification.

### 5.1 [Requirement Title] (REQ-[###])

**Feature Module:** [Module Name]
**Priority:** P0 / P1 / P2
**Total Acceptance Criteria:** [N criteria: e.g., "5 criteria: 1 primary flow, 2 exception flows, 2 edge cases"]

---

**Acceptance Criterion 1: [Criterion Name]**

- **Given:** [Specific preconditions — user identity, authentication state, existing data state]
- **When:** [The single, specific action or event that triggers this test]
- **Then:** [The observable, verifiable outcome]

---

**Acceptance Criterion 2: [Exception Flow: Invalid Input]**

- **Given:** [Preconditions]
- **When:** [Action]
- **Then:** [Outcome — specifically, how the error is communicated to the user]

---

**Acceptance Criterion 3: [Exception Flow: Network Error]**

- **Given:** [Preconditions]
- **When:** [Action — specifically, the error condition being tested]
- **Then:** [Outcome — error handling behavior]

---

[Continue for all criteria]

---

### 5.2 [Next Requirement] (REQ-[###])

[Repeat structure]

---

### 5.3 Integration Acceptance Criteria

> **Integration criteria** verify end-to-end behavior across multiple requirements.

**Integration Criterion 1: [End-to-End: Alert → Transfer → Stock Update → Alert Resolution]**

- **Given:** [State setup]
- **When:** [Full end-to-end chain of events]
- **Then:** [Observable end-to-end outcome]
```

---

### Example Content

> **Example Product A:** SwiftStock — Multi-Warehouse Inventory Sync Module (continued)

---

```markdown
## 5. Acceptance Criteria

> **How to Read This Chapter:** Each section corresponds to a requirement (REQ-###) from Chapter 3. Acceptance criteria are written in Given/When/Then format. Each criterion is independently executable and objectively verifiable. QA Engineers should be able to use these criteria directly as test case specifications. All criteria marked P0 must pass before the feature is eligible for production release. Criteria marked P1 should pass; P1 failures require a documented exception approved by the PM.

---

### 5.1 Real-Time Cross-Warehouse Stock Visibility (REQ-INV-001)

**Feature Module:** Inventory Sync
**Priority:** P0
**Total Acceptance Criteria:** 8 criteria (1 primary flow, 3 exception/error flows, 2 edge cases, 2 real-time update criteria)

---

**Acceptance Criterion 1: Primary Flow — View Stock Levels Across All Warehouses**

- **Given:** Marcus Chen is logged into SwiftStock with Admin role on all 4 warehouses (Warehouse 1: Los Angeles, Warehouse 2: Portland, Warehouse 3: Sacramento, Warehouse 4: San Jose). The WebSocket connection is active and authenticated.
- **When:** Marcus navigates to the Inventory section and selects the Multi-Warehouse view toggle.
- **Then:** The dashboard loads within 2.5 seconds and displays a table with one row per SKU and one column per warehouse. Each cell shows the current ATP stock quantity, color-coded: Green (> threshold), Amber (below threshold but > 0), Red (= 0). Default sort is alphabetical by SKU name. The table includes 4 warehouse columns correctly labeled with warehouse names and locations.

---

**Acceptance Criterion 2: Real-Time Update — Stock Cell Updates Without Page Reload**

- **Given:** Marcus is viewing the Multi-Warehouse Dashboard for SKU-4421. Warehouse 1 (Los Angeles) currently shows 320 units.
- **When:** A warehouse operator at Warehouse 1 records a goods issue of 50 units (reducing available stock from 320 to 270 units). The change event is processed and pushed via WebSocket.
- **Then:** Within 5 minutes of the warehouse event, the Warehouse 1 cell for SKU-4421 updates to show 270 units. A yellow flash animation (300ms ease-in-out) plays on the updated cell. No page reload or manual refresh is required. Marcus remains on the same page and does not lose his current scroll position or filter state.

---

**Acceptance Criterion 3: Real-Time Update — WebSocket Reconnection After Network Interruption**

- **Given:** Marcus's WebSocket connection is active. His network connection drops for 45 seconds and then reconnects.
- **When:** After the connection reconnects, a stock update event for SKU-4421 in Warehouse 2 fires while the connection was down.
- **Then:** Upon reconnection, the WebSocket client immediately fetches the latest stock state from the REST API. The affected cell is updated within 3 seconds of reconnection. No duplicate updates are processed (event deduplication by event ID).

---

**Acceptance Criterion 4: Exception Flow — Warehouse Sync in Error State**

- **Given:** Warehouse 3 (Sacramento) has an Active sync connection. A network error causes Warehouse 3's connection to enter "Error" state. Last known stock for SKU-4421 in Warehouse 3 was 180 units (captured at 14:32 UTC).
- **When:** Marcus opens the Multi-Warehouse Dashboard and views SKU-4421.
- **Then:** The Warehouse 3 column for SKU-4421 displays "Sync Error" in red text. A tooltip on hover reads: "Sync error since [timestamp]. Last known value: 180 units." The stale value is labeled "(as of 14:32 UTC)" in gray italic text. The rest of the dashboard (other warehouses, other SKUs) functions normally.

---

**Acceptance Criterion 5: Exception Flow — SKU Never Received in a Warehouse (Distinguished from Zero Stock)**

- **Given:** SKU-8801 (Premium Bearing Kit) has been received in Warehouse 1 (120 units) and Warehouse 2 (0 units — shipped out) but has never been received in Warehouse 3.
- **When:** Marcus views SKU-8801 in the Multi-Warehouse Dashboard.
- **Then:** Warehouse 1 shows "120" (Green). Warehouse 2 shows "0" (Red — received but at zero). Warehouse 3 shows "—" (em dash, gray text — never received in this warehouse). The distinction between "—" (never received) and "0" (received but at zero) is visually clear.

---

**Acceptance Criterion 6: Edge Case — Negative Stock Value Received from Sync**

- **Given:** A sync error at Warehouse 2 results in a negative stock value of -5 units being received for SKU-1234.
- **When:** The WebSocket processes this event and the dashboard attempts to render the updated cell.
- **Then:** The cell displays "—" (error state) with a red background tint. A data reconciliation flag is automatically created in SwiftStock's internal issue tracking system with fields: `sku_id`, `warehouse_id`, `invalid_value`, `received_at`. No negative numbers are displayed anywhere in the UI. The CS manager receives an email alert.

---

**Acceptance Criterion 7: Edge Case — SKU Deactivated Mid-Session**

- **Given:** Marcus is actively viewing SKU-9911 (Discontinued Model-X Bearing) in the Multi-Warehouse Dashboard. An Admin deactivates SKU-9911 in the product catalog.
- **When:** The deactivation event is processed and pushed via WebSocket.
- **Then:** Within 5 minutes, the SKU-9911 row is removed from Marcus's visible inventory list. A toast notification appears: "SKU 'Discontinued Model-X Bearing' (SKU-9911) has been deactivated and removed from your inventory view." The removal is smooth (fade-out animation, 300ms).

---

**Acceptance Criterion 8: Filter and Sort — Stock Status Filter**

- **Given:** Marcus is viewing a list of 500 SKUs across 4 warehouses.
- **When:** Marcus clicks the filter chip "Out of Stock" in the filter bar.
- **Then:** The list immediately (within 300ms) filters to show only SKUs where at least one warehouse has 0 units. The filter chip is highlighted (active state). The result count is shown: "Showing 47 of 500 SKUs." Clicking the chip again deactivates the filter and returns to the full list.

---

### 5.2 Per-Warehouse Low-Stock Alert Rules (REQ-INV-002)

**Feature Module:** Alerts
**Priority:** P0
**Total Acceptance Criteria:** 9 criteria (2 primary flows, 3 validation/exception flows, 2 edge cases, 2 notification delivery criteria)

---

**Acceptance Criterion 1: Primary Flow — Create Alert Rule for a Specific SKU**

- **Given:** Marcus is logged into SwiftStock with Admin role on Warehouse 2 (Portland). SKU-4421 exists in the product catalog with current stock of 52 units in Warehouse 2. No alert rule currently exists for SKU-4421 in Warehouse 2.
- **When:** Marcus navigates to Settings → Alert Rules, clicks "+ Create Alert Rule," selects "Specific SKU" → SKU-4421, Warehouse 2, threshold 50 units, priority P0 (Immediate), channels In-App + Email. Clicks "Save Rule."
- **Then:** The rule is saved successfully. A confirmation toast appears: "Alert rule created for SKU-4421 in Warehouse 2 (threshold: 50 units)." The rule appears in the Alert Rules list with status "Active." Since 52 > 50, no alert is triggered. When stock falls to 49 or below, the P0 alert fires.

---

**Acceptance Criterion 2: Primary Flow — Alert Fires When Stock Crosses Below Threshold**

- **Given:** Marcus has an active alert rule for SKU-4421 in Warehouse 2 with threshold 50 units (P0, In-App + Email). Current stock in Warehouse 2 is 52 units. An order picks 8 units of SKU-4421 from Warehouse 2, reducing available stock to 44 units.
- **When:** The stock change event is processed and the system evaluates alert rules. Stock in Warehouse 2 is now 44 units, below the 50-unit threshold.
- **Then:** A P0 alert is triggered within 30 seconds of the stock change event. (1) In-App notification: red alert card appears at the top of Marcus's SwiftStock dashboard: "⚠️ Low Stock Alert: SKU-4421 (Industrial Bearings 8mm) in Warehouse 2 is at 44 units — below your threshold of 50 units." (2) Email to Marcus's registered address: subject "⚠️ SwiftStock Low-Stock Alert — SKU-4421, Warehouse 2." The alert is logged in the Alert History with timestamp and delivery confirmation.

---

**Acceptance Criterion 3: Validation — Threshold of Zero Rejected**

- **Given:** Marcus is on the "Create Alert Rule" form.
- **When:** Marcus enters "0" as the threshold quantity and clicks "Save Rule."
- **Then:** The form does not submit. An inline validation error appears: "Threshold must be at least 1 unit." The field border turns red. No alert is created.

---

**Acceptance Criterion 4: Validation — Threshold of Negative Number Rejected**

- **Given:** Marcus is on the "Create Alert Rule" form.
- **When:** Marcus enters "-10" as the threshold quantity and attempts to save.
- **Then:** The form does not submit. Validation error appears: "Threshold must be a positive number." No negative thresholds can be saved under any circumstances.

---

**Acceptance Criterion 5: Exception Flow — Duplicate Rule Warning**

- **Given:** Marcus already has an active rule for SKU-4421 in Warehouse 2 with threshold 50 units. He opens the "Create Alert Rule" form and selects SKU-4421, Warehouse 2, threshold 50.
- **When:** Marcus clicks "Save Rule."
- **Then:** The system displays a warning dialog: "An identical alert rule already exists for SKU-4421 in Warehouse 2 (threshold: 50 units, P0, Active). Do you want to update the existing rule instead?" with [Update Existing Rule] and [Cancel]. Clicking [Update Existing Rule] navigates to the edit view. Clicking [Cancel] closes the dialog with all fields preserved.

---

**Acceptance Criterion 6: Exception Flow — Alert Does Not Re-Fire for Same Stock Level Event**

- **Given:** Marcus has an active P0 alert for SKU-4421 in Warehouse 2 (threshold: 50). Alert has fired because stock dropped to 44. Marcus has acknowledged the alert but has not yet resolved the stock shortage. Stock drops further to 39 units.
- **When:** The system processes the new stock change event (44 → 39 units).
- **Then:** No new P0 alert is triggered. The original alert remains in "Acknowledged" state. A new alert is triggered only when stock rises above the threshold (50) and then falls below it again.

---

**Acceptance Criterion 7: Edge Case — Alert Created for SKU Already Below Threshold**

- **Given:** SKU-4421 is currently at 30 units in Warehouse 2 (already below the 50-unit threshold Marcus wants to set).
- **When:** Marcus opens the "Create Alert Rule" form, selects SKU-4421, Warehouse 2, threshold 50, and clicks "Save Rule."
- **Then:** Before saving, the system displays a confirmation dialog: "Current stock for SKU-4421 in Warehouse 2 is 30 units — already below your threshold of 50 units. Creating this rule will trigger an immediate alert. Continue?" with [Create & Trigger Alert] and [Cancel]. If Marcus clicks [Create & Trigger Alert], the rule is saved AND the P0 alert fires immediately.

---

**Acceptance Criterion 8: Edge Case — Rule Suspended When Warehouse Disconnected**

- **Given:** Marcus has an active alert rule for SKU-4421 in Warehouse 2 (threshold 50, P0). Warehouse 2's connection enters "Disconnected" state due to a network outage.
- **When:** The disconnection event is processed by the sync engine.
- **Then:** Marcus's alert rule for Warehouse 2 is automatically suspended (status changes from "Active" to "Suspended — Warehouse Disconnected"). A banner appears: "⚠️ This rule is paused because Warehouse 2 is not connected. Alerts will resume automatically when the connection is restored." No alerts fire while Warehouse 2 is disconnected. When Warehouse 2 reconnects, the rule automatically resumes to "Active" status and evaluates current stock levels immediately.

---

**Acceptance Criterion 9: Notification Delivery — Push Notification on iOS**

- **Given:** Marcus has granted SwiftStock push notification permission on his iPhone 14 (iOS 17). He is logged into the SwiftStock iOS app with a valid push token. He has an active P0 alert rule for SKU-4421 in Warehouse 2.
- **When:** Stock of SKU-4421 in Warehouse 2 drops from 52 to 44 units, triggering the P0 alert.
- **Then:** Marcus receives a push notification on his iPhone within 30 seconds. Notification title: "⚠️ Low Stock — SKU-4421." Body: "Warehouse 2: 44 units (threshold: 50)." Tapping the notification opens the SwiftStock iOS app directly to the My Alerts screen, showing full alert details. The notification is delivered even when the app is in the background.

---

### 5.3 Cross-Warehouse Transfer Workflow (REQ-INV-003)

**Feature Module:** Transfers
**Priority:** P1
**Total Acceptance Criteria:** 10 criteria (2 primary flows, 4 exception flows, 2 business rule validations, 2 edge cases)

---

**Acceptance Criterion 1: Primary Flow — Create and Confirm Transfer (Full Quantity)**

- **Given:** Marcus (Admin on Warehouse 1 and Warehouse 2) is logged into SwiftStock. Warehouse 1 (Los Angeles) has 320 units of SKU-4421. Warehouse 2 (Portland) has 44 units. No pending transfers exist for SKU-4421 between these warehouses.
- **When:** Marcus clicks "Transfer" from the SKU-4421 row. He selects: Source: Warehouse 1, Destination: Warehouse 2, Quantity: 80 units. Adds note "Urgent: covering order #ORD-8841." Clicks "Submit Transfer Request."
- **Then:** The transfer is created with status "In Transit." Marcus receives confirmation: "Transfer TRF-2026-04182 created. 80 units reserved in Warehouse 1. Destination will confirm receipt." Warehouse 1's available stock decreases from 320 to 240 units immediately. Warehouse 2's stock remains at 44 until confirmed. A notification is sent to all Managers and Admins on Warehouse 2.

---

**Acceptance Criterion 2: Primary Flow — Destination Warehouse Confirms Receipt (Full Quantity)**

- **Given:** Transfer TRF-2026-04182 exists: 80 units of SKU-4421 from Warehouse 1 to Warehouse 2, status "In Transit." Marcus (Admin on Warehouse 2) is logged in. The physical goods have arrived at Warehouse 2.
- **When:** Marcus navigates to Transfers → Incoming, locates TRF-2026-04182, clicks "Confirm Receipt," enters received quantity: 80 (matching requested), and clicks "Confirm."
- **Then:** Transfer status updates to "Completed." Warehouse 2's stock for SKU-4421 increases from 44 to 124 units. Both Marcus (initiator) and the Warehouse 2 Manager receive a completion notification. The transfer is logged in Transfer History with full audit trail.

---

**Acceptance Criterion 3: Exception Flow — Insufficient Source Stock at Transfer Creation**

- **Given:** Warehouse 1 (Los Angeles) has 320 units of SKU-4421. Another process (an order reservation) has reserved 300 units from Warehouse 1, leaving only 20 units available.
- **When:** Marcus enters Source: Warehouse 1, Quantity: 80, and clicks "Submit Transfer Request."
- **Then:** The system validates current available stock. Since only 20 units are available, the submission is rejected. An inline error appears: "Insufficient stock in Warehouse 1 (Los Angeles). Available: 20 units. Please adjust the transfer quantity or select a different source warehouse." The transfer is NOT created. The form remains open with all fields preserved.

---

**Acceptance Criterion 4: Exception Flow — Partial Receipt Confirmation**

- **Given:** Transfer TRF-2026-04182 exists: 80 units from Warehouse 1 to Warehouse 2, status "In Transit." Only 65 units were physically received (15 units delayed in transit).
- **When:** Marcus at Warehouse 2 clicks "Confirm Receipt," enters 65 (less than 80), and clicks "Confirm."
- **Then:** The system prompts: "You are confirming receipt of 65 of 80 requested units. 15 units are outstanding. What would you like to do?" with [Confirm Partial — Close Transfer] and [Confirm Partial — Keep Open]. Marcus selects [Confirm Partial — Keep Open]. Warehouse 2's stock increases by 65 units (44 + 65 = 109). Transfer remains "In Transit" with indicator: "65 of 80 units received. 15 units outstanding."

---

**Acceptance Criterion 5: Exception Flow — Cancel Transfer Before Confirmation**

- **Given:** Transfer TRF-2026-04182 exists: 80 units from Warehouse 1 to Warehouse 2, status "In Transit."
- **When:** Marcus opens the transfer detail and clicks "Cancel Transfer." He optionally enters a reason: "Customer cancelled order #ORD-8841."
- **Then:** Transfer status changes to "Cancelled." The reserved stock of 80 units in Warehouse 1 is immediately released back to available stock (240 + 80 = 320). A notification is sent to Warehouse 2 Managers. The cancellation is logged in Transfer History with timestamp and reason.

---

**Acceptance Criterion 6: Validation — Zero Quantity Rejected**

- **Given:** Marcus is on the "New Transfer" form.
- **When:** Marcus enters Quantity: 0 and attempts to submit.
- **Then:** The form does not submit. An inline validation error appears: "Transfer quantity must be at least 1 unit." No transfer is created.

---

**Acceptance Criterion 7: Validation — Same Source and Destination Warehouse Rejected**

- **Given:** Marcus is on the "New Transfer" form.
- **When:** Marcus selects the same warehouse for both Source and Destination.
- **Then:** The Destination warehouse dropdown does not allow selecting the same warehouse as the Source. Warehouse 1 is immediately removed from the Destination dropdown once selected as Source. Attempting to bypass this via API returns error: "Source and Destination warehouses must be different."

---

**Acceptance Criterion 8: Validation — Transfer Quantity Exceeds Available Stock**

- **Given:** Warehouse 1 has 50 units of SKU-4421 available.
- **When:** Marcus attempts to enter Transfer Quantity: 75 and submits.
- **Then:** Form submission is rejected with error: "Insufficient stock. Available in Warehouse 1: 50 units." The form remains open. No transfer is created.

---

**Acceptance Criterion 9: Edge Case — Destination Warehouse Connection Lost Before Transfer Creation**

- **Given:** Warehouse 2 (Portland) connection enters "Error" state. Marcus attempts to create a transfer from Warehouse 1 to Warehouse 2.
- **When:** Marcus selects Destination: Warehouse 2 (which shows "Error" or "Disconnected" indicator) and submits the transfer request.
- **Then:** The system allows the transfer to be created but marks it "Pending — Destination Unreachable." A warning banner is shown: "Warehouse 2 is not currently connected. This transfer will update stock when the connection is restored." Warehouse 1's stock is reserved immediately.

---

**Acceptance Criterion 10: Edge Case — Multiple Simultaneous Transfer Requests for Same SKU**

- **Given:** Warehouse 1 has 100 units of SKU-4421. Marcus creates Transfer A: 60 units from Warehouse 1 to Warehouse 2 (still "In Transit," not yet confirmed).
- **When:** While Transfer A is pending, Marcus creates Transfer B: 50 units from Warehouse 1 to Warehouse 3.
- **Then:** System validates against current available stock for Warehouse 1. Available = 100 − 60 (reserved by Transfer A) = 40 units. Transfer B requests 50 units. Submission is rejected: "Insufficient stock in Warehouse 1. 60 units are reserved for transfer TRF-[XXX]. Available: 40 units." Marcus can reduce the quantity to 40 or wait for Transfer A to be confirmed or cancelled.

---

### 5.4 Integration Acceptance Criteria

**Integration Criterion 1: End-to-End — Low-Stock Alert → Transfer Request → Stock Confirmation → Alert Resolution**

- **Given:** Marcus has an active P0 alert for SKU-4421 in Warehouse 2 at threshold 50 units. Current stock in Warehouse 2 is 52 units. Warehouse 1 (Los Angeles) has 320 units of SKU-4421.
- **When:** An order picks 8 units from Warehouse 2, reducing stock from 52 to 44 units. The P0 alert fires. Marcus receives the alert. Marcus creates a transfer of 80 units from Warehouse 1 to Warehouse 2. Warehouse 2 receives the transfer and confirms receipt of 80 units.
- **Then:** (1) Alert fires within 30 seconds of stock crossing below threshold. (2) Marcus can create the transfer from the alert deep-link without re-navigating to the inventory dashboard. (3) Upon confirmation, Warehouse 2's stock increments by 80 units, reaching 124 units. (4) The P0 alert is automatically marked as "Action Taken" in the alert history, with a reference to transfer TRF-2026-04182. Marcus receives a notification: "Alert resolved: Stock replenished via transfer TRF-2026-04182."

---

**Integration Criterion 2: End-to-End — Real-Time Sync Accuracy Across Multiple Concurrent Warehouses**

- **Given:** Marcus has 4 warehouses connected: W1 (320 units SKU-4421), W2 (44 units), W3 (95 units), W4 (210 units). All warehouses are in "Active" sync state.
- **When:** Three events occur simultaneously within a 1-second window: (1) W1 processes a goods issue of 50 units. (2) W3 processes a goods receipt of 20 units. (3) W4 processes a goods issue of 100 units. All events are pushed via WebSocket.
- **Then:** Each affected warehouse cell updates independently with the correct new value. No event is lost. Events are processed in correct timestamp order. Stock totals reflect: W1: 270, W2: 44, W3: 115, W4: 110. All three updates arrive within the 5-minute P95 sync latency requirement. The dashboard renders each updated cell without visual artifacts (no overlapping updates, no flash conflicts).
```

---

> **Example Product B:** HelpDesk Pro — Customer Feedback Submission Module
>
> The following example demonstrates Given/When/Then acceptance criteria for a customer-facing feedback submission form, covering the primary user flow, required field validation, and attachment format validation.

---

```markdown
## 5. Acceptance Criteria (Continued)

> **How to Read This Chapter:** Each section corresponds to a requirement (REQ-###) from Chapter 3. Acceptance criteria are written in Given/When/Then format. Each criterion is independently executable and objectively verifiable. QA Engineers should be able to use these criteria directly as test case specifications without additional clarification.

---

### 5.5 Feedback Form Submission — Normal Flow (REQ-FB-001)

**Feature Module:** Feedback Submission
**Priority:** P0
**Total Acceptance Criteria:** 3 criteria (1 primary flow, 1 validation flow, 1 attachment validation flow)

---

**Acceptance Criterion 1: Normal Submission**

- **Given:** The user is logged in to HelpDesk Pro and is viewing the "Submit Feedback" page. The feedback form has loaded successfully with all fields accessible.
- **When:** The user selects problem type "Function Issue," fills in the description field with "Submit button not clickable on the order confirmation page," uploads 1 screenshot (screenshot_order_issue.jpg, 2.3MB, JPG format), and clicks the "Submit" button.
- **Then:** The system validates all fields within 500ms. The form is submitted successfully. The system displays a success message: "✅ Submission Successful — Your feedback ID is FB-2026-00001. Our team will review it within 24 hours." A feedback record is created in the database with the submitted data. The popup auto-closes after 3 seconds and the user is returned to the previous page.

---

**Acceptance Criterion 2: Required Field Validation — Missing Problem Type**

- **Given:** The user opens the feedback form. The description field is empty and no problem type is selected.
- **When:** The user clicks the "Submit" button without selecting a problem type.
- **Then:** The system does not submit the form. An inline validation error appears below the problem type field: "⚠️ Please select a problem type." The error message is displayed in red text with an warning icon. The submit button remains in its enabled state. The form is not cleared — all user input (description text, uploaded files) is preserved. No network request to the submission endpoint is made.

---

**Acceptance Criterion 3: Attachment Format Validation — Unsupported File Type and Oversized File**

- **Given:** The user clicks the "Upload Screenshot" button on the feedback form. The file picker dialog opens.
- **When:** The user selects a 10MB PDF file (order_confirmation.pdf).
- **Then:** The system validates the file immediately upon selection and rejects the upload. An error message is displayed below the upload area: "⚠️ Only JPG, PNG, GIF formats are supported. Single file maximum: 5MB. Selected file: order_confirmation.pdf (10MB)." The file is not uploaded to the server. The upload area remains empty (or shows only previously valid uploads). No partial upload is initiated. The file picker dialog closes.

---

### 5.6 Feedback Form Submission — Additional Flows (REQ-FB-001 / REQ-FB-002)

**Feature Module:** Feedback Submission
**Priority:** P0 / P1

---

**Acceptance Criterion 4: Multiple Attachment Upload — All Valid Files**

- **Given:** The user is filling out the feedback form. The user has selected a valid problem type and entered a description.
- **When:** The user uploads 3 files: screenshot_1.jpg (1.2MB), screenshot_2.png (800KB), error_log.gif (200KB). The user then clicks "Submit."
- **Then:** All three files are uploaded successfully. The success message confirms the submission with a count: "3 attachments received." Each file thumbnail is displayed in the upload area with the filename and file size. The submission is processed with all attachments linked to the feedback record.

---

**Acceptance Criterion 5: Submission with Empty Description — Rejected**

- **Given:** The user opens the feedback form and selects problem type "Function Issue."
- **When:** The user clicks "Submit" without entering any description text.
- **Then:** The system does not submit the form. An inline validation error appears below the description field: "⚠️ Please describe the issue before submitting." The problem type selection is preserved. No submission record is created.

---

**Acceptance Criterion 6: Admin Views Feedback with Attachments**

- **Given:** A customer has submitted feedback FB-2026-00001 with 1 screenshot attached. A customer service agent is logged into the Admin Portal.
- **When:** The agent navigates to the Feedback List, locates FB-2026-00001, and opens the feedback detail view.
- **Then:** The agent can view the full feedback details: submitter name, problem type, description text, submission timestamp, and the attached screenshot. The agent can download the screenshot. The agent can update the feedback status (e.g., "In Review," "Resolved").
```

---

## 6. Technical Constraints

### Chapter Purpose

The Technical Constraints chapter documents the project's non-functional boundaries — the constraints within which the engineering team must design and build. This chapter surfaces constraints early, enabling the team to make informed tradeoffs from day one and serving as an early warning system for risks that could derail the project.

This chapter covers:
1. **Technology Stack Constraints** — mandatory frameworks, languages, and infrastructure choices
2. **Integration Dependencies** — external systems, their owners, and delivery timelines
3. **Security and Compliance Requirements** — authentication, data protection, regulatory requirements
4. **Performance Boundaries** — hard limits on latency, throughput, and data volume
5. **Compatibility and Accessibility Scope** — browsers, devices, internationalization, and accessibility standards

---

### Filling Guide

#### 6.1 Technology Stack Constraints

**What to write here:** Specify mandatory and preferred technology choices for each component. Be explicit about what is **required** (non-negotiable) versus **preferred** (can be changed if engineering provides a compelling reason).

**What to include for each component:**
- **Component name:** e.g., Frontend Framework, Backend Runtime, Database, Cache, File Storage
- **Required / Preferred:** Distinguish between mandatory constraints and preferred-but-negotiable choices
- **Version requirement:** Specific version numbers or minimum versions
- **Rationale:** Why this constraint exists

**Common mistakes to avoid:**
- Listing constraints that are actually implementation decisions.
- Being too vague: "React" is a constraint; "modern JavaScript frameworks" is not actionable.
- Conflating preferred stacks with required ones.

---

#### 6.2 Integration Dependencies

**What to write here:** List every external system that this product depends on. For each dependency, specify: what it provides, who owns it, what the interface contract looks like, and when it will be available.

**For each dependency, include:**
- **Dependent System:** Name and owner team
- **Interface Type:** REST API, GraphQL, message queue, webhook, SDK, etc.
- **Data Flow Direction:** Is this product a producer, a consumer, or both?
- **Contract:** What data is exchanged? What is the SLA?
- **Delivery Date:** When will this integration be ready for consumption?
- **Risk:** What is the risk if this dependency is delayed? (High/Medium/Low)

---

#### 6.3 Security and Compliance Requirements

**What to write here:** Document the security requirements that the architecture and implementation must satisfy.

**Key areas to cover:**
- **Authentication and Authorization:** How users prove their identity and what they are permitted to do
- **Data Protection:** Encryption in transit and at rest, PII handling, data retention policies
- **Audit and Logging:** What events must be logged, for how long, and in what format
- **Compliance:** Any regulatory requirements (GDPR, CCPA, SOC 2, HIPAA, PCI-DSS) that apply

---

### Template Body

```markdown
## 6. Technical Constraints

### 6.1 Technology Stack Constraints

| Component | Constraint Type | Requirement | Rationale | Notes |
|-----------|----------------|-------------|-----------|-------|
| [e.g., Frontend Framework] | **Required** | [React 18+ with TypeScript] | [Aligns with existing frontend tech stack; team has expertise] | [Optional notes] |
| [e.g., Backend Runtime] | **Preferred** | [Node.js 18+ or Python 3.11+] | [Team expertise; existing microservices pattern] | [Can be changed with Eng Lead approval] |
| [e.g., Database] | **Required** | [PostgreSQL 14+ or MySQL 8.0+] | [Existing database infrastructure] | [Use existing RDS instance] |
| [e.g., Cache Layer] | **Preferred** | [Redis 6+ for session and analytics data caching] | [Existing Redis cluster available] | [Optional — Eng Lead may propose alternatives] |
| [e.g., File Storage] | **Required** | [S3-compatible object storage for uploaded files] | [Reuse existing storage infrastructure] | [Files must not be served from the application server] |
| [e.g., CDN] | **Required** | [Cloudflare (existing contract)] | [Existing enterprise contract] | [All static assets must be served via CDN] |

---

### 6.2 Integration Dependencies

| Dependent System | Interface Type | Owner | Delivery Date | Data Flow | Risk if Delayed | Contract / SLA |
|-----------------|----------------|-------|---------------|-----------|----------------|----------------|
| [System name] | REST API (internal) | [Team / Contact] | [YYYY-MM-DD] | Producer → Product | **High** | [API endpoint, auth, rate limit] |
| [System name] | Salesforce REST API | [Team / Contact] | [YYYY-MM-DD] | Product → Salesforce | **Medium** | [OAuth 2.0 connected app] |
| [System name] | Internal Message Queue | [Backend Team / Contact] | [YYYY-MM-DD] | Product → Notification Service | **Medium** | [Message schema, queue name] |
| [System name] | API Pull / Data Export | [Data Team / Contact] | [YYYY-MM-DD] | Product → Analytics Platform | **Low** | [Export frequency, data format] |

---

### 6.3 Security and Compliance Requirements

#### 6.3.1 Authentication and Authorization

| Requirement | Specification | Notes |
|-------------|--------------|-------|
| [e.g., User Authentication] | [OAuth 2.0 with PKCE; JWT tokens with 1-hour expiry; refresh token rotation] | [SwiftStock's existing auth infrastructure — no new auth system required] |
| [e.g., API Authentication] | [API keys for system-to-system integrations; stored in AWS Secrets Manager] | [API key rotation every 90 days] |
| [e.g., Role-Based Access Control] | [RBAC enforced at API layer — no client-side enforcement accepted] | [RBAC matrix in Appendix 7.5] |

#### 6.3.2 Data Protection

| Requirement | Specification | Notes |
|-------------|--------------|-------|
| [e.g., Encryption in Transit] | All API traffic and WebSocket connections over TLS 1.2 or higher | TLS 1.0 and TLS 1.1 must be explicitly rejected |
| [e.g., Encryption at Rest] | All PII, financial data, and API keys encrypted at rest (AES-256) | AWS RDS encryption with KMS-managed keys |
| [e.g., PII Handling] | User email addresses, names, and account data must not appear in application logs | Log redaction implemented in logging middleware |
| [e.g., Data Retention] | Inventory transaction data retained for [X] years; alert history retained for [X] years | [Legal/Compliance to confirm] |

#### 6.3.3 Audit and Logging

| Requirement | Specification | Notes |
|-------------|--------------|-------|
| [e.g., Write Operation Audit Logs] | All create/update/delete operations logged with user ID, timestamp, action, before/after state, IP address | Logs stored in CloudWatch Logs; 90-day hot storage; 2-year archive in S3 Glacier |
| [e.g., Access Logs] | All API calls logged with requester identity, endpoint, response code, and latency | Used for security monitoring and debugging |

#### 6.3.4 Compliance

| Requirement | Specification | Notes |
|-------------|--------------|-------|
| [e.g., SOC 2 Type II] | Infrastructure is SOC 2 Type II certified (last audit: [date]) | No additional compliance work required; verify with Security team |
| [e.g., GDPR (EU sellers)] | For EU-based sellers, PII must be handled per GDPR Article 28 requirements. DPA must be in place. | Legal to confirm if DPA is required |

---

### 6.4 Performance Boundaries

| Metric | Target | Stress Limit (Failure Threshold) | Measurement Method | Notes |
|--------|--------|----------------------------------|-------------------|-------|
| [e.g., API Response Time (Read — P99)] | < 500ms | > 2 seconds triggers automatic scaling | Measured at API gateway | |
| [e.g., WebSocket Message Latency (P95)] | < 5 minutes from event to dashboard render | > 10 minutes triggers PagerDuty alert | WebSocket trace timestamps in Datadog | |
| [e.g., Max Concurrent WebSocket Connections] | 1,000 per seller account; 10,000 platform-wide | Auto-scaling at 70% of limit | Load test via k6 | |
| [e.g., Database Write Throughput] | Support 500 inventory update writes per second (platform-wide) | > 800 writes/second degrades to > 1 second P99 | Load test with synthetic inventory events | |

---

### 6.5 Compatibility Requirements

| Dimension | Requirement | Notes |
|-----------|-------------|-------|
| **Browser Support** | Chrome 90+, Firefox 90+, Safari 14+, Edge 90+ | Excludes Internet Explorer 11 |
| **Mobile OS Support** | iOS 14+ (iPhone and iPad); Android 10+ | Tested on latest stable OS version quarterly |
| **Responsive Breakpoints** | Desktop (≥ 1024px), Tablet (768–1023px), Mobile (< 768px) | Critical pages must be fully functional on all breakpoints |
| **Internationalization** | English (en-US) and Simplified Chinese (zh-CN) in this release | All user-facing strings externalized in i18n resource files |
| **Accessibility** | WCAG 2.1 AA compliance for all user-facing web interfaces | Excludes: third-party embedded content (Salesforce side panel) |
```

---

### Example Content

> **Example Product:** SwiftStock — Multi-Warehouse Inventory Sync Module (continued)

---

```markdown
## 6. Technical Constraints

### 6.1 Technology Stack Constraints

| Component | Constraint Type | Requirement | Rationale | Notes |
|-----------|----------------|-------------|-----------|-------|
| **Frontend Framework (Web)** | **Required** | React 18+ with TypeScript (strict mode) | Aligns with existing SwiftStock frontend tech stack; team has established expertise | No JavaScript files permitted; all components must be TypeScript |
| **Mobile Framework** | **Required** | Swift (iOS 14+); Kotlin (Android 10+) | Native frameworks required for real-time WebSocket support and push notifications | React Native was evaluated and rejected due to WebSocket library immaturity in RN |
| **Backend Runtime** | **Required** | Node.js 18+ (Express or Fastify) | Aligns with existing SwiftStock backend services; team expertise | No Python or Java backends for net-new services without Eng Lead approval |
| **Database** | **Required** | PostgreSQL 14+ (AWS RDS) | Aligns with existing SwiftStock data infrastructure; ACID compliance required for inventory transactions | Use existing RDS instance; new tables in existing `inventory` schema |
| **Cache Layer** | **Preferred** | Redis 6+ (ElastiCache) | Existing Redis cluster available for session caching and real-time analytics data | Optional for Sprint 1 if Eng Lead proposes a viable alternative |
| **Real-Time Messaging** | **Required** | WebSocket (ws library) over TLS for real-time dashboard updates | Core architectural requirement for the 5-minute sync latency target | Server-sent events (SSE) is not acceptable as a replacement |
| **Object Storage** | **Required** | AWS S3 (existing bucket) | Reuse existing SwiftStock S3 bucket for any uploaded files (images, exports) | Files must not be served from the application server |
| **CDN** | **Required** | Cloudflare (existing enterprise contract) | Existing DDoS protection and edge caching infrastructure | All static assets served via Cloudflare CDN; no direct S3 public access |
| **Monitoring and Observability** | **Required** | Datadog (APM, RUM, Synthetics) | Existing SwiftStock monitoring infrastructure | All services must emit structured JSON logs to Datadog |
| **Alerting** | **Required** | PagerDuty (existing contract) | Integration with existing on-call rotation | All critical metric breaches must route to PagerDuty |

---

### 6.2 Integration Dependencies

| Dependent System | Interface Type | Owner | Delivery Date | Data Flow | Risk if Delayed | Contract / SLA |
|-----------------|----------------|-------|---------------|-----------|----------------|----------------|
| **NetSuite ERP (Inventory Source)** | REST API (internal, OAuth 2.0) | NetSuite Admin Team — James Park | 2026-04-15 | NetSuite → SwiftStock (inventory data ingestion) | **High** — Without this, we cannot test the sync engine with real seller data in UAT | NetSuite REST API v2.0; rate limit: 1,000 requests/minute per account; auth via OAuth 2.0 client credentials |
| **Salesforce CRM (Account Manager Integration)** | Salesforce REST API + AppExchange | Sales Engineering — Priya Mehta | 2026-05-01 (Phase 1 GA) | SwiftStock → Salesforce (inventory availability, read-only) | **Medium** — Phase 1 ships without Salesforce integration if delayed | Salesforce Connected App with OAuth 2.0; scoped to `inventory:read` and `activity:write` |
| **In-App Notification Service** | Internal Pub/Sub (AWS SNS/SQS) | Backend Platform Team — Anika Singh | 2026-04-01 | SwiftStock → SNS → Email/Push providers | **Medium** — In-app notifications are the primary alert delivery channel | Message schema: `{ event_type, user_id, payload, timestamp }`; dead-letter queue after 3 retries |
| **Gainsight (Customer Success Dashboard)** | Gainsight REST API (v2) | CS Platform Team — David Okafor | 2026-05-15 | SwiftStock → Gainsight (account health events, alert adoption data) | **Low** — CS dashboard is internal tooling; can be back-filled post-launch | Gainsight API with OAuth 2.0; max 100 API calls/minute; event schema TBD with Gainsight team |
| **Data Analytics Platform (Looker)** | Looker Embedded SDK + API | Data Engineering — Maria Santos | 2026-04-20 | SwiftStock → Looker (aggregated metrics for executive dashboard) | **Low** — Dashboard can use direct database queries during initial launch | Looker API v3.0; embedded lookml dashboard |

---

### 6.3 Security and Compliance Requirements

#### 6.3.1 Authentication and Authorization

| Requirement | Specification | Notes |
|-------------|--------------|-------|
| **User Authentication** | OAuth 2.0 with PKCE for all user-facing API calls; JWT tokens with 1-hour expiry; automatic refresh token rotation | SwiftStock's existing auth infrastructure — no new auth system required |
| **API Authentication (System-to-System)** | API keys for NetSuite and Salesforce integrations; stored in AWS Secrets Manager; never in code, config files, or environment variables | API key rotation every 90 days; automatic rotation supported via Secrets Manager |
| **Role-Based Access Control (RBAC)** | RBAC enforced at the API layer — no client-side enforcement accepted as the sole authorization mechanism | RBAC matrix defined in Appendix 7.5. Permissions: Viewer (read-only), Manager (create transfers, manage alerts), Admin (all permissions including user management) |
| **Warehouse-Level Permissions** | Users must have explicit permission on each warehouse to view or manage it. A user with Admin role on Warehouse 1 cannot automatically access Warehouse 2 unless granted. | Enforced at the API gateway and in each service's authorization layer |

#### 6.3.2 Data Protection

| Requirement | Specification | Notes |
|-------------|--------------|-------|
| **Encryption in Transit** | All API traffic and WebSocket connections over TLS 1.2 or higher | TLS 1.0 and TLS 1.1 must be explicitly rejected at the ALB |
| **Encryption at Rest** | All PII (user email, name, IP addresses), financial data, and API keys encrypted at rest using AES-256 | AWS RDS encryption with KMS-managed keys; key rotation every 90 days |
| **PII Handling in Logs** | User email addresses, names, and account data must not appear in application logs or error messages | Log redaction implemented as middleware in all services; PII fields defined in a central redaction config file that is version-controlled |
| **Data Residency** | All data for EU-based sellers must be stored in AWS EU (Frankfurt) region (eu-central-1) | Legal to confirm data residency requirements for each seller jurisdiction before launch |
| **Data Retention — Inventory Transactions** | Inventory transaction records (stock changes, transfers, adjustments) retained for 7 years | Compliance requirement for financial audit trail; enforced via AWS S3 Glacier lifecycle policies |
| **Data Retention — Alert History** | Alert records (triggered, acknowledged, resolved) retained for 2 years | After 2 years, records are anonymized (user ID removed) and retained for aggregate analytics |
| **Data Retention — Audit Logs** | Write-operation audit logs retained for 2 years in S3 Glacier | Per SOC 2 Type II requirements |

#### 6.3.3 Audit and Logging

| Requirement | Specification | Notes |
|-------------|--------------|-------|
| **Write Operation Audit Logs** | All create/update/delete operations on inventory, transfers, alert rules, and user permissions must be logged with: user ID (or system if automated), timestamp (UTC), action type, before/after state (for updates), IP address, request ID | Logs stored in CloudWatch Logs; 90-day hot storage; 2-year archive in S3 Glacier; immutability enabled on the log group |
| **Access Logs** | All API calls (read and write) logged with: requester identity, endpoint, HTTP method, response code, latency (ms), request ID | Used for security monitoring, debugging, and SLA verification |
| **WebSocket Event Logs** | All WebSocket connect/disconnect events and message delivery events logged with: connection ID, user ID, warehouse IDs in view, message delivery latency | Used for monitoring sync engine health and diagnosing delivery failures |

#### 6.3.4 Compliance

| Requirement | Specification | Notes |
|-------------|--------------|-------|
| **SOC 2 Type II** | SwiftStock's infrastructure and application controls are SOC 2 Type II certified | Last audit: 2026-01-15; no additional compliance work required for this release. Verify with Security team before launch. |
| **GDPR (EU Sellers)** | For sellers based in the European Union, all PII must be handled per GDPR Article 28 requirements. A Data Processing Agreement (DPA) must be executed before EU seller data is processed. | Legal team to confirm. If DPA is required, it must be executed before enabling the Multi-Warehouse feature for EU-based sellers. |
| **CCPA (California Sellers)** | For sellers based in California, the product must support data access and deletion requests per CCPA requirements. | SwiftStock's existing data subject request (DSR) process covers this; verify with Legal that the new data stores are included in the existing DSR workflow. |

---

### 6.4 Performance Boundaries

| Metric | Target | Stress Limit (Failure Threshold) | Measurement Method | Notes |
|--------|--------|----------------------------------|-------------------|-------|
| **API Response Time (Read — P99)** | < 500ms under < 500 concurrent API requests | > 2 seconds triggers automatic scaling; > 5 seconds triggers incident | Measured at API gateway; 30-day rolling average | |
| **API Response Time (Write — Transfer APIs)** | P99 < 1 second under normal load | > 5 seconds triggers incident | Measured at API gateway | |
| **WebSocket Message Latency (P95)** | < 5 minutes from source warehouse event to dashboard render for 95% of events | > 8 minutes triggers PagerDuty alert to on-call engineer | WebSocket trace: `event.timestamp` (at source) → `push.ack.timestamp` (at client) in Datadog | Measured end-to-end including any queueing delay |
| **Dashboard Initial Load Time (P95)** | < 2.5 seconds for initial load with up to 20 warehouses and 500 visible SKUs | > 4 seconds triggers performance review | Synthetic monitoring via Datadog Synthetic Tests; measured at CDN edge | |
| **SKU Detail Drawer Open Time (P95)** | < 800ms from click to drawer fully rendered | > 1.5 seconds triggers performance review | Real User Monitoring via Datadog RUM SDK | Mobile app: < 1.5 seconds |
| **Max Concurrent WebSocket Connections** | 1,000 per seller account; 10,000 platform-wide | Auto-scaling at 70% of limit; at 90% a capacity expansion is triggered | Load test via k6 with WebSocket simulation; reviewed monthly | |
| **Database Write Throughput** | Support 500 inventory update writes per second (platform-wide) | > 800 writes/second degrades to > 1 second P99 on write APIs | Load test with synthetic inventory event stream | |
| **Alert Delivery Latency (P95)** | < 30 seconds from alert trigger to alert received on user's device (in-app, email, or push) | > 2 minutes triggers Slack alert to Engineering Lead | Mixpanel: `alert_rule_triggered` → delivery receipt timestamp | |
| **Transfer API Error Rate** | < 0.5% of transfer API calls (create/confirm/cancel) return HTTP 4xx or 5xx | > 1% triggers PagerDuty alert | Datadog API monitor on transfer API endpoints | |
| **Sync Error Rate** | < 0.1% of daily sync events result in a data error (validation failure, schema mismatch, missed event) | > 0.05% triggers Slack alert to Engineering Lead | Datadog: `sync.events.total` vs `sync.events.error` | |

---

### 6.5 Compatibility Requirements

| Dimension | Requirement | Notes |
|-----------|-------------|-------|
| **Browser Support** | Chrome 90+, Firefox 90+, Safari 14+, Edge 90+ | Excludes Internet Explorer 11 entirely; no IE11 polyfills required |
| **Mobile OS Support** | iOS 14+ (iPhone and iPad); Android 10+ (API level 29+) | Tested on latest stable OS version quarterly; minimum tested resolution: 375×667 (iPhone SE) |
| **Mobile App Architecture** | Native iOS (Swift 5.9+) and Android (Kotlin 1.9+) — not web-wrapped | Push notification support (APNs for iOS; FCM for Android) is a hard requirement |
| **Responsive Breakpoints** | Desktop (≥ 1024px): full multi-warehouse table; Tablet (768–1023px): horizontal scroll on table; Mobile (< 768px): single-warehouse view with warehouse picker | Critical pages (Multi-Warehouse Dashboard, Transfer Center, My Alerts) must be fully functional at all breakpoints |
| **Internationalization** | English (en-US) — this release; Simplified Chinese (zh-CN) — Q3 2026 | All user-facing strings externalized in i18n resource files (react-intl for web; NSLocalizedString for iOS); no hardcoded strings in UI components |
| **Accessibility** | WCAG 2.1 Level AA compliance for all user-facing web and mobile interfaces | Excludes: third-party embedded content (Salesforce side panel), internal-only admin tools |
| **Keyboard Navigation** | All interactive elements reachable and operable via keyboard alone; visible focus indicators on all focusable elements | Automated testing via axe-core in CI pipeline; manual testing on every major release |
| **Screen Reader** | All UI text has semantic meaning and is readable by NVDA (Windows) and VoiceOver (macOS/iOS) | Primary user flows tested quarterly with accessibility consultant |
```

---

## 7. Appendix

### Chapter Purpose

The Appendix provides supplementary reference material that supports the rest of the PRD without being central to the product requirements themselves. It ensures the PRD is self-contained — any reader can find the definition of any term, trace the evolution of any decision, and access all supporting materials without leaving the document.

The Appendix contains four key sections:
1. **Glossary** — standardized definitions of professional terminology used in the project
2. **Document Version History** — a record of changes to this document with author and date for traceability
3. **Reference Documents** — links to all supporting materials (design files, API specs, research reports, competitive analysis)
4. **Contacts and Stakeholders** — key decision-makers and their responsibilities for this project

---

### Filling Guide

#### 7.1 Glossary

**What to write here:** Define every specialized term, acronym, and domain-specific phrase used in the PRD that may not be immediately clear to all readers. A glossary is especially important in B2B products where domain-specific terminology varies between the product team, engineering, and customers.

**Good glossary entries:**
- **Term (as used in this document):** Precise definition. If the term has multiple meanings, specify which meaning applies in this document.
- **Not just definitions of obvious things.** Include terms that are specific to this product, this industry, or this implementation.
- **Cross-reference related terms.** If two terms are related or easily confused, note the distinction.

**Common mistakes to avoid:**
- Defining only obvious acronyms (HTTP, API) while omitting product-specific terms.
- Writing definitions that are circular.
- Including terms that are not actually used in the PRD.

---

#### 7.2 Document Version History

**What to write here:** Record every significant change to this PRD document — initial draft, major revisions, stakeholder feedback incorporated, scope changes, and formal approvals.

**What to include for each version:**
- Version number (v0.1, v0.2, v1.0, etc.)
- Date of the change
- Author (the person who made the change)
- A brief description of what changed and why

---

#### 7.3 Reference Documents

**What to write here:** List all supporting documents, design files, technical specifications, and external resources referenced in the PRD or used to inform the product decisions. Include the document name, its location or link, and a one-sentence description of what it contains and why it is relevant.

---

#### 7.4 Contacts and Stakeholders

**What to write here:** List the key individuals involved in this project — their role, name, contact information, and area of responsibility.

---

### Template Body

```markdown
## 7. Appendix

### 7.1 Glossary

| Term | Definition | Notes / Context |
|------|------------|----------------|
| [Term 1] | [Precise definition. If multiple meanings exist, specify which applies in this document.] | [Related terms: Term X, Term Y] |
| [Term 2] | [Definition] | [Related terms] |
| [Acronym 1] | [Expanded form: Full definition] | |

---

### 7.2 Document Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| v0.1 | [YYYY-MM-DD] | [Name] | Initial draft; Project Overview and User Analysis completed |
| v0.2 | [YYYY-MM-DD] | [Name] | Added Requirements chapter (P0/P1 features); updated Goals based on stakeholder input |
| v0.3 | [YYYY-MM-DD] | [Name] | Added Success Metrics, Acceptance Criteria, and Technical Constraints chapters |
| v0.9 | [YYYY-MM-DD] | [Name] | Full document submitted for engineering and design review |
| v1.0 | [YYYY-MM-DD] | [Name] | Approved; baseline version frozen. Scope locked for Sprint 1. |

---

### 7.3 Reference Documents

| Document Name | Link / Location | Description | Owner |
|--------------|-----------------|-------------|-------|
| [Design spec — e.g., Multi-Warehouse Dashboard Figma] | [Link or file path] | [Contains all page layouts, component designs, and interaction specifications for the Multi-Warehouse Dashboard and Transfer Center] | [Design Lead] |
| [API Documentation — Inventory Sync API] | [Link or Confluence URL] | [Contains request/response formats, authentication, rate limits, and error codes for all inventory sync endpoints] | [Tech Lead] |
| [Competitive Analysis — Multi-Warehouse IMS Features] | [Internal Wiki path] | [Analysis of how competitors handle multi-warehouse inventory visibility and alerting] | [PM] |
| [User Research — Warehouse Manager Pain Points] | [Internal Wiki path] | [Summary of 12 user interviews conducted in January 2026 with operations managers at SMB retailers] | [UX Research Lead] |
| [Technical Architecture — Real-Time Sync Engine] | [Link or Confluence URL] | [System architecture document describing the WebSocket push architecture, event ordering guarantees, and fallback behavior] | [Eng Lead] |
| [Data Tracking Specification — Multi-Warehouse Module] | [Internal Wiki path] | [Complete event taxonomy, parameter definitions, and data collection requirements for the launch dashboard] | [PM + Data Analyst] |

---

### 7.4 Contacts and Stakeholders

| Role | Name | Contact | Responsibilities |
|------|------|---------|-----------------|
| Product Owner | [Name] | [Email] | Requirements final authority; scope decisions; priority arbitration |
| Product Manager | [Name] | [Email] | Day-to-day PRD ownership; requirements clarification; stakeholder communication |
| Engineering Lead | [Name] | [Email] | Technical design and architecture; technical risk management; sprint planning |
| Design Lead | [Name] | [Email] | UI/UX design; interaction specifications; design system compliance |
| QA Lead | [Name] | [Email] | Test planning and test case design; acceptance criteria verification |
| Customer Success Lead | [Name] | [Email] | Customer onboarding flow; adoption monitoring; CS tooling requirements |
| Data / Analytics Lead | [Name] | [Email] | Data tracking implementation; metrics instrumentation; dashboard setup |
| Security Review | [Name] | [Email] | Security architecture review; penetration testing coordination |
| Legal / Compliance | [Name] | [Email] | GDPR/CCPA compliance; DPA execution; data residency confirmation |
| On-Call Engineer (Launch Window) | [Name] | [Email / Pagerduty] | Incident response during launch window (Weeks 1–4 post-launch) |

---

### 7.5 RBAC Matrix (Role-Based Access Control)

| Permission | Viewer | Manager | Admin | Notes |
|------------|--------|---------|-------|-------|
| View inventory levels (all warehouses) | ✓ (own accounts only) | ✓ (assigned warehouses) | ✓ (all warehouses) | |
| View alert rules | ✓ | ✓ | ✓ | |
| Create / edit / delete alert rules | ✗ | ✓ (own rules) | ✓ (all rules) | |
| View transfer history | ✓ | ✓ | ✓ | |
| Create transfer request | ✗ | ✓ | ✓ | |
| Confirm transfer receipt | ✗ | ✓ (destination warehouse) | ✓ (all warehouses) | |
| Cancel transfer | ✗ | ✗ | ✓ (own initiated transfers) | |
| Manage warehouse connections | ✗ | ✗ | ✓ | |
| Manage users and permissions | ✗ | ✗ | ✓ | |
| View audit logs | ✗ | ✗ | ✓ | |
| Export data | ✗ | ✓ (own account data) | ✓ (all data) | Export file retention: 30 days |
```

---

### Example Content

> **Example Product:** SwiftStock — Multi-Warehouse Inventory Sync Module (continued)

---

```markdown
## 7. Appendix

### 7.1 Glossary

| Term | Definition | Notes / Context |
|------|------------|----------------|
| **ATP (Available to Promise)** | The quantity of inventory that is physically on-hand and not reserved for pending orders. ATP = On-Hand Quantity − Reserved Quantity. Used throughout SwiftStock to indicate how much of a SKU can be allocated to new orders. ATP is the number displayed in the Multi-Warehouse Dashboard. | See also: Available to Promise |
| **Available to Promise (ATP)** | See ATP. | |
| **Stockout** | A condition in which a warehouse's on-hand quantity for a given SKU is zero or insufficient to fulfill a pending or new order. A stockout is the primary problem this product aims to prevent. | Not to be confused with "low stock" (below threshold but > 0) |
| **Stockout Cancellation** | An order that was confirmed by the system (and thus promised to the customer) but was subsequently partially or fully cancelled because the warehouse could not fulfill the items due to a stockout that existed at the time of order confirmation. This is the North Star metric. | Not to be confused with cancellations due to customer request, payment failure, or other non-inventory reasons |
| **Multi-Warehouse Dashboard** | The primary UI surface for the Multi-Warehouse Inventory Sync module. Displays a table of SKUs with one column per warehouse, showing ATP quantity per warehouse per SKU. Replaces the previous single-warehouse view. | |
| **WebSocket Push** | A persistent, bidirectional network connection between the SwiftStock web/mobile client and the backend, used to deliver real-time inventory update events without the client needing to poll. Core architectural mechanism for achieving the 5-minute sync latency target. | Contrast with: polling (client repeatedly requests data at intervals); batch sync (data updated nightly) |
| **Warehouse Connection** | The integration between SwiftStock and a seller's physical warehouse management system (e.g., NetSuite, Cin7, proprietary ERP). A warehouse connection can be in one of three states: Active (syncing normally), Error (sync failing), or Disconnected (manually disabled or network unreachable). | A seller may have multiple warehouse connections, one per physical warehouse |
| **Low-Stock Alert Rule** | A user-defined rule that specifies a threshold quantity for a specific SKU in a specific warehouse. When the ATP for that SKU in that warehouse falls below the threshold, an alert is triggered. Rules can be scoped to: a specific SKU in a specific warehouse, a SKU category in a specific warehouse, or a SKU across all warehouses. | The most specific rule wins when multiple rules apply to the same SKU/warehouse combination |
| **P0 / P1 / P2 (MoSCoW Priority)** | Priority classifications used in this PRD: P0 = Must Have (core functionality, must ship); P1 = Should Have (important but not fatal if deferred); P2 = Could Have (nice to have, ship if time permits). | These priorities apply to functional requirements only, not to NFRs or acceptance criteria |
| **MoSCoW Prioritization** | A requirements prioritization technique used to categorize requirements as Must Have, Should Have, Could Have, and Won't Have (this release). Helps teams focus delivery on the highest-impact features. | |
| **Transfer Request** | The first step in the cross-warehouse transfer workflow. A transfer request reserves inventory in the Source warehouse and notifies the Destination warehouse. Status: "In Transit." | Contrast with: Transfer Confirmation (second step, at Destination warehouse) |
| **Transfer Confirmation** | The second step in the cross-warehouse transfer workflow. Confirms that goods have been physically received at the Destination warehouse, incrementing the Destination's inventory. Status: "Completed." | Only the Destination warehouse's Manager or Admin can confirm receipt |
| **RPO (Recovery Point Objective)** | The maximum acceptable amount of data loss measured in time. For example, an RPO of 5 minutes means the system must lose no more than 5 minutes' worth of data during a disaster. | |
| **RTO (Recovery Time Objective)** | The maximum acceptable time to recover from a failure. For example, an RTO of 15 minutes means the system must be fully restored within 15 minutes of a failure occurring. | |
| **P95 / P99 Latency** | The 95th or 99th percentile of response time measurements. P95 = 500ms means 95% of requests are faster than 500ms. Used instead of averages because average latency can be skewed by outlier slow requests. | |
| **Given/When/Then (GWT)** | A structured format for writing acceptance criteria originating from Behavior-Driven Development (BDD). Given = preconditions