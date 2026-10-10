from html.parser import HTMLParser
from importlib import import_module
from pathlib import Path
from unittest import mock

from django.test import TestCase
from django.urls import reverse

from main import badge_utils
from main.models import ContactInfo, Project, Skill


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
        pos_experience = self.html.index('id="experience"')
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
            '.hero-timeline { display: none; }',
            ' '.join(self.css.split()),
        )

    def test_rail_and_timeline_hidden_while_panel_open(self):
        css = ' '.join(self.css.split())
        self.assertIn(
            'body:has(#portfolio.show, #stats.show, #contact.show) .hero-timeline'
            ' { opacity: 0; visibility: hidden; pointer-events: none; }',
            css,
        )
        self.assertIn(
            'body:has(#portfolio.show, #stats.show, #contact.show) .portfolio'
            ' { padding-right: 2rem; }',
            css,
        )
        self.assertIn('body:has(#portfolio.show) #experience { display: none; }', css)
        js = self.JS_PATH.read_text(encoding='utf-8')
        self.assertNotIn('3600', js)
        self.assertIn('initRailMode', js)

    def test_experience_section_chronology_and_escapes(self):
        self.assertIn('id="experience"', self.html)
        self.assertIn('.experience', self.css)
        self.assertIn('.exp-list', self.css)
        self.assertIn('.exp-item', self.css)
        self.assertNotIn('tl-details', self.css)
        js = self.JS_PATH.read_text(encoding='utf-8')
        self.assertIn('function tlEsc(', js)
        self.assertIn('exp-list', js)
        self.assertIn('prefers-reduced-motion', js)
        for raw in ('+ d.title +', '+ d.desc +', '+ d.repo +', '+ d.role +'):
            self.assertNotIn(raw, js)
        self.assertNotIn('timeline-details', js)
        self.assertNotIn('tl-details', js)

    def test_contact_section_three_channels_and_escapes(self):
        self.assertIn('id="contact-card"', self.html)
        self.assertIn('contact-grid', self.html)
        self.assertIn('contact-kind', self.html)
        self.assertIn('contact-value', self.html)
        self.assertIn("https://github.com/' + v.replace(/^@/, '')", self.html)
        self.assertIn('esc(item.label)', self.html)
        self.assertIn('esc(href)', self.html)
        self.assertIn('.contact-grid', self.css)
        self.assertIn('.contact-item', self.css)
        self.assertIn('.sec-label', self.css)
        self.assertNotIn('#27272a', self.css)
        self.assertNotIn('rgba(250, 250, 250', self.css)

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
        self.assertNotIn('.tag::before', self.css)
        self.assertNotIn('.tag::after', self.css)
        self.assertIn('.skill-group-title', self.css)

    def test_project_tag_cloud(self):
        self.assertIn('.ptag::before', self.css)
        self.assertIn('content: "{ "', self.css_rule('.ptag::before'))
        for size in ('ptag-xl', 'ptag-lg', 'ptag-md', 'ptag-sm'):
            self.assertIn(f'.{size}', self.css)
        js = self.PORTFOLIO_JS_PATH.read_text(encoding='utf-8')
        self.assertIn('portfolio-ptags', js)
        self.assertIn('data-tag', js)
        self.assertIn('applyFilters', js)
        self.assertIn("${esc(tag)}", js)

    def test_enhanced_card_format_and_escapes(self):
        js = self.PORTFOLIO_JS_PATH.read_text(encoding='utf-8')
        for fragment in ('portfolio-tagline', 'portfolio-features', 'portfolio-badges', 'portfolio-links'):
            self.assertIn(fragment, js)
        self.assertIn('function esc(', js)
        self.assertIn('${esc(', js)
        for raw in ('${project.title}', '${project.tagline}', '${project.role}', '${b.label}', '${f}'):
            self.assertNotIn(raw, js)
        self.assertNotIn('portfolio-ghost-skill', js)
        self.assertNotIn('ghostFloat', js)

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

    def test_portfolio_eager_reveal_without_observer(self):
        js = self.PORTFOLIO_JS_PATH.read_text(encoding='utf-8')
        self.assertIn('function revealNow(', js)
        self.assertNotIn('function revealIn(', js)
        self.assertNotIn('IntersectionObserver', js)

    def test_mobile_hides_preview_media(self):
        css = ' '.join(self.css.split())
        self.assertIn('.portfolio-preview-media { display: none; }', css)

    def test_skills_are_clickable_filter_buttons(self):
        self.assertIn('<button type="button" class="tag tag-', self.html)
        self.assertIn('data-skill="', self.html)
        self.assertIn('data-filter-tag="', self.html)
        self.assertIn('window.__applyPortfolioTag', self.html)
        self.assertIn('.skills-cloud .tag {', self.css)
        self.assertIn('cursor: pointer', self.css_rule('.skills-cloud .tag'))
        js = self.PORTFOLIO_JS_PATH.read_text(encoding='utf-8')
        self.assertIn('window.__applyPortfolioTag', js)
        self.assertIn('data-filter-tag', self.html)
        self.assertIn('.portfolio-empty', self.css)

    def test_reduced_motion_disables_all_animations(self):
        css = ' '.join(self.css.split())
        self.assertIn('.reveal { opacity: 1; transform: none; transition: none; }', css)
        self.assertIn('.marquee-track { animation: none; }', css)
        self.assertIn('.portfolio-preview-body { transform: none; transition: none; }', css)
        self.assertIn('.hero-text h1 { background-image: none;', css)
        self.assertIn('.hero-blur { backdrop-filter: none;', css)
        self.assertIn('.hero-timeline { transition: none; }', css)


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
            for key in ('type', 'label', 'value'):
                self.assertIn(key, item)
            self.assertIn(item['type'], valid)
            types.add(item['type'])
        self.assertIn('github', types)
        github = next(i for i in data if i['type'] == 'github')
        self.assertEqual(github['value'], 'skislyakow')


class ApiSkillsTest(TestCase):
    def setUp(self):
        Skill.objects.update(category='tools')
        Skill.objects.create(name='TestBackend', category='backend', size='md')
        Skill.objects.create(name='TestWeb', category='web', size='sm')
        Skill.objects.create(name='TestBots', category='bots', size='md', filter_tag='Telegram')

    def test_api_skills_returns_category(self):
        response = self.client.get('/api/skills/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        valid = {code for code, _label in Skill.CATEGORY_CHOICES}
        for skill in data:
            self.assertIn('category', skill)
            self.assertIn('filter_tag', skill)
            self.assertIn(skill['category'], valid)
        by_name = {s['name']: s for s in data}
        self.assertEqual(by_name['TestBackend']['category'], 'backend')
        self.assertEqual(by_name['TestWeb']['category'], 'web')
        self.assertEqual(by_name['TestBackend']['filter_tag'], '')
        self.assertEqual(by_name['TestBots']['filter_tag'], 'Telegram')


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


class MigrationSkillFilterTagSeedTest(TestCase):
    TAGS_BY_REPO = {
        'skislyakow/opencode-py': ['Python', 'httpx', 'Pydantic', 'PyPI', 'opencode-py'],
        'skislyakow/ferma': ['Python', 'FastAPI', 'SQLite', 'VK API', 'requests'],
        'skislyakow/devman-bot': ['Python', 'Telegram', 'requests', 'python-dotenv'],
        'skislyakow/dossier': ['Python', 'Django', 'Nginx', 'Gunicorn', 'GitHub Actions'],
        'skislyakow/online_library': ['Python', 'Jinja2', 'Bootstrap', 'GitHub Pages'],
    }

    def test_seed_0013_filter_tags_and_tags_by_repo(self):
        from django.apps import apps
        module = import_module('main.migrations.0013_skill_filter_tag')
        module.seed(apps, None)
        module.seed(apps, None)
        self.assertEqual(Skill.objects.get(name='Telegram Bot API').filter_tag, 'Telegram')
        self.assertEqual(Skill.objects.get(name='vk_api').filter_tag, 'VK')
        self.assertEqual(Skill.objects.get(name='VK API').filter_tag, 'VK')
        self.assertEqual(Skill.objects.get(name='systemd').filter_tag, '')
        for repo, tags in self.TAGS_BY_REPO.items():
            project = Project.objects.create(title=repo, repo=repo)
            self.assertEqual(project.tags, [])
        module.seed(apps, None)
        for repo, tags in self.TAGS_BY_REPO.items():
            self.assertEqual(Project.objects.get(repo=repo).tags, tags)

