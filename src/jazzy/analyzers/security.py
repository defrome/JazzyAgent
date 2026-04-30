from __future__ import annotations

from pathlib import Path

from jazzy.analyzers.backend import analyze_backend


def analyze_security(root: Path):
    return analyze_backend(root)

