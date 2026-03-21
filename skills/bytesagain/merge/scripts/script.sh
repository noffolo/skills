#!/usr/bin/env bash
# merge — File merge tool
# Powered by BytesAgain | bytesagain.com | hello@bytesagain.com
set -euo pipefail
VERSION="3.0.1"

BOLD='\033[1m'; GREEN='\033[0;32m'; RED='\033[0;31m'; RESET='\033[0m'
die() { echo -e "${RED}Error: $1${RESET}" >&2; exit 1; }
info() { echo -e "${GREEN}✓${RESET} $1"; }

cmd_files() {
    local f1="${1:?Usage: merge files <file1> <file2> [output]}"
    local f2="${2:?Missing second file}"
    local out="${3:-merged-output.txt}"
    [ ! -f "$f1" ] && die "Not found: $f1"
    [ ! -f "$f2" ] && die "Not found: $f2"
    cat "$f1" "$f2" > "$out"
    local lines
    lines=$(wc -l < "$out")
    info "Merged to $out ($lines lines)"
}

cmd_lines() {
    local f1="${1:?Usage: merge lines <file1> <file2>}"
    local f2="${2:?Missing second file}"
    [ ! -f "$f1" ] && die "Not found: $f1"
    [ ! -f "$f2" ] && die "Not found: $f2"
    paste -d '\n' "$f1" "$f2" | grep -v '^$'
}

cmd_csv() {
    local f1="${1:?Usage: merge csv <file1.csv> <file2.csv> <key-col>}"
    local f2="${2:?Missing second CSV}"
    local key="${3:?Missing key column number}"
    [ ! -f "$f1" ] && die "Not found: $f1"
    [ ! -f "$f2" ] && die "Not found: $f2"
    COL="$key" F1="$f1" F2="$f2" python3 << 'PYEOF'
import csv, os
col = int(os.environ["COL"]) - 1
rows = {}
with open(os.environ["F1"]) as f:
    reader = csv.reader(f)
    header1 = next(reader)
    for row in reader:
        if col < len(row):
            rows[row[col]] = row
with open(os.environ["F2"]) as f:
    reader = csv.reader(f)
    header2 = next(reader)
    for row in reader:
        if col < len(row):
            key = row[col]
            if key in rows:
                merged = rows[key] + [c for i,c in enumerate(row) if i != col]
                rows[key] = merged
            else:
                rows[key] = row
merged_header = header1 + [h for i,h in enumerate(header2) if i != col]
print(",".join(merged_header))
for key in sorted(rows):
    print(",".join(str(c) for c in rows[key]))
PYEOF
}

cmd_json() {
    local f1="${1:?Usage: merge json <file1.json> <file2.json>}"
    local f2="${2:?Missing second JSON file}"
    [ ! -f "$f1" ] && die "Not found: $f1"
    [ ! -f "$f2" ] && die "Not found: $f2"
    F1="$f1" F2="$f2" python3 << 'PYEOF'
import json, os
with open(os.environ["F1"]) as f:
    d1 = json.load(f)
with open(os.environ["F2"]) as f:
    d2 = json.load(f)
if isinstance(d1, list) and isinstance(d2, list):
    result = d1 + d2
elif isinstance(d1, dict) and isinstance(d2, dict):
    result = {**d1, **d2}
else:
    result = [d1, d2]
print(json.dumps(result, indent=2))
PYEOF
}

cmd_dedup() {
    local file="${1:?Usage: merge dedup <file>}"
    [ ! -f "$file" ] && die "Not found: $file"
    local before after
    before=$(wc -l < "$file")
    awk '!seen[$0]++' "$file"
    after=$(awk '!seen[$0]++' "$file" | wc -l)
    echo "" >&2
    echo "  Removed $((before - after)) duplicates (${before} → ${after} lines)" >&2
}

cmd_diff() {
    local f1="${1:?Usage: merge diff <file1> <file2>}"
    local f2="${2:?Missing second file}"
    [ ! -f "$f1" ] && die "Not found: $f1"
    [ ! -f "$f2" ] && die "Not found: $f2"
    echo -e "${BOLD}Diff: $f1 vs $f2${RESET}"
    diff --color=auto "$f1" "$f2" || true
}

cmd_common() {
    local f1="${1:?Usage: merge common <file1> <file2>}"
    local f2="${2:?Missing second file}"
    [ ! -f "$f1" ] && die "Not found: $f1"
    [ ! -f "$f2" ] && die "Not found: $f2"
    comm -12 <(sort "$f1") <(sort "$f2")
}

cmd_unique() {
    local f1="${1:?Usage: merge unique <file1> <file2>}"
    local f2="${2:?Missing second file}"
    [ ! -f "$f1" ] && die "Not found: $f1"
    [ ! -f "$f2" ] && die "Not found: $f2"
    echo -e "${BOLD}Only in $f1:${RESET}"
    comm -23 <(sort "$f1") <(sort "$f2")
    echo ""
    echo -e "${BOLD}Only in $f2:${RESET}"
    comm -13 <(sort "$f1") <(sort "$f2")
}

cmd_patch() {
    local file="${1:?Usage: merge patch <file> <patchfile>}"
    local patchfile="${2:?Missing patch file}"
    [ ! -f "$file" ] && die "Not found: $file"
    [ ! -f "$patchfile" ] && die "Not found: $patchfile"
    patch "$file" "$patchfile"
    info "Patched $file"
}

show_help() {
    cat << EOF
merge v$VERSION — File merge tool

Usage: merge <command> [args]

Merge:
  files <f1> <f2> [output]     Concatenate two files
  lines <f1> <f2>              Interleave lines from two files
  csv <f1> <f2> <key-col>      Join two CSVs on a key column
  json <f1> <f2>               Merge two JSON files (arrays or objects)

Compare:
  diff <f1> <f2>               Show differences between files
  common <f1> <f2>             Show lines common to both files
  unique <f1> <f2>             Show lines unique to each file

Transform:
  dedup <file>                 Remove duplicate lines (preserving order)
  patch <file> <patchfile>     Apply a patch file

  help                         Show this help
  version                      Show version

Requires: diff, comm, sort, paste, patch, python3 (for csv/json)
EOF
}

[ $# -eq 0 ] && { show_help; exit 0; }
case "$1" in
    files)   shift; cmd_files "$@" ;;
    lines)   shift; cmd_lines "$@" ;;
    csv)     shift; cmd_csv "$@" ;;
    json)    shift; cmd_json "$@" ;;
    dedup)   shift; cmd_dedup "$@" ;;
    diff)    shift; cmd_diff "$@" ;;
    common)  shift; cmd_common "$@" ;;
    unique)  shift; cmd_unique "$@" ;;
    patch)   shift; cmd_patch "$@" ;;
    help|-h) show_help ;;
    version|-v) echo "merge v$VERSION"; echo "Powered by BytesAgain | bytesagain.com | hello@bytesagain.com" ;;
    *)       echo "Unknown: $1"; show_help; exit 1 ;;
esac
