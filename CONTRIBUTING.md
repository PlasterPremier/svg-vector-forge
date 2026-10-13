# Contributing to svg-vector-forge

Thanks for wanting to forge vectors. A few ground rules to keep the plugin
host sane.

## Setup

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev,cpu]"
pytest -q
```

## Adding a plugin

1. Create `vectorforge/extensions/<name>_plugin.py`.
2. Subclass `vectorforge.contracts.plugin.VectorForgePlugin`.
3. Declare `manifest` as a `PluginManifest` with `capabilities` set.
4. Register it in `pyproject.toml` under `[project.entry-points."vectorforge.plugins"]`.
5. Add a fixture image under `tests/fixtures/` and a round-trip test.

Plugins must be side-effect free at import time. Do all I/O in `setup()`.

## Style

- `ruff` and `mypy --strict` must pass.
- No `print()` in `vectorforge/` — use `logging.getLogger(__name__)`.
- Public functions get type hints. Internal helpers may skip them.

## Commit messages

`<scope>: <imperative summary>` — e.g. `vtrace: handle alpha channel edge case`.

## Reporting

Open an issue with the OS build number, Python version, plugin name, and the
exact command or GUI action that reproduced the bug.