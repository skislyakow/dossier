# Standards review — `88430dc...HEAD` (47571fd) — STANDARDS axis

Источники: AGENTS.md (docs-sync, Project overview, ToDo), GLOSSARY.md, `docs/agents/issue-tracker.md`, `docs/agents/triage-labels.md`, `docs/agents/domain.md`; tooling (`ruff.toml`) — пропущен как включённый в CI. Проверено: `uv run ruff check .` чисто; `uv run manage.py test` → 25/25 OK.

## (a) Documented-standard violations — HARD

1. **Docs-sync rule (AGENTS.md, Dev workflow §5: «обновить README и AGENTS.md»)** — README не попал в диф, хотя поведение сайта изменилось. README.md:20 всё ещё рекламирует удалённое поведение: `клик по точке открывает карточку`. Та же строка называет концепт **«Career timeline»**, нарушая GLOSSARY.md:23-25 («Опыт … _Avoid_: таймлайн, timeline») через domain.md:43 («Don't drift to synonyms the glossary explicitly avoids»). AGENTS.md синхронизирован; README — нет. → **Исправлено:** буллет переписан как «Опыт», клик по точке — переход к строке секции; в буллете админки «таймлайн» → «опыт».
2. **issue-tracker.md:11** («`done` … once all acceptance criteria are met and verified») — в тикете 10 остаётся `Status: done` с AC `[x]` про «карточка `.tl-details` … скрыта», хотя комментарий признаёт: AC отменён, правило удалено. Чекбокс противоречит коду; комментарий — не механизм отмены AC. → **Исправлено:** строка AC помечена зачёркиванием + явной пометкой «отменён тикетом 06».

Обработка тикета 06 соответствует стандарту: `ready-for-human` (triage-labels.md), визуальный AC не отмечен, `## Comments` добавлен в конец (issue-tracker.md:12).

## (b) Baseline smells — JUDGEMENT CALLS

- **Repeated Switches** — каскад по `slot.kind` повторяется в одном файле: `labelFor` (timeline.js:44-48) vs та же логика дат, переизложенная в `itemHtml` (53-55), плюс ветки role/link (56-66) и суффиксов (93-96). Хуже: две вычисления дат уже разошлись (`labelFor` берёт `dateRange.split(" — ")[0]`, `itemHtml` — полный диапазон). → карта `kind → {label, date, cls}`.
- **Duplicated Code** — `prefersReducedMotion()` (timeline.js:11) дублирует `portfolio.js:12 reducedMotion()` (тот же matchMedia-запрос, другое имя); повторный `getElementById("exp-"+id)` в `scrollToItem` (87), хотя `slot.itemEl` уже закэширован (82-84) и используется в `select` (128).
- **Mysterious/dead output** — `itemHtml` эмитит `.exp-name` (timeline.js:77) без CSS-правила; тест проверяет только `.exp-label/.exp-list/.exp-item`.
- Minor: `assertIn('initRailMode', js)` (tests.py:165) — забота рельса, оказавшаяся в `test_experience_section_chronology_and_escapes`.

### Вердикт по судейским вызовам (принято / исправлено)

- **Исправлено:** `scrollToItem` → `slot.itemEl` (без повторного query); атрибут `data-slot` удалён (нигде не читается, speculative generality); `assertIn('initRailMode', js)` перенесён в rail-тест; `.exp-label` на токен `--text-secondary`.
- **Принято:** дрейф дат `labelFor`/`itemHtml` намеренный — компактная подпись рельса («Январь 2026») vs полный диапазон в строке секции; `prefersReducedMotion` vs `reducedMotion` — кросс-файловое дублирование без сборщика (паттерн уже есть в inline-скриптах index.html); `.exp-name` без CSS зеркалит существующий `.cat-name` в фильтрах Projects; source-substring тесты — документированный seam репозитория (DesignSystemTest), он же упраздняет оговорку спеки «JS/CSS автотестов нет».
