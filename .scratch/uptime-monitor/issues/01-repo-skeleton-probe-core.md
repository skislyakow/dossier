# 01: Каркас репо `uptime-monitor` + ядро внешнего пробника

Status: ready-for-agent
Blocked by: —

**What to build:** Новый репозиторий `skislyakow/uptime-monitor` (Python 3.12, stdlib только для рантайма) с ядром проверки URL. Транспорт инжектится — тесты без сети, по образцу `main/fetch.py` в dossier.

## Решения

- Структура: `probe.py`, `config.json` (реальный конфиг), `config.example.json`, `tests/`, `pyproject.toml` (pytest/ruff/mypy в dev-группе), `README.md`, `.gitignore`.
- `CheckResult` (dataclass): `name, ok, status, latency_ms, reason, cert_days, checked_at`.
- `check_target(target, transport)`:
  - GET с `timeout` из конфига (default 15 с), 2 попытки с паузой 20 с внутри прогона;
  - fail, если статус ≠ `expect_status` (default 200), если `expect_marker` не найден в теле, если timeout/сетевая ошибка;
  - TLS: срок сертификата через `ssl`/`socket` (один socket-хендшейк на прогон), `cert_days = (notAfter - now).days`.
- `check_all(config)` → список результатов; CLI: `python probe.py --config config.json --json` печатает JSON (для workflow), без `--json` — человекочитаемо.
- Конфиг (`config.json`) на MVP: один таргет — `{"name": "kislyakov.pro", "url": "https://kislyakov.pro/", "expect_status": 200, "expect_marker": "#skills", "timeout": 15}`.
- README: что это, как локально запустить, как добавить таргет, почему монитор живёт вне VPS.

## Acceptance criteria

- [ ] `uv`-независимый запуск: `python probe.py --config config.json --json` работает на голом Python 3.12 (без pip-зависимостей).
- [ ] Тесты: 200+маркер → ok; 502 → fail `HTTP 502`; timeout → fail с причиной; маркер отсутствует → fail «нет маркера #skills»; латентность считается; TLS-дни парсятся (фейковый сертификат).
- [ ] Тесты не ходят в сеть (фейковый транспорт, проверка «вызван N раз с ожидаемым URL»).
- [ ] Реальный прогон против `https://kislyakov.pro/` → ok, `cert_days > 0`.
- [ ] ruff + mypy + pytest зелёные в CI нового репо.
