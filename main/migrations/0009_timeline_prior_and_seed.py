from django.db import migrations, models


def forwards(apps, schema_editor):
    TimelineItem = apps.get_model('main', 'TimelineItem')

    # filter-first, НЕ get_or_create: на проде строк типа job/present может быть > 1
    def seed(item_type, defaults):
        if not TimelineItem.objects.filter(item_type=item_type).first():
            TimelineItem.objects.create(item_type=item_type, **defaults)

    seed('prior', {
        'date_label': 'До 2026',
        'title': 'ИТ-инфраструктура',
        'description': 'Работа в ИТ вне разработки: поддержка и сопровождение систем. '
                       'С 2026 перешёл в разработку на Python.',
        'sort_order': 5,
    })
    # на проде job/present уже заведены вручную → no-op; локально/в тестах создаются,
    # иначе рендер рельса (JOB.title в JS) падает без них
    seed('job', {
        'date_label': 'Январь 2026',
        'title': 'EFKO',
        'role': 'Python-разработчик',
        'date_range': 'Январь 2026 — настоящее время',
        'url': 'https://efko.digital',
        'description': 'Python-полный стек: Django/DRF, PostgreSQL, боты и автоматизация.',
        'sort_order': 4,
    })
    seed('present', {
        'date_label': 'сейчас',
        'title': 'Сейчас',
        'description': 'Работа в EFKO, pet-проекты во время учёбы; фокус — Python Fullstack (Django/DRF).',
        'sort_order': 10,
    })


def backwards(apps, schema_editor):
    TimelineItem = apps.get_model('main', 'TimelineItem')
    # удаляется только prior (его создала эта миграция);
    # job/present не трогаем — на проде они не наши
    TimelineItem.objects.filter(item_type='prior').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_add_quiz_bot_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timelineitem',
            name='item_type',
            field=models.CharField(choices=[('prior', 'До разработки'), ('project', 'Проект'), ('job', 'Работа'), ('present', 'Настоящее')], max_length=10, verbose_name='Тип'),
        ),
        migrations.RunPython(forwards, backwards),
    ]
