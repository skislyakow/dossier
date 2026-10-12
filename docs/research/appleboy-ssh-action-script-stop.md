# `appleboy/ssh-action`: `script_stop` и тихий провал деплоя

**Зачем эта заметка.** 2026-10-12 деплой упал молча: удалённый скрипт содержал битую apt-команду
(`libpangoft2-0`), но GitHub Action `appleboy/ssh-action@v1` отрапортовал успех, и джоба осталась
зелёной, т.е. прод не обновился незаметно. Причина — поведение `script_stop` по умолчанию (`false`).
Заметка фиксирует это и «боевой» паттерн защиты, который теперь стоит в `deploy.yml`.

## Что делает `script_stop`

В релизах `appleboy/ssh-action@v1.0.x` input `script_stop` описан как «Stop the script after the
first failure», **default `false`** (таблица и `action.yml` в v1.0.3). Значение прокидывается в
`drone-ssh` как `INPUT_SCRIPT_STOP` / `PLUGIN_SCRIPT_STOP`, где это флаг `script.stop`
(`cli.BoolFlag`, у которого явного default нет → Go-ноль `false`; env-переменные
`PLUGIN_SCRIPT_STOP`, `INPUT_SCRIPT_STOP`).

В коде `drone-ssh` (`plugin.go`, функция `scriptCommands()`) при `ScriptStop: false` команды
склеиваются в один поток как есть, без проверки кода возврата. Строка-страж
`... DRONE_SSH_PREV_COMMAND_EXIT_CODE=$? ; if [ $DRONE_SSH_PREV_COMMAND_EXIT_CODE -ne 0 ]; then exit ...; fi;`
добавляется после каждой команды **только** при `ScriptStop: true`.

Поэтому без `script_stop` падение промежуточной команды не прерывает скрипт: наружу уходит статус
последней команды, `Exec()` возвращает `nil`, а action печатает
`✅ Successfully executed commands to all hosts.` — джоба зелёная. Это и есть тихий не-деплой.

> Важно: в свежих релизах `script_stop` из `action.yml` **убран**, а README прямо говорит:
> «To mimic the removed `script_stop` option, add `set -e` at the top of your shell script».
> Значит, `@v1` как плавающий major-тег может уже игнорировать `script_stop`; надёжной
> гарантией остаётся `set -e` / `set -euo pipefail`.

## Паттерн защиты, используемый в проекте

`.github/workflows/deploy.yml`:

```yaml
- name: Deploy via SSH
  uses: appleboy/ssh-action@v1
  with:
    script_stop: true        # историч. опция; теперь дублируется set -e
    script: |
      set -euo pipefail      # любая упавшая команда валит скрипт -> exit != 0 -> красная джоба
      cd /root/dossier
      git fetch origin main
      git checkout -f -B main origin/main   # детерминированный чек-аут
      git clean -fd
      # ... uv sync, migrate, apt-get install, generate_resume, collectstatic, restart
```

Три части паттерна:
1. `script_stop: true` — «стоп на первой ошибке» для версий, где опция ещё существует.
2. `set -euo pipefail` в начале `script` — современный переносимый эквивалент: `-e` останавливает
   на первой ошибке, `-u` ловит неинициализированные переменные, `-o pipefail` — падение в конвейере.
3. Детерминированный чек-аут `git fetch origin main && git checkout -f -B main origin/main && git clean -fd`
   — не зависит от грязного/разъехавшегося дерева на VPS (устойчивее, чем `git pull`).

## Источники
- appleboy/ssh-action README (master; note «To mimic the removed `script_stop`…»): https://github.com/appleboy/ssh-action
- appleboy/ssh-action README v1.0.3 (таблица: `script_stop` default `false`): https://github.com/appleboy/ssh-action/blob/v1.0.3/README.md
- appleboy/ssh-action `action.yml` v1.0.3 (`script_stop`: "Stop the script after the first failure"): https://github.com/appleboy/ssh-action/blob/v1.0.3/action.yml
- appleboy/drone-ssh `main.go` (флаг `script.stop`, env `PLUGIN_SCRIPT_STOP`/`INPUT_SCRIPT_STOP`): https://github.com/appleboy/drone-ssh/blob/master/main.go
- appleboy/drone-ssh `plugin.go` (`scriptCommands()`: страж exit-code только при `ScriptStop`): https://github.com/appleboy/drone-ssh/blob/master/plugin.go
