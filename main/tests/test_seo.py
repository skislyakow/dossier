import json
import re

from django.conf import settings
from django.test import TestCase

from main import seo
from main.models import ContactInfo, ResumeProfile, Skill


class PersonJsonLdTest(TestCase):
    def setUp(self):
        self.profile = ResumeProfile.load()
        self.profile.full_name = 'Сергей Кисляков'
        self.profile.headline = 'Python Fullstack Developer'
        self.profile.summary = 'Django, автоматизация, боты.'
        self.profile.location = 'Москва'
        self.profile.save()
        ContactInfo.objects.create(contact_type='github', label='GitHub', value='skislyakow')
        ContactInfo.objects.create(contact_type='telegram', label='Telegram', value='@skislyakov')
        ContactInfo.objects.create(contact_type='email', label='Email', value='a@b.c')
        Skill.objects.update_or_create(name='Django', defaults={'category': 'backend'})

    def test_person_shape(self):
        data = json.loads(seo.person_json_ld())
        self.assertEqual(data['@context'], 'https://schema.org')
        self.assertEqual(data['@type'], 'Person')
        self.assertEqual(data['name'], 'Сергей Кисляков')
        self.assertEqual(data['jobTitle'], 'Python Fullstack Developer')
        self.assertEqual(data['url'], f'{settings.SITE_URL}/')
        self.assertEqual(data['image'], f'{settings.SITE_URL}/static/og/og-image.png')
        self.assertEqual(data['address']['addressLocality'], 'Москва')

    def test_same_as_excludes_email(self):
        data = json.loads(seo.person_json_ld())
        self.assertIn('https://github.com/skislyakow', data['sameAs'])
        self.assertIn('https://t.me/skislyakov', data['sameAs'])
        self.assertFalse(any(url.startswith('mailto:') for url in data['sameAs']))

    def test_knows_about_lists_skills(self):
        data = json.loads(seo.person_json_ld())
        self.assertIn('Django', data['knowsAbout'])

    def test_special_chars_are_escaped(self):
        self.profile.full_name = 'X</script><b>&'
        self.profile.save()
        raw = seo.person_json_ld()
        self.assertNotIn('<', raw)
        self.assertNotIn('>', raw)
        self.assertNotIn('&', raw)
        self.assertEqual(json.loads(raw)['name'], 'X</script><b>&')


class PersonJsonLdInHomeTest(TestCase):
    def test_home_embeds_ld_json(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        match = re.search(
            r'<script type="application/ld\+json">(.*?)</script>',
            response.content.decode(),
            re.DOTALL,
        )
        self.assertIsNotNone(match)
        data = json.loads(match.group(1))
        self.assertEqual(data['@type'], 'Person')
