# 07: Contact: три канала связи

**What to build:** Посетитель видит крупную секцию Contact с тремя очевидными каналами — email, Telegram, GitHub — и пишет одним движением. Админ добавляет контакты типа `github` через существующий ContactInfo.

**Blocked by:** 02 (Design-система и Signature-момент Hero).

**Status:** done

- [x] Тип `github` добавлен в ContactInfo (миграция), доступен в админке
- [x] Секция Contact показывает три канала крупно, ссылки кликабельны
- [x] Существующие email/telegram отображаются
- [x] Существующие автотесты зелёные (27/27)
- [ ] Визуальная проверка на dev / в проде

## Comments

### Реализация (2026-10-09)

- **Model + migration**: `ContactInfo.TYPE_CHOICES` += `('github', 'GitHub')`, help_text `value` уточнён. `main/migrations/0011_contact_github.py` — `AlterField` (contact_type + value, чтобы `makemigrations --check` был чист) + `RunPython(add_github_contact, remove_github_contact)`: `get_or_create` по `contact_type='github'` с `{label: '@skislyakow', value: 'skislyakow', sort_order: 2}` — контакт попадает на прод при пуше (паттерн 0008/0010).
- **Render** (`templates/index.html`, inline-скрипт): `esc()` на всех значениях (закрыт XSS-ToDo по contact-рендеру); карточка канала: иконка (email/telegram/github, GitHub — path из hero) + `.contact-kind` (имя типа из карты kinds, моно uppercase) + `.contact-value` (label, крупно); href по типу: `mailto:` / `https://t.me/` / `https://github.com/` (username без `@`), `target=_blank rel=noopener` для не-mailto; неизвестный тип — нессылочный `<div>` (безопасный fallback); метка секции `{ контакты: N }`.
- **CSS**: `.contact-card` (max-width 860px, без поверхности) + `.contact-grid` (`repeat(auto-fit, minmax(220px, 1fr))` — 3 канала на десктопе, 1 на мобиле) + `.contact-item` — поверхность `--bg-card`, hover: border accent + translateY(-2px); старые правила (400px-карточка, хардкод `#27272a`/`rgba(250,250,250,.82)`, light-оверрайды `#f6f8fa`) удалены. `.contact-item` добавлен в reduced-motion блок.
- **Компонент метки секции**: `.exp-label/.exp-brace/.exp-count` переименованы в `.sec-label/.sec-brace/.sec-count` (метка теперь общая для Опыта и Контактов, без дублирования CSS).
- **Tests**: `ApiContactTest` (контракт type/label/value, валидные choices, github-seed `skislyakow`) + `test_contact_section_three_channels_and_escapes` (разметка/стили, запрет сырых конкатенаций, запрет старых хардкодов). 27/27, ruff чисто, `makemigrations --check` — No changes detected.
- **Docs-sync**: AGENTS.md — буллет Contact переписан, ContactInfo в CMS-моделях, XSS-ToDo сужен до github.js.

### Правки по code-review (2026-10-09)

Отчёты: `reviews/07-standards.md`, `reviews/07-spec.md` (фикс-поинт `907c27a`, ревью коммита `5b01842`).
- **Исправлено:** README docs-sync (добавлен буллет «Контакты»); `Status` → `ready-for-human`; дедупликация `esc()` — обе локальные копии в index.html удалены, используется глобальный `esc` из `portfolio.js` (гарантированно исполняется раньше обоих IIFE); Repeated Switches — единая таблица `channels[type] = {label, icon, href(v), external}` вместо `kinds`/`icons`/`hrefFor`/тернарника; `.contact`/`.contact.hidden` в reduced-motion (expand-анимация панели); хрупкие негативные ассерты в тесте заменены на позитивные `esc(...)`; валидация: ruff, 27/27, `makemigrations --check` чисто.
- **Сознательно отложено:** общая сборка метки `{ название: N }` (нужен util-модуль ради шаблона из 5 спанов — CSS уже общий `.sec-*`); перевод Contact в постоянный поток страницы (панельный паттерн — утверждённая архитектура, вне скоупа).

### Замечание визуальной проверки (2026-10-09)

- Подпись тоггла контактов в hero (`social-label`) была «Почта» при панели из трёх каналов — **исправлено на «Контакты»** (совпадает с `aria-label`, именем секции и меткой `{ контакты: N }`). Иконка-конверт оставлена (метафора контактов, первый канал — email). Единственное место с текстом «Почта» в репо — было только оно, тесты/доки не ссылались.
