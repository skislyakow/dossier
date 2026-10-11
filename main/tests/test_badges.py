import json

from django.test import TestCase

from main import badge_utils
from main.widgets import BadgePickerWidget


class BadgeSourceRegistryTest(TestCase):
    def test_catalog_covers_every_source(self):
        by_group = {g: [b['source'] for b in items] for g, items in badge_utils.catalog().items()}
        self.assertEqual(set(badge_utils.BADGE_SOURCES), set(by_group['github'] + by_group['pypi']))
        self.assertEqual(len(badge_utils.BADGE_SOURCES), 13)

    def test_every_source_resolves_against_data(self):
        ctx = {
            'repo': {
                'stargazers_count': 42,
                'forks_count': 3,
                'open_issues_count': 1,
                'license': {'spdx_id': 'MIT'},
                'language': 'Python',
                'size': 2048,
                'created_at': '2020-01-01T00:00:00Z',
                'pushed_at': '2021-02-03T00:00:00Z',
            },
            'pypi': {'info': {'version': '1.2.3', 'requires_python': '>=3.8', 'license': 'MIT'}},
            'stats': {'data': {'last_month': 500, 'total': 6000}},
        }
        for source in badge_utils.BADGE_SOURCES:
            badge = {'label': 'x', 'source': source}
            self.assertIsNotNone(badge_utils.resolve_badge(badge, ctx), source)

    def test_every_source_degrades_without_data(self):
        for source in badge_utils.BADGE_SOURCES:
            badge = {'label': 'x', 'source': source}
            self.assertIsNone(badge_utils.resolve_badge(badge, {}), source)

    def test_unknown_source_degrades(self):
        self.assertIsNone(badge_utils.resolve_badge({'label': 'x', 'source': 'no_such_source'}, {}))

    def test_resolver_formatting(self):
        self.assertEqual(
            badge_utils.resolve_badge({'label': 's', 'source': 'github_size'}, {'repo': {'size': 2048}})['value'],
            '2.0 MB',
        )
        self.assertEqual(
            badge_utils.resolve_badge({'label': 's', 'source': 'github_size'}, {'repo': {'size': 512}})['value'],
            '512 KB',
        )
        self.assertEqual(
            badge_utils.resolve_badge({'label': 'd', 'source': 'pypistats_total'}, {'stats': {'data': {'total': 1500000}}})['value'],
            '1.5m',
        )

    def test_custom_badge_without_source(self):
        self.assertEqual(
            badge_utils.resolve_badge({'label': 'note', 'value': 'static'}, {}),
            {'label': 'note', 'value': 'static'},
        )
        self.assertEqual(badge_utils.resolve_badge({'label': 'label-only'}, {}), {'label': 'label-only'})


class BadgePickerWidgetTest(TestCase):
    def test_widget_catalog_derives_from_registry(self):
        html = BadgePickerWidget().render('badges_config', [], attrs={'id': 'id_badges'})
        self.assertIn('data-bp-catalog=', html)
        payload = html.split("data-bp-catalog='")[1].split("'")[0]
        data = json.loads(payload)
        self.assertEqual(
            {b['source'] for b in data['github'] + data['pypi']},
            set(badge_utils.BADGE_SOURCES),
        )

    def test_value_from_datadict_parses_json_array(self):
        value = BadgePickerWidget().value_from_datadict(
            {'badges_config': '[{"source": "github_stars"}, {"source": "pypi_version"}]'},
            None, 'badges_config',
        )
        self.assertEqual(value, [{'source': 'github_stars'}, {'source': 'pypi_version'}])

    def test_value_from_datadict_invalid_or_missing_falls_back(self):
        widget = BadgePickerWidget()
        self.assertEqual(widget.value_from_datadict({'b': 'not json'}, None, 'b'), [])
        self.assertEqual(widget.value_from_datadict({}, None, 'b'), [])