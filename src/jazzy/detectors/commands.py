from __future__ import annotations

from pathlib import Path

from jazzy.detectors.languages import read_package_json
from jazzy.detectors.package_manager import run_script_command
from jazzy.detectors.project import ProjectInfo, ProjectPart


def detect_commands(project: ProjectInfo, mode: str = "auto") -> list[tuple[Path, str]]:
    commands: list[tuple[Path, str]] = []
    for part in project.parts:
        if mode == "frontend" and part.kind != "frontend":
            continue
        if mode == "backend" and part.kind != "backend":
            continue
        commands.extend(_commands_for_part(part))
    return commands


def _commands_for_part(part: ProjectPart) -> list[tuple[Path, str]]:
    if part.language == "javascript/typescript":
        return _node_commands(part)
    if part.language == "python":
        return _python_commands(part)
    return []


def _node_commands(part: ProjectPart) -> list[tuple[Path, str]]:
    package = read_package_json(part.path)
    scripts = package.get("scripts") or {}
    if not isinstance(scripts, dict):
        return []
    manager = part.package_manager or "npm"
    preferred = ("type-check", "typecheck", "lint", "test", "build")
    return [(part.path, run_script_command(manager, script)) for script in preferred if script in scripts]


def _python_commands(part: ProjectPart) -> list[tuple[Path, str]]:
    path = part.path
    commands: list[str] = []
    if (path / "manage.py").exists():
        commands.append("python manage.py test")
    elif _has_tests(path):
        commands.append("pytest")
    if (path / "pyproject.toml").exists():
        text = (path / "pyproject.toml").read_text(encoding="utf-8", errors="ignore")
        if "ruff" in text:
            commands.append("ruff check .")
        if "mypy" in text:
            commands.append("mypy .")
    return [(path, command) for command in commands]


def _has_tests(path: Path) -> bool:
    return any((path / name).exists() for name in ("tests", "test", "pytest.ini"))

