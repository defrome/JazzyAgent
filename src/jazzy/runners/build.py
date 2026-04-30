from __future__ import annotations

from pathlib import Path

from jazzy.reports.final_report import CheckResult
from jazzy.runners.checks import run_checks


def run_builds(commands: list[tuple[Path, str]]) -> list[CheckResult]:
    build_commands = [(path, command) for path, command in commands if "build" in command]
    return run_checks(build_commands)

