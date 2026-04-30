from __future__ import annotations

import sys
from pathlib import Path
from typing import Annotated

import typer
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

from jazzy import __version__
from jazzy.agent.loop import run_agent
from jazzy.agent.models import AgentRequest
from jazzy.config import load_config

console = Console()
app = typer.Typer(
    name="jazzy",
    help="Jazzy - review, fix, verify.",
    no_args_is_help=False,
)


PathOption = Annotated[Path, typer.Option("--path", "-p", help="Project path.")]
FixOption = Annotated[bool, typer.Option("--fix/--no-fix", help="Allow fixes when available.")]
ExecOption = Annotated[
    bool,
    typer.Option("--allow-exec", help="Allow Jazzy to execute detected project commands."),
]
PromptArg = Annotated[str | None, typer.Argument(help="Task prompt.")]


KNOWN_COMMANDS = {
    "review",
    "fix",
    "frontend",
    "backend",
    "fullstack",
    "doctor",
    "mobile",
    "security",
}


@app.callback()
def main(
    version: Annotated[
        bool,
        typer.Option("--version", help="Show Jazzy version.", is_eager=True),
    ] = False,
) -> None:
    """Jazzy - автономный CLI-агент ревью и исправлений."""
    if version:
        console.print(f"jazzy {__version__}")
        raise typer.Exit()


@app.command()
def review(
    prompt: PromptArg = None,
    path: PathOption = Path("."),
    fix: FixOption = False,
    allow_exec: ExecOption = False,
) -> None:
    """Проверить проект без изменений файлов."""
    _run(path=path, mode="review", prompt=prompt, fix=fix, allow_exec=allow_exec)


@app.command()
def fix(
    prompt: PromptArg = None,
    path: PathOption = Path("."),
    allow_exec: ExecOption = False,
) -> None:
    """Проверить и исправить проект."""
    _run(path=path, mode="fix", prompt=prompt, fix=True, allow_exec=allow_exec)


@app.command()
def frontend(
    prompt: PromptArg = None,
    path: PathOption = Path("."),
    fix: FixOption = True,
    allow_exec: ExecOption = False,
) -> None:
    """Проверить frontend-код, layout, routing, images, accessibility и build."""
    _run(path=path, mode="frontend", prompt=prompt, fix=fix, allow_exec=allow_exec)


@app.command()
def backend(
    prompt: PromptArg = None,
    path: PathOption = Path("."),
    fix: FixOption = True,
    allow_exec: ExecOption = False,
) -> None:
    """Проверить backend routes, validation, tests, logging и safety-sensitive код."""
    _run(path=path, mode="backend", prompt=prompt, fix=fix, allow_exec=allow_exec)


@app.command()
def fullstack(
    prompt: PromptArg = None,
    path: PathOption = Path("."),
    fix: FixOption = True,
    allow_exec: ExecOption = False,
) -> None:
    """Проверить frontend и backend вместе."""
    _run(path=path, mode="fullstack", prompt=prompt, fix=fix, allow_exec=allow_exec)


@app.command()
def doctor(
    prompt: PromptArg = "Проект не собирается. Найди команды, запусти проверки и покажи blockers.",
    path: PathOption = Path("."),
    fix: FixOption = True,
    allow_exec: ExecOption = False,
) -> None:
    """Диагностировать ошибки build/test."""
    _run(path=path, mode="doctor", prompt=prompt, fix=fix, allow_exec=allow_exec)


@app.command()
def mobile(
    prompt: PromptArg = None,
    path: PathOption = Path("."),
    fix: FixOption = True,
    allow_exec: ExecOption = False,
) -> None:
    """Диагностировать mobile layout проблемы."""
    _run(path=path, mode="mobile", prompt=prompt, fix=fix, allow_exec=allow_exec)


@app.command()
def security(
    prompt: PromptArg = None,
    path: PathOption = Path("."),
    fix: FixOption = False,
    allow_exec: ExecOption = False,
) -> None:
    """Запустить легкое security review."""
    _run(path=path, mode="security", prompt=prompt, fix=fix, allow_exec=allow_exec)


def interactive(path: Path, mode: str, fix: bool) -> None:
    console.print(Panel("Интерактивный режим Jazzy. Напишите 'exit' для выхода.", title="Jazzy"))
    while True:
        prompt = Prompt.ask("Jazzy")
        if prompt.strip().lower() in {"exit", "quit", ":q"}:
            return
        if prompt.strip():
            _run(path=path, mode=mode, prompt=prompt, fix=fix, allow_exec=False)


def _run(path: Path, mode: str, prompt: str | None, fix: bool, allow_exec: bool) -> None:
    root = path.resolve()
    config = load_config(root)
    request = AgentRequest(mode=mode, prompt=prompt, fix=fix, allow_exec=allow_exec)
    console.print(Panel(f"Режим: {mode}\nПуть: {root}", title="Jazzy"))
    report = run_agent(root=root, request=request, config=config)
    console.print(report.markdown())


def main_entry() -> None:
    load_dotenv()
    args = sys.argv[1:]
    if not args:
        interactive(path=Path("."), mode="auto", fix=True)
        return
    first = args[0]
    if first in KNOWN_COMMANDS or first.startswith("-"):
        app(args=args, standalone_mode=True)
        return
    _run(path=Path("."), mode="auto", prompt=" ".join(args), fix=True, allow_exec=False)


if __name__ == "__main__":
    main_entry()
