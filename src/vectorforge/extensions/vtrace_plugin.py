"""vtrace plugin — raster -> SVG via vtracer."""
from __future__ import annotations

import time
from pathlib import Path

from vectorforge.contracts.plugin import VectorForgePlugin
from vectorforge.handlers.preprocess import flatten_alpha, quantize_palette, to_array
from vectorforge.handlers.trace import trace_to_svg
from vectorforge.models.job import JobRequest, JobResult
from vectorforge.models.plugin_manifest import PluginManifest
from vectorforge.utils.paths import unique_stem
from vectorforge.utils.svg_writer import write as svg_write
from PIL import Image


class VTracePlugin(VectorForgePlugin):
    manifest = PluginManifest(
        name="vtrace",
        version="0.9.4",
        author="svg-vector-forge maintainers",
        capabilities=["raster.trace", "path.optimize"],
        requires=[],
    )

    def run(self, job: JobRequest) -> JobResult:
        started = time.perf_counter()
        img = Image.open(job.source)
        img = flatten_alpha(img)
        img = quantize_palette(img, job.palette_size)
        rgba = to_array(img)

        out_path = unique_stem(job.source, Path(job.output_dir))
        tmp_path = out_path.with_suffix(".svg.tmp")
        path_count = trace_to_svg(rgba, tmp_path)

        svg_text = tmp_path.read_text(encoding="utf-8")
        svg_write(svg_text, out_path)
        tmp_path.unlink(missing_ok=True)

        return JobResult(
            output_path=out_path,
            path_count=path_count,
            duration_ms=int((time.perf_counter() - started) * 1000),
            plugin_name=self.manifest.name,
        )