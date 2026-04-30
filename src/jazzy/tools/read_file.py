from __future__ import annotations

from pathlib import Path


def read_file(path: Path, limit: int = 12000) -> str:
    text = path.read_text(encoding="utf-8", errors="ignore")
    return text[:limit]

