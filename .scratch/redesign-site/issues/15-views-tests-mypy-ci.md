# 15: Тесты на view + mypy в CI

**What to build:** Покрыть основные view тестами и привести все модули `main/` к чистой типизации mypy, встроить шаг в чек-гейт GitHub Actions.

**Status:** done

## Тесты на view
- [x] Покрытие уже было (HomeViewTest + ApiTimeline/ApiContact/ApiSkills/ApiProjects/ApiGithub) — пункт закрыт как выполненный, новые проверки не потребовались

## mypy в CI
- [x] deps уже в dev-группе (mypy==1.15.0, django-stubs==5.1.3) — добавлен только конфиг
- [x] `[tool.mypy]`: python_version 3.12, `mypy_django_plugin`, `warn_unused_ignores`, `no_implicit_optional`, `check_untyped_defs`, `show_error_codes`; `[tool.django-stubs]` → `config.settings` (в pyproject.toml)
- [x] Единственная ошибка: `icon_display.short_description = ''` в `SkillAdmin` → заменено на `@admin.display(description='')`; `uv run mypy main/` — Success в 26 файлах
- [x] `deploy.yml` чек-гейт: step `mypy main/` между Ruff и Tests
- [x] Гейт локально: ruff + mypy + 36/36 тестов + makemigrations --check + node --check
- [x] AGENTS: dev-workflow step 3 (mypy), чек-гейт-описание, To-do — закрыт