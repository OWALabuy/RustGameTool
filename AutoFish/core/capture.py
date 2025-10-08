import threading
import time
from dataclasses import dataclass
from typing import Tuple

import numpy as np
from mss import mss

from .window_x11 import WindowGeometry


@dataclass
class ROIConfig:
    width_pct: float
    height_pct: float
    margin_right_pct: float
    margin_bottom_pct: float


class ScreenCapture:
    def __init__(self, fps: int) -> None:
        self._frame_interval_s = 1.0 / max(1, fps)
        self._tls = threading.local()

    def _ensure_ctx(self) -> None:
        if not hasattr(self._tls, "sct"):
            self._tls.sct = mss()
            self._tls.last_grab_time = 0.0

    @staticmethod
    def compute_roi_rect(window: WindowGeometry, cfg: ROIConfig) -> Tuple[int, int, int, int]:
        roi_width = int(window.width * cfg.width_pct)
        roi_height = int(window.height * cfg.height_pct)
        margin_right = int(window.width * cfg.margin_right_pct)
        margin_bottom = int(window.height * cfg.margin_bottom_pct)
        left = window.left + window.width - margin_right - roi_width
        top = window.top + window.height - margin_bottom - roi_height
        return left, top, roi_width, roi_height

    def grab_roi(self, window: WindowGeometry, cfg: ROIConfig) -> np.ndarray:
        self._ensure_ctx()
        now = time.monotonic()
        sleep_s = self._frame_interval_s - (now - getattr(self._tls, "last_grab_time", 0.0))
        if sleep_s > 0:
            time.sleep(sleep_s)
        left, top, width, height = self.compute_roi_rect(window, cfg)
        raw = self._tls.sct.grab({"left": left, "top": top, "width": width, "height": height})
        self._tls.last_grab_time = time.monotonic()
        frame = np.asarray(raw, dtype=np.uint8)
        return frame[:, :, :3]
