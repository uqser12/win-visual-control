#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试两个图标调换位置后的识别效果"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from visual_control import vc
import time
import pygetwindow as gw

print("=" * 60)
print("🧪 双图标位置调换测试")
print("=" * 60)

icons = [
    ("微信", "wechat_icon.png"),
    ("无影云电脑", "wuying_icon.png"),
]

results = {}

for name, template in icons:
    print(f"\n{'='*50}")
    print(f"🔍 正在识别: {name}")
    print(f"{'='*50}")
    
    if not os.path.exists(template):
        print(f"❌ 模板文件不存在: {template}")
        continue
    
    pos = vc.locator.find_template(template, threshold=0.8)
    if pos:
        results[name] = pos
        print(f"✅ 找到！位置: {pos}")
    else:
        print(f"❌ 未找到")

print(f"\n{'='*60}")
print("📊 识别结果汇总")
print(f"{'='*60}")
for name, pos in results.items():
    print(f"  {name}: {pos}")

# 问用户要不要都打开
print(f"\n{'='*60}")
print("是否要双击打开这两个软件？(y/n)")
print(f"{'='*60}")

# 自动打开两个
print("\n🖱️  正在依次打开...")

for name, pos in results.items():
    print(f"\n👉 打开 {name}...")
    vc.ctrl.mouse.double_click(pos[0], pos[1])
    time.sleep(2)

print("\n⏳ 等待启动 (5秒)...")
time.sleep(5)

# 验证窗口
print("\n🪟 窗口检测结果:")
all_windows = gw.getAllWindows()
for name, _ in results.items():
    matched = [w for w in all_windows if name[:2] in w.title]
    if matched:
        print(f"  ✅ {name}: 已打开")
        for w in matched[:2]:
            print(f"     - {w.title}")
    else:
        print(f"  ⚠️  {name}: 未检测到窗口（可能正在启动）")

print("\n" + "=" * 60)
print("🎉 测试完成！")
print("=" * 60)
