#!/usr/bin/env python3
"""
LLM Proxy with Content Filtering - v3.1
- ThreadingHTTPServer 并发处理
- 线程安全 stats
- 请求 ID 追踪
- 日志缓冲
- 请求体大小限制
- 优雅关闭（signal handler）
- 信号量限流
"""

import json
import re
import time
import os
import sys
import signal
import traceback
import uuid
import threading
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import socket

# 配置
PROXY_PORT = int(os.environ.get("LLM_PROXY_PORT", 18888))
LOG_DIR = os.path.expanduser("~/.openclaw/logs/llm-proxy")
RULES_FILE = os.environ.get(
    "RULES_FILE",
    os.path.join(os.path.dirname(__file__), "content-filter-rules.json")
)

# 超时和限制
READ_TIMEOUT = 60       # 读取超时 60 秒（原 300 秒导致线程长时间阻塞）
MAX_BODY_SIZE = 10 * 1024 * 1024  # 最大请求体 10MB
LOG_PREVIEW_CHARS = 500  # 日志预览字符数
MAX_THREADS = 50        # 最大并发线程数

# 全局服务器引用，用于优雅关闭
server_instance = None
shutdown_event = threading.Event()

# Provider 映射
PROVIDERS = {
    "/bailian": "https://coding.dashscope.aliyuncs.com/v1",
    "/openrouter": "https://openrouter.ai/api/v1",
    "/nvd": "https://integrate.api.nvidia.com/v1",
}

# 线程安全的统计
class ThreadSafeStats:
    def __init__(self):
        self._lock = threading.Lock()
        self._data = {
            "total_requests": 0,
            "total_responses": 0,
            "blocked": 0,
            "warnings": 0,
            "errors": 0,
            "start_time": time.time()
        }
    
    def increment(self, key):
        with self._lock:
            self._data[key] += 1
    
    def get(self, key=None):
        with self._lock:
            if key:
                return self._data[key]
            return dict(self._data)
    
    def to_dict(self):
        with self._lock:
            return dict(self._data)

stats = ThreadSafeStats()

# 线程安全的日志写入
class LogWriter:
    def __init__(self, log_dir):
        self.log_dir = log_dir
        self._lock = threading.Lock()
        os.makedirs(log_dir, exist_ok=True)
    
    def _get_log_file(self):
        return os.path.join(self.log_dir, f"proxy-{datetime.now().strftime('%Y-%m-%d')}.jsonl")
    
    def write(self, entry):
        with self._lock:
            try:
                with open(self._get_log_file(), 'a') as f:
                    f.write(json.dumps(entry, ensure_ascii=False) + '\n')
            except Exception as e:
                print(f"[ERROR] 日志写入失败: {e}")

log_writer = LogWriter(LOG_DIR)

# 加载规则
def load_rules():
    try:
        with open(RULES_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"[WARN] 无法加载规则文件: {e}")
        return {"rules": [], "whitelist": []}

RULES = load_rules()

def check_content(content, rules):
    """分级审核：第一层恶意指令 + 第二层敏感内容"""
    alerts = []
    
    # 白名单检查
    for pattern in rules.get("whitelist", []):
        try:
            if re.search(pattern, content, re.IGNORECASE):
                return []
        except re.error:
            pass
    
    # 第一层：恶意指令检测
    layer1 = rules.get("layer1_malicious", {})
    if layer1.get("enabled", True):
        for rule in layer1.get("rules", []):
            for pattern in rule.get("patterns", []):
                try:
                    if re.search(pattern, content, re.IGNORECASE):
                        alerts.append({
                            "layer": "L1-恶意指令",
                            "rule_id": rule["id"],
                            "rule_name": rule["name"],
                            "severity": rule["severity"]
                        })
                        break
                except re.error:
                    pass
    
    # 第二层：敏感内容检测
    layer2 = rules.get("layer2_sensitive", {})
    if layer2.get("enabled", True):
        for rule in layer2.get("rules", []):
            for pattern in rule.get("patterns", []):
                try:
                    if re.search(pattern, content, re.IGNORECASE):
                        alerts.append({
                            "layer": "L2-敏感内容",
                            "rule_id": rule["id"],
                            "rule_name": rule["name"],
                            "severity": rule["severity"]
                        })
                        break
                except re.error:
                    pass
    
    return alerts


# 使用默认的 ThreadingMixIn，不自定义线程处理
class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    """多线程 HTTP 服务器"""
    daemon_threads = True
    allow_reuse_address = True
    block_on_close = False  # 防止关闭时死锁


class ProxyHandler(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'
    timeout = 10  # 请求处理超时（防止连接挂起）
    
    def log_message(self, format, *args):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {format % args}")
    
    def _send_json_response(self, status, data):
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', len(body))
        self.send_header('Connection', 'close')
        self.end_headers()
        self.wfile.write(body)
    
    def _read_request_body(self):
        content_length = int(self.headers.get('Content-Length', 0))
        
        if content_length > MAX_BODY_SIZE:
            raise ValueError(f"请求体过大: {content_length} > {MAX_BODY_SIZE}")
        
        if content_length == 0:
            return b''
        
        return self.rfile.read(content_length)
    
    def _forward_request(self, target_url, request_body, request_headers):
        headers = {
            'Content-Type': request_headers.get('Content-Type', 'application/json'),
            'User-Agent': 'OpenClaw-LLM-Proxy/3.1',
        }
        for header in ['Authorization', 'X-Api-Key', 'Api-Key', 'HTTP-Referer', 'X-Title']:
            if header in request_headers:
                headers[header] = request_headers[header]
        
        req = Request(target_url, data=request_body, headers=headers, method='POST')
        
        with urlopen(req, timeout=READ_TIMEOUT) as response:
            return response.read(), response.status
    
    def do_POST(self):
        request_id = str(uuid.uuid4())[:8]
        stats.increment("total_requests")
        start_time = time.time()
        
        # 解析 provider
        path = self.path
        provider = None
        target_base = None
        
        for prefix, base_url in PROVIDERS.items():
            if path.startswith(prefix):
                provider = prefix.lstrip("/")
                target_base = base_url
                path = path[len(prefix):] or "/"
                break
        
        if not target_base:
            self._send_json_response(404, {"error": f"Unknown provider: {self.path}"})
            return
        
        # 读取请求体
        try:
            request_body = self._read_request_body()
        except ValueError as e:
            self._send_json_response(413, {"error": str(e)})
            return
        except Exception as e:
            self._send_json_response(400, {"error": f"读取请求体失败: {e}"})
            return
        
        # 转发请求
        target_url = target_base.rstrip('/') + path
        alerts = []
        response_data = None
        status = 500
        
        try:
            response_data, status = self._forward_request(target_url, request_body, self.headers)
            
            # 检查响应内容（仅 JSON）
            try:
                resp_json = json.loads(response_data)
                choices = resp_json.get("choices", [])
                if choices:
                    content = choices[0].get("message", {}).get("content", "")
                    alerts = check_content(content, RULES)
                    
                    if alerts:
                        critical = [a for a in alerts if a["severity"] == "critical"]
                        if critical:
                            stats.increment("blocked")
                            print(f"[{request_id}] 🔴 发现 {len(critical)} 个严重告警!")
                        else:
                            stats.increment("warnings")
                            print(f"[{request_id}] ⚠️ 发现 {len(alerts)} 个警告")
            except (json.JSONDecodeError, KeyError):
                pass
            
            stats.increment("total_responses")
            
            # 返回响应
            self.send_response(status)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', len(response_data))
            self.send_header('Connection', 'close')
            self.end_headers()
            self.wfile.write(response_data)
            
        except HTTPError as e:
            status = e.code
            stats.increment("errors")
            print(f"[{request_id}] ❌ HTTP {e.code}: {e.reason}")
            self._send_json_response(status, {"error": f"上游错误: {e.reason}", "status": status})
            
        except URLError as e:
            status = 502
            stats.increment("errors")
            print(f"[{request_id}] ❌ 连接失败: {e.reason}")
            self._send_json_response(502, {"error": f"连接失败: {e.reason}"})
            
        except socket.timeout:
            status = 504
            stats.increment("errors")
            print(f"[{request_id}] ❌ 请求超时 ({READ_TIMEOUT}s)")
            self._send_json_response(504, {"error": "请求超时"})
            
        except Exception as e:
            status = 500
            stats.increment("errors")
            print(f"[{request_id}] ❌ 内部错误: {e}")
            traceback.print_exc()
            try:
                self._send_json_response(500, {"error": "内部服务器错误"})
            except:
                pass
        
        # 记录日志
        duration_ms = int((time.time() - start_time) * 1000)
        
        response_preview = None
        if response_data:
            try:
                resp_json = json.loads(response_data)
                choices = resp_json.get("choices", [])
                if choices:
                    content = choices[0].get("message", {}).get("content", "")
                    response_preview = content[:LOG_PREVIEW_CHARS] + ("..." if len(content) > LOG_PREVIEW_CHARS else "")
            except:
                response_preview = f"[{len(response_data)} bytes]"
        
        log_writer.write({
            "timestamp": datetime.now().isoformat(),
            "request_id": request_id,
            "provider": provider,
            "path": path,
            "status": status,
            "duration_ms": duration_ms,
            "alerts": alerts,
            "request_size": len(request_body),
            "response_size": len(response_data) if response_data else 0,
            "response_preview": response_preview
        })
    
    def do_GET(self):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] [DEBUG] do_GET called: {self.path}", flush=True)
        if self.path == "/health":
            self._send_json_response(200, {
                "status": "ok",
                "stats": stats.to_dict(),
                "uptime": int(time.time() - stats.get("start_time")),
                "rules_loaded": {
                    "layer1": len(RULES.get("layer1_malicious", {}).get("rules", [])),
                    "layer2": len(RULES.get("layer2_sensitive", {}).get("rules", [])),
                    "layer3": RULES.get("layer3_llm_review", {}).get("enabled", False),
                    "whitelist": len(RULES.get("whitelist", []))
                },
                "max_threads": MAX_THREADS,
                "active_threads": threading.active_count()
            })
        elif self.path == "/stats":
            self._send_json_response(200, stats.to_dict())
        else:
            self._send_json_response(404, {"error": "Not found"})


def print_banner():
    rules_count = len(RULES.get("layer1_malicious", {}).get("rules", [])) + \
                  len(RULES.get("layer2_sensitive", {}).get("rules", []))
    print(f"""
╔══════════════════════════════════════════════════════╗
║  🔒 LLM Proxy v3.1 (多线程 + 线程安全)              ║
╠══════════════════════════════════════════════════════╣
║  Port: {PROXY_PORT:<42}║
║  Rules: {rules_count} rules loaded{' ' * (30 - len(str(rules_count)))}║
║  Timeout: {READ_TIMEOUT}s{' ' * 34}║
║  Max Body: {MAX_BODY_SIZE // 1024 // 1024}MB{' ' * 35}║
║  Max Threads: {MAX_THREADS}{' ' * 33}║
╠══════════════════════════════════════════════════════╣
║  Health: http://127.0.0.1:{PROXY_PORT}/health{' ' * 17}║
║  Stats:  http://127.0.0.1:{PROXY_PORT}/stats{' ' * 18}║
╚══════════════════════════════════════════════════════╝
""")


def signal_handler(signum, frame):
    """优雅关闭：处理 SIGINT/SIGTERM"""
    sig_name = signal.Signals(signum).name
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] 🛑 收到 {sig_name} 信号，正在关闭...")
    
    if server_instance:
        # 停止接受新连接
        server_instance.shutdown()
    
    shutdown_event.set()


def debug_signal_handler(signum, frame):
    """SIGUSR1: 输出所有线程堆栈用于调试"""
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] 🔍 调试信息 - 活跃线程: {threading.active_count()}", flush=True)
    for thread in threading.enumerate():
        print(f"  线程: {thread.name} (daemon={thread.daemon})", flush=True)
    import traceback
    print("\n主线程堆栈:", flush=True)
    traceback.print_stack(frame)
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 🔍 调试信息结束\n", flush=True)


def wait_for_network(max_wait=30):
    """启动时检查网络是否就绪"""
    import urllib.request
    targets = ["https://www.baidu.com", "https://www.apple.com"]
    waited = 0
    print(f"[{datetime.now().strftime('%H:%M:%S')}] ⏳ 检查网络连接...")
    while waited < max_wait:
        for target in targets:
            try:
                urllib.request.urlopen(target, timeout=3)
                print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ 网络就绪 (耗时 {waited}秒)")
                return True
            except:
                pass
        time.sleep(3)
        waited += 3
    print(f"[{datetime.now().strftime('%H:%M:%S')}] ⚠️ 网络检查超时，继续启动")
    return False


def main():
    global server_instance

    print_banner()

    # 启动前检查网络
    wait_for_network(30)
    
    # 注册信号处理器
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGUSR1, debug_signal_handler)  # 调试用
    
    try:
        server_instance = ThreadingHTTPServer(('127.0.0.1', PROXY_PORT), ProxyHandler)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ 代理服务启动 (PID: {os.getpid()})")
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 📋 多线程模式 | 最大线程: {MAX_THREADS} | 超时: {READ_TIMEOUT}s")
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 按 Ctrl+C 停止\n")
        
        # serve_forever 会阻塞，直到 shutdown() 被调用
        server_instance.serve_forever()
        
    except OSError as e:
        if e.errno == 48:
            print(f"[ERROR] 端口 {PROXY_PORT} 已被占用")
            print("[TIP] 运行: lsof -i :18888 然后 kill <PID>")
        else:
            print(f"[ERROR] 启动失败: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] 启动失败: {e}")
        traceback.print_exc()
        sys.exit(1)
    finally:
        s = stats.to_dict()
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 代理服务已停止")
        print(f"[统计] 请求: {s['total_requests']}, 响应: {s['total_responses']}, 错误: {s['errors']}, 告警: {s['blocked'] + s['warnings']}")


if __name__ == "__main__":
    main()
