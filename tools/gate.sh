#!/usr/bin/env bash
# Локальный чек-гейт — тот же набор проверок, что в CI (.github/workflows/deploy.yml).
# Запускать ПЕРЕД коммитом/пушем; exit 0 = всё зелёное.
#   ./tools/gate.sh
# fail-fast: set -euo pipefail, чтобы падение любой проверки роняло весь гейт.
set -euo pipefail
cd "$(dirname "$0")/.."

echo "== ruff =="
uv run ruff check .

echo "== mypy =="
uv run mypy main/

echo "== pytest =="
uv run pytest

echo "== makemigrations --check =="
uv run manage.py makemigrations --check --dry-run

echo "== node --check static/js/*.js =="
for f in static/js/*.js; do
    node --check "$f"
done

echo "GATE_OK"
