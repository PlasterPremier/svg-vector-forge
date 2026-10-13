"""Path helpers — safe output naming, atomic writes."""
from __future__ import annotations

import os
import tempfile
from pathlib import Path


def atomic_write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(text)
        os.replace(tmp, path)
    except Exception:
        os.unlink(tmp)
        raise


def unique_stem(source: Path, output_dir: Path, ext: str = ".svg") -> Path:
    stem = source.stem
    candidate = output_dir / f"{stem}{ext}"
    n = 1
    while candidate.exists():
        candidate = output_dir / f"{stem}-{n}{ext}"
        n += 1
    return candidate