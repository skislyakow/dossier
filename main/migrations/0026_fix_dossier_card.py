from django.db import migrations


# Правка фич карточки Dossier (update-only по repo):
# 1. Убираем ошибочный буллет про Telegram-бота на Dialogflow — это фича Support Bot,
#    копипаст-артефакт, приехавший в карточку Dossier.
# 2. «56+ тестов» → «99 тестов» и дополняем деплой-цепочку health-check'ом и
#    визуальным регрессом, чтобы карточка отражала фактическое состояние репо.
DOSSIER_REPO = 'skislyakow/dossier'

OLD_FEATURES = [
    'Телеграм-бот для поддержки пользователей на Dialogflow (aiogram)',
    'Сайт-визитка kislyakov.pro: Django 6, zero-dependency JS/CSS, тёмная и светлая темы',
    'Авто-деплой на VPS через GitHub Actions: чек-гейт (ruff, mypy, pytest, node --check) → migrate → collectstatic → restart',
    'Инженерный процесс публичный: 56+ тестов, ADR-документы, audit_content, смоук прода',
    'Авто-резюме: PDF генерируется сервером из контента CMS (WeasyPrint), единый источник данных сайта и файла',
]

NEW_FEATURES = [
    'Сайт-визитка kislyakov.pro: Django 6, zero-dependency JS/CSS, тёмная и светлая темы',
    'Авто-деплой на VPS через GitHub Actions: чек-гейт (ruff, mypy, pytest, node --check, audit_content) → migrate → collectstatic → restart с health-check',
    'Инженерный процесс публичный: 99 тестов, ADR-документы, audit_content, смоук прода и визуальный регресс',
    'Авто-резюме: PDF генерируется сервером из контента CMS (WeasyPrint), единый источник данных сайта и файла',
]


def seed(apps, schema_editor):
    Project = apps.get_model('main', 'Project')
    Project.objects.filter(repo=DOSSIER_REPO).update(features=NEW_FEATURES)


def rollback(apps, schema_editor):
    Project = apps.get_model('main', 'Project')
    Project.objects.filter(repo=DOSSIER_REPO).update(features=OLD_FEATURES)


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0025_add_skills_for_synced_projects'),
    ]

    operations = [
        migrations.RunPython(seed, rollback),
    ]