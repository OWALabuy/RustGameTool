"""
精确弹道模式测试脚本
演示AK-47的真实弹道特性
"""

import time
import json
from mouse_controller import MouseController


def test_ak47_precise_pattern():
    """测试AK-47精确弹道模式"""
    print("🎯 AK-47 精确弹道模式测试")
    print("=" * 50)
    
    # 加载精确配置
    try:
        with open("configs/ak47_precise.json", 'r', encoding='utf-8') as f:
            config = json.load(f)
        print("✅ 加载AK-47精确配置成功")
    except FileNotFoundError:
        print("❌ 未找到AK-47精确配置文件，使用默认配置")
        config = {
            "recoil_pattern": {
                "pattern_type": "precise",
                "shot_pattern": [
                    {"shot": 1, "vertical": 8, "horizontal": 0, "description": "第一发，轻微上跳"},
                    {"shot": 2, "vertical": 12, "horizontal": 0, "description": "第二发，继续上跳"},
                    {"shot": 3, "vertical": 15, "horizontal": 0, "description": "第三发，上跳加剧"},
                    {"shot": 4, "vertical": 18, "horizontal": 0, "description": "第四发，上跳继续"},
                    {"shot": 5, "vertical": 20, "horizontal": 0, "description": "第五发，上跳达到峰值"},
                    {"shot": 6, "vertical": 22, "horizontal": -2, "description": "第六发，开始向左偏移"},
                    {"shot": 7, "vertical": 25, "horizontal": -4, "description": "第七发，左偏移加剧"},
                    {"shot": 8, "vertical": 28, "horizontal": -6, "description": "第八发，左偏移继续"},
                    {"shot": 9, "vertical": 30, "horizontal": -8, "description": "第九发，左偏移稳定"},
                    {"shot": 10, "vertical": 32, "horizontal": -10, "description": "第十发，左偏移最大"}
                ]
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
    
    # 分析弹道模式
    print("\n📊 弹道模式分析:")
    shot_pattern = config["recoil_pattern"]["shot_pattern"]
    
    print("🎯 前5发 (主要向下压):")
    for i in range(5):
        shot = shot_pattern[i]
        print(f"  第{shot['shot']}发: 垂直={shot['vertical']}, 水平={shot['horizontal']} - {shot['description']}")
    
    print("\n🎯 6-10发 (向左下压，下压程度递增):")
    for i in range(5, min(10, len(shot_pattern))):
        shot = shot_pattern[i]
        print(f"  第{shot['shot']}发: 垂直={shot['vertical']}, 水平={shot['horizontal']} - {shot['description']}")
    
    # 创建鼠标控制器
    controller = MouseController()
    
    print(f"\n🧪 开始测试 (3秒后开始)...")
    print("💡 观察鼠标移动模式:")
    print("   - 前5发应该只有垂直移动")
    print("   - 6发后开始有水平移动")
    print("   - 垂直移动逐渐增大")
    
    time.sleep(3)
    
    # 开始补偿测试
    controller.start_compensation(config, 2.0)  # 测试2秒
    
    # 等待补偿完成
    time.sleep(2.5)
    
    # 显示统计
    stats = controller.get_stats()
    print(f"\n📊 测试完成:")
    print(f"  总补偿次数: {stats['total_compensations']}")
    print(f"  总移动距离: {stats['total_movement']:.2f}像素")
    print(f"  平均响应时间: {stats['average_response_time']*1000:.2f}毫秒")


def compare_patterns():
    """比较精确模式和传统模式"""
    print("\n🔄 模式对比测试")
    print("=" * 50)
    
    # 精确模式配置
    precise_config = {
        "recoil_pattern": {
            "pattern_type": "precise",
            "shot_pattern": [
                {"shot": 1, "vertical": 8, "horizontal": 0},
                {"shot": 2, "vertical": 12, "horizontal": 0},
                {"shot": 3, "vertical": 15, "horizontal": 0},
                {"shot": 4, "vertical": 18, "horizontal": 0},
                {"shot": 5, "vertical": 20, "horizontal": 0},
                {"shot": 6, "vertical": 22, "horizontal": -2},
                {"shot": 7, "vertical": 25, "horizontal": -4},
                {"shot": 8, "vertical": 28, "horizontal": -6},
                {"shot": 9, "vertical": 30, "horizontal": -8},
                {"shot": 10, "vertical": 32, "horizontal": -10}
            ]
        },
        "timing": {"fire_rate": 600},
        "compensation": {"intensity": 1.0, "humanization": {"enabled": False}}
    }
    
    # 传统模式配置
    traditional_config = {
        "recoil_pattern": {
            "vertical": {
                "initial_kick": 15,
                "per_shot_increase": 8,
                "max_compensation": 120,
                "curve_type": "exponential"
            },
            "horizontal": {
                "random_range": [-3, 3],
                "drift_factor": 0.5
            }
        },
        "timing": {"fire_rate": 600},
        "compensation": {"intensity": 1.0, "humanization": {"enabled": False}}
    }
    
    controller = MouseController()
    
    print("🎯 测试精确模式...")
    time.sleep(1)
    controller.start_compensation(precise_config, 1.0)
    time.sleep(1.5)
    
    precise_stats = controller.get_stats()
    controller.reset_stats()
    
    print("🎯 测试传统模式...")
    time.sleep(1)
    controller.start_compensation(traditional_config, 1.0)
    time.sleep(1.5)
    
    traditional_stats = controller.get_stats()
    
    print(f"\n📊 对比结果:")
    print(f"精确模式 - 补偿次数: {precise_stats['total_compensations']}, 移动距离: {precise_stats['total_movement']:.2f}")
    print(f"传统模式 - 补偿次数: {traditional_stats['total_compensations']}, 移动距离: {traditional_stats['total_movement']:.2f}")


def main():
    """主函数"""
    print("🎯 精确弹道模式测试")
    print("=" * 50)
    
    # 测试精确模式
    test_ak47_precise_pattern()
    
    # 对比测试
    compare_patterns()
    
    print("\n✅ 测试完成！")
    print("💡 精确模式的优势:")
    print("   - 每发子弹都有精确的补偿值")
    print("   - 模拟真实的AK弹道特性")
    print("   - 前5发无水平偏移，6发后开始左偏")
    print("   - 垂直后坐力递增")


if __name__ == "__main__":
    main() 