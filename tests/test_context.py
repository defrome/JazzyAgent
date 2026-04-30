from __future__ import annotations

from pathlib import Path

from jazzy.agent.context import build_review_context


def test_review_context_includes_tree_and_main_py_content(tmp_path: Path) -> None:
    (tmp_path / "main.py").write_text(
        "import requests\n\nrequests.get('https://example.com')\n",
        encoding="utf-8",
    )

    context = build_review_context(tmp_path)

    assert "Файлы проекта:" in context
    assert "- main.py" in context
    assert "--- FILE: main.py ---" in context
    assert "requests.get('https://example.com')" in context
