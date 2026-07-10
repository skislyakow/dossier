# Agents

## Setup
- Virtual environment: `.venv/`
- Python: 3.12+
- Django: 6.0.4
- Run dev server: `python manage.py runserver`

## Structure
- `config/` — Django project settings (settings.py, urls.py, wsgi.py, asgi.py)
- `main/` — Main app (views, models, admin)
- `templates/` — HTML templates
- `static/css/` — Styles
- `static/js/` — Scripts (typing.js, typewriter.js, github.js, portfolio.js)
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
git pull → pip install → collectstatic → restart gunicorn
```
Required GitHub secrets: `VPS_HOST`, `VPS_SSH_KEY`

## Project overview
Personal portfolio / visiting card site for Sergey Kislyakov (Python Fullstack Developer).
- Typing animation for job title
- Interactive terminal with macOS-style window (opencode-py SSE streaming)
- AI assistant with system prompt (portfolio manager role)
- Skills cloud with curly braces `{ Python } { Django }`
- Two-column layout: terminal (left) + skills cloud (right)
- GitHub stats toggle (stars, repos, languages via GitHub API)
- Portfolio section with project cards (GitHub data + badges)
- Dynamic badges from GitHub API, PyPI, PyPistats
- Projects in portfolio: opencode-py, Ferma, Devman Bot, Dossier, Online Library

## Adding a project to portfolio
Edit `static/js/portfolio.js` → append to `PORTFOLIO` array:
```js
{
  repo: "skislyakow/repo-name",
  pypi: "package-name",  // optional: enables PyPI + PyPistats badges
  title: "Project Title",
  tagline: "Short description",
  features: ["Feature 1", "Feature 2"],
  links: { pypi: "https://...", www: "https://..." },
  badges: [
    { label: "pypi", source: "pypi_version" },      // dynamic from PyPI
    { label: "python", source: "pypi_python" },      // dynamic from PyPI
    { label: "downloads/m", source: "pypistats_month" }, // dynamic from PyPistats
    { label: "build", value: "hatchling" },           // static value
    { label: "tests" },                               // static single-section
  ],
}
```

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
- [ ] HTTPS — кастомный домен + TLS-сертификат (Let's Encrypt)
- [ ] `SECRET_KEY` вынести в environment variable
- [ ] Разделить `requirements.txt` и `requirements-prod.txt` — django-stubs/mypy не нужны в production

### SEO / видимость
- [ ] `<meta name="description">`, Open Graph, Twitter Card
- [ ] `sitemap.xml`, `robots.txt`
- [ ] `lang="ru"` вместо `lang="en"` (весь контент на русском)
- [ ] Кастомный домен вместо裸 IP

### UX / контент
- [x] ~~Skills cloud: убрать PostgreSQL и Docker~~ → убраны PostgreSQL и DRF, добавлены Jinja2, Bootstrap, opencode-py
- [ ] Контактная форма (или выделить Telegram-ссылку ярче)
- [ ] Секция «Опыт работы» (timeline мест работы)
- [ ] Оставить 2 шрифта вместо 3 (убрать Share Tech Mono)

### Дизайн
Идеи с [21hrs.space](https://www.21hrs.space/) — иммерсивный Apollo 11 сайт (SvelteKit, Three.js, GSAP).

- [ ] **Тёплая цветовая палитра** — заменить чистый белый `#fff` на `#fff3ea` (тёплый офф-вайт), фон терминала на `#1a1a1a` или `#000`. Акцент `#e4b592` (gold) вместо `#6366f1` (indigo).
- [ ] **Career timeline** — горизонтальный таймлайн опыта работы с прогресс-баром, адаптировать их концепцию 0→21hr под карьеру.
- [ ] **Frame corners** — декоративные L-скобки по углам терминала/карточек портфолио. Анимация stroke на hover через SVG `stroke-dashoffset`.
- [ ] **Film grain / blur** — `filter: blur(0.5px)` на текст терминала для мягкого киношного эффекта.
- [ ] **`mix-blend-mode: screen`** — hover-подсветка кнопок и иконок через screen-blend вместо opacity.
- [ ] **Easing** — заменить стандартные CSS transitions на `cubic-bezier(0.61, 1, 0.88, 1)` (ease-out-expo).

**Рекомендация начать:** цветовая палитра → film grain → frame corners. Палитра — база, от неё пляшут все остальные визуальные решения. Timeline — отдельная фича, её можно делать параллельно.

### Код / доступность
- [ ] Тесты на основные view/home page
- [ ] `aria-label` на иконках GitHub/Telegram/Portfolio
- [ ] Начать использовать `requirements-dev.txt` в CI (mypy)
