<p align="center">
  <img src="./jazzyagent-banner.png" alt="JazzyAgent — Code Review, Fixes, Verification" width="100%" />
</p>

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
- безопасный запуск команд через `argv` без `shell=True`
- read-only review: `jazzy review` не запускает код проекта
- gated execution: проверки запускаются только с `--allow-exec`
- root-bound file tools: чтение и запись файлов не выходят за пределы workspace
- Llama3 analysis через Ollama (`ollama:llama3`)
- контекст для LLM: дерево релевантных файлов и содержимое ключевых файлов
- fallback detection одиночных Python-скриптов, например `main.py`
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
jazzy doctor --allow-exec
```

`jazzy review` по умолчанию только читает код и не выполняет scripts из чужого
репозитория. Для запуска найденных проверок используйте явный флаг:

```bash
jazzy doctor --allow-exec
jazzy fullstack --allow-exec "Проверь frontend и backend"
```

## Llama3 через Ollama

По умолчанию Jazzy пытается использовать локальный Ollama provider с моделью
`llama3` для дополнительного анализа контекста проекта. В LLM-контекст попадает
дерево релевантных файлов и содержимое ключевых файлов: `main.py`, `app.py`,
`routes.py`, `models.py`, `pyproject.toml`, `requirements.txt`, `package.json`,
`Dockerfile`, `README.md` и другие текстовые файлы.

Если Ollama не запущен, Jazzy продолжит deterministic scan и покажет это в
`Остаточный риск`.

Минимальный запуск:

```bash
ollama pull llama3
ollama serve
jazzy review "Проанализируй архитектуру и риски"
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
provider = "ollama"
model = "llama3"
ollama_host = "http://localhost:11434"
ollama_timeout = 120
reasoning_effort = "medium"
```
