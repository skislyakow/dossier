import json

from django.conf import settings

from .models import ContactInfo, ResumeProfile, Skill


def _same_as(contacts):
    urls = []
    for c in contacts:
        if c.contact_type in ('github', 'telegram'):
            href = c.href()
            if href:
                urls.append(href)
    return urls


def person_json_ld():
    profile = ResumeProfile.load()
    data = {
        '@context': 'https://schema.org',
        '@type': 'Person',
        'name': profile.full_name,
        'url': f'{settings.SITE_URL}/',
        'image': f'{settings.SITE_URL}/static/og/og-image.png',
    }
    if profile.headline:
        data['jobTitle'] = profile.headline
    if profile.summary:
        data['description'] = profile.summary
    if profile.location:
        data['address'] = {'@type': 'PostalAddress', 'addressLocality': profile.location}
    same_as = _same_as(ContactInfo.objects.all())
    if same_as:
        data['sameAs'] = same_as
    skills = [s.name for s in Skill.objects.all()]
    if skills:
        data['knowsAbout'] = skills
    raw = json.dumps(data, ensure_ascii=False)
    return raw.replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')
