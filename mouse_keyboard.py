#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通用图标学习工具 (v2)
用法: python learn_icon.py 图标名称  [位置x,y]

模式1: python learn_icon.py wechat
  -> 5秒倒计时, 用户把鼠标移到图标上, 自动截取保存

模式2: python learn_icon.py wechat 596 658
  -> 直接使用给定坐标, 无需倒计时 (AI调用模式)
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from visual_control import vc
from PIL import ImageGrab
import pyautogui
import time

ICONS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "icons")

def learn_icon(icon_name, x=None, y=None, size=50):
    """学习一个图标，保存为模板"""

    template_path = os.path.join(ICONS_DIR, f"{icon_name}_icon.png")

    print("=" * 50)
    print("Learning: %s" % icon_name)
    print("=" * 50)

    # 检查已存在
    if os.path.exists(template_path):
        print("Existing template found, overwriting...")

    if x is not None and y is not None:
        # AI调用模式: 直接使用坐标
        print("Using given position: (%d, %d)" % (x, y))
    else:
        # 人工模式: 倒计时5秒
        print("Move mouse to [%s] icon..." % icon_name)
        for i in range(5, 0, -1):
            print("%d..." % i, end=" ", flush=True)
            time.sleep(1)
        print("capturing!")
        x, y = pyautogui.position()

    print("Cursor at: (%d, %d)" % (x, y))

    # 截图
    left, top = x - size, y - size
    right, bottom = x + size, y + size
    screen_w, screen_h = pyautogui.size()
    left = max(0, left)
    top = max(0, top)
    right = min(screen_w, right)
    bottom = min(screen_h, bottom)

    os.makedirs(ICONS_DIR, exist_ok=True)
    icon_img = ImageGrab.grab(bbox=(left, top, right, bottom))
    icon_img.save(template_path)
    print("Template saved: %s (%s)" % (template_path, str(icon_img.size)))

    # 测试匹配
    print("Testing match...")
    pos = vc.locator.find_template(template_path, threshold=0.8)
    if pos:
        print("OK! Match at: %s" % str(pos))
    else:
        print("WARNING: match confidence low, may need relearn")

    print("=" * 50)
    print("Done: %s" % icon_name)
    return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python learn_icon.py <name>           # 5s countdown mode")
        print("  python learn_icon.py <name> <x> <y>   # direct coordinate mode")
        sys.exit(1)

    icon_name = sys.argv[1]
    x = int(sys.argv[2]) if len(sys.argv) > 2 else None
    y = int(sys.argv[3]) if len(sys.argv) > 3 else None
    learn_icon(icon_name, x, y)
