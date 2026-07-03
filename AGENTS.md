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
Personal portfolio / visiting card site for Sergey Kislyakov (Python Django Developer).
- Typing animation for job title
- GitHub stats toggle (stars, repos, languages via GitHub API)
- Portfolio section with project cards (GitHub data + badges)
- Telegram link

## Adding a project to portfolio
Edit `static/js/portfolio.js` → append to `PORTFOLIO` array:
```js
{
  repo: "skislyakow/repo-name",
  title: "Project Title",
  tagline: "Short description",
  features: ["Feature 1", "Feature 2"],
  links: { pypi: "https://..." },
  badges: ["https://img.shields.io/..."],
}
```
Then push to `main` — site updates automatically.
