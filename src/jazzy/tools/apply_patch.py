from __future__ import annotations

import subprocess
from pathlib import Path

from jazzy.safety.workspace import assert_inside_root


class PatchError(RuntimeError):
    pass


def apply_unified_patch(root: Path, patch_text: str) -> None:
    safe_root = assert_inside_root(root, root)
    result = subprocess.run(
        ["git", "apply", "--whitespace=fix", "-"],
        cwd=safe_root,
        input=patch_text,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise PatchError(result.stderr.strip() or "git apply failed")
