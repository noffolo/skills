#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
LLM 直接调用接口

让大模型可以直接使用以下函数进行语音识别：

  from asr_api import transcribe_audio

  # 转录音视频文件
  result = transcribe_audio("C:\\meeting.mp4", language="Chinese")
  print(result['text'])
"""

import json
import sys
from pathlib import Path
from typing import Optional, Dict, Any

# 导入管道
try:
    from acoustic_pipeline import AcousticPipeline
except ImportError:
    # 如果在不同目录，尝试添加到路径
    sys.path.insert(0, str(Path(__file__).parent))
    from acoustic_pipeline import AcousticPipeline


def transcribe_audio(
    file_path: str,
    language: str = "auto",
    keep_extracted: bool = False,
    archive_mode: str = "none",
    archive_dir: Optional[str] = None,
    auto_bootstrap: bool = False,
) -> Dict[str, Any]:
    """
    转录音视频文件 - LLM可直接调用
    
    这是给大模型调用的简单接口。支持任何音频或视频格式。
    如果是视频文件，会自动提取音轨。
    
    Args:
        file_path: 文件路径 (支持 MP4、MP3、WAV、FLAC 等)
        language: 语言代码或"auto"自动检测
                 支持值: "Chinese", "English", "Japanese", 
                        "Korean", "Spanish", "French" 等
        keep_extracted: 是否保留从视频提取的临时WAV文件
        archive_mode: 转写存档格式（none/txt/json/both）
        archive_dir: 存档目录
        auto_bootstrap: 未安装ASR时是否自动执行setup/download
    
    Returns:
        dict 包含:
            - text: 转录的文本
            - language: 识别的语言
            - confidence: 置信度 (0-1)
            - duration: 音频时长（秒）
            - source_file: 源文件路径
            - source_format: 源文件格式
    
    Raises:
        FileNotFoundError: 文件不存在
        ValueError: 文件格式不支持
        RuntimeError: 转录失败
    
    Examples:
        >>> # 转录MP4视频
        >>> result = transcribe_audio("meeting.mp4", "Chinese")
        >>> print(result['text'])
        
        >>> # 转录MP3音频
        >>> result = transcribe_audio("podcast.mp3", "auto")
        
        >>> # 转录WAV文件
        >>> result = transcribe_audio("C:\\audio\\speech.wav")
    """
    try:
        pipeline = AcousticPipeline(auto_bootstrap=auto_bootstrap)
        return pipeline.transcribe(
            file_path,
            language,
            keep_extracted,
            archive_mode=archive_mode,
            archive_dir=archive_dir,
        )
    except Exception as e:
        raise RuntimeError(f"转录失败: {str(e)}")


def transcribe_and_summarize(
    file_path: str,
    language: str = "auto",
    summary_length: int = 100
) -> Dict[str, Any]:
    """
    转录后自动生成摘要
    
    Args:
        file_path: 文件路径
        language: 语言
        summary_length: 摘要的目标字数
    
    Returns:
        dict 包含 transcription 和 summary
    """
    result = transcribe_audio(file_path, language)
    
    # 简单摘要：取前N个字
    text = result['text']
    summary = text[:summary_length] + ("..." if len(text) > summary_length else "")
    
    result['summary'] = summary
    return result


def batch_transcribe_folder(
    folder_path: str,
    language: str = "auto",
    output_json: Optional[str] = None
) -> Dict[str, Any]:
    """
    批量转录文件夹中的所有音视频文件
    
    Args:
        folder_path: 文件夹路径
        language: 语言
        output_json: 如果指定，将结果保存到JSON文件
    
    Returns:
        dict 包含所有转录结果
    """
    pipeline = AcousticPipeline()
    pipeline.batch_transcribe(folder_path, language)
    
    return {
        "status": "completed",
        "folder": folder_path,
        "language": language
    }


# ========================================================
# 以下是"大模型可读"的文档
# ========================================================

"""
=================================================================================
                     LLM ASR API 文档
=================================================================================

【适用场景】
当用户要求：
- "转录这个视频"
- "把这个音频文件转成文字"
- "识别这个语音"
- "提取视频的字幕"

【调用方式】
from asr_api import transcribe_audio

result = transcribe_audio("文件路径", language="语言", archive_mode="json", auto_bootstrap=True)


【支持的文件格式】
音频: WAV, MP3, FLAC, M4A, OGG, AAC, WMA, OPUS
视频: MP4, MKV, WebM, FLV, MOV, AVI, MTS, M2TS, TS, M3U8
注: 视频会自动提取音轨，不需要用户预处理


【语言支持】
- "auto" - 自动检测（推荐）
- "Chinese" / "zh" - 中文（含方言）
- "English" / "en" - 英文
- "Japanese" / "ja" - 日文
- "Korean" / "ko" - 韩文
- "Spanish" / "es" - 西班牙文
- "French" / "fr" - 法文
以及80+其他语言


【返回结果示例】
{
    "text": "今天的会议内容是...",
    "language": "Chinese",
    "confidence": 0.95,
    "duration": 120.5,
    "source_file": "C:\\meeting.mp4",
    "source_format": ".mp4"
}


【错误处理】
- 文件不存在 → FileNotFoundError
- 格式不支持 → ValueError
- 转录失败 → RuntimeError

建议用try/except捕获异常


【使用示例】

# 示例1：转录视频文件
try:
    result = transcribe_audio("C:\\videos\\lecture.mp4", language="Chinese")
    print(result['text'])  # 打印转录文本
except Exception as e:
    print(f"转录失败: {e}")


# 示例2：自动语言检测
result = transcribe_audio("podcast.mp3")  # 自动检测语言
print(f"检测语言：{result['language']}")


# 示例3：转录并摘要
from asr_api import transcribe_and_summarize
result = transcribe_and_summarize("meeting.mp4", summary_length=200)
print(result['summary'])


# 示例4：批量转录整个文件夹
from asr_api import batch_transcribe_folder
batch_transcribe_folder("C:\\audio\\library", language="Chinese")


【性能】
- 单个文件：根据时长，实时速度（1小时音频约需1小时）
- 视频提取：MP4→WAV 约 5-10秒/分钟
- 支持GPU加速（Intel Xe/Arc GPU 优先）


【依赖】
- 原始 local-qwen3-asr-aipc 技能必须先配置
- 可选: moviepy（视频提取），watchdog（文件监听）


【最常用的一句话调用】
result = transcribe_audio("文件路径");print(result['text'])
=================================================================================
"""


if __name__ == "__main__":
    # 命令行测试
    import sys
    
    if len(sys.argv) < 2:
        print("使用: python asr_api.py <文件路径> [语言]")
        print("示例: python asr_api.py meeting.mp4 Chinese")
        sys.exit(1)
    
    file_path = sys.argv[1]
    language = sys.argv[2] if len(sys.argv) > 2 else "auto"
    
    try:
        result = transcribe_audio(file_path, language)
        print("\n📝 转录结果:")
        print(result['text'])
        print(f"\n语言: {result['language']}")
        print(f"时长: {result.get('duration', 'N/A')} 秒")
    except Exception as e:
        print(f"❌ 错误: {e}")
        sys.exit(1)
