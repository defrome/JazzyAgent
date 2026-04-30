from __future__ import annotations

from pathlib import Path

from jazzy.agent.models import AgentRequest
from jazzy.analyzers.backend import analyze_backend
from jazzy.analyzers.frontend import analyze_frontend
from jazzy.analyzers.python import analyze_python
from jazzy.config import JazzyConfig
from jazzy.detectors.commands import detect_commands
from jazzy.detectors.project import detect_project
from jazzy.reports.final_report import FinalReport
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
                    title="Git worktree is not clean and safety.require_git_clean is enabled",
                    detail=status,
                )
            )
            return report

    report.findings.extend(_scan(root, request.mode))
    commands = detect_commands(project, mode=_command_mode(request.mode))
    if request.mode == "doctor":
        commands = _doctor_commands(commands)
    report.checks.extend(
        run_checks(commands, allow_destructive=config.safety.allow_destructive_commands)
    )

    failed = [check for check in report.checks if not check.passed]
    for check in failed:
        report.findings.append(
            Finding(
                severity=Severity.CRITICAL,
                title=f"Check failed: {check.command}",
                detail=check.output[-1000:],
            )
        )

    if request.fix and failed:
        report.residual_risk.append(
            "MVP detected failing checks but did not apply autonomous code patches yet. "
            "Patch tools and OpenAI loop extension points are present for the next iteration."
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


def _doctor_commands(commands: list[tuple[Path, str]]) -> list[tuple[Path, str]]:
    priority = ("type", "lint", "test", "build")
    return sorted(
        commands,
        key=lambda item: next(
            (index for index, marker in enumerate(priority) if marker in item[1]),
            len(priority),
        ),
    )

