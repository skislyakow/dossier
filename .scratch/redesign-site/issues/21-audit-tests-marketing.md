# 21: Аудит+тесты — README, навыки, карточка Dossier

**What to build:** По запросу пользователя — показать HR «качество» проекта: добавить навыки `Python`/`pytest` в сиды, упомянуть аудит/тесты в README и карточке Dossier.

**Status:** done

- [x] `main/migrations/0017_add_skills_python_pytest.py` — `get_or_create` `Python` (backend/xl) и `pytest` (tools/sm); на проде Python — no-op (есть из админки), pytest добавляется
- [x] `main/migrations/0018_dossier_ci_bullet.py` — буллет CI в features Dossier: `(ruff, mypy, тесты)` → `(ruff, mypy, 42 теста, makemigrations, node)` (update-only по repo)
- [x] README: бейджи 42 tests / Ruff / mypy / audit_content, раздел «Качество кода», буллет аудита в Возможности, CI/CD-буллет
- [x] AGENTS: Skills-сиды `Python`/`pytest`, data-migrations 0017/0018
- [x] dev-аудит: E100 ушёл (Python-навык), exit 0; 6 W101 — предупреждения (FastAPI, GitHub Pages, mypy, pymorphy3, pytest, python-dotenv)
- [x] Гейт зелёный; запушено; CI success; прод-проверка