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