---
name: win-visual-control
description: "Windows 桌面视觉自动化技能，支持 Win 键打开应用、OCR 文字定位、图像模板匹配、人性化鼠标键盘控制。适用于自动化操作 MATLAB、嘉立创 EDA、浏览器、微信等桌面软件。内置 SmartClick 智能图标学习机制：找不到图标时向用户要截图学习，下次自动识别。"
agent_created: true
---

## ⚠️ 免责声明（Disclaimer）

**本技能包仅供学习和技术参考使用，不得用于任何商业目的或非法用途。**

- 本技能包按"原样"提供，作者不对使用本技能包产生的任何直接或间接损失负责
- 使用本技能包进行桌面自动化操作时，请确保遵守相关软件的服务条款
- 禁止使用本技能包进行任何违反法律法规、侵犯他人权益的行为
- 使用本技能包即表示您同意自行承担所有风险和责任

> **Disclaimer**: This skill package is for learning and technical reference only. 
> It is provided "as is" without warranty. Users are solely responsible for any 
> consequences of using this skill package.

---


# ⚠️ AI 须知：加载本技能后必须做的第一件事

**加载时，AI 必须在回复中向用户展示以下开场白（选择符合当前语境的版本）：**


## 开场白（中文版，默认使用）

> 🖥️ **已加载「桌面视觉自动化」技能**
>
> 我能帮你做的事：
> - 🔍 **看图找按钮** — 给我一个按钮截图，我就能在屏幕上找到并点击它
> - ⌨️ **自动打字** — 在你指定的输入框里输入文字（支持中文）
> - 🖱️ **鼠标操作** — 点击、双击、拖拽、滚轮
> - 📸 **截图验证** — 操作前后截图，确认结果
>
> 📖 **怎么教我**：
> - 当你让我点一个我还不认识的按钮时，我会告诉你「不知道长啥样」
> - 你把这个按钮**截个图发给我**，我就学会了
> - 下次就能自动找到它，无论窗口拖到哪
>
> 📋 **当前已学会的图标**：微信、WorkBuddy、Chrome、DevEco Studio、JJ加速器、Steam（6个桌面图标）+ 微信搜索框、表情按钮、工具栏、表情包
>
> ⚙️ **操作逻辑**：先尝试模板匹配 → 不行就用 OCR 文字识别 → 再不行用 Win 键搜索打开应用
>
> 告诉我你想让我操作什么？


## 开场白（英文版）

> 🖥️ **Desktop Visual Automation skill loaded**
>
> What I can do:
> - 🔍 **Find & click buttons** — Give me a screenshot of a button, I'll locate and click it on screen
> - ⌨️ **Auto-typing** — Type text into any input field (supports Chinese via clipboard)
> - 🖱️ **Mouse control** — Click, double-click, drag, scroll
> - 📸 **Screenshot verification** — Capture before/after screenshots to confirm results
>
> 📖 **How to teach me**:
> - When I don't know a button, I'll say "I don't know what that looks like"
> - You screenshot that button and send it to me → I learn it
> - Next time I'll find it automatically, no matter where the window is
>
> Tell me what you want me to do!


---

# win-visual-control Skill

## 概述 / Overview

本技能提供 **视觉识别 + 鼠标键盘控制** 完整能力，适用于自动化操作桌面软件界面。

核心能力:
- **图像模板匹配**：OpenCV 在屏幕上寻找图标/按钮截图 -> 精准点击
- **OCR 文字定位**：Tesseract 识别屏幕文字并定位中心坐标（模板匹配失败时的备选方案）
- **Win 键搜索**：通过 Win 键搜索打开任意已安装应用（前两步都失败时的兜底方案）
- **鼠标控制**：点击、双击、右键、拖拽、滚轮，支持贝塞尔曲线人性化轨迹
- **键盘控制**：打字、按键、快捷键、粘贴（中文字符用剪贴板方式）
- **focus_lock**：打字前自动恢复目标窗口焦点，防止焦点丢失
- **SmartClick 智能学习**：找不到图标时向用户要截图 -> 学习 -> 下次就能找到


## 📖 操作逻辑（四级方案）

**当用户让你操作一个软件时，按以下优先级执行：**

```
用户: "打开微信，搜索文件传输助手，发一条消息"

STEP 0: 检查窗口是否已在运行
  ├── 已在运行 -> 跳过打开步骤
  └── 未运行 -> 进入四级定位

四级定位打开应用:
  Level 1 — 桌面模板匹配
      用已学图标 (icons/*.png) 在全屏搜索
      conf >= 0.8 -> 双击打开 ✅
      conf < 0.8 -> 进入 Level 2

  Level 2 — 任务栏/开始菜单模板匹配
      降低阈值到 0.6，扩大搜索范围
      conf >= 0.6 -> 点击打开 ✅
      conf < 0.6 -> 进入 Level 3

  Level 3 — OCR 文字识别
      用 Tesseract 识别屏幕上所有文字
      找到 "微信" -> 点击该位置 ✅
      没找到 -> 进入 Level 4

  Level 4 — Win 键搜索（兜底）
      Win 键 -> 输入应用名 -> 回车
      这是最后手段，不依赖任何视觉 ✅

STEP 1: 进入应用后判断状态
  截图 -> OCR 判断界面内容
  ├── 包含 "登录" -> 告诉用户需要手动登录 ⚠️
  ├── 包含 "文件传输助手"/聊天列表 -> 主界面，继续 ✅
  └── 无法判断 -> 重试一次，仍不行则告知用户

STEP 2: 在应用内操作（模板优先）
  搜索联系人 -> 输入文字 -> 发送
  每个按钮: 先模板匹配 -> 找不到 -> MISSING_TEMPLATE -> 向用户要截图
```


## 🤝 智能学习机制 (SmartClick v2)

**这是我向你学习的方式——找不到就问你：**

```
我: sc.click("表情按钮", "icons/emoji_btn.png", "表情按钮")
    ↓ 模板不存在 or conf < 0.8
我: MISSING_TEMPLATE: 表情按钮
我: "❌ 我不认识表情按钮长啥样，截个图发给我吧"
    ↓
你: 截图发过来
    ↓
我: sc.learn_from_image("emoji_btn", "你发的截图.png")
我: "学会了！再试一次..."
    ↓
我: sc.click("表情按钮", "icons/emoji_btn.png", "表情按钮")
    ↓ conf = 0.997
我: "找到了！(1365, 512) 点击成功 ✅"
```

**你什么都不用做，截个图发给我就行。**


## 📦 技能文件结构

```
win-visual-control/
├── SKILL.md              <- 你正在看的这个文件
├── icons/                <- 【图标模板库】学过的都在这
│   ├── wechat_icon.png      桌面微信图标
│   ├── wechat_search_box.png  搜索框
│   ├── wechat_toolbar_icons.png  5个功能按钮栏
│   ├── emoji_btn.png       表情按钮 😊
│   ├── emoji_1.png         第一个表情
│   └── emoji_2.png         第二个表情
├── scripts/
│   ├── visual_control.py   <- 【主入口】vc.click_on_template() 等
│   ├── visual_locator.py   <- 底层：模板匹配 + OCR
│   ├── mouse_keyboard.py   <- 底层：鼠标键盘
│   ├── smart_click.py      <- 智能点击：找不到就问你要截图
│   └── learn_icon.py       <- 图标学习工具
├── references/
│   └── api_reference.md    <- 完整 API 文档
├── README.md
└── UPDATE.md
```


## 环境要求 / Environment Requirements

```bash
# Python 库
pip install pytesseract pillow opencv-python pyautogui pywin32

# Tesseract OCR (Windows)
# 下载: https://github.com/UB-Mannheim/tesseract/wiki
# 安装时勾选 chi_sim（简体中文）和 eng（英文）
# 默认路径: C:\Program Files\Tesseract-OCR\tesseract.exe
# 或 D:\Tesseract-OCR\tesseract.exe
```

如果 Tesseract 在非默认路径，修改 `scripts/visual_locator.py` 中的 `TESSERACT_CMD`。


## 脚本说明 / Scripts

| 脚本 | 功能 |
|------|------|
| `visual_control.py` | **主入口**，`vc` 单例，所有上层操作都通过它 |
| `visual_locator.py` | 底层定位：模板匹配 `find_template()` + OCR `find_text()` |
| `mouse_keyboard.py` | 底层控制：鼠标贝塞尔移动、键盘输入、粘贴 |
| `smart_click.py` | 智能点击：`sc.click()` 找不到就报 MISSING_TEMPLATE，向用户要截图 |
| `learn_icon.py` | 图标学习工具：`python learn_icon.py 名称` 或 `python learn_icon.py 名称 x y` |

**核心使用方式：**

```python
import sys
sys.path.insert(0, r'C:\Users\ASUS\.workbuddy\skills\win-visual-control\scripts')
from visual_control import vc      # 主控制器
from smart_click import SmartClick  # 智能学习

sc = SmartClick()

# 方法1: 普通模板点击（已知模板）
pos = vc.locator.find_template(r'C:\...icons\wechat_search_box.png', threshold=0.8)
if pos:
    vc.ctrl.mouse.click(*pos)

# 方法2: SmartClick（不知道模板 -> 自动学习）
sc.click("emoji_btn", "icons/emoji_btn.png", "表情按钮")
```


## 🧪 当前已学会的图标

### 桌面图标（双击打开应用）

| 图标文件 | 应用 | 匹配置信度 |
|----------|------|-----------|
| `wechat_desktop.png` | 微信 | 1.000 |
| `workbuddy_desktop.png` | WorkBuddy | 1.000 |
| `chrome_desktop.png` | Google Chrome | 1.000 |
| `devecostudio_desktop.png` | DevEco Studio | 1.000 |
| `uuaccelerator_desktop.png` | UU加速器 | 1.000 |
| `steam_desktop.png` | Steam | 1.000 |

### 任务栏图标（单击操作）

| 图标文件 | 用途 | 匹配置信度 |
|----------|------|-----------|
| `winmenu_taskbar.png` | Win开始菜单 | 1.000 |
| `search_taskbar.png` | 任务栏搜索框 | 1.000 |
| `taskview_taskbar.png` | 多任务视图 | 1.000 |
| `showhidden_taskbar.png` | 隐藏图标区域（点击展开后台应用） | 1.000 |
| `wifi_taskbar.png` | 网络/WiFi | 1.000 |
| `volume_taskbar.png` | 音量 | 1.000 |

### 微信界面元素

**左侧导航栏（单击切换页面）：**

| 图标文件 | 用途 | 置信度 |
|----------|------|--------|
| `wechat_avatar.png` | 头像（点击进入设置/个人资料） | 1.000 |
| `wechat_msg_nav.png` | 消息界面按钮 | 0.927 |
| `wechat_contacts_nav.png` | 联系人 | 0.997 |
| `wechat_favorites_nav.png` | 收藏（侧栏） | 1.000 |
| `wechat_moments_nav.png` | 朋友圈 | 1.000 |
| `wechat_channels_nav.png` | 视频号 | 1.000 |

**聊天输入区（发消息时使用）：**

| 图标文件 | 用途 | 置信度 |
|----------|------|--------|
| `wechat_search_box.png` | 搜索框（搜联系人/群） | 1.000 |
| `wechat_input_toolbar.png` | 输入框工具栏整体（含5按钮） | 0.991 |
| `emoji_btn.png` | 表情按钮（笑脸图标） | 1.000 |
| `wechat_voice_btn.png` | 语音输入按钮（麦克风图标） | 1.000 |
| `wechat_file_btn.png` | 文件夹按钮（发文件） | 1.000 |
| `wechat_collect_btn.png` | 收藏按钮（输入栏内） | 1.000 |
| `wechat_call_btn.png` | 通话按钮（发起语音/视频通话） | 1.000 |
| `emoji_1.png` | 表情面板第一个表情 | 1.000 |
| `emoji_2.png` | 表情面板第二个表情 | 1.000 |

**工具栏5按钮偏移量（基于 `wechat_input_toolbar.png` 左边缘）：**
- 表情: +24px
- 收藏: +72px
- 文件: +121px
- 剪切: +169px
- 语音: +218px


## 常用代码模板

### 微信发送消息（完整流程）

```python
import sys, os, time, win32gui, win32con, pyautogui
SKILL_DIR = r'C:\Users\ASUS\.workbuddy\skills\win-visual-control\scripts'
sys.path.insert(0, SKILL_DIR)
from visual_control import vc
from smart_click import SmartClick

ICONS = r'C:\Users\ASUS\.workbuddy\skills\win-visual-control\icons'
sc = SmartClick()

# 1. 激活微信
def find_wechat():
    hwnds = []
    def cb(h, rs):
        if win32gui.IsWindowVisible(h) and '微信' in win32gui.GetWindowText(h):
            rs.append(h)
    win32gui.EnumWindows(cb, hwnds)
    return hwnds[0] if hwnds else None

hwnd = find_wechat()
if hwnd:
    win32gui.SetForegroundWindow(hwnd)
    time.sleep(0.5)

# 2. 搜索联系人
sc.click("search", os.path.join(ICONS, "wechat_search_box.png"), "搜索框")
time.sleep(0.5)
vc.type_text("文件传输助手")  # 或 "老妈"、任何联系人
time.sleep(0.8)
pyautogui.press("enter")
time.sleep(0.8)

# 3. 发送文字
vc.type_text("你好，这是测试消息", use_paste=True)
time.sleep(0.3)
pyautogui.press("enter")

# 4. 发送表情
sc.click("emoji_btn", os.path.join(ICONS, "emoji_btn.png"), "表情按钮")
time.sleep(0.8)
sc.click("emoji_1", os.path.join(ICONS, "emoji_1.png"), "第一个表情")
time.sleep(0.3)
pyautogui.press("enter")
```

### MATLAB 自动化

```python
from visual_control import vc
vc.lock_focus()
vc.click_at(22, 86)                   # 新建脚本
vc.wait(0.5)
vc.click_at(459, 233)                 # 编辑器区域
vc.hotkey("ctrl", "a")                # 全选
vc.type_text("your_code_here", use_paste=True)
vc.hotkey("ctrl", "s")                # 保存
```

### OCR 点击

```python
from visual_control import vc
vc.click_on_text("确定", retries=5)
vc.click_on_text("运行", region=(0, 0, 1920, 100))
```

### Win 键打开应用

```python
from visual_control import vc
vc.open_app("哔哩哔哩")
vc.open_app("MATLAB")
```


## 截图保存位置

所有截图保存至：`%USERPROFILE%\.workbuddy\skills\win-visual-control\scripts\screenshots\`

文件名格式：`screenshot_YYYYMMDD_HHMMSS.png` 或自定义 `filename`。


## 参数调优

| 场景 | 推荐设置 |
|------|----------|
| 高精度模板匹配 | `threshold=0.8` |
| 低对比度界面 | `threshold=0.6` |
| 网络/加载延迟 | `retry_interval=2.0`, `retries=5` |
| 快速连续操作 | `human_like=False`, `speed=0.1` |
| 防误触保护 | `human_like=True`, `speed=0.5` |

详细 API 文档见 `references/api_reference.md`。
