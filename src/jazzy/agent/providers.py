from __future__ import annotations

import json
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Protocol


class LLMProvider(Protocol):
    name: str

    def review(self, prompt: str, context: str) -> str:
        """Return a review summary for the provided project context."""


@dataclass(frozen=True)
class NoopProvider:
    name: str = "noop"

    def review(self, prompt: str, context: str) -> str:
        return ""


@dataclass(frozen=True)
class OllamaProvider:
    model: str = "llama3"
    host: str = "http://localhost:11434"
    timeout: float = 8.0

    @property
    def name(self) -> str:
        return f"ollama:{self.model}"

    def review(self, prompt: str, context: str) -> str:
        payload = {
            "model": self.model,
            "prompt": (
                "Ты Jazzy, инженерный code review агент. "
                "Дай короткий структурированный анализ: critical/major/minor, "
                "что проверено, что рискованно, какие следующие проверки нужны.\n\n"
                f"Задача пользователя:\n{prompt}\n\nКонтекст проекта:\n{context}"
            ),
            "stream": False,
        }
        data = json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(
            f"{self.host.rstrip('/')}/api/generate",
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                body = json.loads(response.read().decode("utf-8"))
        except (OSError, urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            raise RuntimeError(f"Ollama/Llama3 is unavailable: {exc}") from exc
        return str(body.get("response", "")).strip()


def build_provider(provider: str, model: str, host: str | None = None) -> LLMProvider:
    if provider == "ollama":
        return OllamaProvider(model=model, host=host or "http://localhost:11434")
    return NoopProvider()
