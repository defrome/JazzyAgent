from __future__ import annotations

import json
from pathlib import Path

from jazzy.detectors.project import detect_project


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data), encoding="utf-8")


def test_detects_vue_frontend_and_fastapi_backend(tmp_path: Path) -> None:
    frontend = tmp_path / "frontend"
    backend = tmp_path / "backend"
    frontend.mkdir()
    backend.mkdir()
    write_json(
        frontend / "package.json",
        {"dependencies": {"vue": "^3.0.0"}, "scripts": {"build": "vite build"}},
    )
    (frontend / "pnpm-lock.yaml").write_text("", encoding="utf-8")
    (backend / "pyproject.toml").write_text(
        '[project]\ndependencies = ["fastapi"]\n',
        encoding="utf-8",
    )

    project = detect_project(tmp_path)

    assert len(project.frontend_parts) == 1
    assert project.frontend_parts[0].framework == "vue"
    assert project.frontend_parts[0].package_manager == "pnpm"
    assert len(project.backend_parts) == 1
    assert project.backend_parts[0].framework == "fastapi"


def test_detects_express_as_backend(tmp_path: Path) -> None:
    write_json(tmp_path / "package.json", {"dependencies": {"express": "^4.0.0"}})

    project = detect_project(tmp_path)

    assert len(project.backend_parts) == 1
    assert project.backend_parts[0].framework == "express"
