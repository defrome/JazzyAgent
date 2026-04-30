from __future__ import annotations

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
    invoke_without_command=True,
    no_args_is_help=False,
)


PathOption = Annotated[Path, typer.Option("--path", "-p", help="Project path.")]
FixOption = Annotated[bool, typer.Option("--fix/--no-fix", help="Allow fixes when available.")]
PromptArg = Annotated[str | None, typer.Argument(help="Task prompt.")] 


@app.callback()
def main(
    ctx: typer.Context,
    prompt: PromptArg = None,
    path: PathOption = Path("."),
    mode: Annotated[str, typer.Option("--mode", "-m", help="Execution mode.")] = "auto",
    fix: FixOption = True,
    version: Annotated[
        bool,
        typer.Option("--version", help="Show Jazzy version.", is_eager=True),
    ] = False,
) -> None:
    """Jazzy - autonomous CLI code review and fix agent."""
    if version:
        console.print(f"jazzy {__version__}")
        raise typer.Exit()
    if ctx.invoked_subcommand:
        return
    load_dotenv()
    if prompt is None:
        interactive(path=path, mode=mode, fix=fix)
        return
    _run(path=path, mode=mode, prompt=prompt, fix=fix)


@app.command()
def review(
    prompt: PromptArg = None,
    path: PathOption = Path("."),
    fix: FixOption = False,
) -> None:
    """Review a project, defaulting to no file changes."""
    _run(path=path, mode="review", prompt=prompt, fix=fix)


@app.command()
def fix(
    prompt: PromptArg = None,
    path: PathOption = Path("."),
) -> None:
    """Review and fix a project."""
    _run(path=path, mode="fix", prompt=prompt, fix=True)


@app.command()
def frontend(
    prompt: PromptArg = None,
    path: PathOption = Path("."),
    fix: FixOption = True,
) -> None:
    """Check frontend code, layout, routing, images, accessibility and builds."""
    _run(path=path, mode="frontend", prompt=prompt, fix=fix)


@app.command()
def backend(
    prompt: PromptArg = None,
    path: PathOption = Path("."),
    fix: FixOption = True,
) -> None:
    """Check backend routes, validation, tests, logging and safety-sensitive code."""
    _run(path=path, mode="backend", prompt=prompt, fix=fix)


@app.command()
def fullstack(
    prompt: PromptArg = None,
    path: PathOption = Path("."),
    fix: FixOption = True,
) -> None:
    """Check frontend and backend together."""
    _run(path=path, mode="fullstack", prompt=prompt, fix=fix)


@app.command()
def doctor(
    prompt: PromptArg = "Project does not build. Detect commands, run checks, and report blockers.",
    path: PathOption = Path("."),
    fix: FixOption = True,
) -> None:
    """Diagnose build and test failures."""
    _run(path=path, mode="doctor", prompt=prompt, fix=fix)


@app.command()
def mobile(
    prompt: PromptArg = None,
    path: PathOption = Path("."),
    fix: FixOption = True,
) -> None:
    """Debug mobile frontend layout issues."""
    _run(path=path, mode="mobile", prompt=prompt, fix=fix)


@app.command()
def security(
    prompt: PromptArg = None,
    path: PathOption = Path("."),
    fix: FixOption = False,
) -> None:
    """Run a light security review."""
    _run(path=path, mode="security", prompt=prompt, fix=fix)


def interactive(path: Path, mode: str, fix: bool) -> None:
    console.print(Panel("Jazzy interactive mode. Type 'exit' to quit.", title="Jazzy"))
    while True:
        prompt = Prompt.ask("Jazzy")
        if prompt.strip().lower() in {"exit", "quit", ":q"}:
            return
        if prompt.strip():
            _run(path=path, mode=mode, prompt=prompt, fix=fix)


def _run(path: Path, mode: str, prompt: str | None, fix: bool) -> None:
    root = path.resolve()
    config = load_config(root)
    request = AgentRequest(mode=mode, prompt=prompt, fix=fix)
    console.print(Panel(f"Mode: {mode}\nPath: {root}", title="Jazzy"))
    report = run_agent(root=root, request=request, config=config)
    console.print(report.markdown())


if __name__ == "__main__":
    app()

