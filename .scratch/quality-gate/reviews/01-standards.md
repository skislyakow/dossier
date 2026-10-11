# Standards review — `0fc7cbe..HEAD` (STANDARDS axis)

Источники: AGENTS.md, ruff.toml, GLOSSARY.md, docs/agents/*.md, docs/adr/. Ruff (E4,E7,E9,F) и mypy проходят — пропущены.

## (a) Documented-standard violations — HARD

1. **`RESUME_AUTOGEN=0` disable path broken.** `config/settings.py:219-220` документирует «В тестах отключается автоматически (PYTEST_CURRENT_TEST или RESUME_AUTOGEN=0)», ADR-0003:26 повторяет; но `main/signals.py:9-14` — `if os.environ.get('RESUME_AUTOGEN', ''): return True`: любое непустое значение, включая `"0"`, истинно — документированный гейт `RESUME_AUTOGEN=0` не выключает сигналы, а также тенит `PYTEST_CURRENT_TEST`. AGENTS.md:18 называет это «гейт `settings.RESUME_AUTOGEN`», но env-`"0"` перебивает сеттинг на True.
2. **AGENTS.md test inventory stale.** AGENTS.md:33 перечисляет `test_views/test_badges/test_audit/test_admin/test_design/test_migrations/test_resume`; дифф добавляет `test_fetch.py` и `test_seo.py` (правильно по правилу зеркала модулей) — AGENTS.md не синхронёнсть (Dev workflow #10).

## (b) Judgement calls

1. **Repeated Switches — `contact_type`.** Каскад if/elif продублирован в трёх местах: `ContactInfo.href()` (models.py:117), `is_external()` (models.py:127), выбор github/telegram в `seo._same_as` (seo.py:8). Добавление нового типа контакта = правка трёх точек.
2. **Mysterious Name — `for names in [skills[code]]`.** resume.py:27 — идиома «распаковать список из одного элемента» без имени, читается хуже намерения «категория → имена навыков».
3. **Primitive Obsession — размер `xl|lg|md|sm`.** Вокабуляр объявлен трижды: пороги только в `taxonomy.skill_size()` (хорошо), но список значений — в `skills.js:18`, `smoke.sh:100,130`, GLOSSARY.md:32. Расширение шкалы = правка Python + JS + смоук.
4. **Speculative Generality — `badge_utils.catalog()`.** Хардкод `{"github": [], "pypi": []}` затем индексируется `meta["group"]` — новый source с другим group даст KeyError.
5. **Inconsistent imports — lazy `.resume`.** `views.py` импортирует `sort_by` только точечно; стиль импортов в модуле неоднороден (сравни с верхом модуля).
6. **Duplicated Code — `resume.py:pdf_path()`.** Суффикс `resume/resume.pdf` собирается в двух ветках (STATIC_ROOT и STATICFILES_DIRS) — рассинхрон имени поправится в одном месте из двух.