from __future__ import annotations

from pathlib import Path

from jazzy.reports.final_report import CheckResult
from jazzy.tools.shell import run_shell_command


def run_checks(commands: list[tuple[Path, str]], allow_destructive: bool = False) -> list[CheckResult]:
    results: list[CheckResult] = []
    for cwd, command in commands:
        result = run_shell_command(command, cwd=cwd, allow_destructive=allow_destructive)
        results.append(
            CheckResult(
                command=command,
                passed=result.passed,
                output=result.combined_output(),
            )
        )
    return results

