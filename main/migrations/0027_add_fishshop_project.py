from django.db import migrations, models


# FishShop + паритет таймлайна.
#
# 1) Проект FishShop (магазин морепродуктов в Telegram; README репо):
#    карточка в портфолио наверху + два навыка под теги (E100).
# 2) Паритет: на проде 5 проектных записей таймлайна заведены через admin
#    (Dossier/онлайн-библиотека/Ferma/Devman Bot/opencode-py), data-миграции
#    их не сидили — свежий migrate давал рельс без них. Синкаем по данным
#    прода (дамп /api/timeline/) + FishShop.
# 3) Хронологическая нумерация всех записей: Meta.ordering=['sort_order']
#    рулит и рельсом (/api/timeline/), и админкой; resume читает
#    prior/job/present c fallback'ом по sort_order (start_date в сиде None)
#    — порядок резюме становится prior → job → present, как на рельсе.
PROJECT = {
    'title': 'FishShop',
    'pypi': '',
    'role': 'Bot Development',
    'tagline': 'Магазин морепродуктов прямо в Telegram: каталог, корзина и заказ в мессенджере',
    'features': [
        'Каталог из Strapi: карточки товаров с фото, ценой и описанием',
        'Корзина: повторный тап увеличивает количество, позиция убирается без пересоздания',
        'Конечный автомат на Redis: 6 состояний диалога переживают перезапуск бота',
        'Почта покупателя проверяется и сохраняется в CMS через REST API',
        'Ретраи и лимиты Telegram гасятся в sending — сбой связи не рвёт диалог',
        'Бэкенд — Strapi 5 в отдельном репозитории FishShop-CMS',
    ],
    'tags': ['Python', 'Telegram', 'python-telegram-bot', 'requests', 'Redis', 'Strapi'],
    'links': {'cms': 'https://github.com/skislyakow/FishShop-CMS'},
    'badges_config': [
        {'label': 'stars', 'source': 'github_stars'},
        {'label': 'license', 'source': 'github_license'},
        {'label': 'language', 'source': 'github_lang'},
        {'label': 'updated', 'source': 'github_updated'},
        {'label': 'Python'},
        {'label': 'python-telegram-bot'},
        {'label': 'Redis'},
        {'label': 'Strapi'},
        {'label': 'uv'},
    ],
    'screenshot': 'https://raw.githubusercontent.com/skislyakow/FishShop/main/docs/screenshots/01-catalog.png',
    'date_label': '',
    'sort_order': 0,
    'is_published': True,
}

# Навыки под теги FishShop (E100: каждый тег проекта имеет навык).
SKILLS = [
    {'name': 'python-telegram-bot', 'category': 'bots'},
    {'name': 'Strapi', 'category': 'backend'},
]

# Синк прод-таймлайна: (repo, date_label, title, description) — данные
# сняты с дампа /api/timeline/ прода; FishShop добавляется последним.
TIMELINE_SYNC = [
    ('skislyakow/dossier', 'Апрель 2026', 'Dossier',
     'Персональный сайт-визитка: Django + Gunicorn + Nginx на VPS, CI/CD через GitHub Actions'),
    ('skislyakow/online_library', 'Июнь 2026', 'Онлайн библиотека',
     'Генератор статического сайта на Jinja2 + Bootstrap 5. 92 книги с пагинацией, обложками и чтением онлайн.'),
    ('skislyakow/ferma', 'Июнь 2026', 'Ferma',
     'Автоматизированная ферма Telegram-каналов: парсинг доноров, фильтрация рекламы, автоперевод, CPA-ссылки.'),
    ('skislyakow/devman-bot', 'Июнь 2026', 'Devman Bot',
     'Telegram-бот для уведомлений о проверке работ на Devman через Long Polling API.'),
    ('skislyakow/opencode-py', 'Июль 2026', 'opencode-py',
     'Python SDK для opencode AI агента: sync + async API, SSE-стриминг, опубликован на PyPI.'),
    ('skislyakow/FishShop', 'Октябрь 2026', 'FishShop',
     'Магазин морепродуктов в Telegram: каталог и корзина на python-telegram-bot, бэкенд — Strapi, состояния диалогов в Redis.'),
]

# Хронология рельса: prior → job → проекты (Апрель…Октябрь) → present.
TYPE_ORDER = {'prior': 0, 'job': 1, 'present': 11}
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
}


def forwards(apps, schema_editor):
    Project = apps.get_model('main', 'Project')
    Skill = apps.get_model('main', 'Skill')
    TimelineItem = apps.get_model('main', 'TimelineItem')

    # --- Project: FishShop наверх, существующие сдвигаются +1 ---
    Project.objects.all().update(sort_order=models.F('sort_order') + 1)
    Project.objects.update_or_create(repo='skislyakow/FishShop', defaults=PROJECT)

    # --- Skills: get_or_create, sort = max + 1 (0016/0025-паттерн) ---
    max_sort = Skill.objects.aggregate(m=models.Max('sort_order'))['m'] or 0
    for i, skill in enumerate(SKILLS):
        Skill.objects.get_or_create(
            name=skill['name'],
            defaults={'category': skill['category'], 'sort_order': max_sort + 1 + i},
        )

    # --- Timeline: синк прод-записей + FishShop (update_or_create по repo) ---
    for repo, date_label, title, description in TIMELINE_SYNC:
        TimelineItem.objects.update_or_create(
            repo=repo,
            defaults={
                'item_type': 'project',
                'date_label': date_label,
                'title': title,
                'description': description,
                'role': '',
                'date_range': '',
                'sort_order': PROJECT_ORDER[repo],
            },
        )

    # --- Глобальная хронологическая нумерация ---
    for item in TimelineItem.objects.all():
        new_sort = TYPE_ORDER.get(item.item_type, PROJECT_ORDER.get(item.repo, item.sort_order))
        if new_sort != item.sort_order:
            item.sort_order = new_sort
            item.save(update_fields=['sort_order'])


def backwards(apps, schema_editor):
    Project = apps.get_model('main', 'Project')
    Skill = apps.get_model('main', 'Skill')
    TimelineItem = apps.get_model('main', 'TimelineItem')

    # FishShop и синкнутые записи — удалить; нумерация prior/job/present и
    # проектов не восстанавливается (значения на проде admin-перенумерованные,
    # обратим только само содержимое — как в 0024).
    TimelineItem.objects.filter(repo='skislyakow/FishShop').delete()
    for repo, _date, _title, _desc in TIMELINE_SYNC:
        if repo != 'skislyakow/FishShop':
            TimelineItem.objects.filter(repo=repo, item_type='project').delete()
    Project.objects.filter(repo='skislyakow/FishShop').delete()
    Project.objects.filter(sort_order__gte=1).update(sort_order=models.F('sort_order') - 1)
    Skill.objects.filter(name__in=[s['name'] for s in SKILLS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0026_fix_dossier_card'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
