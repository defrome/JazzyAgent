from __future__ import annotations

from pathlib import Path

from jazzy.safety.workspace import resolve_workspace_path


def read_file(root: Path, path: Path | str, limit: int = 12000) -> str:
    safe_path = resolve_workspace_path(root, path)
    text = safe_path.read_text(encoding="utf-8", errors="ignore")
    return text[:limit]
