# Spec review - `907c27a...HEAD` (5b01842) - SPEC axis

Основание: `.scratch/redesign-site/issues/07-contact-three-channels.md` (чекбоксы AC — авторитетны), `spec.md` (US#7, US#9, US#11/12, US#15/16, Solution «Contact: три канала… ContactInfo расширяется типом github», Implementation Decisions «рендеринг в JS … экранировать», Testing Decisions), `GLOSSARY.md`. Утверждения `## Comments` тикета сверены с diff — подтверждены все (model+seed `skislyakow`, esc-рендер, href-мапа, fallback-`<div>` для неизвестного типа, ренейм `.sec-*`, reduced-motion, 27/27, docs-sync).

## (a) Missing / partial

1. **US#7 «крупной секцией Contact, so that писать одним движением, не ися футер»** — секция по-прежнему стартует `class="contact hidden"` и раскрывается тогглом из hero; «в потоке страницы» не лежит. **Разбор:** панельный паттерн (`#portfolio/#stats/#contact` как `.show`-панели) — утверждённая архитектура (t01/t10: `body:has(...)`-правила, скрытие рельса при любой панели); AC тикета «показывает три канала крупно» верифицируется в открытом состоянии. Перевод Contact в постоянный поток = переструктура вне скоупа тикета. Отмечено как интерпретация, не как gap.
2. Прочие AC без пробелов: тип github в админке, кликабельные ссылки, существующие email/telegram, зелёные тесты.

## (b) Scope creep (раскрыт в Comments тикета)

1. **Кросс-секционный ренейм** `.exp-label/.exp-brace/.exp-count` → `.sec-label/…` (style.css + timeline.js) — чужой по букве тикета Опыта, но necessitated: метка стала общим компонентом (Опыт + Контакты), без ренейма — дублирование CSS. Behavior-neutral, остатков `exp-*label*` нет.
2. **Рестайл сверх «трёх каналов»** — hover `background → border-accent + translateY(-2px)`, удаление light-оверрайдов `#f6f8fa`. Внутри «крупной секцией» (спека не детализирует визуал), дизайн-решения зафиксированы в Comments.

## (c) Looks implemented but questionable

1. **US#12 «отключать необязательные анимации»** — `.contact-item` был в reduced-motion, но expand-анимация самой панели (`.contact`/`.contact.hidden`, `transition: all 0.4s/0.3s`) — нет; pre-existing, но тикет владел contact-pass по reduced-motion. → **Исправлено:** `.contact, .contact.hidden` добавлены в reduced-motion блок (специфичность `.contact.hidden` покрыта явно, блок позже в файле → выигрывает).
2. **Testing Decisions «тест проверяет внешнее поведение…»** — негативные ассерты на сырые конкатенации (`'+ item.label +'`) хрупки к безвредным рефакторам. → **Исправлено:** заменены на позитивные `esc(item.label)` / `esc(href)` (при исчезновении экранирования тест всё ещё падает).
3. **Migration `backwards`** удаляет все github-контакты, включая админские после seed'а — следует паттерну 0008, принято.

Дрейфа терминов GLOSSARY нет.
