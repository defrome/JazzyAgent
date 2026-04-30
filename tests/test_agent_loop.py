from __future__ import annotations

import json
from pathlib import Path

from jazzy.agent.loop import run_agent
from jazzy.agent.models import AgentRequest
from jazzy.config import JazzyConfig


def test_review_mode_does_not_execute_detected_commands(tmp_path: Path) -> None:
    (tmp_path / "package.json").write_text(
        json.dumps(
            {
                "dependencies": {"react": "^18.0.0"},
                "scripts": {"test": "echo should-not-run"},
            }
        ),
        encoding="utf-8",
    )
    config = JazzyConfig()
    config.agent.provider = "noop"

    report = run_agent(
        tmp_path,
        AgentRequest(mode="review", prompt="review only", fix=False, allow_exec=True),
        config,
    )

    assert report.checks
    assert all(check.skipped for check in report.checks)
    assert "Review mode is read-only." in report.checks[0].output


def test_report_includes_finding_detail() -> None:
    from jazzy.reports.final_report import FinalReport
    from jazzy.reports.findings import Finding, Severity

    report = FinalReport(
        mode="review",
        prompt=None,
        findings=[
            Finding(
                severity=Severity.MAJOR,
                title="Unsafe pattern",
                path="app.py",
                line=10,
                detail="eval(user_input)",
            )
        ],
    )

    assert "Evidence: eval(user_input)" in report.markdown()
