"""Push an image URL to the canvas.

SECURITY MANIFEST:
- Environment variables accessed: CANVAS_SERVER
- External endpoints called: http://localhost:*/api/canvas/sync/gen_image (local canvas only)
- Local files read: none
- Local files written: none
"""
import argparse
import json
import os
import urllib.request
import uuid

CANVAS_SERVER = os.environ.get("CANVAS_SERVER", "http://localhost:39301")


def push_to_canvas(image_url: str, element_id: str | None = None) -> str:
    if not element_id:
        element_id = f"gen_{uuid.uuid4().hex[:12]}"
    payload = json.dumps({"url": image_url, "element_id": element_id}).encode("utf-8")
    req = urllib.request.Request(
        f"{CANVAS_SERVER}/api/canvas/sync/gen_image",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        resp.read()
    return element_id


def main():
    parser = argparse.ArgumentParser(description="Push an image URL to the canvas")
    parser.add_argument("--url", required=True, help="Image URL to push")
    parser.add_argument("--id", default=None, help="Optional element id")
    args = parser.parse_args()

    element_id = push_to_canvas(args.url, args.id)
    print(json.dumps({"status": "ok", "url": args.url, "element_id": element_id}))


if __name__ == "__main__":
    main()
