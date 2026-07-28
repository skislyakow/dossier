from django.core.management.base import BaseCommand
from main.models import Skill, Project, TimelineItem, ContactInfo


class Command(BaseCommand):
    help = 'Seed initial data for the portfolio site'

    def handle(self, *args, **options):
        self._seed_skills()
        self._seed_projects()
        self._seed_timeline()
        self._seed_contacts()
        self.stdout.write(self.style.SUCCESS('All data seeded successfully'))

    def _seed_skills(self):
        Skill.objects.all().delete()
        skills = [
            ('Python', 'xl', 0, 'python'),
            ('Django', 'lg', 1, 'api'),
            ('SQLite', 'md', 2, 'database'),
            ('Docker', 'md', 3, 'deployed_code'),
            ('Nginx', 'md', 4, 'cloud'),
            ('Gunicorn', 'md', 5, 'dns'),
            ('Ubuntu', 'md', 6, 'computer'),
            ('Git', 'md', 7, 'commit'),
            ('REST API', 'md', 8, 'api'),
            ('asyncio', 'sm', 9, 'sync_alt'),
            ('requests', 'sm', 10, 'http'),
            ('httpx', 'sm', 11, 'http'),
            ('Pydantic', 'sm', 12, 'schema'),
            ('PyPI', 'sm', 13, 'package'),
            ('Jinja2', 'sm', 14, 'code'),
            ('Bootstrap', 'sm', 15, 'design_services'),
            ('GitHub Actions', 'sm', 16, 'deployed_code_update'),
            ('HTML', 'sm', 17, 'html'),
            ('CSS', 'sm', 18, 'css'),
            ('JavaScript', 'sm', 19, 'javascript'),
            ('opencode-py', 'sm', 20, 'smart_toy'),
        ]
        for name, size, order, icon in skills:
            Skill.objects.create(name=name, size=size, sort_order=order, icon=icon)
        self.stdout.write(f'  Created {len(skills)} skills')

    def _seed_projects(self):
        Project.objects.all().delete()
        projects = [
            Project(
                repo='skislyakow/opencode-py',
                pypi='opencode-py',
                title='Opencode Python SDK',
                role='Python SDK Development',
                tagline='Python SDK для open source AI coding агента',
                features=[
                    'Published on PyPI — pip install opencode-py',
                    'Sync + Async API со streaming и сессиями',
                    'Встроенный Web UI (ноль зависимостей)',
                ],
                links={'pypi': 'https://pypi.org/project/opencode-py/'},
                badges_config=[
                    {'label': 'pypi', 'source': 'pypi_version'},
                    {'label': 'python', 'source': 'pypi_python'},
                    {'label': 'license', 'source': 'pypi_license'},
                    {'label': 'downloads/m', 'source': 'pypistats_month'},
                    {'label': 'downloads total', 'source': 'pypistats_total'},
                    {'label': 'build', 'value': 'hatchling'},
                    {'label': 'http', 'value': 'httpx'},
                ],
                sort_order=0,
            ),
            Project(
                repo='skislyakow/ferma',
                title='Ferma',
                role='Fullstack Development',
                tagline='Автоматизированная ферма Telegram-каналов',
                features=[
                    'Парсинг постов с t.me/s/ доноров',
                    'Фильтрация рекламы, тизеров, дубликатов',
                    'Автоперевод через Yandex Translate',
                    'Публикация в каналы с CPA-ссылками',
                ],
                links={},
                badges_config=[
                    {'label': 'stars', 'source': 'github_stars'},
                    {'label': 'license', 'source': 'github_license'},
                    {'label': 'language', 'source': 'github_lang'},
                ],
                sort_order=1,
            ),
            Project(
                repo='skislyakow/devman-bot',
                title='Devman Bot',
                role='Bot Development',
                tagline='Telegram-бот для уведомлений о проверке работ на Devman',
                features=[
                    'Long Polling API для мгновенных уведомлений',
                    'Автоматическая отправка результатов в Telegram',
                    'Поддержка .env для токенов',
                ],
                links={},
                badges_config=[
                    {'label': 'stars', 'source': 'github_stars'},
                    {'label': 'license', 'source': 'github_license'},
                    {'label': 'updated', 'source': 'github_updated'},
                    {'label': 'Python'},
                    {'label': 'python-telegram-bot'},
                    {'label': 'requests'},
                    {'label': 'Long Polling'},
                ],
                sort_order=2,
            ),
            Project(
                repo='skislyakow/dossier',
                title='Dossier',
                role='Fullstack Development',
                tagline='Персональный сайт-визитка с production-стеком и CI/CD',
                features=[
                    'Интерактивный терминал с AI-ассистентом (opencode-py, SSE-стриминг)',
                    'Typing-анимация должности на чистом JavaScript (без библиотек)',
                    'Skills cloud — облако тегов с технологиями',
                    'Секция портфолио с карточками проектов, бейджами и распределением языков',
                    'Production: Django + Gunicorn + Nginx на Ubuntu VPS',
                    'Автодеплой через GitHub Actions',
                ],
                links={'www': 'https://kislyakov.pro/'},
                badges_config=[
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
                ],
                sort_order=3,
            ),
            Project(
                repo='skislyakow/online_library',
                title='Онлайн библиотека',
                role='Web Development',
                tagline='Статический сайт онлайн-библиотеки с пагинацией и чтением книг',
                features=[
                    '92 книги с обложками, авторами и жанрами',
                    'Пагинация — 20 книг на страницу',
                    'Bootstrap 5 — адаптивная сетка',
                    'Jinja2-шаблоны и генерация статики на Python',
                    'Публикация на GitHub Pages',
                ],
                links={'www': 'https://skislyakow.github.io/online_library/'},
                badges_config=[
                    {'label': 'stars', 'source': 'github_stars'},
                    {'label': 'license', 'source': 'github_license'},
                    {'label': 'language', 'source': 'github_lang'},
                    {'label': 'Python'},
                    {'label': 'HTML'},
                    {'label': 'CSS'},
                    {'label': 'Bootstrap'},
                    {'label': 'Jinja2'},
                ],
                sort_order=4,
            ),
        ]
        Project.objects.bulk_create(projects)
        self.stdout.write(f'  Created {len(projects)} projects')

    def _seed_timeline(self):
        TimelineItem.objects.all().delete()
        items = [
            TimelineItem(
                item_type='job',
                date_label='Январь 2026',
                title='ЭФКО Цифровые решения',
                description='',
                url='https://efko.digital/',
                role='ИТ-Специалист',
                date_range='Январь 2026 — настоящее время',
                sort_order=0,
            ),
            TimelineItem(
                item_type='project',
                date_label='Апрель 2026',
                title='Dossier',
                description='Персональный сайт-визитка: Django + Gunicorn + Nginx на VPS, CI/CD через GitHub Actions',
                repo='skislyakow/dossier',
                sort_order=1,
            ),
            TimelineItem(
                item_type='project',
                date_label='Июнь 2026',
                title='Онлайн библиотека',
                description='Генератор статического сайта на Jinja2 + Bootstrap 5. 92 книги с пагинацией, обложками и чтением онлайн.',
                repo='skislyakow/online_library',
                sort_order=2,
            ),
            TimelineItem(
                item_type='project',
                date_label='Июнь 2026',
                title='Ferma',
                description='Автоматизированная ферма Telegram-каналов: парсинг доноров, фильтрация рекламы, автоперевод, CPA-ссылки.',
                repo='skislyakow/ferma',
                sort_order=3,
            ),
            TimelineItem(
                item_type='project',
                date_label='Июнь 2026',
                title='Devman Bot',
                description='Telegram-бот для уведомлений о проверке работ на Devman через Long Polling API.',
                repo='skislyakow/devman-bot',
                sort_order=4,
            ),
            TimelineItem(
                item_type='project',
                date_label='Июль 2026',
                title='opencode-py',
                description='Python SDK для opencode AI агента: sync + async API, SSE-стриминг, опубликован на PyPI.',
                repo='skislyakow/opencode-py',
                sort_order=5,
            ),
            TimelineItem(
                item_type='present',
                date_label='сейчас',
                title='Настоящее время',
                description='Продолжаю развиваться как Python-разработчик: pet-проекты, open-source, изучение новых технологий.',
                sort_order=6,
            ),
        ]
        TimelineItem.objects.bulk_create(items)
        self.stdout.write(f'  Created {len(items)} timeline items')

    def _seed_contacts(self):
        ContactInfo.objects.all().delete()
        contacts = [
            ContactInfo(
                contact_type='email',
                label='s.kislyakov84@gmail.com',
                value='s.kislyakov84@gmail.com',
                sort_order=0,
            ),
            ContactInfo(
                contact_type='telegram',
                label='@kislyakow',
                value='@kislyakow',
                sort_order=1,
            ),
        ]
        ContactInfo.objects.bulk_create(contacts)
        self.stdout.write(f'  Created {len(contacts)} contacts')
