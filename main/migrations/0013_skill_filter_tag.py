from django.db import migrations, models


# Некоторым навыкам имя не равно тегу проекта (алиасы) — фильтр по тегу.
FILTER_TAG_BY_NAME = {
    'Telegram Bot API': 'Telegram',
    'vk_api': 'VK',
    'VK API': 'VK',
}

# Теги для ранее таглесс проектов (выведены из README на GitHub).
TAGS_BY_REPO = {
    'skislyakow/opencode-py': ['Python', 'httpx', 'Pydantic', 'PyPI', 'opencode-py'],
    'skislyakow/ferma': ['Python', 'FastAPI', 'SQLite', 'VK API', 'requests'],
    'skislyakow/devman-bot': ['Python', 'Telegram', 'requests', 'python-dotenv'],
    'skislyakow/dossier': ['Python', 'Django', 'Nginx', 'Gunicorn', 'GitHub Actions'],
    'skislyakow/online_library': ['Python', 'Jinja2', 'Bootstrap', 'GitHub Pages'],
}


def seed(apps, schema_editor):
    Skill = apps.get_model('main', 'Skill')
    for name, tag in FILTER_TAG_BY_NAME.items():
        Skill.objects.filter(name=name).update(filter_tag=tag)
    Project = apps.get_model('main', 'Project')
    for repo, tags in TAGS_BY_REPO.items():
        Project.objects.filter(repo=repo).update(tags=tags)


def rollback(apps, schema_editor):
    Skill = apps.get_model('main', 'Skill')
    Skill.objects.filter(name__in=FILTER_TAG_BY_NAME).update(filter_tag='')
    Project = apps.get_model('main', 'Project')
    for repo in TAGS_BY_REPO:
        Project.objects.filter(repo=repo).update(tags=[])


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_project_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='skill',
            name='filter_tag',
            field=models.CharField(blank=True, help_text='Тег проекта, по которому клик по навыку фильтрует список проектов (пусто — по имени навыка)', max_length=50, verbose_name='Тег фильтра проектов'),
        ),
        migrations.RunPython(seed, rollback),
    ]