# 03: Каркас страницы: chrome и marquee

**What to build:** Сайт выглядит цельным от шапки до подвала: переключатель темы, кнопка back-to-top, hover-подписи соцсетей и GitHub stats toggle переработаны под новый дизайн-язык. Между секциями бегёт одна marquee-строка с технологиями — ритм и дополнительный контекст стека без отдельной секции.

**Blocked by:** 02 (Design-система и Signature-момент Hero).

**Status:** ready-for-human

- [x] Переключатель темы, back-to-top, соц-ссылки отрисованы в новом стиле, aria-labels сохранены
- [x] GitHub stats toggle работает без изменений контракта `/api/github/` и выглядит в новом стиле
- [x] Одна marquee-строка технологий между секциями: CSS-анимация, пауза при prefers-reduced-motion
- [x] Существующие автотесты зелёные (18/18); визуальная проверка на dev — за Сергеем (после деплоя)

## Comments

### 2026-10-09: реализация

**Chrome под новый язык:**
- Соц-ссылки и back-to-top: круглые `border-radius: 50%` → квадратные `2px` (brutalist-рамка), расширение по hover (фича «hover-подписи: иконка едет, текст выезжает») сохранено.
- Хардкод-цвета заменены токенами: `#a1a1aa`/`#666` → `var(--text-secondary)`/`var(--text-muted)`.
- Единый акцент: убран telegram-blue `#0088cc` (и hover-тень `rgba(0,136,204,…)`) — все hover'ы соц-ссылок теперь `color: var(--accent)` + `background: var(--accent-soft)`.
- Подписи соц-ссылок: uppercase + `letter-spacing: 0.12em` (editorial).
- GitHub stats card (`.gh-card`): hover-граница `--border` → `--accent`; контракт `/api/github/` не тронут.
- aria-labels сохранены (`GitHub`, `Telegram`, `Переключить тему`, `Back to top`), проверяется тестом.

**Marquee:**
- Размещение: между `.hero` и `.content-body` (page chrome, всегда виден), `aria-hidden="true"`.
- Разметка: два одинаковых `.marquee-group` → бесшовный цикл `translateX(-50%)`, `animation: marquee 32s linear infinite`.
- Контент: статичный курируемый список технологий (Python, Django, DRF, FastAPI, PostgreSQL, Redis, Docker, Linux, systemd, aiogram, SQLAlchemy, Git) — декоративный chrome, не CMS (в отличие от секции Skills).
- Пауза: `@media (prefers-reduced-motion: reduce) { .marquee-track { animation: none; } }`.
- Разделитель `///` — акцентным цветом.
- Открытый вопрос для глаз-чека: справа текст marquee уходит под fixed-рельс таймлайна (full-bleed, как в других marquee). Если мешает — добавить правый жёлоб на `min-width: 1025px`.

**Тесты:** `test_page_chrome_marquee` (наличие/позиция разметки, keyframes, пауза reduced-motion), `test_page_chrome_uses_single_accent` (нет `#0088cc`, aria-labels).

### 2026-10-09: code-review (`c270294...HEAD`)

Отчёты: `reviews/03-standards.md`, `reviews/03-spec.md`.

**Исправлено:**
- HARD (standards): `Status: done` не значился в словаре трекера → задокументирован как терминальный статус в `docs/agents/issue-tracker.md`.
- scope creep (spec): `.social-label` вернул `font-size: 0.85rem` (было ужато до 0.75 — не просилось; uppercase + letter-spacing остаются).
- spec #22 (весь текст на русском): `aria-label="Back to top"` → `"Наверх"` (+ тест).
- хрупкость тестов: `animation: marquee` без пиннинга длительности; `aria-hidden` заскоуплен на `.marquee`.

**Принято как есть:**
- Позиция marquee — Hero→`.content-body` (секции тумблятся, это единственный всегда видимый шов); отмечено на глаз-чек.
- Статичный список технологий в marquee (декоративный chrome, не CMS).
- Дублирование accent-hover-правил — селекторы равной специфичности завязаны на порядок; консолидация вслепую рискованна (прецедент t02 с дублем reduced-motion guard).
- `.gh-card:hover #fafafa` и синий `--accent` в light — by design (карточка белая в обеих темах; лайм-пересмотр light в секционных тикетах).
- AC2: контракт `/api/github/` уже под тестом `ApiGithubTest`.
