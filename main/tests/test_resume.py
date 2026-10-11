from pathlib import Path
from unittest import mock

from django.test import TestCase

from main.models import Skill


class ResumePageTest(TestCase):
    def test_resume_page_200_and_content(self):
        from main.models import ResumeProfile
        response = self.client.get('/resume/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, ResumeProfile.load().full_name)
        self.assertContains(response, 'Опыт')
        self.assertContains(response, 'Навыки')
        self.assertContains(response, 'Скачать PDF')

    def test_resume_pdf_download(self):
        from main import resume

        with mock.patch.object(resume, 'build_pdf', return_value=b'%PDF-1.4 fake'):
            path = resume.write_pdf()
        try:
            response = self.client.get('/resume/pdf/')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response['Content-Type'], 'application/pdf')
            self.assertEqual(b''.join(response.streaming_content), b'%PDF-1.4 fake')
        finally:
            Path(path).unlink(missing_ok=True)

    def test_resume_pdf_404_when_missing(self):
        from main import resume

        with mock.patch.object(resume, 'pdf_path', return_value='/nonexistent/resume.pdf'):
            response = self.client.get('/resume/pdf/')
        self.assertEqual(response.status_code, 404)


class ResumeGenerationTest(TestCase):
    def _write_pdf(self):
        from main import resume

        with mock.patch.object(resume, 'build_pdf', return_value=b'%PDF-1.4 mocked'):
            return resume.write_pdf()

    def test_write_pdf_creates_file(self):
        path = self._write_pdf()
        self.assertTrue(Path(path).exists())
        self.assertEqual(Path(path).read_bytes(), b'%PDF-1.4 mocked')
        Path(path).unlink()

    def test_generate_resume_command(self):
        from io import StringIO
        from django.core.management import call_command
        from main import resume

        with mock.patch.object(resume, 'write_pdf', return_value='/tmp/resume.pdf') as m:
            out = StringIO()
            call_command('generate_resume', stdout=out)
        m.assert_called_once()
        self.assertIn('Резюме записано', out.getvalue())

    def test_signal_regenerates_on_save_when_enabled(self):
        import os
        from main import resume

        os.environ['RESUME_AUTOGEN'] = '1'
        try:
            with mock.patch.object(resume, 'write_pdf') as m:
                Skill.objects.create(name='SignalSkill', category='tools')
            m.assert_called_once()
        finally:
            del os.environ['RESUME_AUTOGEN']

    def test_signal_disabled_under_pytest(self):
        from main import signals
        self.assertFalse(signals._autogen_enabled())