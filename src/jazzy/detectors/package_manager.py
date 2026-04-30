from __future__ import annotations

from pathlib import Path


def detect_package_manager(path: Path) -> str | None:
    markers = [
        ("pnpm-lock.yaml", "pnpm"),
        ("yarn.lock", "yarn"),
        ("package-lock.json", "npm"),
        ("bun.lockb", "bun"),
        ("bun.lock", "bun"),
    ]
    for filename, manager in markers:
        if (path / filename).exists():
            return manager
    if (path / "package.json").exists():
        return "npm"
    return None


def run_script_command(manager: str, script: str) -> str:
    if manager == "npm":
        return f"npm run {script}"
    if manager == "pnpm":
        return f"pnpm {script}"
    if manager == "yarn":
        return f"yarn {script}"
    if manager == "bun":
        return f"bun run {script}"
    return f"{manager} run {script}"

