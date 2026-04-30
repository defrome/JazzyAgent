from __future__ import annotations

from pathlib import Path

from jazzy.reports.findings import Finding, Severity
from jazzy.tools.search import rg_search

BACKEND_PATTERN = r"eval\(|raw\(|execute\(|CORS|SECRET|TOKEN|PASSWORD|process\.env|os\.environ"


def analyze_backend(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for match in rg_search(root, BACKEND_PATTERN)[:50]:
        if match.path.startswith("src/jazzy/analyzers/"):
            continue
        findings.append(
            Finding(
                severity=Severity.MAJOR,
                title="Совпадение backend/security-скана",
                path=match.path,
                line=match.line,
                detail=match.text,
            )
        )
    return findings
