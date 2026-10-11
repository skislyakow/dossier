from django.test import TestCase

from main.models import Project, Skill


class DataConsistencyAuditTest(TestCase):
    def setUp(self):
        Skill.objects.all().delete()
        Project.objects.all().delete()

    def _audit(self):
        from main.audit import audit_content
        return audit_content()

    def test_empty_db_is_clean(self):
        errors, warnings = self._audit()
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

    def test_tag_without_skill_is_error(self):
        Project.objects.create(title='P', repo='user/p', tags=['Glob'])
        errors, _ = self._audit()
        self.assertIn('Glob', errors[0])
        Skill.objects.create(name='Glob')
        errors, _ = self._audit()
        self.assertEqual(errors, [])

    def test_skill_without_matching_tag_warns(self):
        Skill.objects.create(name='Hollow')
        _, warnings = self._audit()
        self.assertIn('Hollow', warnings[0])
        Project.objects.create(title='P', repo='user/p', tags=['Hollow'])
        _, warnings = self._audit()
        self.assertEqual(warnings, [])

    def test_filter_tag_resolves_project_tag(self):
        Skill.objects.create(name='Telegram Bot API', filter_tag='Telegram')
        Project.objects.create(title='P', repo='user/p', tags=['Telegram'])
        errors, warnings = self._audit()
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

    def test_command_exits_1_on_error(self):
        from io import StringIO
        from django.core.management import call_command
        Project.objects.create(title='P', repo='user/p', tags=['Glob'])
        with self.assertRaises(SystemExit) as ctx:
            call_command('audit_content', stdout=StringIO())
        self.assertEqual(ctx.exception.code, 1)

    def test_command_says_ok_when_clean(self):
        from io import StringIO
        from django.core.management import call_command
        Skill.objects.create(name='Glob')
        Project.objects.create(title='P', repo='user/p', tags=['Glob'])
        out = StringIO()
        call_command('audit_content', stdout=out)
        self.assertIn('согласован', out.getvalue())