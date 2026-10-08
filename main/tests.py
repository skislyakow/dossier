from pathlib import Path
from unittest import mock

from django.test import TestCase
from django.urls import reverse

from main import badge_utils
from main.models import Project


class HomeViewTest(TestCase):
    def setUp(self):
        self.response = self.client.get(reverse('home'))
        self.html = self.response.content.decode()

    def test_status_200(self):
        self.assertEqual(self.response.status_code, 200)

    def test_uses_correct_template(self):
        self.assertTemplateUsed(self.response, 'index.html')

    def test_contains_keywords(self):
        self.assertContains(self.response, 'Sergey Kislyakov')
        self.assertContains(self.response, 'Python')
        self.assertContains(self.response, 'Django')

    def test_hero_title_is_static(self):
        self.assertIn('Python Fullstack Developer', self.html)

    def test_hero_decor_removed(self):
        for fragment in (
            'typing.js',
            'typewriter.js',
            'ghost.js',
            'id="typing-text"',
            'class="terminal"',
            'class="hero-ghost"',
            'id="current-time"',
            'id="terminal-content"',
            'content-row',
            'content-column',
        ):
            self.assertNotIn(fragment, self.html)

    def test_section_order(self):
        pos_hero = self.html.index('<div class="hero">')
        pos_portfolio = self.html.index('id="portfolio"')
        pos_experience = self.html.index('id="timeline-details"')
        pos_skills = self.html.index('id="skills"')
        pos_contact = self.html.index('id="contact"')
        self.assertLess(pos_hero, pos_portfolio)
        self.assertLess(pos_portfolio, pos_experience)
        self.assertLess(pos_experience, pos_skills)
        self.assertLess(pos_skills, pos_contact)


class DesignSystemTest(TestCase):
    CSS_PATH = Path(__file__).resolve().parent.parent / 'static' / 'css' / 'style.css'

    def setUp(self):
        self.response = self.client.get(reverse('home'))
        self.html = self.response.content.decode()
        self.css = self.CSS_PATH.read_text(encoding='utf-8')

    def test_design_tokens(self):
        self.assertIn(':root', self.css)
        self.assertIn('--accent: #CDFF50', self.css)
        self.assertIn('--type-scale', self.css)
        self.assertIn('--text-card', self.css)
        self.assertIn('color-mix', self.css)
        self.assertNotIn('rgba(205, 255, 80', self.css)
        self.assertNotIn('#e4b592', self.css)
        self.assertNotIn('228, 181, 146', self.css)

    def test_hero_signature_markup(self):
        self.assertIn('Python-разработчик: автоматизация, Telegram-боты и веб на Django', self.html)
        self.assertIn('class="hero-name reveal"', self.html)
        self.assertIn('class="hero-positioning reveal"', self.html)

    def test_default_theme_dark(self):
        self.assertNotIn('<html lang="ru" data-theme="light">', self.html)
        self.assertIn('<html lang="ru">', self.html)

    def test_scroll_reveal_observer(self):
        self.assertIn('IntersectionObserver', self.html)

    def test_reduced_motion_guards(self):
        self.assertIn('prefers-reduced-motion', self.css)
        self.assertIn('prefers-reduced-motion', self.html)


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


class ApiGithubTest(TestCase):
    @mock.patch.object(badge_utils, '_get_json')
    def test_github_stats_without_network(self, mock_get):
        def fake(url, headers=None, timeout=None):
            if url.endswith('/users/skislyakow'):
                return {
                    'login': 'skislyakow',
                    'name': 'Sergey',
                    'avatar_url': 'http://x/a.png',
                    'html_url': 'https://github.com/skislyakow',
                    'bio': 'dev',
                }
            if 'repos?sort=stars' in url:
                return [{'name': 'repo1'}, {'name': 'repo2'}]
            if url.endswith('/languages'):
                return {'Python': 100, 'JavaScript': 50}
            return None

        mock_get.side_effect = fake

        response = self.client.get('/api/github/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['user']['login'], 'skislyakow')
        self.assertEqual(len(data['langs']), 2)
        by_lang = {lang['lang']: lang['percent'] for lang in data['langs']}
        self.assertEqual(by_lang['Python'], 67)
        self.assertEqual(by_lang['JavaScript'], 33)

