---
name: receipt-snap
description: >
  Process receipt photos and PDFs, extract vendor date amount currency, convert to EUR,
  upload to Google Drive with proper naming Vendor_Date_EURAmount.pdf, and log to a Google Sheet.
  Use when user sends a receipt with #recibo or processes expense receipts for tax reporting.
  Handles: PDF invoices, photo screenshots, USD to EUR conversion, Spanish expense categories,
  quarterly reporting for tax purposes.
---

# Receipt Snap Skill

Process receipts for tax reporting. Handles receipt capture, currency conversion, Drive storage, and logging to Google Sheets.

## Requirements

**Binaries:**
- `gog` CLI — install via `brew install faradayhq/gog/gog`, then authenticate with `gog auth login`

**Environment variables** (set in shell, `.env` file, or launchd plist):
- `RECEIPT_DRIVE_FOLDER_ID` — Google Drive folder ID to upload receipts
- `RECEIPT_GOOGLE_SHEET_ID` — Google Sheet ID to append log rows
- `RECEIPT_LOG_FILE` (optional) — local CSV backup path, default: `~/receipts/log.csv`

**Google account:** The `gog` CLI must be authenticated with a Google account that has read/write access to the Drive folder and Sheet ID above.

## Model Usage

**Cost optimization:** Prefer cheaper models for simple text extraction:
1. **Local model** — free, use for text-based PDFs
2. **MiniMax** — default fallback, good for image receipts
3. Only escalate to Sonnet/Opus if genuinely ambiguous

## Prerequisites

1. Install the `gog` CLI: `brew install faradayhq/gog/gog`
2. Authenticate: `gog auth login`
3. Create a Google Drive folder and a Google Sheet with a "log" tab
4. Copy `.env.example` to `.env` and fill in your IDs:

```bash
cp .env.example .env
# Edit .env with your values:
# RECEIPT_DRIVE_FOLDER_ID="1abc123XYZ..."
# RECEIPT_GOOGLE_SHEET_ID="1abc123XYZ..."
```

**Security:** Never commit `.env` to version control — it contains credentials. The `.gitignore` file excludes it by default.

## Workflow

### 1. Receive Receipt
User sends receipt via Telegram with `#recibo` tag. Accepts:
- PDF invoices
- Photo screenshots of receipts
- Text descriptions (`#recibo Description: ...`)

### 2. Extract Data
Extract from receipt:
- **Vendor** (company name)
- **Date** (invoice date)
- **Amount** (total including VAT)
- **Currency** (EUR, USD, etc.)
- **Description** (what was purchased)

### 2.5 Check for Duplicates
Before processing, check if this receipt already exists:

```bash
gog sheets get "$RECEIPT_GOOGLE_SHEET_ID" "log!A:J" --json
```
Search for matching vendor + date + amount. If duplicate found → warn user and ask before proceeding.

### 3. Currency Conversion
If non-EUR:
- Fetch rate from `https://open.er-api.com/v6/latest/{currency}`
- Convert to EUR
- Log both original and EUR amounts

### 4. Categorize
Spanish tax categories:

- **Software y suscripciones** — SaaS, API credits, subscriptions
- **Telecomunicaciones** — phone, voicemail
- **Combustibles** — fuel, gas
- **Viajes y desplazamientos** — travel, mileage
- **Manutención y restauración** — meals (business)
- **Material informáticos** — hardware
- **Formación** — courses, education
- **Otros gastos** — other

### 5. Upload to Google Drive

```bash
gog drive upload <file> --parent "$RECEIPT_DRIVE_FOLDER_ID"
gog drive rename <file-id> "VendorName_2026-01-15_42.50EUR.pdf"
```

### 6. Log to Google Sheet

```bash
gog sheets append "$RECEIPT_GOOGLE_SHEET_ID" "log!A:J" \
  --values-json '[["2026-01-15","Vendor Name","Description","42.50","EUR","42.50","1.0","Software y suscripciones","https://drive.google.com/...","Notes"]]' \
  --insert INSERT_ROWS
```

### 7. Quarterly Report
At quarter-end:
- Generate category summary: `python3 receipt_snap.py summary`
- Zip receipt images from Drive
- Send summary + ZIP to your tax accountant

## Commands

### Process receipt
```bash
python3 receipt_snap.py process receipt.pdf \
  --vendor "Vendor Name" \
  --date 2026-01-15 \
  --amount 42.50 \
  --currency EUR \
  --category "Software y suscripciones"
```

### Summary
```bash
python3 receipt_snap.py summary
```

### Exchange rate
```bash
python3 receipt_snap.py exchange-rate
```

## Sheet Setup

Create a Google Sheet with a tab named `log`. Add this header row (A through J):

| Date | Vendor | Description | Original Amount | Currency | EUR Amount | Exchange Rate | Category | Drive Link | Notes |

## PDF Extraction

Use the `pdf` tool for automatic extraction from PDF invoices:

```
pdf <path-to-invoice.pdf>
```

Parse output for vendor, date, amount, currency.

## Security

- Add `receipts/` and `*.csv` to `.gitignore` — contains real financial data
- Never hardcode IDs in source files — use the `.env` file
- `gog` manages OAuth tokens locally — verify your Google account is secure
- Files uploaded to Drive and rows appended to Sheets leave copies on Google services
