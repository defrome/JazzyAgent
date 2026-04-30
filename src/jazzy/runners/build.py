from __future__ import annotations

from pathlib import Path

from jazzy.detectors.commands import CommandSpec
from jazzy.reports.final_report import CheckResult
from jazzy.runners.checks import run_checks


def run_builds(
    commands: list[CommandSpec],
    root: Path,
    allow_exec: bool = False,
) -> list[CheckResult]:
    build_commands = [command for command in commands if command.kind == "build"]
    return run_checks(build_commands, root=root, allow_exec=allow_exec)
