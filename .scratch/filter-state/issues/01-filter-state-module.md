# 01: Состояние фильтра портфолио — один владелец (кандидат 1 арх-ревью 2026-10-12)

**What to build:** Закрыть seam leak «Тег фильтра навыка» между skills.js и portfolio.js: единый модуль `static/js/filter-state.js` владеет filter-state (тег + роль), все источники эмитят через него, подсветка кнопок — у владельцев своей разметки. Отчёт: `%TEMP%/opencode/architecture-review-2026-10-12.html` (карточка 1).

**Status:** ready-for-human

Решения grilling (2026-10-12, все рекомендации приняты):
- Q1: модуль владеет **и тегом, и ролью** — единый state.
- Q2: UX открытия сохраняется: ручное открытие сбрасывает фильтр, клик по навыку при закрытой панели открывает её с фильтром (`openPortfolio({restore:true})`); `pendingTag` удаляется — модуль ничего не знает про панели.
- Q3: interface — subscribe-интерфейс `window.filterState = {get, setTag, setRole, clear, subscribe}`; no-op при неизменном значении (защита от лишних emit).
- Q4: инверсия — skills.js сам подписывается и сам переключает `.active` на своих кнопках; `syncSkillButtons` удаляется из portfolio.
- Q5: новый файл `static/js/filter-state.js` (IIFE как соседи), в index.html — сразу после util.js, до portfolio.js/skills.js; в util.js не сливать (там абстрактные утилиты, тут доменный state).
- Q6: тесты = контракт seam: наличие filter-state.js и его interface, отсутствие `__applyPortfolioTag`/`syncSkillButtons`/`#skills` в JS-модулях, порядок загрузки в html; node --check.
- Q7: один тикет, обычный конвейер (gate → code-review → push); GLOSSARY — термин «Состояние фильтра портфолио».

- [x] `static/js/filter-state.js`: get/setTag/setRole/clear/subscribe, no-op-guard, глобал `window.filterState`
- [x] skills.js: клик → `filterState.setTag`; subscribe + пост-рендер sync своих кнопок; глобал `__applyPortfolioTag` удалён
- [x] portfolio.js: state через filterState (role-чипы → setRole, ptag → setTag); subscriber рендерит/синхронит чипы; открытие закрытой панели при внешнем изменении — `openPortfolio({restore:true})`; удалены activeRole/activeTag/pendingTag/syncSkillButtons/window.__applyPortfolioTag
- [x] index.html: `<script js/filter-state.js>` после util.js
- [x] Тесты: контракт seam в test_design; старые greps заменены; 100% зелёные
- [x] AGENTS.md (static/js буллет + секция Skills) и GLOSSARY синхронизированы
- [x] `./tools/gate.sh` зелёный; push; CI success; prod-проверка (клик по навыку фильтрует, подсветка)

## Comments

### 2026-10-12 — реализация + ревью + деплой
- Гейт (по шагам gate.sh): ruff ✓, mypy 53 файлов ✓, pytest **98 passed** ✓, makemigrations --check ✓, node --check все `static/js/*.js` ✓, `migrate` (локальная БД отстала до 0023) + `audit_content` exit 0 (только W101) ✓.
- Коммиты: `36e292b` реализация → `9f4261e` правки по code-review → `1e4192e` отчёты. Фикс-поинт `fe5ace2`.
- Code-review (два агента): spec — conformant (все Q1–Q7, поведенческие ловушки закрыты); standards — 1 hard (glossary avoid «store» в тикете) + находки baseline. Все исправлены в `9f4261e`: dedupe `set(key,value)` в filter-state, rename `syncChips→syncActiveChips`, `#skills`-аssert только против portfolio, точная строка интерфейса и порядок `util<fs<portfolio` в тесте, README 97→98, «subscribe-интерфейс», AC-чекбоксы. Отчёты: `reviews/01-standards.md`, `reviews/01-spec.md`.
- Push `fe5ace2..1e4192e`; **CI run 247 = success** (гейт+деплой).
- Prod-верификация: `/static/js/filter-state.js` 200 с точным интерфейсом; порядок скриптов в `/` util<fs<portfolio ✓; `__applyPortfolioTag`/`syncSkillButtons`/`#skills` (portfolio) отсутствуют в отданном JS ✓; `tools/smoke.sh https://kislyakov.pro` — **32/32 ок**.
- Осталось: визуальная проверка пользователем (клик по навыку на закрытой панели открывает Projects с фильтром + подсветка кнопок; закрытие сбрасывает; ручное открытие без фильтра).
