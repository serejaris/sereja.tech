# STATUS.md

## Current phase

`Issue #102 GSC canonical backlog rollout`

## Done

- [x] Execution pack created for this repo and task.
- [x] Verified issue and board context for `#32`, `#33`, `#34`, and `#66`.
- [x] Verified repo reality for homepage, about page, SEO templates, Hugo, and Python.
- [x] M1 helper artifacts created and validated.
- [x] M2 ghost URL policy finalized and validated.
- [x] M3 canonical, robots, and sitemap hygiene completed and validated.
- [x] M4 discoverability and donor-link work completed and validated.
- [x] M5 search-fit tuning for Batch A completed and smoke-tested.
- [x] M6 search-fit tuning for Batch B completed and smoke-tested.
- [x] M7 final validation, smoke checks, and GitHub sync completed.
- [x] GitHub project `4` synced with follow-up issues `#69`, `#70`, and `#71`.
- [x] M8 production deployment and live smoke completed.
- [x] M9 GSC inspection and request indexing completed.
- [x] M10 canonical coverage KPI refresh completed.
- [x] Live analytics snapshot captured for GSC, PostHog, and Vercel on `2026-04-30`.
- [x] Blog analytics blind spots reduced with CTA click, UTM/referrer, and code-copy tracking.
- [x] First-pass content repack completed for five low-completion articles.
- [x] Repo-local analytics pipeline documented and validated.
- [x] Analytics run `2026-05-05` generated 6 action tasks and GitHub issue `#97`.
- [x] Issue `#98` redirect source cleanup completed locally: slashless internal blog links normalized, old alias links removed from maintained `llms` sources, and `check-redirect-sources` added.
- [x] Issue `#98` GSC reason-by-reason browser audit completed; `Page with redirect` and the crawlable-looking `/blog/{slug}` 404 are covered by PR `#99`, while `Crawled`, `Duplicate`, and `Discovered` remain separate post-merge work.
- [x] Issue `#98` post-merge production smoke found the malformed `/blog/data-layer-for-agents/)` redirect still falling through to 404; follow-up guardrail now requires the Vercel trailing-slash source variant that production actually matches.
- [x] Issue `#98` shipped through the Git-connected Vercel path via PR `#99` and follow-up PR `#100`; production smoke is green and GSC `Page with redirect` validation started on `2026-05-07`.
- [x] Issue `#102` GSC inventory captured for `Crawled`, `Duplicate`, and `Discovered` rows from the `2026-05-03` GSC report.
- [x] Issue `#102` local classifier and conservative donor-link fixes completed; `classify-gsc-backlog` now reports `low_donor_routes=0`.

## In progress

- [ ] Monitor new analytics events after deployment.
- [ ] Work through GitHub issue `#97` before the next analytics run creates new tasks.
- [ ] Ship issue `#102` through Git-connected Vercel, smoke production, then start GSC validation/request indexing.

## Next

1. Merge issue `#102` only through a PR / Git-connected Vercel path; do not use local `vercel deploy`.
2. After production deploy, smoke changed URLs and sitemap, then start GSC validation for `Crawled` and `Duplicate`.
3. Inspect `/blog/remotion-programmatic-video-vibecoding/` and request indexing, or record the existing GSC state if request indexing is unavailable.
4. Re-check GSC `Page with redirect` on `2026-05-11`, `2026-05-14`, and `2026-05-21`; host/protocol redirects may remain.
5. Use `python3 scripts/analytics/site_review.py research/analytics-runs/YYYY-MM-DD.json` for the next analytics run, then revisit issue `#97` before creating new tasks.
6. Keep issue `#35` separate from the GSC rollout track.

## Decisions made

- The goal is canonical blog index coverage, not raw indexed URL count.
- The working KPI is `indexed canonical blog slugs / eligible canonical blog slugs`.
- The execution order is:
  1. drift,
  2. canonical stack,
  3. discoverability,
  4. search-fit tuning.
- Trailing-slash canonical policy stays in place.
- Taxonomy and term pages stay `noindex, follow`.
- Board and issue sync is best-effort and never blocks repo work.
- CTR optimization is intentionally deferred until after indexation fundamentals.
- `context.md` is now the local PRD for this run because the pack referenced it and the file did not exist.
- `subagent-model-cost` is restored from git history instead of redirected because source exists and the URL has meaningful traffic.
- `remotion-programmatic-video-vibecoding` is restored from git history instead of redirected because source exists and the URL already has live traffic.
- `/blog/hooks`, `/blog/personal-corporation-agents-scheduler`, and `/blog/skills` resolve to `410/404` policy because git history did not prove a single safe successor and traffic is negligible.
- Clear aliases are redirected via `vercel.json`: `/blog/llms.txt`, `/blog/data-layer`, `/blog/github-projects-ai-memory`, `/blog/sync-claude-code`, `/blog/superpowers`, and malformed `/blog/data-layer-for-agents/)`.
- Restored `remotion-programmatic-video-vibecoding` intentionally drops the missing `image` frontmatter to avoid a broken OG asset path.
- `static/robots.txt` is removed; `layouts/robots.txt` is the single maintained source of truth.
- Canonical and target-link helper checks now ignore stale `public/` leftovers and operate on current canonical routes only.
- Homepage and `/blog/` now expose explicit curated routes to all Batch A and Batch B targets.
- Preferred donor pages now include additional contextual links to `github-projects-ai-agent-memory`, `agent-teams-opus-4-6`, `homebrew-cli-vibecoding`, `chrome-devtools-mcp-setup`, and `claude-code-token-optimization`.
- Batch A titles and openings now name the problem and outcome in the first screen without changing slugs or voice.
- Batch B titles, descriptions, openings, and headings are now explicit about the tool, problem, and expected outcome without slug changes.
- Final local validation is green across build, ghost policy, canonical, sitemap, target-link, and smoke checks.
- Issue `#66` now has a completion note with local results and post-deploy follow-up items.
- GitHub Project `4` is the current mirror for follow-up status on this SEO track.
- Issues `#32` and `#33` were moved to `In review` because implementation is complete locally and the remaining work is production and GSC verification.
- Issue `#66` was moved to `Done` on Project `4`; new follow-up issues are `#69`, `#70`, and `#71`.
- Superseded on `2026-05-07`: production deploys must use the Git-connected Vercel path; do not deploy this repo from the local working tree with Vercel CLI.
- Production rollout exposed a Vercel-specific redirect ordering quirk: slash normalization runs before the custom redirect on path-like aliases, so slash variants must also be declared in `vercel.json`.
- After the second production deploy, restored pages, alias redirects, sitemap, and canonical checks all matched the intended policy on `https://sereja.tech`.
- On `2026-03-13`, GSC inspection for all 5 priority pages still showed `URL is not on Google` with `Discovered - currently not indexed`, `Last crawl: N/A`, and canonical fields `N/A`.
- Request indexing was submitted on `2026-03-13` for all 5 priority pages from issue `#70`.
- On `2026-04-30`, M10 measured `73/100` indexed canonical blog slugs (`73.0%`) by intersecting local canonical slash URLs with the GSC indexed-pages export.
- The inferred issue `#32` baseline was `30/91` indexed pages (`33.0%`), so canonical coverage improved materially after the rollout.
- Batch A is fully indexed; Batch B has `homebrew-cli-vibecoding` and `chrome-devtools-mcp-setup` indexed, while `claude-code-token-optimization` is still absent from indexed examples.
- Restored `subagent-model-cost` is indexed; restored `remotion-programmatic-video-vibecoding` is still absent from indexed examples.
- Fresh analytics snapshot source is `research/analytics-snapshot-2026-04-30.json`.
- Site analytics now uses a repo-local loop: dated JSON snapshot -> generated review -> generated issue body -> GitHub issue with checkboxes -> next run revisits prior checkboxes before creating new tasks.
- The recurring automation prompt is `prompts/analytics-site-run.md`.
- The current analytics parent issue is `#97`, status `Ready` on GitHub Project `4`.
- Issue `#102` uses GSC report date `2026-05-03` as the baseline: `Crawled - currently not indexed` = `74`, `Duplicate, Google chose different canonical than user` = `9`, `Discovered - currently not indexed` = `1`.
- `live.sereja.tech/*` and `ai-corp.sereja.tech/` examples are out of this Hugo repo scope and should be split if they need SEO work.
- GSC URL Inspection for `/blog/document-conversations-not-code/` showed Google-selected canonical `https://sereja.tech/blog/document-conversations-not-code`, so the current duplicate evidence is slash/canonical lag rather than a semantic duplicate.
- Issue `#102` completion means repo fixes shipped, production smoke green, and GSC validation/request indexing started or state recorded; it does not mean waiting for the final GSC pass.

## Assumptions in force

- `hugo build` is the primary repo-native validation command.
- Local smoke uses:
  `hugo server -D --bind 127.0.0.1 --baseURL http://127.0.0.1:1313`
- Python `3.14.2` is available for lightweight helper scripts.
- Hugo `0.154.5` is available locally.
- These short aliases are likely valid redirect targets unless disproven:
  - `/blog/llms.txt` -> `/blog/llms-txt-agent-readable-web/`
  - `/blog/data-layer` -> `/blog/data-layer-for-agents/`
  - `/blog/github-projects-ai-memory` -> `/blog/github-projects-ai-agent-memory/`
  - `/blog/sync-claude-code` -> `/blog/sync-claude-code-four-machines/`
  - `/blog/superpowers` -> `/blog/superpowers-brainstorming-workflow/`
- `subagent-model-cost` and `remotion-programmatic-video-vibecoding` should be inspected for restore-from-history before redirecting.
- Local `_vercel/insights/script.js` 404s during `hugo server` are known local noise and not blockers for this task.
- Production deploy, GSC inspection, and Yandex.Webmaster remain manual or console-backed steps outside the local repo loop.
- Issue `#35` stays separate from the GSC rollout follow-up; do not merge those tracks implicitly.
- Internal links to blog posts must use final canonical slash URLs and must not point at slashless routes or old redirect aliases.
- `check-redirect-sources` is now part of the regular SEO helper stack and must stay green before GSC redirect validation.
- `classify-gsc-backlog` is now part of the issue `#102` helper stack and expects the dated GSC inventory artifact unless a newer inventory is explicitly captured.

## Baseline snapshot

- Repo blog post count: `89`
- Homepage content source: `content/_index.md`
- About page source: `content/about/index.md`
- Blog index source: `content/blog/_index.md`

### Batch A

- `github-projects-ai-agent-memory`
- `agent-teams-opus-4-6`

### Batch B

- `homebrew-cli-vibecoding`
- `chrome-devtools-mcp-setup`
- `claude-code-token-optimization`

### Known ghost URLs from issue #66

- `/blog/subagent-model-cost`
- `/blog/remotion-programmatic-video-vibecoding`
- `/blog/llms.txt`
- `/blog/data-layer`
- `/blog/github-projects-ai-memory`
- `/blog/hooks`
- `/blog/personal-corporation-agents-scheduler`
- `/blog/sync-claude-code`
- `/blog/superpowers`
- `/blog/skills`

### Malformed URL fixtures from issue #66

- `/blog/%20open%20router`
- `/blog/openclaw-vps-6-kimi.com/code/console`
- `/blog/data-layer-for-agents/)`

## Related issue context

- `#32` — indexing snapshot and previously implemented fixes.
- `#33` — list of `Crawled - currently not indexed` posts.
- `#34` — GSC analytics snapshot referenced by backlog work.
- `#66` — popularity snapshot backlog with ghost URL cleanup list.
- `#69` — production rollout and smoke for the indexation pass.
- `#70` — GSC inspection for Batch A and Batch B pages after rollout.
- `#71` — KPI refresh after the GSC recrawl window.

## GitHub follow-up queue

- `#69` — `Done` on Project `4`
- `#70` — `Done` on Project `4`
- `#71` — `Ready` on Project `4`

## Commands to run

### Repo-native commands available now

```bash
hugo build
hugo server -D --bind 127.0.0.1 --baseURL http://127.0.0.1:1313
```

### Commands expected after M1 helper creation

```bash
python3 scripts/seo/url_audit.py summary
python3 scripts/seo/url_audit.py check-ghosts
python3 scripts/seo/url_audit.py check-canonical
python3 scripts/seo/url_audit.py check-sitemap
python3 scripts/seo/url_audit.py check-target-links
python3 scripts/seo/url_audit.py check-redirect-sources
python3 scripts/seo/url_audit.py classify-gsc-backlog research/gsc-live/2026-05-07-gsc-backlog-inventory.json
```

### Useful local smoke checks after the server is running

```bash
curl -s http://127.0.0.1:1313/ > /dev/null
curl -s http://127.0.0.1:1313/blog/ > /dev/null
curl -s http://127.0.0.1:1313/about/ > /dev/null
curl -s http://127.0.0.1:1313/blog/github-projects-ai-agent-memory/ > /dev/null
curl -s http://127.0.0.1:1313/blog/agent-teams-opus-4-6/ > /dev/null
```

## Current blockers

- The KPI refresh in issue `#71` depends on Google recrawling the 5 requested pages after `2026-03-13`; until then, refreshed index-state data would be premature.

## Audit log

| Timestamp | Task finished | Key files changed | Commands run | Result | Next task |
| --- | --- | --- | --- | --- | --- |
| 2026-03-11 08:06 | Execution pack bootstrap | `AGENTS.md`, `context.md`, `docs/*`, `prompts/*` | `gh issue list`; `gh issue view 32`; `gh issue view 33`; `gh issue view 66`; `gh project item-list 4`; `hugo version`; `python3 --version`; `hugo build` | pass | M1 helper creation |
| 2026-03-11 08:06 | M1 helper creation | `scripts/seo/url_policy.json`, `scripts/seo/url_audit.py`, `docs/PLAN.md`, `docs/STATUS.md` | `python3 -m json.tool scripts/seo/url_policy.json > /dev/null`; `python3 scripts/seo/url_audit.py summary`; `python3 scripts/seo/url_audit.py check-ghosts`; `hugo build` | pass | M2 ghost URL policy |
| 2026-03-11 08:06 | M2 ghost URL policy | `content/blog/subagent-model-cost.md`, `content/blog/remotion-programmatic-video-vibecoding.md`, `scripts/seo/url_policy.json`, `vercel.json`, `docs/PLAN.md`, `docs/STATUS.md` | `hugo build`; `python3 scripts/seo/url_audit.py check-ghosts`; `python3 scripts/seo/url_audit.py summary`; `python3 -m json.tool vercel.json > /dev/null` | pass | M3 canonical hygiene |
| 2026-03-11 08:06 | M3 canonical hygiene | `scripts/seo/url_audit.py`, `static/robots.txt`, `docs/PLAN.md`, `docs/STATUS.md` | `hugo build`; `python3 scripts/seo/url_audit.py check-canonical`; `python3 scripts/seo/url_audit.py check-sitemap`; `rg 'href=\"/blog/[^\"/?#]+\"' public/index.html public/blog/index.html public/about/index.html layouts -g '*.html'` | pass | M4 discoverability |
| 2026-03-11 08:06 | M4 discoverability | `layouts/index.html`, `layouts/blog/list.html`, `content/blog/github-issues-project-context.md`, `content/blog/openclaw-hooks-automation.md`, `content/blog/openclaw-vps-6-dollars.md`, `docs/PLAN.md`, `docs/STATUS.md` | `hugo build`; `python3 scripts/seo/url_audit.py check-target-links`; `rg 'GitHub Projects как память для AI-агента|Agent Teams в Claude Code|Homebrew для вайбкодинга|Chrome DevTools MCP: настройка с живым браузером|Как перестать сжигать контекст Claude Code впустую' public/index.html public/blog/index.html` | pass | M5 search-fit |
| 2026-03-11 08:06 | M5 search-fit Batch A | `content/blog/github-projects-ai-agent-memory.md`, `content/blog/agent-teams-opus-4-6.md`, `docs/PLAN.md`, `docs/STATUS.md` | `hugo build`; `hugo server -D --bind 127.0.0.1 --baseURL http://127.0.0.1:1313`; `curl -s http://127.0.0.1:1313/blog/github-projects-ai-agent-memory/`; `curl -s http://127.0.0.1:1313/blog/agent-teams-opus-4-6/` | pass | M6 search-fit |
| 2026-03-11 08:26 | M6 search-fit Batch B | `content/blog/homebrew-cli-vibecoding.md`, `content/blog/chrome-devtools-mcp-setup.md`, `content/blog/claude-code-token-optimization.md`, `docs/PLAN.md`, `docs/STATUS.md` | `hugo build`; `hugo server -D --bind 127.0.0.1 --baseURL http://127.0.0.1:1313`; `curl -s http://127.0.0.1:1313/blog/homebrew-cli-vibecoding/`; `curl -s http://127.0.0.1:1313/blog/chrome-devtools-mcp-setup/`; `curl -s http://127.0.0.1:1313/blog/claude-code-token-optimization/` | pass | M7 final validation |
| 2026-03-11 08:26 | M7 final validation and handoff | `docs/PLAN.md`, `docs/STATUS.md` | `hugo build`; `python3 scripts/seo/url_audit.py summary`; `python3 scripts/seo/url_audit.py check-ghosts`; `python3 scripts/seo/url_audit.py check-canonical`; `python3 scripts/seo/url_audit.py check-sitemap`; `python3 scripts/seo/url_audit.py check-target-links`; `hugo server -D --bind 127.0.0.1 --baseURL http://127.0.0.1:1313`; `curl -s http://127.0.0.1:1313/`; `curl -s http://127.0.0.1:1313/blog/`; `curl -s http://127.0.0.1:1313/about/`; `curl -s http://127.0.0.1:1313/blog/github-projects-ai-agent-memory/`; `curl -s http://127.0.0.1:1313/blog/agent-teams-opus-4-6/`; `curl -s http://127.0.0.1:1313/blog/homebrew-cli-vibecoding/`; `curl -s http://127.0.0.1:1313/blog/chrome-devtools-mcp-setup/`; `curl -s http://127.0.0.1:1313/blog/claude-code-token-optimization/`; `gh repo view serejaris/sereja.tech --json nameWithOwner,url`; `gh project view 4 --owner serejaris --format json --jq '{id, number, title}'`; `gh issue comment 66 --repo serejaris/sereja.tech --body ...` | pass | post-deploy manual checks |
| 2026-03-13 05:45 | GitHub sync and post-deploy planning | `docs/PLAN.md`, `docs/STATUS.md` | `gh issue list --repo serejaris/sereja.tech`; `gh project item-list 4 --owner serejaris`; `gh project field-list 4 --owner serejaris`; `gh issue create ...` -> `#69`, `#70`, `#71`; `gh project item-add 4 --owner serejaris --url ...`; `gh project item-edit ...`; `gh issue comment 32 --repo serejaris/sereja.tech --body ...`; `gh issue comment 33 --repo serejaris/sereja.tech --body ...` | pass | M8 rollout and production smoke |
| 2026-03-13 05:52 | M8 rollout and production smoke | `vercel.json`, `scripts/seo/url_audit.py`, `.gitignore`, `docs/PLAN.md`, `docs/STATUS.md` | `vercel link --yes --project sereja-tech --scope riiiis-projects-773f996a`; `vercel deploy --prod --yes --scope riiiis-projects-773f996a --logs`; `curl -I https://sereja.tech/...`; `curl -IL https://sereja.tech/blog/github-projects-ai-memory`; `curl -IL https://sereja.tech/blog/data-layer`; `curl -IL https://sereja.tech/blog/sync-claude-code`; `curl -IL https://sereja.tech/blog/superpowers`; `curl -IL 'https://sereja.tech/blog/data-layer-for-agents/)'`; `curl -s https://sereja.tech/sitemap.xml`; `gh issue comment 69 --repo serejaris/sereja.tech --body ...`; `gh issue close 69 --repo serejaris/sereja.tech --reason completed`; `gh project item-edit ...` | pass after 1 deploy-fix loop | M9 GSC inspection |
| 2026-03-13 06:05 | M9 GSC inspection and request indexing | `docs/PLAN.md`, `docs/STATUS.md` | `Chrome DevTools MCP`; URL Inspection for 5 priority pages in GSC; request indexing for all 5 priority pages; `gh issue comment 70 --repo serejaris/sereja.tech --body ...`; `gh issue close 70 --repo serejaris/sereja.tech --reason completed`; `gh issue comment 71 --repo serejaris/sereja.tech --body ...`; `gh project item-edit ...` | pass | M10 KPI refresh after recrawl window |
| 2026-04-30 02:53 UTC | M10 KPI refresh, analytics events, and content repack | `research/analytics-snapshot-2026-04-30.json`, `static/analytics.js`, `scripts/seo/check_analytics_events.py`, five `content/blog/*.md`, `vercel.json`, `docs/PLAN.md`, `docs/STATUS.md` | Chrome CDP live GSC/PostHog/Vercel reads; `hugo build`; `python3 scripts/seo/url_audit.py summary`; `python3 scripts/seo/url_audit.py check-ghosts`; `python3 scripts/seo/url_audit.py check-canonical`; `python3 scripts/seo/url_audit.py check-sitemap`; `python3 scripts/seo/url_audit.py check-target-links`; `python3 scripts/seo/check_analytics_events.py`; `node --check static/analytics.js`; `hugo server -D --bind 127.0.0.1 --baseURL http://127.0.0.1:1313`; local `curl` smoke; GitHub issue `#71` comment/close/project sync | pass | monitor deployed analytics events |
| 2026-05-05 | Analytics pipeline bootstrap | `docs/analytics-pipeline.md`, `prompts/analytics-site-run.md`, `scripts/analytics/site_review.py`, `scripts/analytics/check_site_review.py`, `research/analytics-runs/2026-05-03.json`, `research/analytics-runs/2026-05-04.json`, `research/analytics-runs/2026-05-05.json`, `research/analytics-runs/2026-05-05-review.json`, `research/analytics-runs/2026-05-05-review.md`, `research/analytics-runs/2026-05-05-issue.md`, `docs/STATUS.md` | `python3 scripts/analytics/site_review.py research/analytics-runs/2026-05-05.json`; `python3 scripts/analytics/site_review.py research/analytics-runs/2026-05-05.json --check`; `python3 scripts/analytics/check_site_review.py`; `python3 -m py_compile scripts/analytics/site_review.py scripts/analytics/check_site_review.py`; `python3 -m json.tool research/analytics-runs/2026-05-03.json`; `python3 -m json.tool research/analytics-runs/2026-05-04.json`; `python3 -m json.tool research/analytics-runs/2026-05-05.json`; `hugo build`; `gh issue create ...` -> `#97`; `gh project item-add 4 --owner serejaris --url ...`; `gh project item-edit ...` | pass | work issue `#97`; next analytics run must revisit prior checkboxes |
| 2026-05-07 | GSC redirect diagnosis and guardrail sync | `AGENTS.md`, `docs/STATUS.md`, `research/gsc-live/*`, GitHub issue `#98` | Live GSC Page indexing drilldown; `curl` redirect diagnosis; source leak scan; `python3 scripts/seo/url_audit.py summary`; `python3 scripts/seo/url_audit.py check-ghosts`; `python3 scripts/seo/url_audit.py check-canonical`; `python3 scripts/seo/url_audit.py check-sitemap`; `python3 scripts/seo/url_audit.py check-target-links` | pass for existing local helpers; redirect source leaks confirmed separately | normalize redirect source leaks, add a permanent helper check, then validate in GSC |
| 2026-05-07 | M12 GSC redirect source cleanup | `content/blog/*.md`, `static/llms-full.txt`, `scripts/seo/url_audit.py`, `AGENTS.md`, `docs/PLAN.md`, `docs/TEST_PLAN.md`, `docs/STATUS.md` | `hugo build`; `python3 scripts/seo/url_audit.py summary`; `python3 scripts/seo/url_audit.py check-ghosts`; `python3 scripts/seo/url_audit.py check-canonical`; `python3 scripts/seo/url_audit.py check-sitemap`; `python3 scripts/seo/url_audit.py check-target-links`; `python3 scripts/seo/url_audit.py check-redirect-sources`; `python3 -m py_compile scripts/seo/url_audit.py` | pass | sync issue `#98`, then ship via Git-connected deploy path |
| 2026-05-07 | GSC reason-by-reason browser audit | `research/gsc-live/2026-05-07-reason-by-reason-audit.md`, `content/blog/blog-post-pipeline.md`, `scripts/seo/url_audit.py`, `docs/STATUS.md` | Chrome DevTools browser snapshots for all 7 GSC Page indexing reasons; `hugo build`; `python3 scripts/seo/url_audit.py summary`; `python3 scripts/seo/url_audit.py check-ghosts`; `python3 scripts/seo/url_audit.py check-canonical`; `python3 scripts/seo/url_audit.py check-sitemap`; `python3 scripts/seo/url_audit.py check-target-links`; `python3 scripts/seo/url_audit.py check-redirect-sources`; `python3 -m py_compile scripts/seo/url_audit.py`; `git diff --check` | pass | update PR `#99`; merge before GSC validation |
| 2026-05-07 | Post-merge malformed redirect repair | `vercel.json`, `scripts/seo/url_audit.py`, `docs/STATUS.md` | `curl -sIL 'https://sereja.tech/blog/data-layer-for-agents/)'`; `hugo build`; `python3 scripts/seo/url_audit.py summary`; `python3 scripts/seo/url_audit.py check-ghosts`; `python3 scripts/seo/url_audit.py check-canonical`; `python3 scripts/seo/url_audit.py check-sitemap`; `python3 scripts/seo/url_audit.py check-target-links`; `python3 scripts/seo/url_audit.py check-redirect-sources`; `python3 -m py_compile scripts/seo/url_audit.py`; `git diff --check` | pass locally; shipped via PR `#100` | run production smoke before GSC validation |
| 2026-05-07 | Production smoke and GSC validation start | GitHub PRs `#99` and `#100`, GSC Page indexing report | `gh pr merge 99`; `gh pr merge 100`; Git-connected Vercel checks on `main`; `curl -sL 'https://sereja.tech/blog/blog-post-pipeline/?codex_check=8693c8c'`; `curl -sIL 'https://sereja.tech/blog/data-layer-for-agents/)?codex_check=8693c8c'`; `curl -sI 'https://sereja.tech/blog/telegram-api-vs-json-export?codex_check=8693c8c'`; `curl -sL 'https://sereja.tech/sitemap.xml?codex_check=8693c8c'`; Chrome DevTools MCP click on GSC `VALIDATE FIX` | pass; GSC shows `Validation started`, started `5/7/26` | monitor GSC validation and continue separate canonical backlog |
| 2026-05-07 | M13 GSC canonical backlog classification and conservative fixes | `research/gsc-live/2026-05-07-gsc-backlog-*`, `scripts/seo/url_audit.py`, selected `content/blog/*.md`, `AGENTS.md`, `docs/PLAN.md`, `docs/TEST_PLAN.md`, `docs/STATUS.md` | Chrome DevTools GSC inventory and URL Inspection; `hugo build`; `python3 scripts/seo/url_audit.py classify-gsc-backlog research/gsc-live/2026-05-07-gsc-backlog-inventory.json` | pass locally; `low_donor_routes=0` | ship issue `#102` via Git-connected Vercel path, then production smoke and GSC validation |
| 2026-05-15 12:16 UTC | GSC email interpretation guardrail | `AGENTS.md`, `docs/STATUS.md` | Gmail Search Console email review; live GSC comparison; `hugo build`; `python3 scripts/seo/url_audit.py check-redirect-sources`; `python3 scripts/seo/url_audit.py classify-gsc-backlog research/gsc-live/2026-05-07-gsc-backlog-inventory.json`; `git diff --check` | pass; `redirect-sources-ok`, `low_donor_routes=0` after build | use GSC validation rules before any next indexing fix |

## Blocker log

| Timestamp | Blocker | What was tried | Failing check | Smallest user action needed |
| --- | --- | --- | --- | --- |
| 2026-03-13 05:54 | GSC is not reachable from the current environment | Opened follow-up issue `#70`; attempted browser-backed access via Chrome DevTools MCP | `Could not connect to Chrome. Failed to fetch browser webSocket URL from http://127.0.0.1:9222/json/version` | Run the 5 URL inspections manually in GSC or provide a logged-in browser session for Search Console |
| 2026-03-13 06:05 | Refreshed KPI data is not ready yet | Completed M8 and M9; submitted request indexing for all 5 priority pages | GSC still reports `URL is not on Google`, `Discovered - currently not indexed`, `Last crawl: N/A` immediately after the 2026-03-13 rollout | Wait for the recrawl window, then run issue `#71` |

## Demo and smoke checklist

### Local

- [x] `hugo build` passes
- [x] homepage renders
- [x] `/blog/` renders
- [x] `/about/` renders
- [x] Batch A pages render
- [x] Batch B pages render
- [x] canonical tags on sample posts point to slash URLs
- [x] sitemap is generated
- [x] no known ghost URL is left without policy

### Post-deploy manual

- [x] production slash URL returns `200`
- [x] production non-slash blog URL redirects to slash
- [x] production sitemap does not include ghost URLs
- [x] GSC inspect Batch A pages
- [x] GSC inspect Batch B pages
- [x] request indexing only after deploy and only for changed priority pages

## Board sync notes

- If `gh` is unavailable or unauthenticated, write:
  `board-sync: skipped (<reason>)`
- Do not stop the run for tracker metadata.
- `2026-03-11`: `gh` auth verified, project `4` context verified, and issue `#66` received a completion update comment.
- `2026-03-13`: issues `#69`, `#70`, and `#71` were created and added to Project `4`; issue `#32` and `#33` moved to `In review`, issue `#66` moved to `Done`.
- `2026-03-13`: issue `#69` moved to `Done`; issue `#70` is the next `Ready` follow-up on Project `4`.
- `2026-03-13`: issue `#70` moved to `Done`; issue `#71` is now `Ready` on Project `4`.
