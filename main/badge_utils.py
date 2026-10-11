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


def _ctx_get(ctx, key):
    return ctx.get(key) or {}


def _resolve_stars(ctx):
    v = _ctx_get(ctx, "repo").get("stargazers_count")
    return str(v) if v is not None else None


def _resolve_forks(ctx):
    v = _ctx_get(ctx, "repo").get("forks_count")
    return str(v) if v is not None else None


def _resolve_issues(ctx):
    v = _ctx_get(ctx, "repo").get("open_issues_count")
    return str(v) if v is not None else None


def _resolve_license(ctx):
    return (_ctx_get(ctx, "repo").get("license") or {}).get("spdx_id")


def _resolve_lang(ctx):
    return _ctx_get(ctx, "repo").get("language")


def _resolve_size(ctx):
    v = _ctx_get(ctx, "repo").get("size")
    if v is None:
        return None
    return f"{v / 1024:.1f} MB" if v >= 1024 else f"{v} KB"


def _resolve_created(ctx):
    return _format_date(_ctx_get(ctx, "repo").get("created_at"))


def _resolve_updated(ctx):
    return _format_date(_ctx_get(ctx, "repo").get("pushed_at"))


def _resolve_pypi_version(ctx):
    v = (_ctx_get(ctx, "pypi").get("info") or {}).get("version")
    return f"v{v}" if v else None


def _resolve_pypi_python(ctx):
    v = (_ctx_get(ctx, "pypi").get("info") or {}).get("requires_python")
    return _parse_python_versions(v) if v else None


def _resolve_pypi_license(ctx):
    return (_ctx_get(ctx, "pypi").get("info") or {}).get("license")


def _resolve_pypistats_month(ctx):
    v = (_ctx_get(ctx, "stats").get("data") or {}).get("last_month")
    return f"{_format_downloads(v)}/mo" if v is not None else None


def _resolve_pypistats_total(ctx):
    v = (_ctx_get(ctx, "stats").get("data") or {}).get("total")
    return _format_downloads(v)


BADGE_SOURCES = {
    "github_stars": {"label": "stars", "icon": "star", "group": "github", "resolve": _resolve_stars},
    "github_forks": {"label": "forks", "icon": "call_split", "group": "github", "resolve": _resolve_forks},
    "github_issues": {"label": "issues", "icon": "track_changes", "group": "github", "resolve": _resolve_issues},
    "github_license": {"label": "license", "icon": "balance", "group": "github", "resolve": _resolve_license},
    "github_lang": {"label": "language", "icon": "code", "group": "github", "resolve": _resolve_lang},
    "github_size": {"label": "size", "icon": "hard_drive", "group": "github", "resolve": _resolve_size},
    "github_created": {"label": "created", "icon": "calendar_today", "group": "github", "resolve": _resolve_created},
    "github_updated": {"label": "updated", "icon": "update", "group": "github", "resolve": _resolve_updated},
    "pypi_version": {"label": "pypi", "icon": "package_2", "group": "pypi", "resolve": _resolve_pypi_version},
    "pypi_python": {"label": "python", "icon": "terminal", "group": "pypi", "resolve": _resolve_pypi_python},
    "pypi_license": {"label": "license", "icon": "balance", "group": "pypi", "resolve": _resolve_pypi_license},
    "pypistats_month": {"label": "downloads/m", "icon": "download", "group": "pypi", "resolve": _resolve_pypistats_month},
    "pypistats_total": {"label": "downloads total", "icon": "download_done", "group": "pypi", "resolve": _resolve_pypistats_total},
}


def catalog():
    """Каталог бейджей для админки по группам: {'github': [...], 'pypi': [...]}."""
    out = {"github": [], "pypi": []}
    for source, meta in BADGE_SOURCES.items():
        out[meta["group"]].append({"label": meta["label"], "source": source, "icon": meta["icon"]})
    return out


def resolve_badge(badge, ctx):
    if not badge.get("source"):
        if badge.get("value"):
            return {"label": badge.get("label"), "value": badge.get("value")}
        return {"label": badge.get("label")}

    entry = BADGE_SOURCES.get(badge["source"])
    if entry is None:
        return None
    value = entry["resolve"](ctx)
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


def fetch_github_stats(username="skislyakow"):
    key = f"github:stats:{username}"
    cached = cache.get(key)
    if cached is not None:
        return cached

    hdrs = _github_headers()
    user = _get_json(f"https://api.github.com/users/{username}", hdrs)
    repos = _get_json(
        f"https://api.github.com/users/{username}/repos?sort=stars&per_page=6", hdrs
    ) or []

    lang_count = {}
    for repo in repos:
        name = repo.get("name")
        if not name:
            continue
        langs = fetch_repo_data(f"{username}/{name}")["langs"] or {}
        for lang, bytes_ in langs.items():
            lang_count[lang] = lang_count.get(lang, 0) + bytes_

    total = sum(lang_count.values())
    sorted_langs = sorted(lang_count.items(), key=lambda kv: kv[1], reverse=True)[:5]
    langs_out = []
    if total:
        for lang, bytes_ in sorted_langs:
            langs_out.append({"lang": lang, "percent": round(bytes_ / total * 100)})

    if user is None and not repos:
        cache.set(key, {"user": None, "langs": []}, CACHE_FAIL)
        return {"user": None, "langs": []}

    result = {"user": user or {}, "langs": langs_out}
    cache.set(key, result, CACHE_OK)
    return result
