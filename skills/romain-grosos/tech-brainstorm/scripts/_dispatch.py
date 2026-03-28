"""
_dispatch.py - Output dispatcher for the tech-brainstorm skill.

Dispatches brainstorm reports to configured outputs:
  telegram_bot  - Short recap via Telegram Bot API
  mail-client   - Full HTML report via mail-client skill or SMTP fallback
  nextcloud     - Full Markdown report via nextcloud skill
  file          - Full Markdown report to local file

Content types:
  recap       - Short text summary (Telegram)
  full_report - Full Markdown or HTML report
"""

import html
import json
import os
import pathlib
import re as _re
import subprocess
import sys
import urllib.request
from datetime import datetime, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

_SEP = os.sep

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

_SKILLS_DIR = pathlib.Path.home() / ".openclaw" / "workspace" / "skills"
_OC_CONFIG  = pathlib.Path.home() / ".openclaw" / "openclaw.json"

# ---------------------------------------------------------------------------
# File output safety (same rules as veille skill)
# ---------------------------------------------------------------------------

_BLOCKED_PATH_PATTERNS = [
    ".ssh", ".gnupg", ".config/systemd", "crontab",
    "/etc/", ".bashrc", ".profile", ".bash_profile", ".zshrc",
    ".env",
]

_DEFAULT_ALLOWED_DIR = pathlib.Path.home() / ".openclaw"

_MAX_OUTPUT_SIZE = 1_048_576  # 1 MB

_BLOCKED_CONTENT_PATTERNS = [
    "#!/",
    "ssh-rsa ", "ssh-ed25519 ", "ssh-ecdsa ",
    "BEGIN OPENSSH PRIVATE KEY",
    "BEGIN RSA PRIVATE KEY",
    "BEGIN PGP",
    "eval(", "exec(", "__import__(",
    "import os", "import subprocess",
]

_BLOCKED_CONTENT_RE = _re.compile(
    r"#\s*!.*(?:/bin/|/usr/bin/|python|bash|sh|perl)"
    r"|eval\s*\("
    r"|exec\s*\("
    r"|__import__\s*\("
    r"|import\s+(?:os|subprocess|shutil|pty)"
    r"|getattr\s*\(\s*__builtins__"
    r"|compile\s*\(",
    _re.IGNORECASE,
)


def _validate_skill_script(script_path: pathlib.Path, skill_name: str) -> bool:
    """Validate that a skill script path is under the expected skills directory."""
    try:
        resolved = script_path.resolve()
        skills_resolved = _SKILLS_DIR.resolve()
        resolved_str = str(resolved)
        skills_str = str(skills_resolved)
        if resolved_str != skills_str and not resolved_str.startswith(skills_str + _SEP):
            print(f"[dispatch] BLOCKED: {skill_name} script path {resolved} "
                  f"is outside {skills_resolved}", file=sys.stderr)
            return False
    except (OSError, ValueError):
        return False
    return True


def _validate_output_path(file_path: str, config: dict) -> pathlib.Path | None:
    """Validate that a file output path is safe to write to."""
    try:
        p = pathlib.Path(file_path).expanduser().resolve()
    except (OSError, ValueError):
        print(f"[dispatch:file] BLOCKED: cannot resolve path {file_path!r}",
              file=sys.stderr)
        return None

    p_str = str(p)
    for pattern in _BLOCKED_PATH_PATTERNS:
        if pattern in p_str:
            print(f"[dispatch:file] BLOCKED: path {p} matches blocked "
                  f"pattern {pattern!r}", file=sys.stderr)
            return None

    allowed_dirs = [_DEFAULT_ALLOWED_DIR.resolve()]
    for extra in config.get("security", {}).get("allowed_output_dirs", []):
        try:
            allowed_dirs.append(pathlib.Path(extra).expanduser().resolve())
        except (OSError, ValueError):
            pass

    for allowed in allowed_dirs:
        a_str = str(allowed)
        if str(p) == a_str or str(p).startswith(a_str + _SEP):
            return p

    print(f"[dispatch:file] BLOCKED: {p} is outside allowed directories "
          f"{[str(d) for d in allowed_dirs]} - add to "
          f"config.security.allowed_output_dirs to allow", file=sys.stderr)
    return None


def _validate_file_content(text: str) -> bool:
    """Validate that content does not contain suspicious patterns."""
    if len(text.encode("utf-8")) > _MAX_OUTPUT_SIZE:
        print(f"[dispatch:file] BLOCKED: content too large", file=sys.stderr)
        return False
    for pattern in _BLOCKED_CONTENT_PATTERNS:
        if pattern in text:
            print(f"[dispatch:file] BLOCKED: content contains suspicious "
                  f"pattern {pattern!r}", file=sys.stderr)
            return False
    m = _BLOCKED_CONTENT_RE.search(text)
    if m:
        print(f"[dispatch:file] BLOCKED: content matches suspicious "
              f"regex pattern {m.group()!r}", file=sys.stderr)
        return False
    return True


# ---------------------------------------------------------------------------
# Timezone
# ---------------------------------------------------------------------------


def _get_tz(config: dict):
    tz_name = config.get("timezone", "").strip()
    if not tz_name:
        etc_tz = pathlib.Path("/etc/timezone")
        if etc_tz.exists():
            tz_name = etc_tz.read_text(encoding="utf-8").strip()
    if tz_name:
        try:
            return ZoneInfo(tz_name)
        except (ZoneInfoNotFoundError, Exception):
            print(f"[dispatch] unknown timezone '{tz_name}', using UTC", file=sys.stderr)
    return timezone.utc


# ---------------------------------------------------------------------------
# i18n
# ---------------------------------------------------------------------------

_STRINGS = {
    "fr": {
        "title":       "Brainstorm technique",
        "recap_title": "Brainstorm tech",
        "date_fmt":    "%d/%m/%Y %H:%M",
        "footer":      "OpenClaw tech-brainstorm skill",
    },
    "en": {
        "title":       "Tech Brainstorm",
        "recap_title": "Tech brainstorm",
        "date_fmt":    "%Y-%m-%d %H:%M",
        "footer":      "OpenClaw tech-brainstorm skill",
    },
}

_DEFAULT_LANG = "fr"

JOURS_FR = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
MOIS_FR  = ["janvier", "fevrier", "mars", "avril", "mai", "juin",
             "juillet", "aout", "septembre", "octobre", "novembre", "decembre"]


def _t(lang: str, key: str, **kwargs) -> str:
    s = _STRINGS.get(lang, _STRINGS[_DEFAULT_LANG]).get(key, key)
    return s.format(**kwargs) if kwargs else s


def _date_fr(dt=None) -> str:
    d = dt or datetime.now()
    return f"{JOURS_FR[d.weekday()]} {d.day} {MOIS_FR[d.month - 1]} {d.year}"


# ---------------------------------------------------------------------------
# OpenClaw config helpers
# ---------------------------------------------------------------------------


def _oc_telegram_token() -> str:
    """Read Telegram bot token from ~/.openclaw/openclaw.json (read-only)."""
    if not _OC_CONFIG.exists():
        return ""
    try:
        print(f"[dispatch:telegram] reading bot token from {_OC_CONFIG}", file=sys.stderr)
        d = json.loads(_OC_CONFIG.read_text(encoding="utf-8"))
        return d.get("channels", {}).get("telegram", {}).get("botToken", "")
    except Exception:
        return ""


# ---------------------------------------------------------------------------
# Format helpers
# ---------------------------------------------------------------------------


def format_report_html(data: dict, lang: str = _DEFAULT_LANG, tz=timezone.utc) -> str:
    """Full HTML report for email dispatch."""
    now_dt   = datetime.now(tz)
    today    = _date_fr(now_dt)
    time_str = now_dt.strftime("%H:%M")

    topic   = html.escape(data.get("topic", "?"))
    context = html.escape(data.get("context", ""))
    report  = data.get("report", "")

    # Convert Markdown headers and bold to basic HTML
    body_html = html.escape(report)
    body_html = _re.sub(r'^### (.+)$', r'<h3 style="font-size:15px;font-weight:700;color:#111827;margin:18px 0 8px 0;">\1</h3>', body_html, flags=_re.MULTILINE)
    body_html = _re.sub(r'^## (.+)$', r'<h2 style="font-size:17px;font-weight:700;color:#111827;margin:22px 0 10px 0;border-bottom:1px solid #e5e7eb;padding-bottom:6px;">\1</h2>', body_html, flags=_re.MULTILINE)
    body_html = _re.sub(r'^# (.+)$', r'<h1 style="font-size:20px;font-weight:800;color:#111827;margin:24px 0 12px 0;">\1</h1>', body_html, flags=_re.MULTILINE)
    body_html = _re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', body_html)
    body_html = _re.sub(r'\*(.+?)\*', r'<em>\1</em>', body_html)
    body_html = body_html.replace("\n", "<br>\n")

    # Wrap bullet points
    body_html = _re.sub(r'^- (.+)$', r'<div style="padding-left:16px;margin:4px 0;">&#8226; \1</div>', body_html, flags=_re.MULTILINE)

    title = _t(lang, "title")

    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
</head>
<body style="margin:0;padding:0;background:#f3f4f6;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0">
    <tr>
      <td style="padding:24px 16px;">
        <table width="100%" cellpadding="0" cellspacing="0" style="max-width:800px;margin:0 auto;background:#ffffff;border-radius:10px;border:1px solid #e5e7eb;">
          <tr>
            <td style="padding:24px 32px 16px 32px;border-bottom:1px solid #f3f4f6;">
              <div style="font-size:11px;color:#9ca3af;text-transform:uppercase;letter-spacing:1px;margin-bottom:6px;">{today}</div>
              <div style="font-size:22px;font-weight:800;color:#111827;">🧠 {html.escape(title)}</div>
              <div style="font-size:15px;font-weight:600;color:#374151;margin-top:6px;">{topic}</div>
              <div style="font-size:13px;color:#6b7280;margin-top:4px;">{context}</div>
            </td>
          </tr>
          <tr>
            <td style="padding:16px 32px 24px 32px;font-size:14px;line-height:1.6;color:#374151;">
              {body_html}
            </td>
          </tr>
          <tr>
            <td style="padding:14px 32px;background:#f9fafb;border-top:1px solid #f3f4f6;border-radius:0 0 10px 10px;">
              <div style="font-size:11px;color:#9ca3af;">Jarvis · {time_str} · brainstorm technique</div>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""


# ---------------------------------------------------------------------------
# Handlers
# ---------------------------------------------------------------------------


def _out_telegram(cfg: dict, data: dict, lang: str = _DEFAULT_LANG, tz=timezone.utc) -> bool:
    """Send recap to Telegram via Bot API."""
    token = cfg.get("bot_token") or _oc_telegram_token()
    chat_id = str(cfg.get("chat_id", ""))
    if not token:
        print("[dispatch:telegram] bot_token not found", file=sys.stderr)
        return False
    if not chat_id:
        print("[dispatch:telegram] chat_id required", file=sys.stderr)
        return False

    content = cfg.get("content", "recap")
    if content == "recap":
        text = data.get("recap", data.get("report", "")[:500])
    else:
        text = data.get("report", "")
        # Telegram has a 4096 char limit
        if len(text) > 4000:
            text = text[:4000] + "\n\n... [tronque]"

    payload = json.dumps({
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True,
    }).encode()
    req = urllib.request.Request(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read())
        if result.get("ok"):
            print("[dispatch:telegram] OK", file=sys.stderr)
            return True
        print(f"[dispatch:telegram] API error: {result.get('description','?')}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"[dispatch:telegram] error: {e}", file=sys.stderr)
        return False


def _out_mail(cfg: dict, data: dict, lang: str = _DEFAULT_LANG, tz=timezone.utc) -> bool:
    """Send via mail-client skill CLI, fallback to raw SMTP."""
    mail_to = cfg.get("mail_to", "")
    if not mail_to:
        print("[dispatch:mail-client] mail_to required", file=sys.stderr)
        return False

    date_fmt = _t(lang, "date_fmt")
    now = datetime.now(tz).strftime(date_fmt)
    topic = data.get("topic", "?")
    subject = cfg.get("subject", f"{_t(lang, 'title')} - {topic} - {now}")
    subject = subject.replace("{topic}", topic).replace("{date}", now)

    body_plain = data.get("report", "")
    body_html = format_report_html(data, lang, tz)

    mail_script = _SKILLS_DIR / "mail-client" / "scripts" / "mail.py"
    if mail_script.exists() and _validate_skill_script(mail_script, "mail-client"):
        cmd = [sys.executable, str(mail_script), "send",
               "--to", mail_to, "--subject", subject, "--body", body_plain,
               "--html", body_html]
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if r.returncode == 0:
                print("[dispatch:mail-client] OK", file=sys.stderr)
                return True
            print(f"[dispatch:mail-client] skill error: {r.stderr[:200]}", file=sys.stderr)
        except Exception as e:
            print(f"[dispatch:mail-client] skill call error: {e}", file=sys.stderr)
        print("[dispatch:mail-client] falling back to SMTP config", file=sys.stderr)

    return _smtp_fallback(cfg, subject, body_plain, body_html)


def _smtp_fallback(cfg: dict, subject: str, body_plain: str, body_html: str = None) -> bool:
    """Raw SMTP send when mail-client skill is unavailable."""
    import smtplib
    import ssl as _ssl
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    import email.utils

    host     = cfg.get("smtp_host", "")
    port     = int(cfg.get("smtp_port", 587))
    user     = cfg.get("smtp_user", "")
    password = cfg.get("smtp_app_key", "")
    from_    = cfg.get("mail_from", user)
    to_      = cfg.get("mail_to", "")

    if not all([host, user, password, to_]):
        print("[dispatch:smtp-fallback] missing smtp config", file=sys.stderr)
        return False

    msg = MIMEMultipart("alternative")
    msg["Subject"]    = subject
    msg["From"]       = from_
    msg["To"]         = to_
    msg["Date"]       = email.utils.formatdate(localtime=False)
    msg["Message-ID"] = email.utils.make_msgid()
    msg.attach(MIMEText(body_plain, "plain", "utf-8"))
    if body_html:
        msg.attach(MIMEText(body_html, "html", "utf-8"))

    try:
        ctx = _ssl.create_default_context()
        with smtplib.SMTP(host, port, timeout=30) as s:
            s.ehlo(); s.starttls(context=ctx); s.ehlo()
            s.login(user, password)
            s.sendmail(from_, [to_], msg.as_string())
        print("[dispatch:smtp-fallback] OK", file=sys.stderr)
        return True
    except Exception as e:
        print(f"[dispatch:smtp-fallback] error: {e}", file=sys.stderr)
        return False


def _out_nextcloud(cfg: dict, data: dict, lang: str = _DEFAULT_LANG, tz=timezone.utc) -> bool:
    """Write to Nextcloud via nextcloud skill CLI."""
    nc_path = cfg.get("path", "")
    if not nc_path:
        print("[dispatch:nextcloud] path required", file=sys.stderr)
        return False

    text = data.get("report", "")

    nc_script = _SKILLS_DIR / "nextcloud-files" / "scripts" / "nextcloud.py"
    if not nc_script.exists():
        print(f"[dispatch:nextcloud] skill not installed ({nc_script})", file=sys.stderr)
        return False
    if not _validate_skill_script(nc_script, "nextcloud-files"):
        return False

    mode = cfg.get("mode", "append")

    if mode == "append":
        now = datetime.now(tz)
        topic = data.get("topic", "?")
        separator = f"\n\n---\n\n## {now.strftime('%Y-%m-%d %H:%M')} - {topic}\n\n"
        text = separator + text
        cmd = [sys.executable, str(nc_script), "write", nc_path, "--content", text, "--append"]
    else:
        cmd = [sys.executable, str(nc_script), "write", nc_path, "--content", text]

    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if r.returncode == 0:
            action = "appended to" if mode == "append" else "written to"
            print(f"[dispatch:nextcloud] {action} {nc_path} OK", file=sys.stderr)
            return True
        print(f"[dispatch:nextcloud] error: {r.stderr[:200]}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"[dispatch:nextcloud] error: {e}", file=sys.stderr)
        return False


def _out_file(cfg: dict, data: dict, lang: str = _DEFAULT_LANG, tz=timezone.utc) -> bool:
    """Write report to a local file."""
    file_path = cfg.get("path", "")
    if not file_path:
        print("[dispatch:file] path required", file=sys.stderr)
        return False

    global_config = cfg.get("_global_config", {})
    p = _validate_output_path(file_path, global_config)
    if p is None:
        return False

    text = data.get("report", "")
    if not _validate_file_content(text):
        return False

    try:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
        print(f"[dispatch:file] written to {p} OK", file=sys.stderr)
        return True
    except Exception as e:
        print(f"[dispatch:file] error: {e}", file=sys.stderr)
        return False


# ---------------------------------------------------------------------------
# Handler registry
# ---------------------------------------------------------------------------

_HANDLERS = {
    "telegram_bot": _out_telegram,
    "mail-client":  _out_mail,
    "nextcloud":    _out_nextcloud,
    "file":         _out_file,
}

# ---------------------------------------------------------------------------
# Main dispatch
# ---------------------------------------------------------------------------


def dispatch(data: dict, config: dict, profile: str = None) -> dict:
    """
    Dispatch data to all enabled outputs.
    Returns {"ok": [...], "fail": [...], "skip": [...]}.
    """
    if profile:
        outputs = config.get("profiles", {}).get(profile, [])
        if not outputs:
            print(f"[dispatch] profile '{profile}' not found or empty", file=sys.stderr)
    else:
        outputs = config.get("outputs", [])

    results: dict = {"ok": [], "fail": [], "skip": []}

    if not outputs:
        print("[dispatch] No outputs configured. Run setup.py --manage-outputs", file=sys.stderr)
        return results

    lang = config.get("language", _DEFAULT_LANG)
    if lang not in _STRINGS:
        lang = _DEFAULT_LANG
    tz = _get_tz(config)

    for out in outputs:
        out_type = out.get("type", "")
        if not out.get("enabled", True):
            print(f"[dispatch] {out_type}: skipped (disabled)", file=sys.stderr)
            results["skip"].append(out_type)
            continue
        handler = _HANDLERS.get(out_type)
        if not handler:
            print(f"[dispatch] unknown output type: {out_type!r}", file=sys.stderr)
            results["skip"].append(out_type)
            continue
        out["_global_config"] = config
        ok = handler(out, data, lang=lang, tz=tz)
        results["ok" if ok else "fail"].append(out_type)

    total = len(results["ok"]) + len(results["fail"]) + len(results["skip"])
    print(f"[dispatch] audit: {total} outputs processed "
          f"(ok={results['ok']}, fail={results['fail']}, skip={results['skip']})",
          file=sys.stderr)

    return results
