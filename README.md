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

- **Портфолио** — Усиленные карточки проектов: таглайн, буллеты результата, бейджи (GitHub API, PyPI, PyPistats) и ссылки на светлой карточке; каскадное появление без скролл-обсервера, список названий виден сразу, умеренный magnetic-hover (отключается при `prefers-reduced-motion`); фильтры списка: по роли (curly `{ роль: N }`), облако тегов `{ тег: N }` с кеглем по частоте и кликабельные навыки — клик по технологии открывает портфолио и фильтрует по тегу
- **Опыт** — секция-хронология: до-2026 запись → работа → проекты → настоящее время, вертикальная лента с датами; справа — рельс-навигатор (в hero — с датами, дальше — компактная полоса с подписями по наведению), клик по точке ведёт к строке секции
- **Навыки по категориям** — секция Skills — сетка, сгруппированная по зонам экспертизы (Backend / Web / DevOps / Bots & Integrations / Tools), пустые категории не показываются
- **Контакты** — секция тремя крупными каналами (email / Telegram / GitHub): карточки из ContactInfo с меткой `{ контакты: N }`, ссылки кликабельны (mailto / t.me / github.com)
- **Светлая/тёмная тема** — GitHub-style light + dark, переключатель в hero, сохраняется в localStorage
- **Marquee-строка технологий** — бесшовная бегущая строка между hero и контентом (анимация отключается при `prefers-reduced-motion`)
- **Соцсети с hover-лейблами** — иконка съезжает влево, появляется название (квадратные рамки, акцент на hover)
- **Django admin (unfold)** — управление контентом: навыки, проекты, опыт, контакты; drag-and-drop сортировка записей
- **Production-стек**: Django + Gunicorn + Nginx на Ubuntu VPS
- **CI/CD** через GitHub Actions (автодеплой при пуше в main)

## Сайт

:earth_americas: [kislyakov.pro](https://kislyakov.pro/)

## Запуск

```bash
uv sync --frozen
uv run manage.py runserver
```

Откройте http://127.0.0.1:8000/

Нужен [uv](https://docs.astral.sh/uv/): `pip install uv`.

## Деплой

При пуше в ветку `main` GitHub Actions автоматически деплоит сайт на VPS:

```
git pull → uv sync --frozen --no-dev → migrate → createcachetable → collectstatic → restart gunicorn
```

VPS: Ubuntu 24.04 | Nginx → Gunicorn (127.0.0.1:8000) | systemd | HTTPS (Let's Encrypt)

## Контакты

- GitHub: [skislyakow](https://github.com/skislyakow)
- Telegram: [@kislyakow](https://t.me/kislyakow)
