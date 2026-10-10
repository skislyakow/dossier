from django.db import migrations


# Тег 'pytest' карточке Dossier: репозиторий реально гоняет тесты через pytest
# (pytest + pytest-django, 42 теста) — клик по навыку pytest находит проект.
DOSSIER_REPO = 'skislyakow/dossier'
TAG = 'pytest'


def seed(apps, schema_editor):
    Project = apps.get_model('main', 'Project')
    for project in Project.objects.filter(repo=DOSSIER_REPO):
        if TAG not in project.tags:
            project.tags = project.tags + [TAG]
            project.save(update_fields=['tags'])


def rollback(apps, schema_editor):
    Project = apps.get_model('main', 'Project')
    for project in Project.objects.filter(repo=DOSSIER_REPO):
        if TAG in project.tags:
            project.tags = [t for t in project.tags if t != TAG]
            project.save(update_fields=['tags'])


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_dossier_ci_bullet'),
    ]

    operations = [
        migrations.RunPython(seed, rollback),
    ]