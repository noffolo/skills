---
name: decode
version: "3.0.1"
author: BytesAgain
homepage: https://bytesagain.com
source: https://github.com/bytesagain/ai-skills
license: MIT-0
tags: [decode, tool, utility]
description: "Decode base64, URLs, JWTs, and encoded formats into readable text. Use when decoding base64, parsing JWT tokens, inspecting encoded payloads."
---

# decode

Encoder/decoder tool.

## Commands

### `base64-encode`

Encode to base64

```bash
scripts/script.sh base64-encode <text|file>
```

### `base64-decode`

Decode from base64

```bash
scripts/script.sh base64-decode <encoded>
```

### `url-encode`

URL-encode text

```bash
scripts/script.sh url-encode <text>
```

### `url-decode`

URL-decode text

```bash
scripts/script.sh url-decode <encoded>
```

### `hex-encode`

Convert to hex

```bash
scripts/script.sh hex-encode <text>
```

### `hex-decode`

Convert from hex

```bash
scripts/script.sh hex-decode <hex>
```

### `html-encode`

HTML entity encode

```bash
scripts/script.sh html-encode <text>
```

### `html-decode`

HTML entity decode

```bash
scripts/script.sh html-decode <encoded>
```

### `jwt-decode`

Decode JWT token (header + payload + timestamps)

```bash
scripts/script.sh jwt-decode <token>
```

### `rot13`

ROT13 cipher

```bash
scripts/script.sh rot13 <text>
```

### `binary`

Show binary representation

```bash
scripts/script.sh binary <text>
```

### `detect`

Auto-detect encoding and decode

```bash
scripts/script.sh detect <text>
```

## Requirements

- python3

---

*Powered by BytesAgain | bytesagain.com | hello@bytesagain.com*
