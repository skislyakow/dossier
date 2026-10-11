# 0003 — Авто-резюме: PDF генерируется сервером из контента CMS

Date: 2026-10-11
Status: Accepted
Decision-makers: владелец сайта (движок выбран агентом по делегированию)

## Context

Файла резюме на сайте не было, а работа по сайту (тесты, ADR, CI), которую владелец хотел показывать работодателям, в резюме могла устареть и разойтись с контентом витрины. Нужен единый источник: резюме управляется в админке теми же моделями, что и сайт (опыт, проекты, навыки, контакты), а PDF — производный артефакт, который при правке контента перегенерируется сам.

Ограничения: стек менять нельзя (zero-dependency vanilla JS/CSS); деплой — Ubuntu 24.04, gunicorn, nginx; локально и в CI тот же Python-стек; PDF нужен A4, живой текст (читаемый копипастой/ATS), русский.

## Options considered

1. **Отдавать CMS-данные на клиент и рисовать PDF из браузера (window.print, jsPDF)** — нарушает принцип «сервер — владелец таксономии» (уже есть ADR-0001) и множит JS-зависимости; печать из браузера в PDF теряет единый A4-контроль.
2. **Мануальный DOCX/PDF из отдельного файла** — файл не имеет одного источника с сайтом, рассинхронизируется с контентом.
3. **WeasyPrint (HTML+CSS → PDF) на сервере** — `_body.html`-шаблон резюме рендерится один раз и на страницу `/resume/`, и в PDF; единый источник разметки и стилей.

Победил вариант 3: PDF-подсистема — это одностраничный сайт, у которого уже есть инфраструктура (шаблоны, CSS, админка, деплой).

## Decision

- Данные: `ResumeProfile` (singleton `id=1`, `load()`), `ContactInfo`, `TimelineItem` (non-project, сортировка по `start_date` desc с фолбэком на `sort_order`), `Project` (published, `role`/`date_label`/`tagline`/`features` → буллеты), `Skill` (группировка по категориям). Новые поля: `TimelineItem.start_date/end_date`, `Project.date_label`.
- Рендер: `templates/resume/_body.html` — общий partial; `static/css/resume.css` — единые стили (экрана + `@page A4` для PDF).
- Генерация: `main/resume.py` (`context()`, `build_pdf()`, `write_pdf()`, `pdf_path()`); `manage.py generate_resume`; путь — `STATIC_ROOT/resume/resume.pdf`, если `STATIC_ROOT` доступен на запись, иначе `static/resume/resume.pdf` в репо.
- Перегенерация: сигналы `post_save`/`post_delete` на 5 моделях → `write_pdf()`, гейт `settings.RESUME_AUTOGEN` (в тестах отключён: `PYTEST_CURRENT_TEST` или `RESUME_AUTOGEN=0`); сбой генерации молча проглатывается (резюме — вторичный артефакт, не должен ломать правку контента).
- Раздача: `GET /resume/` — HTML-страница, `GET /resume/pdf/` — `FileResponse(pdf_path(), content_type='application/pdf')`, `404` пока PDF не сгенерирован.
- Деплой: в `deploy.yml` перед `collectstatic` — apt-пакеты pango (WeasyPrint) + `RESUME_AUTOGEN=1 uv run manage.py generate_resume`; на проде файл пишется прямо в `STATIC_ROOT` (nginx раздаёт, `chown www-data` уже в деплое).
- Обозначение работы: инженерная строка под marquee плюс обновлённые буллеты карточки Dossier.

## Consequences

- Единый источник: правка контента в админке автоматически обновляет и сайт, и резюме; при деплое PDF всегда свежий.
- Новое поле = новая зависмость деплоя: WeasyPrint требует pango-библиотеки на VPS — шаг установлен в деплой-скрипте; в CI и тестах WeasyPrint тестируется с моком (без pango).
- PDF-файл — генерируемый артефакт: `static/resume/` в `.gitignore`, в git не входит.
- Сильные стороны серверной генерации подтверждают оба ADR: и таксономия (0001), и витрина (0002) держатся на сервере — резюме не исключение.