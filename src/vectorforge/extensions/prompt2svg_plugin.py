"""prompt2svg plugin — text prompt -> SVG via an ONNX diffusion model."""
from __future__ import annotations

import logging
import time
from pathlib import Path

from vectorforge.contracts.plugin import VectorForgePlugin
from vectorforge.models.job import JobRequest, JobResult
from vectorforge.models.plugin_manifest import PluginManifest

log = logging.getLogger(__name__)


class Prompt2SVGPlugin(VectorForgePlugin):
    manifest = PluginManifest(
        name="prompt2svg",
        version="0.9.4",
        author="svg-vector-forge maintainers",
        capabilities=["prompt.diffusion"],
        requires=["vtrace"],
    )

    def run(self, job: JobRequest) -> JobResult:
        started = time.perf_counter()
        prompt = job.source.read_text(encoding="utf-8").strip()
        if not prompt:
            raise ValueError("prompt file is empty")

        out_path = Path(job.output_dir) / "prompt.svg"
        out_path.parent.mkdir(parents=True, exist_ok=True)

        # Placeholder: real path runs onnxruntime + a small SD-Turbo -> vtracer
        # round trip. Tracked in issue #88.
        out_path.write_text(
            f'<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512">'
            f'<rect width="512" height="512" fill="#101014"/>'
            f'<text x="16" y="32" fill="#e6e6e6" font-family="monospace" font-size="14">'
            f"prompt: {prompt[:64]}</text></svg>",
            encoding="utf-8",
        )
        return JobResult(
            output_path=out_path,
            path_count=1,
            duration_ms=int((time.perf_counter() - started) * 1000),
            plugin_name=self.manifest.name,
        )