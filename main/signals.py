import os

from django.conf import settings
from django.db.models.signals import post_delete, post_save

from .models import ContactInfo, Project, ResumeProfile, Skill, TimelineItem


def _autogen_enabled():
    value = os.environ.get('RESUME_AUTOGEN')
    if value is not None:
        return value.lower() not in ('0', 'false', 'no', '')
    if os.environ.get('PYTEST_CURRENT_TEST'):
        return False
    return getattr(settings, 'RESUME_AUTOGEN', True)


def _regenerate_resume(sender, **kwargs):
    if not _autogen_enabled():
        return
    try:
        from .resume import write_pdf
        write_pdf()
    except Exception:
        # резюме — вторичный артефакт: сбой генерации не должен ломать правку контента
        pass


def connect():
    models = (Project, TimelineItem, Skill, ContactInfo, ResumeProfile)
    for model in models:
        post_save.connect(_regenerate_resume, sender=model)
        post_delete.connect(_regenerate_resume, sender=model)