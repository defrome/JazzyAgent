from __future__ import annotations

import json
from pathlib import Path


def read_package_json(path: Path) -> dict:
    package_json = path / "package.json"
    if not package_json.exists():
        return {}
    try:
        return json.loads(package_json.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def package_dependencies(package: dict) -> set[str]:
    names: set[str] = set()
    for key in ("dependencies", "devDependencies", "peerDependencies"):
        values = package.get(key) or {}
        if isinstance(values, dict):
            names.update(values)
    return names


def detect_node_framework(path: Path) -> str | None:
    package = read_package_json(path)
    deps = package_dependencies(package)
    if "next" in deps or (path / "next.config.js").exists() or (path / "next.config.mjs").exists():
        return "next"
    if "nuxt" in deps or (path / "nuxt.config.ts").exists() or (path / "nuxt.config.js").exists():
        return "nuxt"
    if "vue" in deps:
        return "vue"
    if "react" in deps:
        return "react"
    if "svelte" in deps:
        return "svelte"
    if "astro" in deps or (path / "astro.config.mjs").exists():
        return "astro"
    if "vite" in deps or (path / "vite.config.ts").exists() or (path / "vite.config.js").exists():
        return "vite"
    if "express" in deps:
        return "express"
    if "@nestjs/core" in deps:
        return "nestjs"
    return "node"


def detect_python_framework(path: Path) -> str | None:
    text = ""
    for filename in ("pyproject.toml", "requirements.txt"):
        file = path / filename
        if file.exists():
            text += file.read_text(encoding="utf-8", errors="ignore").lower()
    if (path / "manage.py").exists() or "django" in text:
        return "django"
    if "fastapi" in text:
        return "fastapi"
    if "flask" in text:
        return "flask"
    return "python"

