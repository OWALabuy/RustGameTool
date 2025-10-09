# Rust 弹道控制系统

一个用于Rust游戏的智能弹道补偿工具，支持多种武器的自动压枪。

## 功能特性

- 🎯 支持多种武器配置
- ⚡ 毫秒级响应时间
- 🔧 可调节的补偿参数
- 🛡️ 安全的输入模拟
- 🎮 全局热键开关
- 🐧 跨平台支持 (Windows/Linux)

## 支持的武器

- AK-47 (突击步枪)
- LR-300 (突击步枪)
- Thompson (冲锋枪)
- Semi-Auto Rifle (半自动步枪)
- Python (手枪)
- 更多武器可自定义配置

## 系统要求

### Windows
- Python 3.7+
- pip

### Linux
- Python 3.7+
- pip3
- xdotool
- python3-xlib
- X11环境 (推荐)

## 安装方法

### Windows
```bash
# 克隆或下载项目
cd RecoilControl

# 安装依赖
pip install -r requirements.txt

# 运行
python main.py
# 或双击 run.bat
```

### Linux
```bash
# 克隆或下载项目
cd RecoilControl

# 自动安装 (推荐)
chmod +x install_linux.sh
./install_linux.sh

# 或手动安装
sudo apt install xdotool python3-xlib  # Ubuntu/Debian
sudo pacman -S xdotool python-xlib      # Arch
sudo dnf install xdotool python3-xlib   # Fedora

pip3 install -r requirements.txt

# 运行
./run.sh
# 或
python3 main.py
```

## 使用方法

1. 运行主程序
2. 使用热键开启/关闭系统：
   - Windows: `Ctrl+Shift+R`
   - Linux: `Ctrl+Alt+R`
3. 在游戏中正常射击，系统会自动补偿弹道

## 配置说明

每个武器都有独立的配置文件，位于 `configs/` 目录下。
可以调整补偿强度、移动曲线等参数。

## 命令行选项

```bash
python main.py                    # 启动系统
python main.py --weapon AK-47     # 启动并设置武器
python main.py --list-weapons     # 列出所有武器
python main.py --help             # 显示帮助
```

## Linux特别说明

### 桌面环境兼容性
- **X11**: 完全支持，推荐使用
- **Wayland**: 部分支持，可能需要额外配置

### Proton游戏支持
- 确保在游戏前启动系统
- 使用X11环境获得最佳兼容性
- 如果遇到问题，尝试：`xhost +local:`

### 故障排除
```bash
# 检查xdotool
which xdotool

# 检查X11权限
xhost +local:

# 检查Python依赖
python3 -c "import pynput, pyautogui"
```

## 安全说明

- 仅模拟鼠标移动，不修改游戏内存
- 适用于不运行EAC的PVE服务器
- 建议仅在PVE场景使用
- 请遵守游戏服务器规则

## 开发信息

- **语言**: Python 3.7+
- **主要依赖**: pynput, pyautogui, numpy
- **平台**: Windows 10/11, Linux (Ubuntu/Arch/Fedora等)
- **许可证**: MIT

## 贡献

欢迎提交Issue和Pull Request来改进这个项目！ 