"""VectorForgeHost — owns the registry, loader, and pipeline."""
from __future__ import annotations

import logging
from dataclasses import dataclass

from vectorforge.core.loader import PluginLoader
from vectorforge.core.pipeline import Pipeline
from vectorforge.core.registry import PluginRegistry
from vectorforge.models.job import JobRequest, JobResult

log = logging.getLogger(__name__)


@dataclass
class VectorForgeHost:
    registry: PluginRegistry
    pipeline: Pipeline

    @classmethod
    def autoload(cls) -> "VectorForgeHost":
        registry = PluginRegistry()
        loader = PluginLoader(registry=registry)
        loader.load_from_entry_points()
        loader.load_from_config()
        log.info("registered %d plugins", len(registry))
        return cls(registry=registry, pipeline=Pipeline(registry=registry))

    def run(self, job: JobRequest) -> JobResult:
        return self.pipeline.execute(job)