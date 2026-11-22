from django.db import migrations


# Правка сводной точки рельса: Python-разработка началась в июне 2020
# (частная практика / проектная разработка), а не в 2025-м, как попало в 0035.
TITLE = 'Профессиональная деятельность'
NEW_DESCRIPTION = (
    'С 2007 года — системное администрирование и инженерия; '
    'с 2020 года — Python-разработка: Django/DRF, FastAPI, '
    'Telegram- и VK-боты, интеграции и инфраструктура.'
)
OLD_DESCRIPTION = (
    'С 2007 года — системное администрирование и инженерия; '
    'с 2025 года — Python-разработка: Django/DRF, FastAPI, '
    'Telegram- и VK-боты, интеграции и инфраструктура.'
)


def forwards(apps, schema_editor):
    TimelineItem = apps.get_model('main', 'TimelineItem')
    TimelineItem.objects.filter(title=TITLE).update(description=NEW_DESCRIPTION)


def backwards(apps, schema_editor):
    TimelineItem = apps.get_model('main', 'TimelineItem')
    TimelineItem.objects.filter(title=TITLE).update(description=OLD_DESCRIPTION)


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0035_sync_resume_experience'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
