from __future__ import annotations

from pathlib import Path

from jazzy.detectors.commands import CommandSpec
from jazzy.reports.final_report import CheckResult
from jazzy.tools.shell import run_command


def run_checks(
    commands: list[CommandSpec],
    *,
    root: Path,
    allow_exec: bool = False,
) -> list[CheckResult]:
    results: list[CheckResult] = []
    for command in commands:
        try:
            result = run_command(
                command.argv,
                root=root,
                cwd=command.cwd,
                allow_exec=allow_exec,
            )
        except (PermissionError, ValueError) as exc:
            results.append(CheckResult(command=command.display, passed=False, output=str(exc)))
            continue
        results.append(CheckResult(command=command.display, passed=result.passed, output=result.combined_output()))
    return results
