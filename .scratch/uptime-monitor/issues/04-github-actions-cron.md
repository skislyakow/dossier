# 04: GitHub Actions cron + секреты

Status: ready-for-agent
Blocked by: 01, 02, 03

**What to build:** Workflow `.github/workflows/probe.yml` в `uptime-monitor`: внешний пробник каждые 5 минут, алерты через сохранённый `state.json`, ручной запуск для отладки.

## Решения

- `on: schedule: [{cron: '*/5 * * * *'}], workflow_dispatch: {}`.
- `permissions: contents: write` (только для коммита ветки `state`); `timeout-minutes: 5`.
- Шаги: checkout `main` → checkout `state` в `.state/` (если ветки нет — создать пустое состояние) → `python probe.py --config config.json --json > result.json` → `python -m notify ...` (или единый `run.py`, решает тикет) → commit/push `state`.
- Секреты репо: `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`. При отсутствии — прогон падает с понятной ошибкой и **без** алерта.
- Опционально: `workflow_dispatch` input `force_message` для тестового сообщения («🔔 тестовый алерт»).
- README: известные ограничения GitHub `schedule` (опоздания 5–15 мин; отключение после 60 дней без активности репо) и как проверить, что cron жив.

## Acceptance criteria

- [ ] Ручной запуск (`workflow_dispatch`) → зелёный прогон, в Telegram приходит сообщение (тестовое или реальный статус).
- [ ] Прогон по расписанию есть в Actions (проверить через 10–15 мин), лог содержит результат проверки.
- [ ] При первом изменении статуса ветка `state` создаётся/обновляется одним коммитом; в `main` мусора нет.
- [ ] Без секретов workflow падает с явной ошибкой, не отправляя кривых алертов.
- [ ] Проверено, что два подряд запуска не конфликтуют по `state` (concurrency).
