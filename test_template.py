#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
smart_click.py — 智能点击模块 v2.0
=====================================
模板匹配失败 → 输出 MISSING_TEMPLATE 标记 → AI 向用户要截图 → 用户发截图 → AI 存为模板 → 重试

设计理念:
  找不到 → 问用户要截图（不是倒计时） → 用户从容截图 → 学到手 → 以后直接用

用法:
    from smart_click import SmartClick
    sc = SmartClick()

    # 点搜索框 — 有模板直接用，没有就报 MISSING_TEMPLATE
    ok = sc.click("search_box", r"icons/wechat_search_box.png", "搜索框")

    # 用户给了截图后，AI 用这个接口存模板:
    sc.learn_from_image("search_box", r"C:/screenshot.png")

    # 再跑一次 sc.click() 就能找到了
"""

import os, sys, time, logging

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SKILL_DIR)
from visual_control import vc

log = logging.getLogger("SmartClick")

ICONS_DIR = os.path.join(os.path.dirname(SKILL_DIR), "icons")

MISSING_PREFIX = "[SmartClick] MISSING_TEMPLATE:"


class SmartClick:
    """智能点击器 — 模板优先，找不到就问用户要截图。"""

    def __init__(self, threshold=0.8):
        self.threshold = threshold
        self.missing_list = []  # 本轮缺失的模板列表
        os.makedirs(ICONS_DIR, exist_ok=True)

    # ── 核心方法 ──────────────────────────

    def click(self, name, template_path, label="",
              action="click", double=False):
        """
        尝试模板匹配点击。

        name:          模板名 (如 "wechat_search_box")
        template_path: 模板文件路径 (相对于技能根目录或绝对路径)
        label:         中文描述 (如 "微信搜索框")
        action:        "click" | "move"
        double:        是否双击

        返回:
          True  — 找到并点击成功
          False — 找不到，已输出 MISSING_TEMPLATE 标记，等用户截图
        """
        if not label:
            label = name

        # 路径补全
        if not os.path.isabs(template_path):
            template_path = os.path.join(os.path.dirname(SKILL_DIR), template_path)

        # 1) 尝试模板匹配
        if os.path.exists(template_path):
            pos = vc.locator.find_template(template_path, threshold=self.threshold)
            if pos:
                log.info("[SmartClick] %s found at %s" % (label, pos))
                self._do_action(pos, action, double)
                return True
            else:
                log.warning("[SmartClick] %s template exists but match FAILED (conf < %.2f)" % (label, self.threshold))
        else:
            log.info("[SmartClick] %s template file missing: %s" % (label, template_path))

        # 2) 标记缺失，等用户截图
        self.missing_list.append({"name": name, "label": label, "path": template_path})
        print("\n%s %s | save_to=%s" % (MISSING_PREFIX, label, template_path))
        return False

    def click_many(self, buttons):
        """
        批量点击。遇到第一个缺失就停止并报 MISSING_TEMPLATE。
        等用户给完截图后可以重跑。
        """
        for i, btn in enumerate(buttons):
            ok = self.click(
                btn["name"], btn["path"], btn.get("label", ""),
                action=btn.get("action", "click"),
                double=btn.get("double", False)
            )
            if not ok:
                log.error("[SmartClick] Stopped at #%d: %s" % (i, btn.get("label", "")))
                return False
            time.sleep(0.8)
        return True

    # ── 学习接口（AI 拿到用户截图后调用） ──

    def learn_from_image(self, name, source_image_path, template_path=None):
        """
        用户提供了截图 → 直接存为模板。

        name:              模板名
        source_image_path: 用户提供的截图路径
        template_path:     目标保存路径 (默认 icons/{name}_icon.png)
        """
        from PIL import Image

        if template_path is None:
            template_path = os.path.join(ICONS_DIR, "%s_icon.png" % name)
        elif not os.path.isabs(template_path):
            template_path = os.path.join(os.path.dirname(SKILL_DIR), template_path)

        # 读取 → 保存
        img = Image.open(source_image_path)
        img.save(template_path)
        log.info("[SmartClick] Template saved: %s (%s)" % (template_path, str(img.size)))

        # 自测
        pos = vc.locator.find_template(template_path, threshold=self.threshold)
        if pos:
            log.info("[SmartClick] Self-test PASS at %s" % str(pos))
            return True
        else:
            log.warning("[SmartClick] Self-test FAIL — template may not match current screen")
            return False

    def has_missing(self):
        """本轮是否有缺失的模板"""
        return len(self.missing_list) > 0

    def get_missing_labels(self):
        """返回缺失模板的中文描述列表"""
        return [m["label"] for m in self.missing_list]

    def clear_missing(self):
        """清空缺失列表"""
        self.missing_list = []

    # ── 内部 ────────────────────────────────

    def _do_action(self, pos, action, double):
        x, y = pos
        if action == "move":
            vc.ctrl.mouse.move_to(x, y, duration=0.6)
        elif double:
            vc.ctrl.mouse.double_click(x, y)
        else:
            vc.ctrl.mouse.click(x, y)


# ── 便捷单例 ──

_sc = None

def get_smart_click():
    global _sc
    if _sc is None:
        _sc = SmartClick()
    return _sc


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s", datefmt="%H:%M:%S")
    sc = SmartClick()
    print("SmartClick v2.0 ready.")
