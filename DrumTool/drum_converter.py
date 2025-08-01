#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rust游戏鼓谱MIDI转换工具
将MuseScore的鼓谱MIDI转换为Rust可演奏的钢琴键位，以及反向转换
"""

import json
import mido
import click
from pathlib import Path
from typing import Dict, List, Tuple, Optional


class DrumConverter:
    """鼓谱MIDI转换器"""
    
    def __init__(self, mapping_file: str = "drum_mapping.json"):
        """初始化转换器
        
        Args:
            mapping_file: 映射配置文件路径
        """
        self.mapping_file = mapping_file
        self.load_mapping()
    
    def load_mapping(self):
        """加载映射配置"""
        try:
            with open(self.mapping_file, 'r', encoding='utf-8') as f:
                self.mapping = json.load(f)
            self.drum_to_piano = {int(k): int(v) for k, v in self.mapping['drum_to_piano'].items()}
            self.piano_to_drum = {int(k): int(v) for k, v in self.mapping['piano_to_drum'].items()}
            self.drum_names = {int(k): v for k, v in self.mapping['drum_names'].items()}
        except FileNotFoundError:
            click.echo(f"错误: 找不到映射文件 {self.mapping_file}")
            raise
        except json.JSONDecodeError:
            click.echo(f"错误: 映射文件 {self.mapping_file} 格式错误")
            raise
    
    def save_mapping(self):
        """保存映射配置"""
        with open(self.mapping_file, 'w', encoding='utf-8') as f:
            json.dump(self.mapping, f, indent=2, ensure_ascii=False)
    
    def update_mapping(self, drum_note: int, piano_note: int, drum_name: str = None):
        """更新映射关系
        
        Args:
            drum_note: 鼓音符号
            piano_note: 钢琴音符号
            drum_name: 鼓的名称（可选）
        """
        self.drum_to_piano[drum_note] = piano_note
        self.piano_to_drum[piano_note] = drum_note
        
        # 更新JSON映射
        self.mapping['drum_to_piano'][str(drum_note)] = piano_note
        self.mapping['piano_to_drum'][str(piano_note)] = drum_note
        
        if drum_name:
            self.drum_names[drum_note] = drum_name
            self.mapping['drum_names'][str(drum_note)] = drum_name
        
        self.save_mapping()
        click.echo(f"已更新映射: 鼓 {drum_note} ({drum_name or '未知'}) -> 钢琴 {piano_note}")
    
    def drum_to_piano_midi(self, input_file: str, output_file: str, channel: int = 9):
        """将鼓谱MIDI转换为钢琴键位MIDI
        
        Args:
            input_file: 输入鼓谱MIDI文件
            output_file: 输出钢琴MIDI文件
            channel: 鼓轨通道（通常为9）
        """
        try:
            midi = mido.MidiFile(input_file)
            new_midi = mido.MidiFile()
            
            # 复制元数据
            new_midi.ticks_per_beat = midi.ticks_per_beat
            
            for track in midi.tracks:
                new_track = mido.MidiTrack()
                
                for msg in track:
                    if msg.type in ['note_on', 'note_off']:
                        # 如果是鼓轨（通道9）
                        if msg.channel == channel:
                            # 转换鼓音符到钢琴音符
                            if msg.note in self.drum_to_piano:
                                new_note = self.drum_to_piano[msg.note]
                                new_msg = msg.copy(note=new_note, channel=0)  # 转换为钢琴通道
                                new_track.append(new_msg)
                            else:
                                click.echo(f"警告: 未找到鼓音符 {msg.note} 的映射")
                        else:
                            # 非鼓轨直接复制
                            new_track.append(msg)
                    else:
                        # 其他消息直接复制
                        new_track.append(msg)
                
                new_midi.tracks.append(new_track)
            
            new_midi.save(output_file)
            click.echo(f"转换完成: {input_file} -> {output_file}")
            
        except Exception as e:
            click.echo(f"转换失败: {e}")
            raise
    
    def piano_to_drum_midi(self, input_file: str, output_file: str, channel: int = 0):
        """将钢琴键位MIDI转换为鼓谱MIDI
        
        Args:
            input_file: 输入钢琴MIDI文件
            output_file: 输出鼓谱MIDI文件
            channel: 钢琴轨通道（通常为0）
        """
        try:
            midi = mido.MidiFile(input_file)
            new_midi = mido.MidiFile()
            
            # 复制元数据
            new_midi.ticks_per_beat = midi.ticks_per_beat
            
            for track in midi.tracks:
                new_track = mido.MidiTrack()
                
                for msg in track:
                    if msg.type in ['note_on', 'note_off']:
                        # 如果是钢琴轨
                        if msg.channel == channel:
                            # 转换钢琴音符到鼓音符
                            if msg.note in self.piano_to_drum:
                                new_note = self.piano_to_drum[msg.note]
                                new_msg = msg.copy(note=new_note, channel=9)  # 转换为鼓通道
                                new_track.append(new_msg)
                            else:
                                click.echo(f"警告: 未找到钢琴音符 {msg.note} 的映射")
                        else:
                            # 非钢琴轨直接复制
                            new_track.append(msg)
                    else:
                        # 其他消息直接复制
                        new_track.append(msg)
                
                new_midi.tracks.append(new_track)
            
            new_midi.save(output_file)
            click.echo(f"转换完成: {input_file} -> {output_file}")
            
        except Exception as e:
            click.echo(f"转换失败: {e}")
            raise
    
    def analyze_midi(self, input_file: str):
        """分析MIDI文件中的音符
        
        Args:
            input_file: MIDI文件路径
        """
        try:
            midi = mido.MidiFile(input_file)
            notes = {}
            
            for track in midi.tracks:
                for msg in track:
                    if msg.type in ['note_on', 'note_off']:
                        if msg.note not in notes:
                            notes[msg.note] = {
                                'count': 0,
                                'channel': msg.channel,
                                'velocity': []
                            }
                        notes[msg.note]['count'] += 1
                        if msg.velocity > 0:
                            notes[msg.note]['velocity'].append(msg.velocity)
            
            click.echo(f"\nMIDI文件分析结果: {input_file}")
            click.echo("=" * 50)
            
            for note in sorted(notes.keys()):
                note_info = notes[note]
                channel_type = "鼓轨" if note_info['channel'] == 9 else "钢琴轨"
                avg_velocity = sum(note_info['velocity']) / len(note_info['velocity']) if note_info['velocity'] else 0
                
                click.echo(f"音符 {note}: 出现 {note_info['count']} 次, "
                          f"通道 {note_info['channel']} ({channel_type}), "
                          f"平均力度 {avg_velocity:.1f}")
                
                if note_info['channel'] == 9 and note in self.drum_names:
                    click.echo(f"  -> 鼓名称: {self.drum_names[note]}")
                    if note in self.drum_to_piano:
                        click.echo(f"  -> 映射到钢琴: {self.drum_to_piano[note]}")
                    else:
                        click.echo(f"  -> 未映射到钢琴")
            
        except Exception as e:
            click.echo(f"分析失败: {e}")
            raise
    
    def list_mappings(self):
        """列出所有映射关系"""
        click.echo("当前映射关系:")
        click.echo("=" * 50)
        
        for drum_note in sorted(self.drum_to_piano.keys()):
            piano_note = self.drum_to_piano[drum_note]
            drum_name = self.drum_names.get(drum_note, "未知")
            click.echo(f"鼓 {drum_note} ({drum_name}) -> 钢琴 {piano_note}")


@click.group()
def cli():
    """Rust游戏鼓谱MIDI转换工具"""
    pass


@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.argument('output_file', type=click.Path())
@click.option('--channel', '-c', default=9, help='鼓轨通道号 (默认: 9)')
def drum2piano(input_file, output_file, channel):
    """将鼓谱MIDI转换为钢琴键位MIDI"""
    converter = DrumConverter()
    converter.drum_to_piano_midi(input_file, output_file, channel)


@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.argument('output_file', type=click.Path())
@click.option('--channel', '-c', default=0, help='钢琴轨通道号 (默认: 0)')
def piano2drum(input_file, output_file, channel):
    """将钢琴键位MIDI转换为鼓谱MIDI"""
    converter = DrumConverter()
    converter.piano_to_drum_midi(input_file, output_file, channel)


@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
def analyze(input_file):
    """分析MIDI文件中的音符"""
    converter = DrumConverter()
    converter.analyze_midi(input_file)


@cli.command()
def list_mappings():
    """列出所有映射关系"""
    converter = DrumConverter()
    converter.list_mappings()


@cli.command()
@click.argument('drum_note', type=int)
@click.argument('piano_note', type=int)
@click.argument('drum_name', required=False)
def update_mapping(drum_note, piano_note, drum_name):
    """更新映射关系"""
    converter = DrumConverter()
    converter.update_mapping(drum_note, piano_note, drum_name)


if __name__ == '__main__':
    cli() 