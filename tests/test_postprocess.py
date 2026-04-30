from __future__ import annotations

from jazzy.agent.postprocess import postprocess_llm_review


def test_postprocess_marks_versioned_import_as_suspicious() -> None:
    text = "## Optimized Snippet\n```python\nimport requests==2.25.1\n```"

    processed = postprocess_llm_review(text)

    assert processed.startswith("⚠️ Предупреждение Jazzy")
    assert "requirements.txt" in processed


def test_postprocess_leaves_valid_imports_unchanged() -> None:
    text = "```python\nimport requests\n```"

    assert postprocess_llm_review(text) == text
