from __future__ import annotations

import json
from pathlib import Path

from jazzy.detectors.commands import detect_commands
from jazzy.detectors.project import detect_project


def test_detects_node_scripts_in_preferred_order(tmp_path: Path) -> None:
    (tmp_path / "package.json").write_text(
        json.dumps(
            {
                "dependencies": {"react": "^18.0.0"},
                "scripts": {
                    "build": "vite build",
                    "lint": "eslint .",
                    "type-check": "tsc --noEmit",
                },
            }
        ),
        encoding="utf-8",
    )

    commands = [command for _, command in detect_commands(detect_project(tmp_path))]

    assert commands == ["npm run type-check", "npm run lint", "npm run build"]


def test_detects_python_test_and_quality_commands(tmp_path: Path) -> None:
    (tmp_path / "tests").mkdir()
    (tmp_path / "pyproject.toml").write_text("[tool.ruff]\n[tool.mypy]\n", encoding="utf-8")

    commands = [command for _, command in detect_commands(detect_project(tmp_path))]

    assert commands == ["pytest", "ruff check .", "mypy ."]

