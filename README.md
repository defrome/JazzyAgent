# Jazzy

Jazzy — автономный CLI-агент для ревью и исправления frontend/backend проектов.
Он анализирует репозиторий, находит ошибки, правит код, запускает проверки и
выдает финальный инженерный отчет.

## MVP

Что поддерживает первая версия:

- интерактивный режим `jazzy`
- `jazzy "Проверь проект и исправь ошибки"`
- `jazzy frontend "Исправь mobile layout"`
- `jazzy backend "Исправь failing tests"`
- `jazzy doctor`
- детекцию JS/TS frontend и Python backend проектов
- автоматический выбор команд для build, lint, tests и type checks
- быстрый scan кода через `rg`, если он доступен
- безопасный запуск shell-команд с блокировкой destructive commands
- применение unified-diff patches
- финальный engineering report

## Установка для локальной разработки

```bash
python -m pip install -e ".[dev]"
```

## Примеры

```bash
jazzy "Проверь проект, исправь build errors и запусти тесты"
jazzy frontend "Найди почему на mobile всё вылезает и исправь"
jazzy backend "Проверь API, ошибки валидации, тесты и обработку ошибок"
jazzy doctor
```

## Конфигурация

Создайте `jazzy.toml` в корне проекта:

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
