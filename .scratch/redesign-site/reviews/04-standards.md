# Standards review — `0723413...HEAD` (STANDARDS axis)

Diff reviewed: `git diff 0723413...HEAD` → commits `5d7f473` (t04), `2d4df43` (закрытие 03 + пометки в 09).
Sources checked: AGENTS.md, GLOSSARY.md, `docs/agents/issue-tracker.md`, `docs/agents/domain.md`, `docs/agents/triage-labels.md`, `ruff.toml` (`uv run ruff check .` passes — tooling-enforced, skipped), плюс зафиксированный в спеке smell-baseline (Fowler ch.3).

## (a) Documented-standard violations — HARD

Нет. Docs-sync выполнен (README.md + AGENTS.md в том же изменении); `/api/skills/`-тест через Django test client; новые тесты — substring-on-disk стиль; новый CSS только на токенах (никаких rgba/hex-акцентов); миграция — обратимый `RunPython(forwards, backwards)`; статусы тикетов — канонические; термин «Категория навыка» взят из GLOSSARY без синонимов.

## (b) Baseline smells — JUDGEMENT CALLS

1. **Duplicated Code / Shotgun Surgery — «пятёрка» категорий.** Словари категорий продублированы в `main/models.py` (`CATEGORY_CHOICES`), `0010_skill_category.py` (слаги), `templates/index.html` (метки) и `main/tests.py` (валидные значения). → **Частично исправлено:** тест теперь выводит валидные значения из `Skill.CATEGORY_CHOICES`. Остальное **принято как есть**: слаги в миграции и метки в JS неизбежны (миграция не должна читать код модели, JS меток нет в API-контракте), правка категории = один редкий редакторский шаг.
2. **Dead code в `0010_skill_category.py`** — строка `exclude(category__in=CATEGORY_BY_NAME.values())` ничего не находила (все строки приходят с `default='tools'`), т.е. фолбэк «неизвестное имя → tools» существовал только через default. → **Исправлено:** `exclude(name__in=CATEGORY_BY_NAME)` — фолбэк реально работает.
3. **Docs-sync точность (`AGENTS.md`)** — `0010` был приписан к фразе про `get_or_create`/`sort_order`, хотя использует `filter().update()`. → **Исправлено:** отдельное предложение для `0010_skill_category.py` (schema + data миграция).
4. **XSS — `s.name` в `innerHTML`** (низкий риск, admin-контент; в AGENTS.md заведено как known issue для portfolio/timeline/github.js). → **Исправлено:** добавлен локальный `esc()` + whitelist размера (`sizes[s.size] ? s.size : 'sm'`) — спека требует экранировать при переписывании вывода.
5. **Issue-tracker-конвенция** — заметки ушли под отдельным заголовком `## Implementation notes`. → **Исправлено:** перенесено под `## Comments` (`### Реализация (2026-10-09)`).
6. **Brittle tests** — `test_skills_section_grouped_by_category` проверял точные JS-выражения (`s.category === pair[0]`). → **Исправлено:** проверяет семантику (`class="skill-group"`, метку категории, чтение `s.category`, пропуск пустых групп), не точный текст выражения.

Нет Speculative Generality, Message Chains, Middle Man. ruff-релевантных замечаний нет.
