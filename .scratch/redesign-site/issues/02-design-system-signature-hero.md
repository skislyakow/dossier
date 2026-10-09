# 02: Design-система и Signature-момент Hero

**What to build:** Посетитель получает первое впечатление за 3 секунды: имя и специальность крупной типографикой во всю ширину экрана, появляющиеся при скролле (Signature-момент), под ними строка позиционирования «Python-разработчик: автоматизация, Telegram-боты и веб на Django». Сайт обретает новый визуальный язык: монохром + кислотный лайм `#CDFF50`, дефолт — тёмная тема, приглушённый курсорный градиент.

**Blocked by:** 01 (Prefactor: выпилить hero-декор и двухколоночность).

**Status:** done

- [x] Токены дизайна заданы CSS-переменными: акцент `#CDFF50` (запасной оранжевый включается правкой одного токена), монохромная палитра, типографическая шкала
- [x] Hero: oversized имя/роль во всю ширину + scroll-reveal через IntersectionObserver
- [x] Строка позиционирования под именем
- [x] Курсорный градиент приглушён и отключается при prefers-reduced-motion
- [x] Дефолт тёмная тема; светлая тема работает переключателем
- [x] Таймлайн: вертикальный рельс справа в hero, точки prior → job → проекты → present, карточки по клику
- [x] Рельс закреплён (`position: fixed`): виден на всём скролле; в hero — с подписями дат, вне hero — компакт (полоса 48px, подписи по наведению); контент не перекрыт (правый жёлоб у `.portfolio`, `back-to-top` разведён)
- [x] Тип `prior` в TimelineItem: сеет до-2026 ИТ-запись, локально сеются job/present (рендер сломан без них)
- [x] Рельс скрыт ≤1024px; задержка `3600ms` убрана; скролл идёт на карточку деталей
- [x] Существующие автотесты зелёные (новые: API timeline + rail-CSS); визуальная проверка на dev (headless-замеры; глаз-чек — после деплоя)

**Notes:**
- Тесты зелёные (13/13), CI gate зелёный, деплой выполнен (`9bc3da6` + follow-ups `1046c09`); визуальная проверка на проде — ждём.
- **Scope bump по согласованию:** глобальная миграция legacy-золота `#e4b592` → токены акцента (`6366415`, ~60 мест): на тёмном канвасе/для фонов — `var(--accent)` (лайм; в light-теме автоматически синий), для текста/границ на белых карточках — `--accent-on-card` (`color-mix(accent 50%, black)`, AA-контраст). Отсюда секционные тикеты 04–07 начинают с чистого монохрома+лайма вместо золота.
- Реализация: `:root`-токены (`--accent`/`--accent-soft`/`--accent-ring`/`--accent-faint` через `color-mix` — правка одного `--accent` меняет всё, проверяется тестом), `--text-card*` для текста на белых карточках, `--type-scale-*` (пока применяются в hero; секции подключают шкалу в 03–07), светлая тема сохраняет прежнюю палитру (`--page-bg: #f5f0eb`, синий акцент) — её редизайн не в этой задаче.
- code-review (fixed point `0111982`): отчёты в `reviews/02-standards.md`, `reviews/02-spec.md`; исправлено: контраст текста на карточках, «один токен для акцента», приглушение градиента, docs-sync AGENTS.md; принято как есть: дубль guard'а reduced-motion (cross-script coupling хуже), масштабирование токенов на секции (03–07), сохранение светлой палитры (03–07), substring-тесты (согласованный test seam).

## Comments

### 2026-10-08: план «вертикальный рельс таймлайна + честный контент до-2026»

**Контекст от Сергея (штурм по таймлайну):**
- Нарратив честный, без фейков: до 2026 — работа в ИТ в других профилях (не программирование); с января 2026 — разработка (EFKO, стаж сейчас ~10 мес); pet-проекты — это учёба (июль/август 2026).
- Рельс в hero — **вертикальный, справа** (решено).
- Строка «Опыт…» в hero-text — **пока не нужно**. Пометки «pet-проект» в описаниях — **пока не нужно**. Бейджи-хайлайтер (вчерашний вопрос) — пропущен.
- Контент job-строки взять с https://github.com/skislyakow (company: EFKO, bio: Python Fullstack · Django/FastAPI/DRF/PostgreSQL/Docker · Bots/OCR/CV/AI).

**Проблемы, которые чинит план:**
1. Локальный рендер таймлайна сломан: `job`/`present` есть только на проде (добавлены в админке руками), локально `JOB.title` в JS бросает TypeError → линия не рисуется. Нужна data-migration.
2. `setTimeout(initTimeline, 3600)` — артефакт удалённой typing-анимации.
3. Точки расставлены равномерно по индексу, метки мелкие, горизонтальная линия под именем центрируется через `align-items: center` (предыдущий фикс `margin: 0` — no-op).
4. HR-подача: стаж 10 мес не надо прятать и раздувать — показать полную честную хронологию: ИТ до 2026 → разработка с 01.2026 → проекты → сейчас.

**Решения (зафиксированы):**

| Вопрос | Решение |
|---|---|
| Позиционирование | Равномерные слоты по индексу (как сейчас): массив `[prior?, job, ...projects, present]`, `pct = i/(n-1)*100`. Пропорционально реальным датам — отклонено (строки «Июль 2026» без дней, хрупко); честность несут подписи |
| До-2026 запись | Новый тип `item_type='prior'` (AlterField choices). Не `project` — у проекта нет `repo`, сломалась бы GitHub-ссылка в карточке |
| Слоты | `prior` = 0%, `job` = 1/(n-1), проекты, `present` = 100%. С job без prior — раскладка идентична текущей (0/25/50/75/100) |
| Типы точек | prior — приглушённая полая (dashed), job — lime-контур, проекты — нейтральные, present — залитая lime с glow |
| Мобильные ≤1024px | `.hero-timeline { display: none }`. Ветку 640px со старой горизонтальной геометрией удалить. Полная хронология — секция «Опыт» в тикете 06 |
| `scrollToDetails` | Сейчас скроллит сам рельс; при вертикальном рельсе hero = весь экран и карточка не видна → скроллить `#timeline-details` (`block: 'center'`) |
| Задержка | `setTimeout(initTimeline, 3600)` → сразу по DOMContentLoaded |
| Геометрия рельса | `.hero-timeline { position: absolute; top: 14vh; bottom: 12vh; right: clamp(1rem, 3vw, 3.5rem); z-index: 2 }`; текст hero левой колонки ширину не задевает (проверено по ширинам ≥1025px); `.hero-text` имеет `pointer-events: none` — точки кликабельны |
| Прогресс | `.tl-progress` вертикальный (`width: 2px; height: 0→pct%`, `transition: height`) |
| Правки light-темы | Цветовые оверрайды `[data-theme="light"] .hero-timeline …` (~L1547) остаются; геометрия — в базовых правилах; для prior-точки фоны на `var(--page-bg)` — тема не требует отдельного оверрайда |

**Шаги реализации (каждый шаг — коммит, после тикета — пуш → CI → prod):**

1. **Контент-слой**
   - [ ] `main/models.py`: choice `('prior', 'До разработки')` в `TimelineItem.item_type`
   - [ ] `main/migrations/0009_timeline_prior_and_seed.py`: AlterField choices + RunPython (паттерн `0008`, backwards — delete). Seed через **filter-first** (`.filter(item_type=...).first()`, иначе create), НЕ `get_or_create` — на проде может быть >1 строки, `get_or_create` упал бы `MultipleObjectsReturned`. На проде job/present уже есть → no-op; prior создастся. Значения — «черновики» ниже, править в миграции
   - [ ] `main/views.py` `api_timeline`: ветка `elif item.item_type == 'prior':` → ключ `prior` в JSON (`date`, `title`, `desc`)
   - [ ] Тесты: `test_api_timeline_shape` — GET `/api/timeline/`: ключи `job`/`present`/`prior`/`timeline` непустые (миграции гоняются в тестовой БД), `len(timeline) >= 3`
2. **Вертикальный рельс**
   - [ ] `static/css/style.css` (см. решения: absolute-правка, вертикальные line/progress/dots/labels — `top` в inline %, `left: 15px` для линии/точек, `right: 24px` + `text-align: right` для подписей); новые `.tl-dot-prior`/`.tl-label-prior`/`.tl-details-card--prior`; media ≤1024 → `display: none`; удалить горизонтальную ветку `@media (max-width: 640px)` для `.timeline-track`/`.tl-line`/`.tl-progress`/`.tl-dot`/`.tl-label`; синхронизировать light-блок
   - [ ] `static/js/timeline.js`: массив-порядок `[prior?, job, ...TIMELINE, present]`, `style.top` вместо `style.left` (точки и подписи), `progressEl.style.height`, карточка prior (date+title+desc, без ссылки), scroll на `#timeline-details`, `3600` → 0
   - [ ] Тесты: substring в `DesignSystemTest` (чтение `static/css/style.css` + `static/js/timeline.js` с диска): `.hero-timeline` содержит `position: absolute`, `.tl-progress` — `transition: height`, в JS нет `'3600'`
3. **Docs-sync (AGENTS.md, шаг 6 dev workflow)**
   - [ ] AGENTS.md: `CMS models → TimelineItem` — item_type добавить `prior`; `## Project overview` — «Timeline: вертикальный рельс справа (≤1024 скрыт), типы prior/job/project/present»
   - [ ] Этот тикет: AC + итоги в Notes

**Контент-черновики (правь при реализации; на проде job/present уже свои — править в админке):**

```python
# prior — новая запись (создастся миграцией везде)
{'item_type': 'prior', 'date_label': 'До 2026',        # ← если известны годы, заменить на «2019 — 2025» и т.п.
 'title': 'ИТ-инфраструктура',
 'description': 'Работа в ИТ вне разработки: поддержка и сопровождение систем. '
                'С 2026 перешёл в разработку на Python.',
 'sort_order': 5}

# job — сеется только где нет (локально/тесты); на проде no-op
{'item_type': 'job', 'title': 'EFKO', 'role': 'Python-разработчик',
 'date_range': 'Январь 2026 — настоящее время', 'url': 'https://efko.digital',
 'description': 'Python-полный стек: Django/DRF, PostgreSQL, боты и автоматизация.',
 'sort_order': 4}

# present — сеется только где нет
{'item_type': 'present', 'title': 'Сейчас',
 'description': 'Работа в EFKO, pet-проекты во время учёбы; фокус — Python Fullstack (Django/DRF).',
 'sort_order': 10}
```

**Верификация:** `uv run ruff check .` → `uv run manage.py test` → локально `/` (карточка «сейчас» рендерится сразу, клики по точкам, prior-точка сверху) → коммиты → пуш → CI через GitHub API → прод: рельс справа, обе темы, ≤1024 рельса нет.

**Workflow (дома, другая машина):** `git pull` → `uv sync --frozen` → шаги выше по порядку, один коммит на шаг → пуш после всех шагов тикета (деплой одной волной).

### 2026-10-08: реализация рельса (итог)

Три коммита: `2557931` (контент-слой), `b2ca32d` (рельс), docs-sync.

- **Контент-слой**: `prior` в `TYPE_CHOICES`; `0009_timeline_prior_and_seed` — AlterField + filter-first seed prior/job/present (backwards удаляет только prior — job/present на проде не наши); `api_timeline` отдаёт ключ `prior` (`date`/`title`/`desc`).
- **Рельс**: `.hero-timeline` — `position: absolute; top: 14vh; bottom: 12vh; right: clamp(1rem, 3vw, 3.5rem); width: clamp(140px, 14vw, 190px)`; линия/точки `left: 15px`, подписи `right: 24px`; слоты `[prior?, job, ...projects, present]` через `style.top` (`pct = i/(n-1)*100`), прогресс — `height`; скролл на `#timeline-details` (`block: 'center'`); `3600` → `initTimeline()` на DOMContentLoaded; ≤1024 `display: none`; горизонтальная ветка `@media 640px` удалена; prior — пунктирная полая точка (`--page-bg`), `.tl-details-card--prior` без ссылки. JS переписан на слоты с защитой от отсутствующих job/present (не падает, а пропускает).
- **Отклонение от плана (по замерам)**: `--type-scale-hero` `10.5vw → 9.75vw`. При 10.5vw линия и точка рельса пересекали фамилию на 1025–1366px (headless-замеры: name right 891 vs line x 859 на 1025; 1188 vs 1158 на 1366). После правки зазор ≥20px на всех ширинах ≥1025, имя остаётся одной строкой, максимум шкалы (9rem) не изменился.
- **Верификация**: ruff + 15/15 тестов (новые: `ApiTimelineTest.test_api_timeline_shape`, `DesignSystemTest.test_timeline_rail_vertical`); headless Chrome: 1025/1100/1280/1366/1440/1680/1920 — наложений рельса на текст нет, горизонтального скролла нет; клики по точкам (prior/job/project/present) дают карточки и прогресс 0/20/60/100%; ≤1024 рельс `display: none`; light-тема: prior-точка белая пунктирная = фон hero. Глаз-чек — после деплоя.

### 2026-10-09: рельс закреплён при скролле (follow-up по глаз-чеку)

Запрос: рельс должен динамично оставаться на виду при прокрутке. Решение — `position: fixed` + компакт-режим вне hero (чтобы не перекрывать контент).

- `.hero-timeline` → `position: fixed; top: 14vh; bottom: max(12vh, 6rem)` (низ разведён с `back-to-top`); `z-index: 50` (контент ниже, кнопка наверх 100 — выше). Markup вынесен из `.hero` на уровень `<body>` (page chrome, рядом с `back-to-top`) — не ломается, если hero получит transform.
- **Компакт-режим**: `initRailMode()` в `timeline.js` — класс `.compact` при `scrollY > 0.12 * innerHeight` (в hero полный рельс; ниже — полоса 48px, подписи `opacity: 0`, при `:hover`/`:focus-within` раскрываются поверх контента транзиентно). Порог выбран по геометрии: hero (100vh) не выходит из зоны рельса (14–88vh) до scrollY = 12vh.
- **Жёлоб**: `@media (min-width: 1025px) { .portfolio { padding-right: 7rem } }` — full-bleed секция проектов освобождает полосу под компакт-рельс (48px + right-offset ≤ 56px → 104px); centered-блоки (`tl-details`/`skills` 860px, `contact` 400px) в полосу не заходят начиная с 1025px.
- Reduced-motion: `.hero-timeline { transition: none }`.
- Тесты: `test_timeline_rail_vertical` → `position: fixed` + `.hero-timeline.compact` + `initRailMode`; новый `test_timeline_rail_is_page_chrome` (парсер HTML — у `#hero-timeline` нет предка `.hero`). Итого 16/16.
- **Верификация** (headless 1025×768…1920×1080, портфолио+stats раскрыты): `railTop` константен (108/112/126/151) при скролле от 0 до низа; full + подписи в hero (пересечения с именем/кнопками нет); компакт после 50vh; правые края контента 943/1168/1254/1328/1808 ≤ левого края рельса 946/1194/1277/1349/1816; hover → подписи `opacity: 1`; клик по точке снизу → карточка/active/прогресс, детали в кадре; `back-to-top` разведён (1025×600 зазор 20px); ≤1024 `display: none`; light-тема ок; ошибок консоли нет. Призраки (`.portfolio-ghost-skill`) исключены из замера как декоративные (`overflow: hidden`, `opacity ≤ 0.26`, под рельсом).

### 2026-10-09: глаз-чек — две правки (компакт-подписи + осиротевшая карточка)

По репорту Сергея:

1. **Компакт-подписи перекрывались рельсом.** Подписи позиционировались базовым `right: 24px`; в компакте (коробка 48px) правый край текста попадал на x=24 — внутрь точки/glow (x≈3–27), рельс замазывал конец года («Июль 2…», остальное под полосой). Фикс — в `.hero-timeline.compact .tl-label` добавлен `right: calc(100% + 6px)` (правый край уходит на x≈−6, левее точки/glow): подписи выезжают целиком левее полосы. Только компакт — полный режим в hero не тронут (там `right: 24px` уводит подписи вправо, наложения нет).
2. **Осиротевшая карточка на мобиле.** `initTimeline()` дефолтно выбирает present и пишет в `#timeline-details`, который лежит в `.content-body` (вне `.hero-timeline`); гейтинга по `.show` нет — при `display:none` рельса ≤1024 карточка «Настоящее время…» всё равно видна. Фикс — `.tl-details { display: none }` в тот же `@media (max-width: 1024px)`, что и рельс (сателлит исчезает вместе с рельсом). Тредофф согласован: на мобиле «сейчас»-сводки нет до полной хронологии в тикете 06.

- Тесты: `test_timeline_rail_vertical` расширен (`right: calc(100% + 6px)` в компакт-правиле + нормализованный whitespace-ассерт «`.hero-timeline { display: none; } .tl-details { display: none; }`»); 16/16 зелёные, ruff чистый.
- Глаз-чек на проде — в процессе.

### 2026-10-09: крупнее подписи рельса

Глаз-чек: подписи дат мелкие, неудобно читать. `.tl-label` `font-size: 0.65rem → 0.8rem` (мобильных оверрайдов размера подписей нет — старая 640px-ветка удалена). Геометрия не меняется: подписи привязаны правым краем (`right: calc(100% + 6px)` в компакте), зазор от рельса сохраняется. 16/16 зелёные, ruff чистый.

### 2026-10-09: закрытие

Сергей подтвердил рельс и фикс кегля на проде — все AC закрыты. Тикет `done`, разблокирует 03.
