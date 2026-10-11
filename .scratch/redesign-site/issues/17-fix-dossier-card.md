# 17: Карточка проекта Dossier — устаревшие features

**What to build:** Карточка Dossier на проде описывала удалённый функционал (терминал с AI-ассистентом, typing-анимация, «Skills cloud») — результат тикетов 01/08/10. Обновить `features` под текущее состояние, update-only по `repo`, паттерн 0013.

**Status:** done

- [x] Получены актуальные features из `/api/projects/` на проде (8 проектов)
- [x] `main/migrations/0014_update_dossier_features.py` — RunPython(seed, rollback), update-only по `skislyakow/dossier`, в rollback — guard по равенству features
- [x] `makemigrations --check` пуст; `migrate` применяется; 36/36 тестов; ruff/mypy/node-check зелёные
- [x] Пуш пользователя → data-миграция применится на проде (локально в сидах нет dossier — на прод попадёт только после пуша) — применено (0014 на проде, карточка актуальна; `/api/projects/` — 8 проектов)

Закрыто 2026-10-11: прод подтверждён (тикет Dossier в `/api/projects/`, data-миграция 0014 применилась).

## Сопутствующее (не код)
- GitHub About пользователь поправил сам (description/homepage/topics + telegram)
- Косметические артефакты GitHub About: описание с хвостовой `;`, у homepage пробел — можно убрать вручную