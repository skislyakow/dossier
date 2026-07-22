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
- `static/fonts/` — Material Symbols font (local)
- `static/favicon.svg`
- `requirements.txt` — Python dependencies

## Dev workflow
1. Activate venv: `.venv\Scripts\activate`
2. Run server: `python manage.py runserver`
3. Visit `http://127.0.0.1:8000/`

## Production
- VPS: `132.243.121.192` (Ubuntu 24.04)
- Nginx reverse proxy → gunicorn (127.0.0.1:8000)
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

## CMS models
- **Skill** — name, size (xl/lg/md/sm), icon (Material Symbol name), order
- **Project** — title, repo, pypi, role, tagline, features (JSON), links (JSON), badges_config (JSON), screenshot (URL), order, is_published
- **TimelineItem** — item_type (project/job/present), date_label, title, description, repo, url, role, date_range, order
- **ContactInfo** — contact_type (email/telegram), label, value, order

## Adding a project to portfolio
Admin: Main → Projects → Add. Fill:
- Repo: `skislyakow/repo-name`
- PyPI: package name (optional, enables PyPI + PyPistats badges)
- Role: e.g. "Python SDK Development" (maps to placeholder theme)
- Features: JSON list of strings
- Badges: JSON array `[{"label": "pypi", "source": "pypi_version"}]`
- Links: JSON dict `{"pypi": "https://...", "www": "https://..."}`

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

### Critical
- [ ] HTTPS + кастомный домен (Let's Encrypt)
- [ ] Разделить `requirements.txt` и `requirements-prod.txt`

### SEO / видимость
- [ ] `sitemap.xml`, `robots.txt`
- [ ] `og:image` / `twitter:image` — нет превью при шаринге

### UX / контент
- [ ] Кастомный домен вместо裸 IP

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
