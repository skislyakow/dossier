from django.db import migrations


# Навыки под теги новых проектов из 0024_sync_prod_projects (E100): каждый
# тег проектов должен иметь кликабельную Skill-кнопку (audit_content).
NEW_SKILLS = [
    ('Django', 'web'),
    ('HTML', 'web'),
    ('CSS', 'web'),
    ('JavaScript', 'web'),
    ('Bootstrap', 'web'),
    ('Jinja2', 'web'),
    ('Nginx', 'devops'),
    ('Gunicorn', 'devops'),
    ('GitHub Actions', 'devops'),
    ('SQLite', 'backend'),
    ('httpx', 'backend'),
    ('requests', 'backend'),
    ('Pydantic', 'backend'),
    ('PyPI', 'tools'),
    ('opencode-py', 'tools'),
]


def seed(apps, schema_editor):
    Skill = apps.get_model('main', 'Skill')
    max_order = Skill.objects.order_by('sort_order').values_list('sort_order', flat=True).last() or 0
    for i, (name, category) in enumerate(NEW_SKILLS, start=1):
        Skill.objects.get_or_create(
            name=name,
            defaults={'category': category, 'sort_order': max_order + i},
        )


def rollback(apps, schema_editor):
    Skill = apps.get_model('main', 'Skill')
    Skill.objects.filter(name__in=[name for name, _ in NEW_SKILLS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0024_sync_prod_projects'),
    ]

    operations = [
        migrations.RunPython(seed, rollback),
    ]