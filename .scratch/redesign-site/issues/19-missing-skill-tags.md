# 19: Навыков FastAPI и GitHub Pages нет — теги проектов без кнопок-навыков

**What to build:** Аудит `/api/skills/` vs теги проектов: `FastAPI` (ferma) и `GitHub Pages` (online_library) — теги без соответствующих навыков. Клик по технологии из секции Skills был невозможен.

**Решение:** data-миграция `0016_add_skills_fastapi_github_pages.py` — `get_or_create` по имени, `sort_order` = max+1 (ставятся в конец категорий backend/devops), без иконки (subset шрифта в SKILL не содержит новых лигатур). Rollback — delete.

**Status:** done

- [x] Аудит тегов vs навыков (mismatch: FastAPI, GitHub Pages)
- [x] Миграция 0016, применяется; makemigrations --check пуст; ruff/mypy (28 файлов)/36 тестов зелёные
- [x] Запушено, CI success, прод-проверка /api/skills/ содержит FastAPI и GitHub Pages