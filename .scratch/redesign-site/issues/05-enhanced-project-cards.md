# 05: Усиленные карточки Projects

**What to build:** Рекрутер читает каждый Проект как Усиленную карточку: таглайн, 3–4 конкретных буллета результата, динамические бейджи и ссылки — всё на одной карточке, без перехода в репозиторий. При скролле карточки появляются стаггером, при наведении мягко реагируют (magnetic). Все внешние данные экранируются при вставке.

**Blocked by:** 02 (Design-система и Signature-момент Hero).

**Status:** ready-for-human

- [x] Карточки отрисованы по формату Усиленной карточки: таглайн + буллеты + бейджи + ссылки
- [x] Значения из API экранируются при вставке в DOM (innerHTML- XSS в рендере проектов закрыт)
- [x] Magnetic-hover умеренный и отключается при prefers-reduced-motion
- [x] Stagger-reveal карточек при скролле
- [x] Декоративные «призраки» в карточках (`.portfolio-ghost-skill` + `ghostFloat`) удалены — спека: призраки выпилены целиком
- [x] Контракт `/api/projects/` не изменился; автотесты зелёные (23/23)
- [ ] Визуальная проверка на dev

## Comments

### Реализация (2026-10-09)

- **Карточка получила поверхность.** Найдено при реализации: `.portfolio-preview-body` был `transparent`, а весь текст/бейджи карточки используют `--text-card*` (тёмные токены для светлых карточек) — в тёмной теме заголовок проекта (`--text-card` #2a241f на #0a0a0a) фактически нечитаем, бейджи-«фишки» висели на чёрном фоне. Добавлена поверхность по рецепту `.gh-card`: `background: var(--bg-card)` + `backdrop-filter: blur(4px)` + `border: 1px solid var(--border)` + `border-radius: 12px`; в light-теме — `#ffffff`. Так `--text-card*` стал работать как задумано.
- **Экранирование**: в `static/js/portfolio.js` добавлен `esc()` — титул, таглайн, роль, языки, буллеты, бейджи (label/value), ссылки (url/title), `data-repo`/`data-role`, скриншот; lookup иконки — через `hasOwnProperty` (без цепочки прототипов). `renderProjectMedia` больше не принимает `skills` → из `Promise.all` убран лишний `window.getSkills()`.
- **Stagger-reveal**: элементы карточки/списка получают `class="reveal"` + `style="--i: N"`; `revealIn(root)` создаёт свой `IntersectionObserver` (`threshold: 0.1`) и вызывается после первого рендера и после переключения проекта. Сдвиг — новый правило `.portfolio .reveal { transition-delay: calc(var(--i, 0) * 70ms) }` (специфика выше, чем у `.portfolio-list-item`, чей `transition: all` обнулял бы задержку). При `prefers-reduced-motion` — `is-visible` ставится синхронно, задержка 0.
- **Magnetic**: `initMagnetic(#portfolio)` на `pointermove` (только `pointer: fine`, только если не reduced-motion) ставит `--mag-x/--mag-y` ≤ 6px; CSS — `transform: translate3d(...)` на `.portfolio-preview-body` с плавным `transition`. Хендлер glow (`--mx/--my` в %, `::before` секции) не тронут.
- **Призраки удалены**: `.portfolio-ghost-skill`, `@keyframes ghostFloat` (блок ушёл из `style.css` целиком, включая light-override). Placeholder теперь — статичная монограмма проекта (первая буква названия) + `owner/repo` на лаймовом градиенте с тонкой сеткой, без анимаций.
- **Tests**: `test_enhanced_card_format_and_escapes` + `test_enhanced_card_surface_and_motion_guards` (23/23). Контракт `/api/projects/` не менялся — `ApiProjectsEnrichTest` зелёный.
- **Docs-sync**: AGENTS.md (буллеты Enhanced-карточки + placeholder, убран устаревший «Role-based placeholder themes», ToDo про XSS сужен до timeline/github/contact), README (буллет Портфолио).

### Правки по code-review (2026-10-09)

- **Magnetic → на саму карточку**: `bindMagnetic(.portfolio-preview-body)` вместо слушателя на всей секции (US#21 — hover на карточке); `--mag-x/--mag-y` ставятся на карточке, считается от её rect; биндится при первом рендере и при переключении проекта.
- **Утечка задержки в hover**: `.portfolio .reveal { transition-delay }` перебивал `transition: all` у `.portfolio-list-item` — hover-переходы тормозили до ~0.7 c. Решение: у кнопки списка свой `transition`, а `.reveal` перенесён на вложенный `<span>` (+ `display: block`), задержка действует только на появление.
- **Стаггер**: последовательная нумерация `--i` 0…8 без коллизий, шаг 60ms.
- **`prefers-reduced-motion` в рантайме**: `MOTION_MQ.matches` читается в момент использования (смена настройки учитывается).
- **`projectKey()`** — убраны тройные дубли `(repo && repo.full_name) || title`.
- **Тесты**: узкие запреты (`portfolio-ghost-skill`, `ghostFloat`) вместо общего `ghost`; добавлен запрет на сырые интерполяции API-значений.
- **Статус 04**: чекбокс визуальной проверки отмечен (пользователь подтвердил).
