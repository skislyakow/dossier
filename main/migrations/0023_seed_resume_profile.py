from django.db import migrations

# Профиль резюме и хронология: стартовый контент для фичи авто-резюме (A4, PDF).
# Черновик — владелец правит текст в админке (Main → Профиль резюме).

RESUME_DEFAULTS = {
    'headline': 'Python Fullstack Developer',
    'summary': (
        'Python-разработчик: автоматизация, Telegram-боты и веб на Django. '
        'Строю сервисы от задачи до продакшена: Django/FastAPI, aiogram-боты, '
        'интеграции (GitHub API, PyPI, Telegram, VK, Dialogflow). Привычка '
        'инженерной дисциплины: CI-гейт (ruff, mypy, pytest), авто-деплой, '
        'смоук-проверки прода, реестры вместо рассинхронных копий правил '
        'и ADR-документы о ключевых решениях.'
    ),
    'location': 'Удалённо / Россия',
    'education': 'Самостоятельное инженерное образование: Django, FastAPI, '
                 'алгоритмы и структуры данных, DevOps-основы (Linux, systemd, Nginx).',
}

# Карточка Dossier: буллет инженерии (тесты/CI/ADR) и буллет авто-резюме.
DOSSIER_REPO = 'skislyakow/dossier'


def seed_resume(apps, schema_editor):
    ResumeProfile = apps.get_model('main', 'ResumeProfile')
    os_profile, _ = ResumeProfile.objects.get_or_create(
        id=1, defaults={'full_name': 'Сергей Кисляков', **RESUME_DEFAULTS},
    )
    for field, value in RESUME_DEFAULTS.items():
        if not getattr(os_profile, field):
            setattr(os_profile, field, value)
    if not os_profile.full_name:
        os_profile.full_name = 'Сергей Кисляков'
    os_profile.save()


def rollback_resume(apps, schema_editor):
    ResumeProfile = apps.get_model('main', 'ResumeProfile')
    ResumeProfile.objects.filter(id=1).delete()


FEATURES = [
    'Телеграм-бот для поддержки пользователей на Dialogflow (aiogram)',
    'Сайт-визитка kislyakov.pro: Django 6, zero-dependency JS/CSS, тёмная и светлая темы',
    'Авто-деплой на VPS через GitHub Actions: чек-гейт (ruff, mypy, pytest, node --check) → migrate → collectstatic → restart',
    'Инженерный процесс публичный: 56+ тестов, ADR-документы, audit_content, смоук прода',
    'Авто-резюме: PDF генерируется сервером из контента CMS (WeasyPrint), единый источник данных сайта и файла',
]


def seed_dossier(apps, schema_editor):
    Project = apps.get_model('main', 'Project')
    for project in Project.objects.filter(repo=DOSSIER_REPO):
        project.features = FEATURES
        project.save(update_fields=['features'])


def rollback_dossier(apps, schema_editor):
    Project = apps.get_model('main', 'Project')
    for project in Project.objects.filter(repo=DOSSIER_REPO):
        project.features = [
            f for f in project.features if 'Авто-резюме' not in f and 'Инженерный процесс' not in f
        ]
        project.save(update_fields=['features'])


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0022_resumeprofile_project_date_label_and_more'),
    ]

    operations = [
        migrations.RunPython(seed_resume, rollback_resume),
        migrations.RunPython(seed_dossier, rollback_dossier),
    ]