#!/usr/bin/env python3
"""Refresh Markdown table-of-contents blocks (--toc-only wrapper)."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

_CONFIG_ROOT = Path(__file__).resolve().parents[3]
_LIB = _CONFIG_ROOT / "scripts" / "update_markdown_docs.py"


def _load():
    spec = importlib.util.spec_from_file_location("update_markdown_docs", _LIB)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {_LIB}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    mod = _load()
    argv = ["--toc-only", *sys.argv[1:]]
    return mod.main(argv)


if __name__ == "__main__":
    raise SystemExit(main())
