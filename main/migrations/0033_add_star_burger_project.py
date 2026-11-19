from django.db import migrations, models


# Star Burger — сайт доставки еды на Django (README репо): витрина с корзиной,
# панель менеджера, геокодер Яндекса, PostgreSQL + React-фронтенд, деплой за
# nginx/systemd. Навыки — только те, которых нет в сиде (теги проекта
# обязаны иметь Skill-кнопку, audit E100); категории зеркалят логику
# существующих (БД → backend как SQLite, фронтенд-библиотека → web как
# JavaScript).
PROJECT = {
    'title': 'Star Burger',
    'pypi': '',
    'role': 'Fullstack Development',
    'tagline': 'Доставка еды на Django: витрина с корзиной, панель менеджера и геокодер — PostgreSQL + React за nginx',
    'features': [
        'Витрина: меню по категориям, поиск, корзина, заказ без регистрации; цена фиксируется на сервере в момент заказа',
        'Статус заказа по подписанной ссылке (токен на SECRET_KEY, срок 30 дней), телефон маскируется, страница закрыта от индексации',
        'Панель менеджера: необработанные заказы, подсказка ресторанов по расстоянию (Яндекс.Геокодер с кэшем координат в БД), матрица доступности блюд',
        'PostgreSQL 16 + DRF: публичное API с throttling (30 заказов/час с IP), сумма заказа считается на стороне БД',
        'Прод-периметр: HTTPS-редирект, HSTS, secure-cookies, /healthz/ с проверкой базы, ошибки в Rollbar',
        'Качество кода: ruff + djlint + mypy + pytest-django/vitest в CI, деплой git pull → uv sync → migrate → systemd',
    ],
    'tags': ['Python', 'Django', 'Django REST Framework', 'PostgreSQL', 'React', 'JavaScript', 'Bootstrap', 'Nginx', 'Gunicorn', 'GitHub Actions', 'systemd', 'mypy', 'pytest', 'uv'],
    'links': {'www': 'https://star-burger.kislyakov.pro'},
    'badges_config': [
        {'label': 'stars', 'source': 'github_stars'},
        {'label': 'license', 'source': 'github_license'},
        {'label': 'language', 'source': 'github_lang'},
        {'label': 'updated', 'source': 'github_updated'},
        {'label': 'Python'},
        {'label': 'Django'},
        {'label': 'Django REST Framework'},
        {'label': 'PostgreSQL'},
        {'label': 'React'},
        {'label': 'Nginx'},
    ],
    # Скриншот витрины из README репо (raw-URL, паттерн FishShop 0027).
    'screenshot': 'https://raw.githubusercontent.com/skislyakow/star-burger/main/docs/screenshots/storefront.jpg',
    'date_label': '',
    'sort_order': 0,
    'is_published': True,
}

# Навыки под теги проекта, которых нет в сиде (get_or_create, sort = max + 1).
SKILLS = [
    ('PostgreSQL', 'backend'),
    ('React', 'web'),
]

# Таймлайн: Star Burger (Октябрь 2026) после SelfStorage, present → 15.
TIMELINE = {
    'item_type': 'project',
    'date_label': 'Октябрь 2026',
    'title': 'Star Burger',
    'description': 'Сайт доставки еды на Django: витрина с корзиной и заказом по подписанным ссылкам, панель менеджера с геокодером, PostgreSQL + React.',
    'role': '',
    'date_range': '',
    'sort_order': 12,
}

# Хронология рельса (0027-паттерн, нумерация после вставки в 12).
TYPE_ORDER = {'prior': 0, 'job': 1, 'present': 15}
PROJECT_ORDER = {
    'skislyakow/dossier': 2,
    'skislyakow/online_library': 3,
    'skislyakow/ferma': 4,
    'skislyakow/devman-bot': 5,
    'skislyakow/Devman-monitor': 6,
    'skislyakow/opencode-py': 7,
    'skislyakow/support-bot': 8,
    'skislyakow/quiz-bot': 9,
    'skislyakow/FishShop': 10,
    'skislyakow/SelfStorage': 11,
    'skislyakow/star-burger': 12,
    'skislyakow/BakeCake': 13,
    'skislyakow/fastai-api': 14,
}


def forwards(apps, schema_editor):
    Project = apps.get_model('main', 'Project')
    Skill = apps.get_model('main', 'Skill')
    TimelineItem = apps.get_model('main', 'TimelineItem')

    # --- Project: Star Burger наверх, существующие сдвигаются +1 (0027-паттерн) ---
    Project.objects.all().update(sort_order=models.F('sort_order') + 1)
    Project.objects.update_or_create(repo='skislyakow/star-burger', defaults=PROJECT)

    # --- Skills: get_or_create, sort = max + 1 (0016/0025/0028-паттерн) ---
    max_sort = Skill.objects.aggregate(m=models.Max('sort_order'))['m'] or 0
    for i, (name, category) in enumerate(SKILLS):
        Skill.objects.get_or_create(
            name=name,
            defaults={'category': category, 'sort_order': max_sort + 1 + i},
        )

    # --- Timeline: запись Star Burger (Октябрь 2026) после SelfStorage ---
    TimelineItem.objects.update_or_create(
        repo='skislyakow/star-burger',
        defaults=TIMELINE,
    )

    # --- Глобальная хронологическая нумерация (0027-паттерн) ---
    for item in TimelineItem.objects.all():
        new_sort = TYPE_ORDER.get(item.item_type, PROJECT_ORDER.get(item.repo, item.sort_order))
        if new_sort != item.sort_order:
            item.sort_order = new_sort
            item.save(update_fields=['sort_order'])


def backwards(apps, schema_editor):
    Project = apps.get_model('main', 'Project')
    Skill = apps.get_model('main', 'Skill')
    TimelineItem = apps.get_model('main', 'TimelineItem')

    # Контент удаляется, нумерация возвращается к состоянию 0032: проекты
    # сдвигаются -1, present → 14 (прочие sort'ы на проде admin-перенумерованные,
    # восстанавливаем только созданное здесь — как в 0024/0027).
    TimelineItem.objects.filter(repo='skislyakow/star-burger').delete()
    TimelineItem.objects.filter(item_type='present').update(sort_order=14)
    Project.objects.filter(repo='skislyakow/star-burger').delete()
    Project.objects.filter(sort_order__gte=1).update(sort_order=models.F('sort_order') - 1)
    Skill.objects.filter(name__in=[name for name, _ in SKILLS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0032_add_fastai_api_project'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
