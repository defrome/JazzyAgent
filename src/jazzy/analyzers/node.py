from __future__ import annotations

from pathlib import Path

from jazzy.reports.findings import Finding, Severity
from jazzy.tools.search import rg_search


NODE_PATTERN = r"any|unknown|console\.log|debugger|TODO|FIXME"


def analyze_node(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for match in rg_search(root, NODE_PATTERN)[:50]:
        findings.append(
            Finding(
                severity=Severity.MINOR,
                title="Node/TypeScript scan match",
                path=match.path,
                line=match.line,
                detail=match.text,
            )
        )
    return findings

