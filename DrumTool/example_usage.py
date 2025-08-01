#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例使用脚本
展示如何使用DrumConverter进行MIDI转换
"""

from drum_converter import DrumConverter
import os

def main():
    """示例主函数"""
    
    # 初始化转换器
    converter = DrumConverter()
    
    print("=== Rust游戏鼓谱MIDI转换工具示例 ===\n")
    
    # 1. 查看当前映射关系
    print("1. 查看当前映射关系:")
    converter.list_mappings()
    print()
    
    # 2. 更新映射关系示例
    print("2. 更新映射关系示例:")
    # 这里可以添加你测试后的正确映射关系
    # converter.update_mapping(35, 36, "底鼓")
    # converter.update_mapping(38, 39, "军鼓")
    print("   (需要先在游戏中测试后更新映射关系)")
    print()
    
    # 3. 分析MIDI文件示例
    print("3. 分析MIDI文件示例:")
    # 如果有示例MIDI文件，可以取消注释下面的代码
    # if os.path.exists("example_drum.mid"):
    #     converter.analyze_midi("example_drum.mid")
    # else:
    print("   (需要提供MIDI文件进行分析)")
    print()
    
    # 4. 转换示例
    print("4. 转换示例:")
    print("   鼓谱转钢琴键位:")
    print("   python drum_converter.py drum2piano input_drum.mid output_piano.mid")
    print()
    print("   钢琴键位转鼓谱:")
    print("   python drum_converter.py piano2drum input_piano.mid output_drum.mid")
    print()
    
    # 5. 创建测试MIDI文件
    print("5. 创建测试MIDI文件:")
    create_test_midi()
    print("   已创建 test_drum.mid 测试文件")
    print()

def create_test_midi():
    """创建一个简单的测试鼓谱MIDI文件"""
    import mido
    from mido import Message, MidiFile, MidiTrack
    
    # 创建MIDI文件
    midi = MidiFile()
    track = MidiTrack()
    midi.tracks.append(track)
    
    # 设置鼓轨
    track.append(Message('program_change', program=0, time=0, channel=9))
    
    # 添加一些简单的鼓点
    # 底鼓 (35)
    track.append(Message('note_on', note=35, velocity=100, time=0, channel=9))
    track.append(Message('note_off', note=35, velocity=0, time=480, channel=9))
    
    # 军鼓 (38)
    track.append(Message('note_on', note=38, velocity=100, time=0, channel=9))
    track.append(Message('note_off', note=38, velocity=0, time=480, channel=9))
    
    # 踩镲 (42)
    track.append(Message('note_on', note=42, velocity=80, time=0, channel=9))
    track.append(Message('note_off', note=42, velocity=0, time=240, channel=9))
    track.append(Message('note_on', note=42, velocity=80, time=0, channel=9))
    track.append(Message('note_off', note=42, velocity=0, time=240, channel=9))
    
    # 保存文件
    midi.save('test_drum.mid')

if __name__ == '__main__':
    main() 