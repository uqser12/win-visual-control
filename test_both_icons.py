#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
四级智能方案打开微信：
1. 模板匹配（最精准，已学习的图标）
2. OCR文字识别
3. 颜色识图
4. Win键搜索（兜底）
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
print("🚀 微信自动启动 - 四级智能识别方案")
print("=" * 60)

wechat_pos = None
method_used = ""
template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "wechat_icon.png")

# ========== 方案1: 模板匹配（最精准）==========
if os.path.exists(template_path):
    print("\n🖼️  【方案 1/4】模板匹配 - 精准识别微信图标...")
    try:
        wechat_pos = vc.locator.find_template(template_path, threshold=0.8)
        if wechat_pos:
            method_used = "模板匹配"
            print(f"✅ 精准定位到微信图标: {wechat_pos}")
        else:
            print("❌ 模板匹配未找到，尝试方案2...")
    except Exception as e:
        print(f"❌ 模板匹配出错: {e}")
else:
    print("\n🖼️  【方案 1/4】模板匹配 - 无模板，跳过")

# ========== 方案2: OCR 文字识别 ==========
if not wechat_pos:
    print("\n🔍 【方案 2/4】OCR 文字识别...")
    try:
        wechat_pos = vc.locator.find_text("微信")
        if wechat_pos:
            method_used = "OCR文字识别"
            print(f"✅ 找到微信图标位置: {wechat_pos}")
        else:
            print("❌ OCR 未识别到'微信'文字")
    except Exception as e:
        print(f"❌ OCR 出错: {e}")

# ========== 方案3: 颜色识图 ==========
if not wechat_pos:
    print("\n🎨 【方案 3/4】颜色识图 - 查找绿色微信图标...")
    try:
        screen = ImageGrab.grab()
        screen_np = np.array(screen)
        w, h = screen.size
        
        # 只搜索左侧 300 像素区域
        search_area = screen_np[:, :300, :]
        
        # 微信绿色范围
        lower_green = np.array([0, 150, 50])
        upper_green = np.array([100, 255, 150])
        
        mask = np.all((search_area >= lower_green) & (search_area <= upper_green), axis=2)
        green_pixels = np.where(mask)
        
        if len(green_pixels[0]) > 100:
            center_y = int(np.mean(green_pixels[0]))
            center_x = int(np.mean(green_pixels[1]))
            wechat_pos = (center_x, center_y)
            method_used = "颜色识图"
            print(f"✅ 通过绿色识别找到微信图标: {wechat_pos}")
            print(f"   绿色像素数量: {len(green_pixels[0])}")
        else:
            print(f"❌ 未找到足够的绿色区域")
    except Exception as e:
        print(f"❌ 颜色识图出错: {e}")

# ========== 方案4: Win 键搜索 ==========
if not wechat_pos:
    print("\n⌨️  【方案 4/4】Win 键搜索打开微信...")
    try:
        success = vc.open_app("微信", wait_after=5.0)
        method_used = "Win键搜索"
        if success:
            print("✅ 通过 Win 键搜索成功启动微信！")
        else:
            print("⚠️  Win 键方案执行，请检查微信是否启动")
    except Exception as e:
        print(f"❌ Win 键方案出错: {e}")
        method_used = "全部失败"

# 如果找到了图标位置，双击打开
if wechat_pos and method_used != "Win键搜索":
    print(f"\n🖱️  使用 [{method_used}] 定位成功，正在双击打开...")
    try:
        vc.ctrl.mouse.double_click(wechat_pos[0], wechat_pos[1])
        
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
            print("\n⚠️  未检测到微信窗口，可能正在启动中...")
            
    except Exception as e:
        print(f"❌ 点击操作出错: {e}")

# 截图留证
vc.screenshot(save=True, filename="result_v4.png")

print("\n" + "=" * 60)
print(f"📊 最终使用方案: {method_used}")
print("=" * 60)
