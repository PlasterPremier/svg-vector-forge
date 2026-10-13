"""Pipeline — resolves a job to a plugin and runs the stage chain."""
from __future__ import annotations

import logging

from vectorforge.core.registry import PluginRegistry
from vectorforge.models.job import JobRequest, JobResult

log = logging.getLogger(__name__)
CAPABILITY_BY_PLUGIN = {
    "vtrace": "raster.trace",
    "diffvg": "prompt.diffvg",
    "prompt2svg": "prompt.diffusion",
}


class Pipeline:
    def __init__(self, registry: PluginRegistry) -> None:
        self.registry = registry

    def execute(self, job: JobRequest) -> JobResult:
        capability = CAPABILITY_BY_PLUGIN.get(job.plugin, f"plugin.{job.plugin}")
        candidates = self.registry.resolve(capability)
        if not candidates:
            raise LookupError(f"no plugin provides capability {capability!r}")
        plugin = candidates[0]
        log.info("dispatching job %s -> %s", job.source.name, plugin.manifest.name)
        return plugin.run(job)