from django.test import TestCase, Client
from django.urls import reverse


class HomeViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_status_200(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'index.html')

    def test_contains_keywords(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'Sergey Kislyakov')
        self.assertContains(response, 'terminal')
        self.assertContains(response, 'Python')
        self.assertContains(response, 'Django')


from unittest import mock
from main.models import Project
from main import badge_utils


class ApiProjectsEnrichTest(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            title='Test Project',
            repo='owner/repo',
            pypi='pkg',
            badges_config=[
                {'label': 'stars', 'source': 'github_stars'},
                {'label': 'ver', 'source': 'pypi_version'},
                {'label': 'note', 'value': 'static'},
            ],
            is_published=True,
        )

    @mock.patch.object(badge_utils, '_get_json')
    def test_enriched_without_network(self, mock_get):
        def fake(url, headers=None, timeout=None):
            if 'languages' in url:
                return {'Python': 100}
            if 'api.github.com/repos/owner/repo' in url:
                return {
                    'stargazers_count': 42,
                    'forks_count': 3,
                    'full_name': 'owner/repo',
                    'html_url': 'https://github.com/owner/repo',
                    'language': 'Python',
                    'open_issues_count': 1,
                    'size': 2048,
                    'created_at': '2020-01-01T00:00:00Z',
                    'pushed_at': '2021-01-01T00:00:00Z',
                    'license': {'spdx_id': 'MIT'},
                }
            if 'pypi.org' in url:
                return {'info': {'version': '1.2.3', 'requires_python': '>=3.8', 'license': 'MIT'}}
            if 'pypistats' in url:
                return {'data': {'last_month': 500, 'total': 6000}}
            return None

        mock_get.side_effect = fake

        response = self.client.get('/api/projects/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        p = next(x for x in data if x['title'] == 'Test Project')
        self.assertEqual(p['stars'], 42)
        self.assertEqual(p['langs'], {'Python': 100})
        self.assertEqual(p['repo']['html_url'], 'https://github.com/owner/repo')
        by_label = {b['label']: b.get('value') for b in p['badges']}
        self.assertEqual(by_label['stars'], '42')
        self.assertEqual(by_label['ver'], 'v1.2.3')
        self.assertEqual(by_label['note'], 'static')

