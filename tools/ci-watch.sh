#!/usr/bin/env bash
# Поллинг GitHub Actions для конкретного коммита. Токен берётся из git credential
# store (host=github.com). Ограниченное число попыток + видимый прогресс, чтобы
# ожидание не выглядело зависанием.
#   ./tools/ci-watch.sh <short-sha> [repo]
# exit 0 = success, 1 = failure, 2 = таймаут.
set -euo pipefail

SHA="${1:?usage: ci-watch.sh <short-sha> [repo]}"
REPO="${2:-skislyakow/dossier}"
MAX_TRIES="${CI_WATCH_TRIES:-40}"
SLEEP="${CI_WATCH_SLEEP:-15}"

TOKEN="$(printf 'protocol=https\nhost=github.com\n\n' | git credential fill 2>/dev/null | sed -n 's/^password=//p')"
if [ -z "$TOKEN" ]; then
    echo "не удалось получить GitHub-токен из git credential store" >&2
    exit 2
fi

for i in $(seq 1 "$MAX_TRIES"); do
    ROW="$(curl -fsS -H "Authorization: Bearer $TOKEN" \
        "https://api.github.com/repos/$REPO/actions/runs?per_page=10" \
        | python3 -c "
import json, sys
sha = '$SHA'
for r in json.load(sys.stdin).get('workflow_runs', []):
    if r['head_sha'].startswith(sha):
        print(r['status'], r.get('conclusion') or '...', r['head_sha'][:7])
        break
")"
    echo "[$i/$MAX_TRIES] ${ROW:-нет запуска для $SHA}"
    case "$ROW" in
        completed\ success*) exit 0 ;;
        completed\ *) exit 1 ;;
    esac
    if [ "$i" -lt "$MAX_TRIES" ]; then sleep "$SLEEP"; fi
done

echo "таймаут: $SHA не завершился за $MAX_TRIES попыток" >&2
exit 2
