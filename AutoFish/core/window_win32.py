import logging
import re
from dataclasses import dataclass
from typing import List, Optional

import ctypes
from ctypes import wintypes


@dataclass
class WindowGeometry:
    window_id: str  # HWND as stringified integer
    left: int
    top: int
    width: int
    height: int


user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32


EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)


def _get_window_text(hwnd: int) -> str:
    length = user32.GetWindowTextLengthW(hwnd)
    if length == 0:
        return ""
    buf = ctypes.create_unicode_buffer(length + 1)
    user32.GetWindowTextW(hwnd, buf, length + 1)
    return buf.value


def _is_window_valid(hwnd: int) -> bool:
    # Visible, not minimized, has title
    if not user32.IsWindowVisible(hwnd):
        return False
    title = _get_window_text(hwnd)
    if not title:
        return False
    # Filter tool windows (optional)
    return True


def find_window_id_by_patterns(patterns: List[str]) -> Optional[str]:
    matches: List[int] = []

    def enum_cb(hwnd: int, lparam: int) -> bool:  # noqa: ANN001
        try:
            if not _is_window_valid(hwnd):
                return True
            title = _get_window_text(hwnd)
            for pat in patterns:
                try:
                    if re.search(pat, title):
                        matches.append(hwnd)
                        return False  # stop on first match overall order respected by outer loop
                except re.error:
                    # fallback to substring if pattern invalid
                    if pat in title:
                        matches.append(hwnd)
                        return False
            return True
        except Exception:
            return True

    # We need to respect order of patterns; enumerate once but evaluate regex by order
    # Simpler: call EnumWindows once and collect titles, then run patterns order over that snapshot
    window_list: List[int] = []

    def collect_cb(hwnd: int, lparam: int) -> bool:  # noqa: ANN001
        if _is_window_valid(hwnd):
            window_list.append(hwnd)
        return True

    user32.EnumWindows(EnumWindowsProc(collect_cb), 0)

    titles = {hwnd: _get_window_text(hwnd) for hwnd in window_list}
    for pat in patterns:
        for hwnd, title in titles.items():
            try:
                ok = bool(re.search(pat, title))
            except re.error:
                ok = pat in title
            if ok:
                logging.info("Found window '%s' => %s", pat, title)
                return str(int(hwnd))
    return None


def activate_window(window_id: str) -> None:
    try:
        hwnd = int(window_id)
    except ValueError:
        logging.warning("Invalid window_id for activation: %s", window_id)
        return
    try:
        SW_RESTORE = 9
        user32.ShowWindow(hwnd, SW_RESTORE)
        # Try to set foreground
        if not user32.SetForegroundWindow(hwnd):
            # Fallback: bring to top
            user32.BringWindowToTop(hwnd)
    except Exception as exc:  # noqa: BLE001
        logging.warning("Failed to activate window %s: %s", window_id, exc)


def get_window_geometry(window_id: str) -> Optional[WindowGeometry]:
    try:
        hwnd = int(window_id)
    except ValueError:
        logging.error("Invalid window_id: %s", window_id)
        return None
    try:
        rect = wintypes.RECT()
        if not user32.GetWindowRect(hwnd, ctypes.byref(rect)):
            return None
        left, top, right, bottom = rect.left, rect.top, rect.right, rect.bottom
        width = max(0, right - left)
        height = max(0, bottom - top)
        if width == 0 or height == 0:
            return None
        return WindowGeometry(window_id=str(hwnd), left=left, top=top, width=width, height=height)
    except Exception as exc:  # noqa: BLE001
        logging.error("get_window_geometry error: %s", exc)
        return None


