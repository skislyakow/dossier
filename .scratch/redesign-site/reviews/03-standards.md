# Standards review — `c270294...HEAD` (STANDARDS axis)

Sources checked: AGENTS.md, `docs/agents/issue-tracker.md` + `triage-labels.md`, `ruff.toml` (`uv run ruff check .` passes — tooling-enforced, skipped), GLOSSARY.md.

## (a) Documented-standard violations — HARD

1. **`triage-labels.md` / `issue-tracker.md` — non-canonical `Status` value.** Ticket 02 was set to `Status: done`, but the tracker only documented the five triage roles (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`) — no completion state.
   → **Fixed:** documented `Status: done` as the terminal state in `docs/agents/issue-tracker.md` (Conventions) in the same change.

No other hard breaches: docs-sync (Dev workflow step 6) honored (AGENTS.md `## Project overview` + README updated); token/`color-mix` rules respected; `prefers-reduced-motion → animation: none` guard present; aria-labels preserved.

## (b) Baseline smells — JUDGEMENT CALLS

1. **Duplicated Code (sanctioned)** — two byte-identical `.marquee-group` blocks in `templates/index.html`. Inherent to the seamless `translateX(-50%)` loop; AGENTS.md now documents the two-group shape. → **Accepted as-is.**
2. **Duplicated Code / Shotgun Surgery** — the accent hover pair (`background: var(--accent-soft)`, `color: var(--accent)`) recurs across `.social-link:hover`, `.hero .social-link:hover`, `.telegram-link:hover`, `.portfolio-link:hover`, and the `.hero .*:hover` group. → **Accepted as-is:** the selectors sit at equal specificity and depend on source order; consolidating them blind (no browser here) risks regressions for little gain, matching the t02 precedent of accepting a duplicated reduced-motion guard.
3. **Minor duplication** — `text-transform: uppercase; letter-spacing: 0.12em;` in both `.social-label` and `.marquee-item`. → **Accepted as-is** (two independent components).
4. **Weak/brittle tests** — `test_page_chrome_marquee` pinned the exact animation duration and left `aria-hidden="true"` unscoped.
   → **Fixed:** duration assertion loosened to `animation: marquee`; `aria-hidden` scoped to `<div class="marquee" aria-hidden="true">`.

No Speculative Generality. No ruff-relevant issues.
