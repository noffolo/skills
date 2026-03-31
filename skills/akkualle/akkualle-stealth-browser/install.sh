#!/bin/bash
# Stealth-Browser Skill Installation
# Version: 1.0.0

set -e

echo "================================================"
echo "  Stealth-Browser Skill v1.0.0 Installation"
echo "================================================"
echo ""

# Prüfe Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 ist erforderlich"
    exit 1
fi

echo "✅ Python gefunden: $(python3 --version)"

# Prüfe Chrome
if command -v google-chrome &> /dev/null; then
    echo "✅ Google Chrome gefunden"
elif command -v chromium-browser &> /dev/null; then
    echo "✅ Chromium gefunden"
else
    echo "⚠️  Chrome/Chromium nicht gefunden"
    echo "   Bitte installieren: apt install google-chrome-stable"
fi

# Installiere Python-Abhängigkeiten
echo ""
echo "📦 Installiere Python-Abhängigkeiten..."

pip3 install undetected-chromedriver selenium websocket-client --quiet 2>/dev/null || {
    echo "⚠️  pip3 fehlgeschlagen, versuche pip..."
    pip install undetected-chromedriver selenium websocket-client --quiet
}

echo "✅ Python-Abhängigkeiten installiert"

# Erstelle Verzeichnisse
echo ""
echo "📁 Erstelle Verzeichnisse..."

mkdir -p /root/.openclaw/skills/stealth-browser/{sessions,cookies,logs,config,backups,screenshots}

echo "✅ Verzeichnisse erstellt"

# Setze Berechtigungen
echo ""
echo "🔒 Setze Berechtigungen..."

chmod +x stealth-browser 2>/dev/null || true

echo "✅ Berechtigungen gesetzt"

# Test
echo ""
echo "🧪 Führe Installationstest durch..."

python3 stealth-browser test

echo ""
echo "================================================"
echo "  ✅ Installation erfolgreich!"
echo "================================================"
echo ""
echo "Nächste Schritte:"
echo ""
echo "  1. Google-Login durchführen:"
echo "     stealth-browser login google"
echo ""
echo "  2. URL öffnen:"
echo "     stealth-browser open \"https://mail.google.com\""
echo ""
echo "  3. Status prüfen:"
echo "     stealth-browser status"
echo ""
echo "Dokumentation: https://docs.openclaw.ai/skills/stealth-browser"
echo "Support: support@mk-media.eu"
echo ""
