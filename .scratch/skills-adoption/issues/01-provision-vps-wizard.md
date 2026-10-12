# 01: Wizard восстановления VPS — tools/provision-vps.sh + deploy/

**What to build:** Интерактивный bash-wizard (`tools/provision-vps.sh`, по шаблону скилла `wizard`) ведёт человека по шагам поднятия прод-VPS с голой Ubuntu 24.04 (disaster recovery / смена провайдера): VPS+IP → DNS (reg.ru) → SSH-ключ → GitHub secrets → remote bootstrap → установка systemd/nginx → certbot → опц. `GITHUB_TOKEN` → первый деплой. Конфиги инфры, которые сейчас живут только на VPS, выносятся в репо (`deploy/dossier.service`, `deploy/nginx.conf`). Скрипт **ничего не делает, пока его не запустят вручную**; перед необратимыми шагами — `confirm`.

**Blocked by:** None.

**Status:** ready-for-agent

## Scope
- Сначала **только чтение по ssh**: снять `/etc/systemd/system/dossier.service`, nginx-конфиг, проверить наличие `GITHUB_TOKEN` на проде.
- `deploy/dossier.service`, `deploy/nginx.conf` — закоммитить; wizard их копирует на VPS.
- `tools/provision-vps.sh` — библиотека шаблона `wizard/template.sh` не редактируется; стадии ниже маркера `STAGES`; `TOTAL_STAGES` = число стадий; `chmod +x`.
- README — ссылка на восстановление; AGENTS `## Production` → указатель на `deploy/` и wizard.

## AC
- [x] Считаны живые конфиги с VPS; `deploy/dossier.service` + `deploy/nginx.conf` в репо
- [x] `tools/provision-vps.sh` создан, `bash -n` чист (shellcheck локально нет), `chmod +x`
- [x] Стадии покрывают: VPS+IP, DNS reg.ru, `VPS_SSH_KEY`, GitHub secrets (`VPS_HOST`/`VPS_SSH_KEY`), remote bootstrap, systemd+nginx, certbot, `GITHUB_TOKEN`, первый деплой+smoke
- [x] Каждый `set_secret` совпадает с `secrets.*` в `.github/workflows/deploy.yml` (`VPS_HOST`, `VPS_SSH_KEY`)
- [x] README + AGENTS синхронизированы
- [ ] `./tools/gate.sh` зелёный; push; CI success; прод-смок

## Comments

### 2026-10-12 — реализация
Снято с живого VPS (ssh, только чтение):
- `dossier.service` держал `Environment=DJANGO_SECRET_KEY=<insecure>`, `.env` нет, `GITHUB_TOKEN` на проде **не задан**. В репо вынес секреты в `EnvironmentFile=-/etc/dossier/dossier.env` (wizard пишет туда свежий `token_urlsafe(50)` + опц. токен; `-` = файл опционален, иначе фолбэк на дефолт из `settings.py`).
- VPS **общий**: кроме dossier крутятся bakecake/beauty/selfstorage/star-burger (свои юниты и vhost'ы). Wizard ставит только `sites-available/dossier` + `dossier.service`, чужие сайты не трогает.
- `nginx.conf` — pre-TLS: TLS-блоки и редиректы инжектит certbot (`certbot --nginx -d kislyakov.pro -d www.kislyakov.pro --redirect`), чтобы конфиг был воспроизводим на чистой машине (иначе nginx не стартует без `/etc/letsencrypt/...`).
- Legacy-локации `/api/ask/` и `/vkauth/` из прод-конфига закомментированы: у `/api/ask/` нет роута в `config/urls.py`, на `:8888` нет слушателя. Помечены «verify before re-enabling».
- `.env` добавлен в `.gitignore` (wizard пишет локальный `.env` с `VPS_HOST`/`SSH_KEY_PATH`).
