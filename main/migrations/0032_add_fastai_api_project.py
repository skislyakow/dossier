from django.db import migrations, models


# FastAI API — генератор сайтов на FastAPI (README репо): DeepSeek + LangGraph
# стримит HTML, Unsplash — картинки, MinIO (S3) — хранение, Gotenberg —
# скриншоты. Навыки — только те, которых нет в сиде (теги проекта обязаны
# иметь Skill-кнопку, audit E100); категории зеркалят логику существующих
# (внешний AI-API → Bots & Integrations как Dialogflow, инфра-сервисы →
# devops, пакетный менеджер → tools как PyPI).
PROJECT = {
    'title': 'FastAI API',
    'pypi': '',
    'role': 'Python API Development',
    'tagline': 'Генератор сайтов на FastAPI: LLM пишет HTML, картинки из Unsplash, файлы в S3 и скриншоты через Gotenberg',
    'features': [
        'Стриминг HTML: LangGraph генерирует страницу по мере создания и отдаёт потоком',
        'Генерация в фоне: сохранение в S3 и скриншот — фоновой задачей, до готовности отдаются заглушки',
        'Картинки из Unsplash и скриншоты через Gotenberg (headless-браузер)',
        'MinIO (S3) через aioboto3: HTML и изображения с MIME-типами и Content-Disposition',
        'REST API под префиксом /frontend-api с Swagger-документацией',
        'Конфигурация через Pydantic Settings: группы DeepSeek/Unsplash/S3/Gotenberg, секреты в .env',
    ],
    'tags': ['Python', 'FastAPI', 'Pydantic', 'DeepSeek', 'LangChain', 'MinIO', 'Gotenberg', 'REST API', 'uv'],
    'links': {},
    'badges_config': [
        {'label': 'stars', 'source': 'github_stars'},
        {'label': 'license', 'source': 'github_license'},
        {'label': 'language', 'source': 'github_lang'},
        {'label': 'updated', 'source': 'github_updated'},
        {'label': 'Python'},
        {'label': 'FastAPI'},
        {'label': 'Pydantic'},
        {'label': 'DeepSeek'},
        {'label': 'LangChain'},
        {'label': 'MinIO'},
    ],
    # Скриншотов в репо нет (stub/screenshot.jpg — генеричная заглушка API),
    # карточка идёт с плейсхолдером-монограммой.
    'screenshot': '',
    'date_label': '',
    'sort_order': 0,
    'is_published': True,
}

# Навыки под теги проекта, которых нет в сиде (get_or_create, sort = max + 1).
SKILLS = [
    ('DeepSeek', 'bots'),
    ('LangChain', 'backend'),
    ('MinIO', 'devops'),
    ('Gotenberg', 'devops'),
    ('uv', 'tools'),
]

# Таймлайн: FastAI API (Ноябрь 2026) после BakeCake, present сдвигается на 14.
TIMELINE = {
    'item_type': 'project',
    'date_label': 'Ноябрь 2026',
    'title': 'FastAI API',
    'description': 'Генератор сайтов на FastAPI: DeepSeek + LangGraph стримит HTML, картинки из Unsplash, хранение в S3 (MinIO) и скриншоты через Gotenberg.',
    'role': '',
    'date_range': '',
    'sort_order': 13,
}

# Хронология рельса (0027-паттерн, нумерация после 0030/0031: present → 14).
TYPE_ORDER = {'prior': 0, 'job': 1, 'present': 14}
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
    'skislyakow/BakeCake': 12,
    'skislyakow/fastai-api': 13,
}


def forwards(apps, schema_editor):
    Project = apps.get_model('main', 'Project')
    Skill = apps.get_model('main', 'Skill')
    TimelineItem = apps.get_model('main', 'TimelineItem')

    # --- Project: FastAI API наверх, существующие сдвигаются +1 (0027-паттерн) ---
    Project.objects.all().update(sort_order=models.F('sort_order') + 1)
    Project.objects.update_or_create(repo='skislyakow/fastai-api', defaults=PROJECT)

    # --- Skills: get_or_create, sort = max + 1 (0016/0025/0028-паттерн) ---
    max_sort = Skill.objects.aggregate(m=models.Max('sort_order'))['m'] or 0
    for i, (name, category) in enumerate(SKILLS):
        Skill.objects.get_or_create(
            name=name,
            defaults={'category': category, 'sort_order': max_sort + 1 + i},
        )

    # --- Timeline: запись FastAI API (Ноябрь 2026) ---
    TimelineItem.objects.update_or_create(
        repo='skislyakow/fastai-api',
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

    # Контент удаляется, нумерация возвращается к состоянию 0031: проекты
    # сдвигаются -1, present → 13 (прочие sort'ы на проде admin-перенумерованные,
    # восстанавливаем только созданное здесь — как в 0024/0027).
    TimelineItem.objects.filter(repo='skislyakow/fastai-api').delete()
    TimelineItem.objects.filter(item_type='present').update(sort_order=13)
    Project.objects.filter(repo='skislyakow/fastai-api').delete()
    Project.objects.filter(sort_order__gte=1).update(sort_order=models.F('sort_order') - 1)
    Skill.objects.filter(name__in=[name for name, _ in SKILLS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0031_add_bakecake_project'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
