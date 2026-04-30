from __future__ import annotations

from pathlib import Path

from jazzy.reports.final_report import CheckResult
from jazzy.runners.checks import run_checks


def run_tests(commands: list[tuple[Path, str]]) -> list[CheckResult]:
    test_commands = [(path, command) for path, command in commands if "test" in command or "pytest" in command]
    return run_checks(test_commands)

