from django.db import migrations, models


# SelfStorage (README репо: сервис аренды складских боксов, Django 5.2 + Bootstrap,
# демо-стенд selfstorage.kislyakov.pro):
# 1) Карточка в портфолио наверх (сдвиг остальных +1) + навык «ЮKassa» под тег (E100).
# 2) Запись таймлайна: хронологически после FishShop (Октябрь 2026),
#    present уезжает на +1 — как в 0027.
PROJECT = {
    'title': 'SelfStorage',
    'pypi': '',
    'role': 'Fullstack Development',
    'tagline': 'Сервис аренды складских боксов: каталог, визард оформления, оплата через ЮKassa и QR-доступ',
    'features': [
        'Каталог из 5 складов и боксов с фильтром по площади; аренда оформляется визардом с серверной валидацией каждого шага (django-formtools)',
        'Оплата через API ЮKassa: редирект на оплату, возврат по return_url и webhook о смене статуса; промокоды со сроком действия',
        'QR-код для открытия бокса; личный кабинет с активными арендами, историей платежей и уведомлениями (колокольчик со счётчиком)',
        'Письма и напоминания: «оплата получена», окончание аренды за 30/14/7/3 дня и просрочка — management-команда + systemd timer',
        'Дашборд владельца: занятость боксов, заказы, выручка и заявки на доставку; прод-стенд на nginx + gunicorn под systemd, CI (ruff, mypy, тесты)',
    ],
    'tags': [
        'Python', 'Django', 'SQLite', 'Bootstrap', 'HTML', 'CSS', 'JavaScript',
        'Nginx', 'Gunicorn', 'GitHub Actions', 'systemd', 'mypy', 'ЮKassa',
    ],
    'links': {'www': 'https://selfstorage.kislyakov.pro'},
    'badges_config': [
        {'label': 'stars', 'source': 'github_stars'},
        {'label': 'license', 'source': 'github_license'},
        {'label': 'language', 'source': 'github_lang'},
        {'label': 'updated', 'source': 'github_updated'},
        {'label': 'Python'},
        {'label': 'Django'},
        {'label': 'SQLite'},
        {'label': 'Bootstrap'},
        {'label': 'ЮKassa'},
        {'label': 'GitHub Actions'},
    ],
    'screenshot': 'https://raw.githubusercontent.com/skislyakow/SelfStorage/main/docs/img/home.webp',
    'date_label': '',
    'sort_order': 0,
    'is_published': True,
}

# Навык под тег SelfStorage (E100: каждый тег проекта имеет навык).
SKILLS = [
    {'name': 'ЮKassa', 'category': 'backend'},
]

TIMELINE_REPO = 'skislyakow/SelfStorage'
TIMELINE_SORT = 11  # после FishShop (10), перед present (11 на проде)
TIMELINE_DEFAULTS = {
    'item_type': 'project',
    'date_label': 'Октябрь 2026',
    'title': 'SelfStorage',
    'description': 'Сервис аренды складских боксов: визард оформления, оплата через ЮKassa, QR-доступ к боксу и уведомления.',
    'role': '',
    'date_range': '',
}


def forwards(apps, schema_editor):
    Project = apps.get_model('main', 'Project')
    Skill = apps.get_model('main', 'Skill')
    TimelineItem = apps.get_model('main', 'TimelineItem')

    # present освобождает место (сдвиг +1), затем SelfStorage встаёт после FishShop
    TimelineItem.objects.filter(item_type='present').update(
        sort_order=models.F('sort_order') + 1
    )
    TimelineItem.objects.update_or_create(
        repo=TIMELINE_REPO,
        defaults={**TIMELINE_DEFAULTS, 'sort_order': TIMELINE_SORT},
    )

    # Карточка наверх портфолио, существующие сдвигаются +1
    Project.objects.all().update(sort_order=models.F('sort_order') + 1)
    Project.objects.update_or_create(repo='skislyakow/SelfStorage', defaults=PROJECT)

    # Навыки: get_or_create, sort = max + 1 (0016/0025/0027-паттерн)
    max_sort = Skill.objects.aggregate(m=models.Max('sort_order'))['m'] or 0
    for i, skill in enumerate(SKILLS):
        Skill.objects.get_or_create(
            name=skill['name'],
            defaults={'category': skill['category'], 'sort_order': max_sort + 1 + i},
        )


def backwards(apps, schema_editor):
    Project = apps.get_model('main', 'Project')
    Skill = apps.get_model('main', 'Skill')
    TimelineItem = apps.get_model('main', 'TimelineItem')

    TimelineItem.objects.filter(repo=TIMELINE_REPO).delete()
    TimelineItem.objects.filter(item_type='present').update(
        sort_order=models.F('sort_order') - 1
    )

    Project.objects.filter(repo='skislyakow/SelfStorage').delete()
    Project.objects.filter(sort_order__gte=1).update(sort_order=models.F('sort_order') - 1)

    Skill.objects.filter(name__in=[s['name'] for s in SKILLS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0029_update_dossier_card'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
