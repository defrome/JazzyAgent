from __future__ import annotations

from pathlib import Path

import pathspec

DEFAULT_PATTERNS = [
    ".git/",
    ".venv/",
    "venv/",
    "node_modules/",
    "dist/",
    "build/",
    "__pycache__/",
    "*.pyc",
]


def load_ignore_spec(root: Path) -> pathspec.PathSpec:
    patterns = list(DEFAULT_PATTERNS)
    gitignore = root / ".gitignore"
    if gitignore.exists():
        patterns.extend(gitignore.read_text(encoding="utf-8", errors="ignore").splitlines())
    return pathspec.PathSpec.from_lines("gitwildmatch", patterns)

