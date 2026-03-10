#!/usr/bin/env python3
"""美团CLI入口"""
import sys
from meituan import main
import asyncio

if __name__ == "__main__":
    asyncio.run(main())
