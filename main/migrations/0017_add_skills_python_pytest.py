from django.db import migrations


# Python — тег всех бот-проектов, навыка в сидах не было (live-навык из админки,
# из-за чего dev-аудит показывал E100). pytest — сид по карте 0010, HR-видимый навык.
NEW_SKILLS = [
    # (name, category, size)
    ('Python', 'backend', 'xl'),
    ('pytest', 'tools', 'sm'),
]


def seed(apps, schema_editor):
    Skill = apps.get_model('main', 'Skill')
    max_order = Skill.objects.order_by('sort_order').values_list('sort_order', flat=True).last() or 0
    for i, (name, category, size) in enumerate(NEW_SKILLS, start=1):
        Skill.objects.get_or_create(
            name=name,
            defaults={'category': category, 'size': size, 'sort_order': max_order + i},
        )


def rollback(apps, schema_editor):
    Skill = apps.get_model('main', 'Skill')
    Skill.objects.filter(name__in=[name for name, _, _ in NEW_SKILLS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_add_skills_fastapi_github_pages'),
    ]

    operations = [
        migrations.RunPython(seed, rollback),
    ]