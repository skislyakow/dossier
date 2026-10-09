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
- `main/badge_utils.py` — серверный резолв бейджей и данных GitHub+PyPI (звёзды, форки, лицензия, язык, размер, даты, PyPI-версия/python/лицензия, PyPistats). Ходит в сеть через stdlib `urllib` (без зависимостей), кэширует в БД (`DatabaseCache`, `TIMEOUT` 6ч; при сбое внешнего API — короткий кэш 5мин, чтобы не долбить). Опц. `GITHUB_TOKEN` из env поднимает лимит 60→5000/ч. Браузер внешние API **не** дёргает — только `/api/projects/` (обогащённые `repo/langs/stars/badges`) и `/api/github/` (GitHub-stats toggle: профиль владельца + топ-5 языков, `fetch_github_stats()`), которые сами ходят в сеть и кэшируют.
- `templates/` — HTML templates
- `static/css/` — Styles
- `static/js/` — Scripts (github.js, portfolio.js, timeline.js)
- `static/fonts/` — Material Symbols font (локальный **subset** `MaterialSymbolsOutlined.woff2` ~3 КБ, сгенерирован через `fonttools` только из используемых лигатур: `uvx --from fonttools fonttools subset` по codepoint'ам из `MaterialIconsOutlined-Regular.codepoints` (сама утилита в venv не входит); в `style.css` `@font-face` локальный файл — **первый**, полный Google Fonts woff2 — fallback для офлайна). В subset входят иконки навыков + UI-иконки админки. Каталог `IconPickerWidget` (COMMON_ICONS) в subset **не** входит — при добавлении новой иконки через админку она не отрисуется, пока subset не перегенерирован.
- `static/css/fonts.css` — **самохост** текстовых шрифтов (Inter 400/600/700 + Fira Code 400/700, подмножества latin + cyrillic, скачаны с Google Fonts css2 как woff2 в `static/fonts/`). В `<head>` внешний Google Fonts `<link>` убран — подключается только локальный `fonts.css` (без внешних запросов, `font-display: swap`). При добавлении нового веса/семейства — докачать woff2 и дописать `@font-face` в `fonts.css`.
- `static/favicon.svg`
- `pyproject.toml` + `uv.lock` — Python dependencies (uv; dev-зависимости в `[dependency-groups] dev`)

## Dev workflow
1. Install/update deps: `uv sync --frozen`
2. Lint: `uv run ruff check .` (правила в `ruff.toml`; Ruff в dev-группе)
3. Tests: `uv run manage.py test`
4. Run server: `uv run manage.py runserver`
5. Visit `http://127.0.0.1:8000/`
6. Синхронизация доков: если изменено поведение сайта или команды запуска — обновить README и AGENTS.md в рамках того же изменения. README держать тонким (что это, бейджи, запуск, деплой, контакты); инвентаризация фич живёт в `## Project overview` ниже

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
On push to `main` GitHub Actions сначала гоняет чек-гейт (`uv run ruff check .` + `uv run manage.py test`) на Ubuntu; при его успехе — SSH into VPS and runs:
```
git pull → установка uv (если нет) → uv sync --frozen --no-dev → migrate → createcachetable → collectstatic → restart gunicorn
```
Required GitHub secrets: `VPS_HOST`, `VPS_SSH_KEY`

## Project overview
Personal portfolio / visiting card site for Sergey Kislyakov (Python Fullstack Developer).
- Design tokens in `:root`: монохром + кислотный лайм `#CDFF50` (fallback-акцент — правка одного токена через `color-mix`), типографическая шкала `--type-scale-*`, текст на карточках `--text-card*`
- Skills: сетка, сгруппированная по Категориям навыка (Backend / Web / DevOps / Bots & Integrations / Tools), пустые категории не показываются; кегль тега — `Skill.size` (xl/lg/md/sm), старое curly-облако `{ skill }` убрано
- Hero: full-width oversized name (clamp-шкала), приглушённый курсорный градиент, scroll-reveal через IntersectionObserver, строка позиционирования «Python-разработчик: автоматизация, Telegram-боты и веб на Django»
- Timeline: вертикальный рельс справа `position: fixed` — виден на всём скролле (в hero с подписями дат, вне hero — компактная полоса 48px, подписи по наведению); markup вынесен из `.hero` на уровень `body` (page chrome); ≤1024px скрыт; типы prior/job/project/present, карточка деталей по клику
- Chrome в едином акценте: соц-ссылки/back-to-top — квадратные рамки `2px`, hover на лайме (`--accent`/`--accent-soft`), подписи uppercase-моно; aria-labels сохранены
- Marquee-строка технологий между hero и `.content-body` (page chrome, `aria-hidden`): бесшовный цикл `translateX(-50%)` из двух `.marquee-group`, статичный список (Python/Django/…) — декоративный, не CMS; `prefers-reduced-motion` → `animation: none`
- GitHub stats toggle (stars, repos, languages via GitHub API)
- Portfolio section with project cards (Django CMS, GitHub API + PyPI badges)
- Усиленная карточка проекта: таглайн + буллеты + бейджи + ссылки на светлой карточке (`--bg-card` поверхность, текст `--text-card*`); стаггер-reveal по `--i` при появлении/переключении, magnetic-hover на `--mag-x/--mag-y` (≤6px, `pointer: fine`, off при `prefers-reduced-motion`); все значения из API вставляются через `esc()`
- Placeholder медиа карточки (нет скриншота) — статичная монограмма проекта на лаймовом градиенте с сеткой (без анимаций, без призраков)
- Dynamic badges from GitHub API, PyPI, PyPistats
- Light/dark theme toggle (dark default; light — `data-theme="light"` + localStorage)
- Contact section with email + Telegram
- Back to top button
- Social link hover labels (icon slides, text appears)
- Responsive: breakpoints at 1024px, 768px, 640px
- All content managed via Django admin (Skills, Projects, TimelineItems, ContactInfo)
- Drag-and-drop reordering in admin (unfold `ordering_field` + AJAX save)
- Начальный контент (проекты/навыки/таймлайн) сеется через **data-migrations** в `main/migrations/` (см. `0005_add_devman_monitor_data.py`, `0007_add_support_bot_data.py`, `0008_add_quiz_bot_data.py`): `RunPython(forwards, backwards)` с `get_or_create` по `repo`/`name` и сдвигом `sort_order` существующих таймлайн-записей. `0010_skill_category.py` — schema + data миграция нового поля: `AddField` + `RunPython` с распределением по имени (`CATEGORY_BY_NAME`), в `backwards` — сброс на дефолт. Редактирование наполнения — через admin, массовое добавление новых проектов — через миграцию (чтобы попало на прод при пуше).

## Current CMS content
### Projects (role = "Bot Development")
- **Devman Monitor** — `skislyakow/Devman-monitor` — монитор systemd-сервиса с уведомлениями в Telegram
- **Support Bot** — `skislyakow/support-bot` — поддержка в TG/VK на Dialogflow (aiogram + vk_api)
- **Quiz Bot** — `skislyakow/quiz-bot` — викторина в TG/VK на ~300k вопросов: aiogram + vkbottle, состояние в Redis, нормализация через pymorphy3 (НЕ на PyPI → только github-бейджи)

### Skills
`systemd`, `python-dotenv`, `Telegram Bot API`, `Dialogflow`, `aiogram`, `vk_api`, `Redis`, `vkbottle`, `VK API`, `pymorphy3`, `mypy`

## CMS models
- **Skill** — name, category (backend/web/devops/bots/tools), size (xl/lg/md/sm), icon (Material Symbol name), sort_order
- **Project** — title, repo, pypi, role, tagline, features (JSON), links (JSON), badges_config (JSON), screenshot (URL), sort_order, is_published
- **TimelineItem** — item_type (prior/job/project/present), date_label, title, description, repo, url, role, date_range, sort_order
- **ContactInfo** — contact_type (email/telegram), label, value, sort_order

## Adding a project to portfolio
Admin: Main → Projects → Add. Fill:
- Repo: `skislyakow/repo-name`
- PyPI: package name (optional, enables PyPI + PyPistats badges)
- Role: e.g. "Python SDK Development" (maps to placeholder theme)
- Features: JSON list of strings
- Badges: JSON array `[{"label": "pypi", "source": "pypi_version"}]`
- Links: JSON dict `{"pypi": "https://...", "www": "https://..."}`

Drag-and-drop the `drag_indicator` handle in the list view to reorder. Changes save automatically via AJAX.

Чтобы новый проект/навык попал на прод при пуше — оформляйте массовое добавление через **data-migration** (паттерн `0008_add_quiz_bot_data.py`): `RunPython` + `get_or_create` по `repo`/`name`, со сдвигом `sort_order` таймлайн-записей в `backwards`. Секция Skills, облако навыков и placeholder-карточки портфолио (`portfolio.js`) читают `/api/skills/` (включая `category`) динамически — добавление `Skill` само обновляет эти места, правка JS не нужна.

### Dynamic badge sources
| Source | Data | Requires |
|---|---|---|
| `github_stars` | stargazers_count | repo |
| `github_forks` | forks_count | repo |
| `github_license` | spdx_id | repo |
| `github_lang` | primary language | repo |
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
- [ ] `og:image` / `twitter:image` — нет превью при шаринге

### Код / доступность
- [ ] XSS: innerHTML в timeline.js / github.js и в contact-рендере index.html — данные из API вставляются без экранирования (низкий риск — только admin/API); portfolio.js и секция Skills экранируют через `esc()` (закрыто в тикетах 04–05)
- [ ] Тесты на основные view/home page
- [ ] mypy в CI (зависимости уже ставятся через `uv sync --frozen`)

---

## Идеи с sui.io (анализ)

### 1. Hero-заголовок с градиентом под мышкой ✅
### 2. Gradient blur фон hero ✅
### 3. Arrow-swap на иконках ✅
### 4. Stagger reveal карточек портфолио ✅

---

## Идеи с roshan-sahu.com (анализ)

### 1. Текущее время MSK в hero ✅
### 2. Contact секция ✅
### 3. Back to top ✅
### 5. Теги карточек портфолио с ролями ✅

---

## Идеи с studiomodular.be (анализ)

### 1. Full-width layout ✅
### 2. Hero на всю ширину ✅
### 3. Крупная типографика ✅
### 4. Карточки портфолио — role-based placeholder themes ✅

### Что НЕ берём
- Three.js / 3D сцены — нет сборщика
- GSAP — библиотека, не вписывается в zero-dependency
- Бургер-меню (на визитке важна видимость ссылок)
- Видеобэкграунд (тяжёлый, нет контента)
