# Dossier

Персональный сайт-визитка Сергея Кислякова — Python Django Developer.

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
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white&labelColor=4169E1)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white&labelColor=2496ED)

## Возможности

- Анимация печатной машинки для должности
- GitHub-статистика (звёзды, репозитории, языки)
- Секция портфолио с карточками проектов
- Ссылка на Telegram

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
- `git pull` → `pip install` → `collectstatic` → `restart gunicorn`

## Контакты

- GitHub: [skislyakow](https://github.com/skislyakow)
- Telegram: [@kislyakow](https://t.me/kislyakow)
