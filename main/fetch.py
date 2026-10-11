"""Единый кэшированный fetch-адаптер для внешних API.

Одна политика TTL на всё приложение: успех — `CACHE_OK` (6ч), сбой —
`CACHE_FAIL` (5мин). Транспорт инжектится (`transport` + `mock.patch.object` в
тестах): по умолчанию `UrllibTransport` (stdlib, без зависимостей), для тестов
и локальной разработки без сети — `MemoryTransport`. Преобразования данных —
чистые функции без сети (`aggregate_languages`).
"""

import json
import os
import urllib.request

from django.core.cache import cache

HTTP_TIMEOUT = 8
CACHE_OK = 21600       # 6 hours
CACHE_FAIL = 300       # 5 minutes on upstream failure

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

_MISS = object()


def _github_headers():
    headers = {"User-Agent": "dossier/1.0", "Accept": "application/vnd.github+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"
    return headers


class UrllibTransport:
    """GET → JSON (или None при любой ошибке)."""

    def __init__(self, timeout=HTTP_TIMEOUT):
        self.timeout = timeout

    def get(self, url, headers=None):
        req_headers = {"User-Agent": "dossier/1.0"}
        if headers:
            req_headers.update(headers)
        try:
            req = urllib.request.Request(url, headers=req_headers)
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception:
            return None


class MemoryTransport:
    """In-memory транспорт: тесты и локальная разработка без сети.

    Заполняется словарём url → json (чего нет — то None, как сбой).
    Записывает вызовы в `calls` (url) и `headers_by_call` (headers).
    """

    def __init__(self, urls=None):
        self.urls = dict(urls or {})
        self.calls = []
        self.headers_by_call = []

    def get(self, url, headers=None):
        self.calls.append(url)
        self.headers_by_call.append(headers)
        return self.urls.get(url)


transport = UrllibTransport()


def fetch(url, headers=None):
    """Кэшированный GET → JSON. Успех держится `CACHE_OK`, сбой — `CACHE_FAIL`."""
    key = f"fetch:{url}"
    cached = cache.get(key, _MISS)
    if cached is not _MISS:
        return cached
    data = transport.get(url, headers)
    cache.set(key, data, CACHE_OK if data is not None else CACHE_FAIL)
    return data


def aggregate_languages(repos):
    """Чистая трансформация: repo-langs ({name, langs}) → топ-5 {lang, percent}."""
    counts = {}
    for repo in repos or []:
        for lang, bytes_ in (repo.get("langs") or {}).items():
            counts[lang] = counts.get(lang, 0) + bytes_
    total = sum(counts.values())
    if not total:
        return []
    top = sorted(counts.items(), key=lambda kv: kv[1], reverse=True)[:5]
    return [{"lang": lang, "percent": round(bytes_ / total * 100)} for lang, bytes_ in top]


def fetch_repo_data(repo):
    if not repo or "/" not in repo:
        return {"repo": {}, "langs": {}}
    key = f"github:repo:{repo}"
    cached = cache.get(key, _MISS)
    if cached is not _MISS:
        return cached

    hdrs = _github_headers()
    repo_json = fetch(f"https://api.github.com/repos/{repo}", hdrs)
    langs = fetch(f"https://api.github.com/repos/{repo}/languages", hdrs)

    if repo_json is None and langs is None:
        result = {"repo": {}, "langs": {}}
        cache.set(key, result, CACHE_FAIL)
        return result

    result = {"repo": repo_json or {}, "langs": langs or {}}
    cache.set(key, result, CACHE_OK)
    return result


def fetch_pypi_data(pypi):
    key = f"pypi:{pypi}"
    cached = cache.get(key, _MISS)
    if cached is not _MISS:
        return cached

    ua = {"User-Agent": "dossier/1.0"}
    pypi_json = fetch(f"https://pypi.org/pypi/{pypi}/json", ua)
    stats = fetch(f"https://pypistats.org/api/packages/{pypi}/recent", ua)

    if pypi_json is None and stats is None:
        result = {"pypi": None, "stats": None}
        cache.set(key, result, CACHE_FAIL)
        return result

    result = {"pypi": pypi_json, "stats": stats}
    cache.set(key, result, CACHE_OK)
    return result


def fetch_github_stats(username="skislyakow"):
    key = f"github:stats:{username}"
    cached = cache.get(key, _MISS)
    if cached is not _MISS:
        return cached

    hdrs = _github_headers()
    user = fetch(f"https://api.github.com/users/{username}", hdrs)
    repos = fetch(
        f"https://api.github.com/users/{username}/repos?sort=stars&per_page=6", hdrs
    ) or []

    with_langs = []
    for repo in repos:
        name = repo.get("name")
        if not name:
            continue
        langs = fetch_repo_data(f"{username}/{name}")["langs"] or {}
        with_langs.append({"name": name, "langs": langs})

    langs = aggregate_languages(with_langs)

    if user is None and not repos:
        cache.set(key, {"user": None, "langs": []}, CACHE_FAIL)
        return {"user": None, "langs": []}

    result = {"user": user or {}, "langs": langs}
    cache.set(key, result, CACHE_OK)
    return result