# 05: `nginx-guard` — on-host агент с авто-восстановлением

Status: ready-for-agent
Blocked by: 02

**What to build:** Агент на VPS (`agent/` в репо `uptime-monitor`), который раз в 60 секунд проверяет nginx, безопасно рестартует его при валидном конфиге и сообщает в Telegram. Именно он закрыл бы инцидент 5 ноября за минуту.

## Решения

- `agent/nginx_guard.py`:
  - инъекция `runner(cmd: list[str]) -> (rc, out)` — тесты без реального systemd;
  - алгоритм: `systemctl is-active nginx` → `active` = тишина и сброс состояния; иначе `nginx -t`:
    - rc=0 → `systemctl restart nginx`, пауза 3 с, `is-active` → алерт `nginx_recovered` (причина — последняя строка `journalctl -u nginx -n 5 --no-pager`; если её нет — «сервис был остановлен»);
    - rc≠0 → рестарт **не** выполняется, алерт `nginx_broken(<последняя строка stderr nginx -t>)`, не чаще 1 раза в час;
  - страховки: рестарт не чаще 1 раза в 5 мин; алерты дедуплицируются 30 мин; `--dry-run` (ничего не рестартует и не отправляет, печатает план).
  - состояние `/var/lib/nginx-guard/state.json` (создаётся при первом запуске, каталог 700);
  - любые исключения логируются и **не** валят юнит (exit 0), иначе `OnUnitActiveSec` не сработает снова;
  - логи — stdout → journald; секретов в логах нет.
- `agent/nginx-guard.service`: `Type=oneshot`, `EnvironmentFile=/etc/nginx-guard/env`.
- `agent/nginx-guard.timer`: `OnBootSec=60s`, `OnUnitActiveSec=60s`, `Persistent=true`.
- `agent/env.example` (пустые значения) и `agent/install.sh`:
  - идемпотентная установка: код → `/opt/nginx-guard/`, env → `/etc/nginx-guard/env` (600, не перезаписывать существующий без флага), юниты → `/etc/systemd/system/`, `daemon-reload`, `enable --now nginx-guard.timer`;
  - флаги `--dry-run`, `--uninstall`; проверка «запущено от root».
- README раздела agent: почему `nginx -t` обязателен перед рестартом, как читать алерты, как посмотреть журнал.

## Acceptance criteria

- [ ] Тесты (фейковый runner): nginx active → 0 действий, 0 сообщений; failed + `nginx -t` ok → ровно один restart и один алерт; failed + bad config → restart **не** вызван, алерт с текстом ошибки; повторный bad-config в пределах часа → без нового сообщения; рестарт-лимит 5 мин работает; ошибка Telegram не роняет процесс (exit 0).
- [ ] `--dry-run` на здоровом хосте ничего не делает и печатает «nginx active».
- [ ] ruff + mypy + pytest зелёные в CI.
