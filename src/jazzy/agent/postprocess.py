from __future__ import annotations

import re

INVALID_VERSIONED_IMPORT = re.compile(
    r"(?m)^\s*(?:from\s+[\w.]+==[^\s]+\s+import|import\s+[\w.]+==[^\s]+)"
)


def postprocess_llm_review(text: str) -> str:
    if not INVALID_VERSIONED_IMPORT.search(text):
        return text
    warning = (
        "⚠️ Предупреждение Jazzy: LLM-ответ содержит подозрительный невалидный Python "
        "вида `import package==version`. Версии зависимостей нужно указывать в "
        "`requirements.txt` или `pyproject.toml`, а не в import-строках.\n\n"
    )
    return warning + text
