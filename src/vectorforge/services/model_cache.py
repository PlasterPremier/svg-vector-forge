"""ModelCache — single owner of loaded weights, guarded by an asyncio.Lock."""
from __future__ import annotations

import asyncio
import logging
from pathlib import Path
from typing import Any

log = logging.getLogger(__name__)


class ModelCache:
    def __init__(self, root: Path) -> None:
        self.root = root
        self._lock = asyncio.Lock()
        self._loaded: dict[str, Any] = {}

    async def get(self, key: str, loader) -> Any:  # type: ignore[no-untyped-def]
        async with self._lock:
            if key not in self._loaded:
                path = self.root / key
                log.info("loading weights %s", path)
                self._loaded[key] = loader(path)
            return self._loaded[key]

    async def evict(self, key: str) -> None:
        async with self._lock:
            self._loaded.pop(key, None)

    async def clear(self) -> None:
        async with self._lock:
            self._loaded.clear()