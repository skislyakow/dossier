from django.db import migrations, models


# Yandex Afisha — интерактивная карта интересных мест Москвы (README репо):
# Django 6 + Leaflet + Vue.js 2, WYSIWYG-редактор, drag-and-drop в админке,
# JSON API мест. Навыки — только те, которых нет в сиде (теги проекта
# обязаны иметь Skill-кнопку, audit E100); категории зеркалят логику
# существующих (карта/фронтенд → web).
PROJECT = {
    'title': 'Yandex Afisha',
    'pypi': '',
    'role': 'Web Development',
    'tagline': 'Интерактивная карта интересных мест Москвы: Django, Leaflet и Vue.js с WYSIWYG-редактором и JSON API',
    'features': [
        'Интерактивная карта Москвы (Leaflet) с метками и детальной карточкой места — описание и фотографии',
        'Наполнение контента через WYSIWYG-редактор (django-tinymce) прямо в админке',
        'Админка с drag-and-drop сортировкой фотографий (django-admin-sortable2)',
        'JSON API GET /places/<id>/ с координатами, описаниями и списком фото',
        'Команда load_place: импорт/обновление места из JSON по ссылке (автоконвертация GitHub → raw)',
        'Прод-конфигурация: PostgreSQL через dj_database_url, gunicorn + nginx, статика collectstatic',
    ],
    'tags': ['Python', 'Django', 'SQLite', 'Bootstrap', 'Leaflet', 'Vue 2', 'REST API'],
    'links': {},
    'badges_config': [
        {'label': 'stars', 'source': 'github_stars'},
        {'label': 'license', 'source': 'github_license'},
        {'label': 'language', 'source': 'github_lang'},
        {'label': 'updated', 'source': 'github_updated'},
        {'label': 'Python'},
        {'label': 'Django'},
        {'label': 'Leaflet'},
        {'label': 'Vue 2'},
        {'label': 'Bootstrap'},
        {'label': 'SQLite'},
    ],
    # Скриншотов в репо нет (только favicon) — плейсхолдер-монограмма.
    'screenshot': '',
    'date_label': '',
    'sort_order': 0,
    'is_published': True,
}

# Навыки под теги проекта, которых нет в сиде (get_or_create, sort = max + 1).
SKILLS = [
    ('Leaflet', 'web'),
    ('Vue 2', 'web'),
]

# Таймлайн: Yandex Afisha (Июль 2026, дата создания репо 06.07.2026) после
# opencode-py, present → 16.
TIMELINE = {
    'item_type': 'project',
    'date_label': 'Июль 2026',
    'title': 'Yandex Afisha',
    'description': 'Интерактивная карта интересных мест Москвы: метки на Leaflet, карточки мест с фото, WYSIWYG-редактор и JSON API на Django.',
    'role': '',
    'date_range': '',
    'sort_order': 8,
}

# Хронология рельса (0027-паттерн, нумерация после вставки на 8-е место).
TYPE_ORDER = {'prior': 0, 'job': 1, 'present': 16}
PROJECT_ORDER = {
    'skislyakow/dossier': 2,
    'skislyakow/online_library': 3,
    'skislyakow/ferma': 4,
    'skislyakow/devman-bot': 5,
    'skislyakow/Devman-monitor': 6,
    'skislyakow/opencode-py': 7,
    'skislyakow/yandex-afisha': 8,
    'skislyakow/support-bot': 9,
    'skislyakow/quiz-bot': 10,
    'skislyakow/FishShop': 11,
    'skislyakow/SelfStorage': 12,
    'skislyakow/star-burger': 13,
    'skislyakow/BakeCake': 14,
    'skislyakow/fastai-api': 15,
}


def forwards(apps, schema_editor):
    Project = apps.get_model('main', 'Project')
    Skill = apps.get_model('main', 'Skill')
    TimelineItem = apps.get_model('main', 'TimelineItem')

    # --- Project: Yandex Afisha наверх, существующие сдвигаются +1 (0027-паттерн) ---
    Project.objects.all().update(sort_order=models.F('sort_order') + 1)
    Project.objects.update_or_create(repo='skislyakow/yandex-afisha', defaults=PROJECT)

    # --- Skills: get_or_create, sort = max + 1 (0016/0025/0028-паттерн) ---
    max_sort = Skill.objects.aggregate(m=models.Max('sort_order'))['m'] or 0
    for i, (name, category) in enumerate(SKILLS):
        Skill.objects.get_or_create(
            name=name,
            defaults={'category': category, 'sort_order': max_sort + 1 + i},
        )

    # --- Timeline: запись Yandex Afisha (Июль 2026) после opencode-py ---
    TimelineItem.objects.update_or_create(
        repo='skislyakow/yandex-afisha',
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

    # Контент удаляется, нумерация возвращается к состоянию 0033: проекты
    # сдвигаются -1, present → 15 (прочие sort'ы на проде admin-перенумерованные,
    # восстанавливаем только созданное здесь — как в 0024/0027).
    TimelineItem.objects.filter(repo='skislyakow/yandex-afisha').delete()
    TimelineItem.objects.filter(item_type='present').update(sort_order=15)
    Project.objects.filter(repo='skislyakow/yandex-afisha').delete()
    Project.objects.filter(sort_order__gte=1).update(sort_order=models.F('sort_order') - 1)
    Skill.objects.filter(name__in=[name for name, _ in SKILLS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0033_add_star_burger_project'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
