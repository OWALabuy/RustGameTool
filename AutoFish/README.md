AutoFish (Rust 自动钓鱼 - Linux/X11)

功能
- 基于图像识别（OpenCV 模板匹配）检测右下角“入库/战利品提示”
- X11 多显示器：通过 `xdotool` 获取 Rust 窗口几何，只截取其右下 ROI
- 4 FPS 捕获与去抖；Alt+` 启停；数字键切竿（默认 1、2）
- 抛竿流程：按住右键并单击左键 → 等待检测 → 切竿 → 再次抛竿

依赖
- 系统：`xdotool`（窗口定位/激活），X11 环境（你使用 awesome WM）
  - Ubuntu/Debian: `sudo apt install xdotool`
- Python 3.9+ 包：见 `requirements.txt`

安装
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r AutoFish/requirements.txt
```

使用
```bash
python AutoFish/main.py run
```

- Alt+`：开始/暂停自动钓鱼
- 退出：Ctrl+C（终端）

配置
- `AutoFish/config.yaml` 中的关键项：
  - `window_name_patterns`：Rust 窗口标题匹配（正则，按序尝试）
  - `roi`：右下角 ROI 百分比（相对 Rust 窗口尺寸）
  - `switch_keys`：切竿数字键序列（如 ["1", "2"]）
  - `threshold`、`scales`、`cooldown_s`：模板匹配参数与去抖
  - `fps`: 捕获帧率（默认 4）

模板（识别目标）
- 将代表“入库/战利品提示”的小图标模板放到 `AutoFish/templates/loot_icon.png`。
- 初次可直接运行后观察 `logs` 输出的匹配分数，必要时微调阈值。

多显示器说明
- 本工具不会截取整桌面，而是：
 1) 使用 `xdotool` 查找并激活名为 `window_name_patterns` 的 Rust 窗口；
 2) 获取该窗口的绝对坐标与尺寸（位于哪个显示器均可）；
 3) 仅在该矩形内裁剪右下角 ROI，保证分辨率变化与多屏均可用。

常见问题
- 未安装 `xdotool`：无法定位窗口，请按上文安装。
- 模板误报/漏报：
  - 降低或升高 `threshold`（如 0.86 → 0.83/0.89）
  - 增减 `scales`（如 [0.9, 1.0, 1.1]）以兼容缩放/分辨率
  - 用更稳定的 UI 角标做模板（例如提示条左上角图标）


