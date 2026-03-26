---
name: mercadolibre-return-guide
description: "Mercado Libre return management and authorization code agent. Complete returns workflow management for ML sellers — obtain return codes, manage return shipments, handle disputes, minimize return losses, and track return metrics. Triggers: mercado libre returns, mercadolibre return, ml return code, mercado pago refund, latin america ecommerce returns, ml dispute, mercadolibre seller, brazil ecommerce returns, argentina ecommerce, ml return management"
allowed-tools: Bash
metadata:
  openclaw:
    homepage: https://github.com/mguozhen/mercadolibre-return-guide
---

# Mercado Libre Return Manager

Complete returns management for Mercado Libre sellers — from obtaining return codes to managing disputes, tracking return metrics, and minimizing return-related losses across LATAM markets.

## Commands

```
return guide <situation>          # step-by-step return handling guide
return code <order>               # how to obtain return authorization code
return dispute <case>             # handle a return dispute
return policy <market>            # ML return policy by country
return reduce <category>          # strategies to reduce return rate
return metrics <data>             # analyze your return rate data
return response <buyer-message>   # draft response to return request
return tracking <return-id>       # track return shipment status
return report <period>            # return performance report
return warehouse <setup>          # overseas warehouse return setup
```

## What Data to Provide

- **Order details** — order ID, product, purchase date, buyer message
- **Return reason** — buyer's stated reason for return
- **Country** — which ML market (BR, MX, AR, CO, CL, etc.)
- **Return rate data** — current return % by category/product
- **Dispute details** — case ID and timeline

## Mercado Libre Return Framework

### ML Markets Overview

| Market | Language | Return Window | Key Notes |
|--------|----------|---------------|-----------|
| Brazil (BR) | Portuguese | 7 days (CDC law) | Strict consumer rights |
| Mexico (MX) | Spanish | 30 days | ML policy minimum 7 days |
| Argentina (AR) | Spanish | 30 days | Economic volatility affects returns |
| Colombia (CO) | Spanish | 30 days | Growing market |
| Chile (CL) | Spanish | 10 days (SERNAC) | |
| Peru (PE) | Spanish | 7 days | |

### Brazil Return Law (Direito de Arrependimento)

**Article 49 CDC (Consumer Protection Code):**
- Any purchase made outside a physical store can be returned within 7 days
- No justification needed from buyer
- Seller MUST refund full amount including original shipping
- Return shipping: Seller bears cost if buyer exercises cooling-off right

**Practical implications for ML sellers:**
- High return rate is structurally built into Brazilian e-commerce
- Budget 5-10% returns into your Brazilian marketplace pricing
- Fast processing of returns maintains ML reputation score

### Return Authorization Process

**Step 1: Buyer requests return**
- Buyer opens return request through ML system
- Seller receives notification with deadline to respond

**Step 2: Seller review**
- Review within 3 days (or ML mediates automatically)
- Decide: Accept, offer partial refund, or dispute

**Step 3: Obtain return code (for overseas warehouse)**
If using overseas warehouse or 3PL:
```
a. Login to ML seller account
b. Go to: Sales → Active → Find Order
c. Click "View return details"
d. Download or copy the return authorization code
e. Share code with your local warehouse team
f. Warehouse uses code to accept the returned item
```

**Step 4: Inspect returned item**
- Document condition with photos (for dispute protection)
- Acceptable for resale: restock
- Damaged/used: document for partial refund dispute

**Step 5: Process refund**
- Full refund within 48 hours of receiving item
- Partial refund: requires dispute justification with evidence

### Return Dispute Process

**When to dispute:**
- Item returned in different condition than sold (used, damaged)
- Item not returned but buyer claims they sent it
- Return outside the eligible window
- Fraudulent return (different item returned)

**Evidence to gather for disputes:**
```
[ ] Original order photos (product condition when shipped)
[ ] Tracking confirmation of original delivery
[ ] Photos of returned item condition
[ ] Weight discrepancy documentation
[ ] Timeline documentation (dates and responses)
[ ] Any communication with buyer
```

**Dispute submission:**
1. Go to ML Resolution Center
2. Select case → "I disagree with the return"
3. Upload all evidence
4. Write clear, professional case narrative
5. ML mediates within 7-10 business days

### Reducing Return Rate by Category

**Clothing & Fashion (highest return category):**
```
Root causes: Wrong size, color different from photos
Solutions:
- Add accurate size chart with measurements in cm
- True-to-life product photos (no heavy filters)
- Add model measurements (height, weight, size worn)
- Include fabric composition and care instructions
Target return rate: <15%
```

**Electronics:**
```
Root causes: Doesn't work as expected, compatibility issues
Solutions:
- Detailed compatibility list (tested models)
- Clear instruction video
- Technical specs matched to product page
- Verify product works before shipping
Target return rate: <5%
```

**Home & Furniture:**
```
Root causes: Size not as expected, color mismatch
Solutions:
- Accurate dimensions with photo reference
- Color: show in natural light + artificial light
- "Assembly required" clearly stated
- Include all parts visible in listing image
Target return rate: <8%
```

**Toys & Baby:**
```
Root causes: Age-inappropriate, safety concerns
Solutions:
- Clear age range specification
- Material safety info (BPA-free, non-toxic)
- Safety certifications visible
- Accurate scale reference photo
Target return rate: <7%
```

### Return Rate Metrics

Track weekly by category:
```
Metric              Formula                    Target
Return rate         Returns / Delivered        <8%
Dispute win rate    Won disputes / Total        >70%
Refund turnaround   Avg days to refund         <3 days
Cost per return     Return costs / Returns      Minimize
Net return impact   Return value / Revenue      <5%
```

**ML reputation impact:**
- Returns under 8%: Green reputation maintained
- Returns 8-15%: Yellow warning — address immediately
- Returns >15%: Red — seller account at risk

### Return Response Templates

**Accepting legitimate return:**
```
Hola [Nombre del comprador],

Hemos recibido su solicitud de devolución. Confirmamos que
aceptamos la devolución.

Por favor use el código de autorización [CÓDIGO] para enviar
el producto a nuestra dirección:
[Dirección del almacén]

Una vez recibido e inspeccionado el producto, procesaremos
su reembolso completo en 48 horas.

Gracias por su compra.
[Tu nombre/Tienda]
```

**Requesting more information:**
```
Hola [Nombre],

Lamentamos que no esté satisfecho con su compra.

Para procesar su devolución de manera eficiente, ¿podría
por favor enviarnos fotos del producto mostrando el problema?
Esto nos ayudará a resolver su caso más rápidamente.

Estamos comprometidos a encontrar la mejor solución.
[Tu nombre/Tienda]
```

## Workspace

Creates `~/ml-returns/` containing:
- `cases/` — individual return case files
- `disputes/` — dispute evidence and outcomes
- `templates/` — response templates by language
- `metrics/` — return rate tracking
- `reports/` — return performance reports

## Output Format

Every return management output includes:
1. **Return Status** — current situation and deadline
2. **Recommended Action** — accept/dispute/negotiate with reasoning
3. **Response Draft** — ready-to-send message in Spanish/Portuguese
4. **Process Checklist** — step-by-step actions for this case
5. **Evidence List** — what to document and collect
6. **Cost Impact** — financial impact of various resolution options
7. **Prevention Note** — listing change to prevent similar returns
