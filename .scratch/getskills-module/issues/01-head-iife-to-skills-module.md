# 01: Убрать последний инлайн-скрипт index.html — getSkills в skills.js (кандидат 3 арх-ревью 2026-10-12)

**What to build:** Остался ровно один инлайн-`<script>` в `templates/index.html` (head-IIFE `window.getSkills` + глобал `__skillsPromise`). Единственный потребитель — skillс-секция (`static/js/skills.js:9`). Перенести кэшируемый fetch `/api/skills/` внутрь skills.js как локальную переменную модуля; `window.getSkills`/`window.__skillsPromise` и инлайн-скрипт удалить. Контекст: page-chrome Q4 отметил это как «кандидат 3, вне scope».

**Status:** in-progress

## Scope
- `static/js/skills.js` — локальный кэш promise `getSkills()` (fetch `/api/skills/`, catch → `{skills:[], categories:[]}`), без глобалов.
- `templates/index.html` — удалить head-IIFE (строки 25–34).
- `main/tests/test_design.py` — контракт: `getSkills`/`__skillsPromise` отсутствуют в html и module-scope JS; `count('<script>') == 0`; skills.js содержит `fetch('/api/skills/')`. Порядок/прочие контракты без изменений.
- AGENTS.md — буллет static/js: «инлайн-скриптов в index.html нет» + skills.js владеет fetch.

## AC
- [ ] `index.html`: 0 инлайн-`<script>` (только `type="application/ld+json"` + `src=`)
- [ ] `skills.js`: локальный `getSkills()` с кэшем; `window.getSkills`/`window.__skillsPromise` отсутствуют
- [ ] Тесты: обновлённый контракт зелёный (99)
- [ ] AGENTS.md синхронизирован
- [ ] `./tools/gate.sh` зелёный; push; CI success; прод-смок 35/35

## Comments