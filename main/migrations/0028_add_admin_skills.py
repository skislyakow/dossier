from django.db import migrations


# Паритет «свежий migrate == прод»: эти 5 навыков заведены на проде через
# admin (данные сняты с /api/skills/ прода), в миграциях репо отсутствовали —
# при пересборке БД они бы потерялись. На проде миграция no-op
# (get_or_create находит существующие записи), сид действует на свежей БД.
# Навыки без совпадающих тегов проектов дают W101 (предупреждение, exit 0).
ADMIN_SKILLS = [
    ('Docker', 'devops'),
    ('Git', 'devops'),
    ('Ubuntu', 'devops'),
    ('REST API', 'backend'),
    ('asyncio', 'backend'),
]


def seed(apps, schema_editor):
    Skill = apps.get_model('main', 'Skill')
    max_order = Skill.objects.order_by('sort_order').values_list('sort_order', flat=True).last() or 0
    for i, (name, category) in enumerate(ADMIN_SKILLS, start=1):
        Skill.objects.get_or_create(
            name=name,
            defaults={'category': category, 'sort_order': max_order + i},
        )


def rollback(apps, schema_editor):
    Skill = apps.get_model('main', 'Skill')
    Skill.objects.filter(name__in=[name for name, _ in ADMIN_SKILLS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0027_add_fishshop_project'),
    ]

    operations = [
        migrations.RunPython(seed, rollback),
    ]
