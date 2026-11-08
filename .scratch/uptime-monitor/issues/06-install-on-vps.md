# 06: Установка `nginx-guard` на VPS

Status: ready-for-agent
Blocked by: 05

**What to build:** Развернуть агент на `132.243.121.192` (общий хост, Ubuntu 24.04) и убедиться, что таймер работает, алерты доходят, авто-рестарт безопасен.

## Решения

- Установка — вручную от root по README (не через деплой dossier: хост-уровень, другой проект, не должен зависеть от CI портфолио).
- Порядок: скопировать `agent/` на хост → `install.sh` с токеном/chat_id (вводятся интерактивно, не в history) → `systemctl list-timers | grep nginx-guard` → `journalctl -u nginx-guard -f`.
- Проверить, что env-файл вне git и 600; в репо только `env.example`.
- Обновить `AGENTS.md` dossier: в `## Production` — «на VPS работает `nginx-guard` (репо `uptime-monitor`): раз в минуту проверяет nginx, при failed и валидном `nginx -t` рестартует и шлёт в Telegram; правило — после правки конфига nginx всегда `nginx -t` до reload».
- В `docs/research/` dossier (опционально) — заметка «мониторинг VPS» со ссылками на GitHub Actions cron docs и Bot API sendMessage.

## Acceptance criteria

- [ ] `nginx-guard.timer` active, `nginx-guard.service` отрабатывает раз в минуту (видно в journald, без ошибок).
- [ ] `/etc/nginx-guard/env` — 600; токен не встречается в `journalctl -u nginx-guard` и в истории shell.
- [ ] `--dry-run` на хосте: «nginx active», ноль действий.
- [ ] После установки nginx и все 5 сайтов работают как раньше (smoke dossier + внешний `curl` соседних доменов).
- [ ] `AGENTS.md` обновлён и закоммичен в dossier.
