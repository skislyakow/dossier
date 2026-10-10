from django.db import migrations


# Навыки, отсутствующие в списке, но теги проектов с ними: FastAPI (ferma),
# GitHub Pages (online_library). Клик по навыку должен находить проект.
NEW_SKILLS = [
    # (name, category, size)
    ('FastAPI', 'backend', 'md'),
    ('GitHub Pages', 'devops', 'sm'),
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
        ('main', '0015_dossier_html_tags'),
    ]

    operations = [
        migrations.RunPython(seed, rollback),
    ]