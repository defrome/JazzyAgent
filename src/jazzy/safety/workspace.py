from __future__ import annotations

from pathlib import Path


def assert_inside_root(root: Path, path: Path) -> Path:
    safe_root = root.resolve()
    resolved = path.resolve()
    if resolved != safe_root and safe_root not in resolved.parents:
        raise PermissionError(f"Путь выходит за пределы workspace: {resolved}")
    return resolved


def resolve_workspace_path(root: Path, path: Path | str) -> Path:
    candidate = Path(path)
    if not candidate.is_absolute():
        candidate = root / candidate
    return assert_inside_root(root, candidate)
