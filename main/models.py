from django.db import models


class Skill(models.Model):
    SIZE_CHOICES = [
        ('xl', 'XL'),
        ('lg', 'Large'),
        ('md', 'Medium'),
        ('sm', 'Small'),
    ]
    name = models.CharField(max_length=50, unique=True)
    size = models.CharField(max_length=2, choices=SIZE_CHOICES, default='sm')
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=200)
    repo = models.CharField(max_length=200, help_text='GitHub repo: username/repo')
    pypi = models.CharField(max_length=100, blank=True, help_text='PyPI package name (optional)')
    role = models.CharField(max_length=100, blank=True, help_text='e.g. Fullstack Development')
    tagline = models.TextField(blank=True)
    features = models.JSONField(default=list, help_text='List of feature strings')
    links = models.JSONField(default=dict, help_text='Dict of label->url, e.g. {"pypi": "https://..."}')
    badges_config = models.JSONField(default=list, help_text='List of badge objects: [{"label": "pypi", "source": "pypi_version"}]')
    order = models.PositiveSmallIntegerField(default=0)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class TimelineItem(models.Model):
    TYPE_CHOICES = [
        ('project', 'Project'),
        ('job', 'Job'),
        ('present', 'Present'),
    ]
    item_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    date_label = models.CharField(max_length=100, help_text='e.g. "Апрель 2026", "Январь 2026", "сейчас"')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    repo = models.CharField(max_length=200, blank=True, help_text='GitHub repo (for projects)')
    url = models.URLField(blank=True, help_text='External URL (for job)')
    role = models.CharField(max_length=100, blank=True, help_text='e.g. ИТ-Специалист')
    date_range = models.CharField(max_length=100, blank=True, help_text='e.g. "Январь 2026 — настоящее время"')
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.get_item_type_display()}: {self.title}'


class ContactInfo(models.Model):
    TYPE_CHOICES = [
        ('email', 'Email'),
        ('telegram', 'Telegram'),
    ]
    contact_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    label = models.CharField(max_length=100, help_text='Display text, e.g. "s.kislyakov84@gmail.com"')
    value = models.CharField(max_length=200, help_text='Actual value, e.g. email address or @username')
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Contact info'

    def __str__(self):
        return f'{self.get_contact_type_display()}: {self.label}'
