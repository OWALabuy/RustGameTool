"""
输入检测器 - 负责检测鼠标点击和键盘输入
支持Windows和Linux系统
"""

import time
import threading
import platform
from typing import Callable, Optional
from pynput import mouse, keyboard


class InputDetector:
    def __init__(self):
        # 检测操作系统
        self.os_type = platform.system().lower()
        
        # 监听器
        self.mouse_listener = None
        self.keyboard_listener = None
        
        # 状态
        self.is_listening = False
        self.is_firing = False
        self.fire_start_time = 0
        
        # 回调函数
        self.on_fire_start: Optional[Callable] = None
        self.on_fire_end: Optional[Callable] = None
        self.on_toggle: Optional[Callable] = None
        
        # 配置 - 根据操作系统调整热键
        if self.os_type == "linux":
            # Linux上使用不同的热键组合，避免与桌面环境冲突
            self.toggle_hotkey = {keyboard.Key.ctrl_l, keyboard.Key.alt_l, keyboard.KeyCode.from_char('r')}
        else:
            # Windows上的标准热键
            self.toggle_hotkey = {keyboard.Key.ctrl_l, keyboard.Key.shift, keyboard.KeyCode.from_char('r')}
        
        self.pressed_keys = set()
        
        # 统计
        self.stats = {
            "total_fires": 0,
            "total_fire_time": 0,
            "average_fire_duration": 0
        }
        
        print(f"🖥️  输入检测器初始化 - 操作系统: {self.os_type}")
    
    def start_listening(self):
        """开始监听输入"""
        if self.is_listening:
            return
        
        self.is_listening = True
        
        try:
            # 启动鼠标监听
            self.mouse_listener = mouse.Listener(
                on_click=self._on_mouse_click
            )
            self.mouse_listener.start()
            
            # 启动键盘监听
            self.keyboard_listener = keyboard.Listener(
                on_press=self._on_key_press,
                on_release=self._on_key_release
            )
            self.keyboard_listener.start()
            
            print("✅ 输入检测器已启动")
            
            # 显示热键信息
            if self.os_type == "linux":
                print("🔄 切换热键: Ctrl+Alt+R")
            else:
                print("🔄 切换热键: Ctrl+Shift+R")
            print("🖱️  鼠标左键: 检测射击")
            
        except Exception as e:
            print(f"❌ 启动输入检测器失败: {e}")
            if self.os_type == "linux":
                print("💡 Linux提示:")
                print("   - 确保已安装python-xlib: pip install python-xlib")
                print("   - 确保有X11权限")
                print("   - 如果使用Wayland，可能需要切换到X11")
    
    def stop_listening(self):
        """停止监听输入"""
        self.is_listening = False
        
        if self.mouse_listener:
            self.mouse_listener.stop()
            self.mouse_listener = None
        
        if self.keyboard_listener:
            self.keyboard_listener.stop()
            self.keyboard_listener = None
        
        print("🛑 输入检测器已停止")
    
    def _on_mouse_click(self, x, y, button, pressed):
        """鼠标点击事件"""
        if not self.is_listening:
            return
        
        # 只检测左键
        if button == mouse.Button.left:
            if pressed and not self.is_firing:
                # 开始射击
                self.is_firing = True
                self.fire_start_time = time.perf_counter()
                
                if self.on_fire_start:
                    self.on_fire_start()
                
                print("🎯 检测到射击开始")
                
            elif not pressed and self.is_firing:
                # 结束射击
                self.is_firing = False
                fire_duration = time.perf_counter() - self.fire_start_time
                
                # 更新统计
                self.stats["total_fires"] += 1
                self.stats["total_fire_time"] += fire_duration
                self.stats["average_fire_duration"] = (
                    self.stats["total_fire_time"] / self.stats["total_fires"]
                )
                
                if self.on_fire_end:
                    self.on_fire_end(fire_duration)
                
                print(f"🎯 射击结束，持续时间: {fire_duration:.3f}秒")
    
    def _on_key_press(self, key):
        """键盘按下事件"""
        if not self.is_listening:
            return
        
        # 记录按下的键
        self.pressed_keys.add(key)
        
        # 检查热键组合
        if self._check_hotkey():
            if self.on_toggle:
                self.on_toggle()
    
    def _on_key_release(self, key):
        """键盘释放事件"""
        if not self.is_listening:
            return
        
        # 移除释放的键
        self.pressed_keys.discard(key)
    
    def _check_hotkey(self) -> bool:
        """检查热键组合"""
        return self.toggle_hotkey.issubset(self.pressed_keys)
    
    def set_toggle_hotkey(self, keys):
        """设置切换热键"""
        self.toggle_hotkey = set(keys)
        print(f"🔄 热键已设置为: {keys}")
    
    def set_callbacks(self, on_fire_start=None, on_fire_end=None, on_toggle=None):
        """设置回调函数"""
        self.on_fire_start = on_fire_start
        self.on_fire_end = on_fire_end
        self.on_toggle = on_toggle
    
    def get_stats(self) -> dict:
        """获取统计信息"""
        return self.stats.copy()
    
    def reset_stats(self):
        """重置统计"""
        self.stats = {
            "total_fires": 0,
            "total_fire_time": 0,
            "average_fire_duration": 0
        }
    
    def is_currently_firing(self) -> bool:
        """检查当前是否在射击"""
        return self.is_firing


class FireDetector:
    """专门的射击检测器"""
    
    def __init__(self, input_detector: InputDetector):
        self.input_detector = input_detector
        self.fire_history = []
        self.max_history = 100
    
    def add_fire_event(self, duration: float):
        """添加射击事件"""
        self.fire_history.append({
            "timestamp": time.time(),
            "duration": duration
        })
        
        # 保持历史记录在限制内
        if len(self.fire_history) > self.max_history:
            self.fire_history.pop(0)
    
    def get_recent_fires(self, seconds: float = 5.0) -> list:
        """获取最近的射击记录"""
        current_time = time.time()
        recent_fires = [
            fire for fire in self.fire_history
            if current_time - fire["timestamp"] <= seconds
        ]
        return recent_fires
    
    def get_fire_pattern(self) -> dict:
        """分析射击模式"""
        if not self.fire_history:
            return {}
        
        durations = [fire["duration"] for fire in self.fire_history]
        
        return {
            "total_fires": len(self.fire_history),
            "average_duration": sum(durations) / len(durations),
            "min_duration": min(durations),
            "max_duration": max(durations),
            "recent_fires": len(self.get_recent_fires())
        }


# 测试函数
def test_input_detector():
    """测试输入检测器"""
    detector = InputDetector()
    
    def on_fire_start():
        print("🔥 射击开始回调")
    
    def on_fire_end(duration):
        print(f"🔚 射击结束回调，持续: {duration:.3f}秒")
    
    def on_toggle():
        print("🔄 切换回调")
    
    detector.set_callbacks(on_fire_start, on_fire_end, on_toggle)
    detector.start_listening()
    
    print("🧪 测试开始，请:")
    if detector.os_type == "linux":
        print("1. 按 Ctrl+Alt+R 测试切换")
    else:
        print("1. 按 Ctrl+Shift+R 测试切换")
    print("2. 点击鼠标左键测试射击检测")
    print("3. 按 Ctrl+C 退出")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        detector.stop_listening()
        stats = detector.get_stats()
        print(f"📊 测试结束，统计: {stats}")


if __name__ == "__main__":
    test_input_detector() 