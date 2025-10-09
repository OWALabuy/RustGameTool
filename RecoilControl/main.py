"""
Rust 弹道控制系统 - 主程序
支持Windows和Linux系统
"""

import time
import sys
import os
import platform
from typing import Optional

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from weapon_manager import WeaponManager
from mouse_controller import MouseController
from input_detector import InputDetector, FireDetector


class RecoilControlSystem:
    def __init__(self):
        # 检测操作系统
        self.os_type = platform.system().lower()
        
        # 初始化各个模块
        self.weapon_manager = WeaponManager()
        self.mouse_controller = MouseController()
        self.input_detector = InputDetector()
        self.fire_detector = FireDetector(self.input_detector)
        
        # 系统状态
        self.is_enabled = False
        self.current_weapon = None
        
        # 设置回调函数
        self.input_detector.set_callbacks(
            on_fire_start=self._on_fire_start,
            on_fire_end=self._on_fire_end,
            on_toggle=self._on_toggle
        )
        
        print("🎯 Rust 弹道控制系统已初始化")
        print(f"🖥️  操作系统: {self.os_type}")
        print(f"📋 可用武器: {', '.join(self.weapon_manager.list_weapons())}")
        
        # Linux特定提示
        if self.os_type == "linux":
            print("🐧 Linux用户提示:")
            print("   - 热键: Ctrl+Alt+R (避免与桌面环境冲突)")
            print("   - 确保已安装xdotool: sudo apt install xdotool")
            print("   - 如果使用Proton，建议在游戏前启动系统")
    
    def start(self):
        """启动系统"""
        print("\n🚀 启动弹道控制系统...")
        print("=" * 50)
        print("📖 使用说明:")
        
        # 根据操作系统显示不同的热键
        if self.os_type == "linux":
            print("  Ctrl+Alt+R  - 开启/关闭系统")
        else:
            print("  Ctrl+Shift+R  - 开启/关闭系统")
        
        print("  鼠标左键      - 检测射击")
        print("  Ctrl+C        - 退出程序")
        print("=" * 50)
        
        # 启动输入检测
        try:
            self.input_detector.start_listening()
        except Exception as e:
            print(f"❌ 启动失败: {e}")
            if self.os_type == "linux":
                print("💡 Linux故障排除:")
                print("   1. 安装依赖: sudo apt install xdotool python3-xlib")
                print("   2. 确保在X11环境下运行 (不是Wayland)")
                print("   3. 检查权限: xhost +local:")
            return
        
        try:
            while True:
                time.sleep(0.1)
        except KeyboardInterrupt:
            self.stop()
    
    def stop(self):
        """停止系统"""
        print("\n🛑 正在停止系统...")
        
        # 停止所有模块
        self.input_detector.stop_listening()
        self.mouse_controller.stop_compensation_loop()
        
        # 显示统计信息
        self._show_stats()
        
        print("✅ 系统已安全停止")
    
    def _on_fire_start(self):
        """射击开始回调"""
        if not self.is_enabled:
            return
        
        # 获取当前武器配置
        config = self.weapon_manager.get_current_config()
        if not config:
            print("⚠️  未设置当前武器，使用默认配置")
            config = self.weapon_manager.get_weapon_config("AK-47")
        
        if config and config["compensation"]["enabled"]:
            print(f"🎯 开始补偿: {config['weapon_name']}")
            # 开始补偿（假设射击持续1秒，实际会根据释放时间调整）
            self.mouse_controller.start_compensation(config, 1.0)
    
    def _on_fire_end(self, duration: float):
        """射击结束回调"""
        if not self.is_enabled:
            return
        
        # 停止补偿
        self.mouse_controller.stop_compensation_loop()
        
        # 记录射击事件
        self.fire_detector.add_fire_event(duration)
        
        print(f"🎯 补偿结束，射击持续: {duration:.3f}秒")
    
    def _on_toggle(self):
        """切换系统状态"""
        self.is_enabled = not self.is_enabled
        status = "✅ 已启用" if self.is_enabled else "❌ 已禁用"
        print(f"🔄 系统状态: {status}")
        
        if self.is_enabled:
            # 显示当前武器信息
            current_config = self.weapon_manager.get_current_config()
            if current_config:
                print(f"🔫 当前武器: {current_config['weapon_name']}")
            else:
                print("⚠️  请设置当前武器")
    
    def set_current_weapon(self, weapon_name: str):
        """设置当前武器"""
        self.weapon_manager.set_current_weapon(weapon_name)
        self.current_weapon = weapon_name
    
    def _show_stats(self):
        """显示统计信息"""
        print("\n📊 系统统计:")
        print("-" * 30)
        
        # 输入检测统计
        input_stats = self.input_detector.get_stats()
        print(f"总射击次数: {input_stats['total_fires']}")
        print(f"平均射击时长: {input_stats['average_fire_duration']:.3f}秒")
        
        # 鼠标控制统计
        mouse_stats = self.mouse_controller.get_stats()
        print(f"总补偿次数: {mouse_stats['total_compensations']}")
        print(f"总移动距离: {mouse_stats['total_movement']:.2f}像素")
        print(f"平均响应时间: {mouse_stats['average_response_time']*1000:.2f}毫秒")
        
        # 射击模式分析
        fire_pattern = self.fire_detector.get_fire_pattern()
        if fire_pattern:
            print(f"射击模式分析:")
            print(f"  最近5秒射击: {fire_pattern['recent_fires']}次")
            print(f"  最短射击: {fire_pattern['min_duration']:.3f}秒")
            print(f"  最长射击: {fire_pattern['max_duration']:.3f}秒")


def show_help():
    """显示帮助信息"""
    os_type = platform.system().lower()
    hotkey = "Ctrl+Alt+R" if os_type == "linux" else "Ctrl+Shift+R"
    
    print(f"""
🎯 Rust 弹道控制系统 - 帮助

使用方法:
  python main.py                    # 启动系统
  python main.py --weapon AK-47     # 启动并设置武器
  python main.py --list-weapons     # 列出所有武器
  python main.py --help             # 显示此帮助

热键:
  {hotkey}  - 开启/关闭系统
  Ctrl+C        - 退出程序

配置文件:
  武器配置文件位于 configs/ 目录
  可以手动编辑调整补偿参数

系统支持:
  ✅ Windows 10/11
  ✅ Linux (Ubuntu, Arch, Fedora等)
  🐧 Linux用户需要安装xdotool

安全说明:
  - 仅模拟鼠标移动，不修改游戏内存
  - 适用于不运行EAC的PVE服务器
  - 建议仅在PVE场景使用

Linux安装依赖:
  Ubuntu/Debian: sudo apt install xdotool
  Arch: sudo pacman -S xdotool
  Fedora: sudo dnf install xdotool
""")


def check_linux_dependencies():
    """检查Linux依赖"""
    if platform.system().lower() != "linux":
        return True
    
    try:
        import subprocess
        result = subprocess.run(['which', 'xdotool'], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ 未找到xdotool，请先安装:")
            print("   Ubuntu/Debian: sudo apt install xdotool")
            print("   Arch: sudo pacman -S xdotool")
            print("   Fedora: sudo dnf install xdotool")
            return False
        return True
    except Exception:
        print("⚠️  无法检查xdotool，请确保已安装")
        return False


def main():
    """主函数"""
    # 解析命令行参数
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        
        if arg == "--help" or arg == "-h":
            show_help()
            return
        
        if arg == "--list-weapons" or arg == "-l":
            weapon_manager = WeaponManager()
            print("📋 可用武器列表:")
            for weapon in weapon_manager.list_weapons():
                config = weapon_manager.get_weapon_config(weapon)
                if config:
                    print(f"  {weapon} - {config['description']}")
            return
    
    # Linux依赖检查
    if platform.system().lower() == "linux" and not check_linux_dependencies():
        return
    
    # 创建并启动系统
    system = RecoilControlSystem()
    
    # 设置默认武器（如果指定了）
    if len(sys.argv) > 2 and sys.argv[1] == "--weapon":
        weapon_name = sys.argv[2]
        system.set_current_weapon(weapon_name)
    
    # 启动系统
    system.start()


if __name__ == "__main__":
    main() 