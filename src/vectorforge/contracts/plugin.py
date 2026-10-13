"""The one contract every svg-vector-forge plugin must satisfy."""
from __future__ import annotations

from abc import ABC, abstractmethod

from vectorforge.models.job import JobRequest, JobResult
from vectorforge.models.plugin_manifest import PluginManifest


class VectorForgePlugin(ABC):
    """Base class for all vectorization backends.

    Lifecycle: ``__init__`` -> ``setup`` -> ``run`` (0..n) -> ``teardown``.
    ``setup`` may acquire GPU memory; ``teardown`` must release it.
    """

    manifest: PluginManifest

    def setup(self) -> None:
        """Allocate resources. Must be idempotent."""

    @abstractmethod
    def run(self, job: JobRequest) -> JobResult:
        """Consume a job, produce an SVG on disk, return the result."""

    def teardown(self) -> None:
        """Release resources. Called by the host on shutdown."""