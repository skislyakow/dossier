import os
from pathlib import Path

from django.conf import settings
from django.template.loader import render_to_string

from .models import ContactInfo, Project, ResumeProfile, Skill, TimelineItem


def _resume_sort_key(item):
    if item.start_date:
        return (-item.start_date.toordinal(), item.sort_order)
    return (10**9, item.sort_order)


def context():
    profile = ResumeProfile.load()
    experience = sorted(
        [i for i in TimelineItem.objects.all() if i.item_type != 'project'],
        key=_resume_sort_key,
    )
    projects = list(Project.objects.filter(is_published=True).order_by('sort_order'))
    skills = {code: [] for code, _label in Skill.CATEGORY_CHOICES}
    for s in Skill.objects.all().order_by('sort_order'):
        skills[s.category].append(s.name)
    skill_groups = [(label, names) for code, label in Skill.CATEGORY_CHOICES for names in [skills[code]] if names]
    return {
        'profile': profile,
        'contacts': list(ContactInfo.objects.all()),
        'experience': experience,
        'projects': projects,
        'skill_groups': skill_groups,
    }


def pdf_path():
    root = settings.STATIC_ROOT
    if os.access(root, os.W_OK):
        return os.path.join(root, 'resume', 'resume.pdf')
    return os.path.join(str(Path(settings.STATICFILES_DIRS[0]) / 'resume'), 'resume.pdf')


def build_pdf():
    from weasyprint import HTML

    ctx = context()
    body = render_to_string('resume/_body.html', ctx)
    css = (Path(settings.STATICFILES_DIRS[0]) / 'css' / 'resume.css').read_text(encoding='utf-8')
    html = (
        '<!DOCTYPE html><html lang="ru"><head><meta charset="utf-8">'
        f'<title>Резюме — {ctx["profile"].full_name}</title>'
        f'<style>{css}</style></head>'
        f'<body class="resume-print">{body}</body></html>'
    )
    return HTML(string=html).write_pdf()


def write_pdf():
    path = pdf_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as f:
        f.write(build_pdf())
    return path