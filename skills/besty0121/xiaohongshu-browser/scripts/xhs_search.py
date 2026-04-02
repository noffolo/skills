# -*- coding: utf-8 -*-
"""XHS Search - Click posts and screenshot the modal preview."""
import sys, json, time, urllib.parse, re
from pathlib import Path
from playwright.sync_api import sync_playwright

SKILL_DIR = Path(__file__).resolve().parent.parent
HOME = Path.home()
OPENCLAW = HOME / ".openclaw"

OUT = SKILL_DIR / "output"
OUT.mkdir(exist_ok=True)
USER_DATA = str(OPENCLAW / "xhs_data")
XHS = "https://www.xiaohongshu.com"

def ts(): return str(int(time.time()))

keyword = sys.argv[1] if len(sys.argv) > 1 else "御姐"
count = int(sys.argv[2]) if len(sys.argv) > 2 else 5

with sync_playwright() as pw:
    browser = pw.chromium.launch_persistent_context(
        USER_DATA, headless=True,
        viewport={"width": 1280, "height": 900}, locale="zh-CN",
    )
    page = browser.pages[0] if browser.pages else browser.new_page()

    kw = urllib.parse.quote(keyword)
    search_url = f"{XHS}/search_result?keyword={kw}&source=web_search_result_notes&type=51"
    print(f"[*] Searching: {keyword}", flush=True)
    page.goto(search_url, wait_until="domcontentloaded", timeout=60000)
    time.sleep(5)

    # Dismiss login/overlay popups
    page.keyboard.press("Escape")
    time.sleep(1)

    print(f"[*] URL: {page.url}", flush=True)

    covers = page.query_selector_all("section.note-item a.cover")
    if not covers:
        covers = page.query_selector_all("a.cover")
    print(f"[*] Found {len(covers)} posts", flush=True)

    results = []
    clicked = 0
    for i, cover in enumerate(covers):
        if clicked >= count:
            break
        try:
            cover.scroll_into_view_if_needed()
            time.sleep(0.5)

            href = cover.get_attribute("href") or ""
            note_id = ""
            m = re.search(r'/search_result/([a-f0-9]+)', href)
            if m:
                note_id = m.group(1)

            cover.click()
            time.sleep(5)

            # Dismiss overlay popups
            for popup_sel in [".close-button", ".login-close", "[class*='close']"]:
                try:
                    btn = page.query_selector(popup_sel)
                    if btn and btn.is_visible():
                        btn.click()
                        time.sleep(0.5)
                except:
                    pass

            clicked += 1
            p = OUT / f"post_{clicked}_{ts()}.png"
            page.screenshot(path=str(p))
            post_url = f"{XHS}/explore/{note_id}" if note_id else ""
            print(f"[+] Post {clicked}: {p}", flush=True)
            print(f"    URL: {post_url}", flush=True)
            results.append({"index": clicked, "url": post_url, "screenshot": str(p)})

            page.keyboard.press("Escape")
            time.sleep(2)

        except Exception as e:
            print(f"[!] Error: {e}", flush=True)
            page.keyboard.press("Escape")
            time.sleep(1)

    browser.close()

print("\n=== RESULTS ===")
print(json.dumps(results, ensure_ascii=False, indent=2))
