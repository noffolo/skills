# Create Task Parameters

Common parameters for `create_task.py` and the API, with value reference.

## resolution

- Common values: `720p`, `1080p`
- Required (this skill requires it for predictable output)
- Official docs: if omitted, default is determined by model and duration

## ratio

- Common values: `16:9`, `9:16` (portrait), etc.
- Optional; defaults from API/model when omitted

## duration

- Unit: seconds
- Typically 4–12 seconds; see API and model support for limits

## Other

- `prompt`: Required, max 2000 characters
- `model`: See [models.md](models.md)
- `image_url` / `last_image_url` / `ref_image_urls`: Must be publicly accessible image URLs

Full parameter reference: [Vidau Create Task](https://doc.superaiglobal.com/en/api/create-task.md).
