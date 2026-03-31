#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Acoustic Pipeline - 增强的ASR处理管道

基于原有的 Qwen3-ASR 技能，提供：
1. 视频音轨自动提取
2. 多格式支持（MP4、MP3、WAV等）
3. 自动化处理（文件夹监听或批量）
4. LLM直接调用接口

用法：
  python acoustic_pipeline.py --file "audio.mp4" --language Chinese
  python acoustic_pipeline.py --watch "C:\\inbox"
  python acoustic_pipeline.py --batch "C:\\audio\\library"
"""

import json
import subprocess
import sys
import argparse
import os
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any


class AcousticPipeline:
    """音视频转录管道"""
    
    # 支持的格式
    AUDIO_FORMATS = {'.wav', '.mp3', '.flac', '.m4a', '.ogg', '.aac', '.wma', '.opus'}
    VIDEO_FORMATS = {'.mp4', '.mkv', '.webm', '.flv', '.mov', '.avi', '.mts', '.m2ts', '.ts', '.m3u8'}
    ALL_FORMATS = AUDIO_FORMATS | VIDEO_FORMATS
    
    def __init__(self, asr_skill_dir: Optional[str] = None, auto_bootstrap: bool = False):
        """
        初始化管道

        Args:
            asr_skill_dir: 原始ASR技能的目录（默认为自动检测 *_openvino/asr）
            auto_bootstrap: 当未初始化ASR环境时是否自动执行 setup.py/download_model.py
        """
        if asr_skill_dir:
            self.asr_dir = Path(asr_skill_dir)
        else:
            # 自动扫描盘符查找 *_openvino/asr 目录
            self.asr_dir = self._find_openvino_asr_dir() or Path.cwd()
        self.state_file = self._find_state_json()
        self.venv_py = self._find_venv_python()

        self.runtime_asr_dir = self.asr_dir
        if self.state_file:
            try:
                state = json.loads(self.state_file.read_text(encoding="utf-8"))
                asr_runtime = Path(state.get("ASR_DIR", ""))
                if asr_runtime.exists():
                    self.runtime_asr_dir = asr_runtime
            except Exception:
                pass

        self.transcribe_py = self.runtime_asr_dir / 'transcribe.py'
        if not self.transcribe_py.exists():
            local_transcribe = self.asr_dir / 'transcribe.py'
            if local_transcribe.exists():
                self.transcribe_py = local_transcribe

        if not self.transcribe_py.exists() and auto_bootstrap:
            self._bootstrap_asr_skill()
            self.state_file = self._find_state_json()
            self.venv_py = self._find_venv_python()

            self.runtime_asr_dir = self.asr_dir
            if self.state_file:
                try:
                    state = json.loads(self.state_file.read_text(encoding="utf-8"))
                    asr_runtime = Path(state.get("ASR_DIR", ""))
                    if asr_runtime.exists():
                        self.runtime_asr_dir = asr_runtime
                except Exception:
                    pass
            self.transcribe_py = self.runtime_asr_dir / 'transcribe.py'

        if not self.transcribe_py.exists():
            raise FileNotFoundError(
                "找不到 transcribe.py。请确保ASR已初始化，或使用 --auto-bootstrap 自动初始化。\n"
                f"检查路径: {self.runtime_asr_dir / 'transcribe.py'}"
            )
    
    def _find_venv_python(self) -> Path:
        """查找虚拟环境的Python"""
        # 从state.json查找
        state_file = self._find_state_json()
        if state_file:
            try:
                state = json.loads(state_file.read_text())
                venv_py = Path(state.get('VENV_PY', ''))
                if venv_py.exists():
                    return venv_py
            except:
                pass
        
        # 降级：尝试常见位置
        username = os.environ.get('USERNAME', 'user').lower()
        common_paths = [
            Path.home() / f"{username}_openvino" / "venv" / "Scripts" / "python.exe",
            self.asr_dir / "venv" / "Scripts" / "python.exe",
            Path(sys.executable)  # 最后用系统Python
        ]
        
        for path in common_paths:
            if path.exists():
                return path
        
        return Path(sys.executable)
    
    def _find_openvino_asr_dir(self) -> Optional[Path]:
        """自动扫描盘符查找 *_openvino/asr 目录"""
        import string

        for drive in string.ascii_uppercase:
            base_path = Path(f"{drive}:\\")
            if not base_path.exists():
                continue
            
            # 扫描该盘下的 *_openvino/asr 目录
            try:
                for item in base_path.iterdir():
                    if item.is_dir() and "_openvino" in item.name:
                        asr_candidate = item / "asr"
                        if asr_candidate.exists():
                            return asr_candidate
            except PermissionError:
                continue

        return None

    def _find_state_json(self) -> Optional[Path]:
        """查找state.json"""
        import string

        username = os.environ.get('USERNAME', 'user').lower()

        for drive in string.ascii_uppercase:
            state_file = Path(f"{drive}:\\{username}_openvino\\asr\\state.json")
            if state_file.exists():
                return state_file

        local_state = self.asr_dir / "state.json"
        if local_state.exists():
            return local_state

        return None

    def _run_bootstrap_script(self, script_name: str):
        """执行初始化脚本"""
        script_path = self.asr_dir / script_name
        if not script_path.exists():
            raise FileNotFoundError(f"缺少初始化脚本: {script_path}")

        cmd = [str(Path(sys.executable)), str(script_path)]
        # 在ASR目录下执行脚本，确保生成的文件在正确的位置
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True, 
            timeout=1800,
            cwd=str(self.asr_dir)  # 在ASR目录下执行
        )
        if result.returncode != 0:
            raise RuntimeError(
                f"执行 {script_name} 失败:\n{result.stderr or result.stdout}"
            )

    def _bootstrap_asr_skill(self):
        """当客户未安装ASR时，自动初始化环境和模型"""
        print("⚙️ 检测到ASR未初始化，开始自动执行 setup.py ...")
        self._run_bootstrap_script("setup.py")
        print("⚙️ 开始自动执行 download_model.py ...")
        self._run_bootstrap_script("download_model.py")

    def _archive_transcript(
        self,
        source_file: Path,
        result: Dict[str, Any],
        archive_mode: str = "none",
        archive_dir: Optional[str] = None,
    ) -> Dict[str, str]:
        """按指定格式保存转写结果"""
        if archive_mode == "none":
            return {}

        out_dir = Path(archive_dir) if archive_dir else source_file.parent / "transcripts"
        out_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = f"{source_file.stem}_{timestamp}"
        saved = {}

        if archive_mode in {"txt", "both"}:
            txt_path = out_dir / f"{base_name}.txt"
            txt_path.write_text(str(result.get("text", "")), encoding="utf-8")
            saved["txt"] = str(txt_path)

        if archive_mode in {"json", "both"}:
            json_path = out_dir / f"{base_name}.json"
            json_path.write_text(
                json.dumps(result, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            saved["json"] = str(json_path)

        return saved

    def _is_video(self, file_path: Path) -> bool:
        """检查是否是视频文件"""
        return file_path.suffix.lower() in self.VIDEO_FORMATS
    
    def _is_audio(self, file_path: Path) -> bool:
        """检查是否是音频文件"""
        return file_path.suffix.lower() in self.AUDIO_FORMATS
    
    def _extract_audio_from_video(self, video_path: Path, output_wav: Optional[Path] = None) -> Path:
        """
        从视频文件提取音频
        
        Args:
            video_path: 视频文件路径
            output_wav: 输出WAV文件路径（如果为None自动生成）
        
        Returns:
            输出WAV文件路径
        """
        if output_wav is None:
            output_wav = video_path.parent / f"{video_path.stem}_audio.wav"
        
        print(f"  📹 提取音频: {video_path.name}...")
        
        # 尝试使用ffmpeg（最可靠）
        try:
            cmd = [
                'ffmpeg',
                '-i', str(video_path),
                '-q:a', '9',
                '-n',  # 不覆盖
                str(output_wav)
            ]
            result = subprocess.run(cmd, capture_output=True, timeout=300)
            
            if result.returncode == 0 and output_wav.exists():
                print(f"  ✅ 音频已提取: {output_wav.name}")
                return output_wav
        except:
            pass
        
        # 降级：使用moviepy（较慢但可靠）
        try:
            from moviepy.editor import VideoFileClip
            
            print(f"  🎬 使用moviepy提取（可能较慢）...")
            clip = VideoFileClip(str(video_path))
            if clip.audio is None:
                raise ValueError("视频没有音频轨道")
            
            clip.audio.write_audiofile(str(output_wav), verbose=False, logger=None)
            clip.close()
            
            print(f"  ✅ 音频已提取: {output_wav.name}")
            return output_wav
        except ImportError:
            raise RuntimeError(
                "需要ffmpeg或moviepy来提取视频音频\n"
                "安装: pip install moviepy\n"
                "或下载ffmpeg: https://ffmpeg.org/download.html"
            )
        except Exception as e:
            raise RuntimeError(f"音频提取失败: {e}")
    
    def transcribe(
        self,
        file_path: str,
        language: str = "auto",
        keep_extracted: bool = False,
        archive_mode: str = "none",
        archive_dir: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        转录音视频文件
        
        Args:
            file_path: 文件路径
            language: 语言（默认自动检测）
            keep_extracted: 是否保留提取的WAV文件
            archive_mode: 存档格式（none/txt/json/both）
            archive_dir: 存档目录（默认 source_file 同目录下 transcripts）
        
        Returns:
            转录结果
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"文件不存在: {file_path}")
        
        print(f"\n🎙️  开始转录: {file_path.name}")
        
        # 准备音频文件
        audio_file = file_path
        if self._is_video(file_path):
            audio_file = self._extract_audio_from_video(file_path)
        elif not self._is_audio(file_path):
            raise ValueError(f"不支持的文件格式: {file_path.suffix}")
        
        # 调用原始的transcribe.py
        print(f"  🔄 转录中...")
        
        cmd = [
            str(self.venv_py),
            str(self.transcribe_py),
            '--audio', str(audio_file),
            '--language', language
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            
            if result.returncode != 0:
                raise RuntimeError(f"转录失败: {result.stderr}")
            
            # 尝试解析JSON输出
            try:
                transcription = json.loads(result.stdout)
            except:
                # 如果不是JSON，就把输出当作文本
                transcription = {
                    "text": result.stdout.strip(),
                    "language": language,
                    "confidence": None
                }
            
            # 补充元数据
            transcription['source_file'] = str(file_path)
            transcription['source_format'] = file_path.suffix

            # 存档输出（给客户保留转写记录）
            archived = self._archive_transcript(
                source_file=file_path,
                result=transcription,
                archive_mode=archive_mode,
                archive_dir=archive_dir,
            )
            if archived:
                transcription['archive_files'] = archived

            # 清理临时文件
            if not keep_extracted and audio_file != file_path:
                try:
                    audio_file.unlink()
                except:
                    pass
            
            print(f"  ✅ 转录完成")
            
            return transcription
            
        except subprocess.TimeoutExpired:
            raise RuntimeError("转录超时（文件太大或系统繁忙）")
        except Exception as e:
            raise RuntimeError(f"转录过程出错: {e}")
    
    def batch_transcribe(
        self,
        folder_path: str,
        language: str = "auto",
        archive_mode: str = "none",
        archive_dir: Optional[str] = None,
    ):
        """
        批量转录文件夹中的所有音视频文件
        
        Args:
            folder_path: 文件夹路径
            language: 语言
        """
        folder = Path(folder_path)
        files = []
        
        for ext in self.ALL_FORMATS:
            files.extend(folder.rglob(f'*{ext}'))
            files.extend(folder.rglob(f'*{ext.upper()}'))
        
        print(f"\n📁 发现 {len(set(files))} 个音视频文件")
        
        for idx, file_path in enumerate(sorted(set(files)), 1):
            print(f"\n[{idx}/{len(set(files))}]", end=" ")
            try:
                result = self.transcribe(
                    str(file_path),
                    language,
                    archive_mode=archive_mode,
                    archive_dir=archive_dir,
                )
                print(f"转录: {result['text'][:50]}...")
            except Exception as e:
                print(f"❌ 错误: {e}")
    
    def watch_folder(
        self,
        folder_path: str,
        language: str = "auto",
        archive_mode: str = "none",
        archive_dir: Optional[str] = None,
    ):
        """
        监听文件夹，自动转录新文件
        
        Args:
            folder_path: 要监听的文件夹
            language: 语言
        """
        try:
            from watchdog.observers import Observer
            from watchdog.events import FileSystemEventHandler, FileCreatedEvent
        except ImportError:
            raise RuntimeError("需要watchdog: pip install watchdog")
        
        folder = Path(folder_path)
        processed = set()
        pipeline_self = self
        supported_formats = self.ALL_FORMATS
        
        class AudioHandler(FileSystemEventHandler):
            def on_created(self, event: FileCreatedEvent):
                if event.is_directory:
                    return
                
                file_path = Path(event.src_path)
                if file_path.suffix.lower() not in supported_formats:
                    return
                
                # 简单的文件完成检测
                import time
                time.sleep(1)
                
                file_key = str(file_path.resolve())
                if file_key in processed:
                    return
                
                processed.add(file_key)
                
                try:
                    result = pipeline_self.transcribe(
                        str(file_path),
                        language,
                        archive_mode=archive_mode,
                        archive_dir=archive_dir,
                    )
                    print(f"转录: {result.get('text', '')[:80]}...")
                except Exception as e:
                    print(f"❌ 错误: {e}")
        
        print(f"🎙️  监听中: {folder}")
        print("按 Ctrl+C 停止")
        
        handler = AudioHandler()
        observer = Observer()
        observer.schedule(handler, str(folder), recursive=True)
        observer.start()
        
        try:
            while True:
                import time
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n停止监听")
            observer.stop()
            observer.join()


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description='音视频自动转录管道',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  python acoustic_pipeline.py --file meeting.mp4 --language Chinese
  python acoustic_pipeline.py --watch "C:\\inbox"
  python acoustic_pipeline.py --batch "C:\\audio"
        '''
    )
    
    parser.add_argument('--file', help='转录单个文件')
    parser.add_argument('--watch', help='监听文件夹并自动转录')
    parser.add_argument('--batch', help='批量转录文件夹')
    parser.add_argument('--language', default='auto', help='语言（默认自动检测）')
    parser.add_argument('--dir', help='ASR技能目录（默认为当前目录）')
    parser.add_argument('--keep-audio', action='store_true', help='保留提取的音频文件')
    parser.add_argument('--archive', choices=['none', 'txt', 'json', 'both'], default='none', help='转写存档格式')
    parser.add_argument('--archive-dir', help='转写存档目录（默认源文件目录下 transcripts）')
    parser.add_argument('--auto-bootstrap', action='store_true', help='未安装ASR时自动执行 setup.py + download_model.py')
    
    args = parser.parse_args()
    
    try:
        pipeline = AcousticPipeline(args.dir, auto_bootstrap=args.auto_bootstrap)

        if args.file:
            result = pipeline.transcribe(
                args.file,
                args.language,
                args.keep_audio,
                archive_mode=args.archive,
                archive_dir=args.archive_dir,
            )
            print("\n📝 转录结果:")
            print(result['text'])
            print(f"\nℹ️  元数据: {json.dumps({k: v for k, v in result.items() if k != 'text'}, ensure_ascii=False, indent=2)}")
            
        elif args.watch:
            pipeline.watch_folder(
                args.watch,
                args.language,
                archive_mode=args.archive,
                archive_dir=args.archive_dir,
            )

        elif args.batch:
            pipeline.batch_transcribe(
                args.batch,
                args.language,
                archive_mode=args.archive,
                archive_dir=args.archive_dir,
            )
            
        else:
            parser.print_help()
            
    except Exception as e:
        print(f"❌ 错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
