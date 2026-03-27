#!/usr/bin/env python3
"""
visual_ref.py — Search and download reference images from Unsplash.

Usage:
    python3 visual_ref.py "luxury real estate nordic" --count 5 --output /tmp/refs/
    python3 visual_ref.py "product photo minimalist" --count 3
"""

import argparse
import os
import sys
import json
import urllib.request
import urllib.parse
import urllib.error
from pathlib import Path

UNSPLASH_ACCESS_KEY = os.environ.get("UNSPLASH_ACCESS_KEY", "")


def search_photos(query: str, count: int = 5, orientation: str = None) -> list[dict]:
    """Search photos on Unsplash and return a list of results."""
    import random
    params = {
        "query": query,
        "per_page": count,
        "page": random.randint(1, 5),
    }
    if orientation:
        params["orientation"] = orientation  # landscape | portrait | squarish

    url = "https://api.unsplash.com/search/photos?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={
        "Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}",
        "Accept-Version": "v1",
    })

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
            return data.get("results", [])
    except urllib.error.HTTPError as e:
        print(f"Error: Unsplash API returned {e.code} {e.reason}", file=sys.stderr)
        sys.exit(1)


def download_photo(photo: dict, output_dir: Path, index: int) -> Path:
    """Download a photo at regular resolution (~1080px) and trigger the download event."""
    # Trigger download (required by Unsplash guidelines)
    dl_url = photo["links"]["download_location"]
    req = urllib.request.Request(dl_url, headers={
        "Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}",
        "Accept-Version": "v1",
    })
    try:
        urllib.request.urlopen(req, timeout=10)
    except Exception:
        pass  # Don't block if the ping fails

    # Actual download URL (regular = ~1080px, full = original)
    img_url = photo["urls"]["regular"]
    photo_id = photo["id"]
    author = photo["user"]["username"]
    ext = "jpg"
    filename = output_dir / f"ref_{index:02d}_{photo_id}.{ext}"

    req2 = urllib.request.Request(img_url, headers={"User-Agent": "visual-ref-skill/1.0"})
    with urllib.request.urlopen(req2, timeout=30) as resp:
        filename.write_bytes(resp.read())

    return filename, author


def main():
    parser = argparse.ArgumentParser(description="Download visual references from Unsplash")
    parser.add_argument("query", help='Search query, e.g. "luxury real estate minimalist"')
    parser.add_argument("--count", type=int, default=5, help="Number of images (default: 5)")
    parser.add_argument("--output", default="/tmp/visual-refs", help="Output folder")
    parser.add_argument("--orientation", choices=["landscape", "portrait", "squarish"], help="Orientation (optional)")
    parser.add_argument("--list-only", action="store_true", help="List URLs only, no download")
    args = parser.parse_args()

    if not UNSPLASH_ACCESS_KEY:
        print("Error: UNSPLASH_ACCESS_KEY not found in environment.", file=sys.stderr)
        print("  Set it with: export UNSPLASH_ACCESS_KEY=your_access_key", file=sys.stderr)
        sys.exit(1)

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    import random
    print(f'Searching "{args.query}" on Unsplash ({args.count} images)...')
    photos = search_photos(args.query, args.count, args.orientation)
    random.shuffle(photos)

    if not photos:
        print("No results found.", file=sys.stderr)
        sys.exit(0)

    results = []
    for i, photo in enumerate(photos, 1):
        desc = photo.get("description") or photo.get("alt_description") or "No description"
        author = photo["user"]["name"]

        if args.list_only:
            print(f"  [{i}] {desc[:60]} — {author}")
            print(f"       {photo['urls']['regular']}")
            results.append({"index": i, "description": desc, "author": author, "url": photo["urls"]["regular"]})
        else:
            print(f"  [{i}/{len(photos)}] Downloading: {desc[:50]}...")
            try:
                path, username = download_photo(photo, output_dir, i)
                print(f"       OK: {path.name}  (Photo by {author} / @{username})")
                results.append({"index": i, "file": str(path), "description": desc, "author": author})
            except Exception as e:
                print(f"       Error: {e}")

    if not args.list_only:
        print(f"\n{len(results)} references saved to: {output_dir}")
        print("\nAttribution (required by Unsplash guidelines):")
        for r in results:
            print(f"   Photo by {r.get('author', '?')} on Unsplash")

    # JSON output for programmatic use
    json_path = output_dir / "refs_meta.json"
    json_path.write_text(json.dumps(results, ensure_ascii=False, indent=2))
    print(f"\nMetadata: {json_path}")


if __name__ == "__main__":
    main()
