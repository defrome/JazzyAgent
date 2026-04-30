from __future__ import annotations

import subprocess
from pathlib import Path


class PatchError(RuntimeError):
    pass


def apply_unified_patch(root: Path, patch_text: str) -> None:
    result = subprocess.run(
        ["git", "apply", "--whitespace=fix", "-"],
        cwd=root,
        input=patch_text,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise PatchError(result.stderr.strip() or "git apply failed")

