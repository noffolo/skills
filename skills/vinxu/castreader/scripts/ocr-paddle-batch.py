#!/usr/bin/env python3
"""
PaddleOCR Batch — cross-platform OCR fallback (Windows/Linux/Mac)
Usage: python ocr-paddle-batch.py <dir_with_pngs>
Processes all page-*.png files in order, outputs JSON array of texts to stdout.
Progress is printed to stderr (same interface as ocr-vision-batch).

First run will download models (~30MB). Requires:
  pip install paddlepaddle paddleocr
"""

import sys
import os
import json
import time
import glob

def main():
    if len(sys.argv) < 2:
        print("Usage: ocr-paddle-batch <directory>", file=sys.stderr)
        sys.exit(1)

    dir_path = sys.argv[1]
    page_files = sorted(glob.glob(os.path.join(dir_path, "page-*.png")))

    if not page_files:
        print(f"Error: No page-*.png files found in {dir_path}", file=sys.stderr)
        sys.exit(1)

    # Import paddleocr (lazy — so missing dependency gives clear error)
    try:
        from paddleocr import PaddleOCR
    except ImportError:
        print("Error: paddleocr not installed. Run: pip install paddlepaddle paddleocr", file=sys.stderr)
        sys.exit(1)

    print(f"Processing {len(page_files)} pages...", file=sys.stderr)
    start = time.time()

    # Initialize OCR engine once (reuse across pages)
    # use_angle_cls=True for rotated text, lang covers both en+ch
    ocr = PaddleOCR(use_angle_cls=False, lang='en', show_log=False)

    results = []
    for i, fpath in enumerate(page_files):
        try:
            result = ocr.ocr(fpath, cls=False)
            # result is list of pages, each page is list of [bbox, (text, confidence)]
            if result and result[0]:
                # Sort by vertical position (top to bottom), then left to right
                lines = []
                for line in result[0]:
                    bbox = line[0]  # [[x1,y1],[x2,y2],[x3,y3],[x4,y4]]
                    text = line[1][0]
                    y_center = (bbox[0][1] + bbox[2][1]) / 2
                    x_center = (bbox[0][0] + bbox[2][0]) / 2
                    lines.append((y_center, x_center, text))
                # Sort top-to-bottom, then left-to-right
                lines.sort(key=lambda l: (l[0], l[1]))
                page_text = "\n".join(l[2] for l in lines)
            else:
                page_text = ""
        except Exception as e:
            print(f"  Warning: OCR failed for {os.path.basename(fpath)}: {e}", file=sys.stderr)
            page_text = ""

        results.append(page_text)

        if (i + 1) % 50 == 0:
            print(f"  {i + 1}/{len(page_files)} pages", file=sys.stderr)

    elapsed = time.time() - start
    ms_per_page = elapsed / len(page_files) * 1000 if page_files else 0
    print(f"Done: {len(page_files)} pages in {elapsed:.1f}s ({ms_per_page:.0f}ms/page)", file=sys.stderr)

    # Output JSON array to stdout (same format as ocr-vision-batch)
    print(json.dumps(results, ensure_ascii=False))

if __name__ == "__main__":
    main()
