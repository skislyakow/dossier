import datetime
from django.db import migrations, models


# Синк сайта с реальным резюме (22 ноября 2026).
#
# 1) Рельс остаётся компактным: одна запись «Профессиональная деятельность»
#    (prior) вместо старой «До 2026 / ИТ-инфраструктура»; отдельной точки под
#    работу больше нет (она дублировала бы сводку).
# 2) Полная история — 8 мест работы — живёт в секции «Опыт» сайта и в резюме:
#    /api/timeline/ отдаёт массив jobs, resume.context() берёт все не-проектные
#    записи, сортируя их по start_date (обратная хронология).
# 3) Проектные записи таймлайна и сами Project не трогаются: часть добавлена
#    на проде через admin, все ключи — update-only.
PRIOR = {
    'title': 'Профессиональная деятельность',
    'date_label': '2007 — настоящее время',
    'description': 'С 2007 года — системное администрирование и инженерия; с 2025 года — Python-разработка: Django/DRF, FastAPI, Telegram- и VK-боты, интеграции и инфраструктура.',
    'item_type': 'prior',
    'sort_order': 0,
}

# description — построчно: каждая строка становится пунктом списка и в JS, и в PDF.
JOBS = [
    {
        'title': 'ТЦ Тихая Сосна',
        'role': 'Системный администратор',
        'date_label': 'Март 2007 — Апрель 2014',
        'date_range': 'Март 2007 — Апрель 2014',
        'start_date': datetime.date(2007, 3, 1),
        'end_date': datetime.date(2014, 4, 30),
        'description': 'Администрирование и сопровождение ИТ-инфраструктуры компании: парк 25+ рабочих станций, локальная сеть, серверное оборудование.',
        'item_type': 'job',
        'sort_order': 1,
    },
    {
        'title': 'ИП Кисляков Сергей Викторович',
        'role': 'Индивидуальный предприниматель',
        'date_label': 'Июль 2014 — Август 2017',
        'date_range': 'Июль 2014 — Август 2017',
        'start_date': datetime.date(2014, 7, 1),
        'end_date': datetime.date(2017, 8, 31),
        'description': 'Техническое сопровождение и администрирование ИТ-инфраструктуры организаций и частных лиц.',
        'item_type': 'job',
        'sort_order': 2,
    },
    {
        'title': 'АО «ФЦНИВТ «СНПО «Элерон»',
        'role': 'Инженер ПТО / инженер слаботочных систем',
        'date_label': 'Август 2017 — Май 2020',
        'date_range': 'Август 2017 — Май 2020',
        'start_date': datetime.date(2017, 8, 1),
        'end_date': datetime.date(2020, 5, 31),
        'description': '\n'.join([
            'Проектирование и пусконаладка слаботочных и программно-аппаратных комплексов безопасности (ОПС, СКУД, сеть).',
            'Разработка и согласование проектной, исполнительной и эксплуатационной документации, анализ ТЗ.',
            'Сопровождение приёмки и сдачи систем в эксплуатацию.',
        ]),
        'item_type': 'job',
        'sort_order': 3,
    },
    {
        'title': 'Частная практика / Проектная разработка',
        'role': 'Python-разработчик (Backend / Fullstack)',
        'date_label': 'Июнь 2020 — Февраль 2025',
        'date_range': 'Июнь 2020 — Февраль 2025',
        'start_date': datetime.date(2020, 6, 1),
        'end_date': datetime.date(2025, 2, 28),
        'description': '\n'.join([
            '10+ скриптов парсинга и API-интеграций для малого бизнеса — вместо ручного переноса данных.',
            'Веб-сервисы и Telegram-боты под ключ на Linux (Nginx, PostgreSQL) с автоматическим резервным копированием.',
        ]),
        'item_type': 'job',
        'sort_order': 4,
    },
    {
        'title': 'DobroCorp',
        'role': 'Python-разработчик',
        'date_label': 'Март 2025 — Июнь 2025',
        'date_range': 'Март 2025 — Июнь 2025',
        'start_date': datetime.date(2025, 3, 1),
        'end_date': datetime.date(2025, 6, 30),
        'description': '\n'.join([
            'Высоконагруженные парсеры live-данных: нашёл недокументированные API вместо тяжёлого HTML-парсинга.',
            'Перевёл распознавание текста с Google Vision на Mistral OCR + Tesseract — меньше расходов без потери скорости.',
            'Tesseract OCR Preprocessing Tuner: автоматический подбор фильтров предобработки и выше точность распознавания скриншотов.',
        ]),
        'item_type': 'job',
        'sort_order': 5,
    },
    {
        'title': 'DimaTech Ltd',
        'role': 'Python-разработчик (Backend)',
        'date_label': 'Июнь 2025 — Сентябрь 2025',
        'date_range': 'Июнь 2025 — Сентябрь 2025',
        'start_date': datetime.date(2025, 6, 1),
        'end_date': datetime.date(2025, 9, 30),
        'description': '\n'.join([
            'Поддержка платёжных интеграций по REST API: стабильная маршрутизация и корректная обработка статусов транзакций.',
            'Асинхронные обработчики вебхуков на Python / Asyncio / Sanic — без потерь уведомлений при пиковых нагрузках.',
            'Анализ логов и устранение критических багов в интеграционных сценариях со сторонними API.',
        ]),
        'item_type': 'job',
        'sort_order': 6,
    },
    {
        'title': 'Devman',
        'role': 'Python-разработчик',
        'date_label': 'Сентябрь 2025 — Январь 2026',
        'date_range': 'Сентябрь 2025 — Январь 2026',
        'start_date': datetime.date(2025, 9, 1),
        'end_date': datetime.date(2026, 1, 31),
        'description': '\n'.join([
            'Django / DRF-бэкенд для онлайн-бронирования и доставки: проектирование БД, многошаговая логика, серверная валидация и геокодирование адресов.',
            'ЮKassa: идемпотентная обработка вебхуков — без дублирования платежей, двойного бронирования и повторных QR-кодов.',
            'Кроссплатформенный бот на aiogram + vkbottle (~300 тыс. записей): кэш с автоинвалидацией и FSM в Redis.',
            'Docker, Nginx, systemd и CI (pytest, mypy, Ruff) через GitHub Actions.',
        ]),
        'item_type': 'job',
        'sort_order': 7,
    },
    {
        'title': 'ЭФКО Цифровые решения',
        'role': 'Специалист информационных технологий',
        'date_label': 'Январь 2026 — настоящее время',
        'date_range': 'Январь 2026 — настоящее время',
        'start_date': datetime.date(2026, 1, 1),
        'end_date': None,
        'description': '\n'.join([
            'Поддержка и сопровождение ИТ-инфраструктуры: стабильная работа корпоративных сервисов и сети, быстрая локализация типовых инцидентов.',
            'CLI-утилиты на Python / Bash для сбора системной диагностики и настройки окружений — меньше ручных операций.',
            'Первичная проверка работоспособности внутренних систем при выкладке обновлений и сопровождение пользователей.',
        ]),
        'url': 'https://efko.digital/',
        'item_type': 'job',
        'sort_order': 8,
    },
]

PRESENT = {
    'title': 'Настоящее время',
    'date_label': 'сейчас',
    'description': 'Развиваю экспертизу Middle Python-разработчика: сложные архитектурные задачи по бэкенду, высоконагруженные сервисы и измеримая польза бизнесу.',
    'item_type': 'present',
    'sort_order': 20,
}

PROFILE = {
    'full_name': 'Кисляков Сергей Викторович',
    'headline': 'Python Developer (middle)',
    'location': 'Воронеж · готов к переезду: Москва, Санкт-Петербург',
    'summary': (
        'Сильнее всего разбираюсь в проектировании надёжного Python-бэкенда, '
        'интеграциях по API и инфраструктуре. Благодаря бэкграунду в системном '
        'администрировании понимаю приложение в продакшене: Linux, Docker, '
        'Nginx, CI/CD. В оплатах (ЮKassa) — идемпотентные вебхуки и защита от '
        'двойного бронирования; в ботах (Telegram + VK) — кэш с автоинвалидацией '
        'и FSM в Redis. Цель — Middle Python-разработчик в продуктовой команде, '
        'сложные архитектурные задачи и высоконагруженные сервисы.'
    ),
    'education': (
        'Воронежский экономико-правовой институт, 2017 — высшее, '
        'Прикладная информатика в экономике. '
        'Электронный сертификат: интерактивный тренажёр по SQL (2026).'
    ),
}

EMAIL = {'label': 'kislyakov84@yandex.ru', 'value': 'kislyakov84@yandex.ru'}

SKILLS = [
    {'name': 'SQLAlchemy', 'category': 'backend'},
    {'name': 'Alembic', 'category': 'backend'},
    {'name': 'Linux', 'category': 'devops'},
]

# Значения до миграции — для backwards.
OLD_PRIOR = {
    'title': 'ИТ-инфраструктура',
    'date_label': 'До 2026',
    'description': 'Работа в ИТ вне разработки: поддержка и сопровождение систем. С 2026 перешёл в разработку на Python.',
    'item_type': 'prior',
    'sort_order': 0,
}
OLD_JOB = {
    'title': 'ЭФКО Цифровые решения',
    'role': 'ИТ-Специалист',
    'date_label': 'Январь 2026 — настоящее время',
    'date_range': 'Январь 2026 — настоящее время',
    'description': '',
    'url': 'https://efko.digital/',
    'item_type': 'job',
    'sort_order': 1,
}
OLD_PRESENT = {
    'title': 'Настоящее время',
    'date_label': 'сейчас',
    'description': 'Продолжаю развиваться как Python-разработчик: pet-проекты, open-source, изучение новых технологий.',
    'item_type': 'present',
    'sort_order': 11,
}
OLD_PROFILE = {
    'full_name': 'Сергей Кисляков',
    'headline': 'Python Fullstack Developer',
    'location': 'Удалённо / Россия',
    'summary': 'Python-разработчик: автоматизация, Telegram-боты и веб на Django. Строю сервисы от задачи до продакшена: Django/FastAPI, aiogram-боты, интеграции (GitHub API, PyPI, Telegram, VK, Dialogflow).',
    'education': 'Самостоятельное инженерное образование: Django, FastAPI, алгоритмы и структуры данных, DevOps-основы (Linux, systemd, Nginx).',
}
OLD_EMAIL = {'label': 's.kislyakov84@gmail.com', 'value': 's.kislyakov84@gmail.com'}


def forwards(apps, schema_editor):
    TimelineItem = apps.get_model('main', 'TimelineItem')
    Skill = apps.get_model('main', 'Skill')
    ResumeProfile = apps.get_model('main', 'ResumeProfile')
    ContactInfo = apps.get_model('main', 'ContactInfo')

    # Старые prior/job/present — из сидов 0009/0027 и ручных правок админки;
    # заменяем их целиком, чтобы не осталось дублей (EFKO, вторая present-точка).
    TimelineItem.objects.filter(item_type__in=('prior', 'job', 'present')).delete()
    TimelineItem.objects.create(**PRIOR)
    # Работы нумеруются вне диапазона проектных sort_order (2…20 на проде),
    # чтобы админка не перемешивала два списка.
    for i, job in enumerate(JOBS):
        TimelineItem.objects.create(**{**job, 'sort_order': 100 + i})
    TimelineItem.objects.create(**{**PRESENT, 'sort_order': 200})

    max_sort = Skill.objects.aggregate(m=models.Max('sort_order'))['m'] or 0
    for i, skill in enumerate(SKILLS):
        Skill.objects.get_or_create(
            name=skill['name'],
            defaults={**skill, 'sort_order': max_sort + 1 + i},
        )

    ResumeProfile.objects.update_or_create(id=1, defaults=PROFILE)
    ContactInfo.objects.update_or_create(contact_type='email', defaults=EMAIL)


def backwards(apps, schema_editor):
    TimelineItem = apps.get_model('main', 'TimelineItem')
    Skill = apps.get_model('main', 'Skill')
    ResumeProfile = apps.get_model('main', 'ResumeProfile')
    ContactInfo = apps.get_model('main', 'ContactInfo')

    TimelineItem.objects.filter(title__in=[j['title'] for j in JOBS]).delete()
    TimelineItem.objects.update_or_create(title=PRIOR['title'], defaults=OLD_PRIOR)
    TimelineItem.objects.update_or_create(title=OLD_JOB['title'], defaults=OLD_JOB)
    TimelineItem.objects.update_or_create(title=PRESENT['title'], defaults=OLD_PRESENT)

    Skill.objects.filter(name__in=[s['name'] for s in SKILLS]).delete()
    ResumeProfile.objects.update_or_create(id=1, defaults=OLD_PROFILE)
    ContactInfo.objects.update_or_create(contact_type='email', defaults=OLD_EMAIL)


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0034_add_yandex_afisha_project'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
