# Spec review — `c270294...HEAD` (SPEC axis)

Spec: `.scratch/redesign-site/issues/03-page-chrome-marquee.md`; overall `.scratch/redesign-site/spec.md`.

## Acceptance criteria

- **AC1 (chrome restyle + aria-labels) ✓** — square `2px` frames, hover на `--accent`/`--accent-soft`; aria-labels present (test-gated).
- **AC2 (`/api/github/` contract untouched) ✓** — no view/JS changes; contract already guarded by existing `ApiGithubTest.test_github_stats_without_network`.
- **AC3 (marquee + reduced-motion) ✓ (partial on placement)** — animation + `prefers-reduced-motion { .marquee-track { animation: none } }` present; placement arguable (below).
- **AC4 (tests green / dev check) ✓** — 18/18 OK; dev visual check remains with the human.

## (a) Missing / partial

1. **Placement** — ticket AC3 / spec #14: «marquee-строку технологий **между секциями**». It sits between `.hero` and the single `.content-body` (which wraps *all* sections) — i.e. after Hero / before Projects. → **Accepted:** a literal "between two mid-page sections" spot is unstable because the sections are toggle panels; Hero→body is the one always-visible seam. Documented in the ticket; flagged for the human eye-check.
2. **Content source** — 12-item list is hardcoded in `templates/index.html`, not CMS (spec #15). → **Accepted:** marquee is decorative page chrome (like the hero grid), documented as non-CMS in `## Comments` and AGENTS.md.

## (b) Scope creep

1. `.social-label` `font-size: 0.85rem → 0.75rem` — not requested. → **Reverted** to `0.85rem` (kept the asked-for uppercase + letter-spacing).

## (c) Implemented-but-wrong

1. `.gh-card:hover { background: #fafafa }` left hardcoded → **not a bug:** `--bg-card` is a near-white card in dark too, so `#fafafa` is consistent; only `border-color` was tokenized intentionally.
2. Light theme `--accent: #0969da` → social hovers are blue, not lime → **by design:** single `--accent` token, light palette redesign explicitly deferred to section tickets (t02 decision).
3. `aria-label="Back to top"` was English vs spec #22 «весь текст на русском» → **Fixed:** `aria-label="Наверх"` (+ test updated).
