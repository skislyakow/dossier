# 02: Research-заметки по деплою — docs/research/

**What to build:** Завести конвенцию `docs/research/` и зафиксировать первичные знания, добытые при починке тихого не-задеплоя (2026-10-12), чтобы знание не терялось. Делегируется фоновому агенту (скилл `research`), каждый факт — со ссылкой на первоисточник (офиц. доки / исходники / spec).

**Blocked by:** None.

**Status:** ready-for-agent

## Scope
- `docs/research/weasyprint-ubuntu-2404-deps.md` — точный набор apt-либ для WeasyPrint на Ubuntu 24.04; почему `libpangoft2-1.0-0`, а не `libpangoft2-0`.
- `docs/research/appleboy-ssh-action-script-stop.md` — семантика `script_stop`, как возникал тихий не-задеплой.
- Указатель из AGENTS (Dev workflow / Auto-deploy) и/или README.

## AC
- [ ] `docs/research/` создан, заметки написаны со ссылками на первоисточники
- [ ] Факты сверены с реальным поведением/пакетами (не пересказ вторички)
- [ ] AGENTS/README указывают на `docs/research/`
- [ ] `./tools/gate.sh` зелёный; push; CI success

## Comments
