# 01 — Spec review (`fe5ace2...9f4261e`)

Агент: Spec-ось code-review (research only). Спека: `.scratch/filter-state/issues/01-filter-state-module.md` (Q1–Q7) + `.scratch/redesign-site/spec.md` (t11) + GLOSSARY «Состояние фильтра портфолио».

## Вердикт: spec-conformant

Все восемь grilling-решений реализованы буквально; scope creep отсутствует (все 8 файлов диффа = пункты тикета).

- **Q1** — тег+роль в одном модуле (`filter-state.js:6-7`).
- **Q2** — `pendingTag` удалён; ручное открытие чистит (`portfolio.js`), навык на закрытой панели открывает с фильтром через `openPortfolio({restore:true})`; в модуле ноль ссылок на панели.
- **Q3** — интерфейс точный, no-op-guard во всех сеттерах.
- **Q4** — skills.js владеет своими кнопками; `syncSkillButtons` удалён; в portfolio нет `#skills`.
- **Q5** — новый IIFE-файл, порядок в `index.html` util → filter-state → portfolio/skills; в util.js не свёрнут.
- **Q6** — `test_filter_state_module_seam`, старые greps заменены.
- **Q7** — тикет в новом трекере, термин в GLOSSARY.

**Ловушки поведения — закрыты**: `disclosurePanel.close()` вызывает `set(false)` до `onClose`; subscriber открывает панель только при `state.tag` непустом → close→clear не переоткрывает. Клик по role/ptag при открытой панели рендерит через subscriber. t11 AC (AND с ролью, empty-state, сброс при закрытии) — сохранены.

**Checks**: ruff / mypy / pytest 98 / makemigrations / node --check — зелёные после правок.

## Найдено (minor) → disposition

1. **Load-order тест неполный** (не проверял `util < filter-state`). → **Исправлено в `9f4261e`**: добавлен `assertLess(util, filter-state)`.
2. **Интерфейс «stringly»** (`'get,'`). → **Исправлено**: точная строка `window.filterState = { get, setTag, setRole, clear, subscribe };`.
3. **AGENTS Skills-буллет потерял факт про `active`**. → **Исправлено**: «кнопка совпавшего тега — `.active`».

Примечание к п.2: no-op-guard остаётся семантическим (поверхностный grep не доказывает поведения) — покрыто ревью-агентом чтением кода, unit-теста на emit-шум не заводим (портфейльный проект, seam-контракт достаточен по Q6).
