# win-visual-control v2.0 - 增强版

## 🎉 版本更新说明

### ✨ 新增功能

#### 1. 人工学习模式 📚
- **通用图标学习工具**：`scripts/learn_icon.py`
  - 用法：`python learn_icon.py 图标名称`
  - 倒计时 5 秒，用户将鼠标移到目标图标上
  - 自动截图保存为模板，一次学习永久识别
  - 支持覆盖已有模板

- **微信专用学习脚本**：`scripts/learn_wechat_icon.py`
  - 快速学习微信图标

#### 2. 四级智能识别方案 🎯
- **模板匹配**（最精准，置信度 99%+）
- **OCR 文字识别**
- **颜色识图**（绿色图标识别）
- **Win 键搜索**（兜底方案）

示例脚本：`scripts/open_wechat_v4.py`

#### 3. 已学习的图标模板 🖼️
- `icons/wechat_icon.png` - 微信图标（置信度 99.8%）
- `icons/wuying_icon.png` - 无影云电脑图标（置信度 99.9%）

#### 4. 测试工具集 🧪
- `scripts/test_template.py` - 单图标模板匹配测试
- `scripts/test_both_icons.py` - 双图标识别测试
- `scripts/find_wuying.py` - 无影云电脑查找测试

### 🔧 适配优化

1. **Tesseract 路径适配**：已修改为 `D:\Tesseract-OCR\tesseract.exe`
2. **截图路径适配**：修改为脚本同级目录下的 `screenshots` 文件夹
3. **中文文件名兼容**：建议模板文件使用英文文件名

### 📖 使用方法

#### 快速开始
```python
from visual_control import vc

# 模板匹配（最精准）
pos = vc.locator.find_template("icons/wechat_icon.png", threshold=0.8)
if pos:
    vc.ctrl.mouse.double_click(pos[0], pos[1])

# 学习新图标
# 命令行运行：python scripts/learn_icon.py 图标名称
```

#### 四级方案打开应用
```python
# 参考 scripts/open_wechat_v4.py
# 1. 模板匹配 → 2. OCR → 3. 颜色识图 → 4. Win键搜索
```

### 📊 性能数据

| 识别方式 | 准确率 | 速度 | 适用场景 |
|---------|--------|------|---------|
| 模板匹配 | 99%+ | 快 | 已学习的图标 |
| OCR文字 | 中等 | 中 | 有文字标签的图标 |
| 颜色识图 | 较低 | 快 | 同色系图标（需配合其他方案） |
| Win键搜索 | 100% | 慢 | 兜底方案 |

### 🎯 核心优势

1. **一次学习，永久识别**：人工标注一次，模板匹配终身可用
2. **四级容错机制**：从精准到兜底，层层保障成功率
3. **位置无关**：图标挪到哪里都能找到，认图不认位置
4. **高置信度**：模板匹配置信度可达 99.9%

---

*原始版本：win-visual-control v1.0*
*增强版本：v2.0 - 新增学习模式与四级智能识别*
