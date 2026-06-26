# ⚠️ 重要声明

**本技能包仅供个人学习与技术研究使用。**

- ❌ **禁止**用于任何商业目的
- ❌ **禁止**用于违反软件服务条款的自动化操作
- ❌ **禁止**用于任何违法或侵权行为
- ✅ 使用者需自行确保遵守相关法律法规及各软件的服务条款

使用本技能包产生的一切后果由使用者自行承担。

---

# Visual Control 技能 - 安装与使用指南

> ⚠️ **免责声明**：本技能包仅供学习和技术参考使用，不得用于任何商业目的或非法用途。使用本技能包即表示您同意自行承担所有风险和责任。详情请参阅 SKILL.md 和 LICENSE 文件中的完整免责声明。

> 适用于 WorkBuddy 的桌面视觉自动化技能，支持 OCR 文字定位、图像模板匹配、人性化鼠标键盘控制。

---

## 快速安装

### 方式一：WorkBuddy 命令安装（推荐）

在 WorkBuddy 聊天窗口输入：

```
/skills install visual-control.zip
```

### 方式二：手动解压

将 `visual-control.zip` 解压到：

```
%USERPROFILE%\.workbuddy\skills\visual-control\
```

即最终目录结构为：

```
%USERPROFILE%\.workbuddy\skills\visual-control\
├── SKILL.md
├── README.md
├── scripts/
│   ├── visual_control.py
│   ├── visual_locator.py
│   └── mouse_keyboard.py
├── references/
│   └── api_reference.md
└── assets/
```

---

## 环境依赖

### 📦 完整安装步骤（Windows）

#### 步骤 1：安装 Python 依赖库

在命令提示符或 PowerShell 中执行：

```bash
pip install pytesseract pillow opencv-python pyautogui pywin32
```

**或使用国内镜像加速：**

```bash
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pytesseract pillow opencv-python pyautogui pywin32
```

**验证安装：**

```bash
python -c "import pytesseract, PIL, cv2, pyautogui, win32api; print('✅ 所有依赖库已正确安装')"
```

---

#### 步骤 2：安装 Tesseract-OCR 引擎（必需）

> ⚠️ **重要**：仅安装 `pytesseract` Python 库**不够**，还必须安装 Tesseract-OCR 引擎本身！

**Windows 下载地址：**
- GitHub Release：https://github.com/UB-Mannheim/tesseract/wiki
- 或直接下载：https://github.com/UB-Mannheim/tesseract/releases

**安装要点：**
1. 下载并运行安装程序（如 `tesseract-ocr-w64-setup-v5.3.3.20230408.exe`）
2. 安装时勾选 **Additional script data** 和 **Additional language data**
3. 确保勾选语言包：**简体中文 (chi_sim)** 和 **英文 (eng)**
4. 默认安装路径：`C:\Program Files\Tesseract-OCR\tesseract.exe`

**配置路径（如安装在非默认路径）：**

编辑 `scripts/visual_locator.py`，修改以下行：

```python
# 约第 15 行
TESSERACT_CMD = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
```

**验证 Tesseract 安装：**

```bash
tesseract --version
```

应输出类似：`tesseract v5.3.3`

---

#### 步骤 3：安装 Tesseract 中文语言包（如未自动安装）

如果 OCR 识别中文失败，手动下载语言包：

1. 访问：https://github.com/tesseract-ocr/tessdata
2. 下载 `chi_sim.traineddata`（简体中文）
3. 放入 Tesseract 安装目录的 `tessdata` 文件夹，例如：
   ```
   C:\Program Files\Tesseract-OCR\tessdata\chi_sim.traineddata
   ```

---

#### 步骤 4：测试环境

创建一个测试脚本 `test_env.py`：

```python
import sys

print("=== 环境测试 ===\n")

# 测试 Python 库
try:
    import pytesseract
    import PIL
    import cv2
    import pyautogui
    import win32api
    print("✅ Python 库：全部正常")
except ImportError as e:
    print(f"❌ Python 库缺失：{e}")
    sys.exit(1)

# 测试 Tesseract 引擎
try:
    version = pytesseract.get_tesseract_version()
    print(f"✅ Tesseract-OCR 版本：{version}")
except Exception as e:
    print(f"❌ Tesseract-OCR 未正确安装或路径未配置：{e}")
    sys.exit(1)

# 测试中文语言包
try:
    langs = pytesseract.get_languages()
    if 'chi_sim' in langs:
        print("✅ 中文语言包：已安装")
    else:
        print("⚠️ 中文语言包：未安装（OCR 中文可能失败）")
except Exception as e:
    print(f"⚠️ 无法检测语言包：{e}")

print("\n=== 测试完成 ===")
```

运行测试：

```bash
python test_env.py
```

---

### 🐧 Linux / macOS 安装（可选）

**Linux (Ubuntu/Debian)：**

```bash
sudo apt update
sudo apt install tesseract-ocr tesseract-ocr-chi-sim
sudo apt install python3-pip
pip3 install pytesseract pillow opencv-python pyautogui pywin32
```

**macOS：**

```bash
brew install tesseract tesseract-lang
pip3 install pytesseract pillow opencv-python pyautogui
```

---

### ❓ 常见安装问题

| 问题 | 解决方案 |
|------|----------|
| `tesseract is not installed or it's not in your PATH` | 安装 Tesseract-OCR 引擎，或在 `visual_locator.py` 中手动指定路径 |
| 中文 OCR 识别率低 | 确保 `chi_sim.traineddata` 已放入 `tessdata` 目录 |
| `ImportError: DLL load failed` | 重新安装 `pywin32`：`pip install --upgrade pywin32` |
| `cv2` 模块找不到 | 使用 `pip install opencv-python-headless`（无 GUI 依赖）|

---

## 功能概览

| 能力 | 说明 |
|------|------|
| OCR 文字定位 | 识别屏幕上的文字并返回中心坐标 |
| 图像模板匹配 | 在屏幕上寻找图标/按钮图片位置 |
| 混合定位 | 模板优先，失败自动回退 OCR |
| 鼠标控制 | 点击、双击、拖拽、滚轮，支持贝塞尔曲线轨迹 |
| 键盘控制 | 打字、按键、快捷键、剪贴板粘贴（支持中文） |
| 焦点锁定 | 打字前自动恢复目标窗口焦点 |
| 截图验证 | 操作前后截图，OCR 验证结果 |

---

## 快速开始

### 在 WorkBuddy 中使用

当需要自动化操作桌面软件时，WorkBuddy 会自动加载本技能。

**示例：点击"确定"按钮**

```python
from visual_control import vc

# 点击屏幕上文字为"确定"的按钮
vc.click_on_text("确定", retries=3)
```

**示例：在 MATLAB 中输入代码**

```python
from visual_control import vc

# 锁定 MATLAB 窗口焦点
vc.lock_focus()

# 点击编辑器区域（已知坐标）
vc.click_at(459, 233)

# 全选并粘贴代码
vc.hotkey("ctrl", "a")
vc.type_text("x = 0:0.1:2*pi; plot(x, sin(x));", use_paste=True)

# 运行
vc.hotkey("f5")
```

**示例：截图验证**

```python
# 操作前截图
vc.screenshot(save=True, filename="before.png")

# 执行操作...

# 操作后截图
vc.screenshot(save=True, filename="after.png")

# OCR 验证结果文字是否在屏幕上
if vc.verify_text_visible("成功"):
    print("操作成功！")
```

---

## 决策树：如何选择定位方式

```
目标元素坐标是否已知？
├── 是 → 直接使用 vc.click_at(x, y)（最快、最稳定）
└── 否 → 坐标未知，需视觉定位
    ├── 有对应图标截图？ → vc.click_on_template("icon.png")
    ├── 有可识别文字标签？ → vc.click_on_text("标签文字")
    └── 两者皆可尝试 → vc.click_hybrid("文字", template_path="icon.png")
```

---

## 注意事项

1. **中文输入**：必须使用 `use_paste=True`，否则中文字符无法正常输入
2. **分辨率**：模板匹配的图片需与屏幕显示比例一致
3. **焦点问题**：长时间操作前建议调用 `vc.lock_focus()` 锁定目标窗口
4. **权限**：首次运行可能需要管理员权限（控制鼠标键盘）

---

## 文件说明

| 文件 | 作用 |
|------|------|
| `SKILL.md` | WorkBuddy 技能入口文件（元数据 + 使用说明） |
| `scripts/visual_control.py` | **推荐使用** — 一体化控制接口 |
| `scripts/visual_locator.py` | 底层 — OCR + 模板匹配定位 |
| `scripts/mouse_keyboard.py` | 底层 — 鼠标键盘控制 |
| `references/api_reference.md` | 完整 API 文档 |

---

## 常见问题

**Q: OCR 识别率低怎么办？**
A: 在 `scripts/visual_locator.py` 中调整预处理参数，或提高屏幕亮度。

**Q: 模板匹配找不到图标？**
A: 确保模板截图与屏幕显示比例一致，或降低 `match_threshold`（默认 0.8）。

**Q: 点击位置有偏差？**
A: 使用 `offset` 参数微调，如 `vc.click_on_text("确定", offset=(10, 5))`。

---

## 作者

uqser12
