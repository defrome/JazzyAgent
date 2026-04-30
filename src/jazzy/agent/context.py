from __future__ import annotations

from pathlib import Path

from jazzy.tools.search import list_files

TEXT_EXTENSIONS = {
    ".py",
    ".toml",
    ".txt",
    ".md",
    ".json",
    ".yaml",
    ".yml",
    ".js",
    ".ts",
    ".tsx",
    ".jsx",
    ".css",
    ".scss",
}

IMPORTANT_NAMES = {
    ".env.example",
    "Dockerfile",
    "README.md",
    "api.py",
    "app.py",
    "docker-compose.yml",
    "main.py",
    "models.py",
    "package.json",
    "pyproject.toml",
    "requirements.txt",
    "routes.py",
    "server.py",
    "views.py",
}


def build_review_context(root: Path, max_chars: int = 30_000) -> str:
    files = list_files(root)
    relevant = [path for path in files if _is_relevant(path)]
    rel_files = [path.relative_to(root).as_posix() for path in relevant]
    selected = _select_context_files(root, relevant)

    chunks = [
        "Файлы проекта:",
        *[f"- {name}" for name in rel_files[:150]],
        "",
        "Содержимое ключевых файлов:",
    ]
    used = len("\n".join(chunks))

    for path in selected:
        rel = path.relative_to(root).as_posix()
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue

        block = f"\n--- FILE: {rel} ---\n{text[:8000]}\n"
        if used + len(block) > max_chars:
            break
        chunks.append(block)
        used += len(block)

    return "\n".join(chunks)


def _select_context_files(root: Path, files: list[Path]) -> list[Path]:
    def priority(path: Path) -> tuple[int, str]:
        rel = path.relative_to(root).as_posix()
        if path.name in IMPORTANT_NAMES:
            return (0, rel)
        if path.suffix == ".py":
            return (1, rel)
        if path.name == "package.json":
            return (2, rel)
        return (3, rel)

    return sorted(files, key=priority)[:20]


def _is_relevant(path: Path) -> bool:
    return path.suffix in TEXT_EXTENSIONS or path.name in IMPORTANT_NAMES
