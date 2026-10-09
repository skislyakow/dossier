# Standards review — `c7818d3...HEAD` (STANDARDS axis)

Diff reviewed: `git diff c7818d3...HEAD` → commits `9ceee6b` (t05), `9efd426` (закрытие 04).
Sources checked: AGENTS.md, GLOSSARY.md, `docs/agents/issue-tracker.md`, `docs/agents/triage-labels.md`, `ruff.toml` (`uv run ruff check .` — tooling-enforced, skipped), плюс smell-baseline (Fowler ch.3).

## (a) Documented-standard violations — HARD

1. **`issue-tracker.md:11` — `Status: done` при незакрытом AC.** В тикете 04 оставался непроверенным чекбокс «Визуальная проверка», хотя `done` = «все AC выполнены и верифицированы». → **Исправлено:** чекбокс отмечен с датой и подтверждением пользователя.
2. **Docs-sync: устаревший раздел AGENTS.md.** Строка `### 4. Карточки портфолио — role-based placeholder themes ✅` оставалась после того, как этот буллет удалён из Project overview и README. → **Исправлено:** запись уточнена (в редизайне заменена monogram-плейсхолдером).

Соблюдено: акценты только через `color-mix`/`--accent*`, `esc()` на всех значениях API, `prefers-reduced-motion` в CSS и JS, docs-sync (AGENTS + README в том же коммите), тесты остались в seam-паттерне «чтение файла с диска + substring».

## (b) Baseline smells — JUDGEMENT CALLS

1. **Duplicated Code + Message Chains** — `(project.repo && project.repo.full_name) || project.title` трижды и обходы `project.repo.html_url` / `.stargazers_count`. → **Исправлено:** хелпер `projectKey(project)`; обращения к repo остались локальными в одном месте (`buildPreviewHtml`).
2. **Duplicated Code** — `[data-theme="light"] .portfolio-preview-body` повторял группу `.gh-card, .tl-details-card, .contact-card`, включая мёртвый `border-color` (база уже `1px solid var(--border)`). → **Исправлено:** селектор сведён в общую light-группу.
3. **Brittle test** — `assertNotIn('ghost', js)` был шире всех остальных проверок (ловит любое слово с «ghost»). → **Исправлено:** сузил до `portfolio-ghost-skill` / `ghostFloat`; вместо этого добавлены запреты на сырую интерполяцию API-значений (`${project.title}`, `${b.label}`…), что ближе к поведению «экранируется при вставке».
4. **Снятие `prefers-reduced-motion` один раз при загрузке** — `const REDUCE_MOTION = matchMedia(...).matches` не видит смену настройки в рантайме. → **Исправлено:** `MOTION_MQ` (MediaQueryList) + `reducedMotion()` — значение читается в момент использования.
5. **Speculative Generality** — `window.getSkills()` в `Promise.all` после удаления призраков стал не нужен. → **Исправлено:** fetch навыков из карточек убран (сам хелпер остаётся — им пользуется секция Skills).

Не тронуто (принято): заголовок тикета 05 `ready-for-human` — в словаре нет роли «ожидает визуалки», остальные пять не подходят.
