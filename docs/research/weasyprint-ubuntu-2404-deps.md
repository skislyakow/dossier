# WeasyPrint на Ubuntu 24.04 (noble): системные пакеты

**Зачем эта заметка.** 2026-10-12 авто-деплой этого сайта молча не доехал на прод:
в `.github/workflows/deploy.yml` вместо `libpangoft2-1.0-0` стоял несуществующий
`libpangoft2-0`, apt упал с `E: Unable to locate package libpangoft2-0`, а GitHub Action
всё равно отрапортовал успех (см. `appleboy-ssh-action-script-stop.md`). Здесь зафиксированы
точные имена пакетов для WeasyPrint на Ubuntu 24.04 и объяснена схема версионирования,
почему `libpangoft2-1.0-0`, а не `libpangoft2-0`.

## Точный набор пакетов (Ubuntu 24.04 «noble»)

| Пакет (noble) | Версия | Зачем | Первоисточник |
|---|---|---|---|
| `libpango-1.0-0` | 1.52.1+ds-1build1 | Pango — раскладка текста | https://packages.ubuntu.com/noble/libpango-1.0-0 |
| `libpangoft2-1.0-0` | 1.52.1+ds-1build1 | Pango + FreeType, нужен WeasyPrint | https://packages.ubuntu.com/noble/libpangoft2-1.0-0 |
| `libharfbuzz-subset0` | 8.3.0-2build2 | HarfBuzz subset (шрифтовые сабсеты) | https://packages.ubuntu.com/noble/libharfbuzz-subset0 |
| `fonts-dejavu-core` | 2.37-8 | базовые шрифты (есть кириллица) | https://packages.ubuntu.com/noble/fonts-dejavu-core |
| `fonts-dejavu-extra` | 2.37-8 | доп. начертания DejaVu | https://packages.ubuntu.com/noble/fonts-dejavu-extra |

Официальные доки WeasyPrint для Ubuntu ≥ 20.04 перечисляют
`python3-pip libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0 libharfbuzz-subset0`
(https://doc.courtbouillon.org/weasyprint/stable/first_steps.html). `fonts-dejavu-*` — добавка
проекта: доки советуют поставить шрифты, если в PDF «квадраты» вместо букв; DejaVu гарантирует
кириллицу. `libharfbuzz0b` не указан отдельно — он транзитивно тянется как зависимость
`libpangoft2-1.0-0` (`dep: libharfbuzz0b (>= 5.1.0)`).

## Почему `libpangoft2-1.0-0`, а не `libpangoft2-0`

- Пакет ставит файл `/usr/lib/x86_64-linux-gnu/libpangoft2-1.0.so.0`
  (filelist: https://packages.ubuntu.com/noble/amd64/libpangoft2-1.0-0/filelist) — это и есть SONAME.
- Debian Policy §8.1: имя runtime-пакета = имя библиотеки + *soversion*, где *soversion* — часть
  SONAME **после** `.so.` (https://www.debian.org/doc/debian-policy/ch-sharedlibs.html#run-time-shared-libraries).
  Для `libpangoft2-1.0.so.0` *soversion* = `0`, поэтому пакет `libpangoft2-1.0-0`.
- `1.0` здесь — версия ABI-интерфейса Pango (Pango 1.x), `-0` — собственно SONAME-мажор.
- Пакета `libpangoft2-0` не существует: он соответствовал бы SONAME `libpangoft2.so.0`
  (без `1.0`), которого у Pango нет.

## apt-команда проекта

```bash
apt-get update
DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    libpango-1.0-0 libpangoft2-1.0-0 libharfbuzz-subset0 \
    fonts-dejavu-core fonts-dejavu-extra
```

**Симптом опечатки в имени пакета:** `E: Unable to locate package libpangoft2-0`.

## Источники
- WeasyPrint — First Steps (Ubuntu ≥ 20.04): https://doc.courtbouillon.org/weasyprint/stable/first_steps.html
- libpangoft2-1.0-0 (noble): https://packages.ubuntu.com/noble/libpangoft2-1.0-0
- libpango-1.0-0 (noble): https://packages.ubuntu.com/noble/libpango-1.0-0
- libharfbuzz-subset0 (noble): https://packages.ubuntu.com/noble/libharfbuzz-subset0
- fonts-dejavu-core (noble): https://packages.ubuntu.com/noble/fonts-dejavu-core
- fonts-dejavu-extra (noble): https://packages.ubuntu.com/noble/fonts-dejavu-extra
- File list libpangoft2-1.0-0 (SONAME-файл .so.0): https://packages.ubuntu.com/noble/amd64/libpangoft2-1.0-0/filelist
- Debian Policy §8.1 Run-time shared libraries: https://www.debian.org/doc/debian-policy/ch-sharedlibs.html
