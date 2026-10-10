# 10: Баг: невидимые названия проектов в списке портфолио

**What to build:** Названия проектов в списке слева невидимы при открытии панели Projects — виден только первый (активный); остальные проявляются только после клика (по одному). Баг воспроизводился на двух машинах пользователя.

**Blocked by:** 09 (Облако тегов проектов).

**Status:** done

- [x] Диагностика: названия списка рендерились `<span class="reveal" style="--i">`, видимость зависела от `IntersectionObserver` + отложенного `scrollIntoView` (150 мс) — хрупкая цепочка, срывается; клик «проявлял» пункт, когда IO ре-обсервил элемент
- [x] Фикс: `revealIn` (IO-наблюдатель) удалён из `portfolio.js`, заменён на синхронный `revealNow` (мгновенное добавление `.is-visible`); после рендера списка/превью вызывается сразу
- [x] Названия пунктов списка рендерятся обычным `<span>` без `.reveal` — не зависят от reveal вообще; reveal остаётся только в превью-карточке (по `--i`), что работает
- [x] Препятствия: heading-фрагмент списка собран как `revealNow(portfolioSection)` после полного рендера; переключение превью — `revealNow(preview)` (как было `revealIn`)
- [x] Тесты: `test_portfolio_eager_reveal_without_observer` (нет `revealIn`/`IntersectionObserver` в JS, есть `revealNow`); из `test_enhanced_card_surface_and_motion_guards` убран assert на `IntersectionObserver`
- [x] Полный гейт зелёный: 33/33 теста + ruff + node --check + makemigrations --check
- [x] Инвентаризация: AGENTS.md «стаггер-reveal по `--i`» уточнён (reveal стал eager-синхронным), GLOSSARY/README не менялись — термин «scroll-reveal» остаётся про hero
- [x] Проверка на проде после пуша: открыть Projects, список слева полностью виден сразу, без клика

Коммит: `023b2ce t10+t11: баг-фикс reveal списка + кликабельные навыки — фильтр проектов`