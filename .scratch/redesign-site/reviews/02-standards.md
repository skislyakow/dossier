# Standards review — `9bc3da6` (STANDARDS axis)

Sources checked: AGENTS.md, ruff.toml (E4,E7,E9,F — `uv run ruff check .` passes, skipped below), GLOSSARY.md, docs/agents/*.md, docs/adr/ (empty).

## (a) Documented-standard violations — HARD

1. **AGENTS.md → Dev workflow, step 6 («Синхронизация доков… обновить README и AGENTS.md»)** — site behavior changed (dark default, hero left-aligned + positioning line, scroll-reveal) but `AGENTS.md ## Project overview` was not updated in this commit; it still claims:
   - "Light/dark theme toggle (GitHub-style light theme, **default**)" — now dark is default (`templates/index.html:2`: `<html lang="ru">`).
   - "Hero: **centered** name + title gradient following cursor" — now left-aligned (`style.css`: `text-align: left`, `align-items: flex-start`) plus a new positioning paragraph and reveal animation.

   README stays accurate enough ("GitHub-style light + dark" doesn't claim a default), but the feature inventory that step 6 points at lives in AGENTS.md and is stale.

No other documented-standard breaches: ruff clean; glossary vocabulary respected (`test_hero_signature_markup` matches **Signature-момент**; no avoided synonyms like «флишка»/«таймлайн»); no ADRs to conflict with.

## (b) Baseline smells — JUDGEMENT CALLS

1. **Duplicated Code** — `templates/index.html`, two IIFEs in the diff:
   `if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;` (hero mousemove) and the same matchMedia call in the new reveal script. → extract one `prefersReducedMotion()` helper.

2. **Duplicated Code → bordering on Shotgun Surgery** — `static/css/style.css` `:root` comment promises «правится одним токеном», but the migration is incomplete, so an accent change still touches many rules:
   - lime hardcoded a second time: `radial-gradient(... rgba(205, 255, 80, 0.05) ...)` (`.hero`) instead of a token;
   - old warm accent `#e4b592` remains in ~50 rules; diff hunk mixes new and old in the same rule: `.contact-item:hover { background: var(--accent-soft); color: #e4b592; }`;
   - `--border: #e4e4e7` exists, yet `.gh-card` keeps literal `border: 1px solid #e4e4e7` while its own `:hover` uses `var(--border)`; `.gh-card:hover { background: #fafafa }` literal beside `var(--bg-card)`.

3. **Extra (not a listed smell): brittle test coupling** — `main/tests.py` substring-asserts exact CSS formatting (`assertIn('--accent: #CDFF50', self.css)`); a harmless reformat (`#cdff50`, extra space) fails a working site. Prefer pattern/regex assertions.

No Speculative Generality: every new token (`--type-scale-*`, `--accent-ring`, `--text-muted`) is referenced.
