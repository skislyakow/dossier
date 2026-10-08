# 01: Перевод проекта на uv (lockfile зависимостей)

**What to build:** Окружение проекта детерминировано на всех машинах: домашний ПК, рабочий ПК, CI и VPS получают одинаковые версии Python-зависимостей (включая транзитивные) из закоммиченного `uv.lock`. Зависимости описаны в `pyproject.toml`, установка везде через `uv sync --frozen`, запуск через `uv run`. Файлы `requirements.txt` / `requirements-dev.txt` удаляются.

Решения, зафиксированные при обсуждении:
- **uv ставится и на VPS** (не только локально/CI)
- Dev-зависимости — в `[dependency-groups] dev` uv (стандартная замена `requirements-dev.txt`)
- Код Django не меняется вообще — только tooling
- Секция `AGENTS.md` обновляется, чтобы агенты не искали venv/pip

**Blocked by:** None.

**Status:** ready-for-agent

- [ ] `pyproject.toml`: `[project]` с django==6.0.4, gunicorn==23.0.0, django-unfold==0.100.0, `requires-python = ">=3.12"`; `[dependency-groups] dev` с django-stubs==5.1.3, mypy==1.15.0, ruff==0.15.20
- [ ] `.python-version` (3.12) и `uv.lock` созданы и закоммичены
- [ ] `requirements.txt` и `requirements-dev.txt` удалены; все ссылки на них обновлены (`deploy.yml`, `AGENTS.md`, где ещё встретится)
- [ ] CI: `astral-sh/setup-uv` → `uv sync --frozen` → `uv run ruff check .` → `uv run manage.py test`; деплой-job: `uv sync --frozen --no-dev` и `uv run manage.py ...` вместо прямых путей к `.venv/bin/*`
- [ ] VPS: uv установлен условной командой в деплой-скрипте (`command -v uv || curl -LsSf https://astral.sh/uv/install.sh | sh`, PATH из `~/.local/bin`) — ручной вход не требуется
- [ ] systemd-сервис `dossier.service` продолжает работать (путь `/root/dossier/.venv/bin/gunicorn` сохраняется — uv использует тот же `.venv`)
- [ ] `AGENTS.md`: Setup (установка uv, `uv run` вместо активации venv), Dev workflow (`uv run manage.py test`, `uv run ruff check .`), Auto-deploy
- [ ] Локально: `uv sync --frozen` + `uv run manage.py test` + `uv run ruff check .` проходят
- [ ] Push → workflow `Deploy to VPS` success (check + deploy)
