# Jazzy

Jazzy is an autonomous CLI code review and fix agent for frontend and backend projects.
It scans your repo, finds bugs, patches code, runs checks, and returns a verified engineering report.

## MVP

Supported in this first version:

- `jazzy` interactive mode
- `jazzy "Проверь проект и исправь ошибки"`
- `jazzy frontend "Исправь mobile layout"`
- `jazzy backend "Исправь failing tests"`
- `jazzy doctor`
- JS/TS frontend and Python backend project detection
- command detection for build, lint, tests and type checks
- fast code scanning through `rg` when available
- safe shell command runner with blocked destructive commands
- unified-diff patch application
- final engineering report

## Install for local development

```bash
python -m pip install -e ".[dev]"
```

## Examples

```bash
jazzy "Проверь проект, исправь build errors и запусти тесты"
jazzy frontend "Найди почему на mobile всё вылезает и исправь"
jazzy backend "Проверь API, ошибки валидации, тесты и обработку ошибок"
jazzy doctor
```

## Configuration

Create `jazzy.toml` in a project root:

```toml
[project]
name = "my-app"
root = "."
mode = "fullstack"

[frontend]
path = "frontend"
framework = "vue"
package_manager = "npm"
build = "npm run build"
typecheck = "npm run type-check"
lint = "npm run lint"

[backend]
path = "backend"
language = "python"
framework = "fastapi"
test = "pytest"
lint = "ruff check ."
typecheck = "mypy ."

[safety]
allow_destructive_commands = false
require_git_clean = false
max_patch_files = 25

[agent]
model = "gpt-5.3-codex"
reasoning_effort = "medium"
```

