# 14: SEO — og:image / twitter:image (превью при шаринге)

**What to build:** При шаринге ссылки в Telegram/Twitter/FB/вайбере карточки без картинки. Нужен превью-ассет + полный набор meta.

**Status:** done

- [x] Сгенерирован `static/og/og-image.png` (1200×630, PNG ~156 КБ): тёмный фон `#0a0a0a`, лайм-акцент `#CDFF50`, Inter/Fira Code (локальные woff2 из `static/fonts/`), моно-строка `kislyakov.pro / ● Python Fullstack`, H1 «Sergey Kislyakov», позиционирование «Автоматизация, Telegram-боты и веб на Django»
- [x] Рендер: Chrome headless из `/tmp/opencode/og/og.html` (шаблон лежит только в /tmp — сам ассет перегенерируется из него при правке дизайна)
- [x] `<head>`: `og:image` + `og:image:width/height/alt`, `twitter:card` `summary` → `summary_large_image`, `twitter:image` — абсолютный URL `https://kislyakov.pro/static/og/og-image.png`
- [x] `collectstatic` разнесёт `static/og/` на прод автоматически
- [x] Тест `test_og_image_meta_and_file`: meta-теги в HTML, файл существует (36/36)
- [x] AGENTS: To-do — og:image закрыт, структура `static/og/`