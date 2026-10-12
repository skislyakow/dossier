# 01: Page-chrome — инлайн-скрипты index.html → модуль (кандидат 2 арх-ревью 2026-10-12)

**What to build:** Убрать 6 инлайн-IIFE из `templates/index.html` в модуль `static/js/page-chrome.js` (theme, acid-gradient ×2, reveal, back-to-top), contact-toggle — в `contact.js` (владелец секции), вторую реализацию reveal (`revealNow` в portfolio.js) заменить вызовом общей. Отчёт: `%TEMP%/opencode/architecture-review-2026-10-12.html` (карточка 2).

**Status:** ready-for-agent

Решения grilling (2026-10-12, все рекомендации приняты):
- Q1: новый `static/js/page-chrome.js` (IIFE как соседи), грузится последним после contact.js; util.js = абстрактные хелперы, chrome = DOM-поведение страницы.
- Q2: contact-toggle IIFE — в `contact.js` (паттерн portfolio/github: панель роутится владельцем секции), с сохранением UX (disclosurePanel + scrollIntoView через 150мс).
- Q3: reveal — один гард + два входа: `reveal.observeAll()` (загрузка, IntersectionObserver, `.reveal` в разметке) и `reveal.now(target)` (eager, после инъекции HTML — поведение текущего `revealNow` буквально). Один `prefersReducedMotion()`, один `classList.add('is-visible')`.
- Q4: контракт-тесты: в index.html остаётся ровно один инлайн-`<script>` (head-IIFE `window.getSkills` — кандидат 3, вне scope); строка `'prefers-reduced-motion'` в `static/js/` — только в util.js; page-chrome.js существует (reveal/theme/back-to-top/gradient); portfolio.js без `function revealNow(`; contact.js вайрит `contact-btn` через `disclosurePanel`; порядок загрузки contact < page-chrome; node --check.

## Scope
- `static/js/page-chrome.js` — новый: bindGradient (с гардом reduced-motion, раньше гард был только у hero), reveal {now, observeAll}, initTheme, initBackToTop; глобал `window.pageChrome`.
- `static/js/contact.js` — вайринг `#contact-btn` (disclosurePanel + scrollIntoView 150ms, verbatim UX).
- `static/js/portfolio.js` — удалить локальный `revealNow`, вызовы → `window.pageChrome.reveal.now(...)`.
- `templates/index.html` — удалить 6 инлайн-IIFE, добавить `<script js/page-chrome.js>` после contact.js; head-IIFE getSkills оставить.
- `main/tests/test_design.py` — обновить 3 теста (scroll_reveal_observer, reduced_motion_guards, portfolio_eager_reveal) + новый контракт `test_page_chrome_module`.
- AGENTS.md docs-sync (Structure-буллет про инлайн-скрипты + static/js); README 98→99.

## Микро-изменения поведения (осознанные)
- Portfolio-gradient: раньше mousemove биндился без reduced-motion-гарда (hero — с гардом). Единый `bindGradient` гардит оба: при reduced-motion `--mx/--my` больше не обновляются (анимации и так выключены).
- `prefers-reduced-motion` в html больше нет (guards через `prefersReducedMotion()` из util.js).

## AC
- [ ] `page-chrome.js`: theme/gradients/reveal/back-to-top, глобал `window.pageChrome`
- [ ] contact.js: клик по `#contact-btn` открывает/закрывает панель + scrollIntoView
- [ ] portfolio.js: без локального `revealNow`; вызовы через `pageChrome.reveal.now`
- [ ] index.html: 0 инлайн-IIFE кроме head getSkills; page-chrome.js после contact.js
- [ ] Тесты: обновить 3 + новый контракт; 100% зелёные
- [ ] AGENTS.md + README синхронизированы
- [ ] `./tools/gate.sh` зелёный; push; CI success; prod-проверка (тема, градиент, reveal, back-to-top, contact)

## Comments
