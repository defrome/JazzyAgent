from __future__ import annotations

import shlex


DESTRUCTIVE_COMMANDS = {
    "rm",
    "rmdir",
    "dd",
    "mkfs",
    "shutdown",
    "reboot",
}

BLOCKED_GIT_ARGS = {
    ("git", "reset"),
    ("git", "checkout"),
    ("git", "clean"),
}


def assert_command_allowed(command: str, allow_destructive: bool = False) -> None:
    if allow_destructive:
        return
    parts = shlex.split(command)
    if not parts:
        raise ValueError("Empty shell command is not allowed.")
    executable = parts[0]
    if executable in DESTRUCTIVE_COMMANDS:
        raise PermissionError(f"Destructive command is blocked: {executable}")
    if len(parts) >= 2 and (parts[0], parts[1]) in BLOCKED_GIT_ARGS:
        raise PermissionError(f"Potentially destructive git command is blocked: {parts[0]} {parts[1]}")

