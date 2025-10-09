# Proton 使用指南

本指南专门针对在Linux上使用Proton运行Rust的用户。

## 前置要求

1. **Steam + Proton**
   - 确保Rust在Proton环境下正常运行
   - 推荐使用Proton 8.0或更新版本

2. **系统依赖**
   ```bash
   # Ubuntu/Debian
   sudo apt install xdotool python3-xlib
   
   # Arch
   sudo pacman -S xdotool python-xlib
   
   # Fedora
   sudo dnf install xdotool python3-xlib
   ```

3. **桌面环境**
   - **推荐**: X11 (最佳兼容性)
   - **可选**: Wayland (可能需要额外配置)

## 安装步骤

### 1. 安装弹道控制系统
```bash
cd RecoilControl
chmod +x install_linux.sh
./install_linux.sh
```

### 2. 配置X11权限
```bash
# 允许本地X11连接
xhost +local:

# 或者更安全的方式，仅允许当前用户
xhost +local:$USER
```

### 3. 启动系统
```bash
./run.sh
```

## 使用流程

### 推荐流程
1. **启动Steam**
2. **启动弹道控制系统**
3. **启动Rust (Proton)**
4. **在游戏中按 `Ctrl+Alt+R` 启用系统**
5. **正常游戏**

### 热键说明
- **启用/禁用**: `Ctrl+Alt+R`
- **退出程序**: `Ctrl+C`

## 故障排除

### 问题1: 鼠标移动不工作
```bash
# 检查xdotool
which xdotool

# 测试鼠标移动
xdotool mousemove 100 100

# 检查X11权限
xhost
```

### 问题2: 输入检测不工作
```bash
# 检查Python依赖
python3 -c "import pynput, pyautogui"

# 检查X11环境
echo $DISPLAY
echo $XDG_SESSION_TYPE
```

### 问题3: Proton游戏窗口检测问题
```bash
# 确保在游戏前启动系统
# 如果仍有问题，尝试：
export DISPLAY=:0
./run.sh
```

### 问题4: Wayland环境问题
```bash
# 切换到X11
# 在登录时选择X11会话

# 或者配置Wayland兼容性
export XDG_SESSION_TYPE=x11
./run.sh
```

## 性能优化

### 1. 系统设置
```bash
# 减少鼠标移动延迟
export PYTHONUNBUFFERED=1

# 优化X11性能
export __GL_SYNC_TO_VBLANK=0
```

### 2. 游戏设置
- 使用全屏窗口模式 (不是全屏独占)
- 关闭垂直同步
- 降低鼠标灵敏度以获得更精确的控制

## 安全建议

1. **仅用于PVE服务器**
   - 不要在有EAC的服务器上使用
   - 遵守服务器规则

2. **权限管理**
   ```bash
   # 游戏结束后恢复X11权限
   xhost -local:
   ```

3. **系统监控**
   - 监控系统资源使用
   - 如果发现异常，立即停止使用

## 高级配置

### 自定义热键
编辑 `input_detector.py` 中的热键设置：
```python
# Linux热键
self.toggle_hotkey = {keyboard.Key.ctrl_l, keyboard.Key.alt_l, keyboard.KeyCode.from_char('r')}
```

### 武器配置
在 `configs/` 目录下编辑武器配置文件，调整：
- 补偿强度
- 移动曲线
- 人性化参数

## 技术支持

如果遇到问题：
1. 检查系统日志: `journalctl -f`
2. 检查X11日志: `~/.local/share/xorg/Xorg.0.log`
3. 提交Issue到项目仓库

## 更新日志

- **v1.0**: 初始版本，支持Windows和Linux
- **v1.1**: 添加Proton专用优化
- **v1.2**: 改进Linux兼容性 