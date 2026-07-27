from django.db import migrations, models


def forwards(apps, schema_editor):
    Skill = apps.get_model('main', 'Skill')
    Project = apps.get_model('main', 'Project')
    TimelineItem = apps.get_model('main', 'TimelineItem')

    # --- New skills ---
    skills = [
        {'name': 'systemd', 'size': 'sm', 'icon': 'settings', 'order': 21},
        {'name': 'python-dotenv', 'size': 'sm', 'icon': 'key', 'order': 22},
        {'name': 'Telegram Bot API', 'size': 'md', 'icon': 'smart_toy', 'order': 23},
    ]
    for s in skills:
        Skill.objects.get_or_create(name=s['name'], defaults=s)

    # --- Project ---
    Project.objects.get_or_create(
        repo='skislyakow/Devman-monitor',
        defaults={
            'title': 'Devman Monitor',
            'role': 'Bot Development',
            'tagline': 'Бот-монитор, который следит за состоянием systemd-сервиса и уведомляет в Telegram при падении или восстановлении',
            'features': [
                'Автоматическая проверка статуса каждые 10 секунд',
                'Уведомления в Telegram при падении/восстановлении',
                'Защита от спама — одноразовое уведомление',
                'Работает как systemd-сервис с Restart=always',
                'Логирование через journalctl',
            ],
            'links': {},
            'badges_config': [
                {'label': 'python', 'source': 'github_lang'},
                {'label': 'license', 'source': 'github_license'},
            ],
            'screenshot': '',
            'order': 5,
            'is_published': True,
        },
    )

    # --- Timeline: shift existing items with order >= 5 by +2 ---
    TimelineItem.objects.filter(order__gte=5).update(order=models.F('order') + 2)
    TimelineItem.objects.get_or_create(
        repo='skislyakow/Devman-monitor',
        defaults={
            'item_type': 'project',
            'date_label': 'Июль 2026',
            'title': 'Devman Monitor',
            'description': 'Бот-монитор для systemd-сервисов с уведомлениями в Telegram',
            'role': '',
            'date_range': '',
            'order': 6,
        },
    )


def backwards(apps, schema_editor):
    Skill = apps.get_model('main', 'Skill')
    Project = apps.get_model('main', 'Project')
    TimelineItem = apps.get_model('main', 'TimelineItem')

    Skill.objects.filter(name__in=['systemd', 'python-dotenv', 'Telegram Bot API']).delete()
    Project.objects.filter(repo='skislyakow/Devman-monitor').delete()
    TimelineItem.objects.filter(repo='skislyakow/Devman-monitor').delete()
    TimelineItem.objects.filter(order__gte=7).update(order=models.F('order') - 2)


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_project_screenshot'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
