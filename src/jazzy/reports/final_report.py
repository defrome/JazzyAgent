from __future__ import annotations

from dataclasses import dataclass, field

from jazzy.reports.findings import Finding


@dataclass
class CheckResult:
    command: str
    passed: bool
    output: str = ""
    skipped: bool = False


@dataclass
class FinalReport:
    mode: str
    prompt: str | None
    findings: list[Finding] = field(default_factory=list)
    changed_files: list[str] = field(default_factory=list)
    checks: list[CheckResult] = field(default_factory=list)
    residual_risk: list[str] = field(default_factory=list)

    def markdown(self) -> str:
        lines = [f"Jazzy report ({self.mode})", ""]
        if self.prompt:
            lines += ["Task:", f"- {self.prompt}", ""]

        lines.append("Findings:")
        if self.findings:
            for finding in self.findings:
                lines.append(f"- {finding.label()}")
                if finding.detail:
                    detail = finding.detail.strip()
                    if detail:
                        lines.append(f"  Evidence: {detail[:800]}")
        else:
            lines.append("- No obvious issues found during MVP scan.")
        lines.append("")

        lines.append("Changed:")
        if self.changed_files:
            lines.extend(f"- `{path}`" for path in self.changed_files)
        else:
            lines.append("- No files changed by the MVP local fixer.")
        lines.append("")

        lines.append("Checks:")
        if self.checks:
            for check in self.checks:
                status = "skipped" if check.skipped else "passed" if check.passed else "failed"
                lines.append(f"- `{check.command}` - {status}")
                if check.output and not check.passed:
                    lines.append(f"  Output: {check.output.strip()[:800]}")
        else:
            lines.append("- No checks were detected or run.")
        lines.append("")

        lines.append("Residual risk:")
        if self.residual_risk:
            lines.extend(f"- {item}" for item in self.residual_risk)
        else:
            lines.append(
                "- OpenAI/Codex autonomous patch loop is scaffolded but not enabled in MVP."
            )
        return "\n".join(lines)
