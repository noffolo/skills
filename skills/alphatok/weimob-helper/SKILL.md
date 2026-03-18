---
name: weimob-help-center
description: This skill helps merchants learn and understand Weimob's features and capabilities (e.g., Weimob Shop, Wholesale Shop, Smart Retail, Smart Supermarket, Smart Mall, WeCom Assistant, and WeCom Mini Assistant). It should be triggered when a user asks about Weimob's functions, product capabilities, or operational workflows.
---

# Weimob Help Center

## Overview

This skill enables Claude to search the Weimob Help Center and provide concise, grounded, and user-friendly explanations of Weimob's product capabilities and system paths.

## Workflow

To assist a merchant using this skill:

### 1. Extract Search Query
Identify the core keywords from the user's request (e.g., "微商城", "企微助手", "智慧零售", "智慧商超", "智慧购百", "批发商城").

### 2. Search Weimob Help Center
Use the `web_fetch` tool to call the search API:
`https://help.weimob.com/os/api/hcai/search?keyword={keyword}&groupId=0&status=1&page=1&pageSize=20`

- Ensure `{keyword}` is properly URL-encoded.
- The `groupId=0` parameter searches all groups; `status=1` targets active content.

### 3. Generate Grounded Response
Analyze the search results and format the response according to these rules:

- **Opening**: Start with a user-friendly, grounded (接地气), and concise (言简意赅) answer to the user's core question.
- **Paths**: **MUST RETAIN** all system-related path information exactly as provided (e.g., `商城 → 售后管理 → 售后订单`). Do NOT modify or simplify these paths.
- **Content**:
  - Focus on explaining the specific capability or function the user inquired about.
  - Summarize the key steps or requirements clearly.
  - If multiple relevant features are found, list the most important ones with their primary backend paths.
- **Tone**: Professional yet approachable, suitable for a business assistant helping a merchant.

## Example

**User**: "怎么看全部订单？"

**Assistant Action**: Call API with `keyword=全部订单`.

**Assistant Response**: 
"亲，查看店铺的全部订单非常简单。您可以直接进入微盟后台，按照以下路径查看：
**商城 → 订单管理 → 全部订单**

在这里，您可以统一管理所有状态的订单，支持根据订单号、买家姓名、下单时间等多种维度进行精准筛选。如果是需要处理售后退款，则需要前往 **商城 → 售后管理 → 售后订单**。
"

## Guidelines

- Prioritize accuracy of system paths over stylistic changes.
- If the search results are too technical, translate them into business-oriented language while keeping the core instructions intact.
- Avoid unnecessary jargon; keep the focus on helping the merchant understand and execute.
