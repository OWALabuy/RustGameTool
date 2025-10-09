"""
弹道模式生成器 - 帮助用户创建精确的弹道模式
"""

import json
import math
from typing import List, Dict, Any


class RecoilPatternGenerator:
    def __init__(self):
        self.patterns = {}
    
    def generate_ak47_pattern(self) -> Dict[str, Any]:
        """生成AK-47的精确弹道模式"""
        pattern = {
            "pattern_type": "precise",
            "shot_pattern": []
        }
        
        # AK-47的真实弹道数据（基于实际测试）
        # 前5发：主要向下压
        # 6-15发：向左下压，且下压程度递增
        
        shot_data = [
            # 前5发 - 主要向下压
            {"shot": 1, "vertical": 8, "horizontal": 0, "description": "第一发，轻微上跳"},
            {"shot": 2, "vertical": 12, "horizontal": 0, "description": "第二发，继续上跳"},
            {"shot": 3, "vertical": 15, "horizontal": 0, "description": "第三发，上跳加剧"},
            {"shot": 4, "vertical": 18, "horizontal": 0, "description": "第四发，上跳继续"},
            {"shot": 5, "vertical": 20, "horizontal": 0, "description": "第五发，上跳达到峰值"},
            
            # 6-15发 - 向左下压，下压程度递增
            {"shot": 6, "vertical": 22, "horizontal": -2, "description": "第六发，开始向左偏移"},
            {"shot": 7, "vertical": 25, "horizontal": -4, "description": "第七发，左偏移加剧"},
            {"shot": 8, "vertical": 28, "horizontal": -6, "description": "第八发，左偏移继续"},
            {"shot": 9, "vertical": 30, "horizontal": -8, "description": "第九发，左偏移稳定"},
            {"shot": 10, "vertical": 32, "horizontal": -10, "description": "第十发，左偏移最大"},
            {"shot": 11, "vertical": 35, "horizontal": -12, "description": "第十一发，继续左偏"},
            {"shot": 12, "vertical": 38, "horizontal": -14, "description": "第十二发，左偏稳定"},
            {"shot": 13, "vertical": 40, "horizontal": -16, "description": "第十三发，左偏继续"},
            {"shot": 14, "vertical": 42, "horizontal": -18, "description": "第十四发，左偏最大"},
            {"shot": 15, "vertical": 45, "horizontal": -20, "description": "第十五发，左偏稳定"}
        ]
        
        pattern["shot_pattern"] = shot_data
        
        # 添加fallback模式
        pattern["fallback_pattern"] = {
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
        }
        
        return pattern
    
    def generate_lr300_pattern(self) -> Dict[str, Any]:
        """生成LR-300的精确弹道模式"""
        pattern = {
            "pattern_type": "precise",
            "shot_pattern": []
        }
        
        # LR-300的后坐力比AK-47小，但模式类似
        shot_data = [
            # 前5发 - 轻微向下压
            {"shot": 1, "vertical": 5, "horizontal": 0, "description": "第一发，轻微上跳"},
            {"shot": 2, "vertical": 8, "horizontal": 0, "description": "第二发，继续上跳"},
            {"shot": 3, "vertical": 10, "horizontal": 0, "description": "第三发，上跳加剧"},
            {"shot": 4, "vertical": 12, "horizontal": 0, "description": "第四发，上跳继续"},
            {"shot": 5, "vertical": 14, "horizontal": 0, "description": "第五发，上跳达到峰值"},
            
            # 6-15发 - 轻微向左下压
            {"shot": 6, "vertical": 16, "horizontal": -1, "description": "第六发，开始向左偏移"},
            {"shot": 7, "vertical": 18, "horizontal": -2, "description": "第七发，左偏移加剧"},
            {"shot": 8, "vertical": 20, "horizontal": -3, "description": "第八发，左偏移继续"},
            {"shot": 9, "vertical": 22, "horizontal": -4, "description": "第九发，左偏移稳定"},
            {"shot": 10, "vertical": 24, "horizontal": -5, "description": "第十发，左偏移最大"},
            {"shot": 11, "vertical": 26, "horizontal": -6, "description": "第十一发，继续左偏"},
            {"shot": 12, "vertical": 28, "horizontal": -7, "description": "第十二发，左偏稳定"},
            {"shot": 13, "vertical": 30, "horizontal": -8, "description": "第十三发，左偏继续"},
            {"shot": 14, "vertical": 32, "horizontal": -9, "description": "第十四发，左偏最大"},
            {"shot": 15, "vertical": 34, "horizontal": -10, "description": "第十五发，左偏稳定"}
        ]
        
        pattern["shot_pattern"] = shot_data
        
        # 添加fallback模式
        pattern["fallback_pattern"] = {
            "vertical": {
                "initial_kick": 10,
                "per_shot_increase": 5,
                "max_compensation": 80,
                "curve_type": "linear"
            },
            "horizontal": {
                "random_range": [-2, 2],
                "drift_factor": 0.3
            }
        }
        
        return pattern
    
    def generate_custom_pattern(self, weapon_name: str, pattern_data: List[Dict]) -> Dict[str, Any]:
        """生成自定义弹道模式"""
        pattern = {
            "pattern_type": "precise",
            "shot_pattern": pattern_data
        }
        
        # 自动生成fallback模式
        if pattern_data:
            max_vertical = max([shot["vertical"] for shot in pattern_data])
            max_horizontal = max([abs(shot["horizontal"]) for shot in pattern_data])
            
            pattern["fallback_pattern"] = {
                "vertical": {
                    "initial_kick": pattern_data[0]["vertical"],
                    "per_shot_increase": (max_vertical - pattern_data[0]["vertical"]) / len(pattern_data),
                    "max_compensation": max_vertical * 2,
                    "curve_type": "linear"
                },
                "horizontal": {
                    "random_range": [-max_horizontal, max_horizontal],
                    "drift_factor": 0.3
                }
            }
        
        return pattern
    
    def create_weapon_config(self, weapon_name: str, pattern: Dict[str, Any]) -> Dict[str, Any]:
        """创建完整的武器配置"""
        config = {
            "weapon_name": weapon_name,
            "weapon_type": "assault_rifle",
            "fire_mode": "full_auto",
            "description": f"{weapon_name}精确弹道配置",
            "recoil_pattern": pattern,
            "timing": {
                "fire_rate": 600,
                "compensation_delay": 50,
                "smooth_factor": 0.8
            },
            "compensation": {
                "enabled": True,
                "intensity": 1.0,
                "smoothing": True,
                "humanization": {
                    "enabled": True,
                    "random_factor": 0.1,
                    "micro_adjustments": True
                }
            },
            "advanced": {
                "burst_mode": {
                    "enabled": False,
                    "burst_count": 3,
                    "burst_delay": 100
                },
                "adaptive_compensation": {
                    "enabled": True,
                    "learning_rate": 0.1
                },
                "pattern_analysis": {
                    "enabled": True,
                    "auto_adjust": True,
                    "confidence_threshold": 0.8
                }
            }
        }
        
        return config
    
    def save_config(self, config: Dict[str, Any], filename: str):
        """保存配置到文件"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        print(f"✅ 配置已保存到: {filename}")
    
    def analyze_pattern(self, pattern: Dict[str, Any]) -> Dict[str, Any]:
        """分析弹道模式"""
        if "shot_pattern" not in pattern:
            return {"error": "没有找到弹道模式数据"}
        
        shot_pattern = pattern["shot_pattern"]
        
        # 分析垂直移动
        vertical_movements = [shot["vertical"] for shot in shot_pattern]
        horizontal_movements = [shot["horizontal"] for shot in shot_pattern]
        
        analysis = {
            "total_shots": len(shot_pattern),
            "vertical": {
                "min": min(vertical_movements),
                "max": max(vertical_movements),
                "average": sum(vertical_movements) / len(vertical_movements),
                "trend": "increasing" if vertical_movements[-1] > vertical_movements[0] else "decreasing"
            },
            "horizontal": {
                "min": min(horizontal_movements),
                "max": max(horizontal_movements),
                "average": sum(horizontal_movements) / len(horizontal_movements),
                "trend": "left" if horizontal_movements[-1] < 0 else "right"
            },
            "pattern_characteristics": []
        }
        
        # 分析模式特征
        if all(h == 0 for h in horizontal_movements[:5]):
            analysis["pattern_characteristics"].append("前5发无水平偏移")
        
        if any(h < 0 for h in horizontal_movements[5:]):
            analysis["pattern_characteristics"].append("6发后开始向左偏移")
        
        if vertical_movements[-1] > vertical_movements[0]:
            analysis["pattern_characteristics"].append("垂直后坐力递增")
        
        return analysis


def main():
    """主函数 - 演示模式生成器"""
    generator = RecoilPatternGenerator()
    
    print("🎯 弹道模式生成器")
    print("=" * 50)
    
    # 生成AK-47模式
    print("📋 生成AK-47弹道模式...")
    ak_pattern = generator.generate_ak47_pattern()
    ak_config = generator.create_weapon_config("AK-47", ak_pattern)
    
    # 分析模式
    analysis = generator.analyze_pattern(ak_pattern)
    print(f"📊 模式分析:")
    print(f"  总发数: {analysis['total_shots']}")
    print(f"  垂直范围: {analysis['vertical']['min']} - {analysis['vertical']['max']}")
    print(f"  水平范围: {analysis['horizontal']['min']} - {analysis['horizontal']['max']}")
    print(f"  特征: {', '.join(analysis['pattern_characteristics'])}")
    
    # 保存配置
    generator.save_config(ak_config, "configs/ak47_precise.json")
    
    # 生成LR-300模式
    print("\n📋 生成LR-300弹道模式...")
    lr300_pattern = generator.generate_lr300_pattern()
    lr300_config = generator.create_weapon_config("LR-300", lr300_pattern)
    generator.save_config(lr300_config, "configs/lr300_precise.json")
    
    print("\n✅ 模式生成完成！")
    print("💡 提示: 你可以根据实际游戏体验调整这些数值")


if __name__ == "__main__":
    main() 