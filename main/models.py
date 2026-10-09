from django.db import models


class Skill(models.Model):
    SIZE_CHOICES = [
        ('xl', 'XL'),
        ('lg', 'Large'),
        ('md', 'Medium'),
        ('sm', 'Small'),
    ]
    CATEGORY_CHOICES = [
        ('backend', 'Backend'),
        ('web', 'Web'),
        ('devops', 'DevOps'),
        ('bots', 'Bots & Integrations'),
        ('tools', 'Tools'),
    ]
    name = models.CharField('Название', max_length=50, unique=True)
    category = models.CharField('Категория', max_length=10, choices=CATEGORY_CHOICES, default='tools')
    size = models.CharField('Размер', max_length=2, choices=SIZE_CHOICES, default='sm')
    icon = models.CharField('Иконка', max_length=50, blank=True, help_text='Название Material Symbols иконки')
    sort_order = models.PositiveSmallIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Навык'
        verbose_name_plural = 'Навыки'
        ordering = ['sort_order']

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField('Название', max_length=200)
    repo = models.CharField('Репозиторий', max_length=200, help_text='GitHub: username/repo')
    pypi = models.CharField('PyPI пакет', max_length=100, blank=True, help_text='Название пакета на PyPI (опционально)')
    role = models.CharField('Роль', max_length=100, blank=True, help_text='например: Fullstack Development')
    tagline = models.TextField('Слоган', blank=True)
    features = models.JSONField('Особенности', default=list, blank=True, help_text='Список характеристик')
    links = models.JSONField('Ссылки', default=dict, blank=True, help_text='{"pypi": "https://...", "www": "https://..."}')
    badges_config = models.JSONField('Бейджи', default=list, blank=True, help_text='[{"label": "pypi", "source": "pypi_version"}]')
    screenshot = models.URLField('Скриншот', blank=True, help_text='URL изображения для карточки проекта')
    sort_order = models.PositiveSmallIntegerField('Порядок', default=0)
    is_published = models.BooleanField('Опубликован', default=True)

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
        ordering = ['sort_order']

    def __str__(self):
        return self.title


class TimelineItem(models.Model):
    TYPE_CHOICES = [
        ('prior', 'До разработки'),
        ('project', 'Проект'),
        ('job', 'Работа'),
        ('present', 'Настоящее'),
    ]
    item_type = models.CharField('Тип', max_length=10, choices=TYPE_CHOICES)
    date_label = models.CharField('Дата', max_length=100, help_text='например: Апрель 2026, сейчас')
    title = models.CharField('Название', max_length=200)
    description = models.TextField('Описание', blank=True)
    repo = models.CharField('Репозиторий', max_length=200, blank=True, help_text='GitHub репозиторий (для проектов)')
    url = models.URLField('Ссылка', blank=True, help_text='Внешняя ссылка (для работы)')
    role = models.CharField('Роль', max_length=100, blank=True, help_text='например: ИТ-Специалист')
    date_range = models.CharField('Период', max_length=100, blank=True, help_text='например: Январь 2026 — настоящее время')
    sort_order = models.PositiveSmallIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'События'
        ordering = ['sort_order']

    def __str__(self):
        return f'{self.get_item_type_display()}: {self.title}'


class ContactInfo(models.Model):
    TYPE_CHOICES = [
        ('email', 'Email'),
        ('telegram', 'Telegram'),
    ]
    contact_type = models.CharField('Тип', max_length=10, choices=TYPE_CHOICES)
    label = models.CharField('Метка', max_length=100, help_text='Отображаемый текст')
    value = models.CharField('Значение', max_length=200, help_text='email или @username')
    sort_order = models.PositiveSmallIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'
        ordering = ['sort_order']

    def __str__(self):
        return f'{self.get_contact_type_display()}: {self.label}'
