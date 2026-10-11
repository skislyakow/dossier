import os

from django.shortcuts import render
from django.http import JsonResponse, FileResponse, Http404
from .models import Skill, Project, TimelineItem, ContactInfo
from .taxonomy import resolve_tag, skill_size, tag_cloud, tag_counts
from .badge_utils import enrich_project, fetch_github_stats


def home(request):
    return render(request, 'index.html')


def resume(request):
    from .resume import context
    return render(request, 'resume.html', context())


def resume_pdf(request):
    from .resume import pdf_path
    path = pdf_path()
    if not os.path.exists(path):
        raise Http404('Резюме ещё не сгенерировано: запустите uv run manage.py generate_resume')
    return FileResponse(
        open(path, 'rb'),
        content_type='application/pdf',
        filename='Sergey-Kislyakov-resume.pdf',
    )


def api_skills(request):
    counts = tag_counts()
    return JsonResponse([
        {
            'name': s.name,
            'category': s.category,
            'size': skill_size(counts.get(resolve_tag(s), 0)),
            'tag': resolve_tag(s),
        }
        for s in Skill.objects.all()
    ], safe=False)


def api_tags(request):
    return JsonResponse(tag_cloud(), safe=False)


def api_projects(request):
    projects = Project.objects.filter(is_published=True)
    data = []
    for p in projects:
        enriched = enrich_project(p)
        data.append({
            'repo': enriched['repo'],
            'pypi': p.pypi or None,
            'title': p.title,
            'role': p.role or None,
            'tagline': p.tagline,
            'features': p.features,
            'tags': p.tags or [],
            'links': p.links,
            'badges': enriched['badges'],
            'screenshot': p.screenshot or None,
            'langs': enriched['langs'],
            'stars': enriched['stars'],
        })
    return JsonResponse(data, safe=False)


def api_timeline(request):
    items = TimelineItem.objects.all()
    prior = None
    job = None
    present = None
    timeline = []

    for item in items:
        obj = {
            'date': item.date_label,
            'title': item.title,
            'desc': item.description,
        }
        if item.item_type == 'prior':
            prior = {
                'date': item.date_label,
                'title': item.title,
                'desc': item.description,
            }
        elif item.item_type == 'job':
            job = {
                'title': item.title,
                'role': item.role,
                'dateRange': item.date_range,
                'url': item.url,
                'desc': item.description,
            }
        elif item.item_type == 'present':
            present = {
                'title': item.title,
                'desc': item.description,
            }
        else:
            obj['repo'] = item.repo
            timeline.append(obj)

    return JsonResponse({
        'prior': prior,
        'job': job,
        'present': present,
        'timeline': timeline,
    })


def api_contact(request):
    contacts = ContactInfo.objects.all()
    return JsonResponse([
        {
            'type': c.contact_type,
            'label': c.label,
            'value': c.value,
        }
        for c in contacts
    ], safe=False)


def api_github(request):
    return JsonResponse(fetch_github_stats())
