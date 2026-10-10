from django.db import migrations


# Карточка Dossier: буллет CI упоминает реальное число тестов (42) и полный гейт.
DOSSIER_REPO = 'skislyakow/dossier'
OLD_BULLET = 'Автодеплой через GitHub Actions с чек-гейтом (ruff, mypy, тесты)'
NEW_BULLET = 'Автодеплой через GitHub Actions с чек-гейтом (ruff, mypy, 42 теста, makemigrations, node)'


def seed(apps, schema_editor):
    Project = apps.get_model('main', 'Project')
    for project in Project.objects.filter(repo=DOSSIER_REPO):
        if OLD_BULLET in project.features:
            project.features = [NEW_BULLET if f == OLD_BULLET else f for f in project.features]
            project.save(update_fields=['features'])


def rollback(apps, schema_editor):
    Project = apps.get_model('main', 'Project')
    for project in Project.objects.filter(repo=DOSSIER_REPO):
        if NEW_BULLET in project.features:
            project.features = [OLD_BULLET if f == NEW_BULLET else f for f in project.features]
            project.save(update_fields=['features'])


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_add_skills_python_pytest'),
    ]

    operations = [
        migrations.RunPython(seed, rollback),
    ]