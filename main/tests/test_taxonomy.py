from django.test import TestCase

from main import taxonomy
from main.models import Project, Skill


class SkillSizeTest(TestCase):
    def test_buckets(self):
        expected = [(0, 'sm'), (1, 'md'), (2, 'md'), (3, 'lg'), (4, 'lg'), (5, 'xl'), (99, 'xl')]
        for count, size in expected:
            self.assertEqual(taxonomy.skill_size(count), size)

    def test_size_belongs_to_known_vocabulary(self):
        for count in (0, 1, 2, 3, 4, 5, 10):
            self.assertIn(taxonomy.skill_size(count), taxonomy.SKILL_SIZES)


class ResolveTagTest(TestCase):
    def test_falls_back_to_name(self):
        self.assertEqual(taxonomy.resolve_tag(Skill(name='Django', filter_tag='')), 'Django')
        self.assertEqual(taxonomy.resolve_tag(Skill(name='Telegram Bot API', filter_tag='Telegram')), 'Telegram')


class TagCloudTest(TestCase):
    def setUp(self):
        Project.objects.all().delete()

    def test_counts_and_sorts_published(self):
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