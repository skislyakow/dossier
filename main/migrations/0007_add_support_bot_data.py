from django.db import migrations, models


def forwards(apps, schema_editor):
    Skill = apps.get_model('main', 'Skill')
    Project = apps.get_model('main', 'Project')
    TimelineItem = apps.get_model('main', 'TimelineItem')

    # --- New skills ---
    skills = [
        {'name': 'Dialogflow', 'size': 'md', 'icon': 'psychology', 'sort_order': 24},
        {'name': 'aiogram', 'size': 'sm', 'icon': 'chat', 'sort_order': 25},
        {'name': 'vk_api', 'size': 'sm', 'icon': 'forum', 'sort_order': 26},
    ]
    for s in skills:
        Skill.objects.get_or_create(name=s['name'], defaults=s)

    # --- Project ---
    Project.objects.get_or_create(
        repo='skislyakow/support-bot',
        defaults={
            'title': 'Support Bot',
            'role': 'Bot Development',
            'tagline': 'Поддержка в Telegram и ВКонтакте на базе Google Dialogflow',
            'features': [
                'Telegram (aiogram) + ВКонтакте (vk_api Long Poll) в одном проекте',
                'Google Dialogflow — распознавание намерений по обучающим фразам',
                'Интенты из phrases.json грузятся через API скриптом create_intent.py',
                'systemd-сервисы для обоих ботов с Restart=always',
                'Если Dialogflow не понял во ВКонтакте — бот молчит, не мешая операторам',
            ],
            'links': {
                'telegram': 'https://t.me/kislyakov_support_bot',
                'vk': 'https://vk.ru/club238875331',
            },
            'badges_config': [
                {'label': 'stars', 'source': 'github_stars'},
                {'label': 'license', 'source': 'github_license'},
                {'label': 'language', 'source': 'github_lang'},
                {'label': 'updated', 'source': 'github_updated'},
                {'label': 'Python'},
                {'label': 'aiogram'},
                {'label': 'Dialogflow'},
                {'label': 'vk_api'},
                {'label': 'systemd'},
            ],
            'screenshot': '',
            'sort_order': 6,
            'is_published': True,
        },
    )

    # --- Fix Dossier www link to the domain ---
    Project.objects.filter(repo='skislyakow/dossier').update(
        links={'www': 'https://kislyakov.pro/'}
    )

    # --- Timeline: shift existing items with sort_order >= 8 by +1 ---
    TimelineItem.objects.filter(sort_order__gte=8).update(sort_order=models.F('sort_order') + 1)
    TimelineItem.objects.get_or_create(
        repo='skislyakow/support-bot',
        defaults={
            'item_type': 'project',
            'date_label': 'Август 2026',
            'title': 'Support Bot',
            'description': 'Поддержка в Telegram и ВКонтакте на базе Google Dialogflow: aiogram + vk_api Long Poll, интенты через API.',
            'role': '',
            'date_range': '',
            'sort_order': 8,
        },
    )


def backwards(apps, schema_editor):
    Skill = apps.get_model('main', 'Skill')
    Project = apps.get_model('main', 'Project')
    TimelineItem = apps.get_model('main', 'TimelineItem')

    Skill.objects.filter(name__in=['Dialogflow', 'aiogram', 'vk_api']).delete()
    Project.objects.filter(repo='skislyakow/support-bot').delete()
    TimelineItem.objects.filter(repo='skislyakow/support-bot').delete()
    TimelineItem.objects.filter(sort_order__gte=9).update(sort_order=models.F('sort_order') - 1)
    Project.objects.filter(repo='skislyakow/dossier').update(
        links={'www': 'http://132.243.121.192/'}
    )


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_rename_order_to_sort_order'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
