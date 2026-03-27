---
name: aioz-stream-toolkit
description: Respond to user requests for AIOZ Stream API. Use provided scripts to upload videos, fetch analytics, manage media, and create livestreams.
metadata:
  openclaw:
    emoji: "🎥"
    requires:
      bins:
        - curl
        - jq
        - md5sum
---

# AIOZ Stream Operations

Interact with AIOZ Stream API quickly with API key authentication. A suite of integrated bash scripts are provided to automatically call the REST APIs.

## When to use this skill

- User wants to upload or create a video on AIOZ Stream
- User mentions "upload video", "create video", "aioz stream video"
- User wants to query view analytics, live streams, or account balances
- User wants to get an HLS/MP4 streaming link for their video

## Authentication

This skill uses API key authentication. The user must provide:

- `stream-public-key`: their AIOZ Stream public key
- `stream-secret-key`: their AIOZ Stream secret key

Ask the user for these keys if not provided. They will be passed as parameters to all scripts in the `scripts/` folder.

## Usage Options (Available Scripts)

When the user asks for a feature, use one of the bash scripts located in the `scripts/` directory.

### Script Routing Map (for Clawbot)

- Upload local file to video: `./scripts/upload_video_file.sh PUBLIC_KEY SECRET_KEY FILE_PATH "TITLE"`
- Get media list (GET with optional query params): `./scripts/get_media_list.sh PUBLIC_KEY SECRET_KEY [SEARCH] [PAGE]`
- Get media list via POST body (search/page): `./scripts/get_total_media.sh PUBLIC_KEY SECRET_KEY [SEARCH] [PAGE]`
- Get all media via POST `{}`: `./scripts/get_video_list.sh PUBLIC_KEY SECRET_KEY`
- Search media by name via POST body: `./scripts/get_video_url_by_name.sh PUBLIC_KEY SECRET_KEY "VIDEO_NAME"`
- Create livestream key: `./scripts/create_livestream_key.sh PUBLIC_KEY SECRET_KEY "KEY_NAME"`
- Get account/user info and balance: `./scripts/get_balance.sh PUBLIC_KEY SECRET_KEY`
- Get usage data (fixed interval=hour): `./scripts/get_usage_data.sh PUBLIC_KEY SECRET_KEY FROM(dd/mm/yyyy) TO(dd/mm/yyyy)`
- Get aggregate analytics (watch_time + view_count): `./scripts/get_aggregate_metric.sh PUBLIC_KEY SECRET_KEY TYPE FROM(dd/mm/yyyy) TO(dd/mm/yyyy)`
- Get breakdown analytics (device/os/country/browser): `./scripts/get_breakdown_metric.sh PUBLIC_KEY SECRET_KEY TYPE FROM(dd/mm/yyyy) TO(dd/mm/yyyy)`
- Combined aggregate + breakdown report: `./scripts/analytic_data.sh PUBLIC_KEY SECRET_KEY TYPE FROM(dd/mm/yyyy) TO(dd/mm/yyyy)`

### 1. Upload Video (Default Flow)

Use this script to automatically create a video object, upload the file, and complete the flow:

```bash
./scripts/upload_video_file.sh PUBLIC_KEY SECRET_KEY "/path/to/video.mp4" "Video Title"
```

Actual behavior in script:

- Accepts local file path only.
- Validates video by extension (and by MIME where possible).
- File must exist on the local system.

### 2. Analytics & Usage

To get metrics or account usage:

- **Usage Data:** `./scripts/get_usage_data.sh PUBLIC_KEY SECRET_KEY FROM(dd/mm/yyyy) TO(dd/mm/yyyy)`
  - Calls `GET /analytics/data?from=...&to=...&interval=hour`
  - `FROM`/`TO` must be `dd/mm/yyyy` format (scripts convert to Unix timestamp)
- **Aggregate Metrics:** `./scripts/get_aggregate_metric.sh PUBLIC_KEY SECRET_KEY TYPE FROM(dd/mm/yyyy) TO(dd/mm/yyyy)`
  - Returns: Watch time sum + View count for selected media type
  - `TYPE` must be `video` or `audio`
- **Breakdown Metrics:** `./scripts/get_breakdown_metric.sh PUBLIC_KEY SECRET_KEY TYPE FROM(dd/mm/yyyy) TO(dd/mm/yyyy)`
  - Returns: Device type, Operating system, Country, Browser breakdowns (with total count and data array)
  - `TYPE` must be `video` or `audio`
- **All-in-one Analytics:** `./scripts/analytic_data.sh PUBLIC_KEY SECRET_KEY TYPE FROM(dd/mm/yyyy) TO(dd/mm/yyyy)`
  - Returns: Combined aggregate metrics + all breakdown metrics in one call
  - `TYPE` must be `video` or `audio`

Date format notes:

- `FROM` and `TO` must be `dd/mm/yyyy` (scripts convert to Unix timestamp internally)

### 3. Media & Livestream Management

To search existing media, get balance, or create keys:

- **List Media:** `./scripts/get_media_list.sh PUBLIC_KEY SECRET_KEY [SEARCH] [PAGE]`
- **Total Media:** `./scripts/get_total_media.sh PUBLIC_KEY SECRET_KEY [SEARCH] [PAGE]`
- **Video List:** `./scripts/get_video_list.sh PUBLIC_KEY SECRET_KEY`
- **Search Video URL:** `./scripts/get_video_url_by_name.sh PUBLIC_KEY SECRET_KEY "Video Name"`
- **Livestream Key:** `./scripts/create_livestream_key.sh PUBLIC_KEY SECRET_KEY "Key Name"`
- **Balance:** `./scripts/get_balance.sh PUBLIC_KEY SECRET_KEY`

Notes:

- `get_video_list.sh` currently returns all media (`POST /media` with empty body), not strictly video-only filtering.
- `get_video_url_by_name.sh` currently returns search results JSON; it does not extract one URL field automatically.

## Full Upload Flow (Script does 5 steps)

For reference, `upload_video_file.sh` does:

1. Create media object
2. Upload media part
3. Complete upload
4. Fetch media detail
5. Print status and URLs (`hls_player_url`, `hls_url`, `mp4_url`)

If doing manual `curl`, the core upload flow is the first 3 steps below.

### Step 1: Create Video Object

```bash
curl -s -X POST 'https://api.aiozstream.network/api/media/create' \
  -H "stream-public-key: PUBLIC_KEY" \
  -H "stream-secret-key: SECRET_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "title": "VIDEO_TITLE",
    "type": "video"
  }'
```

Response: Extract `data.id` — this is the `VIDEO_ID` used in the next steps.

### Step 2: Upload File Part

Upload the actual video file binary to the created video object.
First, get the file size and compute the MD5 hash:

```bash
# Get file size (cross-platform compatible)
FILE_SIZE=$(stat -f%z /path/to/video.mp4 2>/dev/null || stat -c%s /path/to/video.mp4)
END_POS=$((FILE_SIZE - 1))

# Compute MD5 hash
HASH=$(md5sum /path/to/video.mp4 | awk '{print $1}')
```

Then upload via multipart form-data with the Content-Range header:

```bash
curl -s -X POST "https://api.aiozstream.network/api/media/VIDEO_ID/part" \
  -H "stream-public-key: PUBLIC_KEY" \
  -H "stream-secret-key: SECRET_KEY" \
  -H "Content-Range: bytes 0-$END_POS/$FILE_SIZE" \
  -F "file=@/path/to/video.mp4" \
  -F "index=0" \
  -F "hash=$HASH"
```

**Important:** The `Content-Range` header is required for the upload to succeed. Format: `bytes {start}-{end}/{total_size}`.
Form-data fields:

- `file`: the video file binary (use `@/path/to/video.mp4`)
- `index`: 0 (for single-part upload)
- `hash`: MD5 hash of the file part

### Step 3: Complete Upload

After the file part is uploaded, call the complete endpoint to finalize:

```bash
curl -s -X GET "https://api.aiozstream.network/api/media/VIDEO_ID/complete" \
  -H 'accept: application/json' \
  -H "stream-public-key: PUBLIC_KEY" \
  -H "stream-secret-key: SECRET_KEY"
```

This triggers transcoding. The upload is now considered successful.

## After Upload — Get Video Link

After completing the upload, fetch the video detail to get the streaming URL:

```bash
curl -s "https://api.aiozstream.network/api/media/VIDEO_ID" \
  -H "stream-public-key: PUBLIC_KEY" \
  -H "stream-secret-key: SECRET_KEY"
```

Parse the response to find the HLS or MP4 URL from the `assets` field and return it to the user.

## Custom Upload Config Reference

_(Applicable if implementing custom logic via API directly)_

### Quality Presets (`resolution` field):

- `standard` — Standard quality
- `good` — Good quality
- `highest` — Highest quality
- `lossless` — Lossless quality

### Streaming Formats (`type` field):

- `hls` — HTTP Live Streaming (container: `mpegts` or `mp4`)
- `dash` — Dynamic Adaptive Streaming (container: `fmp4`)

## Response Handling

1. Run the appropriate script from the `scripts/` directory.
2. **Media/Search scripts** return raw JSON: `get_video_list`, `get_video_url_by_name`, `get_total_media`, `get_media_list`
3. **Metrics scripts** return structured output:
   - `get_aggregate_metric.sh`: Two labeled outputs (Watch Time Sum, View Count)
   - `get_breakdown_metric.sh`: Four labeled JSON blocks (=== device_type ===, === operator_system ===, === country ===, === browser ===)
   - `analytic_data.sh`: Combined aggregate + breakdown output
   - `get_usage_data.sh`: Raw JSON response with pretty-printed format
4. **Upload/Management scripts**: `upload_video_file.sh` prints step-by-step status with final URLs
5. Return useful fields explicitly (IDs, status, URLs, totals). If upload status is `transcoding` or URLs are empty, inform the user to check again later.

## Error Handling

- **401**: Invalid API keys — ask user to verify their public and secret keys
- **Missing Parameters**: Scripts validate arguments; pass exactly what they require.
- **500**: Server error — suggest retrying

## Example Interaction Flow

1. User: "Upload my video to AIOZ Stream"
2. Ask for API keys (public + secret) if not known
3. Ask for the video file path and title
4. **Step 1:** Execute `./scripts/upload_video_file.sh PUBLIC_KEY SECRET_KEY "FILE_PATH" "TITLE"`
5. Extract the outputted HLS/MP4 link
6. Return the video link to the user
