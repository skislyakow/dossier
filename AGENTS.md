# Agents

## Setup
- Tooling: [uv](https://docs.astral.sh/uv/) — зависимости описаны в `pyproject.toml`, лок в `uv.lock` (закоммичен), версия Python пинится в `.python-version` (3.12). Установка uv: `pip install uv` или по докам
- `uv sync --frozen` создаёт/обновляет `.venv/`; команды запускаются через `uv run` (активация venv не нужна)
- Django: 6.0.4
- Run dev server: `uv run manage.py runserver`
- Agent skills: после первого клонирования выполнить `npx skills experimental_install` — восстанавливает `.agents/skills/` из закоммиченного `skills-lock.json` (хеши версий пинятся там же; сам каталог `.agents/` в git не входит)

## Structure
- `config/` — Django project settings (settings.py, urls.py, wsgi.py, asgi.py)
- `main/` — Main app (views, models, admin, widgets, management/commands)
- `main/views.py` — views + JSON API (`api_skills`/`api_projects`/`api_tags`/…)
- `main/taxonomy.py` — **единый владелец таксономии**: `skill_size()` (5+→xl / 3–4→lg / 1–2→md / 0→sm), `resolve_tag()` (`filter_tag || name`), `tag_cloud()`/`tag_counts()` (частоты тегов опубликованных проектов). Используется в `api_skills`, `api_tags` и `audit_content` — пороги и резолв меняются в одном месте, JS размеры не считает. Подробности — `docs/adr/0001-taxonomy-owned-by-server.md`
- `main/badge_utils.py` — серверный резолв бейджей и данных GitHub+PyPI (звёзды, форки, лицензия, язык, размер, даты, PyPI-версия/python/лицензия, PyPistats). Реестр `BADGE_SOURCES` (`source → {label, icon, group, resolve}`) — единственный источник правды: из него строится каталог пикера бейджей в `widgets.py`, резолверы `resolve_badge`/`resolve_badges` и coverage-тест `BadgeSourceRegistryTest`. Подробности — `docs/adr/0002-badge-registry.md`. Ходит в сеть через stdlib `urllib` (без зависимостей), кэширует в БД (`DatabaseCache`, `TIMEOUT` 6ч; при сбое внешнего API — короткий кэш 5мин, чтобы не долбить). Опц. `GITHUB_TOKEN` из env поднимает лимит 60→5000/ч. Браузер внешние API **не** дёргает — только `/api/projects/` (обогащённые `repo/langs/stars/badges`) и `/api/github/` (GitHub-stats toggle: профиль владельца + топ-5 языков, `fetch_github_stats()`), которые сами ходят в сеть и кэшируют.
- `main/resume.py` — авто-резюме: `context()` (ResumeProfile/ContactInfo/TimelineItem/Project/Skill → словарь для шаблона `resume/_body.html`), `build_pdf()` (WeasyPrint `HTML(string=...).write_pdf()` с этим же `static/css/resume.css`), `write_pdf()`, `pdf_path()` (`STATIC_ROOT/resume/resume.pdf`, если записываем, иначе `static/resume/resume.pdf`). Страницы `GET /resume/` (HTML) и `GET /resume/pdf/` (`FileResponse`); перегенерация — сигналы в `main/signals.py` (гейт `settings.RESUME_AUTOGEN`; в тестах отключён) + команда `generate_resume` в деплое перед `collectstatic`. Решение — `docs/adr/0003-resume-generated-from-cms.md`.
- `templates/` — HTML templates
- `static/css/` — Styles
- `static/js/` — Scripts (`util.js` — общие `esc()` (XSS-экранирование) и `prefersReducedMotion()`; github.js, portfolio.js, timeline.js + инлайн-скрипты index.html грузят его первым и переиспользуют)
- `static/fonts/` — самoxost текстовых шрифтов (см. ниже `fonts.css`). Иконки навыков: **удалены** (см. `0020_remove_skill_icon`) — сайт рендерит навыки текст-тегами, админка использует бандл unfold (Material Symbols), свой subset и `IconPickerWidget` больше нет.
- `static/css/fonts.css` — **самохост** текстовых шрифтов (Inter 400/600/700 + Fira Code 400/700, подмножества latin + cyrillic, скачаны с Google Fonts css2 как woff2 в `static/fonts/`). В `<head>` внешний Google Fonts `<link>` убран — подключается только локальный `fonts.css` (без внешних запросов, `font-display: swap`). При добавлении нового веса/семейства — докачать woff2 и дописать `@font-face` в `fonts.css`.
- `static/favicon.svg`
- `static/og/og-image.png` — превью при шаринге (1200×630, `og:image`/`twitter:image`, `summary_large_image`); перегенерировать из шаблона при правке дизайна
- `pyproject.toml` + `uv.lock` — Python dependencies (uv; dev-зависимости в `[dependency-groups] dev`)

## Dev workflow
Чек-гейт перед коммитом/пушем: `./tools/gate.sh` — fail-fast (`set -euo pipefail`), тот же набор, что CI: ruff → mypy → pytest → makemigrations --check → node --check по каждому `static/js/*.js`; exit 0 = зелёный. Ниже — те же проверки и остальные шаги по отдельности.
1. Install/update deps: `uv sync --frozen`
2. Lint: `uv run ruff check .` (правила в `ruff.toml`; Ruff в dev-группе)
3. Type check: `uv run mypy main/` (mypy + django-stubs в dev-группе; plugin `mypy_django_plugin`, настройки в `[tool.mypy]`/`[tool.django-stubs]` в pyproject.toml)
4. Tests: `uv run pytest` (pytest + pytest-django; настройки в `[tool.pytest.ini_options]` в pyproject.toml)
5. Audit контента: `uv run manage.py audit_content` — теги проектов ↔ навыки (кнопки Skills). E100 (тег без навыка) — выход 1; W101 (навык без совпадающего тега) — предупреждение. Против прода: выполнить на проде или через `manage.py` с живой БД
6. Smoke-верификация без браузера: `./tools/smoke.sh` (curl + python3 stdlib, без зависимостей). Проверяет `/`, статику, JSON-контракты `/api/skills/` `/api/projects/` `/api/tags/` `/api/timeline/` `/api/contact/` `/api/github/`, страницы `/resume/` и `/resume/pdf/`; код выхода 0 = всё ок. Локально — против запущенного `uv run manage.py runserver --insecure` (иначе статику не отдаёт: `DEBUG=False`), прод — `./tools/smoke.sh https://kislyakov.pro`
7. Наблюдение за CI после пуша: `./tools/ci-watch.sh <short-sha>` (токен из git credential store, ограниченный поллинг + видимый прогресс; exit 0 success / 1 failure / 2 timeout)
8. Run server: `uv run manage.py runserver` (статика только с `--insecure`)
9. Visit `http://127.0.0.1:8000/`
10. Синхронизация доков: если изменено поведение сайта или команды запуска — обновить README и AGENTS.md в рамках того же изменения. README держать тонким (что это, бейджи, запуск, деплой, контакты); инвентаризация фич живёт в `## Project overview` ниже

## Production
- Domain: `kislyakov.pro` (reg.ru)
- VPS: `132.243.121.192` (Ubuntu 24.04)
- Nginx reverse proxy → gunicorn (127.0.0.1:8000)
- HTTPS via Let's Encrypt (certbot, auto-renewal)
- HTTP → HTTPS redirect, www → root redirect
- systemd service: `dossier.service`
- Static files: `/var/www/dossier/static/`
- Auto-deploy: GitHub Actions on push to `main`

## Auto-deploy
On push to `main` GitHub Actions сначала гоняет чек-гейт (`uv run ruff check .` + `uv run mypy main/` + `uv run pytest` + `makemigrations --check` + `node --check` по каждому `static/js/*.js`) на Ubuntu; при его успехе — SSH into VPS and runs:
```
git pull → установка uv (если нет) → uv sync --frozen --no-dev → migrate → createcachetable → collectstatic → restart gunicorn
```
Required GitHub secrets: `VPS_HOST`, `VPS_SSH_KEY`

## Project overview
Personal portfolio / visiting card site for Sergey Kislyakov (Python Fullstack Developer).
- Design tokens in `:root`: монохром + кислотный лайм `#CDFF50` (fallback-акцент — правка одного токена через `color-mix`), типографическая шкала `--type-scale-*`, текст на карточках `--text-card*`
- Skills: сетка, сгруппированная по Категориям навыка (Backend / Web / DevOps / Bots & Integrations / Tools), пустые категории не показываются; кегль тега рассчитывается автоматически по частоте в тегах опубликованных проектов (`api_skills`: поле `tag` = резолв `filter_tag || имя`; пороги `taxonomy.skill_size`: 5+→xl / 3–4→lg / 1–2→md / 0→sm, поле `Skill.size` удалено — см. `0021_remove_skill_size`), старое curly-облако `{ skill }` убрано
- Hero: full-width oversized name (clamp-шкала), приглушённый курсорный градиент, scroll-reveal через IntersectionObserver, строка позиционирования «Python-разработчик: автоматизация, Telegram-боты и веб на Django»
- Timeline: вертикальный рельс справа `position: fixed` — виден на всём скролле (в hero с подписями дат, вне hero — компактная полоса 48px, подписи по наведению); markup вынесен из `.hero` на уровень `body` (page chrome); ≤1024px скрыт; типы prior/job/project/present; клик по точке — скролл к строке секции Опыт + подсветка; при раскрытии любой панели (Проекты/Статистика/Контакты) рельс скрывается (`body:has(... .show)`), жёлоб 7rem у секции Projects снимается
- Опыт: секция-хронология `#experience` в `.content-body` (между Projects и Skills) — все элементы `/api/timeline/` (prior → job → проекты → present) вертикальной лентой с точками на линии, даты — моно; рендерит `timeline.js` с экранированием `esc()`; на мобиле секция видна (рельс скрыт ≤1024px); при раскрытии раздела Проекты секция скрывается (`body:has(#portfolio.show) #experience`); старая detail-карточка `.tl-details` удалена (тикеты 06/10)
- Chrome в едином акценте: соц-ссылки/back-to-top — квадратные рамки `2px`, hover на лайме (`--accent`/`--accent-soft`), подписи uppercase-моно; aria-labels сохранены
- Marquee-строка технологий между hero и `.content-body` (page chrome, `aria-hidden`): бесшовный цикл `translateX(-50%)` из двух `.marquee-group`, статичный список (Python/Django/…) — декоративный, не CMS; `prefers-reduced-motion` → `animation: none`
- GitHub stats toggle (stars, repos, languages via GitHub API)
- Portfolio section with project cards (Django CMS, GitHub API + PyPI badges)
- Облако тегов проектов: `Project.tags` (JSONField, курируемые метки) → объединение тегов опубликованных Проектов в облако `{ тег: N }` (свой класс `.ptag` с curly в `::before`/`::after`, кегль по частоте **теми же бакетами, что и у навыков** — классы `ptag-xl|lg|md|sm`: 5+→xl / 3–4→lg / 1–2→md / 0→sm; размеры считает сервер — `main/taxonomy.py` (`tag_cloud`), облако рендерит кликер из `GET /api/tags/`), клик — фильтр списка (одиночный, `All` — сброс), комбинируется с фильтром по роли AND; тег без проектов не показывается; значения из API экранируются (`esc()`)
- Навыки — кликабельные кнопки (`window.__applyPortfolioTag`): клик по навыку открывает секцию Projects и фильтрует список по резолв-тегу навыка (`filter_tag || имя`, поле `tag` из `/api/skills/`); нет совпадений — явный empty-state `.portfolio-empty`, навык без совпадений получает `active`-состояние; фильтр сбрасывается при закрытии панели
- Усиленная карточка проекта: таглайн + буллеты + бейджи + ссылки на светлой карточке (`--bg-card` поверхность, текст `--text-card*`); превью — `grid-template-columns: minmax(0,2fr) minmax(0,1fr)` (инфо/медиа), на ≤768px колонка медиа скрыта и сетка схлопывается в `1fr`, чтобы инфо занимало всю карточку; стаггер-reveal по `--i` при появлении/переключении — **eager-синхронный** (`revealNow`, без IntersectionObserver; названия пунктов списка вообще без `.reveal`), magnetic-hover на `--mag-x/--mag-y` (≤6px, `pointer: fine`, off при `prefers-reduced-motion`); все значения из API вставляются через `esc()`
- Placeholder медиа карточки (нет скриншота) — статичная монограмма проекта на лаймовом градиенте с сеткой (без анимаций, без призраков); на мобильном (≤768px, когда превью сворачивается в одну колонку) `.portfolio-preview-media` скрыта — всё серое пространство карточки занято инфо
- Dynamic badges from GitHub API, PyPI, PyPistats
- Резюме: `GET /resume/` — A4-страница из контента CMS (ResumeProfile/Опыт/Проекты/Навыки/Контакты), `GET /resume/pdf/` — PDF (WeasyPrint), перегенерируется сигналами при правке контента и командой `generate_resume` в деплое; кнопка «Резюме» в hero и «Скачать PDF» на странице
- Инженерная строка `.eng-strip` между marquee и контентом: mono uppercase, монохром + лаймовые ❋ (page chrome, `aria-hidden`)
- Light/dark theme toggle (dark default; light — `data-theme="light"` + localStorage)
- Contact: секция тремя крупными каналами (email / Telegram / GitHub) — сетка карточек `--bg-card` (иконка + тип моно + значение), метка `{ контакты: N }` (общий компонент `.sec-label` с Опытом); данные из ContactInfo через `/api/contact/`, рендер в index.html с экранированием `esc()`; href по типу (mailto / t.me / github.com)
- Back to top button
- Social link hover labels (icon slides, text appears)
- Responsive: breakpoints at 1024px, 768px, 640px
- All content managed via Django admin (Skills, Projects, TimelineItems, ContactInfo)
- Drag-and-drop reordering in admin (unfold `ordering_field` + AJAX save)
- Начальный контент (проекты/навыки/таймлайн) сеется через **data-migrations** в `main/migrations/` (см. `0005_add_devman_monitor_data.py`, `0007_add_support_bot_data.py`, `0008_add_quiz_bot_data.py`): `RunPython(forwards, backwards)` с `get_or_create` по `repo`/`name` и сдвигом `sort_order` существующих таймлайн-записей. `0010_skill_category.py` — schema + data миграция нового поля: `AddField` + `RunPython` с распределением по имени (`CATEGORY_BY_NAME`), в `backwards` — сброс на дефолт. `0012_project_tags.py` — schema + data сида тегов: `AddField` + `RunPython` c `filter`-first по `repo`. `0013_skill_filter_tag.py` — schema + data: `AddField` + `RunPython` сида `filter_tag` навыков (`FILTER_TAG_BY_NAME`) и тегов таглесс-проектов (`TAGS_BY_REPO`, update-only по `repo`, на проде 5 проектов). `0014_update_dossier_features.py` / `0015_dossier_html_tags.py` — контентные правки карточки Dossier (update-only по `repo`). `0016_add_skills_fastapi_github_pages.py` — `get_or_create` недостающих навыков с `sort_order = max + 1`. `0017_add_skills_python_pytest.py` — сиды `Python`/`pytest` (Python чинит dev-E100, pytest — HR-видимый скилл). `0018_dossier_ci_bullet.py` — замена буллета CI в features Dossier (update-only). `0019_add_dossier_pytest_tag.py` — тег `pytest` карточке Dossier (репо реально гоняет тесты через pytest; update-only по `repo`). Редактирование наполнения — через admin, массовое добавление новых проектов — через миграцию (чтобы попало на прод при пуше). Согласованность тегов ↔ навыков проверяется `uv run manage.py audit_content` (см. Dev workflow).

## Current CMS content
### Projects (role = "Bot Development")
- **Devman Monitor** — `skislyakow/Devman-monitor` — монитор systemd-сервиса с уведомлениями в Telegram (теги: Python, systemd, Telegram)
- **Support Bot** — `skislyakow/support-bot` — поддержка в TG/VK на Dialogflow (aiogram + vk_api) (теги: Python, aiogram, Dialogflow, Telegram, VK)
- **Quiz Bot** — `skislyakow/quiz-bot` — викторина в TG/VK на ~300k вопросов: aiogram + vkbottle, состояние в Redis, нормализация через pymorphy3 (НЕ на PyPI → только github-бейджи) (теги: Python, aiogram, vkbottle, Redis, Telegram, VK)

### Skills
`systemd`, `python-dotenv`, `Telegram Bot API`, `Dialogflow`, `aiogram`, `vk_api`, `Redis`, `vkbottle`, `VK API`, `pymorphy3`, `mypy`, `Python`, `pytest`

## CMS models
- **Skill** — name, category (backend/web/devops/bots/tools), filter_tag (тег проекта для клика-фильтра, пусто → имя навыка), sort_order (размер не хранится — кегль вычисляется в `/api/skills/` по тегам опубликованных проектов)
- **Project** — title, repo, pypi, role, tagline, features (JSON), tags (JSON, список строк), links (JSON), badges_config (JSON), screenshot (URL), sort_order, is_published
- **TimelineItem** — item_type (prior/job/project/present), date_label, title, description, repo, url, role, date_range, sort_order
- **ContactInfo** — contact_type (email/telegram/github), label, value, sort_order
- **ResumeProfile** — full_name, headline, summary, location, education (singleton `id=1`, `load()`; стартовый контент сидится миграцией `0023_seed_resume_profile`)

## Adding a project to portfolio
Admin: Main → Projects → Add. Fill:
- Repo: `skislyakow/repo-name`
- PyPI: package name (optional, enables PyPI + PyPistats badges)
- Role: e.g. "Python SDK Development" (maps to placeholder theme)
- Features: JSON list of strings
- Tags: JSON list of short stack labels, e.g. `["Django", "aiogram"]` (попадают в облако тегов секции Projects)
- Badges: JSON array `[{"label": "pypi", "source": "pypi_version"}]`
- Links: JSON dict `{"pypi": "https://...", "www": "https://..."}`

Drag-and-drop the `drag_indicator` handle in the list view to reorder. Changes save automatically via AJAX.

Чтобы новый проект/навык попал на прод при пуше — оформляйте массовое добавление через **data-migration** (паттерн `0008_add_quiz_bot_data.py`): `RunPython` + `get_or_create` по `repo`/`name`, со сдвигом `sort_order` таймлайн-записей в `backwards`. Секция Skills, облако навыков и placeholder-карточки портфолио (`portfolio.js`) читают `/api/skills/` (включая `category` и `tag`) динамически — добавление `Skill` само обновляет эти места, правка JS не нужна. Облако тегов в портфолио рендерится из `GET /api/tags/` (`main/taxonomy.tag_cloud`).

### Dynamic badge sources
Единый источник правды — реестр `BADGE_SOURCES` в `main/badge_utils.py` (`source → {label, icon, group, resolve}`); каталог пикера в админке (`widgets.py`) строится из него, рассинхрон невозможен, покрывается `BadgeSourceRegistryTest`. Новый источник бейджа = одна запись в реестре (лейбл, иконка, резолвер).

| Source | Data | Requires |
|---|---|---|
| `github_stars` | stargazers_count | repo |
| `github_forks` | forks_count | repo |
| `github_issues` | open_issues_count | repo |
| `github_license` | spdx_id | repo |
| `github_lang` | primary language | repo |
| `github_size` | repo size (KB/MB) | repo |
| `github_created` | created date | repo |
| `github_updated` | last push date | repo |
| `pypi_version` | latest version | `pypi` field |
| `pypi_python` | requires_python | `pypi` field |
| `pypi_license` | license | `pypi` field |
| `pypistats_month` | downloads/month | `pypi` field |
| `pypistats_total` | total downloads | `pypi` field |

Then push to `main` — site updates automatically.

## Agent skills

### Issue tracker

Local markdown under `.scratch/<feature>/`. See `docs/agents/issue-tracker.md`.

### Triage labels

Five canonical roles as-is (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`). See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: `GLOSSARY.md` + `docs/adr/` at the repo root. See `docs/agents/domain.md`.

## To-do

### SEO / видимость
- [x] `og:image` / `twitter:image` (1200×630, `static/og/og-image.png`, `summary_large_image`) — превью при шаринге (сгенерировано Chrome headless из шаблона; при правке дизайна перегенерировать и обновить `<meta og:image>` в `<head>`)

### Код / доступность
- [x] Светлая тема (`data-theme="light"`) — глаз-чек пройден пользователем (моб. верстка скрыта `portfolio-preview-media`, см. тикет 12)
- [x] XSS: `util.js` определяет единственный `esc()` и грузится первым; им экранируют github.js (данные GitHub API, закрыто в тикете 13), portfolio.js, секция Skills, timeline.js и contact-рендер
- [x] Тесты на основные view/home page (HomeViewTest + ApiTimeline/ApiContact/ApiSkills/ApiProjects/ApiGithub — закрыто в тикете 15)
- [x] mypy в CI (mypy + django-stubs в dev-группе, `[tool.mypy]` + `[tool.django-stubs]`; чек-гейт в deploy.yml: step `mypy main/`; локально — `uv run mypy main/`; закрыто в тикете 15)

## Ограничения (наследие «Идеи с …», все пункты внедрены)
- Стек не меняем: zero-dependency vanilla JS/CSS, без сборщика (нет Vite/webpack/React/Vue/HTMX), не тащим библиотеки (GSAP/Three.js) — декоративными фичами это не оправдано
- Бургер-меню не делаем: на визитке важна видимость ссылок; видеобэкграунда нет (тяжёлый, нет контента)
- Анимации — только с уважением `prefers-reduced-motion`; декоративные без контента не добавляем
