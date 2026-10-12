from django.test import TestCase

from main.models import Project, Skill


class MigrationSkillFilterTagSeedTest(TestCase):
    TAGS_BY_REPO = {
        'skislyakow/opencode-py': ['Python', 'httpx', 'Pydantic', 'PyPI', 'opencode-py'],
        'skislyakow/ferma': ['Python', 'FastAPI', 'SQLite', 'VK API', 'requests'],
        'skislyakow/devman-bot': ['Python', 'Telegram', 'requests', 'python-dotenv'],
        'skislyakow/dossier': ['Python', 'Django', 'Nginx', 'Gunicorn', 'GitHub Actions', 'HTML', 'CSS', 'JavaScript', 'pytest', 'mypy'],
        'skislyakow/online_library': ['Python', 'Jinja2', 'Bootstrap', 'GitHub Pages'],
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