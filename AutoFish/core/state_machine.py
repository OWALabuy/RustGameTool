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

    def start(self) -> None:
        self._running = True

    def stop(self) -> None:
        self._running = False

    def run_once(self, cast_cfg: CastConfig) -> None:
        # Cast
        self._input.perform_cast(
            right_hold_ms=cast_cfg.right_hold_ms,
            post_left_delay_ms=cast_cfg.post_left_delay_ms,
            keep_right_during_wait=cast_cfg.keep_right_during_wait,
            window_id=self._window.window_id,
        )
        logging.info("Casting done; waiting for loot cue...")
        # Wait for loot
        t0 = time.monotonic()
        while self._running and (time.monotonic() - t0) < self._wait_timeout_s:
            frame = self._capture.grab_roi(self._window, self._roi_cfg)
            hit, score = self._detector.detect(frame)
            if hit:
                logging.info("Loot detected, score=%.3f", score)
                break
        # Switch rod and re-cast
        self._input.switch_rod(self._switch_keys, self._switch_pause_ms, self._window.window_id)

    def loop(self, cast_cfg: CastConfig) -> None:
        self._running = True
        while self._running:
            self.run_once(cast_cfg)
