from importlib import import_module

from django.test import TestCase

from main.models import Project, Skill


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