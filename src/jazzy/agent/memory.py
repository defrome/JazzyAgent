from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class AgentMemory:
    notes: list[str] = field(default_factory=list)

    def add(self, note: str) -> None:
        self.notes.append(note)

