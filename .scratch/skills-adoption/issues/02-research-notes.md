# 02: Research-заметки по деплою — docs/research/

**What to build:** Завести конвенцию `docs/research/` и зафиксировать первичные знания, добытые при починке тихого не-задеплоя (2026-10-12), чтобы знание не терялось. Делегируется фоновому агенту (скилл `research`), каждый факт — со ссылкой на первоисточник (офиц. доки / исходники / spec).

**Blocked by:** None.

**Status:** done

## Scope
- `docs/research/weasyprint-ubuntu-2404-deps.md` — точный набор apt-либ для WeasyPrint на Ubuntu 24.04; почему `libpangoft2-1.0-0`, а не `libpangoft2-0`.
- `docs/research/appleboy-ssh-action-script-stop.md` — семантика `script_stop`, как возникал тихий не-задеплой.
- Указатель из AGENTS (Dev workflow / Auto-deploy) и/или README.

## AC
- [x] `docs/research/` создан, заметки написаны со ссылками на первоисточники
- [x] Факты сверены с реальным поведением/пакетами (не пересказ вторички)
- [x] AGENTS/README указывают на `docs/research/`
- [x] `./tools/gate.sh` зелёный; push; CI success

## Comments

### 2026-10-12 — реализация
- Делегировано фоновому агенту (скилл `research`). Коммит `583a3a4`.
- `weasyprint-ubuntu-2404-deps.md`: пакеты сверены с `packages.ubuntu.com/noble`; объяснение имени по Debian Policy §8.1 (SONAME `libpangoft2-1.0.so.0` → пакет `libpangoft2-1.0-0`).
- `appleboy-ssh-action-script-stop.md`: `script_stop` default `false` (action.yml v1.0.3); в свежих релизах опция убрана — надёжен `set -euo pipefail`.
- CI `583a3a4` success. Тикет → `done`.
