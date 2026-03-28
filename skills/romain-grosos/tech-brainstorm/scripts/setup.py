#!/usr/bin/env python3
"""
setup.py - Wizard interactif d'initialisation du skill tech-brainstorm.

Modes :
  python3 setup.py                      # wizard initial
  python3 setup.py --manage-outputs     # gestion des sorties (dispatch)
  python3 setup.py --show               # affiche la config actuelle
  python3 setup.py --cleanup            # supprime les fichiers persistants
  python3 setup.py --non-interactive    # valeurs par defaut sans prompts
"""

import argparse
import json
import sys
from pathlib import Path

# ---- Paths ------------------------------------------------------------------

SKILL_DIR    = Path(__file__).resolve().parent.parent
_CONFIG_DIR  = Path.home() / ".openclaw" / "config" / "tech-brainstorm"
_DATA_DIR    = Path.home() / ".openclaw" / "data" / "tech-brainstorm"
CONFIG_FILE  = _CONFIG_DIR / "config.json"
EXAMPLE_FILE = SKILL_DIR / "config.example.json"


# ---- Helpers ----------------------------------------------------------------


def _ask(prompt: str, default: str, interactive: bool) -> str:
    if not interactive:
        return default
    try:
        answer = input(f"{prompt} [{default}]: ").strip()
        return answer if answer else default
    except (EOFError, KeyboardInterrupt):
        print()
        return default


def _confirm(prompt: str, interactive: bool) -> bool:
    if not interactive:
        return False
    try:
        answer = input(f"{prompt} [y/N]: ").strip().lower()
        return answer in ("y", "yes", "o", "oui")
    except (EOFError, KeyboardInterrupt):
        print()
        return False


def _load_json(path: Path) -> dict:
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"[WARN] Could not read {path}: {e}", file=sys.stderr)
    return {}


def _save_json(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


# ---- Initial setup ----------------------------------------------------------


def run_setup(interactive: bool = True):
    print()
    print("=" * 52)
    print("  OpenClaw Skill Tech-Brainstorm - Setup")
    print("=" * 52)

    # Step 1: Create directories
    print()
    print("[1/4] Creating directories...")
    _CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    _DATA_DIR.mkdir(parents=True, exist_ok=True)
    (_DATA_DIR / "reports").mkdir(parents=True, exist_ok=True)
    print(f"  OK  {_CONFIG_DIR}")
    print(f"  OK  {_DATA_DIR}")

    # Load example config as base
    if not EXAMPLE_FILE.exists():
        print(f"\n[ERROR] config.example.json not found at {EXAMPLE_FILE}", file=sys.stderr)
        sys.exit(1)

    example_cfg = _load_json(EXAMPLE_FILE)

    # Step 2: Language & timezone
    print()
    print("[2/4] Configuration generale...")

    default_lang = example_cfg.get("language", "fr")
    lang = _ask("  Language (fr / en)", default_lang, interactive).strip().lower()
    if lang not in ("fr", "en"):
        print(f"  [WARN] Unknown language '{lang}', using 'fr'")
        lang = "fr"
    example_cfg["language"] = lang

    default_tz = example_cfg.get("timezone", "Europe/Paris")
    tz_val = _ask("  Timezone (e.g. Europe/Paris)", default_tz, interactive).strip()
    example_cfg["timezone"] = tz_val or default_tz

    # Step 3: LLM config
    print()
    print("[3/4] Configuration LLM...")

    llm = example_cfg.get("llm", {})

    default_url = llm.get("base_url", "https://api.openai.com/v1")
    llm["base_url"] = _ask("  API base URL", default_url, interactive)

    default_model = llm.get("model", "gpt-4o-mini")
    llm["model"] = _ask("  Model", default_model, interactive)

    default_key = llm.get("api_key_file", "~/.openclaw/secrets/openai_api_key")
    key_path = _ask("  API key file path", default_key, interactive)
    llm["api_key_file"] = key_path

    # Check if key file exists
    key_p = Path(key_path).expanduser()
    if key_p.exists():
        print(f"  OK  API key file found: {key_p}")
    else:
        print(f"  [WARN] API key file not found: {key_p}")
        if _confirm("  Create it now?", interactive):
            try:
                api_key = input("  Paste your API key: ").strip()
            except (EOFError, KeyboardInterrupt):
                api_key = ""
            if api_key:
                key_p.parent.mkdir(parents=True, exist_ok=True)
                key_p.write_text(api_key, encoding="utf-8")
                import os
                if os.name != "nt":
                    key_p.chmod(0o600)
                print(f"  OK  API key saved: {key_p}")
            else:
                print("  SKIP (no key provided)")

    llm["enabled"] = True
    example_cfg["llm"] = llm

    # Step 4: Write config
    print()
    print("[4/4] Writing config file...")
    if CONFIG_FILE.exists():
        print(f"  [WARN] Config already exists: {CONFIG_FILE}")
        if _confirm("  Overwrite with defaults?", interactive):
            _save_json(CONFIG_FILE, example_cfg)
            print(f"  OK  {CONFIG_FILE} (overwritten)")
        else:
            print(f"  SKIP {CONFIG_FILE} (kept existing)")
    else:
        _save_json(CONFIG_FILE, example_cfg)
        print(f"  OK  {CONFIG_FILE} (created)")

    # Summary
    print()
    print("=" * 52)
    print("  Setup complete!")
    print()
    print(f"  Config  : {CONFIG_FILE}")
    print(f"  Data    : {_DATA_DIR}/")
    print(f"  Reports : {_DATA_DIR / 'reports'}/")
    print()
    print("  Next steps:")
    print("    python3 init.py                          # validate")
    print("    python3 setup.py --manage-outputs        # configure dispatch")
    print("    python3 tech_brainstorm.py brainstorm \\")
    print('      --topic "k8s on-prem" \\')
    print('      --context "AWX + Terraform, 10 apps"')
    print("=" * 52)
    print()


# ---- Output management ------------------------------------------------------

_OUTPUT_TYPES = {
    "1": "telegram_bot",
    "2": "mail-client",
    "3": "nextcloud",
    "4": "file",
}

_OUTPUT_DEFAULTS = {
    "telegram_bot": {
        "type": "telegram_bot",
        "chat_id": "",
        "content": "recap",
        "enabled": True,
    },
    "mail-client": {
        "type": "mail-client",
        "mail_to": "",
        "subject": "Tech Brainstorm - {topic} - {date}",
        "content": "full_report",
        "enabled": True,
    },
    "nextcloud": {
        "type": "nextcloud",
        "path": "/Brainstorms/brainstorm.md",
        "content": "full_report",
        "mode": "append",
        "enabled": True,
    },
    "file": {
        "type": "file",
        "path": "~/.openclaw/data/tech-brainstorm/reports/report-latest.md",
        "content": "full_report",
        "enabled": True,
    },
}

_OUTPUT_REQUIRED_FIELDS = {
    "telegram_bot": [("chat_id", "Telegram chat_id", "")],
    "mail-client":  [("mail_to", "Recipient email", "")],
    "nextcloud":    [("path", "Nextcloud path", "/Brainstorms/brainstorm.md")],
    "file":         [("path", "Local file path", "~/.openclaw/data/tech-brainstorm/reports/report-latest.md")],
}


def _display_outputs(outputs: list):
    if not outputs:
        print("  (no outputs configured)")
        return
    for i, out in enumerate(outputs):
        status = "[ON] " if out.get("enabled", True) else "[off]"
        t = out.get("type", "?")
        details = []
        for k in ("chat_id", "mail_to", "path"):
            if k in out:
                details.append(f"{k}={out[k]}")
        content = out.get("content", "full_report")
        details.append(f"content={content}")
        print(f"  {i + 1}. {status} {t}  ({', '.join(details)})")


def run_manage_outputs():
    """Interactive output management menu."""
    print()
    print("=" * 52)
    print("  Tech-Brainstorm - Gestion des sorties")
    print("=" * 52)

    if not CONFIG_FILE.exists():
        print(f"\n[WARN] {CONFIG_FILE} not found. Run setup.py first.", file=sys.stderr)
        sys.exit(1)

    user_cfg = _load_json(CONFIG_FILE)
    outputs: list = user_cfg.get("outputs", [])

    print("\n  Types disponibles :")
    for k, v in _OUTPUT_TYPES.items():
        print(f"    {k}. {v}")
    print()
    print("  Commandes : t <n> = toggle, a = add, d <n> = delete, q = save & quit")

    while True:
        print()
        print("  Sorties configurees :")
        _display_outputs(outputs)
        print()

        try:
            raw = input("  Action (t/a/d/q) : ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            raw = "q"

        if not raw:
            continue

        parts = raw.split()
        cmd = parts[0].lower()

        if cmd == "q":
            break

        elif cmd == "t":
            if len(parts) < 2:
                print("  Usage: t <numero>")
                continue
            try:
                idx = int(parts[1]) - 1
                if 0 <= idx < len(outputs):
                    outputs[idx]["enabled"] = not outputs[idx].get("enabled", True)
                    status = "ON" if outputs[idx]["enabled"] else "off"
                    print(f"  -> {outputs[idx]['type']}: {status}")
                else:
                    print(f"  Numero hors plage (1-{len(outputs)})")
            except ValueError:
                print("  Numero invalide")

        elif cmd == "a":
            print("  Type de sortie :")
            for k, v in _OUTPUT_TYPES.items():
                print(f"    {k}. {v}")
            try:
                choice = input("  Choix (1-4) : ").strip()
            except (EOFError, KeyboardInterrupt):
                continue
            out_type = _OUTPUT_TYPES.get(choice)
            if not out_type:
                print("  Choix invalide")
                continue

            new_out = dict(_OUTPUT_DEFAULTS[out_type])

            for field, label, default in _OUTPUT_REQUIRED_FIELDS.get(out_type, []):
                try:
                    val = input(f"  {label} [{default}] : ").strip()
                    new_out[field] = val if val else default
                except (EOFError, KeyboardInterrupt):
                    new_out[field] = default

            # Content type
            print("  Contenu : 1. recap (court)  2. full_report (complet)")
            try:
                ct = input("  Choix [2] : ").strip()
                new_out["content"] = "recap" if ct == "1" else "full_report"
            except (EOFError, KeyboardInterrupt):
                new_out["content"] = "full_report"

            outputs.append(new_out)
            print(f"  -> Added: {out_type}")

        elif cmd == "d":
            if len(parts) < 2:
                print("  Usage: d <numero>")
                continue
            try:
                idx = int(parts[1]) - 1
                if 0 <= idx < len(outputs):
                    removed = outputs.pop(idx)
                    print(f"  -> Removed: {removed.get('type','?')}")
                else:
                    print(f"  Numero hors plage (1-{len(outputs)})")
            except ValueError:
                print("  Numero invalide")

        else:
            print("  Commandes : t <n>=toggle, a=add, d <n>=delete, q=save&quit")

    user_cfg["outputs"] = outputs
    _save_json(CONFIG_FILE, user_cfg)
    print()
    print(f"  Sauvegarde : {len(outputs)} sortie(s) -> {CONFIG_FILE}")
    print()


# ---- Show config ------------------------------------------------------------


def show_config():
    """Display current config."""
    print()
    if not CONFIG_FILE.exists():
        print(f"Config not found: {CONFIG_FILE}")
        print("Run: python3 setup.py")
        return
    cfg = _load_json(CONFIG_FILE)
    print(f"Config: {CONFIG_FILE}")
    print()
    print(json.dumps(cfg, indent=2, ensure_ascii=False))
    print()


# ---- Cleanup ----------------------------------------------------------------


def cleanup():
    """Remove all persistent files written by this skill."""
    print("Removing tech-brainstorm skill persistent files...")
    removed = []

    if CONFIG_FILE.exists():
        CONFIG_FILE.unlink()
        removed.append(str(CONFIG_FILE))

    # Remove report files
    reports_dir = _DATA_DIR / "reports"
    if reports_dir.exists():
        for f in reports_dir.iterdir():
            if f.is_file():
                f.unlink()
                removed.append(str(f))
        try:
            reports_dir.rmdir()
        except OSError:
            pass

    for d in [_DATA_DIR, _CONFIG_DIR]:
        try:
            d.rmdir()
        except OSError:
            pass

    if removed:
        for p in removed:
            print(f"  Removed: {p}")
        print("Done. Re-run setup.py to reconfigure.")
    else:
        print("  Nothing to remove.")


# ---- Main -------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(description="OpenClaw tech-brainstorm - setup wizard")
    parser.add_argument("--manage-outputs", action="store_true",
                        help="Gestion interactive des sorties (telegram, mail, nextcloud, file)")
    parser.add_argument("--show", action="store_true",
                        help="Affiche la config actuelle")
    parser.add_argument("--non-interactive", action="store_true",
                        help="Utilise les valeurs par defaut sans prompts")
    parser.add_argument("--cleanup", action="store_true",
                        help="Remove all persistent files (config + data)")
    args = parser.parse_args()

    if args.cleanup:
        cleanup()
    elif args.manage_outputs:
        run_manage_outputs()
    elif args.show:
        show_config()
    else:
        run_setup(interactive=not args.non_interactive)


if __name__ == "__main__":
    main()
