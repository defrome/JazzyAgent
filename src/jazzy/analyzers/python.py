from __future__ import annotations

from pathlib import Path

from jazzy.reports.findings import Finding, Severity
from jazzy.tools.search import rg_search

PYTHON_PATTERN = r"except Exception|pass|print\(|Any|TODO|FIXME|raise NotImplementedError"


def analyze_python(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for match in rg_search(root, PYTHON_PATTERN)[:50]:
        findings.append(
            Finding(
                severity=Severity.MINOR,
                title="Python quality scan match",
                path=match.path,
                line=match.line,
                detail=match.text,
            )
        )
    return findings

