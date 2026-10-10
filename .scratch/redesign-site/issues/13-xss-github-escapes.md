# 13: XSS — экранирование данных GitHub API в github.js

**What to build:** Блок статистики GitHub (`/api/github/`) вставлялся в `innerHTML` без экранирования — синтетические значения из API могли выполнить инъекцию.

**Status:** done

- [x] Все значения из `/api/github/` обёрнуты в глобальный `esc()`: `user.html_url`, `user.avatar_url`, `user.name`, `user.login`, `user.bio`, `lang`, `percent`
- [x] `esc()` (экранирует `&<>"'`) определён в portfolio.js; github.js исполняет handle по клику — после загрузки обоих скриптов, вызов гарантированно разрешается
- [x] Тест `test_github_stats_escapes`: сырые `${user.*}`, `${lang}`, `${percent}` отсутствуют в github.js, `esc()` применён
- [x] Гейт: 35/35 тестов, ruff, node --check
- [x] AGENTS To-do: XSS-пункт закрыт; `og:image` остался в «SEO / видимость»