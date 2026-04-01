#!/usr/bin/env python3
"""
抖音视频分析 MCP Server
支持本地语音识别和云端识别可选
结合 MiniMax 图像理解
"""

import os
import re
import json
import requests
import subprocess
import tempfile
import nest_asyncio
nest_asyncio.apply()  # 允许在 async 事件循环中运行 sync 代码
from typing import Optional, Dict, Any, List
from urllib.parse import urlparse, parse_qs
from datetime import datetime

# ============ 配置 ============
class Config:
    # 语音识别模式: "local" | "cloud" | "auto" (local优先，失败则cloud)
    STT_MODE = os.environ.get("DOUYIN_STT_MODE", "auto")
    
    # SiliconFlow API (cloud 模式需要)
    SILICONFLOW_API_KEY = os.environ.get("SILICONFLOW_API_KEY", "")
    SILICONFLOW_BASE_URL = os.environ.get("SILICONFLOW_BASE_URL", "https://api.siliconflow.cn")
    
    # MiniMax API (图像理解需要)
    MINIMAX_API_KEY = os.environ.get("MINIMAX_API_KEY", "")
    MINIMAX_BASE_URL = os.environ.get("MINIMAX_BASE_URL", "https://api.minimax.chat")
    
    # 本地 whisper 模型路径
    WHISPER_MODEL = os.environ.get("WHISPER_MODEL", "small")  # tiny/base/small/medium/large
    WHISPER_MODEL_DIR = os.environ.get("WHISPER_MODEL_DIR", os.path.expanduser("~/.whisper.cpp/models"))
    
    # 第三方 API (备选)
    THIRD_PARTY_API = os.environ.get("DOUYIN_THIRD_PARTY_API", "https://liuxingw.com/api/douyin/api.php")

# ============ 抖音链接解析 ============
class DouyinParser:
    """解析抖音分享链接"""
    
    SHARE_URL_PATTERN = r'https?://v\.douyin\.com/[a-zA-Z0-9_-]+'
    
    @staticmethod
    def extract_video_id(url: str) -> Optional[str]:
        """从分享链接提取视频ID"""
        # 处理短链接
        match = re.search(DouyinParser.SHARE_URL_PATTERN, url)
        if not match:
            return None
        
        share_url = match.group(0)
        
        # 获取重定向后的URL
        try:
            resp = requests.head(share_url, allow_redirects=True, timeout=10)
            final_url = resp.url
        except:
            return None
        
        # 从URL中提取video_id
        # 格式: https://www.iesdouyin.com/share/video/7123456789012345678/...
        match = re.search(r'/video/(\d+)', final_url)
        if match:
            return match.group(1)
        
        return None
    
    @staticmethod
    def extract_share_url(url: str) -> Optional[str]:
        """从分享链接提取完整的分享URL（用于浏览器访问）"""
        match = re.search(DouyinParser.SHARE_URL_PATTERN, url)
        if match:
            return match.group(0) + "/"
        return None
    
    @staticmethod
    def get_video_info(video_id: str, share_url: str = None) -> Optional[Dict]:
        """获取视频信息 - 优先官方API，失败则用第三方，最后用浏览器"""
        
        # 先尝试官方 API
        info = DouyinParser._get_video_info_official(video_id)
        if info:
            return info
        
        # 第三方
        info = DouyinParser._get_video_info_third_party(video_id)
        if info:
            return info
        
        # 最后尝试浏览器
        return DouyinParser._get_video_info_browser(video_id, share_url)
    
    @staticmethod
    def _get_video_info_browser(video_id: str, share_url: str = None) -> Optional[Dict]:
        """使用 Playwright 浏览器获取视频信息（通过 subprocess 避免 asyncio 冲突）"""
        try:
            # 如果没有提供分享链接，使用 video_id 构造（可能跳转到首页）
            if not share_url:
                share_url = f"https://v.douyin.com/{video_id}/"
            
            # 使用 subprocess 运行浏览器代码，避免与 asyncio 冲突
            _python = "/Users/kk/.openclaw/mcp-servers/douyin-analyzer/.venv/bin/python3"
            _share_url = share_url.replace("'", "'\\''")
            result = subprocess.run(
                [ _python, "-c", f"""
import sys
sys.path.insert(0, '/Users/kk/.openclaw/mcp-servers/douyin-analyzer')
from playwright.sync_api import sync_playwright

share_url = '{_share_url}'
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        viewport={{"width": 375, "height": 812}},
        user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"
    )
    page = context.new_page()
    page.goto(share_url, wait_until='domcontentloaded', timeout=30000)
    page.wait_for_timeout(8000)

    # 提取标题（从 meta description 中提取，格式：标题 - 作者）
    title = "未知标题"
    desc_elem = page.query_selector('meta[name="description"]')
    if desc_elem:
        desc = desc_elem.get_attribute('content') or ""
        if desc:
            title = desc.split(" - ")[0].strip()

    # 提取视频下载链接
    video = page.query_selector('video')
    download_url = None
    if video:
        src = page.evaluate('el => el.src', video)
        if src and 'playwm' in src:
            download_url = src.replace('playwm', 'play')

    browser.close()
    import json
    print(json.dumps({{'url': download_url, 'title': title}}), flush=True)
"""
                ],
                capture_output=True, text=True, timeout=60
            )
            try:
                data = json.loads(result.stdout.strip())
                download_url = data.get("url")
                title = data.get("title", "未知标题")
            except:
                download_url = None
                title = "未知标题"
            if not download_url:
                print(f"Browser stderr: {result.stderr[:200]}")
            
            return {
                "video_id": video_id,
                "title": title,
                "author": "",
                "download_url": download_url,
                "source": "browser"
            }
        except Exception as e:
            print(f"Browser parsing error: {e}")
            return None
    
    @staticmethod
    def _get_video_info_official(video_id: str) -> Optional[Dict]:
        """官方 API 获取视频信息"""
        url = f"https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids={video_id}"
        
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Referer": "https://www.douyin.com/",
                "Cookie": "tt_webid=xxx"
            }
            resp = requests.get(url, headers=headers, timeout=10)
            
            if resp.status_code != 200 or not resp.text:
                return None
            
            data = resp.json()
            
            if data.get("status_code") != 0:
                return None
            
            item = data.get("item_list", [{}])[0]
            
            return {
                "video_id": video_id,
                "title": item.get("desc", ""),
                "author": item.get("author", {}).get("nickname", ""),
                "create_time": item.get("create_time", 0),
                "digg_count": item.get("statistic", {}).get("digg_count", 0),
                "comment_count": item.get("statistic", {}).get("comment_count", 0),
                "share_count": item.get("statistic", {}).get("share_count", 0),
                "duration": item.get("video", {}).get("duration", 0) / 1000,
            }
        except Exception as e:
            print(f"Official API error: {e}")
            return None
    
    @staticmethod
    def _get_video_info_third_party(video_id: str) -> Optional[Dict]:
        """第三方 API 获取视频信息"""
        try:
            # 使用第三方解析服务
            share_url = f"https://v.douyin.com/{video_id}"
            api_url = f"{Config.THIRD_PARTY_API}?url={share_url}"
            
            resp = requests.get(api_url, timeout=15)
            
            if resp.status_code == 200:
                data = resp.json()
                
                # 解析第三方API响应
                if data.get("success") or data.get("code") == 200:
                    return {
                        "video_id": video_id,
                        "title": data.get("title", ""),
                        "author": data.get("author", ""),
                        "digg_count": data.get("digg_count", 0),
                        "comment_count": data.get("comment_count", 0),
                        "share_count": data.get("share_count", 0),
                        "duration": data.get("duration", 0),
                        "cover_url": data.get("cover", ""),
                        "download_url": data.get("url", ""),
                    }
            
            return None
        except Exception as e:
            print(f"Third party API error: {e}")
            return None
    
    @staticmethod
    def get_download_url(video_id: str, share_url: str = None) -> Optional[str]:
        """获取无水印视频下载链接 - 优先官方，失败则用第三方，最后用浏览器"""
        
        # 先尝试官方
        url = DouyinParser._get_download_url_official(video_id)
        if url:
            return url
        
        # 第三方
        url = DouyinParser._get_download_url_third_party(video_id)
        if url:
            return url
        
        # 最后尝试浏览器 (传入share_url)
        return DouyinParser._get_download_url_browser(video_id, share_url)
    
    @staticmethod
    def _get_download_url_browser(video_id: str, share_url: str = None) -> Optional[str]:
        """使用 Playwright 浏览器获取下载链接（通过 subprocess 避免 asyncio 冲突）"""
        try:
            # 如果没有提供分享链接，使用 video_id 构造
            if not share_url:
                share_url = f"https://v.douyin.com/{video_id}/"
            
            _python = "/Users/kk/.openclaw/mcp-servers/douyin-analyzer/.venv/bin/python3"
            _share_url = share_url.replace("'", "'\\''")
            result = subprocess.run(
                [_python, "-c", f"""
import sys
sys.path.insert(0, '/Users/kk/.openclaw/mcp-servers/douyin-analyzer')
from playwright.sync_api import sync_playwright

share_url = '{_share_url}'
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        viewport={{"width": 375, "height": 812}},
        user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"
    )
    page = context.new_page()
    page.goto(share_url, wait_until='domcontentloaded', timeout=30000)
    page.wait_for_timeout(10000)
    video = page.query_selector('video')
    download_url = None
    if video:
        src = page.evaluate('el => el.src', video)
        if src:
            if src.startswith('/'):
                src = 'https://aweme.snssdk.com' + src
            if 'playwm' in src:
                download_url = src.replace('playwm', 'play')
            elif 'play' in src:
                download_url = src
    browser.close()
    import json
    print(json.dumps({{'url': download_url}}), flush=True)
"""
                ],
                capture_output=True, text=True, timeout=60
            )
            try:
                data = json.loads(result.stdout.strip())
                return data.get("url")
            except:
                return None
        except Exception as e:
            print(f"Browser download URL error: {e}")
            return None
    
    @staticmethod
    def _get_download_url_official(video_id: str) -> Optional[str]:
        """官方 API 获取下载链接"""
        info_url = f"https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids={video_id}"
        
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Referer": "https://www.douyin.com/"
            }
            resp = requests.get(info_url, headers=headers, timeout=10)
            data = resp.json()
            
            item = data.get("item_list", [{}])[0]
            video_info = item.get("video", {})
            
            # 获取playwm链接，去掉wm变成无水印
            playwm_url = video_info.get("playwm_addr", {}).get("url_list", [None])[0]
            
            if playwm_url:
                download_url = playwm_url.replace("playwm", "play")
                return download_url
            
            return None
        except Exception as e:
            print(f"Official download URL error: {e}")
            return None
    
    @staticmethod
    def _get_download_url_third_party(video_id: str) -> Optional[str]:
        """第三方 API 获取下载链接"""
        try:
            share_url = f"https://v.douyin.com/{video_id}"
            api_url = f"{Config.THIRD_PARTY_API}?url={share_url}"
            
            resp = requests.get(api_url, timeout=15)
            
            if resp.status_code == 200:
                data = resp.json()
                # 尝试多种返回格式
                return data.get("url") or data.get("video_url") or data.get("download_url")
            
            return None
        except Exception as e:
            print(f"Third party download URL error: {e}")
            return None
            
            item = data.get("item_list", [{}])[0]
            video_info = item.get("video", {})
            
            # 获取playwm链接，去掉wm变成无水印
            playwm_url = video_info.get("playwm_addr", {}).get("url_list", [None])[0]
            
            if playwm_url:
                # 替换 playwm 为 play
                download_url = playwm_url.replace("playwm", "play")
                return download_url
            
            return None
        except Exception as e:
            print(f"Error getting download URL: {e}")
            return None

# ============ 音频处理 ============
class AudioProcessor:
    """音频处理和语音识别"""
    
    @staticmethod
    def download_video(url: str, output_path: str) -> bool:
        """下载视频"""
        try:
            resp = requests.get(url, stream=True, timeout=60)
            with open(output_path, 'wb') as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    f.write(chunk)
            return True
        except Exception as e:
            print(f"Error downloading video: {e}")
            return False
    
    @staticmethod
    def extract_audio(video_path: str, audio_path: str) -> bool:
        """提取音频"""
        try:
            cmd = [
                "ffmpeg", "-i", video_path,
                "-vn", "-acodec", "libmp3lame", "-q:a", "2",
                "-y", audio_path
            ]
            subprocess.run(cmd, capture_output=True, check=True)
            return True
        except Exception as e:
            print(f"Error extracting audio: {e}")
            return False
    
    @staticmethod
    def transcribe_local(audio_path: str) -> Optional[str]:
        """本地 whisper.cpp 语音识别"""
        try:
            # 尝试使用 whisper.cpp 的二进制
            cmd = [
                "whisper-cli", "-m", 
                f"{Config.WHISPER_MODEL_DIR}/ggml-{Config.WHISPER_MODEL}.bin",
                "-f", audio_path, "-otxt"
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                txt_path = audio_path.replace(".mp3", ".txt")
                if os.path.exists(txt_path):
                    with open(txt_path, 'r', encoding='utf-8') as f:
                        return f.read()
            
            # 如果 whisper-cli 不可用，尝试 Python binding
            try:
                import whisper
                model = whisper.load_model(Config.WHISPER_MODEL)
                result = model.transcribe(audio_path)
                return result["text"]
            except:
                pass
                
            return None
        except Exception as e:
            print(f"Error in local transcription: {e}")
            return None
    
    @staticmethod
    def transcribe_cloud(audio_path: str) -> Optional[str]:
        """SiliconFlow 云端语音识别"""
        if not Config.SILICONFLOW_API_KEY:
            print("SiliconFlow API key not configured")
            return None
        
        try:
            url = f"{Config.SILICONFLOW_BASE_URL}/v1/audio/transcriptions"
            
            with open(audio_path, 'rb') as f:
                files = {'file': f}
                data = {
                    'model': 'FunAudioLLM/SenseVoiceSmall',
                }
                headers = {'Authorization': f'Bearer {Config.SILICONFLOW_API_KEY}'}
                
                resp = requests.post(url, files=files, data=data, headers=headers, timeout=120)
                
                if resp.status_code == 200:
                    result = resp.json()
                    return result.get("text", "")
                else:
                    print(f"Cloud transcription error: {resp.status_code} {resp.text}")
                    return None
                    
        except Exception as e:
            print(f"Error in cloud transcription: {e}")
            return None
    
    @staticmethod
    def transcribe(audio_path: str) -> Optional[str]:
        """语音识别 - 自动选择模式"""
        
        # 优先尝试本地
        if Config.STT_MODE in ("local", "auto"):
            result = AudioProcessor.transcribe_local(audio_path)
            if result:
                return result
        
        # 本地失败或选择云端
        if Config.STT_MODE in ("cloud", "auto"):
            if Config.SILICONFLOW_API_KEY:
                result = AudioProcessor.transcribe_cloud(audio_path)
                if result:
                    return result
        
        return None

# ============ 关键帧提取 ============
class VideoFrameExtractor:
    """视频关键帧提取"""
    
    @staticmethod
    def extract_frame(video_path: str, timestamp: float, output_path: str) -> bool:
        """提取指定时间点的帧"""
        try:
            cmd = [
                "ffmpeg", "-ss", str(timestamp),
                "-i", video_path,
                "-vframes", "1",
                "-y", output_path
            ]
            subprocess.run(cmd, capture_output=True, check=True)
            return os.path.exists(output_path)
        except Exception as e:
            print(f"Error extracting frame: {e}")
            return False

# ============ MiniMax 图像理解 ============
class MiniMaxImageUnderstander:
    """MiniMax 图像理解"""
    
    @staticmethod
    def analyze(image_path: str, prompt: str = "描述这张图片的内容") -> Optional[str]:
        """使用 MiniMax 分析图像"""
        if not Config.MINIMAX_API_KEY:
            return "MiniMax API key not configured"
        
        try:
            # 将图片转为 base64
            import base64
            with open(image_path, 'rb') as f:
                img_data = base64.b64encode(f.read()).decode()
            
            url = f"{Config.MINIMAX_BASE_URL}/v1/images/generation"
            
            headers = {
                "Authorization": f"Bearer {Config.MINIMAX_API_KEY}",
                "Content-Type": "application/json"
            }
            
            # MiniMax 图像理解使用文本对话 API
            payload = {
                "model": "MiniMax-M2.1",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{img_data}"
                                }
                            },
                            {
                                "type": "text",
                                "text": prompt
                            }
                        ]
                    }
                ],
                "max_tokens": 1000
            }
            
            resp = requests.post(url, json=payload, headers=headers, timeout=60)
            
            if resp.status_code == 200:
                result = resp.json()
                return result.get("choices", [{}])[0].get("message", {}).get("content", "")
            else:
                return f"Error: {resp.status_code} {resp.text[:200]}"
                
        except Exception as e:
            return f"Error: {str(e)}"

# ============ 内容分析 ============
class ContentAnalyzer:
    """分析语音内容，找出高潮/亮点"""
    
    @staticmethod
    def find_highlights(transcript: str, duration: float) -> List[Dict]:
        """分析内容，找出亮点时间点"""
        if not Config.MINIMAX_API_KEY:
            return []
        
        try:
            url = f"{Config.MINIMAX_BASE_URL}/v1/chat/completions"
            
            headers = {
                "Authorization": f"Bearer {Config.MINIMAX_API_KEY}",
                "Content-Type": "application/json"
            }
            
            prompt = f"""分析以下抖音视频语音内容，找出可能的高潮或亮点部分。

视频时长: {duration}秒

语音内容:
{transcript[:2000]}

请分析内容，找出3-5个可能的亮点时间点（用占视频时长的百分比表示，0-100%）。
返回JSON数组格式:
[
  {{"timestamp_percent": 30, "reason": "观众笑声/掌声/情绪高潮"}},
  {{"timestamp_percent": 65, "reason": "核心内容/关键信息"}}
]

只返回JSON数组，不要其他内容。"""

            payload = {
                "model": "MiniMax-M2.1",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 500
            }
            
            resp = requests.post(url, json=payload, headers=headers, timeout=30)
            
            if resp.status_code == 200:
                result = resp.json()
                content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
                
                # 解析 JSON
                import re
                json_match = re.search(r'\[.*\]', content, re.DOTALL)
                if json_match:
                    highlights = json.loads(json_match.group())
                    return [
                        {
                            "timestamp": (h.get("timestamp_percent", 0) / 100) * duration,
                            "reason": h.get("reason", "")
                        }
                        for h in highlights
                    ]
            
            return []
            
        except Exception as e:
            print(f"Error analyzing content: {e}")
            return []

# ============ 主流程 ============
class DouyinAnalyzer:
    """抖音视频完整分析"""
    
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp()
    
    def analyze(self, share_url: str, focus_highlight: bool = True) -> Dict[str, Any]:
        """完整分析流程"""
        result = {
            "status": "pending",
            "video_info": None,
            "transcript": None,
            "highlights": [],
            "frame_analysis": [],
            "error": None
        }
        
        try:
            # 1. 解析链接
            video_id = DouyinParser.extract_video_id(share_url)
            if not video_id:
                result["error"] = "无法解析抖音链接"
                return result
            
            # 2. 获取视频信息
            video_info = DouyinParser.get_video_info(video_id, share_url)
            if not video_info:
                result["error"] = "无法获取视频信息"
                return result
            result["video_info"] = video_info
            
            # 3. 获取下载链接 (传入share_url用于浏览器模式)
            download_url = DouyinParser.get_download_url(video_id, share_url)
            if not download_url:
                result["error"] = "无法获取视频下载链接"
                return result
            
            # 4. 下载视频
            video_path = os.path.join(self.temp_dir, "video.mp4")
            if not AudioProcessor.download_video(download_url, video_path):
                result["error"] = "视频下载失败"
                return result
            
            # 5. 提取音频
            audio_path = os.path.join(self.temp_dir, "audio.mp3")
            if not AudioProcessor.extract_audio(video_path, audio_path):
                result["error"] = "音频提取失败"
                return result
            
            # 6. 语音识别
            transcript = AudioProcessor.transcribe(audio_path)
            if transcript:
                result["transcript"] = transcript
                
                # 7. 分析内容找亮点
                if focus_highlight and Config.MINIMAX_API_KEY:
                    highlights = ContentAnalyzer.find_highlights(
                        transcript, 
                        video_info.get("duration", 0)
                    )
                    result["highlights"] = highlights
                    
                    # 8. 提取关键帧并分析
                    for hl in highlights[:2]:  # 最多取2个亮点
                        frame_path = os.path.join(self.temp_dir, f"frame_{hl['timestamp']}.jpg")
                        if VideoFrameExtractor.extract_frame(video_path, hl["timestamp"], frame_path):
                            frame_analysis = MiniMaxImageUnderstander.analyze(
                                frame_path, 
                                "描述这个视频关键时刻的画面内容"
                            )
                            result["frame_analysis"].append({
                                "timestamp": hl["timestamp"],
                                "reason": hl["reason"],
                                "frame_path": frame_path,
                                "analysis": frame_analysis
                            })
            
            result["status"] = "success"
            
        except Exception as e:
            result["error"] = str(e)
        
        finally:
            # 清理临时文件
            import shutil
            try:
                shutil.rmtree(self.temp_dir)
            except:
                pass
        
        return result

# ============ MCP 工具函数 ============
def parse_douyin_video_info(share_link: str) -> str:
    """解析抖音视频基本信息"""
    video_id = DouyinParser.extract_video_id(share_link)
    if not video_id:
        return json.dumps({"error": "无法解析抖音链接"}, ensure_ascii=False)
    
    info = DouyinParser.get_video_info(video_id, share_link)
    if not info:
        return json.dumps({"error": "无法获取视频信息"}, ensure_ascii=False)
    
    return json.dumps(info, ensure_ascii=False, indent=2)

def get_douyin_download_link(share_link: str) -> str:
    """获取抖音视频无水印下载链接"""
    video_id = DouyinParser.extract_video_id(share_link)
    if not video_id:
        return json.dumps({"error": "无法解析抖音链接"}, ensure_ascii=False)
    
    # 传入 share_url 用于浏览器模式
    url = DouyinParser.get_download_url(video_id, share_link)
    if not url:
        return json.dumps({"error": "无法获取下载链接"}, ensure_ascii=False)
    
    return json.dumps({
        "video_id": video_id,
        "download_url": url,
        "share_link": share_link
    }, ensure_ascii=False)

def analyze_douyin_video(share_link: str, focus_highlight: bool = True) -> str:
    """完整分析抖音视频（语音+画面）"""
    analyzer = DouyinAnalyzer()
    result = analyzer.analyze(share_link, focus_highlight)
    return json.dumps(result, ensure_ascii=False, indent=2)

def extract_douyin_audio(share_link: str) -> str:
    """提取抖音视频音频"""
    video_id = DouyinParser.extract_video_id(share_link)
    if not video_id:
        return json.dumps({"error": "无法解析抖音链接"}, ensure_ascii=False)
    
    download_url = DouyinParser.get_download_url(video_id)
    if not download_url:
        return json.dumps({"error": "无法获取下载链接"}, ensure_ascii=False)
    
    temp_dir = tempfile.mkdtemp()
    video_path = os.path.join(temp_dir, "video.mp4")
    audio_path = os.path.join(temp_dir, "audio.mp3")
    
    try:
        if not AudioProcessor.download_video(download_url, video_path):
            return json.dumps({"error": "视频下载失败"}, ensure_ascii=False)
        
        if not AudioProcessor.extract_audio(video_path, audio_path):
            return json.dumps({"error": "音频提取失败"}, ensure_ascii=False)
        
        # 读取音频返回
        with open(audio_path, 'rb') as f:
            import base64
            audio_b64 = base64.b64encode(f.read()).decode()
        
        return json.dumps({
            "status": "success",
            "audio": audio_b64,
            "format": "mp3"
        }, ensure_ascii=False)
        
    finally:
        import shutil
        shutil.rmtree(temp_dir, ignore_errors=True)

# ============ MCP Server ============
from mcp.server import Server
from mcp.types import Tool, TextContent
from mcp.server.stdio import stdio_server

app = Server("douyin-analyzer")

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="parse_douyin_video_info",
            description="解析抖音视频基本信息（标题、作者、点赞数等）",
            inputSchema={
                "type": "object",
                "properties": {
                    "share_link": {"type": "string", "description": "抖音分享链接"}
                },
                "required": ["share_link"]
            }
        ),
        Tool(
            name="get_douyin_download_link",
            description="获取抖音视频无水印下载链接",
            inputSchema={
                "type": "object",
                "properties": {
                    "share_link": {"type": "string", "description": "抖音分享链接"}
                },
                "required": ["share_link"]
            }
        ),
        Tool(
            name="analyze_douyin_video",
            description="完整分析抖音视频：语音识别+内容分析+关键帧提取+画面理解",
            inputSchema={
                "type": "object",
                "properties": {
                    "share_link": {"type": "string", "description": "抖音分享链接"},
                    "focus_highlight": {"type": "boolean", "description": "是否分析内容找亮点", "default": True}
                },
                "required": ["share_link"]
            }
        ),
        Tool(
            name="extract_douyin_audio",
            description="提取抖音视频音频（Base64编码）",
            inputSchema={
                "type": "object",
                "properties": {
                    "share_link": {"type": "string", "description": "抖音分享链接"}
                },
                "required": ["share_link"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "parse_douyin_video_info":
        result = parse_douyin_video_info(arguments["share_link"])
    elif name == "get_douyin_download_link":
        result = get_douyin_download_link(arguments["share_link"])
    elif name == "analyze_douyin_video":
        result = analyze_douyin_video(
            arguments["share_link"], 
            arguments.get("focus_highlight", True)
        )
    elif name == "extract_douyin_audio":
        result = extract_douyin_audio(arguments["share_link"])
    else:
        result = json.dumps({"error": f"Unknown tool: {name}"})
    
    return [TextContent(type="text", text=result)]

async def main():
    async with stdio_server() as (read, write):
        await app.run(read, write, app.create_initialization_options())

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
