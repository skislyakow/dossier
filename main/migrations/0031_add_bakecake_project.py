from django.db import migrations, models


# BakeCake (README репо: конструктор тортов с живым SVG-предпросмотром,
# Django 5.2 + DRF + Vue 3, оплата ЮKassa, демо-стенд bakecake.kislyakov.pro):
# 1) Карточка в портфолио наверх (сдвиг остальных +1) + 4 навыка под новые теги (E100).
# 2) Запись таймлайна: хронологически после SelfStorage (Октябрь 2026),
#    т.к. репо создано в сентябре, разработка — в ноябре 2026;
#    present уезжает на +1 — как в 0027/0030.
PROJECT = {
    'title': 'BakeCake',
    'pypi': '',
    'role': 'Fullstack Development',
    'tagline': 'Конструктор тортов с живым SVG-предпросмотром: сборка, оплата ЮKassa и админка с аналитикой',
    'features': [
        'Конструктор: пять групп опций (ярусы, форма, топпинг, ягоды, декор) собираются в SVG-предпросмотр; цену считает сервер, а заказ хранит снимок состава и цен — история не меняется вслед за прайсом',
        'Витрина и оформление: каталог по поводам, доставка с окном 10:00–23:00, срочный заказ с надбавкой 20 %, промокоды, согласие на ПДП с датой, IP и версией документа',
        'Оплата через ЮKassa: редирект и webhook, идемпотентность платежей, статусы pending/succeeded/canceled; заказы new/paid/delivered с историей изменений',
        'Личный кабинет (вход по телефону, история, «повторить заказ», жалобы) и тематическая админка: сводка по выручке, конверсии и каналам, доставки на сегодня/завтра, выгрузка CSV',
        'Инженерия: API на Django REST Framework с единым форматом ответов, pytest и pyright, CI на каждый push, идемпотентный seed и автодеплой на VPS под nginx + gunicorn + systemd',
    ],
    'tags': [
        'Python', 'Django', 'Django REST Framework', 'Vue 3', 'VeeValidate',
        'SQLite', 'Bootstrap', 'HTML', 'CSS', 'JavaScript', 'Nginx', 'Gunicorn',
        'GitHub Actions', 'systemd', 'ЮKassa', 'pytest', 'pyright',
    ],
    'links': {'www': 'https://bakecake.kislyakov.pro/'},
    'badges_config': [
        {'label': 'stars', 'source': 'github_stars'},
        {'label': 'license', 'source': 'github_license'},
        {'label': 'language', 'source': 'github_lang'},
        {'label': 'updated', 'source': 'github_updated'},
        {'label': 'Python'},
        {'label': 'Django'},
        {'label': 'Django REST Framework'},
        {'label': 'Vue 3'},
        {'label': 'SQLite'},
        {'label': 'Bootstrap'},
        {'label': 'ЮKassa'},
        {'label': 'pytest'},
    ],
    'screenshot': 'https://raw.githubusercontent.com/skislyakow/BakeCake/main/docs/screenshots/configurator.png',
    'date_label': '',
    'sort_order': 0,
    'is_published': True,
}

# Навыки под новые теги BakeCake (E100: каждый тег проекта имеет навык).
SKILLS = [
    {'name': 'Django REST Framework', 'category': 'backend'},
    {'name': 'Vue 3', 'category': 'web'},
    {'name': 'VeeValidate', 'category': 'web'},
    {'name': 'pyright', 'category': 'tools'},
]

TIMELINE_REPO = 'skislyakow/BakeCake'
TIMELINE_SORT = 12  # после SelfStorage (11), перед present (12 на проде)
TIMELINE_DEFAULTS = {
    'item_type': 'project',
    'date_label': 'Ноябрь 2026',
    'title': 'BakeCake',
    'description': 'Конструктор тортов с живым SVG-предпросмотром: серверный расчёт цены, оплата ЮKassa, личный кабинет и админка с аналитикой.',
    'role': '',
    'date_range': '',
}


def forwards(apps, schema_editor):
    Project = apps.get_model('main', 'Project')
    Skill = apps.get_model('main', 'Skill')
    TimelineItem = apps.get_model('main', 'TimelineItem')

    # present освобождает место (сдвиг +1), затем BakeCake встаёт после SelfStorage
    TimelineItem.objects.filter(item_type='present').update(
        sort_order=models.F('sort_order') + 1
    )
    TimelineItem.objects.update_or_create(
        repo=TIMELINE_REPO,
        defaults={**TIMELINE_DEFAULTS, 'sort_order': TIMELINE_SORT},
    )

    # Карточка наверх портфолио, существующие сдвигаются +1
    Project.objects.all().update(sort_order=models.F('sort_order') + 1)
    Project.objects.update_or_create(repo='skislyakow/BakeCake', defaults=PROJECT)

    # Навыки: get_or_create, sort = max + 1 (0016/0025/0027/0030-паттерн)
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

    Project.objects.filter(repo='skislyakow/BakeCake').delete()
    Project.objects.filter(sort_order__gte=1).update(sort_order=models.F('sort_order') - 1)

    Skill.objects.filter(name__in=[s['name'] for s in SKILLS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0030_add_selfstorage_project'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
