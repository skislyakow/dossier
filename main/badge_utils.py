import os
import re
import json
import datetime

import urllib.request
import urllib.error

from django.core.cache import cache

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
HTTP_TIMEOUT = 8

CACHE_OK = 21600       # 6 hours
CACHE_FAIL = 300       # 5 minutes on upstream failure


def _get_json(url, headers=None, timeout=HTTP_TIMEOUT):
    req_headers = {"User-Agent": "dossier/1.0"}
    if headers:
        req_headers.update(headers)
    try:
        req = urllib.request.Request(url, headers=req_headers)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception:
        return None


def _github_headers():
    headers = {"User-Agent": "dossier/1.0", "Accept": "application/vnd.github+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"
    return headers


def fetch_repo_data(repo):
    if not repo or "/" not in repo:
        return {"repo": {}, "langs": {}}
    key = f"github:repo:{repo}"
    cached = cache.get(key)
    if cached is not None:
        return cached

    hdrs = _github_headers()
    repo_json = _get_json(f"https://api.github.com/repos/{repo}", hdrs)
    langs = _get_json(f"https://api.github.com/repos/{repo}/languages", hdrs)

    if repo_json is None and langs is None:
        cache.set(key, {"repo": {}, "langs": {}}, CACHE_FAIL)
        return {"repo": {}, "langs": {}}

    result = {"repo": repo_json or {}, "langs": langs or {}}
    cache.set(key, result, CACHE_OK)
    return result


def fetch_pypi_data(pypi):
    key = f"pypi:{pypi}"
    cached = cache.get(key)
    if cached is not None:
        return cached

    pypi_json = _get_json(f"https://pypi.org/pypi/{pypi}/json", {"User-Agent": "dossier/1.0"})
    stats = _get_json(f"https://pypistats.org/api/packages/{pypi}/recent", {"User-Agent": "dossier/1.0"})

    if pypi_json is None and stats is None:
        cache.set(key, {"pypi": None, "stats": None}, CACHE_FAIL)
        return {"pypi": None, "stats": None}

    result = {"pypi": pypi_json, "stats": stats}
    cache.set(key, result, CACHE_OK)
    return result


def _parse_python_versions(requires_python):
    if not requires_python:
        return ""
    matches = re.findall(r"[\d.]+", requires_python)
    return " | ".join(matches) if matches else requires_python


def _format_downloads(count):
    if count is None or count < 0:
        return None
    if count >= 1000000:
        return f"{count / 1000000:.1f}m"
    if count >= 1000:
        return f"{count / 1000:.1f}k"
    return str(count)


def _format_date(iso):
    if not iso:
        return None
    try:
        dt = datetime.datetime.fromisoformat(iso.replace("Z", "+00:00"))
        return dt.strftime("%d.%m.%Y")
    except Exception:
        return None


def resolve_badge(badge, ctx):
    if not badge.get("source"):
        if badge.get("value"):
            return {"label": badge.get("label"), "value": badge.get("value")}
        return {"label": badge.get("label")}

    source = badge["source"]
    repo = ctx.get("repo") or {}
    pypi = ctx.get("pypi") or {}
    stats = ctx.get("stats") or {}
    value = None

    if source == "github_stars":
        v = repo.get("stargazers_count")
        value = str(v) if v is not None else None
    elif source == "github_forks":
        v = repo.get("forks_count")
        value = str(v) if v is not None else None
    elif source == "github_license":
        value = (repo.get("license") or {}).get("spdx_id")
    elif source == "github_lang":
        value = repo.get("language")
    elif source == "github_issues":
        v = repo.get("open_issues_count")
        value = str(v) if v is not None else None
    elif source == "github_size":
        v = repo.get("size")
        if v is not None:
            value = f"{v / 1024:.1f} MB" if v >= 1024 else f"{v} KB"
    elif source == "github_created":
        value = _format_date(repo.get("created_at"))
    elif source == "github_updated":
        value = _format_date(repo.get("pushed_at"))
    elif source == "pypi_version":
        v = (pypi.get("info") or {}).get("version")
        value = f"v{v}" if v else None
    elif source == "pypi_python":
        v = (pypi.get("info") or {}).get("requires_python")
        value = _parse_python_versions(v) if v else None
    elif source == "pypi_license":
        value = (pypi.get("info") or {}).get("license")
    elif source == "pypistats_month":
        v = (stats.get("data") or {}).get("last_month")
        value = f"{_format_downloads(v)}/mo" if v is not None else None
    elif source == "pypistats_total":
        v = (stats.get("data") or {}).get("total")
        value = _format_downloads(v)

    if value is None:
        return None
    return {"label": badge.get("label"), "value": str(value)}


def resolve_badges(badges_config, ctx):
    out = []
    for b in badges_config or []:
        rb = resolve_badge(b, ctx)
        if rb:
            out.append(rb)
    return out


def enrich_project(project):
    repo_str = project.repo
    rd = fetch_repo_data(repo_str)
    repo_obj = dict(rd["repo"] or {})
    langs = rd["langs"] or {}

    if not repo_obj.get("html_url") and repo_str:
        repo_obj["html_url"] = f"https://github.com/{repo_str}"
    if not repo_obj.get("full_name"):
        repo_obj["full_name"] = repo_str

    pypi_str = project.pypi
    pd = fetch_pypi_data(pypi_str) if pypi_str else {"pypi": None, "stats": None}
    ctx = {"repo": repo_obj, "langs": langs, "pypi": pd["pypi"], "stats": pd["stats"]}

    badges = resolve_badges(project.badges_config, ctx)
    stars = repo_obj.get("stargazers_count") or 0
    return {"repo": repo_obj, "langs": langs, "stars": stars, "badges": badges}
