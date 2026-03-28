#!/usr/bin/env python3
"""
tech_brainstorm.py - CLI principal du skill tech-brainstorm OpenClaw.

Commandes :
  run --topic "..." --context "..."   Pipeline complet (recherche + brainstorm + dispatch)
  brainstorm --topic "..." --context "..."   Genere le brainstorm (stdin: sources JSON optionnel)
  send [--profile NAME]              Dispatch le rapport JSON (stdin) vers les sorties configurees
  config                             Affiche la config active

Sortie : JSON sur stdout.
Logs/erreurs : stderr uniquement.
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

_MAX_STDIN_SIZE = 10 * 1024 * 1024  # 10 MB

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _llm import chat_completion, build_research_prompt, build_recap_prompt
from _dispatch import dispatch as _dispatch

# ---- Paths ------------------------------------------------------------------

SKILL_DIR   = Path(__file__).resolve().parent.parent
_CONFIG_DIR = Path.home() / ".openclaw" / "config" / "tech-brainstorm"
_DATA_DIR   = Path.home() / ".openclaw" / "data" / "tech-brainstorm"
CONFIG_FILE = _CONFIG_DIR / "config.json"

# ---- Exceptions -------------------------------------------------------------


class BrainstormError(RuntimeError):
    pass


class BrainstormConfigError(BrainstormError):
    pass


# ---- Default config ---------------------------------------------------------

DEFAULT_CONFIG = {
    "language": "fr",
    "timezone": "Europe/Paris",
    "max_sources": 10,
    "search_depth": "medium",
    "llm": {
        "enabled": True,
        "base_url": "https://api.openai.com/v1",
        "api_key_file": "~/.openclaw/secrets/openai_api_key",
        "model": "gpt-4o-mini",
        "max_tokens": 4096,
        "temperature": 0.7,
    },
    "outputs": [],
}

# ---- Config loading ---------------------------------------------------------


def load_config() -> dict:
    """Load config from CONFIG_FILE, with defaults."""
    cfg = dict(DEFAULT_CONFIG)
    if CONFIG_FILE.exists():
        try:
            user_cfg = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
            # Deep merge llm section
            if "llm" in user_cfg:
                merged_llm = dict(cfg["llm"])
                merged_llm.update(user_cfg["llm"])
                user_cfg["llm"] = merged_llm
            cfg.update(user_cfg)
        except Exception as e:
            print(f"[WARN] Could not read config: {e}", file=sys.stderr)
    else:
        example = SKILL_DIR / "config.example.json"
        if example.exists():
            try:
                user_cfg = json.loads(example.read_text(encoding="utf-8"))
                if "llm" in user_cfg:
                    merged_llm = dict(cfg["llm"])
                    merged_llm.update(user_cfg["llm"])
                    user_cfg["llm"] = merged_llm
                cfg.update(user_cfg)
                print("[INFO] Using config.example.json (run setup.py to initialize)", file=sys.stderr)
            except Exception:
                pass
    return cfg


# ---- Stdin helper -----------------------------------------------------------


def _read_stdin_json() -> dict | list | None:
    """Read JSON from stdin if available (non-blocking check)."""
    if sys.stdin.isatty():
        return None
    raw = sys.stdin.read(_MAX_STDIN_SIZE + 1)
    if not raw.strip():
        return None
    if len(raw) > _MAX_STDIN_SIZE:
        raise BrainstormError(f"stdin payload too large (>{_MAX_STDIN_SIZE // (1024*1024)} MB)")
    return json.loads(raw)


# ---- Commands ---------------------------------------------------------------


def cmd_brainstorm(args, cfg: dict):
    """
    Generate a brainstorm report.

    Reads optional web research from stdin (JSON array of sources).
    Calls LLM to produce synthesis + brainstorm.
    Outputs structured JSON report to stdout.
    """
    topic = args.topic
    context = args.context or ""
    lang = cfg.get("language", "fr")

    if not topic:
        raise BrainstormError("--topic is required")

    # Read optional sources from stdin
    sources = []
    try:
        stdin_data = _read_stdin_json()
        if stdin_data:
            if isinstance(stdin_data, list):
                sources = stdin_data
            elif isinstance(stdin_data, dict) and "sources" in stdin_data:
                sources = stdin_data["sources"]
            elif isinstance(stdin_data, dict) and "articles" in stdin_data:
                sources = stdin_data["articles"]
    except json.JSONDecodeError:
        print("[WARN] Could not parse stdin JSON, proceeding without sources", file=sys.stderr)

    print(f"[INFO] Topic: {topic}", file=sys.stderr)
    print(f"[INFO] Context: {context or '(none)'}", file=sys.stderr)
    print(f"[INFO] Sources from stdin: {len(sources)}", file=sys.stderr)

    # Build LLM prompt and call
    messages = build_research_prompt(topic, context, sources, lang)

    print(f"[INFO] Calling LLM ({cfg.get('llm', {}).get('model', '?')})...", file=sys.stderr)
    report = chat_completion(messages, cfg)
    print(f"[INFO] Report generated ({len(report)} chars)", file=sys.stderr)

    # Generate recap
    recap = ""
    try:
        recap_messages = build_recap_prompt(report, topic, lang)
        recap = chat_completion(recap_messages, cfg)
        print(f"[INFO] Recap generated ({len(recap)} chars)", file=sys.stderr)
    except Exception as e:
        print(f"[WARN] Could not generate recap: {e}", file=sys.stderr)
        # Fallback: first 500 chars of report
        recap = report[:500]

    # Build output
    result = {
        "topic": topic,
        "context": context,
        "report": report,
        "recap": recap,
        "sources_count": len(sources),
        "sources": [{"url": s.get("url", ""), "title": s.get("title", "")} for s in sources],
        "model": cfg.get("llm", {}).get("model", "?"),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_run(args, cfg: dict):
    """
    Full pipeline: brainstorm + dispatch.

    Same as brainstorm, but also dispatches to configured outputs.
    """
    topic = args.topic
    context = args.context or ""
    lang = cfg.get("language", "fr")

    if not topic:
        raise BrainstormError("--topic is required")

    # Read optional sources from stdin
    sources = []
    try:
        stdin_data = _read_stdin_json()
        if stdin_data:
            if isinstance(stdin_data, list):
                sources = stdin_data
            elif isinstance(stdin_data, dict) and "sources" in stdin_data:
                sources = stdin_data["sources"]
    except json.JSONDecodeError:
        print("[WARN] Could not parse stdin JSON, proceeding without sources", file=sys.stderr)

    print(f"[INFO] Topic: {topic}", file=sys.stderr)
    print(f"[INFO] Context: {context or '(none)'}", file=sys.stderr)
    print(f"[INFO] Sources: {len(sources)}", file=sys.stderr)

    # Generate brainstorm
    messages = build_research_prompt(topic, context, sources, lang)
    print(f"[INFO] Calling LLM ({cfg.get('llm', {}).get('model', '?')})...", file=sys.stderr)
    report = chat_completion(messages, cfg)
    print(f"[INFO] Report generated ({len(report)} chars)", file=sys.stderr)

    # Generate recap
    recap = ""
    try:
        recap_messages = build_recap_prompt(report, topic, lang)
        recap = chat_completion(recap_messages, cfg)
    except Exception as e:
        print(f"[WARN] Recap generation failed: {e}", file=sys.stderr)
        recap = report[:500]

    data = {
        "topic": topic,
        "context": context,
        "report": report,
        "recap": recap,
        "sources_count": len(sources),
        "sources": [{"url": s.get("url", ""), "title": s.get("title", "")} for s in sources],
        "model": cfg.get("llm", {}).get("model", "?"),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    # Save report locally
    _DATA_DIR.mkdir(parents=True, exist_ok=True)
    report_file = _DATA_DIR / "reports" / f"brainstorm-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
    report_file.parent.mkdir(parents=True, exist_ok=True)
    report_file.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[INFO] Report saved: {report_file}", file=sys.stderr)

    # Dispatch
    profile = getattr(args, "profile", None)
    results = _dispatch(data, cfg, profile=profile)

    output = {**data, "dispatched": results}
    print(json.dumps(output, ensure_ascii=False, indent=2))

    if results.get("fail"):
        raise BrainstormError(f"Dispatch failed: {results['fail']}")


def cmd_send(args, cfg: dict):
    """Read report JSON from stdin and dispatch to configured outputs."""
    try:
        stdin_data = _read_stdin_json()
        if not stdin_data:
            raise BrainstormError("No JSON data on stdin")
        data = stdin_data if isinstance(stdin_data, dict) else {"report": str(stdin_data)}
    except json.JSONDecodeError as e:
        raise BrainstormError(f"Invalid JSON on stdin: {e}")

    if not data.get("report"):
        raise BrainstormError("No 'report' field in input JSON")

    results = _dispatch(data, cfg, profile=getattr(args, "profile", None))
    print(json.dumps({"dispatched": results}, ensure_ascii=False, indent=2))

    if results.get("fail"):
        raise BrainstormError(f"Dispatch failed: {results['fail']}")


def cmd_config(_args, cfg: dict):
    """Show active config (no secrets)."""
    # Mask API key file content
    safe_cfg = dict(cfg)
    if "llm" in safe_cfg:
        safe_llm = dict(safe_cfg["llm"])
        if "api_key_file" in safe_llm:
            safe_llm["api_key_file"] = safe_llm["api_key_file"] + " (not shown)"
        safe_cfg["llm"] = safe_llm
    print(json.dumps(safe_cfg, indent=2, ensure_ascii=False))


# ---- Main -------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(
        prog="tech_brainstorm.py",
        description="OpenClaw tech-brainstorm - multi-source research + contextual brainstorm",
    )
    sub = parser.add_subparsers(dest="command")

    # brainstorm
    p_bs = sub.add_parser("brainstorm", help="Generate brainstorm report (optional: sources JSON on stdin)")
    p_bs.add_argument("--topic", required=True, help="Technical subject to brainstorm about")
    p_bs.add_argument("--context", default="", help="Your specific context (stack, constraints, team...)")

    # run (brainstorm + dispatch)
    p_run = sub.add_parser("run", help="Full pipeline: brainstorm + dispatch to outputs")
    p_run.add_argument("--topic", required=True, help="Technical subject to brainstorm about")
    p_run.add_argument("--context", default="", help="Your specific context")
    p_run.add_argument("--profile", default=None, help="Named output profile from config")

    # send
    p_send = sub.add_parser("send", help="Dispatch report JSON (stdin) to configured outputs")
    p_send.add_argument("--profile", default=None, help="Named output profile from config")

    # config
    sub.add_parser("config", help="Show active configuration")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    cfg = load_config()

    try:
        if args.command == "brainstorm":
            cmd_brainstorm(args, cfg)
        elif args.command == "run":
            cmd_run(args, cfg)
        elif args.command == "send":
            cmd_send(args, cfg)
        elif args.command == "config":
            cmd_config(args, cfg)
        else:
            parser.print_help()
            sys.exit(1)
    except BrainstormError as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
