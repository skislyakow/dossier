# 01 — Spec review page-chrome (`d2ffa16...9eec86c`)

Агент: Spec-ось code-review (research only). Спека: `.scratch/page-chrome/issues/01-inline-scripts-to-module.md` (Q1–Q4, Scope, микро-изменения).

## Вердикт: PASS с 2 minor-заметками

- **Q1** — `page-chrome.js` создан, грузится последним ✓
- **Q2** — contact-toggle в `contact.js`, UX verbatim (включая `scrollIntoView` 150ms) ✓
- **Q3** — два входа `reveal.now`/`reveal.observeAll`, гард `prefersReducedMotion()` из util, поведение eager-пути буквально ✓
- **Q4** — ровно один инлайн `<script>` (head `getSkills`, вне scope); `'prefers-reduced-motion'` в `static/js/` только в util.js; контракт-тест `test_page_chrome_module` ✓

**Ловушки (все verified)**: `#back-to-top` (index.html:134) до скриптов (139–146) ✓; нет parse-time доступа к `pageChrome` (portfolio вызывает только внутри `openPortfolio`; `subscribe` не нотифицирует при регистрации) ✓; `revealObserveAll()` один раз при парсинге, threshold 0.15, reduced-motion → immediate ✓; `initTheme()` body-end, как раньше ✓.

## Найдено

1. **F1 (minor, scope creep)** — правка статуса filter-state-тикета заехала этим коммитом. Docs-only bookkeeping → отмечено в комментарии тикета, не исправлялось (история).
2. **F2 (minor, Q3 буквально)** — «один `classList.add('is-visible')`» = 3 сайта в `page-chrome.js` (строки 19/26/32) и 2 вызова `prefersReducedMotion()`. Все внутри одного владельца, до диффа тоже было 3 → интент «один модуль-владелец» выполнен; уточнено в комментарии тикета.
3. **F3 (negligible)** — `if (!root) return;` в новом `revealNow` (старый бросал на null) → занесено в комментарий тикета.

AC1–AC6 по факту выполнены → отмечены; AC7 (gate/push/CI/prod) — до деплоя.
