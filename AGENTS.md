# Agents

## Setup
- Virtual environment: `.venv/`
- Django version: 6.0.4
- Run dev server: `python manage.py runserver`

## Structure
- `config/` — Django project settings (settings.py, urls.py, wsgi.py, asgi.py)
- `main/` — Main app with views and templates
- `templates/` — HTML templates
- `static/` — CSS, JS, images

## Dev workflow
1. Edit code
2. Run server to verify: `python manage.py runserver`
3. Visit `http://127.0.0.1:8000/`

## Notes
- This is a simple visiting card site (Sergey Kislyakov, Python Django Developer)
- Admin panel and models not needed yet
- Static files served from `static/` directory

## Task: Portfolio Section (2026-07-03)

### Current state
- Site has GitHub stats toggle and Telegram link
- Portfolio feature is work-in-progress

### What's done
- AGENTS.md updated with task context

### What to do next
- `static/js/portfolio.js` — массив проектов + фетч из GitHub API + рендер карточек
- `templates/index.html` — добавить кнопку Portfolio и подключить portfolio.js
- `static/css/style.css` — стили для карточек портфолио

### Portfolio data structure (JS)
```js
const PORTFOLIO = [
  {
    repo: "skislyakow/opencode-py",
    title: "Opencode Python SDK",
    tagline: "Python SDK для open source AI coding агента",
    features: [
      "Published on PyPI — pip install opencode-py",
      "Sync + Async API со streaming и сессиями",
      "Встроенный Web UI (ноль зависимостей)",
    ],
    links: {
      pypi: "https://pypi.org/project/opencode-py/",
    },
  },
];
```

### How to add projects
1. Append new entry to `PORTFOLIO` array with `repo`, `title`, `tagline`, `features`, `links`
2. Verify with `python manage.py runserver`