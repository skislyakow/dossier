from django.db import migrations, models


def forwards(apps, schema_editor):
    Skill = apps.get_model('main', 'Skill')
    Project = apps.get_model('main', 'Project')
    TimelineItem = apps.get_model('main', 'TimelineItem')

    # --- New skills (quiz-bot stack) ---
    skills = [
        {'name': 'Redis', 'size': 'md', 'icon': 'storage', 'sort_order': 27},
        {'name': 'vkbottle', 'size': 'md', 'icon': 'forum', 'sort_order': 28},
        {'name': 'VK API', 'size': 'sm', 'icon': 'public', 'sort_order': 29},
        {'name': 'pymorphy3', 'size': 'sm', 'icon': 'psychology', 'sort_order': 30},
        {'name': 'mypy', 'size': 'sm', 'icon': 'verified', 'sort_order': 31},
    ]
    for s in skills:
        Skill.objects.get_or_create(name=s['name'], defaults=s)

    # --- Project ---
    Project.objects.get_or_create(
        repo='skislyakow/quiz-bot',
        defaults={
            'title': 'Quiz Bot',
            'role': 'Bot Development',
            'tagline': 'Викторина в Telegram и ВКонтакте на базе ~300k вопросов: aiogram + vkbottle, состояние в Redis, нормализация ответов через pymorphy3',
            'features': [
                'Telegram (aiogram) и ВКонтакте (vkbottle) — два независимых процесса на разных токенах',
                'Единая бизнес-логика сравнения ответов для обеих платформ',
                'Нормализация ответов: лемматизация через pymorphy3, игнор пунктуации',
                'Состояние в Redis с TTL 1 час — без мусора от заброшенных диалогов',
                'Умный кэш базы ~302k вопросов с атомарной записью (os.replace)',
                'Полностью типизирован, проверяется mypy',
            ],
            'links': {},
            'badges_config': [
                {'label': 'stars', 'source': 'github_stars'},
                {'label': 'license', 'source': 'github_license'},
                {'label': 'language', 'source': 'github_lang'},
                {'label': 'updated', 'source': 'github_updated'},
                {'label': 'Python'},
                {'label': 'aiogram'},
                {'label': 'vkbottle'},
                {'label': 'Redis'},
                {'label': 'pymorphy3'},
            ],
            'screenshot': '',
            'sort_order': 7,
            'is_published': True,
        },
    )

    # --- Timeline: shift existing items with sort_order >= 9 by +1 ---
    TimelineItem.objects.filter(sort_order__gte=9).update(sort_order=models.F('sort_order') + 1)
    TimelineItem.objects.get_or_create(
        repo='skislyakow/quiz-bot',
        defaults={
            'item_type': 'project',
            'date_label': 'Август 2026',
            'title': 'Quiz Bot',
            'description': 'Викторина в Telegram и ВКонтакте на базе ~300k вопросов: aiogram + vkbottle, состояние в Redis, нормализация через pymorphy3.',
            'role': '',
            'date_range': '',
            'sort_order': 9,
        },
    )


def backwards(apps, schema_editor):
    Skill = apps.get_model('main', 'Skill')
    Project = apps.get_model('main', 'Project')
    TimelineItem = apps.get_model('main', 'TimelineItem')

    Skill.objects.filter(name__in=['Redis', 'vkbottle', 'VK API', 'pymorphy3', 'mypy']).delete()
    Project.objects.filter(repo='skislyakow/quiz-bot').delete()
    TimelineItem.objects.filter(repo='skislyakow/quiz-bot').delete()
    TimelineItem.objects.filter(sort_order__gte=10).update(sort_order=models.F('sort_order') - 1)


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_add_support_bot_data'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
