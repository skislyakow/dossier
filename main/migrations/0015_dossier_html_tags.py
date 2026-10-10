from django.db import migrations


# Клик по навыкам HTML/CSS/JavaScript не находил ни одного проекта — в tags
# карточек этих технологий не было, хотя Dossier их использует (бейджи + языковая
# полоса GitHub). Добавляем в теги Dossier (update-only по repo).
DOSSIER_REPO = 'skislyakow/dossier'
TAGS_TO_ADD = ['HTML', 'CSS', 'JavaScript']


def seed(apps, schema_editor):
    Project = apps.get_model('main', 'Project')
    project = Project.objects.filter(repo=DOSSIER_REPO).first()
    if project:
        merged = list(dict.fromkeys(project.tags + TAGS_TO_ADD))
        project.tags = merged
        project.save(update_fields=['tags'])


def rollback(apps, schema_editor):
    Project = apps.get_model('main', 'Project')
    project = Project.objects.filter(repo=DOSSIER_REPO).first()
    if project:
        project.tags = [t for t in project.tags if t not in TAGS_TO_ADD]
        project.save(update_fields=['tags'])


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_update_dossier_features'),
    ]

    operations = [
        migrations.RunPython(seed, rollback),
    ]