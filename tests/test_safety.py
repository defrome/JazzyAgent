from __future__ import annotations

from pathlib import Path

import pytest

from jazzy.safety.workspace import resolve_workspace_path
from jazzy.tools.read_file import read_file
from jazzy.tools.shell import run_command
from jazzy.tools.write_file import write_file


def test_workspace_rejects_path_traversal(tmp_path: Path) -> None:
    with pytest.raises(PermissionError):
        resolve_workspace_path(tmp_path, "../outside.txt")


def test_file_tools_stay_inside_workspace(tmp_path: Path) -> None:
    write_file(tmp_path, "nested/hello.txt", "hello")

    assert read_file(tmp_path, "nested/hello.txt") == "hello"
    with pytest.raises(PermissionError):
        read_file(tmp_path, "/etc/passwd")


def test_command_execution_requires_explicit_gate(tmp_path: Path) -> None:
    with pytest.raises(PermissionError, match="allow_exec=True"):
        run_command(["python3", "--version"], root=tmp_path, cwd=tmp_path)


def test_command_execution_rejects_shell_bypass(tmp_path: Path) -> None:
    with pytest.raises(PermissionError):
        run_command(["sh", "-c", "echo unsafe"], root=tmp_path, cwd=tmp_path, allow_exec=True)
