from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path

from jazzy.safety.workspace import assert_inside_root

ALLOWED_EXECUTABLES = {
    "python",
    "python3",
    "pytest",
    "ruff",
    "mypy",
    "npm",
    "pnpm",
    "yarn",
    "bun",
}


@dataclass(frozen=True)
class ShellResult:
    argv: list[str]
    returncode: int
    stdout: str
    stderr: str

    @property
    def command(self) -> str:
        return " ".join(self.argv)

    @property
    def passed(self) -> bool:
        return self.returncode == 0

    def combined_output(self, limit: int = 6000) -> str:
        text = "\n".join(part for part in (self.stdout, self.stderr) if part)
        return text[-limit:]


def run_command(
    argv: list[str],
    *,
    root: Path,
    cwd: Path,
    timeout: int = 120,
    allow_exec: bool = False,
) -> ShellResult:
    if not argv:
        raise ValueError("Empty command is not allowed.")
    if not allow_exec:
        raise PermissionError("Command execution requires explicit allow_exec=True.")

    executable = Path(argv[0]).name
    if executable not in ALLOWED_EXECUTABLES:
        raise PermissionError(f"Executable is not allowlisted: {executable}")

    safe_cwd = assert_inside_root(root, cwd)
    result = subprocess.run(
        argv,
        cwd=safe_cwd,
        shell=False,
        text=True,
        capture_output=True,
        timeout=timeout,
        check=False,
    )
    return ShellResult(
        argv=argv,
        returncode=result.returncode,
        stdout=result.stdout,
        stderr=result.stderr,
    )
