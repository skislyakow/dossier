from unittest import mock

from django.conf import settings
from django.test import TestCase
from django.urls import reverse

from main import fetch
from main import taxonomy
from main.fetch import MemoryTransport
from main.models import ContactInfo, Project, Skill


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
        pos_experience = self.html.index('id="experience"')
        pos_skills = self.html.index('id="skills"')
        pos_contact = self.html.index('id="contact"')
        self.assertLess(pos_hero, pos_portfolio)
        self.assertLess(pos_portfolio, pos_experience)
        self.assertLess(pos_experience, pos_skills)
        self.assertLess(pos_skills, pos_contact)


class RobotsTxtTest(TestCase):
    def test_robots_txt_disallows_admin_and_api(self):
        response = self.client.get('/robots.txt')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/plain')
        body = response.content.decode()
        self.assertIn('User-agent: *', body)
        self.assertIn('Disallow: /admin/', body)
        self.assertIn('Disallow: /api/', body)
        self.assertIn(f'Sitemap: {settings.SITE_URL}/sitemap.xml', body)


class SitemapXmlTest(TestCase):
    def test_sitemap_is_valid_xml_with_canonical_urls(self):
        import xml.etree.ElementTree as ET

        response = self.client.get('/sitemap.xml')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/xml')
        root = ET.fromstring(response.content.decode())
        ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        locs = [loc.text for loc in root.findall('sm:url/sm:loc', ns)]
        self.assertEqual(locs, [f'{settings.SITE_URL}/', f'{settings.SITE_URL}/resume/'])


class ApiTimelineTest(TestCase):
    def test_api_timeline_shape(self):
        response = self.client.get('/api/timeline/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        for key in ('prior', 'job', 'present', 'timeline'):
            self.assertTrue(data[key], f'empty: {key}')
        self.assertGreaterEqual(len(data['timeline']), 3)
        for key in ('date', 'title', 'desc'):
            self.assertIn(key, data['prior'])


class ApiContactTest(TestCase):
    def test_api_contact_shape_and_github(self):
        response = self.client.get('/api/contact/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        valid = {code for code, _label in ContactInfo.TYPE_CHOICES}
        types = set()
        for item in data:
            for key in ('type', 'type_label', 'label', 'value', 'href', 'external'):
                self.assertIn(key, item)
            self.assertIn(item['type'], valid)
            self.assertEqual(item['type_label'], dict(ContactInfo.TYPE_CHOICES)[item['type']])
            self.assertIsInstance(item['external'], bool)
            types.add(item['type'])
        self.assertIn('github', types)
        github = next(i for i in data if i['type'] == 'github')
        self.assertEqual(github['value'], 'skislyakow')
        self.assertEqual(github['href'], 'https://github.com/skislyakow')
        self.assertTrue(github['external'])
        external_email = [i for i in data if i['type'] != 'email']
        self.assertTrue(all(i['external'] for i in external_email))

    def test_contact_href_builders(self):
        self.assertEqual(
            ContactInfo(contact_type='telegram', value='@user').href(), 'https://t.me/user')
        self.assertEqual(
            ContactInfo(contact_type='github', value='@user').href(), 'https://github.com/user')
        self.assertEqual(
            ContactInfo(contact_type='email', value='a@b.c').href(), 'mailto:a@b.c')
        self.assertEqual(ContactInfo(contact_type='email', value='a@b.c').is_external(), False)
        self.assertEqual(ContactInfo(contact_type='telegram', value='x').is_external(), True)


class ApiSkillsTest(TestCase):
    def setUp(self):
        Skill.objects.update(category='tools')
        Skill.objects.create(name='TestBackend', category='backend')
        Skill.objects.create(name='TestWeb', category='web')
        Skill.objects.create(name='TestBots', category='bots', filter_tag='Telegram')

    def _data(self):
        response = self.client.get('/api/skills/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['categories'], [
            {'code': code, 'label': label} for code, label in Skill.CATEGORY_CHOICES
        ])
        return data['skills']

    def test_api_skills_returns_category_and_label(self):
        skills = self._data()
        codes = {code for code, _label in Skill.CATEGORY_CHOICES}
        labels = dict(Skill.CATEGORY_CHOICES)
        for skill in skills:
            self.assertIn('category', skill)
            self.assertIn('tag', skill)
            self.assertIn('category_label', skill)
            self.assertIn(skill['category'], codes)
            self.assertEqual(skill['category_label'], labels[skill['category']])
        by_name = {s['name']: s for s in skills}
        self.assertEqual(by_name['TestBackend']['category'], 'backend')
        self.assertEqual(by_name['TestBackend']['category_label'], 'Backend')
        self.assertEqual(by_name['TestWeb']['category'], 'web')
        self.assertEqual(by_name['TestBackend']['tag'], 'TestBackend')
        self.assertEqual(by_name['TestBots']['tag'], 'Telegram')

    def test_api_skills_computes_size_from_project_tags(self):
        skills = self._data()
        by_name = {s['name']: s for s in skills}
        self.assertEqual(by_name['TestBots']['size'], 'lg')
        self.assertEqual(by_name['TestBackend']['size'], 'sm')
        self.assertEqual(by_name['TestWeb']['size'], 'sm')

    def test_api_skills_ignores_unpublished_projects(self):
        for i in range(4):
            Project.objects.create(title=f'P{i}', repo=f'owner/p{i}', tags=['TestBackend'])
        Project.objects.create(title='Hidden', repo='owner/h', tags=['TestBackend'], is_published=False)
        by_name = {s['name']: s for s in self._data()}
        self.assertEqual(by_name['TestBackend']['size'], 'lg')


class TaxonomyTest(TestCase):
    def setUp(self):
        Project.objects.all().delete()

    def test_skill_size_buckets(self):
        expected = [(0, 'sm'), (1, 'md'), (2, 'md'), (3, 'lg'), (4, 'lg'), (5, 'xl'), (99, 'xl')]
        for count, size in expected:
            self.assertEqual(taxonomy.skill_size(count), size)

    def test_resolve_tag_falls_back_to_name(self):
        self.assertEqual(taxonomy.resolve_tag(Skill(name='Django', filter_tag='')), 'Django')
        self.assertEqual(taxonomy.resolve_tag(Skill(name='Telegram Bot API', filter_tag='Telegram')), 'Telegram')

    def test_tag_cloud_counts_and_sorts_published(self):
        Project.objects.create(title='A', repo='u/a', tags=['Python', 'Django'])
        Project.objects.create(title='B', repo='u/b', tags=['Django'])
        Project.objects.create(title='H', repo='u/h', tags=['Hidden'], is_published=False)
        self.assertEqual(taxonomy.tag_cloud(), [
            {'name': 'Django', 'count': 2, 'size': 'md'},
            {'name': 'Python', 'count': 1, 'size': 'md'},
        ])

    def test_api_tags_returns_cloud(self):
        Project.objects.create(title='A', repo='u/a', tags=['Django', 'Django'])
        response = self.client.get('/api/tags/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [
            {'name': 'Django', 'count': 2, 'size': 'md'},
        ])


class ApiProjectsEnrichTest(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            title='Test Project',
            repo='owner/repo',
            pypi='pkg',
            tags=['python', 'redis'],
            badges_config=[
                {'label': 'stars', 'source': 'github_stars'},
                {'label': 'ver', 'source': 'pypi_version'},
                {'label': 'note', 'value': 'static'},
            ],
            is_published=True,
        )

    @mock.patch.object(fetch, 'transport', MemoryTransport({
        'https://api.github.com/repos/owner/repo': {
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
        },
        'https://api.github.com/repos/owner/repo/languages': {'Python': 100},
        'https://pypi.org/pypi/pkg/json': {'info': {'version': '1.2.3', 'requires_python': '>=3.8', 'license': 'MIT'}},
        'https://pypistats.org/api/packages/pkg/recent': {'data': {'last_month': 500, 'total': 6000}},
    }))
    def test_enriched_without_network(self):
        response = self.client.get('/api/projects/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        p = next(x for x in data if x['title'] == 'Test Project')
        self.assertEqual(p['stars'], 42)
        self.assertEqual(p['langs'], {'Python': 100})
        self.assertEqual(p['tags'], ['python', 'redis'])
        self.assertEqual(p['repo']['html_url'], 'https://github.com/owner/repo')
        by_label = {b['label']: b.get('value') for b in p['badges']}
        self.assertEqual(by_label['stars'], '42')
        self.assertEqual(by_label['ver'], 'v1.2.3')
        self.assertEqual(by_label['note'], 'static')


class ProjectTagsDefaultTest(TestCase):
    def test_tags_default_empty(self):
        project = Project.objects.create(title='No Tags', repo='owner/none')
        self.assertEqual(project.tags, [])


class ApiGithubTest(TestCase):
    @mock.patch.object(fetch, 'transport', MemoryTransport({
        'https://api.github.com/users/skislyakow': {
            'login': 'skislyakow',
            'name': 'Sergey',
            'avatar_url': 'http://x/a.png',
            'html_url': 'https://github.com/skislyakow',
            'bio': 'dev',
        },
        'https://api.github.com/users/skislyakow/repos?sort=stars&per_page=6': [
            {'name': 'repo1'}, {'name': 'repo2'},
        ],
        'https://api.github.com/repos/skislyakow/repo1': {'name': 'repo1'},
        'https://api.github.com/repos/skislyakow/repo1/languages': {'Python': 100},
        'https://api.github.com/repos/skislyakow/repo2': {'name': 'repo2'},
        'https://api.github.com/repos/skislyakow/repo2/languages': {'JavaScript': 50},
    }))
    def test_github_stats_without_network(self):
        response = self.client.get('/api/github/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['user']['login'], 'skislyakow')
        self.assertEqual(len(data['langs']), 2)
        by_lang = {lang['lang']: lang['percent'] for lang in data['langs']}
        self.assertEqual(by_lang['Python'], 67)
        self.assertEqual(by_lang['JavaScript'], 33)