#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信图标学习模式
用户将鼠标移动到微信图标上，按回车确认，程序自动：
1. 记录图标位置
2. 截图保存为模板
3. 双击打开
4. 下次自动用模板匹配识别
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from visual_control import vc
from PIL import ImageGrab
import pyautogui
import time
import pygetwindow as gw

print("=" * 60)
print("📚 微信图标学习模式")
print("=" * 60)
print("\n请将鼠标移动到【微信图标】上...")
print("（提示：把鼠标指针放在图标正中间）")

# 倒计时 5 秒
for i in range(5, 0, -1):
    print(f"\r⏳ {i} 秒后自动获取位置...", end="", flush=True)
    time.sleep(1)
print("\r✅ 时间到！正在获取位置...    ")

# 获取当前鼠标位置
x, y = pyautogui.position()
print(f"\n✅ 已记录位置: ({x}, {y})")

# 截图该区域作为模板（图标周围 50x50 像素范围）
print("\n📸 正在截取图标区域作为模板...")
icon_size = 50  # 图标大小范围
left = x - icon_size
top = y - icon_size
right = x + icon_size
bottom = y + icon_size

# 确保不超出屏幕范围
screen_w, screen_h = pyautogui.size()
left = max(0, left)
top = max(0, top)
right = min(screen_w, right)
bottom = min(screen_h, bottom)

# 截图
icon_img = ImageGrab.grab(bbox=(left, top, right, bottom))

# 保存模板
template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "wechat_icon.png")
icon_img.save(template_path)
print(f"✅ 模板已保存: {template_path}")
print(f"   模板尺寸: {icon_img.size}")

# 双击打开微信
print("\n🖱️  正在双击打开微信...")
vc.ctrl.mouse.double_click(x, y)

# 等待启动
print("⏳ 等待微信启动 (5秒)...")
time.sleep(5)

# 验证
windows = gw.getWindowsWithTitle("微信")
if not windows:
    windows = gw.getWindowsWithTitle("WeChat")

if windows:
    print(f"\n🎉 微信已成功打开！")
    print(f"   窗口标题: {windows[0].title}")
else:
    print("\n⚠️  未检测到微信窗口，可能正在启动中，请稍候...")

print("\n" + "=" * 60)
print("✅ 学习完成！下次打开微信将自动使用模板匹配精准定位")
print("=" * 60)
