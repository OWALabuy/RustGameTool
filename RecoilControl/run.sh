#!/bin/bash

# Rust 弹道控制系统 - Linux启动脚本

echo "🎯 Rust 弹道控制系统"
echo "========================"

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到Python3，请先安装Python 3.7+"
    echo "   Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "   Arch: sudo pacman -S python python-pip"
    echo "   Fedora: sudo dnf install python3 python3-pip"
    exit 1
fi

# 检查xdotool是否安装
if ! command -v xdotool &> /dev/null; then
    echo "❌ 错误: 未找到xdotool，请先安装:"
    echo "   Ubuntu/Debian: sudo apt install xdotool"
    echo "   Arch: sudo pacman -S xdotool"
    echo "   Fedora: sudo dnf install xdotool"
    exit 1
fi

# 检查依赖是否安装
echo "📦 检查依赖包..."
if ! python3 -c "import pynput" &> /dev/null; then
    echo "📥 安装依赖包..."
    pip3 install -r requirements.txt
fi

# 检查X11环境
if [ "$XDG_SESSION_TYPE" = "wayland" ]; then
    echo "⚠️  警告: 检测到Wayland环境"
    echo "   建议切换到X11以获得更好的兼容性"
    echo "   或者确保Wayland下的X11兼容性"
fi

echo "🚀 启动系统..."
echo

# 设置环境变量
export DISPLAY=${DISPLAY:-:0}

# 启动程序
python3 main.py 