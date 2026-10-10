# 22: Клик по навыку pytest на проде — «проектов не найдено»

**What to build:** Навык `pytest` (тикет 21) без совпадающего тега проекта → пустой state при клике (W101). Сделать pytest честным: подключить pytest-раннер в сам репозиторий и дать карточке Dossier тег `pytest`.

**Status:** done

- [x] `uv add --dev pytest pytest-django` (dev-группа, pyproject + lock)
- [x] `[tool.pytest.ini_options]` (DJANGO_SETTINGS_MODULE, pythonpath, testpaths) — `uv run pytest` гоняет 42/42 теста локально
- [x] CI: Tests-шаг `uv run manage.py test` → `uv run pytest`
- [x] `main/migrations/0019_add_dossier_pytest_tag.py` — тег `pytest` на карточке Dossier (update-only, дер-dup, rollback-вычитание)
- [x] README/AGENTS: команда `uv run pytest`, gate, миграция 0019
- [x] dev-аудит exit 0 (pytest в warnings локально — корр., dossier нет в дев-сидах; на проде тег применится)
- [x] Гейт зелёный; запушено; CI success; прод: клик по pytest → Dossier