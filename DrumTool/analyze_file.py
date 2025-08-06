#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分析用户MIDI文件
检查转换前后的通道和乐器设置
"""

import sys
import mido

def analyze_midi_file(filename):
    print(f"\n=== 分析: {filename} ===")
    
    try:
        midi = mido.MidiFile(filename)
        
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
    
    except Exception as e:
        print(f"分析失败: {e}")

def main():
    if len(sys.argv) < 2:
        print("使用方法: python analyze_file.py <MIDI文件路径>")
        return
    
    filename = sys.argv[1]
    analyze_midi_file(filename)

if __name__ == '__main__':
    main() 