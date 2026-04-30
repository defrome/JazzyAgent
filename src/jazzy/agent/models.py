from __future__ import annotations

from pydantic import BaseModel


class AgentRequest(BaseModel):
    mode: str
    prompt: str | None
    fix: bool = True
    allow_exec: bool = False
