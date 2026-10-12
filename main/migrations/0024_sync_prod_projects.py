from django.db import migrations


# Полный контент-синк прод ↔ сид: проекты, заведённые на проде через admin
# (opencode-py, ferma, devman-bot, dossier, online_library), зеркалируются в
# data-миграцию, чтобы свежий локальный migrate == прод-БД. Данные сняты с
# прод-БД как есть (включая badges_config со статичными label-бейджами).
#
# Заодно закрывает W101: навыки mypy/pymorphy3, чей фильтр не находил тегов.
PROJECTS = [
    {
        'repo': 'skislyakow/opencode-py',
        'title': 'Opencode Python SDK',
        'pypi': 'opencode-py',
        'role': 'Python SDK Development',
        'tagline': 'Python SDK для open source AI coding агента',
        'features': [
            'Published on PyPI — pip install opencode-py',
            'Sync + Async API со streaming и сессиями',
            'Встроенный Web UI (ноль зависимостей)',
        ],
        'tags': ['Python', 'httpx', 'Pydantic', 'PyPI', 'opencode-py'],
        'links': {'pypi': 'https://pypi.org/project/opencode-py/'},
        'badges_config': [
            {'label': 'pypi', 'source': 'pypi_version'},
            {'label': 'python', 'source': 'pypi_python'},
            {'label': 'license', 'source': 'pypi_license'},
            {'label': 'downloads/m', 'source': 'pypistats_month'},
            {'label': 'downloads total', 'source': 'pypistats_total'},
            {'label': 'build', 'value': 'hatchling'},
            {'label': 'http', 'value': 'httpx'},
        ],
        'screenshot': '',
        'date_label': '',
        'sort_order': 0,
        'is_published': True,
    },
    {
        'repo': 'skislyakow/ferma',
        'title': 'Ferma',
        'pypi': '',
        'role': 'Fullstack Development',
        'tagline': 'Автоматизированная ферма Telegram-каналов',
        'features': [
            'Парсинг постов с t.me/s/ доноров',
            'Фильтрация рекламы, тизеров, дубликатов',
            'Автоперевод через Yandex Translate',
            'Публикация в каналы с CPA-ссылками',
        ],
        'tags': ['Python', 'FastAPI', 'SQLite', 'VK API', 'requests'],
        'links': {},
        'badges_config': [
            {'label': 'stars', 'source': 'github_stars'},
            {'label': 'license', 'source': 'github_license'},
            {'label': 'language', 'source': 'github_lang'},
        ],
        'screenshot': '',
        'date_label': '',
        'sort_order': 1,
        'is_published': True,
    },
    {
        'repo': 'skislyakow/devman-bot',
        'title': 'Devman Bot',
        'pypi': '',
        'role': 'Bot Development',
        'tagline': 'Telegram-бот для уведомлений о проверке работ на Devman',
        'features': [
            'Long Polling API для мгновенных уведомлений',
            'Автоматическая отправка результатов в Telegram',
            'Поддержка .env для токенов',
        ],
        'tags': ['Python', 'Telegram', 'requests', 'python-dotenv'],
        'links': {},
        'badges_config': [
            {'label': 'stars', 'source': 'github_stars'},
            {'label': 'license', 'source': 'github_license'},
            {'label': 'updated', 'source': 'github_updated'},
            {'label': 'Python'},
            {'label': 'python-telegram-bot'},
            {'label': 'requests'},
            {'label': 'Long Polling'},
        ],
        'screenshot': '',
        'date_label': '',
        'sort_order': 2,
        'is_published': True,
    },
    {
        'repo': 'skislyakow/dossier',
        'title': 'Dossier',
        'pypi': '',
        'role': 'Fullstack Development',
        'tagline': 'Персональный сайт-визитка с production-стеком и CI/CD',
        'features': [
            'Телеграм-бот для поддержки пользователей на Dialogflow (aiogram)',
            'Сайт-визитка kislyakov.pro: Django 6, zero-dependency JS/CSS, тёмная и светлая темы',
            'Авто-деплой на VPS через GitHub Actions: чек-гейт (ruff, mypy, pytest, node --check) → migrate → collectstatic → restart',
            'Инженерный процесс публичный: 56+ тестов, ADR-документы, audit_content, смоук прода',
            'Авто-резюме: PDF генерируется сервером из контента CMS (WeasyPrint), единый источник данных сайта и файла',
        ],
        'tags': [
            'Python', 'Django', 'Nginx', 'Gunicorn', 'GitHub Actions',
            'HTML', 'CSS', 'JavaScript', 'pytest', 'mypy',
        ],
        'links': {'www': 'https://kislyakov.pro/'},
        'badges_config': [
            {'label': 'stars', 'source': 'github_stars'},
            {'label': 'license', 'source': 'github_license'},
            {'label': 'updated', 'source': 'github_updated'},
            {'label': 'Python'},
            {'label': 'Django'},
            {'label': 'HTML'},
            {'label': 'CSS'},
            {'label': 'JavaScript'},
            {'label': 'Nginx'},
            {'label': 'Gunicorn'},
            {'label': 'Git'},
            {'label': 'GitHub Actions'},
            {'label': 'Ubuntu'},
            {'label': 'opencode-py'},
            {'label': 'pytest'},
        ],
        'screenshot': '',
        'date_label': '',
        'sort_order': 3,
        'is_published': True,
    },
    {
        'repo': 'skislyakow/online_library',
        'title': 'Онлайн библиотека',
        'pypi': '',
        'role': 'Web Development',
        'tagline': 'Статический сайт онлайн-библиотеки с пагинацией и чтением книг',
        'features': [
            '92 книги с обложками, авторами и жанрами',
            'Пагинация — 20 книг на страницу',
            'Bootstrap 5 — адаптивная сетка',
            'Jinja2-шаблоны и генерация статики на Python',
            'Публикация на GitHub Pages',
        ],
        'tags': ['Python', 'Jinja2', 'Bootstrap', 'GitHub Pages'],
        'links': {'www': 'https://skislyakow.github.io/online_library/'},
        'badges_config': [
            {'label': 'stars', 'source': 'github_stars'},
            {'label': 'license', 'source': 'github_license'},
            {'label': 'language', 'source': 'github_lang'},
            {'label': 'Python'},
            {'label': 'HTML'},
            {'label': 'CSS'},
            {'label': 'Bootstrap'},
            {'label': 'Jinja2'},
        ],
        'screenshot': '',
        'date_label': '',
        'sort_order': 4,
        'is_published': True,
    },
]

# W101: теги под профилактики mypy/pymorphy3 (клик по навыку должен находить проект).
TAG_ADD = [
    ('skislyakow/quiz-bot', 'pymorphy3'),
]


def seed(apps, schema_editor):
    Project = apps.get_model('main', 'Project')
    for data in PROJECTS:
        data = dict(data)
        repo = data.pop('repo')
        Project.objects.update_or_create(repo=repo, defaults=data)
    for repo, tag in TAG_ADD:
        for project in Project.objects.filter(repo=repo):
            if tag not in project.tags:
                project.tags = project.tags + [tag]
                project.save(update_fields=['tags'])


def rollback(apps, schema_editor):
    Project = apps.get_model('main', 'Project')
    for repo, tag in TAG_ADD:
        for project in Project.objects.filter(repo=repo):
            if tag in project.tags:
                project.tags = [t for t in project.tags if t != tag]
                project.save(update_fields=['tags'])
    Project.objects.filter(repo__in=[p['repo'] for p in PROJECTS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0023_seed_resume_profile'),
    ]

    operations = [
        migrations.RunPython(seed, rollback),
    ]