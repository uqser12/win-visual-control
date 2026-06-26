# Visual Control API Reference / 视觉控制 API 参考

## 环境依赖 / Environment Requirements

```bash
pip install pytesseract pillow opencv-python pyautogui pywin32
```

Tesseract binary (Windows): https://github.com/UB-Mannheim/tesseract/wiki  
默认路径 / Default path: `C:\Program Files\Tesseract-OCR\tesseract.exe`

语言包 / Language packs:
- `chi_sim` — 简体中文 / Simplified Chinese
- `eng`     — 英文 / English
- `chi_sim+eng` — 中英混合 / Chinese + English (recommended)

---

## VisualController 一体化 API

### 初始化 / Init

```python
from visual_control import VisualController, vc

# 使用默认单例
vc.click_on_text("确定")

# 或自定义参数
ctrl = VisualController(
    ocr_lang="chi_sim+eng",   # OCR 语言
    match_threshold=0.8,       # 模板匹配阈值
    human_like=True,           # 贝塞尔曲线人性化移动
    focus_lock=True,           # 防焦点丢失
    default_retries=3,         # 默认重试次数
    retry_interval=1.0,        # 重试间隔（秒）
)
```

### 定位并点击 / Locate & Click

```python
# OCR 文字定位点击
vc.click_on_text("保存")
vc.click_on_text("确定", region=(0, 0, 800, 600))  # 限定搜索区域
vc.click_on_text("文件", button="left", offset=(0, 20))  # 偏移点击

# 模板图片匹配点击
vc.click_on_template("icons/save_btn.png")
vc.click_on_template("icons/ok.png", retries=5)

# 混合定位（模板优先，失败回退 OCR）
vc.click_hybrid("运行", template_path="icons/run.png")
```

### 定位并输入 / Locate & Type

```python
# 找到文件名框后输入
vc.locate_and_type("文件名", "my_script.m")

# 找到搜索框后输入（中文用粘贴方式）
vc.locate_and_type("搜索", "欧姆定律", use_paste=True)
```

### 直接坐标操作 / Direct Coordinate Operations

```python
# 绝对坐标点击（对已知固定坐标最快）
vc.click_at(459, 233)          # MATLAB 编辑器
vc.click_at(292, 362)          # 保存文件名框
vc.click_at(602, 473)          # 保存按钮

# 移动鼠标
vc.move_to(800, 400)
```

### 键盘操作 / Keyboard Operations

```python
vc.press("enter")                        # 回车
vc.press("tab", presses=3)              # Tab x3
vc.hotkey("ctrl", "s")                  # Ctrl+S 保存
vc.hotkey("ctrl", "a")                  # 全选
vc.hotkey("ctrl", "shift", "s")         # 另存为
vc.type_text("disp('Hello World')")     # 输入文本
vc.type_text("你好世界", use_paste=True) # 中文用粘贴
```

### 截图与验证 / Screenshot & Verify

```python
# 截取全屏
img = vc.screenshot(save=True)

# 截取指定区域 (left, top, width, height)
img = vc.screenshot(region=(0, 0, 1920, 500), save=True, filename="toolbar.png")

# 验证文字是否可见
if vc.verify_text_visible("运行完成"):
    print("执行成功")
else:
    print("执行失败，需重试")
```

### 焦点锁定 / Focus Lock

```python
# 锁定当前前景窗口（打字前自动恢复焦点）
vc.lock_focus()

# 锁定指定窗口句柄
import win32gui
hwnd = win32gui.FindWindow(None, "MATLAB R2014a")
vc.lock_focus(hwnd)

# 解锁
vc.unlock_focus()
```

---

## VisualLocator 独立用法 / VisualLocator Standalone

```python
from visual_locator import VisualLocator

vl = VisualLocator(lang="chi_sim+eng", match_threshold=0.85)

# OCR 找单个文字
pos = vl.find_text("文件")              # 返回 (x, y) 或 None

# OCR 找所有匹配
positions = vl.find_all_text("确定")   # 返回 [(x,y), ...]

# 模板匹配
pos = vl.find_template("icons/ok.png") # 返回 (x, y) 或 None

# 混合定位 + 自动重试
pos = vl.locate("保存", retries=5)
```

---

## MouseController 独立用法 / MouseController Standalone

```python
from mouse_keyboard import MouseController

mouse = MouseController(human_like=True, speed=0.3)
mouse.move_to(500, 300)
mouse.click(500, 300)
mouse.double_click(500, 300)
mouse.right_click(500, 300)
mouse.drag_to(100, 100, 500, 300)
mouse.scroll(500, 300, clicks=3)   # 正数向上
```

---

## KeyboardController 独立用法 / KeyboardController Standalone

```python
from mouse_keyboard import KeyboardController

kb = KeyboardController(interval=0.05, focus_lock=True)
kb.lock_focus()                          # 锁定焦点
kb.type_text("hello world")              # 英文直接打字
kb.type_text("你好世界", use_paste=True) # 中文用剪贴板
kb.press("enter")
kb.hotkey("ctrl", "s")
kb.unlock_focus()
```

---

## 常用场景代码片段 / Common Scenarios

### MATLAB 自动化

```python
from visual_control import vc

# 1. 锁定 MATLAB 窗口焦点
vc.lock_focus()

# 2. 点击新建脚本按钮（固定坐标）
vc.click_at(22, 86)
vc.wait(0.5)

# 3. 在编辑器中全选覆盖写入代码
vc.click_at(459, 233)
vc.hotkey("ctrl", "a")
vc.type_text("x = 0:0.1:2*pi;\nplot(x, sin(x));", use_paste=True)

# 4. 保存文件
vc.hotkey("ctrl", "s")
vc.wait(0.5)

# 5. OCR 验证保存对话框出现
if vc.verify_text_visible("保存"):
    vc.click_at(292, 362)   # 文件名框
    vc.type_text("my_plot", use_paste=True)
    vc.click_at(602, 473)   # 保存按钮

# 6. 截图验证
vc.screenshot(save=True, filename="after_save.png")
```

### 通用按钮点击（OCR）

```python
from visual_control import vc

# 找到并点击"确定"
vc.click_on_text("确定", retries=5)

# 找到并点击"Next"（英文界面）
vc.click_on_text("Next", retries=3)
```

### 嘉立创 EDA 辅助

```python
from visual_control import vc

# 截图记录当前状态
vc.screenshot(save=True, filename="before_place.png")

# 验证元件是否已放置
if vc.verify_text_visible("R1"):
    print("电阻 R1 已在原理图中")

# 点击工具栏放置按钮
vc.click_on_text("放置", retries=3)
```

---

## 区域坐标计算 / Region Coordinate Tips

`region` 参数格式：`(left, top, width, height)`

```python
# 顶部工具栏 / Top toolbar
TOOLBAR = (0, 0, 1920, 80)

# 右侧面板 / Right panel (1920x1080 屏幕)
RIGHT_PANEL = (1600, 0, 320, 1080)

# 对话框中心区域 / Dialog center area
DIALOG = (600, 300, 720, 480)
```
