import logging
import time
from typing import Callable, List, Optional

from pynput import keyboard, mouse

from .window_x11 import activate_window


class InputController:
    def __init__(self, activate_before_actions: bool) -> None:
        self._kb = keyboard.Controller()
        self._ms = mouse.Controller()
        self._activate = activate_before_actions

    @staticmethod
    def _sleep_ms(ms: int) -> None:
        time.sleep(max(0.0, ms / 1000.0))

    def perform_cast(self, right_hold_ms: int, post_left_delay_ms: int, keep_right_during_wait: bool, window_id: str) -> None:
        if self._activate:
            activate_window(window_id)
            time.sleep(0.05)
        # 按住右键 right_hold_ms 毫秒
        self._ms.press(mouse.Button.right)
        self._sleep_ms(right_hold_ms)
        # 在仍按住右键的同时，单击一次左键（显式按下/抬起）
        self._ms.press(mouse.Button.left)
        self._sleep_ms(10)
        self._ms.release(mouse.Button.left)
        # 很短延迟后释放右键，近似“同时松开两个键”
        self._sleep_ms(post_left_delay_ms)
        self._ms.release(mouse.Button.right)
        # keep_right_during_wait 对该抛竿动作不适用

    def switch_rod(self, keys: List[str], switch_pause_ms: int, window_id: str) -> None:
        if self._activate:
            activate_window(window_id)
            time.sleep(0.05)
        for key in keys:
            self._kb.press(key)
            self._kb.release(key)
            self._sleep_ms(switch_pause_ms)


class AltGraveHotkey:
    def __init__(self, on_toggle: Callable[[], None]) -> None:
        self._on_toggle = on_toggle
        self._alt_down = False
        self._last_toggle_ts: float = 0.0
        self._listener = keyboard.Listener(on_press=self._on_press, on_release=self._on_release)

    def _is_backtick(self, key) -> bool:  # noqa: ANN001
        # 反引号字符（`），在 pynput 中通常以 KeyCode.char 提供
        ch: Optional[str] = getattr(key, "char", None)
        return ch == "`"

    def _on_press(self, key) -> None:  # noqa: ANN001
        try:
            if key in (keyboard.Key.alt, keyboard.Key.alt_l, keyboard.Key.alt_r):
                self._alt_down = True
                return
            if self._alt_down and self._is_backtick(key):
                now = time.monotonic()
                if now - self._last_toggle_ts > 0.3:  # 防抖
                    self._last_toggle_ts = now
                    self._on_toggle()
        except Exception as exc:  # noqa: BLE001
            logging.error("Hotkey on_press error: %s", exc)

    def _on_release(self, key) -> None:  # noqa: ANN001
        if key in (keyboard.Key.alt, keyboard.Key.alt_l, keyboard.Key.alt_r):
            self._alt_down = False

    def start(self) -> None:
        self._listener.start()

    def stop(self) -> None:
        self._listener.stop()
