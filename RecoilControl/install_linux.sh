#!/bin/bash

# Rust 弹道控制系统 - Linux安装脚本

echo "🎯 Rust 弹道控制系统 - Linux安装"
echo "================================"

# 检测发行版
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$NAME
    VER=$VERSION_ID
else
    echo "❌ 无法检测操作系统"
    exit 1
fi

echo "🖥️  检测到系统: $OS $VER"

# 安装依赖
echo "📦 安装系统依赖..."

case $ID in
    "ubuntu"|"debian"|"linuxmint")
        echo "📥 使用apt安装依赖..."
        sudo apt update
        sudo apt install -y python3 python3-pip python3-venv xdotool python3-xlib
        ;;
    "arch"|"manjaro")
        echo "📥 使用pacman安装依赖..."
        sudo pacman -Syu --noconfirm
        sudo pacman -S --noconfirm python python-pip xdotool python-xlib
        ;;
    "fedora"|"rhel"|"centos")
        echo "📥 使用dnf安装依赖..."
        sudo dnf update -y
        sudo dnf install -y python3 python3-pip xdotool python3-xlib
        ;;
    *)
        echo "⚠️  未知发行版，请手动安装依赖:"
        echo "   - Python 3.7+"
        echo "   - pip3"
        echo "   - xdotool"
        echo "   - python3-xlib"
        ;;
esac

# 创建虚拟环境
echo "🐍 创建Python虚拟环境..."
python3 -m venv venv
source venv/bin/activate

# 安装Python依赖
echo "📥 安装Python依赖包..."
pip install --upgrade pip
pip install -r requirements.txt

# 设置权限
echo "🔧 设置脚本权限..."
chmod +x run.sh

echo "✅ 安装完成！"
echo ""
echo "🚀 使用方法:"
echo "   ./run.sh                    # 启动系统"
echo "   python3 main.py --help      # 查看帮助"
echo "   python3 main.py --list-weapons  # 查看武器列表"
echo ""
echo "🐧 Linux用户提示:"
echo "   - 热键: Ctrl+Alt+R (避免与桌面环境冲突)"
echo "   - 如果使用Proton，建议在游戏前启动系统"
echo "   - 确保在X11环境下运行以获得最佳兼容性" 