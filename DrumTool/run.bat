@echo off
chcp 65001 >nul
echo ========================================
echo    Rust游戏鼓谱MIDI转换工具
echo ========================================
echo.

if "%1"=="" (
    echo 使用方法:
    echo   run.bat drum2piano 输入文件.mid 输出文件.mid
    echo   run.bat piano2drum 输入文件.mid 输出文件.mid
    echo   run.bat analyze 输入文件.mid
    echo   run.bat list-mappings
    echo   run.bat update-mapping 鼓音符 钢琴音符 "鼓名称"
    echo   run.bat example
    echo   run.bat test
    echo   run.bat ride
    echo   run.bat channel-test
    echo.
    echo 示例:
    echo   run.bat drum2piano drum_score.mid piano_ready.mid
    echo   run.bat analyze drum_score.mid
    echo   run.bat test
    echo.
    goto :end
)

if "%1"=="example" (
    python example_usage.py
    goto :end
)

if "%1"=="test" (
    python test_rust_mapping.py
    goto :end
)

if "%1"=="ride" (
    python ride_example.py
    goto :end
)

if "%1"=="channel-test" (
    python test_channel_fix.py
    goto :end
)

python drum_converter.py %*

:end
pause 