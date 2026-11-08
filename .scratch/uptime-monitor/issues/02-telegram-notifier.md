# 02: Telegram-нотификатор и формат сообщений

Status: ready-for-agent
Blocked by: 01

**What to build:** Модуль отправки сообщений в Telegram (Bot API `sendMessage`, `urllib`, stdlib) + единые шаблоны сообщений для всех слоёв мониторинга.

## Решения

- `notify.py`: `send(token, chat_id, text, transport=UrllibTransport()) -> bool`; 3 попытки с backoff 2/4/8 с; успех — HTTP 200 и `"ok": true`; при окончательной неудаче — `False` (не исключение) и запись причины в stderr.
- Plain text, **без** `parse_mode` (никакого экранирования HTML/Markdown); обрезка до 4096 символов.
- Санитизация: токен и chat_id не попадают в текст исключений/логов (маскировать `<REDACTED>`).
- Шаблоны (`messages.py`), русский язык, время UTC:
  - `down(target, reason, at)`: `🔴 kislyakov.pro недоступен` / причина / `Проверено: 2026-11-08 12:00 UTC` / `Следующая проверка через 5 мин`.
  - `recovered(target, downtime, status, latency_ms, cert_days)`: `🟢 kislyakov.pro снова доступен` / `Простой: 12 мин` / `HTTP 200, 118 мс, сертификат 48 дн.`
  - `reminder(target, downtime, reason, at)`: `🔴 kislyakov.pro всё ещё недоступен (2 ч 15 мин)` + причина.
  - `cert_warning(target, days)`: `🟡 Сертификат kislyakov.pro истекает через 12 дн.`
  - `nginx_recovered(reason)`: `🔴→🟢 nginx упал и восстановлен автоматически` / `Причина: …` / `Время: …`.
  - `nginx_broken(error_line)`: `🔴 nginx не запущен, конфиг невалиден` / `<ошибка nginx -t>` / `Авто-рестарт не выполнялся.`
- `--dry-run`/`--print` в CLI: печатает сообщение, не отправляет.
- Как получить `chat_id` и токен (+BotFather) — в README.

## Acceptance criteria

- [ ] Фейковый транспорт: успех → True; 429 → повтор; 500 → повтор; сетевая ошибка → False без исключения; токен не в тексте ошибки.
- [ ] Все шаблоны покрыты тестами (снапшоты строк, фиксированное `now`).
- [ ] Обрезка текста >4096 символов работает.
- [ ] `python -m notify --dry-run` (или флаг в `probe.py`) печатает сообщение, не делая сетевых вызовов.
