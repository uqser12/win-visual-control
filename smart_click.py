#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
mouse_keyboard.py
鼠标键盘控制模块 / Mouse & Keyboard Control Module

功能 / Features:
  - 鼠标：移动、单击、双击、右键、拖拽、滚轮
  - 键盘：输入文字、按键、快捷键组合、粘贴
  - 贝塞尔曲线移动（拟人化）/ Human-like Bezier mouse movement
  - focus_lock 防焦点丢失保护 / Focus lock protection
  - 内置延迟与安全边距 / Built-in delay and safety margins

依赖 / Dependencies:
  pip install pyautogui pywin32
"""

import time
import math
import random
import logging
from typing import Optional, Tuple

import pyautogui
import win32api
import win32con
import win32gui

log = logging.getLogger("MouseKeyboard")

# 安全设置：移动到屏幕左上角可紧急停止
pyautogui.FAILSAFE = True
# 默认操作间隔 / Default action interval
pyautogui.PAUSE = 0.05


# ────────────────────────────────────────────────
# 鼠标控制 / Mouse Control
# ────────────────────────────────────────────────

class MouseController:
    """
    鼠标控制器，支持人性化移动与各类点击操作。
    Mouse controller with human-like movement and click operations.
    """

    def __init__(self, human_like: bool = True, speed: float = 0.3):
        """
        human_like: 启用贝塞尔曲线模拟人类移动轨迹
        speed:      移动速度系数（秒），越大越慢
        """
        self.human_like = human_like
        self.speed = speed

    def move_to(self, x: int, y: int, duration: Optional[float] = None):
        """移动鼠标到指定坐标 / Move mouse to (x, y)."""
        dur = duration if duration is not None else self.speed
        if self.human_like:
            self._bezier_move(x, y, dur)
        else:
            pyautogui.moveTo(x, y, duration=dur)
        log.info(f"鼠标移到 / Mouse moved to ({x}, {y})")

    def click(self, x: int, y: int, button: str = "left", delay: float = 0.05):
        """
        单击指定坐标 / Single click at (x, y).
        button: 'left' | 'right' | 'middle'
        """
        self.move_to(x, y)
        time.sleep(delay)
        pyautogui.click(x, y, button=button)
        log.info(f"单击 / Click ({x}, {y}) [{button}]")

    def double_click(self, x: int, y: int, delay: float = 0.05):
        """双击 / Double click."""
        self.move_to(x, y)
        time.sleep(delay)
        pyautogui.doubleClick(x, y)
        log.info(f"双击 / Double click ({x}, {y})")

    def right_click(self, x: int, y: int):
        """右键单击 / Right click."""
        self.click(x, y, button="right")

    def drag_to(
        self,
        from_x: int, from_y: int,
        to_x: int, to_y: int,
        duration: float = 0.5,
        button: str = "left",
    ):
        """拖拽 / Drag from source to destination."""
        self.move_to(from_x, from_y)
        pyautogui.mouseDown(button=button)
        time.sleep(0.05)
        pyautogui.moveTo(to_x, to_y, duration=duration)
        pyautogui.mouseUp(button=button)
        log.info(f"拖拽 / Drag ({from_x},{from_y}) -> ({to_x},{to_y})")

    def scroll(self, x: int, y: int, clicks: int = 3):
        """
        滚轮滚动 / Scroll wheel.
        clicks > 0 向上滚，< 0 向下滚 / positive=up, negative=down
        """
        self.move_to(x, y)
        pyautogui.scroll(clicks, x=x, y=y)
        log.info(f"滚轮 / Scroll ({x},{y}) clicks={clicks}")

    # ── 贝塞尔曲线移动 / Bezier Move ──────────────

    @staticmethod
    def _bezier_move(end_x: int, end_y: int, duration: float):
        """人性化贝塞尔曲线轨迹移动 / Human-like Bezier curve movement."""
        start_x, start_y = pyautogui.position()
        # 随机控制点 / Random control points
        cp1_x = start_x + random.randint(-50, 50) + (end_x - start_x) // 3
        cp1_y = start_y + random.randint(-50, 50) + (end_y - start_y) // 3
        cp2_x = start_x + random.randint(-30, 30) + 2 * (end_x - start_x) // 3
        cp2_y = start_y + random.randint(-30, 30) + 2 * (end_y - start_y) // 3

        steps = max(20, int(duration * 60))
        for i in range(steps + 1):
            t = i / steps
            # 三次贝塞尔公式 / Cubic Bezier formula
            x = (
                (1 - t) ** 3 * start_x
                + 3 * (1 - t) ** 2 * t * cp1_x
                + 3 * (1 - t) * t ** 2 * cp2_x
                + t ** 3 * end_x
            )
            y = (
                (1 - t) ** 3 * start_y
                + 3 * (1 - t) ** 2 * t * cp1_y
                + 3 * (1 - t) * t ** 2 * cp2_y
                + t ** 3 * end_y
            )
            pyautogui.moveTo(int(x), int(y))
            time.sleep(duration / steps)


# ────────────────────────────────────────────────
# 键盘控制 / Keyboard Control
# ────────────────────────────────────────────────

class KeyboardController:
    """
    键盘控制器，支持打字、快捷键与粘贴。
    Keyboard controller supporting typing, shortcuts, and paste.
    """

    def __init__(self, interval: float = 0.05, focus_lock: bool = True):
        """
        interval:   按键间隔（秒）/ keystroke interval
        focus_lock: 打字前检查并锁定焦点 / check & lock focus before typing
        """
        self.interval = interval
        self.focus_lock = focus_lock
        self._locked_hwnd: Optional[int] = None

    def type_text(self, text: str, use_paste: bool = False):
        """
        输入文字 / Type text.
        use_paste=True 时用剪贴板粘贴（支持中文）/ use clipboard for Chinese
        """
        if self.focus_lock and self._locked_hwnd:
            self._restore_focus()

        if use_paste:
            import win32clipboard
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardText(text, win32clipboard.CF_UNICODETEXT)
            win32clipboard.CloseClipboard()
            pyautogui.hotkey("ctrl", "v")
            log.info(f"粘贴输入 / Pasted: {text[:30]}...")
        else:
            pyautogui.typewrite(text, interval=self.interval)
            log.info(f"键入 / Typed: {text[:30]}")

    def press(self, key: str, presses: int = 1, interval: float = 0.1):
        """
        按下单个键 / Press a single key.
        key: 'enter', 'tab', 'escape', 'f1'~'f12', 'delete', etc.
        """
        pyautogui.press(key, presses=presses, interval=interval)
        log.info(f"按键 / Press: {key} x{presses}")

    def hotkey(self, *keys: str):
        """
        组合快捷键 / Press hotkey combination.
        例 / e.g.: hotkey('ctrl', 'a')  hotkey('ctrl', 'shift', 's')
        """
        pyautogui.hotkey(*keys)
        log.info(f"快捷键 / Hotkey: {'+'.join(keys)}")

    def key_down(self, key: str):
        """按住键 / Hold down key."""
        pyautogui.keyDown(key)

    def key_up(self, key: str):
        """释放键 / Release key."""
        pyautogui.keyUp(key)

    # ── Focus Lock 防焦点丢失 ──────────────────────

    def lock_focus(self, hwnd: Optional[int] = None):
        """
        锁定当前前景窗口，打字时自动恢复焦点。
        Lock the foreground window; auto-restore focus before typing.
        hwnd=None 时自动获取当前前景窗口。
        """
        self._locked_hwnd = hwnd or win32gui.GetForegroundWindow()
        title = win32gui.GetWindowText(self._locked_hwnd)
        log.info(f"焦点锁定 / Focus locked: [{self._locked_hwnd}] {title}")

    def unlock_focus(self):
        """解锁焦点 / Unlock focus."""
        self._locked_hwnd = None
        log.info("焦点解锁 / Focus unlocked")

    def _restore_focus(self):
        """恢复到锁定窗口 / Restore focus to locked window."""
        try:
            win32gui.SetForegroundWindow(self._locked_hwnd)
            time.sleep(0.05)
        except Exception as e:
            log.warning(f"恢复焦点失败 / Failed to restore focus: {e}")


# ────────────────────────────────────────────────
# 组合控制器 / Combined Controller
# ────────────────────────────────────────────────

class DesktopController:
    """
    组合鼠标+键盘控制器，提供高级操作接口。
    Combined mouse + keyboard controller with high-level API.
    """

    def __init__(self, human_like: bool = True, focus_lock: bool = True):
        self.mouse = MouseController(human_like=human_like)
        self.keyboard = KeyboardController(focus_lock=focus_lock)

    def click_and_type(
        self,
        x: int, y: int,
        text: str,
        use_paste: bool = True,
        clear_first: bool = True,
    ):
        """
        点击位置后输入文字（常用于表单填写）。
        Click at position then type text (common for form filling).
        clear_first: 先全选清空再输入 / clear existing content first
        """
        self.mouse.click(x, y)
        time.sleep(0.1)
        if clear_first:
            self.keyboard.hotkey("ctrl", "a")
            time.sleep(0.05)
        self.keyboard.type_text(text, use_paste=use_paste)
        log.info(f"点击并输入 / Click({x},{y}) + type: {text[:20]}")

    def click_button(self, x: int, y: int, label: str = ""):
        """
        点击按钮（带日志标签）/ Click a button with log label.
        """
        self.mouse.click(x, y)
        log.info(f"点击按钮 / Click button '{label}' at ({x},{y})")

    def select_all_and_replace(self, x: int, y: int, new_text: str):
        """
        点击控件→全选→替换内容（用于 MATLAB 编辑器等）。
        Click control → select all → replace text (e.g. MATLAB editor).
        """
        self.mouse.click(x, y)
        time.sleep(0.1)
        self.keyboard.hotkey("ctrl", "a")
        time.sleep(0.05)
        self.keyboard.type_text(new_text, use_paste=True)
        log.info(f"全选替换 / Select-all & replace at ({x},{y})")

    def save_file(self, hotkey_save: str = "ctrl+s"):
        """
        保存文件（默认 Ctrl+S）/ Save file (default Ctrl+S).
        """
        keys = hotkey_save.split("+")
        self.keyboard.hotkey(*keys)
        log.info(f"保存 / Saved with {hotkey_save}")

    def screenshot_and_verify(
        self,
        region: Optional[Tuple[int, int, int, int]] = None,
        save: bool = True,
        filename: str = "",
    ):
        """
        截图并保存，用于操作后视觉验证。
        Take screenshot for post-action visual verification.
        """
        from visual_locator import VisualLocator
        vl = VisualLocator()
        img = vl.screenshot(region=region, save=save, filename=filename)
        log.info(f"验证截图 / Verification screenshot taken: {img.size}")
        return img


# ── 便捷工厂 / Convenience factory ───────────────
_default_ctrl = None


def get_controller(**kwargs) -> DesktopController:
    """获取默认 DesktopController 单例 / Get default singleton."""
    global _default_ctrl
    if _default_ctrl is None:
        _default_ctrl = DesktopController(**kwargs)
    return _default_ctrl


if __name__ == "__main__":
    ctrl = DesktopController()
    print("测试鼠标移到屏幕中心 / Move mouse to center...")
    sw, sh = pyautogui.size()
    ctrl.mouse.move_to(sw // 2, sh // 2, duration=1.0)
    print("完成 / Done.")
