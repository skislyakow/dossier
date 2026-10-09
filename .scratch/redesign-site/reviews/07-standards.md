# Standards review - `907c27a...HEAD` (5b01842) - STANDARDS axis

Основание: AGENTS.md (docs-sync, data-migration pattern, Project overview, ToDo), GLOSSARY.md, `docs/agents/issue-tracker.md`, `docs/agents/triage-labels.md`; tooling (`ruff.toml`) — исключён, проверен чат-только. Проверено: `uv run ruff check .` чисто; `uv run manage.py test` 27/27 OK.

## (a) Documented-standard violations

1. **Docs-sync (AGENTS.md, Dev workflow: «обновить README и AGENTS.md»)** — AGENTS.md синхронизирован (3 ханка), README — нет. Judgement call: в «Возможности» не было контактного буллета вообще (не устарел, а отсутствовал), но Contact — заметная фича. → **Исправлено:** README.md добавлен буллет «Контакты — секция тремя крупными каналами…».
2. **issue-tracker.md (Status rules)** — после завершения `07-contact-three-channels.md` оставался `ready-for-agent`. Остаточный AC — визуальная проверка человеком → по triage-labels.md корректен `ready-for-human`. → **Исправлено:** статус обновлён.

Соответствия, подтверждённые: seed-паттерн миграции 0011 совпадает с AGENTS.md «Adding a project» (`get_or_create` по натуральному ключу + `RunPython` в обе стороны, cf. 0007/0008/0010) ✓; термин «Опыт» без дрейфа (GLOSSARY) ✓; `makemigrations --check` — No changes detected ✓.

## (b) Baseline smells - JUDGEMENT CALLS

- **Duplicated Code** — третья копия `esc()` в diff (вторая в том же файле): локальная `esc` в contact-IIFE (`index.html:241`) дублировала skills-IIFE (`index.html:208`). → **Исправлено:** обе локальные копии удалены; используется глобальный `esc` из `portfolio.js:20` (загружается на строке раньше обоих IIFE, plain `<script>` без defer/async → порядок исполнения гарантирован).
- **Duplicated Code** — пять-спановая метка `{ название: N }` собрана в двух местах diff (`timeline.js:76-78`, `index.html` contact-label). → **Отложено (сознательно):** общая сборка потребует нового util-модуля/скрипта (третья копия в skills-label живёт вне diff) — для одного шаблона из 5 спанов это Middle Man/Speculative Generality; CSS уже общий (`.sec-*`).
- **Repeated Switches + Mysterious Name** — диспетчеризация `item.type` в 4 хода (`kinds`/`icons`/`hrefFor`-каскад/`target`-тернарник), `var kinds` держал labels. → **Исправлено:** единая таблица `channels[type] = {label, icon, href(v), external}` — каскады и тернарник поглощены, имя честное.
- **Suppressed by repo standard:** shotgun surgery (8 файлов) — предписано правилом docs-sync + тестовых правил; source-string ассерты в `DesignSystemTest` — существующий репо-сийм (зафиксирован в spec Testing Decisions как документированное исключение).
