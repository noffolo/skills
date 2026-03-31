#!/usr/bin/env python3
"""
博查搜索 (Bocha Search) Python 客户端

功能：
- 支持博查 Web Search API
- 多种输出格式：原始 JSON、Brave 兼容格式、Markdown
- 灵活配置：环境变量、配置文件、命令行参数
- 错误处理和重试机制
- 兼容 Bing Search API 响应格式

用法：
    python3 search.py <query> [options]
    python3 search.py --query "<query>" [options]

示例：
    python3 search.py "沪电股份"
    python3 search.py "人工智能" --count 5 --freshness oneWeek --summary
    python3 search.py "阿里巴巴 ESG" --format brave --max-results 10
    python3 search.py "AI 新闻" --format md --include-answer
"""

import argparse
import json
import os
import sys
import time
import pathlib
import re
from typing import Optional, Dict, Any, List
import urllib.request
import urllib.error

# 常量
DEFAULT_API_ENDPOINT = "https://api.bochaai.com/v1/web-search"
ALTERNATE_ENDPOINT = "https://api.bocha.cn/v1/web-search"
ENV_VAR_NAME = "BOCHA_API_KEY"

class BochaSearchClient:
    """博查搜索 API 客户端"""
    
    def __init__(self, api_key: Optional[str] = None, endpoint: str = DEFAULT_API_ENDPOINT):
        """
        初始化客户端
        
        Args:
            api_key: API 密钥，如果为 None 则自动检测
            endpoint: API 端点
        """
        self.endpoint = endpoint
        self.api_key = api_key or self._load_api_key()
        if not self.api_key:
            raise ValueError("未找到博查 API 密钥。请设置环境变量 BOCHA_API_KEY 或在 ~/.openclaw/.env 文件中配置。")
    
    def _load_api_key(self) -> Optional[str]:
        """从多个来源加载 API 密钥"""
        # 1. 用户主目录下的 .openclaw/.env（优先级最高）
        env_path = pathlib.Path.home() / ".openclaw" / ".env"
        if env_path.exists():
            try:
                content = env_path.read_text(encoding='utf-8', errors='ignore')
                # 简单正则匹配
                match = re.search(rf'^\s*{ENV_VAR_NAME}\s*=\s*(.+?)\s*$', content, re.MULTILINE)
                if match:
                    key = match.group(1).strip().strip('"').strip("'")
                    if key:
                        return key
            except Exception:
                pass
        
        # 2. 环境变量
        key = os.environ.get(ENV_VAR_NAME)
        if key:
            return key.strip()
        
        return None
    
    def search(
        self,
        query: str,
        count: int = 10,
        freshness: str = "noLimit",
        summary: bool = False,
        max_retries: int = 2,
        timeout: int = 30
    ) -> Dict[str, Any]:
        """
        执行搜索
        
        Args:
            query: 搜索关键词
            count: 返回结果数量 (1-50)
            freshness: 时间范围过滤
            summary: 是否返回详细摘要
            max_retries: 最大重试次数
            timeout: 请求超时时间（秒）
        
        Returns:
            API 原始响应字典
        
        Raises:
            ValueError: 参数错误
            RuntimeError: API 请求失败
        """
        # 参数验证
        if not query or not query.strip():
            raise ValueError("查询关键词不能为空")
        
        count = max(1, min(count, 50))  # 限制在 1-50 范围内
        
        freshness_options = ["noLimit", "oneDay", "oneWeek", "oneMonth", "oneYear"]
        if freshness not in freshness_options and not re.match(r'^\d{4}-\d{2}-\d{2}(\.\.\d{4}-\d{2}-\d{2})?$', freshness):
            raise ValueError(f"freshness 参数无效，可选值: {', '.join(freshness_options)} 或 YYYY-MM-DD..YYYY-MM-DD 格式")
        
        # 构建请求载荷
        payload = {
            "query": query.strip(),
            "count": count,
            "freshness": freshness,
            "summary": summary
        }
        
        # 重试逻辑
        last_exception = None
        for attempt in range(max_retries + 1):
            try:
                return self._make_request(payload, timeout)
            except urllib.error.HTTPError as e:
                last_exception = e
                if e.code == 429:  # 频率限制
                    if attempt < max_retries:
                        wait_time = 2 ** attempt  # 指数退避
                        time.sleep(wait_time)
                        continue
                # 其他 HTTP 错误立即返回
                raise RuntimeError(f"API 请求失败 (HTTP {e.code}): {e.reason}")
            except urllib.error.URLError as e:
                last_exception = e
                if attempt < max_retries:
                    time.sleep(1)
                    continue
                raise RuntimeError(f"网络连接失败: {e.reason}")
            except Exception as e:
                last_exception = e
                if attempt < max_retries:
                    time.sleep(1)
                    continue
                raise RuntimeError(f"请求失败: {str(e)}")
        
        raise RuntimeError(f"请求失败，重试 {max_retries} 次后仍无响应: {last_exception}")
    
    def _make_request(self, payload: Dict[str, Any], timeout: int) -> Dict[str, Any]:
        """执行 HTTP 请求"""
        data = json.dumps(payload).encode('utf-8')
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
            'User-Agent': 'BochaSearchPython/1.0'
        }
        
        req = urllib.request.Request(
            self.endpoint,
            data=data,
            headers=headers,
            method='POST'
        )
        
        with urllib.request.urlopen(req, timeout=timeout) as response:
            result = response.read().decode('utf-8', errors='replace')
            return json.loads(result)


def format_to_brave(response: Dict[str, Any]) -> Dict[str, Any]:
    """
    转换为 Brave/Bing 兼容格式
    
    Args:
        response: 原始 API 响应
    
    Returns:
        标准化格式
    """
    # 错误处理
    if response.get("code") and response["code"] != 200:
        return {
            "type": "error",
            "code": response.get("code"),
            "message": response.get("message", "Unknown error"),
            "log_id": response.get("log_id")
        }
    
    data = response.get("data", {})
    web_pages = data.get("webPages", {}).get("value", [])
    
    # 无结果
    if not web_pages:
        return {
            "type": "search",
            "query": data.get("queryContext", {}).get("originalQuery", ""),
            "totalResults": 0,
            "results": []
        }
    
    # 格式化结果
    results = []
    for i, page in enumerate(web_pages, 1):
        result = {
            "index": i,
            "title": page.get("name", ""),
            "url": page.get("url", ""),
            "description": page.get("snippet", ""),
            "summary": page.get("summary") if page.get("summary") else None,
            "siteName": page.get("siteName", ""),
            "publishedDate": page.get("datePublished") or page.get("dateLastCrawled")
        }
        results.append(result)
    
    return {
        "type": "search",
        "query": data.get("queryContext", {}).get("originalQuery", ""),
        "totalResults": data.get("webPages", {}).get("totalEstimatedMatches", len(results)),
        "resultCount": len(results),
        "results": results
    }


def format_to_markdown(response: Dict[str, Any]) -> str:
    """
    转换为 Markdown 格式
    
    Args:
        response: 原始 API 响应或已格式化的响应
    
    Returns:
        Markdown 字符串
    """
    # 如果响应是原始格式，先转换为标准格式
    if "data" in response:
        formatted = format_to_brave(response)
    else:
        formatted = response
    
    # 错误处理
    if formatted.get("type") == "error":
        return f"**错误**: {formatted.get('code')} - {formatted.get('message')}"
    
    lines = []
    query = formatted.get("query", "")
    total = formatted.get("totalResults", 0)
    
    lines.append(f"## 搜索结果: {query}")
    lines.append(f"*找到约 {total} 条结果*")
    lines.append("")
    
    results = formatted.get("results", [])
    if not results:
        lines.append("未找到相关结果。")
        return "\n".join(lines)
    
    for i, result in enumerate(results, 1):
        title = result.get("title", "").strip() or "无标题"
        url = result.get("url", "").strip()
        desc = result.get("description", "").strip()
        summary = (result.get("summary") or "").strip()
        site = result.get("siteName", "").strip()
        date = result.get("publishedDate", "")
        
        lines.append(f"{i}. **{title}**")
        if site:
            lines.append(f"   *{site}*")
        if url:
            lines.append(f"   [{url}]({url})")
        if desc:
            # 限制描述长度
            if len(desc) > 200:
                desc = desc[:197] + "..."
            lines.append(f"   {desc}")
        if summary and summary != desc:
            # 限制摘要长度
            if len(summary) > 300:
                summary = summary[:297] + "..."
            lines.append(f"   *摘要*: {summary}")
        if date:
            lines.append(f"   *发布时间*: {date}")
        lines.append("")
    
    return "\n".join(lines)


def format_to_raw(response: Dict[str, Any]) -> str:
    """
    输出原始 JSON 格式
    
    Args:
        response: 原始 API 响应
    
    Returns:
        JSON 字符串
    """
    return json.dumps(response, ensure_ascii=False, indent=2)


def parse_freshness(value: str) -> str:
    """解析 freshness 参数"""
    if value in ["noLimit", "oneDay", "oneWeek", "oneMonth", "oneYear"]:
        return value
    
    # 检查日期格式
    if re.match(r'^\d{4}-\d{2}-\d{2}$', value):
        return value
    if re.match(r'^\d{4}-\d{2}-\d{2}\.\.\d{4}-\d{2}-\d{2}$', value):
        return value
    
    raise ValueError(f"无效的 freshness 值: {value}")


def main():
    parser = argparse.ArgumentParser(
        description="博查搜索 API 命令行工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s "沪电股份"
  %(prog)s "人工智能" --count 5 --freshness oneWeek --summary
  %(prog)s "阿里巴巴 ESG" --format brave --max-results 10
  %(prog)s "AI 新闻" --format md --include-answer
  
时间范围 (freshness):
  noLimit     不限时间 (默认)
  oneDay      一天内
  oneWeek     一周内
  oneMonth    一个月内
  oneYear     一年内
  YYYY-MM-DD          指定日期
  YYYY-MM-DD..YYYY-MM-DD  日期范围
        """
    )
    
    # 必需参数
    parser.add_argument(
        "query",
        nargs="?",
        help="搜索关键词（如果使用 --query 选项则可为空）"
    )
    parser.add_argument(
        "--query", "-q",
        dest="query_arg",
        help="搜索关键词（替代位置参数）"
    )
    
    # 搜索参数
    parser.add_argument(
        "--count", "-c",
        type=int,
        default=10,
        help="返回结果数量 (1-50，默认 10)"
    )
    parser.add_argument(
        "--freshness", "-f",
        default="noLimit",
        help="时间范围过滤 (默认: noLimit)"
    )
    parser.add_argument(
        "--summary", "-s",
        action="store_true",
        help="返回详细摘要"
    )
    parser.add_argument(
        "--max-results",
        type=int,
        dest="count",
        help="同 --count"
    )
    
    # 输出选项
    parser.add_argument(
        "--format", "-F",
        choices=["raw", "brave", "md"],
        default="brave",
        help="输出格式: raw(原始JSON), brave(兼容格式), md(Markdown) (默认: brave)"
    )
    parser.add_argument(
        "--include-answer",
        action="store_true",
        help="包含答案摘要（如支持）"
    )
    parser.add_argument(
        "--endpoint", "-e",
        default=DEFAULT_API_ENDPOINT,
        help=f"API 端点 (默认: {DEFAULT_API_ENDPOINT})"
    )
    
    # 其他选项
    parser.add_argument(
        "--timeout", "-t",
        type=int,
        default=30,
        help="请求超时时间（秒，默认 30）"
    )
    parser.add_argument(
        "--retries", "-r",
        type=int,
        default=2,
        help="失败重试次数（默认 2）"
    )

    parser.add_argument(
        "--version", "-V",
        action="version",
        version="博查搜索 Python 客户端 0.1.1"
    )
    
    args = parser.parse_args()
    
    # 确定查询关键词
    query = args.query_arg or args.query
    if not query:
        parser.error("必须提供搜索关键词（使用位置参数或 --query 选项）")
    
    # 验证参数
    args.count = max(1, min(args.count, 50))
    
    try:
        args.freshness = parse_freshness(args.freshness)
    except ValueError as e:
        parser.error(str(e))
    
    # 执行搜索
    try:
        client = BochaSearchClient(api_key=None, endpoint=args.endpoint)
        
        # 执行搜索
        response = client.search(
            query=query,
            count=args.count,
            freshness=args.freshness,
            summary=args.summary,
            max_retries=args.retries,
            timeout=args.timeout
        )
        
        # 格式化输出
        if args.format == "raw":
            output = format_to_raw(response)
        elif args.format == "md":
            output = format_to_markdown(response)
        else:  # brave
            output = json.dumps(format_to_brave(response), ensure_ascii=False, indent=2)
        
        print(output)
        
    except ValueError as e:
        print(json.dumps({
            "type": "error",
            "code": "INVALID_ARGUMENT",
            "message": str(e)
        }), file=sys.stderr)
        sys.exit(1)
    except RuntimeError as e:
        print(json.dumps({
            "type": "error",
            "code": "API_ERROR",
            "message": str(e)
        }), file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(json.dumps({
            "type": "error",
            "code": "UNKNOWN_ERROR",
            "message": f"未知错误: {str(e)}"
        }), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()