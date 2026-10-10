from collections import Counter

from django.shortcuts import render
from django.http import JsonResponse
from .models import Skill, Project, TimelineItem, ContactInfo
from .badge_utils import enrich_project, fetch_github_stats


def home(request):
    return render(request, 'index.html')


def skill_size(count):
    if count >= 5:
        return 'xl'
    if count >= 3:
        return 'lg'
    if count >= 1:
        return 'md'
    return 'sm'


def api_skills(request):
    tag_counts = Counter()
    for p in Project.objects.filter(is_published=True):
        tag_counts.update(p.tags or [])
    return JsonResponse([
        {
            'name': s.name,
            'category': s.category,
            'size': skill_size(tag_counts.get(s.filter_tag or s.name, 0)),
            'filter_tag': s.filter_tag,
        }
        for s in Skill.objects.all()
    ], safe=False)


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
