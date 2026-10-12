# 01: Состояние фильтра портфолио — один владелец (кандидат 1 арх-ревью 2026-10-12)

**What to build:** Закрыть seam leak «Тег фильтра навыка» между skills.js и portfolio.js: единый модуль `static/js/filter-state.js` владеет filter-state (тег + роль), все источники эмитят через него, подсветка кнопок — у владельцев своей разметки. Отчёт: `%TEMP%/opencode/architecture-review-2026-10-12.html` (карточка 1).

**Status:** ready-for-agent

Решения grilling (2026-10-12, все рекомендации приняты):
- Q1: модуль владеет **и тегом, и ролью** — единый state.
- Q2: UX открытия сохраняется: ручное открытие сбрасывает фильтр, клик по навыку при закрытой панели открывает её с фильтром (`openPortfolio({restore:true})`); `pendingTag` удаляется — модуль ничего не знает про панели.
- Q3: interface — subscribe-store `window.filterState = {get, setTag, setRole, clear, subscribe}`; no-op при неизменном значении (защита от лишних emit).
- Q4: инверсия — skills.js сам подписывается и сам переключает `.active` на своих кнопках; `syncSkillButtons` удаляется из portfolio.
- Q5: новый файл `static/js/filter-state.js` (IIFE как соседи), в index.html — сразу после util.js, до portfolio.js/skills.js; в util.js не сливать (там абстрактные утилиты, тут доменный state).
- Q6: тесты = контракт seam: наличие filter-state.js и его interface, отсутствие `__applyPortfolioTag`/`syncSkillButtons`/`#skills` в JS-модулях, порядок загрузки в html; node --check.
- Q7: один тикет, обычный конвейер (gate → code-review → push); GLOSSARY — термин «Состояние фильтра портфолио».

- [ ] `static/js/filter-state.js`: get/setTag/setRole/clear/subscribe, no-op-guard, глобал `window.filterState`
- [ ] skills.js: клик → `filterState.setTag`; subscribe + пост-рендер sync своих кнопок; глобал `__applyPortfolioTag` удалён
- [ ] portfolio.js: state через filterState (role-чипы → setRole, ptag → setTag); subscriber рендерит/синхронит чипы; открытие закрытой панели при внешнем изменении — `openPortfolio({restore:true})`; удалены activeRole/activeTag/pendingTag/syncSkillButtons/window.__applyPortfolioTag
- [ ] index.html: `<script js/filter-state.js>` после util.js
- [ ] Тесты: контракт seam в test_design; старые greps заменены; 100% зелёные
- [ ] AGENTS.md (static/js буллет + секция Skills) и GLOSSARY синхронизированы
- [ ] `./tools/gate.sh` зелёный; push; CI success; prod-проверка (клик по навыку фильтрует, подсветка)

## Comments
