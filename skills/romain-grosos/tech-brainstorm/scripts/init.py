#!/usr/bin/env python3
"""
init.py - Validation des capacites du skill tech-brainstorm.

Checks :
  1. Config file exists (~/.openclaw/config/tech-brainstorm/config.json)
  2. Data directories exist (creates them if missing)
  3. LLM API key file exists and is readable
  4. LLM API connectivity test (optional, with --test-llm flag)

Sorties : OK / WARN / FAIL pour chaque check.
Exit code : 0 si tout OK ou WARN, 1 si au moins un FAIL.
"""

import argparse
import json
import sys
from pathlib import Path

# ---- Paths ------------------------------------------------------------------

SKILL_DIR   = Path(__file__).resolve().parent.parent
_CONFIG_DIR = Path.home() / ".openclaw" / "config" / "tech-brainstorm"
_DATA_DIR   = Path.home() / ".openclaw" / "data" / "tech-brainstorm"
CONFIG_FILE = _CONFIG_DIR / "config.json"

# ---- Reporting --------------------------------------------------------------

_results = []


def _report(status: str, label: str, detail: str = ""):
    icon = {"OK": "[OK  ]", "WARN": "[WARN]", "FAIL": "[FAIL]"}.get(status, "[????]")
    msg = f"{icon} {label}"
    if detail:
        msg += f"\n         {detail}"
    print(msg)
    _results.append(status)


# ---- Checks -----------------------------------------------------------------


def check_config():
    """Check 1: config file exists and is valid JSON."""
    if not CONFIG_FILE.exists():
        _report("FAIL", "Config file",
                f"Not found: {CONFIG_FILE}\n"
                f"         Run: python3 setup.py")
        return None

    try:
        cfg = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        llm_model = cfg.get("llm", {}).get("model", "?")
        _report("OK", "Config file", f"{CONFIG_FILE} (model: {llm_model})")
        return cfg
    except Exception as e:
        _report("FAIL", "Config file", f"Invalid JSON: {e}")
        return None


def check_data_dirs():
    """Check 2: data directories exist (create if needed)."""
    created = []
    for d in [_DATA_DIR, _DATA_DIR / "reports"]:
        if not d.exists():
            try:
                d.mkdir(parents=True, exist_ok=True)
                created.append(str(d))
            except Exception as e:
                _report("FAIL", "Data directory", f"Cannot create {d}: {e}")
                return

    if created:
        _report("WARN", "Data directories",
                f"Created: {', '.join(created)}")
    else:
        _report("OK", "Data directories", str(_DATA_DIR))


def check_api_key(cfg: dict):
    """Check 3: LLM API key file exists."""
    llm = cfg.get("llm", {})
    if not llm.get("enabled", False):
        _report("WARN", "LLM API key", "LLM is disabled in config")
        return

    key_file = llm.get("api_key_file", "~/.openclaw/secrets/openai_api_key")
    key_path = Path(key_file).expanduser()

    if not key_path.exists():
        _report("FAIL", "LLM API key",
                f"Not found: {key_path}\n"
                f"         Create the file with your API key, then: chmod 600 {key_path}")
        return

    try:
        key = key_path.read_text(encoding="utf-8").strip()
        if not key:
            _report("FAIL", "LLM API key", f"File is empty: {key_path}")
            return
        # Mask key for display
        masked = key[:8] + "..." + key[-4:] if len(key) > 16 else "***"
        _report("OK", "LLM API key", f"{key_path} ({masked})")
    except Exception as e:
        _report("FAIL", "LLM API key", f"Cannot read {key_path}: {e}")


def check_llm_connectivity(cfg: dict):
    """Check 4: test LLM API connectivity (optional)."""
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from _llm import chat_completion

    try:
        response = chat_completion(
            messages=[{"role": "user", "content": "Reply with exactly: OK"}],
            config=cfg,
        )
        if "OK" in response.upper():
            model = cfg.get("llm", {}).get("model", "?")
            _report("OK", "LLM connectivity", f"API responded (model: {model})")
        else:
            _report("WARN", "LLM connectivity",
                    f"API responded but unexpected content: {response[:100]}")
    except Exception as e:
        _report("FAIL", "LLM connectivity", f"API call failed: {e}")


def check_dispatch_skills():
    """Check optional dispatch skills availability."""
    skills_dir = Path.home() / ".openclaw" / "workspace" / "skills"

    for skill_name, script_rel in [
        ("mail-client", "mail-client/scripts/mail.py"),
        ("nextcloud-files", "nextcloud-files/scripts/nextcloud.py"),
    ]:
        script = skills_dir / script_rel
        if script.exists():
            _report("OK", f"Dispatch: {skill_name}", "installed")
        else:
            _report("WARN", f"Dispatch: {skill_name}",
                    f"not installed (optional - needed for {skill_name} output)")


# ---- Main -------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(description="Validate tech-brainstorm skill")
    parser.add_argument("--test-llm", action="store_true",
                        help="Test LLM API connectivity (makes a real API call)")
    args = parser.parse_args()

    print("=== OpenClaw Skill Tech-Brainstorm - Init Check ===")
    print()

    cfg = check_config()
    check_data_dirs()

    if cfg is not None:
        check_api_key(cfg)
        if args.test_llm:
            check_llm_connectivity(cfg)
        check_dispatch_skills()
    else:
        _report("WARN", "LLM API key", "Skipped (config unavailable)")

    print()
    fails = _results.count("FAIL")
    warns = _results.count("WARN")

    if fails > 0:
        print(f"Result: {fails} FAIL, {warns} WARN - fix errors before using the skill")
        sys.exit(1)
    elif warns > 0:
        print(f"Result: {warns} WARN - skill usable but review warnings")
    else:
        print("Result: all checks passed - skill ready")


if __name__ == "__main__":
    main()
