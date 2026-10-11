#!/usr/bin/env bash
# Smoke-проверка витрины без браузера: curl + python3 (stdlib), новых зависимостей не нужно.
# Использование:
#   ./tools/smoke.sh                # локальный dev-сервер (http://127.0.0.1:8000), должен быть запущен
#   ./tools/smoke.sh https://kislyakov.pro
set -u

BASE="${1:-http://127.0.0.1:8000}"
FAILS=0
PASSES=0

say() { printf '%s\n' "$*"; }
fail() { say "FAIL  $*"; FAILS=$((FAILS + 1)); }
pass() { say "PASS  $*"; PASSES=$((PASSES + 1)); }

get() { # get <url> -> body; статус проверяет curl (на стд.ошибку)
    curl -fsS --max-time 15 "$BASE/$1" 2>/dev/null
}

# --- HTML главной ---
HTML="$(get '')" || { fail "GET / -> curl error (сервер запущен?"; say "      BASE=$BASE)"; }
if [ -n "${HTML:-}" ]; then
    if printf '%s' "$HTML" | grep -q 'id="skills"'; then pass "/ содержит #skills"; else fail "/ без #skills"; fi
    if printf '%s' "$HTML" | grep -q 'id="portfolio"'; then pass "/ содержит #portfolio"; else fail "/ без #portfolio"; fi
    if printf '%s' "$HTML" | grep -q 'data-theme'; then pass "/ содержит data-theme"; else fail "/ без data-theme"; fi
fi

# --- Статика ---
for asset in static/css/style.css static/css/fonts.css static/js/util.js static/js/portfolio.js static/js/github.js static/js/timeline.js static/favicon.svg static/og/og-image.png; do
    if curl -fsS --max-time 15 -o /dev/null "$BASE/$asset" 2>/dev/null; then pass "$asset 200"; else fail "$asset"; fi
done
case "$BASE" in
    *127.0.0.1*|*localhost*)
        case "$BASE" in *insecure*) ;; *) HINT=yes ;; esac ;;
esac
if [ "${HINT:-}" = yes ]; then
    say "      подсказка: локально DEBUG=False — статику раздаёт только 'uv run manage.py runserver --insecure'"
fi

# --- JSON-контракты API ---
SKILLS="$(get 'api/skills/')" || { fail "GET /api/skills/"; SKILLS=""; }
PROJECTS="$(get 'api/projects/')" || { fail "GET /api/projects/"; PROJECTS=""; }
TIMELINE="$(get 'api/timeline/')" || { fail "GET /api/timeline/"; TIMELINE=""; }
CONTACT="$(get 'api/contact/')" || { fail "GET /api/contact/"; CONTACT=""; }
GITHUB="$(get 'api/github/')" || { fail "GET /api/github/"; GITHUB=""; }
TAGS="$(get 'api/tags/')" || { fail "GET /api/tags/"; TAGS=""; }

PYOUT="$(python3 - "$SKILLS" "$PROJECTS" "$TIMELINE" "$CONTACT" "$GITHUB" "$TAGS" <<'PY'
import json, sys

passes = fails = 0

def check(cond, label):
    global passes, fails
    if cond:
        passes += 1
    else:
        fails += 1
    print(("PASS  " if cond else "FAIL  ") + label)

def load(raw, name):
    try:
        return json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        check(False, f"{name}: не JSON")
        return None

skills = load(sys.argv[1], "/api/skills/")
if isinstance(skills, list) and skills:
    keys = set(skills[0])
    check({"name", "category", "size", "tag"} <= keys, "/api/skills/: ключи name/category/size/tag")
    check(all(s["size"] in ("xl", "lg", "md", "sm") for s in skills), "/api/skills/: size только xl/lg/md/sm")
    check(all(s["category"] in ("backend", "web", "devops", "bots", "tools") for s in skills), "/api/skills/: category из справочника")
elif skills is not None:
    check(False, "/api/skills/: не список")

projects = load(sys.argv[2], "/api/projects/")
if isinstance(projects, list) and projects:
    first = set(projects[0])
    need = {"repo", "title", "role", "tagline", "features", "tags", "links", "badges", "screenshot", "langs", "stars"}
    check(need <= first, "/api/projects/: ключи карточки присутствуют")
elif projects is not None:
    check(False, "/api/projects/: не список")

timeline = load(sys.argv[3], "/api/timeline/")
if isinstance(timeline, dict):
    check({"prior", "job", "present", "timeline"} <= set(timeline), "/api/timeline/: ключи prior/job/present/timeline")

contact = load(sys.argv[4], "/api/contact/")
if isinstance(contact, list) and contact:
    check(all({"type", "label", "value"} <= set(c) for c in contact), "/api/contact/: ключи type/label/value")
    check(any(c["type"] == "github" for c in contact), "/api/contact/: есть github")

github = load(sys.argv[5], "/api/github/")
if isinstance(github, dict):
    check({"user", "langs"} <= set(github), "/api/github/: ключи user/langs")

tags = load(sys.argv[6], "/api/tags/")
if isinstance(tags, list) and tags:
    check(all({"name", "count", "size"} <= set(t) for t in tags), "/api/tags/: ключи name/count/size")
    check(all(t["size"] in ("xl", "lg", "md", "sm") for t in tags), "/api/tags/: size только xl/lg/md/sm")
elif tags is not None:
    check(False, "/api/tags/: не список")

print(f"# counts: {passes} {fails}")
PY
)"
printf '%s\n' "$PYOUT" | sed '/^# counts:/d'
COUNTS="$(printf '%s\n' "$PYOUT" | sed -n 's/^# counts: //p')"
COUNTS="${COUNTS:-0 0}"
PASSES=$((PASSES + ${COUNTS%% *}))
FAILS=$((FAILS + ${COUNTS##* }))

say ""
say "Итого: $PASSES ок, $FAILS ошибок (BASE=$BASE)"
[ "$FAILS" -eq 0 ]
