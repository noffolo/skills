# csv-data-extractor

Transform, clean, and analyze CSV data using natural language commands. Upload a CSV file and describe what you want to do with it.

## Usage

```
Analyze this CSV and summarize [file]
Extract [specific data] from [file]
Filter rows where [condition] and export [file]
Join [file1] and [file2] on [column]
Convert this data to [format: JSON/Excel/HTML table]
```

## What It Does

- **Data profiling** — row count, column types, null values, unique counts, value distributions
- **Filtering** — select rows matching conditions (e.g., "where status = 'active' and amount > 1000")
- **Column operations** — rename, reorder, drop, split, merge, type cast
- **Aggregations** — GROUP BY with SUM, AVG, COUNT, MIN, MAX, pivot tables
- **Joins** — LEFT/RIGHT/INNER join on specified columns
- **Transformations** — date parsing, string operations, currency formatting, unit conversions
- **Export** — output to CSV, JSON, Excel (.xlsx), HTML table, or Markdown

## Input

A CSV file path or paste CSV content directly in the conversation.

## Examples

- "Show me the top 10 customers by revenue from this sales data"
- "Filter out all rows where email is blank, then export only name/email/phone"
- "Add a column called 'full_name' that combines first_name and last_name"
- "Group by department and show average salary per department"
- "Convert this data to JSON with nested objects by category"

## Notes

- Handles large files (100k+ rows) by processing in chunks
- Auto-detects delimiter (comma, tab, semicolon, pipe)
- Detects date formats automatically
- Preserves original file; always exports to new file
- Encodings supported: UTF-8, Latin-1, Windows-1252
