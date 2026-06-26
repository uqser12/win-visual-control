#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试：自动查找无影云电脑图标
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from visual_control import vc
from PIL import ImageGrab
import numpy as np
import time
import pygetwindow as gw

print("=" * 60)
print("🔍 自动查找: 无影云电脑")
print("=" * 60)

target = "无影云电脑"
found_pos = None
method_used = ""

# ========== 方案1: OCR 文字识别 ==========
print(f"\n🔍 【方案1】OCR 文字识别 - 查找'{target}'...")
try:
    # 试试完整名称
    pos = vc.locator.find_text(target)
    if pos:
        found_pos = pos
        method_used = "OCR-完整名称"
        print(f"✅ 找到: {pos}")
    else:
        # 试试简称
        for short_name in ["无影", "云电脑"]:
            pos = vc.locator.find_text(short_name)
            if pos:
                found_pos = pos
                method_used = f"OCR-简称'{short_name}'"
                print(f"✅ 通过简称'{short_name}'找到: {pos}")
                break
        
        if not found_pos:
            print("❌ OCR 未找到")
except Exception as e:
    print(f"❌ OCR 出错: {e}")

# ========== 方案2: 颜色识图（找绿色图标）==========
if not found_pos:
    print(f"\n🎨 【方案2】颜色识图 - 查找绿色图标...")
    try:
        screen = ImageGrab.grab()
        screen_np = np.array(screen)
        w, h = screen.size
        
        # 搜索左侧 300 像素区域
        search_area = screen_np[:, :300, :]
        
        # 绿色范围
        lower_green = np.array([0, 150, 50])
        upper_green = np.array([100, 255, 150])
        
        mask = np.all((search_area >= lower_green) & (search_area <= upper_green), axis=2)
        green_pixels = np.where(mask)
        
        if len(green_pixels[0]) > 100:
            # 找到所有绿色区域的聚类中心
            # 简单处理：找所有绿色像素的分组
            print(f"   找到 {len(green_pixels[0])} 个绿色像素")
            
            # 计算中心
            center_y = int(np.mean(green_pixels[0]))
            center_x = int(np.mean(green_pixels[1]))
            found_pos = (center_x, center_y)
            method_used = "颜色识图"
            print(f"✅ 找到绿色区域中心: {found_pos}")
        else:
            print(f"❌ 未找到足够的绿色区域")
    except Exception as e:
        print(f"❌ 颜色识图出错: {e}")

# ========== 方案3: Win 键搜索 ==========
if not found_pos:
    print(f"\n⌨️  【方案3】Win 键搜索...")
    try:
        success = vc.open_app(target, wait_after=5.0)
        method_used = "Win键搜索"
        if success:
            print(f"✅ 通过 Win 键搜索成功启动！")
        else:
            print("⚠️  Win 键方案执行")
    except Exception as e:
        print(f"❌ Win 键出错: {e}")
        method_used = "全部失败"

# 如果找到了位置，双击打开
if found_pos and method_used != "Win键搜索":
    print(f"\n🖱️  使用 [{method_used}] 定位，正在双击打开...")
    try:
        vc.ctrl.mouse.double_click(found_pos[0], found_pos[1])
        
        print("⏳ 等待启动 (5秒)...")
        time.sleep(5)
        
        # 验证
        windows = gw.getWindowsWithTitle(target)
        if windows:
            print(f"\n🎉 {target} 已成功打开！")
            print(f"   窗口标题: {windows[0].title}")
        else:
            # 试试部分匹配
            all_windows = gw.getAllWindows()
            matched = [w for w in all_windows if "无影" in w.title or "云电脑" in w.title]
            if matched:
                print(f"\n🎉 找到相关窗口！")
                for w in matched[:3]:
                    print(f"   - {w.title}")
            else:
                print(f"\n⚠️  未检测到窗口，可能正在启动中...")
            
    except Exception as e:
        print(f"❌ 点击出错: {e}")

# 截图
vc.screenshot(save=True, filename="wuying_test.png")

print("\n" + "=" * 60)
print(f"📊 最终使用方案: {method_used}")
print(f"📍 定位位置: {found_pos}")
print("=" * 60)
