from __future__ import annotations

from pathlib import Path

from jazzy.agent.context import build_review_context
from jazzy.agent.models import AgentRequest
from jazzy.agent.providers import build_provider
from jazzy.analyzers.backend import analyze_backend
from jazzy.analyzers.frontend import analyze_frontend
from jazzy.analyzers.python import analyze_python
from jazzy.config import JazzyConfig
from jazzy.detectors.commands import CommandSpec, detect_commands
from jazzy.detectors.project import detect_project
from jazzy.reports.final_report import CheckResult, FinalReport
from jazzy.reports.findings import Finding, Severity
from jazzy.runners.checks import run_checks
from jazzy.safety.git_safety import git_status


def run_agent(root: Path, request: AgentRequest, config: JazzyConfig) -> FinalReport:
    project = detect_project(root)
    report = FinalReport(mode=request.mode, prompt=request.prompt)
    report.residual_risk.append(project.summary())

    if config.safety.require_git_clean:
        status = git_status(root)
        if status and status != "not a git repository":
            report.findings.append(
                Finding(
                    severity=Severity.CRITICAL,
                    title="Git worktree не чистый, а safety.require_git_clean включен",
                    detail=status,
                )
            )
            return report

    report.findings.extend(_scan(root, request.mode))
    commands = detect_commands(project, mode=_command_mode(request.mode))
    if request.mode == "doctor":
        commands = _doctor_commands(commands)

    llm_review, llm_risk = _llm_review(root, request, config, project.summary(), commands)
    report.llm_review = llm_review
    report.residual_risk.extend(llm_risk)

    if _can_run_checks(request):
        report.checks.extend(run_checks(commands, root=root, allow_exec=request.allow_exec))
    elif commands:
        report.checks.extend(_skipped_checks(commands, request.mode))

    failed = [check for check in report.checks if not check.passed and not check.skipped]
    for check in failed:
        report.findings.append(
            Finding(
                severity=Severity.CRITICAL,
                title=f"Проверка завершилась ошибкой: {check.command}",
                detail=check.output[-1000:],
            )
        )

    if request.fix and failed:
        report.residual_risk.append(
            "Fix-режим нашел упавшие проверки, но автономное исправление пока требует "
            "безопасный patch-план. Инструменты unified diff уже есть; следующий шаг - "
            "автоматическая итерация patch -> verify."
        )
    return report


def _scan(root: Path, mode: str) -> list[Finding]:
    if mode == "frontend" or mode == "mobile":
        return analyze_frontend(root)
    if mode == "backend":
        return analyze_backend(root) + analyze_python(root)
    if mode == "security":
        return analyze_backend(root)
    return analyze_frontend(root) + analyze_backend(root) + analyze_python(root)


def _command_mode(mode: str) -> str:
    if mode in {"frontend", "mobile"}:
        return "frontend"
    if mode in {"backend", "security"}:
        return "backend"
    return "auto"


def _doctor_commands(commands: list[CommandSpec]) -> list[CommandSpec]:
    priority = ("type", "lint", "test", "build")
    return sorted(
        commands,
        key=lambda item: next(
            (index for index, marker in enumerate(priority) if marker in item.display),
            len(priority),
        ),
    )


def _can_run_checks(request: AgentRequest) -> bool:
    if request.mode == "review":
        return False
    return request.allow_exec


def _skipped_checks(commands: list[CommandSpec], mode: str) -> list[CheckResult]:
    reason = (
        "Review-режим только читает код."
        if mode == "review"
        else "Запуск команд заблокирован. Повторите с --allow-exec, чтобы выполнить проверки."
    )
    return [
        CheckResult(command=command.display, passed=False, output=reason, skipped=True)
        for command in commands
    ]


def _llm_review(
    root: Path,
    request: AgentRequest,
    config: JazzyConfig,
    project_summary: str,
    commands: list[CommandSpec],
) -> tuple[str | None, list[str]]:
    provider = build_provider(
        config.agent.provider,
        config.agent.model,
        host=config.agent.ollama_host,
        timeout=config.agent.ollama_timeout,
    )
    if provider.name == "noop":
        return None, ["LLM-провайдер отключен."]

    context = "\n".join(
        [
            f"Root: {root}",
            f"Mode: {request.mode}",
            f"Project: {project_summary}",
            "",
            "Найденные команды:",
            *[f"- {command.display} в {command.cwd}" for command in commands[:20]],
            "",
            build_review_context(root),
        ]
    )
    try:
        response = provider.review(request.prompt or "Проверь этот проект.", context)
    except RuntimeError as exc:
        return None, [str(exc)]
    if not response:
        return None, [f"{provider.name} вернул пустой анализ."]
    return response[:6000], []
