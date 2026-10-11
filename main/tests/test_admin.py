import json

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from main.models import Skill


class AdminReorderTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='admin', password='x')
        self.user.is_staff = True
        self.user.save()
        self.client.force_login(self.user)

    def _post(self, url, body):
        return self.client.post(url, data=json.dumps(body), content_type='application/json')

    def test_requires_staff(self):
        response = self.client_class().post(reverse('admin:main_skill_reorder'))
        self.assertEqual(response.status_code, 302)

    def test_requires_post(self):
        response = self.client.get(reverse('admin:main_skill_reorder'))
        self.assertEqual(response.status_code, 405)

    def test_unknown_model_400(self):
        from django.test import RequestFactory
        from main.admin_views import admin_reorder
        request = RequestFactory().post(
            '/admin/main/nope/reorder/',
            data=json.dumps({'items': []}),
            content_type='application/json',
        )
        request.user = self.user
        response = admin_reorder(request, 'nope')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), {'error': 'Unknown model'})

    def test_invalid_json_400(self):
        url = reverse('admin:main_skill_reorder')
        response = self.client.post(url, data='not json', content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'error': 'Invalid JSON'})

    def test_items_not_list_400(self):
        response = self._post(reverse('admin:main_skill_reorder'), {'items': 'x'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'error': 'items must be a list'})

    def test_reorders_by_list_index(self):
        s1 = Skill.objects.create(name='a', sort_order=0)
        s2 = Skill.objects.create(name='b', sort_order=1)
        s3 = Skill.objects.create(name='c', sort_order=2)
        response = self._post(
            reverse('admin:main_skill_reorder'),
            {'items': [s3.pk, s1.pk, s2.pk]},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'ok': True, 'count': 3})
        self.assertEqual(Skill.objects.get(pk=s3.pk).sort_order, 0)
        self.assertEqual(Skill.objects.get(pk=s1.pk).sort_order, 1)
        self.assertEqual(Skill.objects.get(pk=s2.pk).sort_order, 2)