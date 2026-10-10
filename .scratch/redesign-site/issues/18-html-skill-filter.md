# 18: Клик по навыкам HTML/CSS/JavaScript — «проектов не найдено»

**What to build:** Навык `HTML` (и `CSS`, `JavaScript`) в секции Skills: клик фильтрует портфолио по имени, но ни у одного проекта в `tags` нет этих технологий → пустой state, хотя Dossier их использует (статичные бейджи + языковая полоса GitHub: HTML 13%).

**Причина:** теги карточек не учитывают web-технологии (HTML/CSS/JS).

**Решение:** data-миграция `0015_dossier_html_tags.py` — merge `['HTML', 'CSS', 'JavaScript']` в `tags` Dossier (update-only по `repo`, dedup через `dict.fromkeys`, rollback — вычитание). Dossier — единственный сайт-проект с этими бейджами; click по HTML/CSS/JS снова находит его.

**Status:** done

- [x] Диагноз: `/api/skills/` (кнопка HTML, filter_tag пуст) vs `/api/projects/` (ни один `tags` не содержит HTML)
- [x] Миграция 0015, применяется; makemigrations --check пуст; ruff/mypy (27 файлов)/36 тестов зелёные
- [x] Запушено, CI success, прод-проверка: клик по HTML → Dossier найден