"""Plugin search paths — user dir wins over bundled dir."""
from __future__ import annotations

import os
from pathlib import Path


def plugin_search_paths() -> list[Path]:
    user = Path(os.environ.get("APPDATA", Path.home())) / "vectorforge" / "plugins"
    bundled = Path(__file__).resolve().parent / "plugins"
    return [p for p in (user, bundled) if p.exists()]


def model_root() -> Path:
    local = Path(os.environ.get("LOCALAPPDATA", Path.home()))
    return local / "vectorforge" / "models"