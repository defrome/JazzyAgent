from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path

from jazzy.safety.permissions import assert_command_allowed


@dataclass(frozen=True)
class ShellResult:
    command: str
    returncode: int
    stdout: str
    stderr: str

    @property
    def passed(self) -> bool:
        return self.returncode == 0

    def combined_output(self, limit: int = 6000) -> str:
        text = "\n".join(part for part in (self.stdout, self.stderr) if part)
        return text[-limit:]


def run_shell_command(
    command: str,
    cwd: Path,
    timeout: int = 120,
    allow_destructive: bool = False,
) -> ShellResult:
    assert_command_allowed(command, allow_destructive=allow_destructive)
    result = subprocess.run(
        command,
        cwd=cwd,
        shell=True,
        text=True,
        capture_output=True,
        timeout=timeout,
        check=False,
    )
    return ShellResult(
        command=command,
        returncode=result.returncode,
        stdout=result.stdout,
        stderr=result.stderr,
    )

