#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试通道转换修复
验证鼓谱到钢琴的转换是否正确处理了通道和乐器设置
"""

import mido
from mido import Message, MidiFile, MidiTrack
from drum_converter import DrumConverter

def create_test_drum_midi():
    """创建一个测试鼓谱MIDI文件"""
    
    # 创建MIDI文件
    midi = MidiFile()
    track = MidiTrack()
    midi.tracks.append(track)
    
    # 设置鼓轨（通道9，乐器0）
    track.append(Message('program_change', program=0, time=0, channel=9))
    
    # 添加一些鼓音符
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
    midi.save('test_channel_drums.mid')
    print("已创建测试鼓谱文件: test_channel_drums.mid")

def analyze_midi_channels(input_file):
    """分析MIDI文件的通道信息"""
    print(f"\n=== 分析MIDI文件: {input_file} ===")
    
    midi = mido.MidiFile(input_file)
    
    for i, track in enumerate(midi.tracks):
        print(f"\n轨道 {i}:")
        
        # 查找program_change消息
        for msg in track:
            if msg.type == 'program_change':
                print(f"  乐器变更: 通道 {msg.channel}, 乐器 {msg.program}")
        
        # 统计音符的通道分布
        channels = {}
        for msg in track:
            if msg.type in ['note_on', 'note_off']:
                if msg.channel not in channels:
                    channels[msg.channel] = 0
                channels[msg.channel] += 1
        
        for channel, count in channels.items():
            print(f"  通道 {channel}: {count} 个音符")

def test_conversion():
    """测试转换功能"""
    print("\n=== 测试转换功能 ===")
    
    converter = DrumConverter()
    
    try:
        # 转换鼓谱到钢琴
        converter.drum_to_piano_midi('test_channel_drums.mid', 'test_channel_piano.mid')
        print("✓ 鼓谱转钢琴转换成功")
        
        # 分析转换后的文件
        analyze_midi_channels('test_channel_piano.mid')
        
    except Exception as e:
        print(f"✗ 转换失败: {e}")

def main():
    """主函数"""
    print("=== 通道转换修复测试 ===")
    
    # 创建测试文件
    print("\n1. 创建测试鼓谱文件")
    create_test_drum_midi()
    
    # 分析原始文件
    print("\n2. 分析原始鼓谱文件")
    analyze_midi_channels('test_channel_drums.mid')
    
    # 测试转换
    print("\n3. 测试转换功能")
    test_conversion()
    
    print("\n=== 测试完成 ===")
    print("如果转换成功，test_channel_piano.mid 应该显示为钢琴轨道（通道0）")
    print("而不是鼓轨（通道9/10）")

if __name__ == '__main__':
    main() 