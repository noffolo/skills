# Stealth-Browser Skill

**Professionelle Browser-Automation für OpenClaw mit automatischem Google-Login.**

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-commercial-green)
![Price](https://img.shields.io/badge/price-79€-orange)

---

## 🎯 Features

- ✅ **Automatischer Google-Login** – Einmal einloggen, immer eingeloggt
- ✅ **Anti-Bot-Erkennung** – Umgeht alle gängigen Detection-Methoden
- ✅ **Persistente Sessions** – Login bleibt dauerhaft gespeichert
- ✅ **Multi-Account** – Unterstützt mehrere Profile gleichzeitig
- ✅ **Cookie-Management** – Export, Import, Backup
- ✅ **Stealth-Modus** – Läuft wie ein echter Nutzer

---

## 🚀 Schnellstart

```bash
# 1. Skill installieren
clawhub install stealth-browser

# 2. Google-Login durchführen (einmalig)
stealth-browser login google

# 3. URL öffnen
stealth-browser open "https://mail.google.com"

# 4. Fertig! 🎉
```

---

## 📦 Installation

### Via ClawHub (Empfohlen)

```bash
clawhub install stealth-browser
```

### Manuell

```bash
git clone https://github.com/mk-media/stealth-browser.git
cd stealth-browser
chmod +x stealth-browser
./install.sh
```

---

## 💼 Use Cases

### SEO & Backlink-Outreach
```bash
# Foren-Accounts erstellen
stealth-browser register "https://forum.example.com"

# Profile mit Backlink
stealth-browser fill-profile --website "https://deine-site.de"
```

### Social Media Automation
```bash
# YouTube-Kommentare
stealth-browser youtube comment --video "xyz" --text "..."

# Twitter Posts
stealth-browser twitter post --text "..."
```

### Data-Scraping
```bash
# Seiten scrapen
stealth-browser scrape --url "..." --selector ".product"

# Screenshots
stealth-browser screenshot --url "..."
```

---

## 📋 Befehle

| Befehl | Beschreibung |
|--------|--------------|
| `login <service>` | Login für Service durchführen |
| `open <url>` | URL öffnen |
| `sessions` | Alle Sessions auflisten |
| `status` | System-Status anzeigen |
| `cookies export <service>` | Cookies exportieren |
| `screenshot` | Screenshot machen |
| `delete <session>` | Session löschen |

---

## 💰 Pricing

| Paket | Preis | Features |
|-------|-------|----------|
| **Basic** | 29€ | Google Login, 3 Sessions |
| **Pro** | 79€ | Alle Logins, Cookies, Stealth |
| **Enterprise** | 199€ | + Multi-Account, Proxy, API |

---

## 🔧 Technische Details

- **Version:** 1.0.0
- **Autor:** MK Media
- **Python:** 3.8+
- **Browser:** Chrome, Chromium
- **OS:** Ubuntu, Debian, macOS

---

## 📚 Dokumentation

- 📖 [Benutzerhandbuch](docs/BENUTZERHANDBUCH.md)
- 🔧 [API-Referenz](docs/API-REFERENZ.md)
- 💡 [Beispiele](examples/)
- 🐛 [Troubleshooting](docs/TROUBLESHOOTING.md)

---

## 🆘 Support

- **E-Mail:** support@mk-media.eu
- **Telegram:** @VerstehenVertiefenVerwandeln
- **Discord:** OpenClaw Community

---

## 📜 Lizenz

**Commercial License** - Ein Kauf berechtigt zur Nutzung auf einem OpenClaw-Server.

---

**Entwickelt von MK Media | © 2026 Alle Rechte vorbehalten**