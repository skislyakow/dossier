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


class AskStreamViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_missing_q_returns_400(self):
        response = self.client.get(reverse('ask_stream'))
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {'error': 'No question'})

    def test_empty_q_returns_400(self):
        response = self.client.get(reverse('ask_stream'), {'q': ''})
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {'error': 'No question'})

    def test_streaming_content_type(self):
        response = self.client.get(reverse('ask_stream'), {'q': 'hello'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/event-stream')
        self.assertEqual(response['Cache-Control'], 'no-cache')
