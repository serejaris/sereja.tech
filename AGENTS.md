# sereja.tech Agent Guide

## Purpose and scope

- This repo is a single Hugo blog deployed to Vercel.
- The current execution focus is canonical blog index coverage for `sereja.tech`.
- Work in milestone order from `docs/PLAN.md`; do not expand scope mid-run.

## Canonical paths and task files

- `content/blog/` — canonical blog post source files.
- `content/_index.md` — homepage content.
- `content/about/index.md` — about page content.
- `content/blog/_index.md` — blog index content.
- `layouts/partials/seo.html` — canonical and SEO tags.
- `layouts/sitemap.xml` — sitemap generation.
- `layouts/robots.txt` and `static/robots.txt` — current robots sources to reconcile.
- `vercel.json` — redirect and platform behavior.
- `scripts/seo/` — repo-local SEO audit helpers for this task.
- `docs/PLAN.md`, `docs/STATUS.md`, `docs/TEST_PLAN.md`, `docs/BACKLOG.md` — execution pack state.
- `context.md` — PRD/source of truth for this indexation run.

## Source of truth precedence

1. `docs/PLAN.md` for execution order and milestone boundaries.
2. `context.md` for product intent, KPI, batches, and constraints.
3. Current repo reality in:
   - `content/blog/*.md`
   - `content/_index.md`
   - `content/about/index.md`
   - `content/blog/_index.md`
   - `layouts/partials/seo.html`
   - `layouts/sitemap.xml`
   - `layouts/robots.txt`
   - `static/robots.txt`
   - `hugo.toml`
   - `vercel.json`
4. Verified GitHub context:
   - issue `#32`
   - issue `#33`
   - issue `#34`
   - issue `#66`
   - `docs/board-analysis-2026-02-17.md`
   - `docs/board-analysis-analytics-2026-03-02.md`
5. `docs/STATUS.md` for current assumptions, decisions, and audit log.

If sources conflict:
- use `docs/PLAN.md` for order,
- use repo files for implementation reality,
- use `context.md` for intent,
- record the conflict in `docs/STATUS.md`.

## High-priority operating rules

- Keep diffs scoped to the active milestone only.
- Implement, validate, repair, then continue.
- Do not flip the trailing-slash policy.
- Do not add internal links to slashless blog URLs. Source links must point to
  the final canonical slash URL, for example `/blog/example/`, not
  `/blog/example`.
- Do not link to old redirect aliases when the final canonical post URL is
  known.
- Do not widen the indexable surface accidentally.
- Do not edit `public/` by hand.
- Do not deploy directly from the local working tree with `vercel deploy`, `vercel --prod`, or similar CLI flows.
- Production deploys must happen through the Git-connected repository update path used by Vercel.
- Do not push or merge to `main`.
- Do not block on GitHub board or issue sync.

## Pre-approved scope for this run

- `content/blog/**/*.md`
- `content/_index.md`
- `content/about/index.md`
- `content/blog/_index.md`
- `layouts/**/*.html`
- `hugo.toml`
- `vercel.json`
- `static/robots.txt`
- `layouts/robots.txt`
- `scripts/seo/**`
- `docs/**`
- `prompts/**`
- `context.md`

## Not pre-approved

- Deleting content without explicit restore, redirect, or `410` policy.
- Renaming slugs without an explicit successor and validation.
- Changing analytics behavior in `static/analytics.js`.
- Editing unrelated GitHub Actions.
- Direct Vercel CLI deployments from the local checkout.
- Pushing to remote or merging PRs.

## Dependency order

Always work in this order unless `docs/PLAN.md` narrows the active task:

1. Baseline inventory and helper checks
2. Live/repo drift and ghost URL policy
3. Canonical, robots, and sitemap hygiene
4. Internal discoverability and donor links
5. Search-fit tuning for Batch A
6. Search-fit tuning for Batch B
7. Final validation and handoff

Do not start a later phase while an earlier phase still fails validation.

## Execution loop

For every task:
1. gather only the minimum context required,
2. implement with a scoped diff,
3. run the task validation commands,
4. fix until green,
5. mark the task done in `docs/PLAN.md`,
6. append a concise log entry to `docs/STATUS.md`,
7. continue immediately.

## Scoped-diff policy

- Change only files needed for the current task.
- Avoid opportunistic cleanup.
- Avoid broad content rewrites outside the named target slugs.
- Keep `layouts/`, `hugo.toml`, and `vercel.json` edits surgical and validate immediately.
- If behavior changes, update the matching checks in the same milestone.

## Architecture guardrails

- Hugo + Vercel remains the delivery model.
- Blog canonicals keep the trailing slash policy.
- Internal blog links must use final canonical slash URLs and must not feed
  GSC `Page with redirect` examples.
- Taxonomy and term pages stay `noindex, follow` unless `docs/PLAN.md` says otherwise.
- Only one canonical URL per post.
- Sitemap must contain only intended canonical `200` pages.
- Prefer restore-from-history over redirect when a live-only page has recoverable source.
- Prefer explicit redirects only when the successor is unambiguous.
- Do not treat `llms.txt`, analytics extras, or AI-era experiments as blockers for core indexation work.

## Reasonable assumptions

Proceed without asking when the assumption is local, reversible, and consistent with the repo:

- `context.md` is the PRD for this run.
- `hugo build` is the primary validation command.
- `hugo server -D --bind 127.0.0.1 --baseURL http://127.0.0.1:1313` is the local smoke server.
- Python `3.14.2` is available for lightweight helpers in `scripts/seo/`.
- Hugo `0.154.5` is available locally.
- These redirects are already clear unless disproven during implementation:
  - `/blog/llms.txt` -> `/blog/llms-txt-agent-readable-web/`
  - `/blog/data-layer` -> `/blog/data-layer-for-agents/`
  - `/blog/github-projects-ai-memory` -> `/blog/github-projects-ai-agent-memory/`
  - `/blog/sync-claude-code` -> `/blog/sync-claude-code-four-machines/`
  - `/blog/superpowers` -> `/blog/superpowers-brainstorming-workflow/`
- `subagent-model-cost` and `remotion-programmatic-video-vibecoding` should be checked for restore-from-history before redirecting.
- Local `_vercel/insights/script.js` noise during `hugo server` is not a blocker for this task.

Record every assumption adopted during execution in `docs/STATUS.md`.

## Ask the user only when

Ask only if one of these is true:

1. a secret, credential, or logged-in console is required,
2. a public URL change is irreversible and there is no unambiguous successor,
3. live-only content cannot be recovered and deletion or `410` would remove meaningful traffic with no clear replacement,
4. a deploy is required, because this repo must ship through the Git-connected Vercel path rather than local CLI deployment,
5. a manual production verification step is required,
6. after 3 repair attempts a real blocker remains,
7. the change would be a broad refactor outside the execution pack.

Do not ask for routine confirmation between milestones.

## Stop conditions

Stop only if:
1. all tasks are done,
2. a real blocker remains after 3 repair attempts,
3. a secret, credential, or manual action is required,
4. an irreversible action needs explicit approval.

## Blocker format

When blocked, output only:

- `blocker:` one sentence
- `tried:` concise bullets
- `failing check:` exact command or validation
- `smallest user action:` minimum action required

## Board and issue sync policy

Board sync is best-effort only.

- If `gh` is available and authenticated, sync milestone completion notes to the relevant issue or project item.
- If `gh` fails, is missing, or is unauthenticated:
  - append `board-sync: skipped (<reason>)` to `docs/STATUS.md`
  - continue execution
- Never treat board sync as a blocker for local repo progress.

## Validation commands

- Content, metadata, config, or template change: `hugo build`
- Local smoke: `hugo server -D --bind 127.0.0.1 --baseURL http://127.0.0.1:1313`
- Helper checks after `scripts/seo/` exists:
  - `python3 scripts/seo/url_audit.py summary`
  - `python3 scripts/seo/url_audit.py check-ghosts`
  - `python3 scripts/seo/url_audit.py check-canonical`
  - `python3 scripts/seo/url_audit.py check-sitemap`
  - `python3 scripts/seo/url_audit.py check-target-links`
  - `python3 scripts/seo/url_audit.py check-redirect-sources`

## Execution contract

- Report which files changed and why.
- Report which validations actually ran and which were skipped.
- Keep edits focused; do not clean up unrelated files or user artifacts.
- A task is done only when implementation exists, validations pass, `docs/PLAN.md` is updated, `docs/STATUS.md` is updated, and the repo is resumable.
- New `AGENTS.md` rules apply on the next Codex run or session.
