from __future__ import annotations

import tomllib
from pathlib import Path

from pydantic import BaseModel, Field


class ProjectConfig(BaseModel):
    name: str | None = None
    root: str = "."
    mode: str = "auto"


class FrontendConfig(BaseModel):
    path: str | None = None
    framework: str | None = None
    package_manager: str | None = None
    build: str | None = None
    typecheck: str | None = None
    lint: str | None = None
    test: str | None = None


class BackendConfig(BaseModel):
    path: str | None = None
    language: str | None = None
    framework: str | None = None
    test: str | None = None
    lint: str | None = None
    typecheck: str | None = None
    build: str | None = None


class SafetyConfig(BaseModel):
    allow_destructive_commands: bool = False
    require_git_clean: bool = False
    max_patch_files: int = 25


class AgentConfig(BaseModel):
    provider: str = "ollama"
    model: str = "llama3"
    ollama_host: str = "http://localhost:11434"
    ollama_timeout: float = 120.0
    reasoning_effort: str = "medium"


class JazzyConfig(BaseModel):
    project: ProjectConfig = Field(default_factory=ProjectConfig)
    frontend: FrontendConfig = Field(default_factory=FrontendConfig)
    backend: BackendConfig = Field(default_factory=BackendConfig)
    safety: SafetyConfig = Field(default_factory=SafetyConfig)
    agent: AgentConfig = Field(default_factory=AgentConfig)


def load_config(root: Path) -> JazzyConfig:
    config_path = root / "jazzy.toml"
    if not config_path.exists():
        return JazzyConfig()
    with config_path.open("rb") as file:
        data = tomllib.load(file)
    return JazzyConfig.model_validate(data)
