"""diffvg plugin — differentiable-rendering refinement of an existing SVG."""
from __future__ import annotations

import logging
import time
from pathlib import Path

from vectorforge.contracts.plugin import VectorForgePlugin
from vectorforge.models.job import JobRequest, JobResult
from vectorforge.models.plugin_manifest import PluginManifest

log = logging.getLogger(__name__)


class DiffVGPlugin(VectorForgePlugin):
    manifest = PluginManifest(
        name="diffvg",
        version="0.9.4",
        author="svg-vector-forge maintainers",
        capabilities=["path.refine"],
        requires=["vtrace"],
    )

    def run(self, job: JobRequest) -> JobResult:
        started = time.perf_counter()
        out_path = Path(job.output_dir) / f"{job.source.stem}.refined.svg"
        out_path.parent.mkdir(parents=True, exist_ok=True)

        # diffvg is optional; if the wheel isn't installed we pass the input through.
        try:
            import diffvg  # type: ignore[import-not-found]  # noqa: F401
        except ImportError:
            log.warning("diffvg not installed; emitting passthrough copy")
            out_path.write_bytes(job.source.read_bytes())
            return JobResult(
                output_path=out_path,
                path_count=0,
                duration_ms=int((time.perf_counter() - started) * 1000),
                plugin_name=self.manifest.name,
            )

        raise NotImplementedError("diffvg refinement loop is WIP — see issue #142")