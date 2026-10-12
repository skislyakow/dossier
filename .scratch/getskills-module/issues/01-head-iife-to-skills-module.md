# 01: Убрать последний инлайн-скрипт index.html — getSkills в skills.js (кандидат 3 арх-ревью 2026-10-12)

**What to build:** Остался ровно один инлайн-`<script>` в `templates/index.html` (head-IIFE `window.getSkills` + глобал `__skillsPromise`). Единственный потребитель — skillс-секция (`static/js/skills.js:9`). Перенести кэшируемый fetch `/api/skills/` внутрь skills.js как локальную переменную модуля; `window.getSkills`/`window.__skillsPromise` и инлайн-скрипт удалить. Контекст: page-chrome Q4 отметил это как «кандидат 3, вне scope».

**Status:** done

## Scope
- `static/js/skills.js` — локальный кэш promise `getSkills()` (fetch `/api/skills/`, catch → `{skills:[], categories:[]}`), без глобалов.
- `templates/index.html` — удалить head-IIFE (строки 25–34).
- `main/tests/test_design.py` — контракт: `getSkills`/`__skillsPromise` отсутствуют в html и module-scope JS; `count('<script>') == 0`; skills.js содержит `fetch('/api/skills/')`. Порядок/прочие контракты без изменений.
- AGENTS.md — буллет static/js: «инлайн-скриптов в index.html нет» + skills.js владеет fetch.

## AC
- [x] `index.html`: 0 инлайн-`<script>` (только `type="application/ld+json"` + `src=`)
- [x] `skills.js`: локальный `getSkills()` с кэшем; `window.getSkills`/`window.__skillsPromise` отсутствуют
- [x] Тесты: обновлённый контракт зелёный (99)
- [x] AGENTS.md синхронизирован
- [x] `./tools/gate.sh` зелёный; push; CI success; прод-смок 35/35 — **прод НЕ применился**: тихий сбой деплоя (см. ниже)

## Comments

### 2026-10-12 — реализация
- Коммит `81e33bc`. Гейт зелёный (99 тестов), CI `81e33bc` = success, локально смоук 35/35 + визуальный регресс 14/14.
- **Обнаружен тихий сбой авто-деплоя**: джоба `deploy` рапортует success, но прод отдаёт старый `skills.js` (`Last-Modified` = время деплоя `321018d`), инлайн `window.getSkills` в `/` остался. Причина: `appleboy/ssh-action` без `script_stop`/`set -e` — упавшая команда (вероятно `git pull`) не валит джобу. Прод-статик байт-в-байт с репо совпадает везде, кроме `skills.js`.
- Фикс — в коммите с харднингом `deploy.yml` (`script_stop` + `set -euo pipefail` + `git checkout -f -B main origin/main` + джоба `verify`: smoke + байт-сверка `static/**`).

### 2026-10-12 — прод-деплой починен, тикет закрыт
- Харднинг `f746a91` сразу проявил истинную причину: `deploy` упал с `E: Unable to locate package libpangoft2-0` — пакет weasyprint называется `libpangoft2-1.0-0`. Пакетный шаг падал **всегда**, но игнорировался; вместе с ним игнорировался и упавший `git pull` (отсюда старый код).
- `458f5b0` — исправлено имя пакета. CI run `458f5b0`: **check success, deploy success, verify success**.
- Прод-верификация: `skills.js` содержит `let skillsPromise` ✓, `/` без инлайн `window.getSkills` ✓, `Last-Modified 2026-10-12 16:22:23 GMT` ✓, `tools/smoke.sh https://kislyakov.pro` 35/35 (в джобе `verify`).
- Тикет → `done`.