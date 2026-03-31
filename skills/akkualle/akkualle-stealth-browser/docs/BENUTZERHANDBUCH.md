# Stealth-Browser Benutzerhandbuch

**Version 1.0.0 | MK Media**

---

## 📚 Inhaltsverzeichnis

1. [Einführung](#einführung)
2. [Installation](#installation)
3. [Erste Schritte](#erste-schritte)
4. [Session-Management](#session-management)
5. [Cookie-Management](#cookie-management)
6. [Use Cases](#use-cases)
7. [Troubleshooting](#troubleshooting)
8. [FAQ](#faq)

---

## 🎯 Einführung

### Was ist Stealth-Browser?

Stealth-Browser ist ein professioneller OpenClaw Skill für automatisierte Browser-Aufgaben mit integriertem Anti-Bot-Schutz. Er ermöglicht es Ihnen, sich einmalig bei Services wie Google anzumelden und diese Anmeldung dauerhaft zu nutzen.

### Hauptfeatures

- ✅ **Automatischer Login** – Einmal einloggen, immer eingeloggt
- ✅ **Anti-Bot-Erkennung** – Umgeht alle gängigen Detection-Methoden
- ✅ **Persistente Sessions** – Login bleibt dauerhaft gespeichert
- ✅ **Multi-Account** – Unterstützt mehrere Profile gleichzeitig
- ✅ **Cookie-Management** – Export, Import, Backup

---

## 📦 Installation

### Voraussetzungen

- OpenClaw v2.0 oder höher
- Python 3.8+
- Google Chrome oder Chromium

### Installation via ClawHub

```bash
clawhub install stealth-browser
```

### Manuelle Installation

```bash
git clone https://github.com/mk-media/stealth-browser.git
cd stealth-browser
./install.sh
```

---

## 🚀 Erste Schritte

### Schritt 1: Google-Login

Der erste Schritt ist ein einmaliger Login bei Google:

```bash
stealth-browser login google
```

**Was passiert:**
1. Browser öffnet sich
2. Sie loggen sich manuell ein
3. Session wird automatisch gespeichert

### Schritt 2: Testen

Prüfen Sie ob der Login funktioniert:

```bash
stealth-browser open "https://mail.google.com"
```

Sie sollten jetzt eingeloggt sein!

### Schritt 3: Status prüfen

```bash
stealth-browser status
```

---

## 💼 Session-Management

### Sessions auflisten

```bash
stealth-browser sessions
```

**Ausgabe:**
```
📱 3 Sessions gefunden:

✅ google
   Erstellt: 2026-03-18T18:00:00
   Zuletzt verwendet: 2026-03-18T19:00:00
   Service: google

✅ youtube
   Erstellt: 2026-03-18T18:00:00
   Service: youtube
```

### Session löschen

```bash
stealth-browser delete google
```

**Hinweis:** Ein Backup wird automatisch erstellt.

---

## 🍪 Cookie-Management

### Cookies exportieren

```bash
stealth-browser cookies export google
```

### Cookies importieren

```bash
stealth-browser cookies import google --file cookies.json
```

---

## 🎯 Use Cases

### 1. Backlink-Outreach

```bash
# Forum öffnen
stealth-browser open "https://forum.example.com/register"

# Account erstellen
# (Automatisierung via Script möglich)
```

### 2. Social Media

```bash
# YouTube Studio öffnen
stealth-browser open "https://studio.youtube.com"

# Twitter öffnen
stealth-browser open "https://twitter.com"
```

### 3. SEO

```bash
# Google Search Console
stealth-browser open "https://search.google.com/search-console"

# Google Analytics
stealth-browser open "https://analytics.google.com"
```

---

## 🐛 Troubleshooting

### Problem: Browser startet nicht

**Lösung:**
```bash
# Chrome installieren
apt install google-chrome-stable

# Oder Chromium
apt install chromium-browser
```

### Problem: Login funktioniert nicht

**Lösung:**
```bash
# Session löschen und neu einloggen
stealth-browser delete google
stealth-browser login google
```

### Problem: Cookies werden nicht erkannt

**Lösung:**
```bash
# Cookies exportieren und prüfen
stealth-browser cookies export google
cat /root/.openclaw/skills/stealth-browser/cookies/google_cookies.json
```

---

## ❓ FAQ

### F: Wie lange bleibt der Login aktiv?

**A:** Google-Sessions sind normalerweise 2 Wochen aktiv. Der Skill aktualisiert sie automatisch.

### F: Funktioniert das mit allen Google-Diensten?

**A:** Ja, nach dem Google-Login funktionieren alle Google-Dienste: Gmail, YouTube, Ads, Analytics, Search Console, etc.

### F: Kann ich mehrere Accounts nutzen?

**A:** Ja, erstellen Sie verschiedene Profile:
```bash
stealth-browser login google --profile account1
stealth-browser login google --profile account2
```

### F: Ist das sicher?

**A:** Ja, alle Daten bleiben lokal auf Ihrem Server. Cookies werden verschlüsselt gespeichert.

### F: Kann ich das auf ClawHub verkaufen?

**A:** Ja, mit einer Commercial License können Sie den Skill auf ClawHub anbieten.

---

## 📞 Support

- **E-Mail:** support@mk-media.eu
- **Telegram:** @VerstehenVertiefenVerwandeln
- **Discord:** OpenClaw Community
- **Dokumentation:** https://docs.openclaw.ai/skills/stealth-browser

---

**Entwickelt von MK Media | © 2026 Alle Rechte vorbehalten**
