from django.db import migrations, models


TAGS_BY_REPO = {
    'skislyakow/Devman-monitor': ['Python', 'systemd', 'Telegram'],
    'skislyakow/support-bot': ['Python', 'aiogram', 'Dialogflow', 'Telegram', 'VK'],
    'skislyakow/quiz-bot': ['Python', 'aiogram', 'vkbottle', 'Redis', 'Telegram', 'VK'],
}


def forwards(apps, schema_editor):
    Project = apps.get_model('main', 'Project')
    for repo, tags in TAGS_BY_REPO.items():
        Project.objects.filter(repo=repo).update(tags=tags)


def backwards(apps, schema_editor):
    Project = apps.get_model('main', 'Project')
    Project.objects.filter(repo__in=TAGS_BY_REPO).update(tags=[])


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_contact_github'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='tags',
            field=models.JSONField(
                blank=True,
                default=list,
                help_text='Курируемые метки стека, например ["Django", "Redis"]',
                verbose_name='Теги',
            ),
        ),
        migrations.RunPython(forwards, backwards),
    ]
