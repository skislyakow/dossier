# 06: Визуальный редизайн секции Опыт

**What to build:** Посетитель читает Опыт (хронологию карьеры) в новом визуале: работа, проекты и текущий статус подаются современно и читаемо, на десктопе и мобильном. Данные и контракт не меняются — меняется только подача. Вывод экранирован.

**Blocked by:** 02 (Design-система и Signature-момент Hero).

**Status:** ready-for-human

- [x] Секция Опыт отрисована в новом стиле (данные/контракт не изменились)
- [x] Значения из данных экранированы при вставке в DOM
- [x] Секция читаема на мобильных
- [x] Существующие автотесты зелёные (25/25)
- [ ] Визуальная проверка на dev / в проде

## Comments

### Реализация (2026-10-09)

- **Решения до реализации** (подтверждены пользователем): формат — полная хронология (все элементы сразу); проекты (8 репозиториев) входят в строки секции (GLOSSARY «Опыт» = работы + проекты + статус; US#5 «длительность проектов»); клик по точке рельса → скролл к строке секции + подсветка; секция при раскрытии панелей НЕ скрывается (обычная страница, в отличие от detail-карточки из t10).
- **`templates/index.html`**: `<div class="tl-details" id="timeline-details">` → `<div class="experience" id="experience">`; позиция в `.content-body` та же (Projects → Опыт → Skills → Contact).
- **`static/js/timeline.js`**: добавлен `tlEsc()` (5 замен, включая атрибуты/URL); рендер секции одним `innerHTML`: метка `{ опыт: N }` (Fira Code, скобки — акцент, как у фильтров Projects) + `.exp-list` из всех слотов (prior → job → проекты → present), по строке на слот: `.exp-date` (моно) / `.exp-title` / `.exp-role` (job) / `.exp-desc` / `.exp-link` (job → hostname из `d.url`, проект → GitHub). `itemHtml`/detail-карточка/`scrollToDetails` удалены; `select()` теперь переключает `active` и на точке, и на строке секции; клик по точке — `scrollIntoView({ block: 'center' })` c `behavior` по `prefers-reduced-motion`. Контракт `/api/timeline/` не тронут (`ApiTimelineTest` зелёный).
- **`static/css/style.css`**: блок стилей `.tl-details*` (карточка + светлые оверрайды + мобилка) заменён на `.experience/.exp-*`: лента `border-left: 2px`, точки `::before` на линии с вариантами (prior — пунктир, job — акцент, present — залитая, active — ring через `--accent-ring`), строка — прозрачная карточка с hover-less подсветкой `active` (`color-mix` 7% акцента). Мобилка ≤1024px: `.hero-timeline { display: none }` остался один — секция видна. Из t10-правил удалён `body:has(...) .tl-details { display: none }` (см. комментарий в тикете 10), остаётся скрытие рельса + жёлоб.
- **Tests**: `test_section_order` → `id="experience"`; `test_timeline_rail_vertical` — мобилка прячет только рельс; `test_rail_and_timeline_hidden_while_panel_open` — без `.tl-details`; новый `test_experience_section_chronology_and_escapes` (контейнер, стили, `tlEsc`, запрет сырых конкатенаций `+ d.* +` и любых `tl-details`-ссылок). 25/25, ruff чисто.
- **Docs-sync**: AGENTS.md — буллет Timeline переписан, добавлен буллет «Опыт», ToDo про XSS сужен (timeline.js закрыт в этом тикете).
