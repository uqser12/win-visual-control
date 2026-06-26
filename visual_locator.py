#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试模板匹配效果"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from visual_control import vc

print("=" * 50)
print("🧪 模板匹配测试")
print("=" * 50)

template_path = "wechat_icon.png"

if not os.path.exists(template_path):
    print("❌ 模板文件不存在")
    sys.exit(1)

print(f"\n模板文件: {template_path}")
print("正在进行模板匹配...\n")

# 测试不同置信度
for conf in [0.9, 0.8, 0.7, 0.6]:
    pos = vc.locator.find_template(template_path, threshold=conf)
    status = "✅ 找到" if pos else "❌ 未找到"
    print(f"阈值 {conf}: {status} - {pos}")

print("\n" + "=" * 50)
print("测试完成！")
print("=" * 50)
