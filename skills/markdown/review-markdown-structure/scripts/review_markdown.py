#!/usr/bin/env python3
"""Run the shared Markdown reviewer from cursor-config."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

_LIB = Path(__file__).resolve().parents[3] / "scripts" / "review_markdown.py"


def _load():
    spec = importlib.util.spec_from_file_location("review_markdown", _LIB)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {_LIB}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


if __name__ == "__main__":
    raise SystemExit(_load().main())
