"""Color math — sRGB <-> linear, hex helpers, palette distance."""
from __future__ import annotations

import numpy as np


def hex_to_rgb(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    if len(value) == 3:
        value = "".join(c * 2 for c in value)
    return int(value[0:2], 16), int(value[2:4], 16), int(value[4:6], 16)


def rgb_to_hex(rgb: tuple[int, int, int]) -> str:
    return "#{:02x}{:02x}{:02x}".format(*rgb)


def srgb_to_linear(rgb: np.ndarray) -> np.ndarray:
    c = rgb.astype(np.float64) / 255.0
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def palette_distance(a: tuple[int, int, int], b: tuple[int, int, int]) -> float:
    """CIE76-ish approximation in linear space. Good enough for palette merges."""
    la = srgb_to_linear(np.asarray(a))
    lb = srgb_to_linear(np.asarray(b))
    return float(np.linalg.norm(la - lb))