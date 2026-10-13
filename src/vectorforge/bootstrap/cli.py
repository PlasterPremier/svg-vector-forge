"""CLI entry point. `vecforge <input> --out <dir> --plugin vtrace`."""
from __future__ import annotations

import logging
from pathlib import Path

import typer

from vectorforge.core.host import VectorForgeHost
from vectorforge.models.job import JobRequest

app = typer.Typer(add_completion=False, help="svg-vector-forge CLI")


@app.command()
def main(
    source: Path = typer.Argument(..., exists=True, readable=True),
    out: Path = typer.Option(Path("out"), "--out", "-o"),
    plugin: str = typer.Option("vtrace", "--plugin", "-p"),
    verbose: bool = typer.Option(False, "--verbose", "-v"),
) -> None:
    logging.basicConfig(level=logging.DEBUG if verbose else logging.INFO)
    host = VectorForgeHost.autoload()
    job = JobRequest(source=source, output_dir=out, plugin=plugin)
    result = host.run(job)
    typer.echo(str(result.output_path))


if __name__ == "__main__":
    app()