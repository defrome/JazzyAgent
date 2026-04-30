<p align="center">
  <img src="./jazzyagent-banner.png" alt="JazzyAgent — Code Review, Fixes, Verification" width="100%" />
</p>

# Jazzy

**Jazzy** — автономный CLI-агент для ревью и исправления frontend/backend проектов.
Он анализирует репозиторий, определяет стек, находит проблемы, запускает проверки
только с явного разрешения и выдает инженерный отчет на русском языке.

```bash
jazzy review
jazzy doctor --allow-exec
jazzy frontend "Найди mobile overflow"
jazzy backend "Проверь обработку ошибок и тесты"
```

## Что Уже Умеет

- Определяет JS/TS frontend, Node backend и Python backend.
- Находит одиночные Python-скрипты вроде `main.py`.
- Выбирает команды `build`, `lint`, `test`, `type-check`, `pytest`, `ruff`, `mypy`.
- Делает быстрый scan через `rg`.
- Строит LLM-контекст: дерево файлов и содержимое ключевых файлов.
- Использует Llama3 через Ollama для подробного review narrative.
- Пишет отчет строго на русском: что делает код, поток выполнения, риски, рекомендации и план улучшений.
- Не запускает код проекта в `review`-режиме.
- Запускает проверки только с `--allow-exec`.
- Запускает команды через `argv` без `shell=True`.
- Защищает file tools от выхода за пределы workspace.
- Помечает подозрительные LLM-советы вроде `import package==version`.

## Быстрый Старт

Установка для разработки:

```bash
cd /Users/defrome/Documents/JazzyAgent
python -m pip install -e ".[dev]"
```

Если используется локальное окружение из этого репозитория:

```bash
cd /Users/defrome/Documents/JazzyAgent
source .venv/bin/activate
jazzy review
```

Проверить другой проект:

```bash
cd /path/to/project
/Users/defrome/Documents/JazzyAgent/.venv/bin/jazzy review
```

Или через `--path`:

```bash
cd /Users/defrome/Documents/JazzyAgent
.venv/bin/jazzy review --path /path/to/project
```

## Команды

| Команда | Что делает |
| --- | --- |
| `jazzy` | Открывает интерактивный режим. |
| `jazzy "задача"` | Одноразовый запуск в auto-режиме. |
| `jazzy review` | Read-only review без запуска кода проекта. |
| `jazzy fix` | Режим исправлений. Сейчас patch-loop подготовлен, но автопатчинг еще gated. |
| `jazzy frontend` | Проверка frontend-кода, layout, routing, CSS, accessibility. |
| `jazzy backend` | Проверка backend-кода, routes, validation, tests, error handling. |
| `jazzy fullstack` | Проверка frontend и backend вместе. |
| `jazzy doctor` | Диагностика build/test проблем. |
| `jazzy mobile` | Поиск mobile layout проблем. |
| `jazzy security` | Легкий security review очевидных рисков. |

## Безопасность

По умолчанию Jazzy безопасен для чтения:

```bash
jazzy review --path /path/to/project
```

Этот режим:

- не выполняет `npm scripts`, `pytest`, `ruff`, `make` и другие команды проекта;
- не изменяет файлы;
- анализирует только содержимое workspace;
- показывает найденные команды как пропущенные.

Чтобы реально запустить проверки, нужен явный флаг:

```bash
jazzy doctor --path /path/to/project --allow-exec
jazzy fullstack --path /path/to/project --allow-exec
```

Команды запускаются через `subprocess.run(argv, shell=False)`. Jazzy блокирует
shell-bypass вроде `sh -c` и не дает file tools читать или писать вне root проекта.

## Llama3 Через Ollama

Jazzy использует локальный Ollama provider:

```toml
[agent]
provider = "ollama"
model = "llama3"
ollama_host = "http://localhost:11434"
ollama_timeout = 120
```

Подготовка:

```bash
ollama pull llama3
ollama serve
```

Запуск:

```bash
jazzy review --path /path/to/project "Проанализируй архитектуру и риски"
```

В LLM-контекст попадает:

- список релевантных файлов;
- содержимое `main.py`, `app.py`, `server.py`, `routes.py`, `models.py`;
- `pyproject.toml`, `requirements.txt`, `package.json`;
- `Dockerfile`, `README.md` и другие текстовые файлы.

Если Ollama не запущен или недоступен, Jazzy продолжит deterministic scan и
покажет причину в секции `Остаточный риск`.

## Формат Отчета

Отчет Jazzy включает:

- `Находки` — deterministic scan с file:line и доказательством.
- `LLM-анализ` — подробный review narrative от Llama3.
- `Изменено` — список измененных файлов.
- `Проверки` — найденные, запущенные или пропущенные команды.
- `Остаточный риск` — что не удалось проверить.

LLM-анализ просит модель отвечать в таком формате:

- `Summary`
- `Что делает код`
- `Поток выполнения`
- `Critical Issues`
- `Major Issues`
- `Minor Issues`
- `Security Review`
- `Architecture & Clean Code`
- `Рекомендации по улучшению`
- `План улучшений`
- `Optimized Snippet`

## Примеры

Read-only review:

```bash
jazzy review --path ./my-app
```

Диагностика сборки с запуском проверок:

```bash
jazzy doctor --path ./my-app --allow-exec
```

Frontend:

```bash
jazzy frontend --path ./web "Найди почему на mobile все вылезает"
```

Backend:

```bash
jazzy backend --path ./api "Проверь validation, error handling и тесты"
```

Fullstack:

```bash
jazzy fullstack --path ./project --allow-exec "Проверь frontend и backend"
```

Одиночный Python-скрипт:

```bash
mkdir demo
echo 'print("hello")' > demo/main.py
jazzy review --path ./demo
```

## Поддерживаемая Детекция

Frontend:

- `package.json`
- Vite, React, Vue, Next.js, Nuxt, Svelte, Astro
- npm, pnpm, yarn, bun

Backend:

- Python: `pyproject.toml`, `requirements.txt`, `manage.py`, `setup.py`, одиночные `.py`
- FastAPI, Django, Flask
- Node backend: Express, NestJS

Команды:

- JS/TS: `type-check`, `typecheck`, `lint`, `test`, `build`
- Python: `pytest`, `ruff check .`, `mypy .`, `python manage.py test`

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

## Разработка

```bash
python -m pip install -e ".[dev]"
python -m pytest
python -m ruff check .
```

Текущий статус проверок:

```text
pytest: 17 passed
ruff: all checks passed
```

## Статус

Jazzy сейчас находится на стадии MVP. Уже есть безопасный read-only reviewer,
детекция проекта, Llama3-анализ, gated execution и базовый patch-инструментарий.
Следующий крупный шаг — полноценный gated loop `analyze -> plan -> patch -> verify`.
