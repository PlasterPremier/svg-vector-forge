"""Pydantic models for jobs and results."""
from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field


class JobRequest(BaseModel):
    source: Path
    output_dir: Path = Path("out")
    plugin: str = "vtrace"
    palette_size: int = Field(default=16, ge=2, le=256)
    simplify_tolerance: float = Field(default=1.5, ge=0.0, le=20.0)
    width_px: int | None = None


class JobResult(BaseModel):
    output_path: Path
    path_count: int
    duration_ms: int
    plugin_name: str