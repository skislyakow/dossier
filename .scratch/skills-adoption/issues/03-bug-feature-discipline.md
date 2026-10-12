# 03: Дисциплина багов и фич — diagnosing-bugs + tdd (указатели в AGENTS)

**What to build:** Принять скиллы `diagnosing-bugs` (тяжёлые баги) и `tdd` (кодовые фичи) как рабочий процесс, зафиксировав короткие указатели в `AGENTS.md ## Dev workflow` (в стиле `writing-for-agents` — 1–2 строки на скилл, без дублирования тела скиллов).

**Blocked by:** None.

**Status:** done

## Scope
- AGENTS `## Dev workflow`: тяжёлый баг → цикл `diagnosing-bugs` (сначала tight feedback loop, потом гипотезы); кодовая фича → `tdd` (согласовать seams, red→green), словарь — `codebase-design`.
- Код не трогаем — только доки.

## AC
- [x] Указатели добавлены в AGENTS, формулировки короткие и триггерные
- [x] `./tools/gate.sh` зелёный; push; CI success

## Comments

### 2026-10-12 — реализация
- Коммит `583a3a4`: строка-указатель в `AGENTS.md ## Dev workflow`, код не менялся. CI success. Тикет → `done`.
