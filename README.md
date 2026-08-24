# Dossier

Персональный сайт-визитка Сергея Кислякова — Python Fullstack Developer.

## Технологии

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white&labelColor=3776AB)
![Django](https://img.shields.io/badge/Django-092E20?style=flat-square&logo=django&logoColor=white&labelColor=092E20)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5&logoColor=white&labelColor=E34F26)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat-square&logo=css3&logoColor=white&labelColor=1572B6)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black&labelColor=F7DF1E)
![Nginx](https://img.shields.io/badge/Nginx-009639?style=flat-square&logo=nginx&logoColor=white&labelColor=009639)
![Gunicorn](https://img.shields.io/badge/Gunicorn-499848?style=flat-square&logo=gunicorn&logoColor=white&labelColor=499848)
![Git](https://img.shields.io/badge/Git-F05032?style=flat-square&logo=git&logoColor=white&labelColor=F05032)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat-square&logo=githubactions&logoColor=white&labelColor=2088FF)
![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=flat-square&logo=ubuntu&logoColor=white&labelColor=E95420)

## Возможности

- **Интерактивный терминал** — macOS-style окно с анимированным перечнем технологий и стека (typewriter на чистом JS)
- **Typing-анимация** должности на чистом JS (без библиотек)
- **Skills cloud** — облако тегов с технологиями + ghost-иконки, плавающие в фоне hero
- **Career timeline** — горизонтальная линия с точками (работа → проекты → настоящее время)
- **Портфолио** — карточки проектов с бейджами (GitHub API, PyPI, PyPistats), скриншотами или role-based placeholder-темами
- **Светлая/тёмная тема** — GitHub-style light + dark, переключатель в hero, сохраняется в localStorage
- **Соцсети с hover-лейблами** — иконка съезжает влево, появляется название
- **Drag-and-drop сортировка** в админке (django-admin-sortable2)
- **Django admin (unfold)** — управление контентом: навыки, проекты, таймлайн, контакты
- **Production-stек**: Django + Gunicorn + Nginx на Ubuntu VPS
- **CI/CD** через GitHub Actions (автодеплой при пуше в main)

## Сайт

:earth_americas: [kislyakov.pro](https://kislyakov.pro/)

## Запуск

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py runserver
```

Откройте http://127.0.0.1:8000/

## Деплой

При пуше в ветку `main` GitHub Actions автоматически деплоит сайт на VPS:

```
git pull → pip install → migrate → collectstatic → restart gunicorn
```

VPS: Ubuntu 24.04 | Nginx → Gunicorn (127.0.0.1:8000) | systemd | HTTPS (Let's Encrypt)

## Контакты

- GitHub: [skislyakow](https://github.com/skislyakow)
- Telegram: [@kislyakow](https://t.me/kislyakow)
