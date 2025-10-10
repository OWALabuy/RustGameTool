AutoFish (Rust 自动钓鱼 - Linux/Windows)

重要提示：被ban了不要找我！

已经兼容windows了喵喵

功能
- 基于图像识别（OpenCV 模板匹配）检测右下角“入库/战利品提示”
- X11 多显示器：通过 `xdotool` 获取 Rust 窗口几何，只截取其右下 ROI
- 4 FPS 捕获与去抖；Alt+` 启停；数字键切竿（默认 1、2）
- 抛竿流程：按住右键并单击左键 → 等待检测 → 切竿 → 再次抛竿

依赖
- 系统：
  - Linux：`xdotool`（窗口定位/激活），X11 环境（作者使用 awesome WM）
    - Ubuntu/Debian: `sudo apt install xdotool`
  - Windows：无需额外依赖，使用 WinAPI（`ctypes`）实现窗口定位/激活
- Python 3.9+ 包：见 `requirements.txt`

安装
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r AutoFish/requirements.txt
```

运行
- 推荐（项目根目录执行）：
```bash
python -m AutoFish.main run
```
- 也可从项目根目录执行脚本方式（已内置路径引导）：
```bash
python AutoFish/main.py run
```
- 或者进入目录后运行：
```bash
cd AutoFish && python main.py run
```

热键
- Alt+\`：开始/暂停自动钓鱼（Windows/Linux 通用，输入由 `pynput` 实现）
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

  - 在 Windows 下，使用 WinAPI 查找/激活窗口并获取几何。

常见问题
- Linux：未安装 `xdotool`：无法定位窗口，请按上文安装。
- 模块找不到：推荐使用 `python -m AutoFish.main run`，或使用脚本方式（已加入路径引导）。
- 模板误报/漏报：
  - 降低或升高 `threshold`（如 0.86 → 0.83/0.89）
  - 增减 `scales`（如 [0.9, 1.0, 1.1]）以兼容缩放/分辨率
  - 用更稳定的 UI 角标做模板（例如提示条左上角图标）

Windows 注意事项
- 若 Rust 以管理员身份运行，请也以管理员身份运行本工具（确保 `pynput` 与前台激活权限）。
- 部分系统策略可能阻止程序切到前台，已包含 `BringWindowToTop` 兜底，但建议手动聚焦一次 Rust 窗口。
- 如使用中文或其他本地化标题，可在 `AutoFish/config.yaml` 的 `window_name_patterns` 中追加对应正则或子串。


