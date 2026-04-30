from __future__ import annotations

from pathlib import Path

from jazzy.safety.workspace import resolve_workspace_path


def write_file(root: Path, path: Path | str, content: str) -> None:
    safe_path = resolve_workspace_path(root, path)
    safe_path.parent.mkdir(parents=True, exist_ok=True)
    safe_path.write_text(content, encoding="utf-8")
