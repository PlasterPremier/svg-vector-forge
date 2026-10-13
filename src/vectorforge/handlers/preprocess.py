"""Raster preprocess handler — alpha flatten, denoise, palette quantize."""
from __future__ import annotations

import numpy as np
from PIL import Image


def flatten_alpha(img: Image.Image, background: tuple[int, int, int] = (255, 255, 255)) -> Image.Image:
    """Composite RGBA over a solid background. Returns RGB."""
    if img.mode not in ("RGBA", "LA"):
        return img.convert("RGB")
    base = Image.new("RGB", img.size, background)
    base.paste(img, mask=img.split()[-1])
    return base


def quantize_palette(img: Image.Image, colors: int) -> Image.Image:
    """Median-cut quantization. `colors` is clamped to [2, 256] by the model."""
    return img.convert("P", palette=Image.Palette.ADAPTIVE, colors=colors).convert("RGB")


def to_array(img: Image.Image) -> np.ndarray:
    return np.asarray(img, dtype=np.uint8)