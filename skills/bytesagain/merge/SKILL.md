---
name: merge
version: "3.0.1"
author: BytesAgain
homepage: https://bytesagain.com
source: https://github.com/bytesagain/ai-skills
license: MIT-0
tags: [merge, file-management, diff, data-processing]
description: "Combine files, resolve conflicts, concatenate data, and deduplicate across sources. Use when merging files, resolving conflicts, deduplicating datasets."
---

# merge

File merge tool.

## Commands

### `files`

Concatenate two files

```bash
scripts/script.sh files <f1> <f2> [output]
```

### `lines`

Interleave lines from two files

```bash
scripts/script.sh lines <f1> <f2>
```

### `csv`

Join two CSVs on a key column

```bash
scripts/script.sh csv <f1> <f2> <key-col>
```

### `json`

Merge two JSON files (arrays or objects)

```bash
scripts/script.sh json <f1> <f2>
```

### `diff`

Show differences between files

```bash
scripts/script.sh diff <f1> <f2>
```

### `common`

Show lines common to both files

```bash
scripts/script.sh common <f1> <f2>
```

### `unique`

Show lines unique to each file

```bash
scripts/script.sh unique <f1> <f2>
```

### `dedup`

Remove duplicate lines (preserving order)

```bash
scripts/script.sh dedup <file>
```

### `patch`

Apply a patch file

```bash
scripts/script.sh patch <file> <patchfile>
```

## Requirements

- python3

---

*Powered by BytesAgain | bytesagain.com | hello@bytesagain.com*
