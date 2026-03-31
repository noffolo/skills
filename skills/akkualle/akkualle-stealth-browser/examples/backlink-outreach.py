"""
Beispiel: Backlink-Outreach Automation
Zeigt wie man Foren-Profile automatisch mit Backlinks erstellt
"""

import sys
sys.path.append("/root/.openclaw/skills/stealth-browser")

from stealth_browser import StealthBrowser

# ============================================================
# KONFIGURATION
# ============================================================

WEBSITE = "https://akku-alle.de"
ANCHOR_TEXT = "E-Scooter kaufen"

FORUMS = [
    {
        "name": "Gutefrage.net",
        "url": "https://www.gutefrage.net",
        "register": "https://www.gutefrage.net/registrieren",
        "profile": "https://www.gutefrage.net/profil"
    },
    {
        "name": "Pedelec-Forum",
        "url": "https://www.pedelec-forum.de",
        "register": "https://www.pedelec-forum.de/register",
        "profile": "https://www.pedelec-forum.de/members"
    }
]

# ============================================================
# MAIN
# ============================================================

def main():
    browser = StealthBrowser()
    
    print("=" * 60)
    print("  Backlink-Outreach Automation")
    print("=" * 60)
    print()
    
    for forum in FORUMS:
        print(f"\n📍 Bearbeite: {forum['name']}")
        print("-" * 60)
        
        # 1. Forum öffnen
        print("1. Öffne Registrierungsseite...")
        browser.open(forum['register'], headless=False)
        
        # 2. Manuelle Registrierung
        print("2. Bitte registrieren Sie sich manuell...")
        print("   Drücken Sie ENTER wenn fertig.")
        input()
        
        # 3. Profil bearbeiten
        print("3. Öffne Profilseite...")
        browser.open(forum['profile'], headless=False)
        
        print("4. Fügen Sie Ihre Website hinzu:")
        print(f"   URL: {WEBSITE}")
        print(f"   Linktext: {ANCHOR_TEXT}")
        print("   Drücken Sie ENTER wenn fertig.")
        input()
        
        # 4. Session speichern
        browser._save_cookies(forum['name'].lower().replace('-', '_'))
        print(f"✅ Session gespeichert: {forum['name']}")
    
    print()
    print("=" * 60)
    print("  ✅ Backlink-Outreach abgeschlossen!")
    print("=" * 60)
    
    browser.close()

if __name__ == "__main__":
    main()
