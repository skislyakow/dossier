from unittest import mock

from django.test import TestCase

from main import fetch
from main.fetch import MemoryTransport

GITHUB_REPO = 'https://api.github.com/repos/owner/repo'
GITHUB_LANGS = 'https://api.github.com/repos/owner/repo/languages'


class _RecordingCache:
    """Дубль Django-кэша, запоминающий timeout в set — для проверки TTL."""

    def __init__(self):
        self.mem = {}
        self.ttls = {}

    def get(self, key, default=None):
        return self.mem.get(key, default)

    def set(self, key, value, timeout=None):
        self.mem[key] = value
        self.ttls[key] = timeout


class CachedFetchTest(TestCase):
    def test_ok_cached_6h_and_transport_once(self):
        rc = _RecordingCache()
        with mock.patch.object(fetch, 'cache', rc), mock.patch.object(
            fetch, 'transport', MemoryTransport({GITHUB_REPO: {'ok': True}}),
        ):
            self.assertEqual(fetch.fetch(GITHUB_REPO), {'ok': True})
            self.assertEqual(fetch.fetch(GITHUB_REPO), {'ok': True})
        self.assertEqual(rc.mem['fetch:' + GITHUB_REPO], {'ok': True})
        self.assertEqual(rc.ttls['fetch:' + GITHUB_REPO], fetch.CACHE_OK)

    def test_failure_cached_5min_and_returns_none(self):
        url = 'https://example.test/always-down'
        transport = MemoryTransport({})
        rc = _RecordingCache()
        with mock.patch.object(fetch, 'cache', rc), mock.patch.object(fetch, 'transport', transport):
            self.assertIsNone(fetch.fetch(url))
            self.assertIsNone(fetch.fetch(url))
        self.assertEqual(len(transport.calls), 1)
        self.assertEqual(rc.ttls['fetch:' + url], fetch.CACHE_FAIL)

    def test_github_headers_passed(self):
        transport = MemoryTransport({GITHUB_REPO: {'x': 1}, GITHUB_LANGS: {'Python': 1}})
        with mock.patch.object(fetch, 'cache', _RecordingCache()), mock.patch.object(
            fetch, 'transport', transport,
        ):
            fetch.fetch_repo_data('owner/repo')
        self.assertEqual(transport.headers_by_call[0].get('Accept'), 'application/vnd.github+json')


class AggregateLanguagesTest(TestCase):
    def test_percent_top5(self):
        repos = [
            {'name': 'a', 'langs': {'Python': 200}},
            {'name': 'b', 'langs': {'Python': 100, 'JavaScript': 50}},
        ]
        result = fetch.aggregate_languages(repos)
        by_lang = {lang['lang']: lang['percent'] for lang in result}
        self.assertEqual(by_lang, {'Python': 86, 'JavaScript': 14})

    def test_empty(self):
        self.assertEqual(fetch.aggregate_languages([]), [])
        self.assertEqual(fetch.aggregate_languages([{'name': 'a', 'langs': {}}]), [])


class FetchRepoDataTest(TestCase):
    def test_shape_and_cached_ok(self):
        urls = {GITHUB_REPO: {'stargazers_count': 3}, GITHUB_LANGS: {'Python': 80}}
        rc = _RecordingCache()
        with mock.patch.object(fetch, 'cache', rc), mock.patch.object(fetch, 'transport', MemoryTransport(urls)):
            data = fetch.fetch_repo_data('owner/repo')
        self.assertEqual(data, {'repo': {'stargazers_count': 3}, 'langs': {'Python': 80}})
        self.assertEqual(rc.ttls['github:repo:owner/repo'], fetch.CACHE_OK)

    def test_total_failure_short_ttl(self):
        transport = MemoryTransport({})
        rc = _RecordingCache()
        with mock.patch.object(fetch, 'cache', rc), mock.patch.object(fetch, 'transport', transport):
            self.assertEqual(fetch.fetch_repo_data('owner/gone'), {'repo': {}, 'langs': {}})
            self.assertEqual(fetch.fetch_repo_data('owner/gone'), {'repo': {}, 'langs': {}})
        self.assertEqual(transport.calls, [
            GITHUB_REPO.replace('owner/repo', 'owner/gone'),
            GITHUB_LANGS.replace('owner/repo', 'owner/gone'),
        ])
        self.assertEqual(rc.ttls['github:repo:owner/gone'], fetch.CACHE_FAIL)

    def test_invalid_repo_returns_empty_without_network(self):
        self.assertEqual(fetch.fetch_repo_data('nope'), {'repo': {}, 'langs': {}})
        self.assertEqual(fetch.fetch_repo_data(''), {'repo': {}, 'langs': {}})


class FetchPypiDataTest(TestCase):
    def test_shape_and_cached_ok(self):
        urls = {
            'https://pypi.org/pypi/pkg/json': {'info': {'version': '1.2.3'}},
            'https://pypistats.org/api/packages/pkg/recent': {'data': {'total': 10}},
        }
        rc = _RecordingCache()
        with mock.patch.object(fetch, 'cache', rc), mock.patch.object(fetch, 'transport', MemoryTransport(urls)):
            data = fetch.fetch_pypi_data('pkg')
        self.assertEqual(data['pypi']['info']['version'], '1.2.3')
        self.assertEqual(data['stats']['data']['total'], 10)
        self.assertEqual(rc.ttls['pypi:pkg'], fetch.CACHE_OK)

    def test_total_failure_short_ttl(self):
        transport = MemoryTransport({})
        rc = _RecordingCache()
        with mock.patch.object(fetch, 'cache', rc), mock.patch.object(fetch, 'transport', transport):
            self.assertEqual(fetch.fetch_pypi_data('gone'), {'pypi': None, 'stats': None})
        self.assertEqual(rc.ttls['pypi:gone'], fetch.CACHE_FAIL)


class FetchGithubStatsTest(TestCase):
    def test_aggregates_user_and_langs(self):
        urls = {
            'https://api.github.com/users/skislyakow': {'login': 'skislyakow'},
            'https://api.github.com/users/skislyakow/repos?sort=stars&per_page=6': [
                {'name': 'repo1'}, {'name': 'repo2'},
            ],
            'https://api.github.com/repos/skislyakow/repo1': {'name': 'repo1'},
            'https://api.github.com/repos/skislyakow/repo1/languages': {'Python': 100},
            'https://api.github.com/repos/skislyakow/repo2': {'name': 'repo2'},
            'https://api.github.com/repos/skislyakow/repo2/languages': {'JavaScript': 50},
        }
        rc = _RecordingCache()
        with mock.patch.object(fetch, 'cache', rc), mock.patch.object(fetch, 'transport', MemoryTransport(urls)):
            data = fetch.fetch_github_stats('skislyakow')
            again = fetch.fetch_github_stats('skislyakow')
        self.assertEqual(data['user'], {'login': 'skislyakow'})
        by_lang = {lang['lang']: lang['percent'] for lang in data['langs']}
        self.assertEqual(by_lang, {'Python': 67, 'JavaScript': 33})
        self.assertEqual(again, data)
        self.assertEqual(rc.mem['github:stats:skislyakow'], data)
        self.assertEqual(rc.ttls['github:stats:skislyakow'], fetch.CACHE_OK)

    def test_total_failure_short_ttl(self):
        transport = MemoryTransport({})
        rc = _RecordingCache()
        with mock.patch.object(fetch, 'cache', rc), mock.patch.object(fetch, 'transport', transport):
            self.assertEqual(fetch.fetch_github_stats('nobody'), {'user': None, 'langs': []})
        self.assertEqual(rc.ttls['github:stats:nobody'], fetch.CACHE_FAIL)