"""
鼠标控制器 - 负责精确的鼠标移动和弹道补偿
支持Windows和Linux系统
"""

import time
import random
import math
import threading
import platform
from typing import Tuple, List, Optional, Dict, Any
import pyautogui
import numpy as np


class MouseController:
    def __init__(self):
        # 检测操作系统
        self.os_type = platform.system().lower()
        
        # 设置pyautogui的安全设置
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.001  # 最小延迟
        
        # Linux特定设置
        if self.os_type == "linux":
            # 在Linux上，pyautogui使用xdotool
            # 确保xdotool已安装
            self._check_linux_dependencies()
        
        # 补偿状态
        self.is_compensating = False
        self.compensation_thread = None
        self.stop_compensation = False
        
        # 性能统计
        self.stats = {
            "total_compensations": 0,
            "total_movement": 0,
            "average_response_time": 0
        }
        
        # 弹道模式缓存
        self.pattern_cache = {}
        
        print(f"🖥️  检测到操作系统: {self.os_type}")
    
    def _check_linux_dependencies(self):
        """检查Linux依赖"""
        try:
            import subprocess
            result = subprocess.run(['which', 'xdotool'], capture_output=True, text=True)
            if result.returncode != 0:
                print("⚠️  警告: 未找到xdotool，请安装:")
                print("   Ubuntu/Debian: sudo apt install xdotool")
                print("   Arch: sudo pacman -S xdotool")
                print("   Fedora: sudo dnf install xdotool")
        except Exception as e:
            print(f"⚠️  无法检查xdotool: {e}")
    
    def move_mouse_smooth(self, dx: float, dy: float, duration: float = 0.1):
        """平滑移动鼠标"""
        try:
            # 获取当前鼠标位置
            current_x, current_y = pyautogui.position()
            
            # 计算目标位置
            target_x = current_x + dx
            target_y = current_y + dy
            
            # 平滑移动
            pyautogui.moveTo(target_x, target_y, duration=duration, _pause=False)
            
        except Exception as e:
            print(f"鼠标移动失败: {e}")
    
    def move_mouse_relative(self, dx: float, dy: float):
        """相对移动鼠标（更快）"""
        try:
            # Linux上使用更精确的相对移动
            if self.os_type == "linux":
                # 在Linux上，相对移动可能更稳定
                pyautogui.moveRel(dx, dy, duration=0, _pause=False)
            else:
                # Windows上的标准相对移动
                pyautogui.moveRel(dx, dy, duration=0, _pause=False)
                
        except Exception as e:
            print(f"相对移动失败: {e}")
    
    def humanize_movement(self, dx: float, dy: float, humanization_factor: float = 0.1) -> Tuple[float, float]:
        """人性化移动，添加随机性"""
        if humanization_factor <= 0:
            return dx, dy
        
        # 添加随机偏移
        random_dx = random.uniform(-humanization_factor, humanization_factor)
        random_dy = random.uniform(-humanization_factor, humanization_factor)
        
        # 添加微调
        micro_dx = random.uniform(-0.5, 0.5)
        micro_dy = random.uniform(-0.5, 0.5)
        
        return dx + random_dx + micro_dx, dy + random_dy + micro_dy
    
    def _get_precise_pattern(self, shot_count: int, config: dict) -> Tuple[float, float]:
        """获取精确弹道模式"""
        pattern_type = config["recoil_pattern"].get("pattern_type", "fallback")
        
        if pattern_type == "precise" and "shot_pattern" in config["recoil_pattern"]:
            shot_pattern = config["recoil_pattern"]["shot_pattern"]
            
            # 查找精确的弹道数据
            for pattern in shot_pattern:
                if pattern["shot"] == shot_count:
                    vertical_comp = pattern["vertical"]
                    horizontal_comp = pattern["horizontal"]
                    
                    # 添加描述信息用于调试
                    if "description" in pattern:
                        print(f"🎯 第{shot_count}发: {pattern['description']}")
                    
                    return vertical_comp, horizontal_comp
            
            # 如果超出预定义范围，使用fallback模式
            print(f"⚠️  第{shot_count}发超出预定义范围，使用fallback模式")
            return self._get_fallback_pattern(shot_count, config)
        
        # 使用fallback模式
        return self._get_fallback_pattern(shot_count, config)
    
    def _get_fallback_pattern(self, shot_count: int, config: dict) -> Tuple[float, float]:
        """获取fallback弹道模式"""
        fallback_config = config["recoil_pattern"].get("fallback_pattern", config["recoil_pattern"])
        
        vertical_config = fallback_config["vertical"]
        horizontal_config = fallback_config["horizontal"]
        
        # 垂直补偿计算
        initial_kick = vertical_config["initial_kick"]
        per_shot = vertical_config["per_shot_increase"]
        max_comp = vertical_config["max_compensation"]
        curve_type = vertical_config["curve_type"]
        
        if curve_type == "exponential":
            # 指数增长曲线
            vertical_comp = min(initial_kick * (1.5 ** shot_count) + per_shot * shot_count, max_comp)
        elif curve_type == "linear":
            # 线性增长
            vertical_comp = min(initial_kick + per_shot * shot_count, max_comp)
        else:
            # 默认线性
            vertical_comp = min(initial_kick + per_shot * shot_count, max_comp)
        
        # 水平补偿计算
        random_range = horizontal_config["random_range"]
        drift_factor = horizontal_config["drift_factor"]
        
        # 基础水平偏移
        base_horizontal = random.uniform(random_range[0], random_range[1])
        
        # 累积偏移（连发时的漂移）
        cumulative_drift = shot_count * drift_factor * random.uniform(-1, 1)
        
        horizontal_comp = base_horizontal + cumulative_drift
        
        return vertical_comp, horizontal_comp
    
    def calculate_compensation_curve(self, shot_count: int, config: dict) -> Tuple[float, float]:
        """计算补偿曲线 - 支持精确模式和fallback模式"""
        # 优先使用精确模式
        return self._get_precise_pattern(shot_count, config)
    
    def start_compensation(self, config: dict, fire_duration: float = 1.0):
        """开始弹道补偿"""
        if self.is_compensating:
            return
        
        self.is_compensating = True
        self.stop_compensation = False
        
        # 在新线程中运行补偿
        self.compensation_thread = threading.Thread(
            target=self._compensation_loop,
            args=(config, fire_duration)
        )
        self.compensation_thread.daemon = True
        self.compensation_thread.start()
    
    def stop_compensation_loop(self):
        """停止补偿循环"""
        self.stop_compensation = True
        if self.compensation_thread:
            self.compensation_thread.join(timeout=1.0)
        self.is_compensating = False
    
    def _compensation_loop(self, config: dict, fire_duration: float):
        """补偿循环"""
        start_time = time.perf_counter()
        shot_count = 0
        
        # 获取配置参数
        fire_rate = config["timing"]["fire_rate"]
        compensation_delay = config["timing"]["compensation_delay"] / 1000.0  # 转换为秒
        smooth_factor = config["timing"]["smooth_factor"]
        
        compensation_config = config["compensation"]
        intensity = compensation_config["intensity"]
        humanization = compensation_config["humanization"]
        
        # 计算射击间隔
        shot_interval = 60.0 / fire_rate  # 秒
        
        print(f"🎯 开始弹道补偿 - 射速: {fire_rate} RPM, 间隔: {shot_interval:.3f}秒")
        
        while not self.stop_compensation and (time.perf_counter() - start_time) < fire_duration:
            # 计算当前应该发射的子弹数
            elapsed_time = time.perf_counter() - start_time
            expected_shots = int(elapsed_time / shot_interval)
            
            if expected_shots > shot_count:
                shot_count = expected_shots
                
                # 计算补偿
                vertical_comp, horizontal_comp = self.calculate_compensation_curve(shot_count, config)
                
                # 应用强度
                vertical_comp *= intensity
                horizontal_comp *= intensity
                
                # 人性化处理
                if humanization["enabled"]:
                    vertical_comp, horizontal_comp = self.humanize_movement(
                        vertical_comp, horizontal_comp, humanization["random_factor"]
                    )
                
                # 执行补偿移动
                self.move_mouse_relative(horizontal_comp, vertical_comp)
                
                # 更新统计
                self.stats["total_compensations"] += 1
                self.stats["total_movement"] += abs(vertical_comp) + abs(horizontal_comp)
                
                # 显示补偿信息
                print(f"🎯 第{shot_count}发补偿: 垂直={vertical_comp:.1f}, 水平={horizontal_comp:.1f}")
            
            # 短暂休眠
            time.sleep(0.001)  # 1ms精度
        
        # 计算平均响应时间
        if self.stats["total_compensations"] > 0:
            self.stats["average_response_time"] = (time.perf_counter() - start_time) / self.stats["total_compensations"]
    
    def get_stats(self) -> dict:
        """获取性能统计"""
        return self.stats.copy()
    
    def reset_stats(self):
        """重置统计"""
        self.stats = {
            "total_compensations": 0,
            "total_movement": 0,
            "average_response_time": 0
        }


# 测试函数
def test_mouse_controller():
    """测试鼠标控制器"""
    controller = MouseController()
    
    # 测试配置 - 使用精确模式
    test_config = {
        "recoil_pattern": {
            "pattern_type": "precise",
            "shot_pattern": [
                {"shot": 1, "vertical": 5, "horizontal": 0, "description": "第一发"},
                {"shot": 2, "vertical": 10, "horizontal": 0, "description": "第二发"},
                {"shot": 3, "vertical": 15, "horizontal": -2, "description": "第三发"},
                {"shot": 4, "vertical": 20, "horizontal": -4, "description": "第四发"},
                {"shot": 5, "vertical": 25, "horizontal": -6, "description": "第五发"}
            ],
            "fallback_pattern": {
                "vertical": {
                    "initial_kick": 10,
                    "per_shot_increase": 5,
                    "max_compensation": 50,
                    "curve_type": "linear"
                },
                "horizontal": {
                    "random_range": [-2, 2],
                    "drift_factor": 0.3
                }
            }
        },
        "timing": {
            "fire_rate": 600,
            "compensation_delay": 50,
            "smooth_factor": 0.8
        },
        "compensation": {
            "intensity": 1.0,
            "humanization": {
                "enabled": True,
                "random_factor": 0.1
            }
        }
    }
    
    print("🧪 测试开始，3秒后开始补偿...")
    time.sleep(3)
    
    controller.start_compensation(test_config, 2.0)
    time.sleep(2.5)
    
    stats = controller.get_stats()
    print(f"📊 测试完成，统计: {stats}")


if __name__ == "__main__":
    test_mouse_controller() 