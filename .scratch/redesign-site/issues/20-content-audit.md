# 20: Retro-фолов-ап — аудит контента и полный CI-гейт

**What to build:** Пункты 1–2 ретро `docs/retro/2026-10-10-redesign.md`: детерминированная проверка «теги проектов ↔ навыки» (инциденты t18/t19) и закрытие дыр CI-гейта.

**Статус:** done

- [x] `main/audit.py::audit_content()` — E100 (тег без навыка), W101 (навык без совпадающего тега); только опубликованные проекты
- [x] `manage.py audit_content` — печать + exit 1 при E100 (вместо системного чека: dev-БД — легаси-подмножество, чек убивал бы runserver ложными Error)
- [x] Тесты: helper (E100/W101/пусто/filter_tag) + команда (exit 1 / ok) — 42/42; тест-БД из миграций посеяна (3 бот-проекта + навыки, 0014–0016) → класс чистит Skill/Project в setUp (UNIQUE-коллизии на сидах)
- [x] deploy.yml: добавлены `makemigrations --check --dry-run` + `node --check static/js/*.js`
- [x] AGENTS: Dev workflow + Auto-deploy + data-migrations (0014/0015/0016) — синхронизированы
- [x] Гейт зелёный; запушено; CI success