# Spec review — `0fc7cbe..HEAD` (SEO + CI-аудит + a11y + авто-резюме)

Диапазон: 13 коммитов, база `0fc7cbe` («retro-2»), HEAD `3d52b3b`. Требования — из арх-ревью (c5 SEO, c8 CI-аудит, c9 a11y) и ADR-0003.

## (a) Missing / partial

1. **Taxonomy-тесты не в своём модуле.** ADR-0004 pакрывает «каждый модуль зеркалит тесты»; `TaxonomyTest` живёт в `test_views.py:177` (skill_size/tag_cloud/resolve_tag) — правило модульного зеркала нарушено с рождения. Тест-класс человеком не отличим по имени от API-тестов.
2. **Порядок опыта резюме не покрыт тестами.** ADR-0003:23 — «сортировка start_date desc с фолбэком на sort_order»: ни один тест не проверяет `_resume_sort_key`/`context()['experience']`. Более того, этот порядок реализован неверно (см. c(3)).
3. **Визуальный регресс не оставил артефакта.** Прогон headless Chrome (5 брейкпоинтов + reduced-motion) прошёл зелёным, но в репо нет ни скрипта, ни снапшота — проверку нельзя воспроизвести.
4. Verified OK: robots/sitemap (SITE_URL, Disallow /admin/+/api/, Sitemap-строка, canonical `/` `/resume/`), JSON-LD в `<head>` через `|safe` с `\uXXXX`-экранированием `<`/`>`/`&`, `disclosurePanel` wiring (aria-controls/expanded, Esc → focus вернуть на триггер), `audit_content` в gate.sh и check-джобе CI.

## (b) Not asked for (scope creep)

1. **Server-built contact links** (`ContactInfo.href()`, `api_contact` отдаёт готовые href/external) — в авторитетном списке c5/c6 не заявлены. (Факт: это кандидат c4 «Ship taxonomy and contact data from the server» арх-ревью — требование заявлено там, претензия снята.)
2. **`brotli>=1.2.0`** в pyproject — не запрашивалось; мотивируется PDF-весом, но в доки/ADR не внесено.

## (c) Implemented but looks wrong

1. **`RESUME_AUTOGEN=0` включает, а не выключает.** `main/signals.py:10`: `if os.environ.get('RESUME_AUTOGEN', ''): return True` — любая непустая строка (включая `"0"`) истинна и перебивает `PYTEST_CURRENT_TEST`. Документировано обратное: settings.py:219-220, ADR-0003:26, AGENTS.md:18.
2. **`_resume_sort_key` инвертирует фолбэк под reverse=True.** ADR-0003:23 «desc с фолбэком на sort_order», модель по умолчанию `ordering = ['sort_order']` (asc). Ключ `(0|1, start_date/sort_order)` + `reverse=True` отдаёт undated по sort_order **по убыванию** и в ти-брейке дат тоже по убыванию. Скорее всего инверсия; непокрыто тестом.
3. Correctly done: остальное совпадает со спекой — ADR-0001/0002/0004, `esc()` во всех рендерах, cтэк изменён (no new JS/CSS deps).