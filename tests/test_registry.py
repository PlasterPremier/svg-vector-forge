from __future__ import annotations

import pytest

from vectorforge.core.registry import PluginRegistry
from vectorforge.extensions.vtrace_plugin import VTracePlugin


def test_register_and_resolve() -> None:
    reg = PluginRegistry()
    reg.register(VTracePlugin())
    assert len(reg) == 1
    assert reg.resolve("raster.trace")
    assert reg.get("vtrace").manifest.version == "0.9.4"


def test_duplicate_name_rejected() -> None:
    reg = PluginRegistry()
    reg.register(VTracePlugin())
    with pytest.raises(ValueError, match="already registered"):
        reg.register(VTracePlugin())


def test_unknown_capability_returns_empty() -> None:
    reg = PluginRegistry()
    assert reg.resolve("nope.nope") == []