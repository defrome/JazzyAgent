from __future__ import annotations

from pathlib import Path

from jazzy.detectors.commands import CommandSpec
from jazzy.reports.final_report import CheckResult
from jazzy.runners.checks import run_checks


def run_tests(
    commands: list[CommandSpec],
    root: Path,
    allow_exec: bool = False,
) -> list[CheckResult]:
    test_commands = [
        command
        for command in commands
        if command.kind == "test" or "pytest" in command.argv
    ]
    return run_checks(test_commands, root=root, allow_exec=allow_exec)
