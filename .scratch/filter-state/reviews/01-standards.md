# 01 — Standards review (`fe5ace2...9f4261e`)

Агент: Standards-ось code-review (research only). Фикс-поинт `fe5ace2`, коммиты `36e292b` (реализация) + `9f4261e` (правки).

## Документированные стандарты

**HARD — `docs/agents/domain.md` + GLOSSARY `_Avoid_: store`**: тикет `01-filter-state-module.md` использовал «subscribe-store» — термин из avoid-листа нового правила. → **Исправлено в `9f4261e`** («subscribe-интерфейс»).

**JUDGEMENT — issue-tracker.md (Status/checklist)**: кодовые AC остались `- [ ]` при готовом коде. → **Исправлено в `9f4261e`** (первые 6 AC отмечены; gate/push/CI/prod ещё открыты — Status остаётся `ready-for-agent` до prod-верификации).

**JUDGEMENT — AGENTS.md Dev workflow §10 (docs-sync)**: README фиксировал «97 тестов», после `test_filter_state_module_seam` их 98. → **Исправлено в `9f4261e`** (README: бейдж, CI/CD-буллет, счётчик).

**Compliant, verified**: ADR-0001 — клиент не считает размеры/частоты (только `visible` для empty-state); порядок скриптов util → filter-state → portfolio/skills; тест в `test_design.py`; термин GLOSSARY консистентен.

## Baseline-смеллы (judgement calls)

- **Duplicated Code** — идентичные `setTag`/`setRole`. → **Исправлено в `9f4261e`**: приватный `set(key, value)`, публичный интерфейс не изменился.
- **Duplicated Code (suppressed)** — `syncActiveChips` (бывш. `syncChips`) vs `skills.syncButtons` повторяют форму subscribe-toggle, но AGENTS.md-mandated («portfolio чужую разметку не трогает») → репо переопределяет baseline.
- **Mysterious Name (weak)** — `syncChips` не отражал `.ptag`. → **Исправлено**: переименован в `syncActiveChips`.
- **Speculative Generality (weak)** — `subscribe()` возвращал unsubscribe-closure, которой никто не пользуется. → **Исправлено**: возврат удалён (Q3-интерфейс не включает unsubscribe).
- **Test over-reach** — `assertNotIn('#skills', skills_js)` проверял правило владения portfolio против чужого файла (skills.js законно референсит свой контейнер). → **Исправлено**: `#skills` проверяется только против `portfolio_js`.
