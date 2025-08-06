#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
叮叮镲使用示例
展示如何在鼓谱中使用叮叮镲（Ride Cymbal）
"""

import mido
from mido import Message, MidiFile, MidiTrack
from drum_converter import DrumConverter

def create_ride_example():
    """创建叮叮镲使用示例"""
    
    # 创建MIDI文件
    midi = MidiFile()
    track = MidiTrack()
    midi.tracks.append(track)
    
    # 设置鼓轨
    track.append(Message('program_change', program=0, time=0, channel=9))
    
    # 创建一个简单的爵士节奏，突出叮叮镲的使用
    # 每小节的拍子：1-2-3-4
    # 叮叮镲：每拍都打
    # 底鼓：1和3拍
    # 军鼓：2和4拍
    # 踩镲：2和4拍
    
    # 第一小节
    # 叮叮镲 (51) - 每拍
    track.append(Message('note_on', note=51, velocity=80, time=0, channel=9))
    track.append(Message('note_off', note=51, velocity=0, time=240, channel=9))
    track.append(Message('note_on', note=51, velocity=80, time=0, channel=9))
    track.append(Message('note_off', note=51, velocity=0, time=240, channel=9))
    track.append(Message('note_on', note=51, velocity=80, time=0, channel=9))
    track.append(Message('note_off', note=51, velocity=0, time=240, channel=9))
    track.append(Message('note_on', note=51, velocity=80, time=0, channel=9))
    track.append(Message('note_off', note=51, velocity=0, time=240, channel=9))
    
    # 底鼓 (35) - 1和3拍
    track.append(Message('note_on', note=35, velocity=100, time=0, channel=9))
    track.append(Message('note_off', note=35, velocity=0, time=240, channel=9))
    track.append(Message('note_on', note=35, velocity=100, time=0, channel=9))
    track.append(Message('note_off', note=35, velocity=0, time=240, channel=9))
    
    # 军鼓 (38) - 2和4拍
    track.append(Message('note_on', note=38, velocity=100, time=0, channel=9))
    track.append(Message('note_off', note=38, velocity=0, time=240, channel=9))
    track.append(Message('note_on', note=38, velocity=100, time=0, channel=9))
    track.append(Message('note_off', note=38, velocity=0, time=240, channel=9))
    
    # 踩镲 (42) - 2和4拍
    track.append(Message('note_on', note=42, velocity=90, time=0, channel=9))
    track.append(Message('note_off', note=42, velocity=0, time=240, channel=9))
    track.append(Message('note_on', note=42, velocity=90, time=0, channel=9))
    track.append(Message('note_off', note=42, velocity=0, time=240, channel=9))
    
    # 保存文件
    midi.save('ride_example.mid')
    print("已创建叮叮镲示例文件: ride_example.mid")
    print("这个文件展示了一个基本的爵士节奏，叮叮镲在每拍都打")

def convert_ride_example():
    """转换叮叮镲示例为Rust可播放格式"""
    converter = DrumConverter()
    
    try:
        converter.drum_to_piano_midi('ride_example.mid', 'ride_example_rust.mid')
        print("已转换为Rust格式: ride_example_rust.mid")
        print("可以在Rust游戏中播放这个文件测试叮叮镲效果")
    except Exception as e:
        print(f"转换失败: {e}")

def show_ride_mapping():
    """显示叮叮镲的映射信息"""
    print("=== 叮叮镲映射信息 ===")
    print("GM鼓音符: 51 (Ride Cymbal 1)")
    print("Rust钢琴键位: F#3 (MIDI音符 54)")
    print("说明: 叮叮镲映射到原牛铃位置，因为使用频率更高")
    print()
    print("在MuseScore中使用:")
    print("1. 在鼓谱中添加Ride Cymbal音符")
    print("2. 导出为MIDI文件")
    print("3. 使用转换工具转换为Rust格式")
    print("4. 在Rust游戏中播放，F#3键位会触发叮叮镲音色")

def main():
    """主函数"""
    print("=== 叮叮镲使用示例 ===")
    print()
    
    # 显示映射信息
    show_ride_mapping()
    print()
    
    # 创建示例文件
    print("=== 创建示例文件 ===")
    create_ride_example()
    print()
    
    # 转换文件
    print("=== 转换为Rust格式 ===")
    convert_ride_example()
    print()
    
    print("=== 使用说明 ===")
    print("1. ride_example.mid - 原始鼓谱MIDI（可在MuseScore中查看）")
    print("2. ride_example_rust.mid - Rust可播放格式")
    print("3. 在Rust游戏中播放ride_example_rust.mid测试叮叮镲效果")
    print()
    print("叮叮镲特点:")
    print("- 持续音色，适合作为节奏的基础")
    print("- 在爵士、摇滚等风格中经常使用")
    print("- 可以配合开镲创造丰富的镲片音色")

if __name__ == '__main__':
    main() 