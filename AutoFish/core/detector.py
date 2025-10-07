import logging
import time
from dataclasses import dataclass
from typing import List, Optional, Tuple

import cv2
import numpy as np


@dataclass
class DetectorConfig:
    threshold: float
    consecutive_required: int
    cooldown_s: float
    scales: List[float]


class LootDetector:
    def __init__(self, template_path: str, cfg: DetectorConfig) -> None:
        self._cfg = cfg
        base = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
        if base is None:
            logging.error("Template not found at %s", template_path)
            self._templates: List[Tuple[float, np.ndarray]] = []
        else:
            self._templates = []
            for s in cfg.scales:
                scaled = cv2.resize(base, None, fx=s, fy=s, interpolation=cv2.INTER_AREA)
                self._templates.append((s, scaled))
        self._streak = 0
        self._last_trigger_time = 0.0

    def detect(self, frame_bgr: np.ndarray) -> Tuple[bool, float]:
        if not self._templates:
            return False, 0.0
        gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)
        best_score = 0.0
        for _, tmpl in self._templates:
            if gray.shape[0] < tmpl.shape[0] or gray.shape[1] < tmpl.shape[1]:
                continue
            res = cv2.matchTemplate(gray, tmpl, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, _ = cv2.minMaxLoc(res)
            if max_val > best_score:
                best_score = max_val
        if best_score >= self._cfg.threshold:
            self._streak += 1
        else:
            self._streak = 0
        now = time.monotonic()
        if self._streak >= self._cfg.consecutive_required and (now - self._last_trigger_time) >= self._cfg.cooldown_s:
            self._last_trigger_time = now
            self._streak = 0
            return True, best_score
        return False, best_score
