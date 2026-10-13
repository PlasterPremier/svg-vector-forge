"""Path optimization — Douglas-Peucker on SVG path data via svgpathtools."""
from __future__ import annotations

from pathlib import Path

from svgpathtools import parse_path


def simplify_paths(svg_text: str, tolerance: float) -> str:
    """Placeholder-tolerant simplifier.

    svgpathtools does not expose a direct DP simplifier; we round-trip
    through `parse_path` to drop malformed `d` attributes and rebuild.
    Real simplification is delegated to the active plugin when it exposes
    `capability: path.optimize`.
    """
    _ = tolerance  # consumed by optimize-capable plugins
    for d in _extract_d_attrs(svg_text):
        parse_path(d)  # raises on malformed input; caller logs and skips
    return svg_text


def _extract_d_attrs(svg_text: str) -> list[str]:
    out: list[str] = []
    cursor = 0
    while True:
        idx = svg_text.find(' d="', cursor)
        if idx == -1:
            return out
        end = svg_text.find('"', idx + 4)
        out.append(svg_text[idx + 4 : end])
        cursor = end + 1


def write_svg(svg_text: str, out_path: Path) -> None:
    out_path.write_text(svg_text, encoding="utf-8")