# 11: Фича: кликабельные навыки — фильтр списка проектов

**What to build:** Клик по навыку в секции Skills открывает секцию Projects и фильтрует список по соответствующему тегу (пусто у навыка → по имени навыка). Нет совпадений — явный empty-state. Фильтр — AND с фильтром по роли, сбрасывается при закрытии панели.

**Blocked by:** 09 (Облако тегов), 10 (Баг невидимого списка — общий каркас `applyFilters`).

**Status:** dev-done (пуш пользователем + проверка проде)

- [x] Модель: `Skill.filter_tag` (CharField 50, blank) — тег проекта для клика-фильтра; пусто → имя навыка. API `/api/skills/` возвращает `filter_tag` для всех навыков
- [x] Миграция `0013_skill_filter_tag.py`: `AddField` + `RunPython(seed, rollback)`; `FILTER_TAG_BY_NAME` (алиасы: Telegram Bot API→Telegram, vk_api→VK, VK API→VK); `TAGS_BY_REPO` — теги 5 таглесс-проектов (opencode-py, ferma, devman-bot, dossier, online_library), выведены из README на GitHub, update-only по `repo` (пропуск отсутствующих → локально no-op)
- [x] Admin: `SkillAdmin.list_display` += `filter_tag` (поле auto в форме)
- [x] Шаблон skills: рендер навыков `<button type="button" class="tag tag-{size}" data-skill data-filter-tag>`, делегирование клика по контейнеру → `window.__applyPortfolioTag(data-filter-tag || data-skill)`
- [x] `portfolio.js`: модульные `activeRole/activeTag/pendingTag/portfolioMeta(Map)`, `applyFilters()` + `portfolio-empty` (текст через `textContent`, сообщение по «тегу»/«роли»), `syncSkillButtons()`, `activateProjectTag()`; `window.__applyPortfolioTag` — три ветки (панель закрыта → открыть + pendingTag после рендера; панель открыта+отрендерена → применить сразу); закрытие панели сбрасывает фильтры и `active`-состояния
- [x] CSS: `.skills-cloud .tag` — кнопочный reset (`appearance:none; background:none; border:0; cursor:pointer`), `.skills-cloud .tag.active` — лаймовый + bold; `.portfolio-empty` (grid-column 1/-1, моно, muted)
- [x] Тесты: `ApiSkillsTest` — `filter_tag` в API и значения; `test_skills_are_clickable_filter_buttons` (кнопки, data-атрибуты, `window.__applyPortfolioTag` в html+JS, CSS-reset/cursor, `.portfolio-empty`); `MigrationSkillFilterTagSeedTest` — idempotent `seed(apps, None)`, алиасы навыков, теги по `repo` (33/33 с тикетом 10)
- [x] Полный гейт зелёный: 33/33 теста + ruff + node --check + makemigrations --check
- [x] Docs-синк: AGENTS.md (overview — кликабельные навыки, Skill-model `filter_tag`, миграция 0013, `/api/skills/` включает `filter_tag`); GLOSSARY.md — «Тег фильтра навыка»

- [ ] Проверка на проде после пуша: клик по навыку открывает Projects с отфильтрованным списком; навык без совпадений → empty-state; сброс при закрытии; на проде у 5 новых проектов появились теги в облаке

Коммит: `023b2ce t10+t11: баг-фикс reveal списка + кликабельные навыки — фильтр проектов`