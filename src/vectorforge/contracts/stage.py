"""Stage protocol for composable pipeline steps inside a plugin."""
from __future__ import annotations

from typing import Protocol, runtime_checkable

import numpy as np


@runtime_checkable
class Stage(Protocol):
    name: str

    def __call__(self, image: np.ndarray) -> np.ndarray: ...