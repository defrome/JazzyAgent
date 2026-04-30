from __future__ import annotations

from jazzy.agent.prompts import SYSTEM_PROMPT


def test_system_prompt_requires_russian_review_narrative_and_valid_python() -> None:
    assert "Отвечай строго на русском языке." in SYSTEM_PROMPT
    assert "Никогда не пиши `import package==version`." in SYSTEM_PROMPT
    assert "## Что делает код" in SYSTEM_PROMPT
    assert "## Поток выполнения" in SYSTEM_PROMPT
    assert "## План улучшений" in SYSTEM_PROMPT
