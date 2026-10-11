import os

from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, FileResponse, Http404
from .models import Skill, Project, TimelineItem, ContactInfo
from .taxonomy import resolve_tag, skill_size, tag_cloud, tag_counts
from .badge_utils import enrich_project
from .fetch import fetch_github_stats
from .resume import context, pdf_path
from .seo import person_json_ld


def home(request):
    return render(request, 'index.html', {'person_ld': person_json_ld()})


def robots_txt(request):
    lines = [
        'User-agent: *',
        'Disallow: /admin/',
        'Disallow: /api/',
        '',
        f'Sitemap: {settings.SITE_URL}/sitemap.xml',
        '',
    ]
    return HttpResponse('\n'.join(lines), content_type='text/plain')


def sitemap_xml(request):
    pages = ['', 'resume/']
    urls = '\n'.join(
        f'  <url><loc>{settings.SITE_URL}/{page}</loc></url>' for page in pages
    )
    body = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f'{urls}\n'
        '</urlset>\n'
    )
    return HttpResponse(body, content_type='application/xml')


def resume(request):
    return render(request, 'resume.html', context())


def resume_pdf(request):
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
    skills = [
        {
            'name': s.name,
            'category': s.category,
            'category_label': s.get_category_display(),
            'size': skill_size(counts.get(resolve_tag(s), 0)),
            'tag': resolve_tag(s),
        }
        for s in Skill.objects.all()
    ]
    categories = [{'code': code, 'label': label} for code, label in Skill.CATEGORY_CHOICES]
    return JsonResponse({'skills': skills, 'categories': categories})


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
            'type_label': c.get_contact_type_display(),
            'label': c.label,
            'value': c.value,
            'href': c.href(),
            'external': c.is_external(),
        }
        for c in contacts
    ], safe=False)


def api_github(request):
    return JsonResponse(fetch_github_stats())
