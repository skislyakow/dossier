from django.test import TestCase

from main.models import Project, Skill


class MigrationSkillFilterTagSeedTest(TestCase):
    TAGS_BY_REPO = {
        'skislyakow/opencode-py': ['Python', 'httpx', 'Pydantic', 'PyPI', 'opencode-py'],
        'skislyakow/ferma': ['Python', 'FastAPI', 'SQLite', 'VK API', 'requests'],
        'skislyakow/devman-bot': ['Python', 'Telegram', 'requests', 'python-dotenv'],
        'skislyakow/dossier': ['Python', 'Django', 'Nginx', 'Gunicorn', 'GitHub Actions', 'HTML', 'CSS', 'JavaScript', 'pytest', 'mypy'],
        'skislyakow/online_library': ['Python', 'Jinja2', 'Bootstrap', 'GitHub Pages'],
        'skislyakow/FishShop': ['Python', 'Telegram', 'python-telegram-bot', 'requests', 'Redis', 'Strapi'],
    }
    SKILL_FILTER_TAGS = {
        'Telegram Bot API': 'Telegram',
        'vk_api': 'VK',
        'VK API': 'VK',
        'systemd': '',
    }

    def test_migrated_seed_filter_tags_and_project_tags(self):
        for name, filter_tag in self.SKILL_FILTER_TAGS.items():
            self.assertEqual(Skill.objects.get(name=name).filter_tag, filter_tag)
        for repo, tags in self.TAGS_BY_REPO.items():
            self.assertEqual(Project.objects.get(repo=repo).tags, tags)

    def test_fishshop_skills_categories(self):
        self.assertEqual(Skill.objects.get(name='python-telegram-bot').category, 'bots')
        self.assertEqual(Skill.objects.get(name='Strapi').category, 'backend')

    def test_admin_skills_categories(self):
        # 0028: навыки, заведённые на проде через admin, — категории зеркалят прод
        for name, category in {
            'Docker': 'devops',
            'Git': 'devops',
            'Ubuntu': 'devops',
            'REST API': 'backend',
            'asyncio': 'backend',
        }.items():
            self.assertEqual(Skill.objects.get(name=name).category, category)