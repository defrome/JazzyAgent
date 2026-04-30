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
    llm_review: str | None = None
    changed_files: list[str] = field(default_factory=list)
    checks: list[CheckResult] = field(default_factory=list)
    residual_risk: list[str] = field(default_factory=list)

    def markdown(self) -> str:
        lines = [f"Отчет Jazzy ({self.mode})", ""]
        if self.prompt:
            lines += ["Задача:", f"- {self.prompt}", ""]

        lines.append("Находки:")
        if self.findings:
            for finding in self.findings:
                lines.append(f"- {finding.label()}")
                if finding.detail:
                    detail = finding.detail.strip()
                    if detail:
                        lines.append(f"  Доказательство: {detail[:800]}")
        else:
            lines.append("- Во время MVP-скана явных проблем не найдено.")
        lines.append("")

        lines.append("LLM-анализ:")
        if self.llm_review:
            lines.append(self.llm_review.strip())
        else:
            lines.append("- LLM-анализ не выполнялся.")
        lines.append("")

        lines.append("Изменено:")
        if self.changed_files:
            lines.extend(f"- `{path}`" for path in self.changed_files)
        else:
            lines.append("- Файлы не изменялись.")
        lines.append("")

        lines.append("Проверки:")
        if self.checks:
            for check in self.checks:
                status = "пропущено" if check.skipped else "успешно" if check.passed else "ошибка"
                lines.append(f"- `{check.command}` - {status}")
                if check.output and not check.passed:
                    lines.append(f"  Вывод: {check.output.strip()[:800]}")
        else:
            lines.append("- Проверки не обнаружены или не запускались.")
        lines.append("")

        lines.append("Остаточный риск:")
        if self.residual_risk:
            lines.extend(f"- {item}" for item in self.residual_risk)
        else:
            lines.append(
                "- Автономный patch-loop подготовлен, но еще не включен в MVP."
            )
        return "\n".join(lines)
