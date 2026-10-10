from django.db import migrations


# Обновление карточки Dossier: убраны терминал и typing (тикет 01),
# skills-облако заменено категориями с кликабельными фильтрами.
DOSSIER_REPO = 'skislyakow/dossier'

DOSSIER_FEATURES = [
    'Секция портфолио: карточки проектов с бейджами GitHub/PyPI и фильтрами по тегам и навыкам',
    'Дизайн: монохром + кислотный лайм, светлая/тёмная тема, hero с курсорным градиентом',
    'Хронология опыта с вертикальным рельсом-навигатором',
    'Всё содержимое — из Django admin (unfold) через JSON API',
    'Production: Django + Gunicorn + Nginx на Ubuntu VPS с HTTPS',
    'Автодеплой через GitHub Actions с чек-гейтом (ruff, mypy, тесты)',
]


def seed(apps, schema_editor):
    Project = apps.get_model('main', 'Project')
    Project.objects.filter(repo=DOSSIER_REPO).update(features=DOSSIER_FEATURES)


def rollback(apps, schema_editor):
    Project = apps.get_model('main', 'Project')
    project = Project.objects.filter(repo=DOSSIER_REPO).first()
    if project and project.features == DOSSIER_FEATURES:
        project.features = [
            'Интерактивный терминал с AI-ассистентом (opencode-py, SSE-стриминг)',
            'Typing-анимация должности на чистом JavaScript (без библиотек)',
            'Skills cloud — облако тегов с технологиями',
            'Секция портфолио с карточками проектов, бейджами и распределением языков',
            'Production: Django + Gunicorn + Nginx на Ubuntu VPS',
            'Автодеплой через GitHub Actions',
        ]
        project.save(update_fields=['features'])


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_skill_filter_tag'),
    ]

    operations = [
        migrations.RunPython(seed, rollback),
    ]