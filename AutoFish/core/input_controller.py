import logging
import time
from typing import List

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
        self._ms.press(mouse.Button.right)
        self._sleep_ms(right_hold_ms)
        self._ms.click(mouse.Button.left, 1)
        self._sleep_ms(post_left_delay_ms)
        if not keep_right_during_wait:
            self._ms.release(mouse.Button.right)

    def switch_rod(self, keys: List[str], switch_pause_ms: int, window_id: str) -> None:
        if self._activate:
            activate_window(window_id)
            time.sleep(0.05)
        for key in keys:
            self._kb.press(key)
            self._kb.release(key)
            self._sleep_ms(switch_pause_ms)


class AltGraveHotkey:
    def __init__(self, on_toggle) -> None:
        self._on_toggle = on_toggle
        self._alt_pressed = False
        self._listener = keyboard.Listener(on_press=self._on_press, on_release=self._on_release)

    def _on_press(self, key) -> None:  # noqa: ANN001
        if key in (keyboard.Key.alt, keyboard.Key.alt_l, keyboard.Key.alt_r):
            self._alt_pressed = True
        elif getattr(key, "vk", None) == 96 or key == keyboard.Key.grave:  # backtick
            if self._alt_pressed:
                self._on_toggle()

    def _on_release(self, key) -> None:  # noqa: ANN001
        if key in (keyboard.Key.alt, keyboard.Key.alt_l, keyboard.Key.alt_r):
            self._alt_pressed = False

    def start(self) -> None:
        self._listener.start()

    def stop(self) -> None:
        self._listener.stop()
