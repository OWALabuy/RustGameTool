import argparse
import logging
import threading
import time
from pathlib import Path

import yaml
import os
import sys

# Allow running via: python AutoFish/main.py or from inside AutoFish/
if __package__ is None or __package__ == "":
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from AutoFish.core.capture import ROIConfig
from AutoFish.core.detector import DetectorConfig, LootDetector
from AutoFish.core.input_controller import AltGraveHotkey, InputController
from AutoFish.core.logging_utils import setup_logging
from AutoFish.core.state_machine import CastConfig, FishingStateMachine
from AutoFish.core.window_backend import (
    WindowGeometry,
    activate_window,
    find_window_id_by_patterns,
    get_window_geometry,
)


def load_config(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def build_components(cfg: dict) -> tuple:
    patterns = cfg.get("window_name_patterns", ["Rust"])  # type: ignore[assignment]
    window_id = find_window_id_by_patterns(patterns)
    if not window_id:
        raise SystemExit("未找到 Rust 窗口（检查 window_name_patterns 或是否运行中）")
    if cfg.get("activate_window_before_actions", True):
        activate_window(window_id)
        time.sleep(0.05)
    geom = get_window_geometry(window_id)
    if not geom:
        raise SystemExit("无法获取窗口几何信息")

    roi_cfg = ROIConfig(
        width_pct=float(cfg["roi"]["width_pct"]),
        height_pct=float(cfg["roi"]["height_pct"]),
        margin_right_pct=float(cfg["roi"]["margin_right_pct"]),
        margin_bottom_pct=float(cfg["roi"]["margin_bottom_pct"]),
    )

    det_cfg = DetectorConfig(
        threshold=float(cfg["threshold"]),
        consecutive_required=int(cfg["consecutive_required"]),
        cooldown_s=float(cfg["cooldown_s"]),
        scales=[float(x) for x in cfg.get("scales", [1.0])],
    )

    detector = LootDetector(cfg["loot_template_path"], det_cfg)
    input_ctrl = InputController(cfg.get("activate_window_before_actions", True))
    sm = FishingStateMachine(
        window=geom,
        roi_cfg=roi_cfg,
        fps=int(cfg["fps"]),
        detector=detector,
        input_ctrl=input_ctrl,
        switch_keys=list(cfg.get("switch_keys", ["1", "2"])),
        switch_pause_ms=int(cfg.get("switch_pause_ms", 250)),
        wait_timeout_s=int(cfg.get("wait_timeout_s", 60)),
        detect_suppress_after_cast_s=float(cfg.get("detect_suppress_after_cast_s", 5.0)),
    )

    cast_cfg = CastConfig(
        right_hold_ms=int(cfg["cast"]["right_hold_ms"]),
        post_left_delay_ms=int(cfg["cast"]["post_left_delay_ms"]),
        keep_right_during_wait=bool(cfg["cast"]["keep_right_during_wait"]),
    )
    return sm, cast_cfg


def run_bot(cfg_path: str) -> None:
    setup_logging()
    cfg = load_config(Path(cfg_path))
    sm, cast_cfg = build_components(cfg)

    running = {"v": False}

    def toggle() -> None:
        if running["v"]:
            running["v"] = False
            sm.stop()
            logging.info("暂停自动钓鱼")
        else:
            running["v"] = True
            logging.info("开始自动钓鱼…… 按 Alt+` 可暂停/继续")
            t = threading.Thread(target=sm.loop, args=(cast_cfg,), daemon=True)
            t.start()

    hotkey = AltGraveHotkey(on_toggle=toggle)
    hotkey.start()

    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        sm.stop()


def main() -> None:
    parser = argparse.ArgumentParser(description="Rust AutoFish - Linux/Windows")
    parser.add_argument("command", choices=["run"], help="运行机器人")
    parser.add_argument("--config", default="AutoFish/config.yaml")
    args = parser.parse_args()

    if args.command == "run":
        run_bot(args.config)


if __name__ == "__main__":
    main()
