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
- `static/js/` — Scripts (typing.js, github.js, portfolio.js)
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
- Directions section: Telegram-боты, Django-сайты, API-интеграции, Python SDK, Парсинг данных, Автоматизация
- Skills panel: Python, Django, DRF, PostgreSQL, SQLite, Docker, Nginx, Gunicorn, GitHub Actions, Ubuntu, Git, REST API, asyncio, requests, httpx, Pydantic, PyPI, HTML, CSS, JavaScript
- GitHub stats toggle (stars, repos, languages via GitHub API)
- Portfolio section with project cards (GitHub data + badges)
- Dynamic badges from GitHub API, PyPI, PyPistats
- Telegram link

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
