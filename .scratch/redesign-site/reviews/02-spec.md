# Spec review: 9bc3da6 (design tokens + hero signature)

## (a) Missing / partial

1. **Fallback orange via one token — partial.** Spec: «акцент `#CDFF50` (запасной оранжевый включается правкой одного токена)». There is no orange token — only a comment (`style.css:27`). Editing `--accent` alone leaves lime in `--accent-soft` / `--accent-ring` (`style.css:30-31`) and in the hardcoded hero gradient `rgba(205, 255, 80, 0.05)` (`style.css:73`). One-token switch does not actually work.
2. **Типографическая шкала — partial.** Spec: «типографическая шкала» как токены. `--type-scale-*` is applied only to hero name/role/positioning; section `h1` (4rem, `style.css:218`), `.title` (1.5rem), card titles stay hardcoded.
3. Verified OK: «Существующие автотесты зелёные» — full suite 13 tests pass.

## (b) Not asked for (scope creep)

1. **Light-theme restyle.** Diff changes `[data-theme="light"] --page-bg: #ffffff → #f5f0eb` and `--bg-card: #ffffff → rgba(255,255,255,0.82)`. Ticket only asks: «Дефолт тёмная тема; светлая тема работает переключателем». The beige is the old warm palette and contradicts «Сайт обретает новый визуальный язык: монохром + кислотный лайм».
2. **New tests assert raw file contents.** `DesignSystemTest` reads `style.css` and substring-matches it. Spec Testing Decisions: «Хороший тест проверяет внешнее поведение через HTTP, а не внутренности», «JS/CSS автотестов нет».

## (c) Implemented but looks wrong

1. **Dark default palette mixes light values with light text → broken contrast.** Spec: «дефолт — тёмная тема» + «монохромная палитра». `:root` sets `--bg-card: rgba(255,255,255,0.9)`, `--border: #e4e4e7` (`style.css:35-36`) while `--text-primary: #f4f4f5`. This diff recolors `.gh-card-name` and `.tl-details-title` to `var(--text-primary)` → near-white text on near-white card in default theme. Same pattern: `.badge-label`/`.badge-value`/`.tag` keep hardcoded `#e4e4e7` bg with `var(--text-secondary)` (#a1a1aa).
2. **Cursor gradient is not «приглушён».** Spec: «приглушённый курсорный градиент». Old gradient faded to `rgba(...,0.15)`; new one ends in full-opacity `var(--accent)` at 90% (`style.css:108-111`), so text away from the cursor renders saturated `#CDFF50` — louder, not muted.
3. Correctly done (no issue): dark default (`<html lang="ru">`, JS `stored === 'light'` branch), positioning line text, IntersectionObserver reveal, reduced-motion guards (JS early-return + CSS media query).
