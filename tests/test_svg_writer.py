from __future__ import annotations

from pathlib import Path

from vectorforge.utils.svg_writer import sanitize, write


def test_strips_script_tag() -> None:
    dirty = (
        '<svg xmlns="http://www.w3.org/2000/svg">'
        '<script>alert(1)</script>'