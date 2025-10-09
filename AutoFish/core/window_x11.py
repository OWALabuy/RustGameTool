import logging
import shlex
import subprocess
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class WindowGeometry:
    window_id: str
    left: int
    top: int
    width: int
    height: int


def _run(cmd: str) -> str:
    out = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT)
    return out.decode("utf-8", errors="ignore")


def find_window_id_by_patterns(patterns: List[str]) -> Optional[str]:
    for pat in patterns:
        try:
            out = _run(f"xdotool search --name {shlex.quote(pat)}")
            candidates = [line.strip() for line in out.splitlines() if line.strip()]
            if candidates:
                logging.info("Found window '%s' => %s", pat, candidates[0])
                return candidates[0]
        except subprocess.CalledProcessError:
            continue
    return None


def activate_window(window_id: str) -> None:
    try:
        _run(f"xdotool windowactivate {window_id}")
    except subprocess.CalledProcessError:
        logging.warning("Failed to activate window %s", window_id)


def get_window_geometry(window_id: str) -> Optional[WindowGeometry]:
    try:
        out = _run(f"xdotool getwindowgeometry --shell {window_id}")
        env = {}
        for line in out.splitlines():
            if "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip()
        left = int(env.get("X", "0"))
        top = int(env.get("Y", "0"))
        width = int(env.get("WIDTH", "0"))
        height = int(env.get("HEIGHT", "0"))
        if width <= 0 or height <= 0:
            return None
        return WindowGeometry(window_id=window_id, left=left, top=top, width=width, height=height)
    except Exception as exc:  # noqa: BLE001
        logging.error("get_window_geometry error: %s", exc)
        return None


