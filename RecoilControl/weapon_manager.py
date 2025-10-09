"""
武器管理器 - 负责加载和管理不同武器的配置
"""

import json
import os
from typing import Dict, Any, Optional
from pathlib import Path


class WeaponManager:
    def __init__(self, config_dir: str = "configs"):
        self.config_dir = Path(config_dir)
        self.weapons: Dict[str, Dict[str, Any]] = {}
        self.current_weapon: Optional[str] = None
        self.load_weapons()
    
    def load_weapons(self):
        """加载所有武器配置文件"""
        if not self.config_dir.exists():
            print(f"配置目录不存在: {self.config_dir}")
            return
        
        for config_file in self.config_dir.glob("*.json"):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    weapon_config = json.load(f)
                    weapon_name = weapon_config.get("weapon_name", config_file.stem)
                    self.weapons[weapon_name] = weapon_config
                    print(f"加载武器配置: {weapon_name}")
            except Exception as e:
                print(f"加载配置文件失败 {config_file}: {e}")
    
    def get_weapon_config(self, weapon_name: str) -> Optional[Dict[str, Any]]:
        """获取指定武器的配置"""
        return self.weapons.get(weapon_name)
    
    def set_current_weapon(self, weapon_name: str):
        """设置当前使用的武器"""
        if weapon_name in self.weapons:
            self.current_weapon = weapon_name
            print(f"切换到武器: {weapon_name}")
        else:
            print(f"未知武器: {weapon_name}")
    
    def get_current_config(self) -> Optional[Dict[str, Any]]:
        """获取当前武器的配置"""
        if self.current_weapon:
            return self.weapons.get(self.current_weapon)
        return None
    
    def list_weapons(self) -> list:
        """列出所有可用武器"""
        return list(self.weapons.keys())
    
    def create_weapon_config(self, weapon_name: str, config: Dict[str, Any]):
        """创建新的武器配置"""
        config_file = self.config_dir / f"{weapon_name.lower().replace(' ', '_')}.json"
        try:
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            self.weapons[weapon_name] = config
            print(f"创建武器配置: {weapon_name}")
        except Exception as e:
            print(f"创建配置文件失败: {e}")


# 默认武器配置模板
DEFAULT_WEAPON_TEMPLATE = {
    "weapon_name": "New Weapon",
    "weapon_type": "unknown",
    "fire_mode": "semi_auto",
    "description": "新武器配置",
    
    "recoil_pattern": {
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
    },
    
    "timing": {
        "fire_rate": 400,
        "compensation_delay": 40,
        "smooth_factor": 0.8
    },
    
    "compensation": {
        "enabled": true,
        "intensity": 0.8,
        "smoothing": true,
        "humanization": {
            "enabled": true,
            "random_factor": 0.1,
            "micro_adjustments": true
        }
    },
    
    "advanced": {
        "burst_mode": {
            "enabled": false,
            "burst_count": 1,
            "burst_delay": 0
        },
        "adaptive_compensation": {
            "enabled": true,
            "learning_rate": 0.05
        }
    }
} 