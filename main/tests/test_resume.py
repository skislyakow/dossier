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

    def test_signal_env_zero_disables_autogen(self):
        import os
        from main import signals

        os.environ['RESUME_AUTOGEN'] = '0'
        try:
            self.assertFalse(signals._autogen_enabled())
        finally:
            del os.environ['RESUME_AUTOGEN']

    def test_signal_env_one_still_enables_autogen(self):
        import os
        from main import signals

        os.environ['RESUME_AUTOGEN'] = '1'
        try:
            self.assertTrue(signals._autogen_enabled())
        finally:
            del os.environ['RESUME_AUTOGEN']


class ResumeOrderingTest(TestCase):
    def test_experience_newest_first_then_undated_by_sort_order(self):
        from datetime import date

        from main.models import TimelineItem
        from main import resume

        TimelineItem.objects.create(
            item_type='job', title='older', date_label='x',
            start_date=date(2020, 1, 1), sort_order=1,
        )
        TimelineItem.objects.create(
            item_type='job', title='newer', date_label='x',
            start_date=date(2024, 1, 1), sort_order=2,
        )
        TimelineItem.objects.create(
            item_type='present', title='undated-2', date_label='x', sort_order=30,
        )
        TimelineItem.objects.create(
            item_type='present', title='undated-1', date_label='x', sort_order=10,
        )

        titles = [i.title for i in resume.context()['experience']]
        self.assertLess(titles.index('newer'), titles.index('older'))
        self.assertLess(titles.index('older'), titles.index('undated-1'))
        self.assertLess(titles.index('undated-1'), titles.index('undated-2'))

    def test_key_tiebreak_falls_back_to_ascending_sort_order(self):
        from datetime import date

        from main.models import TimelineItem
        from main.resume import _resume_sort_key

        a = TimelineItem(item_type='job', title='a', date_label='x',
                         start_date=date(2023, 1, 1), sort_order=7)
        b = TimelineItem(item_type='job', title='b', date_label='x',
                         start_date=date(2023, 1, 1), sort_order=2)
        self.assertLess(_resume_sort_key(b), _resume_sort_key(a))