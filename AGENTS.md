# Agents

## Setup
- Virtual environment: `.venv/`
- Python: 3.12+
- Django: 6.0.4
- Run dev server: `python manage.py runserver`

## Structure
- `config/` — Django project settings (settings.py, urls.py, wsgi.py, asgi.py)
- `main/` — Main app (views, models, admin, widgets, management/commands)
- `templates/` — HTML templates
- `static/css/` — Styles
- `static/js/` — Scripts (typing.js, typewriter.js, github.js, portfolio.js, timeline.js, ghost.js)
- `static/fonts/` — Material Symbols font (локальный **subset** `MaterialSymbolsOutlined.woff2`; в `style.css` `@font-face` полный Google Fonts woff2 стоит **первым**, локальный — fallback для офлайна)
- `static/favicon.svg`
- `requirements.txt` — Python dependencies

## Dev workflow
1. Activate venv: `.venv\Scripts\activate`
2. Run server: `python manage.py runserver`
3. Visit `http://127.0.0.1:8000/`

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
GitHub Actions SSH into VPS and runs:
```
git pull → pip install → migrate → collectstatic → restart gunicorn
```
Required GitHub secrets: `VPS_HOST`, `VPS_SSH_KEY`

## Project overview
Personal portfolio / visiting card site for Sergey Kislyakov (Python Fullstack Developer).
- Typing animation for job title
- Interactive terminal with macOS-style window (opencode-py SSE streaming)
- AI assistant with system prompt (portfolio manager role)
- Skills cloud with curly braces `{ Python } { Django }`
- Two-column layout: skills cloud (left) + terminal (right) in hero
- Hero: centered name + title gradient following cursor, ghost floating skill icons
- Timeline with career dots (job start → projects → present)
- GitHub stats toggle (stars, repos, languages via GitHub API)
- Portfolio section with project cards (Django CMS, GitHub API + PyPI badges)
- Dynamic badges from GitHub API, PyPI, PyPistats
- Role-based placeholder themes for card media (SVG gradients)
- Light/dark theme toggle (GitHub-style light theme, default)
- Contact section with email + Telegram
- Back to top button
- Social link hover labels (icon slides, text appears)
- Responsive: breakpoints at 1024px, 768px, 640px
- All content managed via Django admin (Skills, Projects, TimelineItems, ContactInfo)
- Drag-and-drop reordering in admin (unfold `ordering_field` + AJAX save)
- Начальный контент (проекты/навыки/таймлайн) сеется через **data-migrations** в `main/migrations/` (см. `0005_add_devman_monitor_data.py`, `0007_add_support_bot_data.py`, `0008_add_quiz_bot_data.py`). Каждая миграция — `RunPython(forwards, backwards)` с `get_or_create` по `repo`/`name` и сдвигом `sort_order` существующих таймлайн-записей. Редактирование наполнения — через admin, массовое добавление новых проектов — через миграцию (чтобы попало на прод при пуше).

## Current CMS content
### Projects (role = "Bot Development")
- **Devman Monitor** — `skislyakow/Devman-monitor` — монитор systemd-сервиса с уведомлениями в Telegram
- **Support Bot** — `skislyakow/support-bot` — поддержка в TG/VK на Dialogflow (aiogram + vk_api)
- **Quiz Bot** — `skislyakow/quiz-bot` — викторина в TG/VK на ~300k вопросов: aiogram + vkbottle, состояние в Redis, нормализация через pymorphy3 (НЕ на PyPI → только github-бейджи)

### Skills
`systemd`, `python-dotenv`, `Telegram Bot API`, `Dialogflow`, `aiogram`, `vk_api`, `Redis`, `vkbottle`, `VK API`, `pymorphy3`, `mypy`

## CMS models
- **Skill** — name, size (xl/lg/md/sm), icon (Material Symbol name), sort_order
- **Project** — title, repo, pypi, role, tagline, features (JSON), links (JSON), badges_config (JSON), screenshot (URL), sort_order, is_published
- **TimelineItem** — item_type (project/job/present), date_label, title, description, repo, url, role, date_range, sort_order
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

Чтобы новый проект/навык попал на прод при пуше — оформляйте массовое добавление через **data-migration** (паттерн `0008_add_quiz_bot_data.py`): `RunPython` + `get_or_create` по `repo`/`name`, со сдвигом `sort_order` таймлайн-записей в `backwards`. Летающие «призраки» (`ghost.js`), облако навыков и placeholder-карточки портфолио (`portfolio.js`) читают `/api/skills/` динамически — добавление `Skill` само обновляет эти места, правка JS не нужна.

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

## To-do

### SEO / видимость
- [ ] `og:image` / `twitter:image` — нет превью при шаринге

### Код / доступность
- [ ] XSS: innerHTML в portfolio.js / timeline.js / github.js — данные из API вставляются без экранирования (низкий риск — только admin/API)
- [ ] Тесты на основные view/home page
- [ ] `requirements-dev.txt` в CI (mypy)

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
