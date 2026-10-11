from django.db import models


class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('backend', 'Backend'),
        ('web', 'Web'),
        ('devops', 'DevOps'),
        ('bots', 'Bots & Integrations'),
        ('tools', 'Tools'),
    ]
    name = models.CharField('Название', max_length=50, unique=True)
    category = models.CharField('Категория', max_length=10, choices=CATEGORY_CHOICES, default='tools')
    filter_tag = models.CharField('Тег фильтра проектов', max_length=50, blank=True, help_text='Тег проекта, по которому клик по навыку фильтрует список проектов (пусто — по имени навыка)')
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
    tags = models.JSONField('Теги', default=list, blank=True, help_text='Курируемые метки стека, например ["Django", "Redis"]')
    links = models.JSONField('Ссылки', default=dict, blank=True, help_text='{"pypi": "https://...", "www": "https://..."}')
    badges_config = models.JSONField('Бейджи', default=list, blank=True, help_text='[{"label": "pypi", "source": "pypi_version"}]')
    screenshot = models.URLField('Скриншот', blank=True, help_text='URL изображения для карточки проекта')
    date_label = models.CharField('Период (резюме)', max_length=100, blank=True, help_text='например: 2024–2025')
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
    start_date = models.DateField('Дата начала', null=True, blank=True, help_text='Для хронологии резюме (опционально)')
    end_date = models.DateField('Дата конца', null=True, blank=True, help_text='Для хронологии резюме (опционально)')
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


class ResumeProfile(models.Model):
    full_name = models.CharField('Имя', max_length=200, default='Сергей Кисляков')
    headline = models.CharField('Целевая роль', max_length=200, blank=True)
    summary = models.TextField('Резюме-описание', blank=True)
    location = models.CharField('Локация', max_length=200, blank=True)
    education = models.TextField('Образование', blank=True)

    class Meta:
        verbose_name = 'Профиль резюме'
        verbose_name_plural = 'Профиль резюме'

    def __str__(self):
        return self.full_name

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(id=1)
        return obj


class ContactInfo(models.Model):
    TYPE_CHOICES = [
        ('email', 'Email'),
        ('telegram', 'Telegram'),
        ('github', 'GitHub'),
    ]
    contact_type = models.CharField('Тип', max_length=10, choices=TYPE_CHOICES)
    label = models.CharField('Метка', max_length=100, help_text='Отображаемый текст')
    value = models.CharField('Значение', max_length=200, help_text='email, @username или username GitHub')
    sort_order = models.PositiveSmallIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'
        ordering = ['sort_order']

    def __str__(self):
        return f'{self.get_contact_type_display()}: {self.label}'

    def href(self):
        value = (self.value or '').lstrip('@')
        if self.contact_type == 'email':
            return f'mailto:{self.value or ""}'
        if self.contact_type == 'telegram':
            return f'https://t.me/{value}'
        if self.contact_type == 'github':
            return f'https://github.com/{value}'
        return ''

    def is_external(self):
        return self.contact_type != 'email'
