from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

from jazzy.detectors.languages import read_package_json
from jazzy.detectors.package_manager import run_script_argv
from jazzy.detectors.project import ProjectInfo, ProjectPart


@dataclass(frozen=True)
class CommandSpec:
    cwd: Path
    argv: list[str]
    kind: str
    risky: bool = True

    @property
    def display(self) -> str:
        return " ".join(self.argv)


def detect_commands(project: ProjectInfo, mode: str = "auto") -> list[CommandSpec]:
    commands: list[CommandSpec] = []
    for part in project.parts:
        if mode == "frontend" and part.kind != "frontend":
            continue
        if mode == "backend" and part.kind != "backend":
            continue
        commands.extend(_commands_for_part(part))
    return commands


def _commands_for_part(part: ProjectPart) -> list[CommandSpec]:
    if part.language == "javascript/typescript":
        return _node_commands(part)
    if part.language == "python":
        return _python_commands(part)
    return []


def _node_commands(part: ProjectPart) -> list[CommandSpec]:
    package = read_package_json(part.path)
    scripts = package.get("scripts") or {}
    if not isinstance(scripts, dict):
        return []
    manager = part.package_manager or "npm"
    preferred = ("type-check", "typecheck", "lint", "test", "build")
    return [
        CommandSpec(
            cwd=part.path,
            argv=run_script_argv(manager, script),
            kind=script,
            risky=True,
        )
        for script in preferred
        if script in scripts
    ]


def _python_commands(part: ProjectPart) -> list[CommandSpec]:
    path = part.path
    python = sys.executable
    commands: list[CommandSpec] = []
    if (path / "manage.py").exists():
        commands.append(CommandSpec(path, [python, "manage.py", "test"], "test"))
    elif _has_tests(path):
        commands.append(CommandSpec(path, [python, "-m", "pytest"], "test"))
    if (path / "pyproject.toml").exists():
        text = (path / "pyproject.toml").read_text(encoding="utf-8", errors="ignore")
        if "ruff" in text:
            commands.append(CommandSpec(path, [python, "-m", "ruff", "check", "."], "lint"))
        if "mypy" in text:
            commands.append(CommandSpec(path, [python, "-m", "mypy", "."], "typecheck"))
    return commands


def _has_tests(path: Path) -> bool:
    return any((path / name).exists() for name in ("tests", "test", "pytest.ini"))
