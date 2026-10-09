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
