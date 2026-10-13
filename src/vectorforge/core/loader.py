"""PluginLoader — entry-point + config-dir discovery, topo-sorted registration."""
from __future__ import annotations

import importlib
import importlib.metadata as md
import logging
import tomllib
from pathlib import Path
from typing import Any

from vectorforge.config.paths import plugin_search_paths
from vectorforge.contracts.plugin import VectorForgePlugin
from vectorforge.core.registry import PluginRegistry
from vectorforge.models.plugin_manifest import PluginManifest

log = logging.getLogger(__name__)
ENTRY_GROUP = "vectorforge.plugins"


class PluginLoader:
    def __init__(self, registry: PluginRegistry) -> None:
        self.registry = registry
        self._pending: list[tuple[PluginManifest, VectorForgePlugin]] = []

    def load_from_entry_points(self) -> None:
        for ep in md.entry_points(group=ENTRY_GROUP):
            try:
                cls = ep.load()
                instance = cls()
                self._stage(instance)
            except Exception:  # noqa: BLE001 — one bad plugin must not kill the host
                log.exception("failed to load entry point %s", ep.name)
        self._flush()

    def load_from_config(self) -> None:
        for base in plugin_search_paths():
            cfg = base / "plugins.toml"
            if not cfg.exists():
                continue
            data: dict[str, Any] = tomllib.loads(cfg.read_text("utf-8"))
            for entry in data.get("plugin", ()):
                mod = importlib.import_module(entry["module"])
                instance = getattr(mod, entry["class"])()
                self._stage(instance)
        self._flush()

    def _stage(self, instance: VectorForgePlugin) -> None:
        manifest = instance.manifest
        instance.setup()
        self._pending.append((manifest, instance))

    def _flush(self) -> None:
        for _manifest, instance in self._toposort(self._pending):
            self.registry.register(instance)
        self._pending.clear()

    @staticmethod
    def _toposort(
        items: list[tuple[PluginManifest, VectorForgePlugin]],
    ) -> list[tuple[PluginManifest, VectorForgePlugin]]:
        by_name = {m.name: (m, p) for m, p in items}
        ordered: list[tuple[PluginManifest, VectorForgePlugin]] = []
        seen: set[str] = set()

        def visit(name: str) -> None:
            if name in seen or name not in by_name:
                return
            manifest, plugin = by_name[name]
            for dep in manifest.requires:
                visit(dep)
            seen.add(name)
            ordered.append((manifest, plugin))

        for name in by_name:
            visit(name)
        return ordered