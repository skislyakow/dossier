# 04: Категории навыков: schema → API → секция Skills

**What to build:** Посетитель видит навыки, сгруппированные по Категориям навыка (Backend / Web / DevOps / Bots & Integrations / Tools) — сканирует по нужной зоне за секунду. Админ при добавлении навыка выбирает Категорию; существующие 36 навыков уже распределены. Путь полный: схема → миграция → админ → API → секция UI → тесты.

**Blocked by:** 02 (Design-система и Signature-момент Hero).

**Status:** ready-for-human

- [x] У Skill есть поле `category` с choices по пяти Категориям, отображается в админке
- [x] Обратимая data-migration распределяет существующие 36 навыков по Категориям (паттерн `0008`)
- [x] `/api/skills/` отдаёт `category`
- [x] Секция Skills — сетка, сгруппированная по Категориям; пустые Категории не показываются
- [x] Curly-формат облака (`{ skill }` вокруг каждого навыка) убран — спека: «убирается… облако навыков в curly-формате»
- [x] Тесты: JSON-контракт `/api/skills/` с `category` + рендеринг групп; существующие автотесты зелёные (21/21)
- [ ] Визуальная проверка на dev / в проде

## Comments

### Реализация (2026-10-09)

- **Schema**: `main/models.py` — `Skill.CATEGORY_CHOICES` + `Skill.category` (`max_length=10`, `default='tools'`). Виден в админке: `list_display = ['icon_display', 'name', 'category', 'size']`, `list_filter = ['category', 'size']`.
- **Migration**: `main/migrations/0010_skill_category.py` — `AddField` + `RunPython(assign_categories, reset_categories)`. Распределение по словарю `CATEGORY_BY_NAME` (по `name`); навык со старым/неизвестным именем → `tools` (default). Обратно — `reset_categories` (все в `tools`), сам столбец убирает реверс `AddField`. Проверено: `migrate main 0009` → `migrate main` — категории переназначаются.
- **API**: `main/views.py` `api_skills` → `{'name', 'category', 'size', 'icon'}`.
- **UI**: `templates/index.html` (inline script) — группировка по пяти категориям в фиксированном порядке, пустые группы пропускаются; разметка `.skill-group` / `.skill-group-title` / `.skill-group-items`.
- **CSS**: `static/css/style.css` — `.skills-cloud` стал grid (`repeat(auto-fit, minmax(220px, 1fr))`), добавлены `.skill-group*`; `.tag::before/::after` (curly), `.hero .tag` и их hover/light-правила удалены.
- **Tests**: `ApiSkillsTest` (контракт `category` + валидные choices) + `test_skills_section_grouped_by_category` + `test_skills_curly_cloud_removed`.
- **Follow-up**: прод-навыки, имен которых нет в `CATEGORY_BY_NAME`, после деплоя попадут в Tools — нужно просмотреть `/api/skills/` в проде и либо поправить имена, либо распределить вручную в админке.
- **Conflict note**: тикет 09 (облако тегов Проектов) опирался на переиспользование curly-компонента `.tag` — тикет 04 убрал curly из `.tag`, поэтому у 09 свой класс/разметка.
