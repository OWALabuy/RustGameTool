import os
import sys
import platform

from typing import Optional


if os.name == "nt":
    from .window_win32 import (  # type: ignore[F401]
        WindowGeometry,
        activate_window,
        find_window_id_by_patterns,
        get_window_geometry,
    )
else:
    from .window_x11 import (  # type: ignore[F401]
        WindowGeometry,
        activate_window,
        find_window_id_by_patterns,
        get_window_geometry,
    )


