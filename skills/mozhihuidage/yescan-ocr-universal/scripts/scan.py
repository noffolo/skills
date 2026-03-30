#!/usr/bin/env python3
"""Quark OCR - 夸克扫描王 OCR 识别服务"""
import sys
from pathlib import Path

# 导入公共模块 - 同级目录（发布版本）
SCRIPTS_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS_DIR))

from common import run_ocr

if __name__ == "__main__":
    run_ocr()
