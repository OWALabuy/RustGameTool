# Rust游戏鼓谱MIDI转换工具

这个工具用于将MuseScore编写的鼓谱MIDI文件转换为Rust游戏中可演奏的钢琴键位MIDI文件，以及反向转换。

## 功能特性

- 🥁 鼓谱MIDI → 钢琴键位MIDI转换
- 🎹 钢琴键位MIDI → 鼓谱MIDI转换
- 📊 MIDI文件分析功能
- 🔧 可配置的映射关系
- 📝 详细的命令行界面

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 1. 鼓谱转钢琴键位

将MuseScore的鼓谱MIDI转换为Rust可演奏的钢琴键位：

```bash
python drum_converter.py drum2piano input_drum.mid output_piano.mid
```

### 2. 钢琴键位转鼓谱

将钢琴键位MIDI转换回鼓谱格式：

```bash
python drum_converter.py piano2drum input_piano.mid output_drum.mid
```

### 3. 分析MIDI文件

分析MIDI文件中的音符信息：

```bash
python drum_converter.py analyze input.mid
```

### 4. 查看映射关系

查看当前的鼓谱到钢琴键位的映射关系：

```bash
python drum_converter.py list-mappings
```

### 5. 更新映射关系

更新特定鼓音符到钢琴键位的映射：

```bash
python drum_converter.py update-mapping 35 36 "底鼓"
```

## 映射配置

映射关系存储在 `drum_mapping.json` 文件中，包含：

- `drum_to_piano`: 鼓音符到钢琴音符的映射
- `piano_to_drum`: 钢琴音符到鼓音符的映射
- `drum_names`: 鼓音符对应的名称

### 通用MIDI鼓音符对照表

| 音符 | 鼓名称 | 音符 | 鼓名称 |
|------|--------|------|--------|
| 35 | Acoustic Bass Drum | 58 | Vibraslap |
| 36 | Bass Drum 1 | 59 | Ride Cymbal 2 |
| 37 | Side Stick | 60 | Hi Bongo |
| 38 | Acoustic Snare | 61 | Low Bongo |
| 39 | Hand Clap | 62 | Mute Hi Conga |
| 40 | Electric Snare | 63 | Open Hi Conga |
| 41 | Low Floor Tom | 64 | Low Conga |
| 42 | Closed Hi-Hat | 65 | High Timbale |
| 43 | High Floor Tom | 66 | Low Timbale |
| 44 | Pedal Hi-Hat | 67 | High Agogo |
| 45 | Low Tom | 68 | Low Agogo |
| 46 | Open Hi-Hat | 69 | Cabasa |
| 47 | Low-Mid Tom | 70 | Maracas |
| 48 | Hi-Mid Tom | 71 | Short Whistle |
| 49 | Crash Cymbal 1 | 72 | Long Whistle |
| 50 | High Tom | 73 | Short Guiro |
| 51 | Ride Cymbal 1 | 74 | Long Guiro |
| 52 | Chinese Cymbal | 75 | Claves |
| 53 | Ride Bell | 76 | Hi Wood Block |
| 54 | Tambourine | 77 | Low Wood Block |
| 55 | Splash Cymbal | 78 | Mute Cuica |
| 56 | Cowbell | 79 | Open Cuica |
| 57 | Crash Cymbal 2 | 80 | Mute Triangle |
| 81 | Open Triangle |

## 工作流程

1. **在MuseScore中编写鼓谱**
   - 创建新的鼓谱
   - 使用鼓谱工具编写节奏
   - 导出为MIDI文件

2. **使用工具转换**
   ```bash
   python drum_converter.py drum2piano your_drum_score.mid rust_ready.mid
   ```

3. **在Rust游戏中播放**
   - 将转换后的MIDI文件放入游戏
   - 使用游戏内的乐器系统播放

## 自定义映射

如果你发现某些鼓音符在Rust中的映射不正确，可以：

1. 分析原始MIDI文件：
   ```bash
   python drum_converter.py analyze your_drum_score.mid
   ```

2. 在游戏中测试并确定正确的映射关系

3. 更新映射配置：
   ```bash
   python drum_converter.py update-mapping <鼓音符> <钢琴音符> "<鼓名称>"
   ```

## 注意事项

- 鼓谱MIDI通常使用通道9（鼓轨）
- 钢琴MIDI使用通道0（钢琴轨）
- 确保映射关系正确，否则可能产生错误的音效
- 建议先用分析功能查看MIDI文件内容

## 故障排除

### 常见问题

1. **找不到映射文件**
   - 确保 `drum_mapping.json` 文件存在
   - 检查文件路径是否正确

2. **转换后没有声音**
   - 检查映射关系是否正确
   - 确认Rust游戏支持该MIDI格式

3. **音符映射错误**
   - 使用分析功能查看原始MIDI
   - 更新映射关系

### 获取帮助

```bash
python drum_converter.py --help
```

查看特定命令的帮助：

```bash
python drum_converter.py drum2piano --help
``` 