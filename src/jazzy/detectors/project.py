from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from jazzy.detectors.languages import detect_node_framework, detect_python_framework
from jazzy.detectors.package_manager import detect_package_manager


@dataclass(frozen=True)
class ProjectPart:
    kind: str
    path: Path
    language: str
    framework: str | None = None
    package_manager: str | None = None


@dataclass(frozen=True)
class ProjectInfo:
    root: Path
    parts: list[ProjectPart] = field(default_factory=list)

    @property
    def frontend_parts(self) -> list[ProjectPart]:
        return [part for part in self.parts if part.kind == "frontend"]

    @property
    def backend_parts(self) -> list[ProjectPart]:
        return [part for part in self.parts if part.kind == "backend"]

    def summary(self) -> str:
        if not self.parts:
            return "Поддерживаемые части проекта не обнаружены."
        chunks = []
        for part in self.parts:
            rel = part.path.relative_to(self.root) if part.path != self.root else Path(".")
            kind = "frontend" if part.kind == "frontend" else "backend"
            label = f"{kind}: {part.language}"
            if part.framework:
                label += f"/{part.framework}"
            label += f" в {rel}"
            if part.package_manager:
                label += f" ({part.package_manager})"
            chunks.append(label)
        return "; ".join(chunks)


FRONTEND_DIR_HINTS = ("frontend", "client", "web", "apps/web", "packages/web")
BACKEND_DIR_HINTS = ("backend", "server", "api", "apps/api", "packages/api")


def detect_project(root: Path) -> ProjectInfo:
    root = root.resolve()
    candidates = [root]
    for hint in FRONTEND_DIR_HINTS + BACKEND_DIR_HINTS:
        path = root / hint
        if path.exists() and path.is_dir():
            candidates.append(path)

    parts: list[ProjectPart] = []
    seen: set[tuple[str, Path]] = set()
    for path in candidates:
        if (path / "package.json").exists():
            framework = detect_node_framework(path)
            kind = _classify_node_part(path, framework)
            part = ProjectPart(
                kind=kind,
                path=path,
                language="javascript/typescript",
                framework=framework,
                package_manager=detect_package_manager(path),
            )
            key = (part.kind, part.path)
            if key not in seen:
                parts.append(part)
                seen.add(key)

        if _has_python_markers(path):
            framework = detect_python_framework(path)
            part = ProjectPart(kind="backend", path=path, language="python", framework=framework)
            key = (part.kind, part.path)
            if key not in seen:
                parts.append(part)
                seen.add(key)

    return ProjectInfo(root=root, parts=parts)


def _classify_node_part(path: Path, framework: str | None) -> str:
    lower = str(path).lower()
    if framework in {"express", "nestjs"}:
        return "backend"
    if any(token in lower for token in ("backend", "server", "api")):
        return "backend"
    return "frontend"


def _has_python_markers(path: Path) -> bool:
    if any(
        (path / marker).exists()
        for marker in ("pyproject.toml", "requirements.txt", "manage.py", "setup.py")
    ):
        return True
    return any(file.is_file() and file.suffix == ".py" for file in path.glob("*.py"))
