"""File watcher — hot-reloads plugins from the user plugin dir."""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Callable

from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

log = logging.getLogger(__name__)


class _PluginReloadHandler(FileSystemEventHandler):
    def __init__(self, on_change: Callable[[Path], None]) -> None:
        self._on_change = on_change

    def on_modified(self, event: FileSystemEvent) -> None:
        if event.is_directory:
            return
        path = Path(event.src_path)
        if path.suffix == ".py":
            log.info("plugin changed: %s", path.name)
            self._on_change(path)


def watch_plugins(directory: Path, on_change: Callable[[Path], None]) -> Observer:
    observer = Observer()
    observer.schedule(_PluginReloadHandler(on_change), str(directory), recursive=True)
    observer.start()
    return observer