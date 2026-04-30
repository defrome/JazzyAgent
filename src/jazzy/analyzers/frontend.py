from __future__ import annotations

from pathlib import Path

from jazzy.reports.findings import Finding, Severity
from jazzy.tools.search import rg_search

FRONTEND_PATTERN = r"TODO|FIXME|console\.log|debugger|overflow|100vw|min-width"


def analyze_frontend(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for match in rg_search(root, FRONTEND_PATTERN)[:50]:
        if _is_analyzer_definition(match.path):
            continue
        severity = Severity.MAJOR if match.text in {"100vw", "overflow"} else Severity.MINOR
        findings.append(
            Finding(
                severity=severity,
                title="Frontend scan match",
                path=match.path,
                line=match.line,
                detail=match.text,
            )
        )
    return findings


def _is_analyzer_definition(path: str) -> bool:
    return path.startswith("src/jazzy/analyzers/")
