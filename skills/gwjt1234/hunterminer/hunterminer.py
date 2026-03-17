#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import re
import shutil
import socket
import subprocess
import sys
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Set, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    import psutil
except ImportError:  # pragma: no cover
    psutil = None

from billing import BillingClient, BillingError

BASE_DIR = Path(__file__).resolve().parent
CONFIG = json.loads((BASE_DIR / "config.json").read_text(encoding="utf-8"))
INDICATORS_DIR = BASE_DIR / "indicators"
OUTPUT_DIR = BASE_DIR / CONFIG.get("report_dir", "output")
QUARANTINE_DIR = BASE_DIR / CONFIG.get("quarantine_dir", "output/quarantine")
DEFAULT_MAX_BYTES = int(float(CONFIG.get("default_scan_max_file_size_mb", 20)) * 1024 * 1024)
DEFAULT_READ_BYTES = int(float(CONFIG.get("default_text_read_limit_kb", 512)) * 1024)
SKIP_DIR_NAMES = {
    ".git", ".svn", ".hg", "node_modules", "vendor", "__pycache__", ".cache",
    "Library", "System Volume Information", "$Recycle.Bin", "Windows\\WinSxS"
}
TEXT_EXTS = {
    ".py", ".sh", ".ps1", ".bat", ".cmd", ".yaml", ".yml", ".json", ".toml", ".ini", ".conf",
    ".txt", ".xml", ".js", ".ts", ".go", ".rs", ".c", ".cpp", ".cc", ".h", ".hpp", ".java",
    ".swift", ".rb", ".php", ".pl", ".lua", ".service", ".desktop", ".plist", ".env", ".cfg"
}
WINDOWS_DEFENDER_PATTERNS = [
    r"Set-MpPreference\s+-DisableRealtimeMonitoring\s+\$?true",
    r"Set-MpPreference\s+-DisableBehaviorMonitoring\s+\$?true",
    r"DisableAntiSpyware",
    r"DisableRealtimeMonitoring",
    r"sc\s+(stop|config)\s+WinDefend",
    r"reg\s+add\s+.*Windows Defender",
]
WINDOWS_FIREWALL_PATTERNS = [
    r"netsh\s+advfirewall\s+set\s+allprofiles\s+state\s+off",
    r"Set-NetFirewallProfile\s+-Enabled\s+False",
    r"netsh\s+firewall\s+set\s+opmode\s+disable",
]
LINUX_FIREWALL_PATTERNS = [
    r"ufw\s+disable",
    r"systemctl\s+stop\s+firewalld",
    r"service\s+firewalld\s+stop",
    r"iptables\s+-P\s+INPUT\s+ACCEPT",
    r"iptables\s+-F",
    r"nft\s+flush\s+ruleset",
]
MAC_FIREWALL_PATTERNS = [
    r"pfctl\s+-d",
    r"socketfilterfw\s+--setglobalstate\s+off",
    r"/usr/libexec/ApplicationFirewall/socketfilterfw\s+--setglobalstate\s+off",
]
MINING_CONTENT_HINTS = [
    "stratum+tcp", "stratum+ssl", "nicehash", "mining_pool", "wallet", "rig_id", "xmrig", "cgminer"
]


@dataclass
class Finding:
    id: str
    category: str
    severity: str
    source: str
    path: Optional[str] = None
    pid: Optional[int] = None
    process_name: Optional[str] = None
    remote_ip: Optional[str] = None
    remote_port: Optional[int] = None
    rule: Optional[str] = None
    evidence: List[str] = field(default_factory=list)
    sha256: Optional[str] = None


@dataclass
class IndicatorSet:
    websites: Set[str]
    filenames: Set[str]
    ips: Set[str]
    ports: Set[int]


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def normalize_name(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.lower())


def safe_read_text(path: Path, limit: int = DEFAULT_READ_BYTES) -> str:
    try:
        with path.open("rb") as f:
            chunk = f.read(limit)
        if b"\x00" in chunk[:4096]:
            return ""
        return chunk.decode("utf-8", errors="ignore")
    except Exception:
        return ""


def sha256_file(path: Path) -> Optional[str]:
    try:
        h = hashlib.sha256()
        with path.open("rb") as f:
            for part in iter(lambda: f.read(1024 * 1024), b""):
                h.update(part)
        return h.hexdigest()
    except Exception:
        return None


def load_lines(path: Path) -> List[str]:
    if not path.exists():
        return []
    values = []
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        values.append(line)
    return values


def load_indicators() -> IndicatorSet:
    websites = {v.lower() for v in load_lines(INDICATORS_DIR / "mining_pool_websites.txt")}
    filenames = {v.lower() for v in load_lines(INDICATORS_DIR / "mining_software_filenames.txt")}
    ips = {v for v in load_lines(INDICATORS_DIR / "mining_pool_public_ips.txt")}
    ports = set()
    for item in load_lines(INDICATORS_DIR / "mining_pool_ports.txt"):
        try:
            ports.add(int(item))
        except ValueError:
            continue
    return IndicatorSet(websites=websites, filenames=filenames, ips=ips, ports=ports)


def default_openclaw_skill_roots() -> List[Path]:
    roots = []
    home = Path.home()
    candidates = [
        home / ".openclaw" / "skills",
        home / ".openclaw" / "workspace" / "skills",
        Path.cwd() / "skills",
    ]
    env_dir = os.getenv("OPENCLAW_SKILLS_DIR", "").strip()
    if env_dir:
        candidates.append(Path(env_dir))
    for item in candidates:
        if item.exists():
            roots.append(item)
    return roots


def default_local_scan_roots() -> List[Path]:
    home = Path.home()
    system = platform.system().lower()
    candidates = [home, home / "Desktop", home / "Documents", home / "Downloads"]
    if system == "windows":
        for env_name in ["PROGRAMDATA", "APPDATA", "LOCALAPPDATA", "PUBLIC", "TEMP"]:
            value = os.getenv(env_name)
            if value:
                candidates.append(Path(value))
    elif system == "darwin":
        candidates.extend([Path("/Applications"), Path("/Library/LaunchAgents"), Path("/Library/LaunchDaemons")])
    else:
        candidates.extend([Path("/etc"), Path("/opt"), Path("/usr/local/bin"), Path("/tmp")])
    deduped = []
    seen = set()
    for c in candidates:
        try:
            s = str(c.resolve()) if c.exists() else str(c)
        except Exception:
            s = str(c)
        if s not in seen and c.exists():
            seen.add(s)
            deduped.append(c)
    return deduped


def should_skip_dir(path: Path) -> bool:
    name = path.name
    if name in SKIP_DIR_NAMES:
        return True
    lower = str(path).lower()
    if any(token.lower() in lower for token in ["/proc/", "/sys/", "/dev/"]):
        return True
    return False


def detect_miner_filename(path: Path, indicators: IndicatorSet) -> List[str]:
    findings = []
    name = path.name.lower()
    normalized = normalize_name(name)
    for keyword in indicators.filenames:
        k = keyword.lower()
        if k in name or normalize_name(k) in normalized:
            findings.append(f"filename matched miner keyword: {keyword}")
    return findings


def detect_disable_patterns(text: str) -> List[Tuple[str, str]]:
    matches = []
    tables = [
        ("windows_defender_disable_code", WINDOWS_DEFENDER_PATTERNS),
        ("windows_firewall_disable_code", WINDOWS_FIREWALL_PATTERNS),
        ("linux_firewall_disable_code", LINUX_FIREWALL_PATTERNS),
        ("macos_firewall_disable_code", MAC_FIREWALL_PATTERNS),
    ]
    for category, patterns in tables:
        for pattern in patterns:
            if re.search(pattern, text, flags=re.IGNORECASE):
                matches.append((category, pattern))
    return matches


def detect_content_matches(text: str, indicators: IndicatorSet) -> List[str]:
    out = []
    text_lower = text.lower()
    for domain in indicators.websites:
        if domain in text_lower:
            out.append(f"content matched mining pool domain: {domain}")
    for ip in indicators.ips:
        if ip in text:
            out.append(f"content matched mining pool IP: {ip}")
    for hint in MINING_CONTENT_HINTS:
        if hint in text_lower:
            out.append(f"content matched mining hint: {hint}")
    for port in indicators.ports:
        if re.search(rf"(?<!\d){port}(?!\d)", text):
            out.append(f"content referenced mining port: {port}")
    return out


def make_finding_id(prefix: str, value: str) -> str:
    digest = hashlib.sha1(value.encode("utf-8", errors="ignore")).hexdigest()[:12]
    return f"{prefix}-{digest}"


def scan_files(category: str, roots: Sequence[Path], indicators: IndicatorSet) -> List[Finding]:
    results: List[Finding] = []
    for root in roots:
        if not root.exists():
            continue
        for current_root, dirnames, filenames in os.walk(root, topdown=True):
            current_path = Path(current_root)
            dirnames[:] = [d for d in dirnames if not should_skip_dir(current_path / d)]
            for name in filenames:
                path = current_path / name
                try:
                    if path.stat().st_size > DEFAULT_MAX_BYTES:
                        continue
                except Exception:
                    continue

                evidence = detect_miner_filename(path, indicators)
                text = ""
                suffix = path.suffix.lower()
                if suffix in TEXT_EXTS or evidence:
                    text = safe_read_text(path)
                    evidence.extend(detect_content_matches(text, indicators))
                    for disable_category, rule in detect_disable_patterns(text):
                        results.append(
                            Finding(
                                id=make_finding_id("FILE", f"{path}:{disable_category}:{rule}"),
                                category=disable_category,
                                severity="high",
                                source=category,
                                path=str(path),
                                rule=rule,
                                evidence=["disable pattern matched in file content"],
                                sha256=sha256_file(path),
                            )
                        )
                if evidence:
                    results.append(
                        Finding(
                            id=make_finding_id("FILE", str(path)),
                            category="suspected_mining_file",
                            severity="high" if any("filename matched" in e for e in evidence) else "medium",
                            source=category,
                            path=str(path),
                            rule="keyword_or_content_match",
                            evidence=sorted(set(evidence))[:12],
                            sha256=sha256_file(path),
                        )
                    )
    return dedupe_findings(results)


def process_matches(proc_name: str, exe: str, cmdline: str, indicators: IndicatorSet) -> List[str]:
    evidence = []
    joined = " ".join([proc_name, exe, cmdline]).lower()
    normalized = normalize_name(joined)
    for keyword in indicators.filenames:
        if keyword in joined or normalize_name(keyword) in normalized:
            evidence.append(f"process matched miner keyword: {keyword}")
    for domain in indicators.websites:
        if domain in joined:
            evidence.append(f"process referenced mining domain: {domain}")
    if "stratum+tcp" in joined or "stratum+ssl" in joined:
        evidence.append("process referenced stratum protocol")
    for _, rule in detect_disable_patterns(joined):
        evidence.append(f"process commandline matched disable pattern: {rule}")
    return evidence


def scan_processes(indicators: IndicatorSet) -> List[Finding]:
    if psutil is None:
        return []
    results: List[Finding] = []
    for proc in psutil.process_iter(["pid", "name", "exe", "cmdline"]):
        try:
            info = proc.info
            pid = int(info.get("pid") or 0)
            name = info.get("name") or ""
            exe = info.get("exe") or ""
            cmdline_list = info.get("cmdline") or []
            cmdline = " ".join(cmdline_list) if isinstance(cmdline_list, list) else str(cmdline_list)
            evidence = process_matches(name, exe, cmdline, indicators)
            remote_hits = []
            try:
                conns = proc.net_connections(kind="inet")
            except Exception:
                conns = []
            for conn in conns:
                raddr = getattr(conn, "raddr", None)
                if not raddr:
                    continue
                remote_ip = getattr(raddr, "ip", None) or (raddr[0] if isinstance(raddr, tuple) and len(raddr) >= 1 else None)
                remote_port = getattr(raddr, "port", None) or (raddr[1] if isinstance(raddr, tuple) and len(raddr) >= 2 else None)
                hit = False
                if remote_ip and remote_ip in indicators.ips:
                    evidence.append(f"connected to mining pool IP: {remote_ip}")
                    hit = True
                if remote_port and int(remote_port) in indicators.ports:
                    evidence.append(f"connected to mining pool port: {remote_port}")
                    hit = True
                if hit:
                    remote_hits.append((remote_ip, int(remote_port) if remote_port else None))
            if evidence:
                if remote_hits:
                    for remote_ip, remote_port in remote_hits:
                        results.append(
                            Finding(
                                id=make_finding_id("PROC", f"{pid}:{remote_ip}:{remote_port}"),
                                category="suspected_mining_process",
                                severity="critical" if remote_ip or remote_port else "high",
                                source="processes",
                                pid=pid,
                                process_name=name or Path(exe).name,
                                path=exe or None,
                                remote_ip=remote_ip,
                                remote_port=remote_port,
                                rule="process_keyword_and_network_match",
                                evidence=sorted(set(evidence))[:12],
                            )
                        )
                else:
                    category = "security_disabling_process" if any("disable pattern" in e for e in evidence) else "suspected_mining_process"
                    results.append(
                        Finding(
                            id=make_finding_id("PROC", f"{pid}:{exe}:{cmdline}"),
                            category=category,
                            severity="high",
                            source="processes",
                            pid=pid,
                            process_name=name or Path(exe).name,
                            path=exe or None,
                            rule="process_keyword_match",
                            evidence=sorted(set(evidence))[:12],
                        )
                    )
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
        except Exception:
            continue
    return dedupe_findings(results)


def probe_security_status() -> Dict[str, object]:
    system = platform.system().lower()
    status: Dict[str, object] = {"platform": system}

    if system == "windows":
        status["defender"] = run_command([
            "powershell", "-NoProfile", "-Command", "(Get-MpPreference).DisableRealtimeMonitoring"
        ])
        status["firewall"] = run_command([
            "powershell", "-NoProfile", "-Command", "Get-NetFirewallProfile | Select Name,Enabled | ConvertTo-Json -Compress"
        ])
    elif system == "linux":
        status["ufw"] = run_command(["bash", "-lc", "command -v ufw >/dev/null 2>&1 && ufw status || true"])
        status["firewalld"] = run_command(["bash", "-lc", "command -v firewall-cmd >/dev/null 2>&1 && firewall-cmd --state || true"])
    elif system == "darwin":
        status["application_firewall"] = run_command([
            "bash", "-lc", "/usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate 2>/dev/null || true"
        ])
        status["pf"] = run_command(["bash", "-lc", "pfctl -s info 2>/dev/null || true"])

    return status


def run_command(cmd: Sequence[str]) -> Dict[str, object]:
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
        return {
            "cmd": list(cmd),
            "returncode": proc.returncode,
            "stdout": proc.stdout.strip(),
            "stderr": proc.stderr.strip(),
        }
    except Exception as exc:
        return {"cmd": list(cmd), "error": str(exc)}


def dedupe_findings(items: List[Finding]) -> List[Finding]:
    out = []
    seen = set()
    for item in items:
        key = (item.category, item.source, item.path, item.pid, item.remote_ip, item.remote_port, tuple(item.evidence))
        if key in seen:
            continue
        seen.add(key)
        out.append(item)
    return out


def write_report(report: Dict[str, object]) -> Tuple[Path, Path]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    json_path = OUTPUT_DIR / f"hunterminer_report_{stamp}.json"
    md_path = OUTPUT_DIR / f"hunterminer_report_{stamp}.md"
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(render_markdown_report(report), encoding="utf-8")
    latest_json = OUTPUT_DIR / "latest_report.json"
    latest_md = OUTPUT_DIR / "latest_report.md"
    shutil.copy2(json_path, latest_json)
    shutil.copy2(md_path, latest_md)
    return json_path, md_path


def render_markdown_report(report: Dict[str, object]) -> str:
    lines = []
    lines.append(f"# HunterMiner Scan Report")
    lines.append("")
    meta = report.get("scan_meta", {})
    summary = report.get("summary", {})
    lines.append(f"- Time: {meta.get('scan_time')}")
    lines.append(f"- Platform: {meta.get('platform')}")
    lines.append(f"- User ID: {meta.get('user_id')}")
    lines.append(f"- Billing charged: {meta.get('billing_charged')}")
    lines.append(f"- Total findings: {summary.get('total_findings', 0)}")
    lines.append("")
    for section in ["openclaw_skills", "local_disk", "processes", "security_disable_code"]:
        findings = report.get("findings", {}).get(section, [])
        lines.append(f"## {section}")
        if not findings:
            lines.append("No findings.")
            lines.append("")
            continue
        for item in findings:
            lines.append(f"- [{item['severity']}] {item['id']} :: {item['category']}")
            if item.get("path"):
                lines.append(f"  - path: {item['path']}")
            if item.get("pid"):
                lines.append(f"  - pid: {item['pid']}")
            if item.get("process_name"):
                lines.append(f"  - process: {item['process_name']}")
            if item.get("remote_ip") or item.get("remote_port"):
                lines.append(f"  - remote: {item.get('remote_ip')}:{item.get('remote_port')}")
            for e in item.get("evidence", []):
                lines.append(f"  - evidence: {e}")
        lines.append("")
    lines.append("## protection_status")
    lines.append("```json")
    lines.append(json.dumps(report.get("protection_status", {}), ensure_ascii=False, indent=2))
    lines.append("```")
    return "\n".join(lines)


def build_report(findings_skills: List[Finding], findings_disk: List[Finding], findings_proc: List[Finding], security_findings: List[Finding], user_id: str, billing_info: Dict[str, object], scanned_roots: Dict[str, List[str]]) -> Dict[str, object]:
    all_findings = findings_skills + findings_disk + findings_proc + security_findings
    severity_counts: Dict[str, int] = {}
    for item in all_findings:
        severity_counts[item.severity] = severity_counts.get(item.severity, 0) + 1
    report = {
        "scan_meta": {
            "software": CONFIG.get("software_name", "HunterMiner"),
            "scan_time": now_iso(),
            "platform": platform.platform(),
            "user_id": user_id,
            "billing_charged": billing_info.get("ok", False),
            "billing_balance": billing_info.get("balance"),
            "scan_price_usdt": CONFIG.get("scan_price_usdt", 0.1),
            "scanned_roots": scanned_roots,
        },
        "findings": {
            "openclaw_skills": [asdict(x) for x in findings_skills],
            "local_disk": [asdict(x) for x in findings_disk],
            "processes": [asdict(x) for x in findings_proc],
            "security_disable_code": [asdict(x) for x in security_findings],
        },
        "summary": {
            "total_findings": len(all_findings),
            "severity_counts": severity_counts,
        },
        "protection_status": probe_security_status(),
    }
    return report


def split_security_findings(items: List[Finding]) -> Tuple[List[Finding], List[Finding]]:
    normal = []
    security = []
    for item in items:
        if "disable_code" in item.category or item.category == "security_disabling_process":
            security.append(item)
        else:
            normal.append(item)
    return normal, security


def _resolve_one_domain(domain: str) -> Set[str]:
    found = set()
    try:
        infos = socket.getaddrinfo(domain, None, proto=socket.IPPROTO_TCP)
    except Exception:
        return found
    for info in infos:
        sockaddr = info[4]
        if sockaddr and sockaddr[0]:
            found.add(sockaddr[0])
    return found


def resolve_domain_ips(domains: Iterable[str]) -> Set[str]:
    resolved = set()
    domain_list = list(domains)
    if not domain_list:
        return resolved
    workers = min(8, max(1, len(domain_list)))
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(_resolve_one_domain, domain): domain for domain in domain_list}
        for future in as_completed(futures, timeout=max(5, len(domain_list) * 1.5)):
            try:
                resolved.update(future.result(timeout=0.5))
            except Exception:
                continue
    return resolved


def fetch_remote_lines(url: str) -> List[str]:
    import requests

    try:
        resp = requests.get(url, timeout=20)
        resp.raise_for_status()
        lines = []
        for line in resp.text.splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                lines.append(line)
        return lines
    except Exception:
        return []


def update_databases() -> Dict[str, object]:
    indicators = load_indicators()
    summary: Dict[str, object] = {"updated": [], "counts_before": {}, "counts_after": {}}
    summary["counts_before"] = {
        "websites": len(indicators.websites),
        "filenames": len(indicators.filenames),
        "ips": len(indicators.ips),
        "ports": len(indicators.ports),
    }

    remote_sources_path = INDICATORS_DIR / "remote_sources.json"
    remote_sources = {}
    if remote_sources_path.exists():
        try:
            remote_sources = json.loads(remote_sources_path.read_text(encoding="utf-8"))
        except Exception:
            remote_sources = {}

    websites = set(indicators.websites)
    filenames = set(indicators.filenames)
    ips = set(indicators.ips)
    ports = {str(p) for p in indicators.ports}

    for url in remote_sources.get("websites", []):
        websites.update(v.lower() for v in fetch_remote_lines(url))
    for url in remote_sources.get("filenames", []):
        filenames.update(v.lower() for v in fetch_remote_lines(url))
    for url in remote_sources.get("ips", []):
        ips.update(fetch_remote_lines(url))
    for url in remote_sources.get("ports", []):
        ports.update(fetch_remote_lines(url))

    resolved_ips = resolve_domain_ips(websites)
    ips.update(resolved_ips)

    (INDICATORS_DIR / "mining_pool_websites.txt").write_text("\n".join(sorted(websites)) + "\n", encoding="utf-8")
    (INDICATORS_DIR / "mining_software_filenames.txt").write_text("\n".join(sorted(filenames)) + "\n", encoding="utf-8")
    (INDICATORS_DIR / "mining_pool_public_ips.txt").write_text("\n".join(sorted(ips)) + "\n", encoding="utf-8")
    clean_ports = sorted({str(int(p)) for p in ports if str(p).isdigit()}, key=lambda x: int(x))
    (INDICATORS_DIR / "mining_pool_ports.txt").write_text("\n".join(clean_ports) + "\n", encoding="utf-8")

    summary["counts_after"] = {
        "websites": len(websites),
        "filenames": len(filenames),
        "ips": len(ips),
        "ports": len(clean_ports),
    }
    summary["updated"] = [
        str(INDICATORS_DIR / "mining_pool_websites.txt"),
        str(INDICATORS_DIR / "mining_software_filenames.txt"),
        str(INDICATORS_DIR / "mining_pool_public_ips.txt"),
        str(INDICATORS_DIR / "mining_pool_ports.txt"),
    ]
    return summary


def load_report(path: Path) -> Dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def find_item_by_id(report: Dict[str, object], finding_id: str) -> Optional[Dict[str, object]]:
    for section in report.get("findings", {}).values():
        for item in section:
            if item.get("id") == finding_id:
                return item
    return None


def remediate(report_path: Path, finding_ids: List[str], action: str, yes: bool) -> Dict[str, object]:
    report = load_report(report_path)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    QUARANTINE_DIR.mkdir(parents=True, exist_ok=True)
    changes = []
    for fid in finding_ids:
        item = find_item_by_id(report, fid)
        if not item:
            changes.append({"id": fid, "status": "not_found"})
            continue
        if item.get("pid"):
            pid = int(item["pid"])
            if yes:
                try:
                    if psutil is None:
                        raise RuntimeError("psutil not installed")
                    proc = psutil.Process(pid)
                    proc.terminate()
                    changes.append({"id": fid, "status": "terminated_process", "pid": pid})
                except Exception as exc:
                    changes.append({"id": fid, "status": "process_error", "pid": pid, "error": str(exc)})
            else:
                changes.append({"id": fid, "status": "dry_run_process", "pid": pid})
        if item.get("path"):
            path = Path(item["path"])
            if not path.exists():
                changes.append({"id": fid, "status": "path_missing", "path": str(path)})
                continue
            if yes:
                try:
                    if action == "delete":
                        if path.is_dir():
                            shutil.rmtree(path)
                        else:
                            path.unlink()
                        changes.append({"id": fid, "status": "deleted", "path": str(path)})
                    else:
                        target = QUARANTINE_DIR / f"{int(time.time())}_{path.name}"
                        shutil.move(str(path), str(target))
                        changes.append({"id": fid, "status": "quarantined", "path": str(path), "target": str(target)})
                except Exception as exc:
                    changes.append({"id": fid, "status": "path_error", "path": str(path), "error": str(exc)})
            else:
                changes.append({"id": fid, "status": "dry_run_path", "path": str(path), "action": action})
    out = {
        "time": now_iso(),
        "report": str(report_path),
        "action": action,
        "confirmed": yes,
        "changes": changes,
        "recommendation": "After confirmed cleanup, restart the computer.",
    }
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    remediation_path = OUTPUT_DIR / f"hunterminer_remediation_{stamp}.json"
    remediation_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    out["output"] = str(remediation_path)
    return out


def get_payment_url(user_id: str, amount: Optional[float] = None) -> str:
    client = BillingClient(BASE_DIR)
    final_amount = float(amount) if amount is not None else float(CONFIG.get("payment_link_default_amount_usdt", 5.0))
    return client.get_payment_link(user_id, final_amount)


def do_scan(user_id: str, roots: List[Path], skill_roots: List[Path], skip_billing: bool) -> Dict[str, object]:
    indicators = load_indicators()
    billing_info: Dict[str, object]
    if skip_billing:
        billing_info = {"ok": False, "balance": None, "skipped": True}
    else:
        client = BillingClient(BASE_DIR)
        billing_info = client.charge_user(user_id)
        if not billing_info.get("ok"):
            payment_url = billing_info.get("payment_url")
            message = "余额不足，请使用返回的支付链接充值后再试"
            return {
                "ok": False,
                "mode": "PAYMENT_URL_ONLY",
                "message": message,
                "payment_url": payment_url,
                "payment_url_raw": payment_url,
                "balance": billing_info.get("balance"),
            }

    findings_skills_raw = scan_files("openclaw_skills", skill_roots, indicators)
    findings_disk_raw = scan_files("local_disk", roots, indicators)
    findings_proc_raw = scan_processes(indicators)

    findings_skills, sec1 = split_security_findings(findings_skills_raw)
    findings_disk, sec2 = split_security_findings(findings_disk_raw)
    findings_proc, sec3 = split_security_findings(findings_proc_raw)
    security_findings = dedupe_findings(sec1 + sec2 + sec3)

    scanned_roots = {
        "openclaw_skills": [str(p) for p in skill_roots],
        "local_disk": [str(p) for p in roots],
    }
    report = build_report(findings_skills, findings_disk, findings_proc, security_findings, user_id, billing_info, scanned_roots)
    json_path, md_path = write_report(report)
    return {
        "ok": True,
        "json_report": str(json_path),
        "markdown_report": str(md_path),
        "summary": report["summary"],
        "billing": billing_info,
    }


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="HunterMiner - cross-platform miner scanner for OpenClaw")
    sub = parser.add_subparsers(dest="command", required=True)

    scan = sub.add_parser("scan", help="Run a billed scan")
    scan.add_argument("--user-id", required=True, help="Billing user ID")
    scan.add_argument("--root", action="append", default=[], help="Extra local scan root")
    scan.add_argument("--skill-root", action="append", default=[], help="Extra OpenClaw skills root")
    scan.add_argument("--skip-billing", action="store_true", help="Debug only: skip billing")

    pay = sub.add_parser("payment-link", help="Generate a raw payment URL only")
    pay.add_argument("--user-id", required=True, help="Billing user ID")
    pay.add_argument("--amount", type=float, default=None, help="Optional top-up amount in USDT")

    update = sub.add_parser("update-db", help="Update local indicator databases without charging")

    remed = sub.add_parser("remediate", help="Terminate/quarantine/delete selected findings")
    remed.add_argument("--report", default=str(OUTPUT_DIR / "latest_report.json"), help="Report JSON path")
    remed.add_argument("--finding-id", action="append", required=True, help="Finding ID to process")
    remed.add_argument("--action", choices=["quarantine", "delete"], default="quarantine")
    remed.add_argument("--yes", action="store_true", help="Actually apply changes")

    latest = sub.add_parser("show-latest", help="Print latest report path")

    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)
    try:
        if args.command == "update-db":
            result = update_databases()
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 0
        if args.command == "payment-link":
            print(get_payment_url(args.user_id, args.amount))
            return 0
        if args.command == "scan":
            roots = ([Path(x) for x in (args.root or []) if Path(x).exists()] or default_local_scan_roots())
            skill_roots = ([Path(x) for x in (args.skill_root or []) if Path(x).exists()] or default_openclaw_skill_roots())
            result = do_scan(args.user_id, roots, skill_roots, args.skip_billing)
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 0 if result.get("ok") else 2
        if args.command == "remediate":
            result = remediate(Path(args.report), args.finding_id, args.action, args.yes)
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 0
        if args.command == "show-latest":
            print(json.dumps({
                "json_report": str(OUTPUT_DIR / "latest_report.json"),
                "markdown_report": str(OUTPUT_DIR / "latest_report.md")
            }, ensure_ascii=False, indent=2))
            return 0
        return 1
    except BillingError as exc:
        print(json.dumps({
            "ok": False,
            "message": str(exc)
        }, ensure_ascii=False, indent=2), file=sys.stderr)
        return 3
    except KeyboardInterrupt:
        return 130
    except Exception as exc:
        print(json.dumps({"ok": False, "message": str(exc)}, ensure_ascii=False, indent=2), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
