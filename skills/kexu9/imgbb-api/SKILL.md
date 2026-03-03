---
name: imgbb-api
description: Upload images to ImgBB and get shareable URLs. Use when: (1) User wants to upload images to imgbb, (2) Need to get direct image URLs for sharing, (3) Converting local images to shareable links, (4) Bulk uploading images, (5) Uploading from URL, (6) Base64 encoding.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
      env:
        - IMGBB_API_KEY
    primaryEnv: IMGBB_API_KEY
    emoji: "📸"
    homepage: https://github.com/KeXu9/imgbb-api
---

# ImgBB API

Free image hosting API. Upload images and get shareable URLs.

## Setup

**Option 1: Environment Variable (Recommended)**
```bash
export IMGBB_API_KEY="your_api_key_here"
```

**Option 2: Config File**
Create `~/.imgbb_api_key` file with your API key.

**Option 3: Pass as Parameter**
```bash
python scripts/imgbb.py image.jpg --key YOUR_API_KEY
```

## Get API Key

1. Go to https://api.imgbb.com/
2. Click "Get API Key"
3. Copy your API key

## Upload Methods

### 1. Local File
```bash
curl -s -X POST "https://api.imgbb.com/1/upload?key=YOUR_KEY" -F "image=@/path/to/image.jpg"
```

### 2. From URL
```bash
curl -s -X POST "https://api.imgbb.com/1/upload?key=YOUR_KEY" -F "image=https://example.com/image.jpg"
```

### 3. Base64
```bash
curl -s -X POST "https://api.imgbb.com/1/upload?key=YOUR_KEY" -F "image=base64_data"
```

### 4. With Expiration (60-15552000 sec)
```bash
curl -s -X POST "https://api.imgbb.com/1/upload?key=YOUR_KEY&expiration=3600" -F "image=@image.jpg"
```

## Script Usage

```bash
# Upload file (uses IMGBB_API_KEY env or ~/.imgbb_api_key)
python scripts/imgbb.py /path/to/image.jpg

# With custom API key
python scripts/imgbb.py /path/to/image.jpg --key YOUR_KEY

# With name
python scripts/imgbb.py image.jpg --name custom_name

# With expiration
python scripts/imgbb.py image.jpg --expiration 3600

# From URL
python scripts/imgbb.py --url "https://..."

# JSON output
python scripts/imgbb.py image.jpg --json

# Batch upload
python scripts/imgbb.py --batch /folder/
```

## Response Fields

| Field | Description |
|-------|-------------|
| `url` | Direct image URL |
| `url_viewer` | Viewer page |
| `thumb.url` | Thumbnail |
| `delete_url` | Delete link |
| `width` | Width |
| `height` | Height |
| `size` | Size (bytes) |

## Priority

API key is read in this order:
1. `--key` parameter (highest)
2. `IMGBB_API_KEY` environment variable
3. `~/.imgbb_api_key` config file

## Dependencies

- Python 3
- `requests` library (`pip install requests`)
