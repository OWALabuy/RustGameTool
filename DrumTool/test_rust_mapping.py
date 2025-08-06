#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rust游戏鼓谱映射测试脚本
生成测试MIDI文件，验证映射关系是否正确
"""

import json
import mido
from mido import Message, MidiFile, MidiTrack
from drum_converter import DrumConverter

def create_rust_test_midi():
    """创建Rust游戏测试MIDI文件"""
    
    # 创建MIDI文件
    midi = MidiFile()
    track = MidiTrack()
    midi.tracks.append(track)
    
    # 设置鼓轨
    track.append(Message('program_change', program=0, time=0, channel=9))
    
    # Rust游戏实际映射的鼓音符
    rust_drums = {
        35: "底鼓 (C3)",
        36: "底鼓2 (C#3)", 
        38: "军鼓 (D3)",
        40: "军鼓2 (G#3)",
        41: "1通鼓 (D#3)",
        42: "闭合踩镲 (E3)",
        43: "2通鼓 (F3)",
        45: "3通鼓 (G3)",
        47: "4通鼓 (A3)",
        48: "踩镲2/开镲 (A#3)",
        49: "吊镲 (B3)",
        51: "叮叮镲 (F#3)"
    }
    
    # 添加每个鼓音符的测试
    time_offset = 0
    for drum_note, drum_name in rust_drums.items():
        # 添加鼓音符
        track.append(Message('note_on', note=drum_note, velocity=100, time=time_offset, channel=9))
        track.append(Message('note_off', note=drum_note, velocity=0, time=480, channel=9))
        time_offset = 0  # 下一个音符立即开始
        
        print(f"添加鼓音符: {drum_note} - {drum_name}")
    
    # 保存文件
    midi.save('rust_test_drums.mid')
    print(f"\n已创建测试文件: rust_test_drums.mid")
    print("这个文件包含了Rust游戏中所有可用的鼓音符")

def create_piano_test_midi():
    """创建钢琴键位测试MIDI文件"""
    
    # 创建MIDI文件
    midi = MidiFile()
    track = MidiTrack()
    midi.tracks.append(track)
    
    # Rust游戏的钢琴键位映射
    rust_piano_keys = {
        48: "C3 - 底鼓",
        49: "C#3 - 底鼓2",
        50: "D3 - 军鼓", 
        51: "D#3 - 1通鼓",
        52: "E3 - 闭合踩镲",
        53: "F3 - 2通鼓",
        54: "F#3 - 叮叮镲",
        55: "G3 - 3通鼓",
        56: "G#3 - 军鼓2",
        57: "A3 - 4通鼓",
        58: "A#3 - 踩镲2/开镲",
        59: "B3 - 吊镲"
    }
    
    # 添加每个钢琴键位的测试
    time_offset = 0
    for piano_note, key_name in rust_piano_keys.items():
        # 添加钢琴音符
        track.append(Message('note_on', note=piano_note, velocity=100, time=time_offset, channel=0))
        track.append(Message('note_off', note=piano_note, velocity=0, time=480, channel=0))
        time_offset = 0  # 下一个音符立即开始
        
        print(f"添加钢琴音符: {piano_note} - {key_name}")
    
    # 保存文件
    midi.save('rust_test_piano.mid')
    print(f"\n已创建测试文件: rust_test_piano.mid")
    print("这个文件包含了Rust游戏中所有可用的钢琴键位")

def test_conversion():
    """测试转换功能"""
    print("=== 测试转换功能 ===")
    
    converter = DrumConverter()
    
    # 测试鼓谱转钢琴
    print("\n1. 测试鼓谱转钢琴键位:")
    try:
        converter.drum_to_piano_midi('rust_test_drums.mid', 'converted_piano.mid')
        print("✓ 鼓谱转钢琴转换成功")
    except Exception as e:
        print(f"✗ 鼓谱转钢琴转换失败: {e}")
    
    # 测试钢琴转鼓谱
    print("\n2. 测试钢琴键位转鼓谱:")
    try:
        converter.piano_to_drum_midi('rust_test_piano.mid', 'converted_drums.mid')
        print("✓ 钢琴转鼓谱转换成功")
    except Exception as e:
        print(f"✗ 钢琴转鼓谱转换失败: {e}")

def show_mapping_summary():
    """显示映射关系摘要"""
    print("=== Rust游戏鼓谱映射摘要 ===")
    
    # 加载映射配置
    with open('rust_drum_mapping.json', 'r', encoding='utf-8') as f:
        rust_mapping = json.load(f)
    
    print("\n主要鼓音符映射:")
    for key, info in rust_mapping['rust_drum_mapping'].items():
        print(f"  {key} (MIDI {info['midi_note']}) -> {info['drum_name']} (GM {info['gm_drum']})")
    
    print(f"\n特殊说明:")
    for special, info in rust_mapping['special_notes'].items():
        print(f"  {special}: {info['description']}")
    
    print(f"\n使用建议:")
    for tip in rust_mapping['usage_tips']:
        print(f"  {tip}")

def main():
    """主函数"""
    print("=== Rust游戏鼓谱MIDI转换工具测试 ===")
    print()
    
    # 显示映射摘要
    show_mapping_summary()
    print()
    
    # 创建测试文件
    print("=== 创建测试文件 ===")
    create_rust_test_midi()
    print()
    create_piano_test_midi()
    print()
    
    # 测试转换功能
    test_conversion()
    print()
    
    print("=== 测试完成 ===")
    print("生成的文件:")
    print("  - rust_test_drums.mid (原始鼓谱MIDI)")
    print("  - rust_test_piano.mid (原始钢琴MIDI)")
    print("  - converted_piano.mid (转换后的钢琴MIDI)")
    print("  - converted_drums.mid (转换后的鼓谱MIDI)")
    print()
    print("使用说明:")
    print("  1. 将 rust_test_drums.mid 导入MuseScore查看原始鼓谱")
    print("  2. 将 converted_piano.mid 在Rust游戏中播放测试")
    print("  3. 对比原始和转换后的文件，验证映射是否正确")

if __name__ == '__main__':
    main() 