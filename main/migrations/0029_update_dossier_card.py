from django.db import migrations

# Правка карточки Dossier (update-only по repo) — сверка с фактическим состоянием:
# 1. Скриншот: поле было пустым, карточка показывала монограмму-плейсхолдер;
#    кладём raw-URL на docs/screenshot.png (паттерн FishShop, 0027).
# 2. Деплой-буллет: добавляем verify-джобу (smoke прода + байт-сверка статики) —
#    цепочка в карточке должна отражать фактический пайплайн deploy.yml.
# 3. «99 тестов» → без числа: счётчик дважды устаревал (56+ → 99 → 101),
#    убираем digit, чтобы не чинить его при каждом добавлении тестов.
# 4. Теги += Ubuntu, systemd (реальный деплой: VPS Ubuntu + systemd-юнит)
#    и opencode-py (в репо лежит opencode.json — разработка через агента);
#    чипы бейджей выравниваются с тегами: −Git, +mypy, +systemd.

DOSSIER_REPO = 'skislyakow/dossier'

OLD_FEATURES = [
    'Сайт-визитка kislyakov.pro: Django 6, zero-dependency JS/CSS, тёмная и светлая темы',
    'Авто-деплой на VPS через GitHub Actions: чек-гейт (ruff, mypy, pytest, node --check, audit_content) → migrate → collectstatic → restart с health-check',
    'Инженерный процесс публичный: 99 тестов, ADR-документы, audit_content, смоук прода и визуальный регресс',
    'Авто-резюме: PDF генерируется сервером из контента CMS (WeasyPrint), единый источник данных сайта и файла',
]

NEW_FEATURES = [
    'Сайт-визитка kislyakov.pro: Django 6, zero-dependency JS/CSS, тёмная и светлая темы',
    'Авто-деплой на VPS через GitHub Actions: чек-гейт (ruff, mypy, pytest, node --check, audit_content) → migrate → collectstatic → restart с health-check → verify (smoke прода и байт-сверка статики)',
    'Инженерный процесс публичный: тесты, ADR-документы, audit_content, смоук прода и визуальный регресс',
    'Авто-резюме: PDF генерируется сервером из контента CMS (WeasyPrint), единый источник данных сайта и файла',
]

OLD_TAGS = [
    'Python', 'Django', 'Nginx', 'Gunicorn', 'GitHub Actions',
    'HTML', 'CSS', 'JavaScript', 'pytest', 'mypy',
]

NEW_TAGS = [
    'Python', 'Django', 'Nginx', 'Gunicorn', 'GitHub Actions',
    'HTML', 'CSS', 'JavaScript', 'pytest', 'mypy',
    'Ubuntu', 'systemd', 'opencode-py',
]

NEW_SCREENSHOT = (
    'https://raw.githubusercontent.com/skislyakow/dossier/main/docs/screenshot.png'
)


def _is_static_chip(badge):
    """Статический чип: без source (группа GitHub/Pypi резолвится из API)."""
    return not badge.get('source') and badge.get('label')


def _update_badges(badges):
    out = [
        b for b in (badges or [])
        if not (_is_static_chip(b) and b['label'] == 'Git')
    ]
    labels = {b.get('label') for b in out if _is_static_chip(b)}
    for label in ('mypy', 'systemd'):
        if label not in labels:
            out.append({'label': label})
    return out


def _rollback_badges(badges):
    out = [
        b for b in (badges or [])
        if not (_is_static_chip(b) and b['label'] in {'mypy', 'systemd'})
    ]
    labels = {b.get('label') for b in out if _is_static_chip(b)}
    if 'Git' not in labels:
        git_chip = {'label': 'Git'}
        for i, b in enumerate(out):
            if _is_static_chip(b) and b.get('label') == 'GitHub Actions':
                out.insert(i, git_chip)
                break
        else:
            out.append(git_chip)
    return out


def seed(apps, schema_editor):
    Project = apps.get_model('main', 'Project')
    for p in Project.objects.filter(repo=DOSSIER_REPO):
        p.features = NEW_FEATURES
        p.tags = NEW_TAGS
        p.screenshot = NEW_SCREENSHOT
        p.badges_config = _update_badges(p.badges_config)
        p.save()


def rollback(apps, schema_editor):
    Project = apps.get_model('main', 'Project')
    for p in Project.objects.filter(repo=DOSSIER_REPO):
        p.features = OLD_FEATURES
        p.tags = OLD_TAGS
        p.screenshot = ''
        p.badges_config = _rollback_badges(p.badges_config)
        p.save()


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0028_add_admin_skills'),
    ]

    operations = [
        migrations.RunPython(seed, rollback),
    ]
