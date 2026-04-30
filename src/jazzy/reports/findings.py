from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class Severity(StrEnum):
    CRITICAL = "critical"
    MAJOR = "major"
    MINOR = "minor"


@dataclass(frozen=True)
class Finding:
    severity: Severity
    title: str
    path: str | None = None
    line: int | None = None
    detail: str | None = None

    def label(self) -> str:
        location = ""
        if self.path:
            location = self.path
            if self.line:
                location += f":{self.line}"
        return f"{self.severity.value}: {self.title}" + (f" ({location})" if location else "")

