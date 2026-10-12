from html.parser import HTMLParser
from pathlib import Path

from django.test import TestCase
from django.urls import reverse


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


class DesignSystemTest(TestCase):
    ROOT = Path(__file__).resolve().parents[2]
    CSS_PATH = ROOT / 'static' / 'css' / 'style.css'
    JS_DIR = ROOT / 'static' / 'js'
    JS_PATH = JS_DIR / 'timeline.js'
    PORTFOLIO_JS_PATH = JS_DIR / 'portfolio.js'
    UTIL_JS_PATH = JS_DIR / 'util.js'
    FILTER_STATE_JS_PATH = JS_DIR / 'filter-state.js'
    PAGE_CHROME_JS_PATH = JS_DIR / 'page-chrome.js'
    SKILLS_JS_PATH = JS_DIR / 'skills.js'
    CONTACT_JS_PATH = JS_DIR / 'contact.js'
    GITHUB_JS_PATH = JS_DIR / 'github.js'

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
        chrome = self.PAGE_CHROME_JS_PATH.read_text(encoding='utf-8')
        self.assertIn('IntersectionObserver', chrome)
        self.assertIn('revealObserveAll', chrome)

    def test_reduced_motion_guards(self):
        self.assertIn('prefers-reduced-motion', self.css)
        chrome = self.PAGE_CHROME_JS_PATH.read_text(encoding='utf-8')
        self.assertIn('prefersReducedMotion()', chrome)
        self.assertNotIn('prefers-reduced-motion', self.html)

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

    def test_shared_esc_defined_once_and_loaded_first(self):
        util = self.UTIL_JS_PATH.read_text(encoding='utf-8')
        self.assertIn('function esc(', util)
        self.assertIn('function prefersReducedMotion(', util)
        self.assertIn('prefers-reduced-motion', util)
        for path in sorted(self.UTIL_JS_PATH.parent.glob('*.js')):
            if path == self.UTIL_JS_PATH:
                continue
            source = path.read_text(encoding='utf-8')
            self.assertNotIn('function esc(', source, f'{path.name} повторно определяет esc()')
            self.assertNotIn(
                'function prefersReducedMotion(', source,
                f'{path.name} повторно определяет prefersReducedMotion()',
            )
        for path in (self.PORTFOLIO_JS_PATH, self.JS_PATH):
            self.assertIn('prefersReducedMotion()', path.read_text(encoding='utf-8'))
        self.assertNotIn('tlEsc', self.JS_PATH.read_text(encoding='utf-8'))
        util_pos = self.html.index('js/util.js')
        github_pos = self.html.index('js/github.js')
        self.assertLess(util_pos, github_pos)

    def test_experience_section_chronology_and_escapes(self):
        self.assertIn('id="experience"', self.html)
        self.assertIn('.experience', self.css)
        self.assertIn('.exp-list', self.css)
        self.assertIn('.exp-item', self.css)
        self.assertNotIn('tl-details', self.css)
        js = self.JS_PATH.read_text(encoding='utf-8')
        self.assertIn('esc(', js)
        self.assertNotIn('tlEsc', js)
        self.assertIn('exp-list', js)
        self.assertIn('prefersReducedMotion()', js)
        for raw in ('+ d.title +', '+ d.desc +', '+ d.repo +', '+ d.role +'):
            self.assertNotIn(raw, js)
        self.assertNotIn('timeline-details', js)
        self.assertNotIn('tl-details', js)

    def test_contact_section_three_channels_and_escapes(self):
        js = self.CONTACT_JS_PATH.read_text(encoding='utf-8')
        self.assertIn('id="contact-card"', self.html)
        self.assertIn('js/contact.js', self.html)
        self.assertIn('contact-grid', js)
        self.assertIn('contact-kind', js)
        self.assertIn('contact-value', js)
        self.assertIn('esc(item.label)', js)
        self.assertIn('esc(href)', js)
        self.assertNotIn('channels[item.type]', js)
        self.assertNotIn("href: function(v) { return 'https://github.com/'", js)
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

    def test_panels_are_disclosure_widgets(self):
        util = self.UTIL_JS_PATH.read_text(encoding='utf-8')
        self.assertIn('function disclosurePanel(', util)
        self.assertIn("setAttribute('aria-expanded'", util)
        self.assertIn("setAttribute('aria-controls'", util)
        self.assertIn("e.key !== 'Escape'", util)
        self.assertIn('trigger.focus({ preventScroll: true })', util)
        self.assertIn('aria-controls="stats"', self.html)
        self.assertIn('aria-controls="portfolio"', self.html)
        self.assertIn('aria-controls="contact"', self.html)
        self.assertEqual(self.html.count('aria-expanded="false"'), 3)
        for path in (self.GITHUB_JS_PATH, self.PORTFOLIO_JS_PATH):
            self.assertIn('disclosurePanel(', path.read_text(encoding='utf-8'))
        self.assertNotIn("classList.toggle('hidden')", self.html)

    def test_skills_section_grouped_by_category(self):
        js = self.SKILLS_JS_PATH.read_text(encoding='utf-8')
        self.assertIn('id="skills"', self.html)
        self.assertIn('js/skills.js', self.html)
        self.assertIn('class="skill-group"', js)
        self.assertIn('class="skill-group-title"', js)
        self.assertIn('data.categories', js)
        self.assertIn('esc(cat.label)', js)
        self.assertIn('s.category', js)
        self.assertNotIn('var categories = [', js)

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
        self.assertIn("${esc(t.name)}", js)

    def test_enhanced_card_format_and_escapes(self):
        js = self.PORTFOLIO_JS_PATH.read_text(encoding='utf-8')
        for fragment in ('portfolio-tagline', 'portfolio-features', 'portfolio-badges', 'portfolio-links'):
            self.assertIn(fragment, js)
        self.assertNotIn('function esc(', js)
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
        self.assertIn('prefersReducedMotion()', js)

    def test_portfolio_eager_reveal_without_observer(self):
        js = self.PORTFOLIO_JS_PATH.read_text(encoding='utf-8')
        self.assertIn('window.pageChrome.reveal.now', js)
        self.assertNotIn('function revealNow(', js)
        self.assertNotIn('IntersectionObserver', js)
        chrome = self.PAGE_CHROME_JS_PATH.read_text(encoding='utf-8')
        self.assertIn('function revealNow(', chrome)
        self.assertIn('IntersectionObserver', chrome)

    def test_mobile_hides_preview_media(self):
        css = ' '.join(self.css.split())
        self.assertIn('.portfolio-preview-media { display: none; }', css)
        self.assertIn('.portfolio-preview-content { grid-template-columns: 1fr;', css)

    def test_github_stats_escapes(self):
        js = self.GITHUB_JS_PATH.read_text(encoding='utf-8')
        for raw in ('${user.html_url', '${user.avatar_url', '${user.name', '@${user.login',
                    '${user.bio}</span>', '${lang}', '${percent}'):
            self.assertNotIn(raw, js)
        self.assertIn('${esc(user.', js)
        self.assertIn('${esc(lang)}', js)
        self.assertIn('${esc(percent)}', js)

    def test_og_image_meta_and_file(self):
        self.assertIn('property="og:image" content="https://kislyakov.pro/static/og/og-image.png"', self.html)
        self.assertIn('name="twitter:card" content="summary_large_image"', self.html)
        self.assertIn('name="twitter:image" content="https://kislyakov.pro/static/og/og-image.png"', self.html)
        og_path = self.ROOT / 'static' / 'og' / 'og-image.png'
        self.assertTrue(og_path.is_file(), 'static/og/og-image.png missing')

    def test_skills_are_clickable_filter_buttons(self):
        js = self.SKILLS_JS_PATH.read_text(encoding='utf-8')
        self.assertIn('<button type="button" class="tag tag-', js)
        self.assertIn('data-tag="', js)
        self.assertIn('window.filterState.setTag', js)
        self.assertIn('window.filterState.subscribe', js)
        self.assertIn("fetch('/api/skills/')", js)
        self.assertIn('.skills-cloud .tag {', self.css)
        self.assertIn('cursor: pointer', self.css_rule('.skills-cloud .tag'))
        portfolio_js = self.PORTFOLIO_JS_PATH.read_text(encoding='utf-8')
        self.assertIn('window.filterState', portfolio_js)
        self.assertNotIn('__applyPortfolioTag', js + portfolio_js)
        self.assertNotIn('window.getSkills', js)
        self.assertNotIn('__skillsPromise', js)
        self.assertNotIn('getSkills', self.html)
        self.assertIn('js/skills.js', self.html)
        self.assertIn('.portfolio-empty', self.css)

    def test_filter_state_module_seam(self):
        fs = self.FILTER_STATE_JS_PATH.read_text(encoding='utf-8')
        self.assertIn('window.filterState = { get, setTag, setRole, clear, subscribe };', fs)
        portfolio_js = self.PORTFOLIO_JS_PATH.read_text(encoding='utf-8')
        skills_js = self.SKILLS_JS_PATH.read_text(encoding='utf-8')
        for src in (portfolio_js, skills_js):
            self.assertNotIn('__applyPortfolioTag', src)
            self.assertNotIn('syncSkillButtons', src)
        self.assertNotIn('#skills', portfolio_js)
        self.assertIn('js/filter-state.js', self.html)
        self.assertLess(
            self.html.index('js/util.js'),
            self.html.index('js/filter-state.js'),
        )
        self.assertLess(
            self.html.index('js/filter-state.js'),
            self.html.index('js/portfolio.js'),
        )
        self.assertLess(
            self.html.index('js/filter-state.js'),
            self.html.index('js/skills.js'),
        )

    def test_page_chrome_module(self):
        chrome = self.PAGE_CHROME_JS_PATH.read_text(encoding='utf-8')
        for fragment in (
            'window.pageChrome =',
            'function revealNow(',
            'revealObserveAll',
            'bindGradient',
            "getElementById('theme-toggle')",
            "getElementById('back-to-top')",
        ):
            self.assertIn(fragment, chrome)
        self.assertEqual(self.html.count('<script>'), 0)
        self.assertIn('js/page-chrome.js', self.html)
        self.assertLess(
            self.html.index('js/contact.js'),
            self.html.index('js/page-chrome.js'),
        )
        for path in self.JS_DIR.glob('*.js'):
            if path == self.UTIL_JS_PATH:
                continue
            self.assertNotIn('prefers-reduced-motion', path.read_text(encoding='utf-8'))
        contact = self.CONTACT_JS_PATH.read_text(encoding='utf-8')
        self.assertIn("getElementById('contact-btn')", contact)
        self.assertIn('disclosurePanel(', contact)

    def test_reduced_motion_disables_all_animations(self):
        css = ' '.join(self.css.split())
        self.assertIn('.reveal { opacity: 1; transform: none; transition: none; }', css)
        self.assertIn('.marquee-track { animation: none; }', css)
        self.assertIn('.portfolio-preview-body { transform: none; transition: none; }', css)
        self.assertIn('.hero-text h1 { background-image: none;', css)
        self.assertIn('.hero-blur { backdrop-filter: none;', css)
        self.assertIn('.hero-timeline { transition: none; }', css)