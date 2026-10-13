# svg-vector-forge — Architecture

`svg-vector-forge` is a Windows-first desktop tool for turning raster images
and text prompts into clean, editable SVG. It is built as a **plugin host**:
the core ships the pipeline, the registry, and the contracts; every actual
vectorization backend (tracing, differentiable rendering, prompt-to-SVG
diffusion) lives in an extension module loaded at runtime.

## Layers

- `vectorforge/bootstrap/` — entry points (CLI, desktop GUI, plugin autoload)
- `vectorforge/core/` — pipeline orchestration, host, registry, loader
- `vectorforge/contracts/` — plugin ABCs, dataclasses, schemas
- `vectorforge/handlers/` — per-stage handlers (preprocess, trace, optimize, export)
- `vectorforge/services/` — long-lived services (model cache, telemetry-free logging, file watcher)
- `vectorforge/models/` — Pydantic models for jobs, configs, plugin manifests
- `vectorforge/utils/` — color math, path math, SVG writer, unit conversion
- `vectorforge/config/` — default TOML configs and plugin search paths
- `vectorforge/extensions/` — first-party plugins (vtrace, diffvg, prompt2svg)

## Plugin lifecycle

1. Host scans `vectorforge/config/plugins.toml` and the `vectorforge.plugins`
   entry-point group.
2. `PluginLoader` imports each module, validates the manifest against
   `PluginManifest`, and registers the instance with `PluginRegistry`.
3. `Pipeline` resolves stages by capability tag (`raster.trace`,
   `prompt.diffvg`, `path.optimize`) and dispatches jobs.
4. Extensions may declare dependencies on other extensions; the loader
   topologically sorts before registration.

## Threading

The GUI runs the pipeline on a `QThreadPool`. Extensions that touch the GPU
must acquire `vectorforge.services.model_cache.ModelCache` under its
`asyncio.Lock` — the cache is the single owner of loaded weights.