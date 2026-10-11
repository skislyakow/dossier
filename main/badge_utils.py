import re
import datetime

from .fetch import fetch_pypi_data, fetch_repo_data


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
