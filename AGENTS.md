# Agents

## Setup
- Virtual environment: `.venv/`
- Python: 3.12+
- Django: 6.0.4
- Run dev server: `python manage.py runserver`

## Structure
- `config/` — Django project settings (settings.py, urls.py, wsgi.py, asgi.py)
- `main/` — Main app (views, models, admin)
- `templates/` — HTML templates
- `static/css/` — Styles
- `static/js/` — Scripts (typing.js, typewriter.js, github.js, portfolio.js)
- `static/favicon.svg`
- `requirements.txt` — Python dependencies

## Dev workflow
1. Activate venv: `.venv\Scripts\activate`
2. Run server: `python manage.py runserver`
3. Visit `http://127.0.0.1:8000/`

## Production
- VPS: `132.243.121.192` (Ubuntu 24.04)
- Nginx reverse proxy → gunicorn (127.0.0.1:8000)
- systemd service: `dossier.service`
- Static files: `/var/www/dossier/static/`
- Auto-deploy: GitHub Actions on push to `main`

## Auto-deploy
GitHub Actions SSH into VPS and runs:
```
git pull → pip install → collectstatic → restart gunicorn
```
Required GitHub secrets: `VPS_HOST`, `VPS_SSH_KEY`

## Project overview
Personal portfolio / visiting card site for Sergey Kislyakov (Python Fullstack Developer).
- Typing animation for job title
- Interactive terminal with macOS-style window (opencode-py SSE streaming)
- AI assistant with system prompt (portfolio manager role)
- Skills cloud with curly braces `{ Python } { Django }`
- Two-column layout: terminal (left) + skills cloud (right)
- GitHub stats toggle (stars, repos, languages via GitHub API)
- Portfolio section with project cards (GitHub data + badges)
- Dynamic badges from GitHub API, PyPI, PyPistats
- Projects in portfolio: opencode-py, Ferma, Devman Bot, Dossier, Online Library

## Adding a project to portfolio
Edit `static/js/portfolio.js` → append to `PORTFOLIO` array:
```js
{
  repo: "skislyakow/repo-name",
  pypi: "package-name",  // optional: enables PyPI + PyPistats badges
  title: "Project Title",
  tagline: "Short description",
  features: ["Feature 1", "Feature 2"],
  links: { pypi: "https://...", www: "https://..." },
  badges: [
    { label: "pypi", source: "pypi_version" },      // dynamic from PyPI
    { label: "python", source: "pypi_python" },      // dynamic from PyPI
    { label: "downloads/m", source: "pypistats_month" }, // dynamic from PyPistats
    { label: "build", value: "hatchling" },           // static value
    { label: "tests" },                               // static single-section
  ],
}
```

### Dynamic badge sources
| Source | Data | Requires |
|---|---|---|
| `github_stars` | stargazers_count | repo |
| `github_forks` | forks_count | repo |
| `github_license` | spdx_id | repo |
| `github_lang` | primary language | repo |
| `github_updated` | last push date | repo |
| `pypi_version` | latest version | `pypi` field |
| `pypi_python` | requires_python | `pypi` field |
| `pypi_license` | license | `pypi` field |
| `pypistats_month` | downloads/month | `pypi` field |
| `pypistats_total` | total downloads | `pypi` field |

Then push to `main` — site updates automatically.

## To-do

### Critical
- [ ] HTTPS — кастомный домен + TLS-сертификат (Let's Encrypt)
- [ ] `SECRET_KEY` вынести в environment variable
- [ ] Разделить `requirements.txt` и `requirements-prod.txt` — django-stubs/mypy не нужны в production

### SEO / видимость
- [ ] `<meta name="description">`, Open Graph, Twitter Card
- [ ] `sitemap.xml`, `robots.txt`
- [ ] `lang="ru"` вместо `lang="en"` (весь контент на русском)
- [ ] Кастомный домен вместо裸 IP

### UX / контент
- [x] ~~Skills cloud: убрать PostgreSQL и Docker~~ → убраны PostgreSQL и DRF, добавлены Jinja2, Bootstrap, opencode-py
- [ ] Контактная форма (или выделить Telegram-ссылку ярче)
- [ ] Секция «Опыт работы» (timeline мест работы)
- [ ] Оставить 2 шрифта вместо 3 (убрать Share Tech Mono)

### Дизайн
Идеи с [21hrs.space](https://www.21hrs.space/) — иммерсивный Apollo 11 сайт (SvelteKit, Three.js, GSAP).

- [ ] **Тёплая цветовая палитра** — заменить чистый белый `#fff` на `#fff3ea` (тёплый офф-вайт), фон терминала на `#1a1a1a` или `#000`. Акцент `#e4b592` (gold) вместо `#6366f1` (indigo).
- [ ] **Career timeline** — горизонтальный таймлайн опыта работы с прогресс-баром, адаптировать их концепцию 0→21hr под карьеру.
- [ ] **Frame corners** — декоративные L-скобки по углам терминала/карточек портфолио. Анимация stroke на hover через SVG `stroke-dashoffset`.
- [ ] **Film grain / blur** — `filter: blur(0.5px)` на текст терминала для мягкого киношного эффекта.
- [ ] **`mix-blend-mode: screen`** — hover-подсветка кнопок и иконок через screen-blend вместо opacity.
- [ ] **Easing** — заменить стандартные CSS transitions на `cubic-bezier(0.61, 1, 0.88, 1)` (ease-out-expo).

**Рекомендация начать:** цветовая палитра → film grain → frame corners. Палитра — база, от неё пляшут все остальные визуальные решения. Timeline — отдельная фича, её можно делать параллельно.

### Код / доступность
- [ ] Тесты на основные view/home page
- [ ] `aria-label` на иконках GitHub/Telegram/Portfolio
- [ ] Начать использовать `requirements-dev.txt` в CI (mypy)

---

## Идеи с sui.io (анализ)

### 1. Hero-заголовок с градиентом под мышкой
Текст «Sergey Kislyakov» — `background-clip: text` + радиальный градиент, центр следует за курсором.

**CSS:**
```css
.hero h1 {
  background-image: radial-gradient(
    circle at var(--mx) var(--my),
    #fff3ea 0%, #fff3ea 40%,
    #e4b592 75%, rgba(228,181,146,0.15) 95%
  );
  background-clip: text;
  -webkit-text-fill-color: transparent;
}
```

**JS:** `mousemove` на `.hero` → обновляет `--mx` и `--my` в процентах. Без библиотек, ~10 строк.

### 2. Gradient blur фон hero
Один слой `backdrop-filter: blur()` с радиальной маской под курсором — тёмный фон «оживает» при движении мыши.

**Реализация:**
```html
<div class="hero-blur"></div>
```
```css
.hero-blur {
  position: absolute; inset: 0;
  backdrop-filter: blur(6px);
  -webkit-mask: radial-gradient(
    circle 200px at var(--mx) var(--my),
    transparent 0%, black 100%
  );
  pointer-events: none;
  z-index: 0;
}
```

### 3. Arrow-swap на иконках (portfolio link-icon)
При ховере одна стрелка уезжает (`→ 200%`), вторая приезжает из `-200% → 0%`.

**Реализация:** два `path` в SVG, у каждого `transform: translateX()` с `transition`. На `:hover` у первого `→ 200%`, у второго `→ 0%`.

### 4. Stagger reveal карточек портфолио
Каждая карточка — не просто `fadeIn`, а заголовок с `overflow: hidden` + `translateY` + `transition-delay` по индексу.

**Рекомендация:** 1 → 2 → 3 → 4 по приоритету. 1+2 дают максимум вау-эффекта за минимум кода.

---

## Идеи с roshan-sahu.com (анализ)

**Сайт:** минималистичный креативный дев — тёмный hero, белый контент, 3D/GSAP эксперименты.

### Что интегрировать (от простого к сложному)

### 1. Текущее время MSK в hero
Добавить `<span class="current-time">17:52 MSK</span>` в hero (под заголовком или рядом с социальными ссылками).

**JS** (~5 строк в `index.html` inline):
```js
function updateTime() {
  document.querySelector('.current-time').textContent =
    new Date().toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' }) + ' MSK';
}
updateTime();
setInterval(updateTime, 30000);
```

**CSS:**
```css
.current-time { font-family: 'Fira Code', monospace; color: #71717a; font-size: 0.85rem; }
```

Приоритет: ★☆☆, займёт 5 мин.

---

### 2. Contact секция (выделить Telegram)
Заменить п. «Контактная форма» на минимальную контактную секцию в `content-body`:
- Иконка/ссылка Telegram (уже есть)
- Email: `s.kislyakov84@gmail.com`
- Без формы — только ссылки

**HTML** — блок после `#portfolio`:
```html
<div id="contact" class="contact hidden">
  <h2>Contact</h2>
  <a href="mailto:s.kislyakov84@gmail.com" class="contact-link">s.kislyakov84@gmail.com</a>
  <a href="https://t.me/kislyakow" class="contact-link">@kislyakow</a>
</div>
```

**JS** — кнопка в `.social-links` (или отдельная nav-ссылка), тоггл как у portfolio/github.

**CSS** — минимально, стиль под existing cards.

Приоритет: ★☆☆

---

### 3. Back to top
Кнопка в правом нижнем углу, появляется при скролле вниз.

**HTML:**
```html
<button id="back-to-top" class="back-to-top hidden" aria-label="Back to top">
  <!-- SVG arrow up -->
</button>
```

**CSS:**
```css
.back-to-top {
  position: fixed; bottom: 2rem; right: 2rem;
  z-index: 100; opacity: 0; pointer-events: none;
  transition: opacity 0.3s var(--ease-expo);
}
.back-to-top.visible { opacity: 1; pointer-events: auto; }
```

**JS** — `scroll` listener → toggle `.visible`; `click` → `window.scrollTo({ top: 0, behavior: 'smooth' })`.

Приоритет: ★☆☆



### 5. Теги карточек портфолио с ролями
Добавить в карточки портфолио метку «Role» (как у Рошана `Role: Web Development`).

**Как:** добавить опциональное поле `role` в объекты `PORTFOLIO` массива. Отображать как badge с префиксом `role:`.

```js
{
  repo: "...",
  role: "Fullstack Development",   // new optional field
  // ...
}
```

В шаблоне карточки:
```js
${project.role ? `<span class="badge badge-role">role: ${project.role}</span>` : ''}
```

**CSS:**
```css
.badge-role { background: #e4b59220; color: #e4b592; border-color: #e4b59240; }
```

Приоритет: ★☆☆

---

### Приоритет выполнения
1. **Time MSK** — быстрый, заметный, стильный
2. **Contact секция** — уже висит в to-do
3. **Back to top** — тривиально, улучшает UX
4. **Role-теги** — мелочь, но завершает карточки

### Что НЕ берём
- Three.js / 3D сцены — нет сборщика
- GSAP — библиотека, не вписывается в zero-dependency
- Webflow / Shopify / Next.js — не релевантно

---

## Идеи с studiomodular.be (анализ)

**Сайт:** бельгийское дизайн-агентство. Минималистичный full-width лендинг с крупной типографикой, карточками кейсов на всю ширину и видеобэкграундом в hero.

### Что интегрировать (от простого к сложному)

### 1. Full-width layout
Убрать `max-width` и боковые паддинги у `.content-body`, растянуть карточки портфолио на всю ширину.

**CSS:**
```css
.content-body {
  max-width: none;
  padding-left: 0;
  padding-right: 0;
}
```

**JS:** у карточек убрать `max-width: 1200px` / маржины, растянуть на 100vw.

Бонус: увеличить секционные отступы (padding-block: 6rem вместо 4rem).

### 2. Hero на всю ширину (уже есть)
`.hero` уже 100vw × 100vh. Внутренний контент `.content-row` — двухколоночный с gap, это наша фишка (терминал + скиллы). Оставляем как есть, только чуть больше padding.

### 3. Крупная типографика
Увеличить `h1` в hero (у нас уже 2.5rem → можно 3rem). Увеличить заголовки секций в `.content-body`.

### 4. Карточки портфолио как кейсы
Вдохновение: у них карточка = медиа (видео/картинка) на весь экран + overlay с названием.
У нас: карточка с текстом/бейджами. Можно сделать фоном карточки скриншот проекта (через `og:image` из GitHub или вручную).

Приоритет: ★☆☆ (долгая история — нужны скриншоты)

### Приоритет выполнения
1. **Full-width + отступы** — 5 мин, даёт 80% эффекта
2. **Крупная типографика** — 5 мин, усиливает визуал
3. **Карточки как кейсы** — когда появятся скриншоты

### Что НЕ берём
- Бургер-меню (на визитке важна видимость ссылок)
- Видеобэкграунд (тяжёлый, нет контента)
- Overlay на карточках (сложно автоматизировать без скриншотов)
