from django.test import TestCase, Client
from django.urls import reverse


class HomeViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_status_200(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'index.html')

    def test_contains_keywords(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'Sergey Kislyakov')
        self.assertContains(response, 'terminal')
        self.assertContains(response, 'Python')
        self.assertContains(response, 'Django')
