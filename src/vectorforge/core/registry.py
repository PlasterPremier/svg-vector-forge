"""Capability-keyed plugin registry."""
from __future__ import annotations

from collections import defaultdict
from typing import Iterable

from vectorforge.contracts.plugin import VectorForgePlugin


class PluginRegistry:
    def __init__(self) -> None:
        self._by_name: dict[str, VectorForgePlugin] = {}
        self._by_cap: dict[str, list[VectorForgePlugin]] = defaultdict(list)

    def register(self, plugin: VectorForgePlugin) -> None:
        name = plugin.manifest.name
        if name in self._by_name:
            raise ValueError(f"plugin already registered: {name}")
        self._by_name[name] = plugin
        for cap in plugin.manifest.capabilities:
            self._by_cap[cap].append(plugin)

    def get(self, name: str) -> VectorForgePlugin:
        return self._by_name[name]

    def resolve(self, capability: str) -> list[VectorForgePlugin]:
        return list(self._by_cap.get(capability, ()))

    def __len__(self) -> int:
        return len(self._by_name)

    def __iter__(self) -> Iterable[VectorForgePlugin]:
        return iter(self._by_name.values())