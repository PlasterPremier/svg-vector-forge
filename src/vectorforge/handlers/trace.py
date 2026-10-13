"""Trace handler — thin wrapper around vtracer's Python bindings."""
from __future__ import annotations

import logging
from pathlib import Path

import numpy as np

log = logging.getLogger(__name__)


def trace_to_svg(
    rgba: np.ndarray,
    out_path: Path,
    *,
    color_precision: int = 6,
    filter_speckle: int = 4,
    corner_threshold: int = 60,
) -> int:
    """Run vtracer and write SVG. Returns the number of path elements emitted.

    vtracer >= 0.6.11 expects HxWx4 uint8; older versions accepted HxWx3 and
    silently produced a black canvas — the alpha channel is added here.
    """
    import vtracer  # type: ignore[import-untyped]

    if rgba.shape[-1] == 3:
        alpha = np.full(rgba.shape[:2] + (1,), 255, dtype=np.uint8)
        rgba = np.concatenate([rgba, alpha], axis=-1)

    svg = vtracer.convert_pixels_to_svg(
        rgba,
        colormode="color",
        hierarchical="stacked",
        mode="spline",
        filter_speckle=filter_speckle,
        color_precision=color_precision,
        corner_threshold=corner_threshold,
    )
    out_path.write_text(svg, encoding="utf-8")
    return svg.count("<path")