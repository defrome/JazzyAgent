from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

from jazzy.safety.ignore import load_ignore_spec


@dataclass(frozen=True)
class SearchMatch:
    path: str
    line: int
    text: str


def list_files(root: Path) -> list[Path]:
    if shutil.which("rg"):
        result = subprocess.run(
            ["rg", "--files", *_rg_exclude_args()],
            cwd=root,
            text=True,
            capture_output=True,
            check=False,
        )
        if result.returncode in (0, 1):
            return [root / line for line in result.stdout.splitlines() if line]

    spec = load_ignore_spec(root)
    files: list[Path] = []
    for path in root.rglob("*"):
        if path.is_file():
            rel = path.relative_to(root).as_posix()
            if not spec.match_file(rel):
                files.append(path)
    return files


def rg_search(root: Path, pattern: str) -> list[SearchMatch]:
    if shutil.which("rg"):
        result = subprocess.run(
            ["rg", "--line-number", "--no-heading", *_rg_exclude_args(), pattern],
            cwd=root,
            text=True,
            capture_output=True,
            check=False,
        )
        return _parse_rg_output(result.stdout)
    return _python_search(root, pattern)


def _parse_rg_output(output: str) -> list[SearchMatch]:
    matches: list[SearchMatch] = []
    for line in output.splitlines():
        path, sep, rest = line.partition(":")
        if not sep:
            continue
        number, sep, text = rest.partition(":")
        if not sep or not number.isdigit():
            continue
        matches.append(SearchMatch(path=path, line=int(number), text=text.strip()))
    return matches


def _rg_exclude_args() -> list[str]:
    ignored = [
        ".git",
        ".venv",
        "venv",
        "node_modules",
        "dist",
        "build",
        "__pycache__",
        ".pytest_cache",
        ".ruff_cache",
    ]
    args: list[str] = []
    for name in ignored:
        args.extend(["--glob", f"!{name}/**"])
    args.extend(["--glob", "!*.pyc"])
    return args


def _python_search(root: Path, pattern: str) -> list[SearchMatch]:
    import re

    regex = re.compile(pattern)
    matches: list[SearchMatch] = []
    for path in list_files(root):
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            continue
        for index, text in enumerate(lines, start=1):
            if regex.search(text):
                matches.append(
                    SearchMatch(
                        path=path.relative_to(root).as_posix(),
                        line=index,
                        text=text.strip(),
                    )
                )
    return matches
