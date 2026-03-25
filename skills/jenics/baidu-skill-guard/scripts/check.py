#!/usr/bin/env python3
"""Skill security check CLI tool — Python 3.9+ (stdlib only)."""

import argparse
import hashlib
import json
import os
import re
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

# ============================================================
# Configuration
# ============================================================

API_BASE_URL = 'https://skill-sec.baidu.com'
API_PATH = '/v1/skill/security/results'
REQUEST_TIMEOUT = 10  # 10s
CONCURRENT_LIMIT = 5

SCAN_API_PATH = '/v1/skill/security/scan'
POLL_TIMEOUT = 10 * 60  # 10 minutes
FIRST_POLL_INTERVAL = 1  # 1s
NORMAL_POLL_INTERVAL = 5  # 5s

UPLOAD_API_PATH = '/v1/skill/security/upload'
UPLOAD_TIMEOUT = 60  # 60s

# ============================================================
# Utilities
# ============================================================

_ssl_ctx = ssl.create_default_context()


def safe_json_parse(text):
    """Parse JSON text safely, raising a descriptive error on failure."""
    try:
        return json.loads(text)
    except (json.JSONDecodeError, ValueError):
        raise Exception(f'响应解析失败（非JSON格式）: {text[:200]}')


def make_query_full_result(code, msg, **overrides):
    """Build a standard queryfull result dict with default counters."""
    result = {
        'code': code,
        'msg': msg,
        'ts': int(time.time() * 1000),
        'total': 0,
        'safe_count': 0,
        'danger_count': 0,
        'caution_count': 0,
        'error_count': 0,
        'results': [],
    }
    result.update(overrides)
    return result


def output_and_exit(obj, exit_code):
    """Print JSON object to stdout and exit with the given code."""
    print(json.dumps(obj, indent=2, ensure_ascii=False))
    sys.exit(exit_code)


# ============================================================
# Report Builder
# ============================================================

_SOURCE_MAP = {
    'openclaw': 'ClawdHub',
    'github': 'GitHub',
    'appbuilder': '百度AppBuilder',
}

_CONFIDENCE_MAP = {
    'safe': {
        'verdict': '✅ 白名单(可信)',
        'final_verdict': '✅ 安全安装',
        'suggestion': '已通过安全检查，可安全安装',
    },
    'caution': {
        'verdict': '⚠️ 灰名单，谨慎安装',
        'final_verdict': '⚠️ 谨慎安装(需人工确认)',
        'suggestion': '存在潜在风险，建议人工审查后再安装',
    },
    'dangerous': {
        'verdict': '🚫 黑名单，❌ 不建议安装',
        'final_verdict': '❌ 不建议安装(需人工确认)',
        'suggestion': '发现严重安全风险，建议人工审查后再安装',
    },
}

_CONFIDENCE_DEFAULT = {
    'verdict': '❓ 未收录，不建议安装',
    'final_verdict': '❌ 不建议安装(需人工确认)',
    'suggestion': '尚未被安全系统收录，建议人工审查后再安装'
}


def _format_timestamp(ms):
    """Convert millisecond timestamp to formatted string."""
    if not ms:
        return '未知'
    import datetime
    dt = datetime.datetime.fromtimestamp(ms / 1000)
    return dt.strftime('%Y-%m-%d %H:%M:%S')


def _build_overview(confidence, findings_count, virus_count):
    """Build the overview text based on confidence level."""
    if confidence == 'safe':
        return None
    if confidence == 'dangerous':
        text = '🚫 Skill存在安全风险'
        if findings_count > 0:
            text += f'，发现{findings_count}项危险行为'
        if virus_count > 0:
            text += f'，发现{virus_count}项病毒风险'
    elif confidence == 'caution':
        text = '⚠️ Skill存在信誉风险'
        if findings_count > 0:
            text += f'，发现{findings_count}项可疑行为'
    else:
        text = '❓ Skill未收录'
    return text


def build_report(data):
    """Build a pre-processed report object from data[0] for the LLM template."""
    if not isinstance(data, list) or len(data) == 0:
        return None

    item = data[0]
    detail = item.get('detail') or {}
    confidence = (item.get('bd_confidence') or '').lower()
    mapped = _CONFIDENCE_MAP.get(confidence, _CONFIDENCE_DEFAULT)

    github = detail.get('github') or {}
    vt = detail.get('virustotal') or {}
    oc = detail.get('openclaw') or {}
    scanner = detail.get('skillscanner') or {}
    av = detail.get('antivirus') or {}

    vt_status = vt.get('vt_status')
    vt_describe = None
    if vt_status and vt_status != 'Benign' and vt_status != 'Pending' and vt.get('vt_describe'):
        vt_describe = vt['vt_describe']

    oc_status = oc.get('oc_status')
    oc_describe = oc.get('oc_describe') if (oc_status and oc_status != 'Benign') else None

    raw_findings = scanner.get('findings') or []
    findings = [
        {'severity': f.get('severity'), 'title': f.get('title'), 'description': f.get('description')}
        for f in raw_findings
    ]

    findings_count = scanner.get('findings_count') or len(findings)
    virus_count = av.get('virus_count') or 0
    virus_list = []
    if virus_count > 0 and isinstance(av.get('virus_details'), list):
        virus_list = [
            {'virus_name': v.get('virus_name'), 'file': v.get('file')}
            for v in av['virus_details']
        ]

    return {
        'name': item.get('slug'),
        'version': item.get('version'),
        'source': _SOURCE_MAP.get(item.get('source'), '其他'),
        'author': github.get('name'),
        'scanned_at': _format_timestamp(item.get('scanned_at')),
        'bd_confidence': confidence or None,
        'verdict': mapped['verdict'],
        'final_verdict': mapped['final_verdict'],
        'suggestion': mapped['suggestion'],
        'bd_describe': item.get('bd_describe'),
        'overview': _build_overview(confidence, findings_count, virus_count),
        'virustotal': {'status': vt_status, 'describe': vt_describe},
        'openclaw': {'status': oc_status, 'describe': oc_describe},
        'findings': findings,
        'antivirus': {'virus_count': virus_count, 'virus_list': virus_list},
    }


# ============================================================
# HTTP Client
# ============================================================

def make_request(url, timeout=REQUEST_TIMEOUT):
    """Send a GET request and return parsed JSON."""
    req = urllib.request.Request(url, method='GET')
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=_ssl_ctx) as resp:
            data = resp.read().decode('utf-8')
            return safe_json_parse(data)
    except urllib.error.HTTPError as e:
        body = ''
        try:
            body = e.read().decode('utf-8')[:200]
        except Exception:
            pass
        raise Exception(f'HTTP {e.code}: {body}')
    except urllib.error.URLError as e:
        raise Exception(f'请求失败: {e.reason}')


def make_request_with_body(url, body_dict, timeout=REQUEST_TIMEOUT):
    """Send a POST request with JSON body and return parsed JSON."""
    data = json.dumps(body_dict).encode('utf-8')
    req = urllib.request.Request(
        url, data=data, method='POST',
        headers={'Content-Type': 'application/json'},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=_ssl_ctx) as resp:
            resp_data = resp.read().decode('utf-8')
            return safe_json_parse(resp_data)
    except urllib.error.HTTPError as e:
        body = ''
        try:
            body = e.read().decode('utf-8')[:200]
        except Exception:
            pass
        raise Exception(f'HTTP {e.code}: {body}')
    except urllib.error.URLError as e:
        raise Exception(f'请求失败: {e.reason}')


# ============================================================
# API: checkSkillSecurityFullResponse
# ============================================================

def check_skill_security_full_response(slug, version=None):
    """Query the security API for a skill by slug and optional version."""
    params = {'slug': slug}
    if version:
        params['version'] = version
    query_string = urllib.parse.urlencode(params)
    url = f'{API_BASE_URL}{API_PATH}?{query_string}'
    return make_request(url)


# ============================================================
# API: URL Scan (submit + poll)
# ============================================================

def submit_scan_task(source_url):
    """Submit a URL scan task and return the API response."""
    url = f'{API_BASE_URL}{SCAN_API_PATH}'
    return make_request_with_body(url, {'source_url': source_url})


def poll_scan_task_status(task_id):
    """Poll a scan task until it completes or times out."""
    start_time = time.time()
    poll_count = 0
    last_status = 'pending'

    while True:
        if poll_count == 0:
            wait_time = FIRST_POLL_INTERVAL
        elif poll_count == 1:
            wait_time = 3
        else:
            wait_time = NORMAL_POLL_INTERVAL
        time.sleep(wait_time)

        if time.time() - start_time > POLL_TIMEOUT:
            raise Exception('扫描任务超时（超过10分钟未完成）')

        poll_count += 1
        elapsed = int(time.time() - start_time)
        print(f'[polling] 第{poll_count}次轮询，已等待{elapsed}s，当前状态: {last_status}', file=sys.stderr)

        encoded_id = urllib.parse.quote(task_id, safe='')
        url = f'{API_BASE_URL}{SCAN_API_PATH}/{encoded_id}'
        response = make_request(url)

        data = response.get('data') or {}
        if data.get('status') == 'done':
            return response
        if data.get('status') == 'failed':
            raise Exception(data.get('error_message', '扫描任务失败'))
        if data.get('status'):
            last_status = data['status']
        # pending / processing -> continue polling


def convert_scan_result_to_slug_format(poll_response):
    """Convert a poll response into the standard slug query format."""
    data = poll_response.get('data') or {}
    results = data.get('results') or []
    if results:
        return {'code': 'success', 'data': results}
    return {'code': 'error', 'msg': '扫描完成但无结果数据', 'data': []}


# ============================================================
# Slug Extraction from SKILL.md
# ============================================================

def extract_slug_from_skill_md(dir_path):
    """Extract skill slug and version from _meta.json (preferred) or SKILL.md front-matter."""
    fallback_slug = os.path.basename(dir_path)

    # Step 1: 尝试从 _meta.json 读取
    meta_json_path = os.path.join(dir_path, '_meta.json')
    if os.path.isfile(meta_json_path):
        try:
            with open(meta_json_path, 'r', encoding='utf-8') as f:
                meta = json.load(f)
            if meta.get('slug'):
                return meta['slug'], meta.get('version') or None
        except Exception:
            pass  # _meta.json 解析失败，继续回退

    # Step 2: 回退 - slug使用目录名，从SKILL.md提取version
    skill_md_path = os.path.join(dir_path, 'SKILL.md')
    if not os.path.isfile(skill_md_path):
        return fallback_slug, None

    with open(skill_md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    fm_match = re.match(r'^---\r?\n([\s\S]*?)\r?\n---', content)
    if not fm_match:
        return fallback_slug, None

    fm = fm_match.group(1)
    version_match = re.search(r'^version:\s*(.+)$', fm, re.MULTILINE)
    version = version_match.group(1).strip() if version_match else None
    # 若顶层未找到，尝试 metadata.version
    if not version:
        meta_version_match = re.search(
            r'^metadata:\s*\r?\n(?:[ \t]+.*\r?\n)*?[ \t]+version:\s*(.+)$',
            fm, re.MULTILINE
        )
        if meta_version_match:
            version = meta_version_match.group(1).strip()
    if version and len(version) >= 2 and version[0] == version[-1] and version[0] in ('"', "'"):
        version = version[1:-1]
    return fallback_slug, version


# ============================================================
# Content SHA256 (directory-based, matches server-side algorithm)
# ============================================================

def compute_content_sha256(dir_path):
    """Compute content_sha256 for a skill directory, matching server-side algo."""
    # 1. Recursively collect all files (relative paths)
    files = []
    for root, dirs, filenames in os.walk(dir_path):
        dirs[:] = [d for d in dirs if d != '__MACOSX']
        for fname in filenames:
            abs_path = os.path.join(root, fname)
            rel = os.path.relpath(abs_path, dir_path)
            files.append(rel)

    # 2. Filter out top-level _meta.json, .clawhub/ directory and .DS_Store
    filtered = [
        f for f in files
        if f != '_meta.json'
        and not f.startswith('.clawhub' + os.sep)
        and not f.startswith('.clawhub/')
        and os.path.basename(f) != '.DS_Store'
    ]
    if not filtered:
        return ''

    # 3. Normalize paths and sort lexicographically
    normalized = []
    for f in filtered:
        p = f.replace('\\', '/')
        p = os.path.normpath(p).replace('\\', '/')
        p = p.lstrip('/')
        normalized.append(p)
    normalized.sort()

    # 4. Build manifest: "{relativePath}\n{fileSHA256}\n" for each file
    manifest = ''
    for rel in normalized:
        abs_path = os.path.join(dir_path, rel)
        h = hashlib.sha256()
        with open(abs_path, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                h.update(chunk)
        manifest += f'{rel}\n{h.hexdigest()}\n'

    # 5. SHA256 of the entire manifest
    return hashlib.sha256(manifest.encode('utf-8')).hexdigest()


# ============================================================
# API: check_skill_security_by_sha256
# ============================================================

def check_skill_security_by_sha256(sha256_val):
    """Query the security API for a skill by content SHA256."""
    query_string = urllib.parse.urlencode({'sha256': sha256_val})
    url = f'{API_BASE_URL}{API_PATH}?{query_string}'
    return make_request(url)


# ============================================================
# Upload ZIP fallback (create zip + multipart upload)
# ============================================================

def create_zip_buffer(dir_path):
    """Create a ZIP archive of the directory in memory and return bytes."""
    import io
    import zipfile

    buf = io.BytesIO()
    base_name = os.path.basename(dir_path)
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(dir_path):
            dirs[:] = [d for d in dirs if d != '__MACOSX']
            for fname in files:
                abs_path = os.path.join(root, fname)
                arc_name = os.path.join(
                    base_name,
                    os.path.relpath(abs_path, dir_path),
                )
                zf.write(abs_path, arc_name)
    return buf.getvalue()


def upload_skill_zip(zip_bytes, slug, version=None):
    """Upload a ZIP file via multipart/form-data to the upload API."""
    boundary = '----SkillGuard' + hashlib.sha256(
        os.urandom(16)
    ).hexdigest()[:32]

    parts = []

    # slug field
    if slug:
        parts.append(
            f'--{boundary}\r\n'
            f'Content-Disposition: form-data; name="slug"\r\n\r\n'
            f'{slug}\r\n'
        )

    # version field
    if version:
        parts.append(
            f'--{boundary}\r\n'
            f'Content-Disposition: form-data; name="version"\r\n\r\n'
            f'{version}\r\n'
        )

    # file field header
    file_name = (slug or 'skill') + '.zip'
    file_header = (
        f'--{boundary}\r\n'
        f'Content-Disposition: form-data; name="file";'
        f' filename="{file_name}"\r\n'
        f'Content-Type: application/zip\r\n\r\n'
    )
    ending = f'\r\n--{boundary}--\r\n'

    body = b''
    for p in parts:
        body += p.encode('utf-8')
    body += file_header.encode('utf-8')
    body += zip_bytes
    body += ending.encode('utf-8')

    url = f'{API_BASE_URL}{UPLOAD_API_PATH}'
    req = urllib.request.Request(url, data=body, method='POST')
    req.add_header(
        'Content-Type',
        f'multipart/form-data; boundary={boundary}',
    )
    req.add_header('Content-Length', str(len(body)))

    try:
        with urllib.request.urlopen(
            req, timeout=UPLOAD_TIMEOUT, context=_ssl_ctx
        ) as resp:
            resp_data = resp.read().decode('utf-8')
            return safe_json_parse(resp_data)
    except urllib.error.HTTPError as e:
        body_text = e.read().decode('utf-8', errors='replace')[:200]
        raise Exception(f'HTTP {e.code}: {body_text}')
    except urllib.error.URLError as e:
        raise Exception(f'请求失败: {e.reason}')


# ============================================================
# Concurrent execution with limit
# ============================================================

def parallel_limit(task_fns, limit):
    """Run callables concurrently (max *limit*) and return results in order."""
    results = [None] * len(task_fns)
    with ThreadPoolExecutor(max_workers=limit) as executor:
        future_to_index = {executor.submit(fn): i for i, fn in enumerate(task_fns)}
        for future in as_completed(future_to_index):
            idx = future_to_index[future]
            try:
                results[idx] = future.result()
            except Exception:
                results[idx] = {'__error': True}
    return results


# ============================================================
# QueryFull: Batch query all subdirectories by slug (Scenario C)
# ============================================================

def classify_confidence(response):
    """Classify a skill response into safe, dangerous, caution, or error."""
    if (response.get('code') == 'success'
            and isinstance(response.get('data'), list)
            and len(response['data']) > 0):
        c = (response['data'][0].get('bd_confidence') or '').lower()
        if c in ('safe', 'trusted'):
            return 'safe'
        if c == 'dangerous':
            return 'dangerous'
        if c == 'caution':
            return 'caution'
    return 'error'


def query_full_directory(dir_path):
    """Batch query security results for all skill subdirectories."""
    if not dir_path or not os.path.exists(dir_path):
        return make_query_full_result('error', f'❌ 错误：目录路径不存在 -- {dir_path or "(空)"}')

    if not os.path.isdir(dir_path):
        return make_query_full_result('error', f'❌ 错误：路径不是目录 -- {dir_path}')

    # List immediate subdirectories, skip hidden dirs
    entries = [
        name for name in sorted(os.listdir(dir_path))
        if not name.startswith('.') and name != '__MACOSX' and os.path.isdir(os.path.join(dir_path, name))
    ]

    if not entries:
        return make_query_full_result('success', 'queryfull completed, no skill subdirectories found')

    # Build task callables
    def make_task(name):
        def task():
            skill_dir = os.path.join(dir_path, name)
            slug, version = extract_slug_from_skill_md(skill_dir)
            try:
                response = check_skill_security_full_response(slug, version)
                result = {'slug': slug, **response}

                # SHA256 fallback: when slug query returns empty data, try content_sha256
                if (response.get('code') == 'success'
                        and isinstance(response.get('data'), list)
                        and len(response['data']) == 0):
                    try:
                        content_sha256 = compute_content_sha256(skill_dir)
                        if content_sha256:
                            sha256_resp = check_skill_security_by_sha256(content_sha256)
                            if (sha256_resp.get('code') == 'success'
                                    and isinstance(sha256_resp.get('data'), list)
                                    and len(sha256_resp['data']) > 0):
                                result = {'slug': slug, **sha256_resp}
                    except Exception:
                        pass  # SHA256 fallback failed, keep original empty result

                # Upload ZIP fallback: when SHA256 also returns empty
                if (result.get('code') == 'success'
                        and isinstance(result.get('data'), list)
                        and len(result['data']) == 0):
                    try:
                        print(
                            f'[upload-fallback] slug={slug}, uploading zip...',
                            file=sys.stderr,
                        )
                        zip_bytes = create_zip_buffer(skill_dir)
                        upload_resp = upload_skill_zip(zip_bytes, slug, version)
                        upload_data = upload_resp.get('data') or {}
                        if (upload_resp.get('code') == 'success'
                                and upload_data.get('task_id')):
                            task_id = upload_data['task_id']
                            print(
                                f'[upload-fallback] slug={slug},'
                                f' task_id={task_id}, polling...',
                                file=sys.stderr,
                            )
                            poll_resp = poll_scan_task_status(task_id)
                            converted = convert_scan_result_to_slug_format(
                                poll_resp
                            )
                            if (converted.get('code') == 'success'
                                    and isinstance(converted.get('data'), list)
                                    and len(converted['data']) > 0):
                                result = {'slug': slug, **converted}
                    except Exception as upload_err:
                        print(
                            f'[upload-fallback] slug={slug},'
                            f' error: {upload_err}',
                            file=sys.stderr,
                        )

                report = build_report(result.get('data'))
                if report:
                    result['report'] = report
                return result
            except Exception as e:
                return {'slug': slug, 'code': 'error', 'msg': str(e), 'data': []}
        return task

    task_fns = [make_task(name) for name in entries]
    results = parallel_limit(task_fns, CONCURRENT_LIMIT)

    # Classify results
    safe_count = 0
    danger_count = 0
    caution_count = 0
    error_count = 0
    for r in results:
        category = classify_confidence(r)
        if category == 'safe':
            safe_count += 1
        elif category == 'dangerous':
            danger_count += 1
        elif category == 'caution':
            caution_count += 1
        else:
            error_count += 1

    return make_query_full_result(
        'success', 'queryfull completed',
        total=len(entries),
        safe_count=safe_count,
        danger_count=danger_count,
        caution_count=caution_count,
        error_count=error_count,
        results=results,
    )


# ============================================================
# QuerySingle: Query one skill directory by slug (Scenario A2)
# ============================================================

def query_single_directory(dir_path):
    """Query security results for a single skill directory."""
    if not dir_path or not os.path.exists(dir_path):
        return {
            'code': 'error',
            'msg': f'❌ 错误：目录路径不存在 -- {dir_path or "(空)"}',
            'ts': int(time.time() * 1000),
            'data': [],
        }

    if not os.path.isdir(dir_path):
        return {
            'code': 'error',
            'msg': f'❌ 错误：路径不是目录 -- {dir_path}',
            'ts': int(time.time() * 1000),
            'data': [],
        }

    slug, version = extract_slug_from_skill_md(dir_path)

    try:
        response = check_skill_security_full_response(slug, version)
        result = {**response}

        # SHA256 fallback: when slug query returns empty data
        if (response.get('code') == 'success'
                and isinstance(response.get('data'), list)
                and len(response['data']) == 0):
            try:
                content_sha256 = compute_content_sha256(dir_path)
                print(
                    f'[sha256-fallback] slug={slug}, contentSha256='
                    f'{content_sha256 or "(empty)"}',
                    file=sys.stderr,
                )
                if content_sha256:
                    sha256_resp = check_skill_security_by_sha256(
                        content_sha256
                    )
                    data_len = (
                        len(sha256_resp['data'])
                        if isinstance(sha256_resp.get('data'), list)
                        else 'N/A'
                    )
                    print(
                        f'[sha256-fallback] slug={slug},'
                        f' sha256 query result: code={sha256_resp.get("code")},'
                        f' data.length={data_len}',
                        file=sys.stderr,
                    )
                    if (sha256_resp.get('code') == 'success'
                            and isinstance(sha256_resp.get('data'), list)
                            and len(sha256_resp['data']) > 0):
                        result = {**sha256_resp}
            except Exception as fallback_err:
                print(
                    f'[sha256-fallback] slug={slug},'
                    f' fallback error: {fallback_err}',
                    file=sys.stderr,
                )

        # Upload ZIP fallback: when SHA256 fallback also returns empty
        if (result.get('code') == 'success'
                and isinstance(result.get('data'), list)
                and len(result['data']) == 0):
            try:
                print(
                    f'[upload-fallback] slug={slug}, uploading zip...',
                    file=sys.stderr,
                )
                zip_bytes = create_zip_buffer(dir_path)
                upload_resp = upload_skill_zip(zip_bytes, slug, version)
                upload_data = upload_resp.get('data') or {}
                if (upload_resp.get('code') == 'success'
                        and upload_data.get('task_id')):
                    task_id = upload_data['task_id']
                    print(
                        f'[upload-fallback] slug={slug},'
                        f' task_id={task_id}, polling...',
                        file=sys.stderr,
                    )
                    poll_resp = poll_scan_task_status(task_id)
                    converted = convert_scan_result_to_slug_format(
                        poll_resp
                    )
                    if (converted.get('code') == 'success'
                            and isinstance(converted.get('data'), list)
                            and len(converted['data']) > 0):
                        result = {**converted}
            except Exception as upload_err:
                print(
                    f'[upload-fallback] slug={slug},'
                    f' error: {upload_err}',
                    file=sys.stderr,
                )

        report = build_report(result.get('data'))
        if report:
            result['report'] = report
        return result
    except Exception as error:
        return {
            'code': 'error',
            'msg': f'🚫 安全检查服务调用失败：{error}',
            'ts': int(time.time() * 1000),
            'data': [],
        }


# ============================================================
# CLI Entry Point
# ============================================================

def parse_args():
    """Parse and return command-line arguments."""
    parser = argparse.ArgumentParser(
        description='Skill security check CLI',
        add_help=False,
    )
    parser.add_argument('--slug', default=None)
    parser.add_argument('--version', default=None)
    parser.add_argument('--url', default=None)
    parser.add_argument('--action', default=None)
    parser.add_argument('--file', default=None)
    return parser.parse_args()


def main():
    """CLI entry point dispatching to url-scan, queryfull, or slug-query."""
    args = parse_args()

    if args.url:
        # URL scan flow: submit + poll
        try:
            submit_response = submit_scan_task(args.url)
            submit_data = submit_response.get('data') or {}
            if submit_response.get('code') != 'success' or not submit_data.get('task_id'):
                output_and_exit({
                    'code': 'error',
                    'msg': '扫描任务提交失败: ' + (
                        submit_response.get('message')
                        or submit_response.get('msg')
                        or '未知错误'
                    ),
                    'ts': int(time.time() * 1000),
                    'data': [],
                }, 1)

            task_id = submit_data['task_id']
            poll_response = poll_scan_task_status(task_id)
            response = convert_scan_result_to_slug_format(poll_response)
            report = build_report(response.get('data'))
            if report:
                response['report'] = report
            print(json.dumps(response, indent=2, ensure_ascii=False))

            if (response.get('code') == 'success'
                    and isinstance(response.get('data'), list)
                    and len(response['data']) > 0):
                bd_confidence = (response['data'][0].get('bd_confidence') or '').lower()
                safe = bd_confidence in ('safe', 'trusted')
                sys.exit(0 if safe else 1)
            else:
                sys.exit(1)
        except SystemExit:
            raise
        except Exception as error:
            output_and_exit({
                'code': 'error',
                'msg': f'🚫 安全检查服务调用失败：{error}',
                'ts': int(time.time() * 1000),
                'data': [],
            }, 1)

    elif args.action == 'queryfull':
        # Batch query all subdirectories by slug
        if not args.file:
            output_and_exit(make_query_full_result(
                'error',
                '❌ 错误：--action queryfull 需要提供 --file 参数（skills 父目录）\n'
                '用法：python3 check.py --action queryfull --file "/path/to/skills"',
            ), 1)

        response = query_full_directory(args.file)
        print(json.dumps(response, indent=2, ensure_ascii=False))

        # Exit code: 0 if all safe and total > 0, 1 otherwise
        all_safe = (
            response.get('code') == 'success'
            and response.get('total', 0) > 0
            and response.get('safe_count', 0) == response.get('total', 0)
        )
        sys.exit(0 if all_safe else 1)

    elif args.action == 'query':
        # Single directory query
        if not args.file:
            output_and_exit({
                'code': 'error',
                'msg': (
                    '❌ 错误：--action query 需要提供 --file 参数（skill 目录路径）\n'
                    '用法：python3 check.py --action query --file "/path/to/skill-dir"'
                ),
                'ts': int(time.time() * 1000),
                'data': [],
            }, 1)

        response = query_single_directory(args.file)
        print(json.dumps(response, indent=2, ensure_ascii=False))

        if (response.get('code') == 'success'
                and isinstance(response.get('data'), list)
                and len(response['data']) > 0):
            bd_confidence = (response['data'][0].get('bd_confidence') or '').lower()
            safe = bd_confidence in ('safe', 'trusted')
            sys.exit(0 if safe else 1)
        else:
            sys.exit(1)

    else:
        # Slug query flow
        if not args.slug:
            output_and_exit({
                'code': 'error',
                'msg': (
                    '❌ 错误：缺少必填参数 --slug 或 --url\n'
                    "用法：python3 check.py --slug 'skill-slug' [--version '1.0.0']\n"
                    "      python3 check.py --url 'https://example.com/skill'"
                ),
                'ts': int(time.time() * 1000),
                'data': [],
            }, 1)

        try:
            response = check_skill_security_full_response(args.slug, args.version)
            report = build_report(response.get('data'))
            if report:
                response['report'] = report
            print(json.dumps(response, indent=2, ensure_ascii=False))

            # Determine exit code based on bd_confidence
            if (response.get('code') == 'success'
                    and isinstance(response.get('data'), list)
                    and len(response['data']) > 0):
                item = response['data'][0]
                bd_confidence = (item.get('bd_confidence') or '').lower()
                safe = bd_confidence in ('safe', 'trusted')
                sys.exit(0 if safe else 1)
            else:
                sys.exit(1)
        except SystemExit:
            raise
        except Exception as error:
            output_and_exit({
                'code': 'error',
                'msg': f'🚫 安全检查服务调用失败：{error}',
                'ts': int(time.time() * 1000),
                'data': [],
            }, 1)


if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        raise
    except Exception as err:
        output_and_exit({
            'code': 'error',
            'msg': f'❌ 脚本执行异常：{err}',
            'ts': int(time.time() * 1000),
            'data': [],
        }, 1)
