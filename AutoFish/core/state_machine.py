import logging
import time
from dataclasses import dataclass
from typing import List

from .capture import ROIConfig, ScreenCapture
from .detector import DetectorConfig, LootDetector
from .input_controller import InputController
from .window_x11 import WindowGeometry


@dataclass
class CastConfig:
    right_hold_ms: int
    post_left_delay_ms: int
    keep_right_during_wait: bool


class FishingStateMachine:
    def __init__(
        self,
        window: WindowGeometry,
        roi_cfg: ROIConfig,
        fps: int,
        detector: LootDetector,
        input_ctrl: InputController,
        switch_keys: List[str],
        switch_pause_ms: int,
        wait_timeout_s: int,
    ) -> None:
        self._window = window
        self._roi_cfg = roi_cfg
        self._capture = ScreenCapture(fps)
        self._detector = detector
        self._input = input_ctrl
        self._switch_keys = switch_keys
        self._switch_pause_ms = switch_pause_ms
        self._wait_timeout_s = wait_timeout_s
        self._running = False
        # 从 0 开始（对应 switch_keys[0]，例如 "1"），每次命中后在 0 与 1 间切换
        self._rod_index = 0

    def start(self) -> None:
        self._running = True

    def stop(self) -> None:
        self._running = False

    def run_once(self, cast_cfg: CastConfig) -> None:
        # 抛竿
        self._input.perform_cast(
            right_hold_ms=cast_cfg.right_hold_ms,
            post_left_delay_ms=cast_cfg.post_left_delay_ms,
            keep_right_during_wait=cast_cfg.keep_right_during_wait,
            window_id=self._window.window_id,
        )
        logging.info("Casting done; waiting for loot cue...")
        # 等待入库提示
        t0 = time.monotonic()
        detected = False
        last_score = 0.0
        while self._running and (time.monotonic() - t0) < self._wait_timeout_s:
            frame = self._capture.grab_roi(self._window, self._roi_cfg)
            hit, score = self._detector.detect(frame)
            last_score = score
            if hit:
                detected = True
                logging.info("Loot detected, score=%.3f", score)
                break
        # 只有在检测命中时才切竿，并且按 0<->1 交替
        if detected:
            # 如果 keys 多于 1，按交替 0<->1；若只有 1 个键则不过度切换
            if len(self._switch_keys) >= 2:
                # 下一个使用的键索引
                self._rod_index = 1 - self._rod_index
                key_to_press = [self._switch_keys[self._rod_index]]
                self._input.switch_rod(key_to_press, self._switch_pause_ms, self._window.window_id)
            elif len(self._switch_keys) == 1:
                self._input.switch_rod([self._switch_keys[0]], self._switch_pause_ms, self._window.window_id)
        else:
            logging.info("No loot detected within timeout (last score=%.3f); re-cast without switching", last_score)

    def loop(self, cast_cfg: CastConfig) -> None:
        self._running = True
        while self._running:
            self.run_once(cast_cfg)
