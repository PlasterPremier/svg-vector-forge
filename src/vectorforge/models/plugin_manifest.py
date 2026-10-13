"""PluginManifest — validated at load time."""
from __future__ import annotations

from pydantic import BaseModel, Field


class PluginManifest(BaseModel):
    name: str = Field(pattern=r"^[a-z0-9_\-]{2,64}$")
    version: str
    author: str
    capabilities: list[str] = Field(min_length=1)
    requires: list[str] = Field(default_factory=list)
    sha256: str | None = None
    min_host_version: str = "0.9.0"