from __future__ import annotations

import subprocess
from pathlib import Path

from jazzy.tools.apply_patch import apply_unified_patch


def test_apply_unified_patch(tmp_path: Path) -> None:
    subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True)
    target = tmp_path / "hello.txt"
    target.write_text("hello\n", encoding="utf-8")
    patch = """diff --git a/hello.txt b/hello.txt
--- a/hello.txt
+++ b/hello.txt
@@ -1 +1 @@
-hello
+hello jazzy
"""

    apply_unified_patch(tmp_path, patch)

    assert target.read_text(encoding="utf-8") == "hello jazzy\n"

