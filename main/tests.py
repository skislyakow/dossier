from html.parser import HTMLParser
from pathlib import Path
from unittest import mock

from django.test import TestCase
from django.urls import reverse

from main import badge_utils
from main.models import Project, Skill


class _ElementTree(HTMLParser):
    """Карта id -> список предков (тег.класс) для проверки разметки."""

    VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input',
            'link', 'meta', 'param', 'source', 'track', 'wbr'}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.ancestors = {}

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag not in self.VOID:
            self.stack.append(f"{tag}.{attrs.get('class', '')}")
        if attrs.get('id'):
            self.ancestors[attrs['id']] = list(self.stack)

    def handle_startendtag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get('id'):
            self.ancestors[attrs['id']] = list(self.stack)

    def handle_endtag(self, tag):
        if tag not in self.VOID and self.stack:
            self.stack.pop()


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
    JS_PATH = Path(__file__).resolve().parent.parent / 'static' / 'js' / 'timeline.js'
    PORTFOLIO_JS_PATH = Path(__file__).resolve().parent.parent / 'static' / 'js' / 'portfolio.js'

    def setUp(self):
        self.response = self.client.get(reverse('home'))
        self.html = self.response.content.decode()
        self.css = self.CSS_PATH.read_text(encoding='utf-8')

    def css_rule(self, selector):
        start = self.css.index(selector)
        return self.css[start:self.css.index('}', start)]

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

    def test_timeline_rail_vertical(self):
        self.assertIn('position: fixed', self.css_rule('.hero-timeline {'))
        self.assertIn('transition: height', self.css_rule('.tl-progress'))
        self.assertIn('.hero-timeline.compact', self.css)
        self.assertIn('right: calc(100% + 6px)', self.css_rule('.hero-timeline.compact .tl-label'))
        self.assertIn(
            '.hero-timeline { display: none; } .tl-details { display: none; }',
            ' '.join(self.css.split()),
        )
        js = self.JS_PATH.read_text(encoding='utf-8')
        self.assertNotIn('3600', js)
        self.assertIn('initRailMode', js)

    def test_timeline_rail_is_page_chrome(self):
        parser = _ElementTree()
        parser.feed(self.html)
        ancestors = parser.ancestors.get('hero-timeline', [])
        self.assertTrue(ancestors)
        self.assertNotIn('div.hero', ancestors)

    def test_page_chrome_marquee(self):
        self.assertIn('<div class="marquee" aria-hidden="true">', self.html)
        pos_marquee = self.html.index('class="marquee"')
        self.assertLess(self.html.index('<div class="hero">'), pos_marquee)
        self.assertLess(pos_marquee, self.html.index('<div class="content-body">'))
        self.assertIn('@keyframes marquee', self.css)
        self.assertIn('animation: marquee', self.css_rule('.marquee-track'))
        self.assertIn(
            '.marquee-track { animation: none; }',
            ' '.join(self.css.split()),
        )

    def test_page_chrome_uses_single_accent(self):
        self.assertNotIn('#0088cc', self.css)
        self.assertIn('aria-label="Наверх"', self.html)
        self.assertIn('aria-label="Переключить тему"', self.html)
        self.assertIn('aria-label="GitHub"', self.html)
        self.assertIn('aria-label="Telegram"', self.html)

    def test_skills_section_grouped_by_category(self):
        self.assertIn('class="skill-group"', self.html)
        self.assertIn('class="skill-group-title"', self.html)
        self.assertIn('Bots & Integrations', self.html)
        self.assertIn('s.category', self.html)
        self.assertIn('if (!items.length) return;', self.html)

    def test_skills_curly_cloud_removed(self):
        self.assertNotIn('content: "{ "', self.css)
        self.assertNotIn('content: " }"', self.css)
        self.assertIn('.skill-group-title', self.css)

    def test_enhanced_card_format_and_escapes(self):
        js = self.PORTFOLIO_JS_PATH.read_text(encoding='utf-8')
        for fragment in ('portfolio-tagline', 'portfolio-features', 'portfolio-badges', 'portfolio-links'):
            self.assertIn(fragment, js)
        self.assertIn('function esc(', js)
        self.assertIn('${esc(', js)
        self.assertNotIn('portfolio-ghost-skill', js)
        self.assertNotIn('ghost', js)

    def test_enhanced_card_surface_and_motion_guards(self):
        rule = self.css_rule('.portfolio-preview-body')
        self.assertIn('background: var(--bg-card)', rule)
        self.assertIn('transform: translate3d', rule)
        self.assertIn(
            '.portfolio-preview-body { transform: none; transition: none; }',
            ' '.join(self.css.split()),
        )
        self.assertNotIn('ghostFloat', self.css)
        js = self.PORTFOLIO_JS_PATH.read_text(encoding='utf-8')
        self.assertIn('prefers-reduced-motion', js)
        self.assertIn('IntersectionObserver', js)


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


class ApiSkillsTest(TestCase):
    def setUp(self):
        Skill.objects.update(category='tools')
        Skill.objects.create(name='TestBackend', category='backend', size='md')
        Skill.objects.create(name='TestWeb', category='web', size='sm')

    def test_api_skills_returns_category(self):
        response = self.client.get('/api/skills/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        valid = {code for code, _label in Skill.CATEGORY_CHOICES}
        for skill in data:
            self.assertIn('category', skill)
            self.assertIn(skill['category'], valid)
        by_name = {s['name']: s for s in data}
        self.assertEqual(by_name['TestBackend']['category'], 'backend')
        self.assertEqual(by_name['TestWeb']['category'], 'web')


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

