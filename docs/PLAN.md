# PLAN.md

Status key:
- `[ ]` not started
- `[~]` in progress
- `[x]` done

## Objective

Increase index coverage of canonical blog posts for `sereja.tech` by fixing the fundamentals in dependency order:

1. baseline visibility,
2. URL policy and live/repo drift,
3. canonical signals,
4. internal discoverability,
5. targeted search-fit tuning.

## Global architecture guardrails

- Keep Hugo + Vercel.
- Keep trailing-slash canonicals for blog posts.
- Keep taxonomy and term pages `noindex, follow`.
- Do not widen the indexable surface accidentally.
- Do not rename slugs unless an explicit redirect or restore policy exists.
- Prefer restore-from-history over redirect when a live page still has traffic.
- Prefer explicit, inspectable checks over manual guesswork.
- Do not continue past a milestone with failing validations.

## Global stop-and-fix rule

If any milestone validation fails:
1. stop new implementation,
2. repair only the failing area,
3. rerun the same validation,
4. continue only when green.

---

## M1 — Baseline inventory and helper checks

Status: `[x]`

### Goal

Create inspectable local checks so later SEO changes can be validated without guesswork.

### Tasks

- [x] Create `scripts/seo/url_policy.json` with:
  - priority batches,
  - known ghost URLs from `context.md`,
  - malformed URL fixtures,
  - expected canonical policy (`trailing_slash`),
  - alias mappings that are already unambiguous.
- [x] Create `scripts/seo/url_audit.py` with at least these subcommands:
  - `summary`
  - `check-ghosts`
  - `check-canonical`
  - `check-sitemap`
  - `check-target-links`
- [x] Record the initial baseline in `docs/STATUS.md`:
  - repo post count,
  - Batch A and Batch B slugs,
  - ghost URL list,
  - known validation commands.
- [x] Keep this milestone repo-internal only; do not change public behavior yet.

### Definition of done

- `scripts/seo/url_policy.json` exists and parses.
- `scripts/seo/url_audit.py summary` runs.
- `docs/STATUS.md` contains the baseline snapshot.
- No public behavior changes yet.

### Validation commands

```bash
hugo build
python3 scripts/seo/url_audit.py summary
python3 scripts/seo/url_audit.py check-ghosts
```

### Known risks

- Frontmatter parsing may need one repair pass.
- Ghost URL normalization may need slash handling.
- Helper expectations may need adjustment once real template output is inspected.

### Milestone guardrails

- No redirect changes yet.
- No homepage or blog UX changes yet.
- No content rewrites yet.

### Stop-and-fix rule

If repo parsing fails, fix the helper first before moving to M2.

---

## M2 — Live/repo drift policy and ghost URL remediation

Status: `[x]`

### Goal

Give every known live-only or stale public URL an explicit fate before canonical cleanup.

### Tasks

- [x] Search git history for recoverable source for:
  - `subagent-model-cost`
  - `remotion-programmatic-video-vibecoding`
- [x] For each known ghost URL, choose exactly one policy:
  - `restore`
  - `redirect`
  - `410_or_404`
- [x] Implement explicit redirect mappings only for already-clear aliases:
  - `/blog/llms.txt` -> `/blog/llms-txt-agent-readable-web/`
  - `/blog/data-layer` -> `/blog/data-layer-for-agents/`
  - `/blog/github-projects-ai-memory` -> `/blog/github-projects-ai-agent-memory/`
  - `/blog/sync-claude-code` -> `/blog/sync-claude-code-four-machines/`
  - `/blog/superpowers` -> `/blog/superpowers-brainstorming-workflow/`
- [x] Resolve these only after successor verification:
  - `/blog/hooks`
  - `/blog/personal-corporation-agents-scheduler`
  - `/blog/skills`
- [x] Classify malformed garbage URLs from `context.md` as redirectable, ignorable, or `410`.
- [x] Record final URL policy decisions in `docs/STATUS.md`.

### Definition of done

- Every ghost URL from `context.md` has an explicit policy.
- Clear aliases are implemented.
- Recoverable live-only pages are restored if appropriate.
- No ambiguous ghost URL is left undocumented.

### Validation commands

```bash
hugo build
python3 scripts/seo/url_audit.py check-ghosts
python3 -m json.tool vercel.json > /dev/null
```

### Known risks

- Some live URLs may have traffic but no recoverable source.
- Redirecting to the wrong successor wastes signal.
- `vercel.json` changes can have broader impact if not kept surgical.

### Milestone guardrails

- Do not delete a live URL with traffic unless policy is explicit.
- Do not guess the successor for ambiguous URLs.
- Keep redirect rules minimal and inspectable.

### Stop-and-fix rule

If a ghost URL cannot be mapped unambiguously after history inspection, stop and raise a blocker instead of inventing a target.

---

## M3 — Canonical, robots, and sitemap hygiene

Status: `[x]`

### Goal

Make the repo emit one clear canonical signal stack for each indexable page.

### Tasks

- [x] Consolidate robots source of truth:
  - keep exactly one maintained source,
  - remove duplication or drift between `layouts/robots.txt` and `static/robots.txt`.
- [x] Keep the trailing-slash policy unchanged and explicit.
- [x] Normalize template-generated internal links to canonical slash URLs where templates control output.
- [x] Verify `layouts/partials/seo.html` canonical behavior remains `.Permalink`-based.
- [x] Ensure sitemap contains only intended canonical `200` pages:
  - home
  - about
  - canonical blog posts
- [x] Ensure taxonomy and term pages stay out of sitemap and remain `noindex, follow`.

### Definition of done

- One robots source of truth remains.
- Canonical pages render with slash canonicals.
- Sitemap contains no stale, alternate, or noindex URLs.
- No trailing-slash strategy flip occurred.

### Validation commands

```bash
hugo build
python3 scripts/seo/url_audit.py check-canonical
python3 scripts/seo/url_audit.py check-sitemap
```

### Known risks

- Robots duplication may be harmless locally but drift-prone in production.
- Template changes can affect more pages than intended.
- Sitemap logic can regress if overly generalized.

### Milestone guardrails

- Keep changes surgical in `layouts/` and config.
- Do not touch unrelated rendering.
- Do not add extra page types to sitemap.

### Stop-and-fix rule

If any rendered canonical points to a non-canonical or redirected URL, fix that before M4.

---

## M4 — Internal discoverability and donor links

Status: `[x]`

### Goal

Increase the chance that priority posts are crawled and prioritized by strengthening internal discovery.

### Batch targets

#### Batch A

- `github-projects-ai-agent-memory`
- `agent-teams-opus-4-6`

#### Batch B

- `homebrew-cli-vibecoding`
- `chrome-devtools-mcp-setup`
- `claude-code-token-optimization`

### Tasks

- [x] Add a compact featured or hub section to the homepage linking core evergreen clusters.
- [x] Improve `/blog/` so it has curated entry points above the raw reverse-chronological list.
- [x] Add donor links from existing strong pages to Batch A and Batch B targets.
- [x] Prefer donor pages that already have visibility or strong cluster fit:
  - `superpowers-brainstorming-workflow`
  - `openclaw-hooks-automation`
  - `claude-code-auto-memory`
  - `github-issues-project-context`
  - `openclaw-vps-6-dollars`
  - `youtube-metadata-relevance-fix`
- [x] Ensure each Batch A and Batch B page has at least `3` donor links from indexable pages.
- [x] Ensure each Batch A and Batch B page is reachable from at least one of:
  - homepage,
  - `/blog/`,
  - a curated hub block.

### Definition of done

- Batch A and Batch B pages are no longer weakly discoverable.
- Homepage and `/blog/` both expose curated entry points.
- `check-target-links` passes for all target slugs.

### Validation commands

```bash
hugo build
python3 scripts/seo/url_audit.py check-target-links
```

### Known risks

- Over-linking can clutter the UI.
- Related-post logic may not surface the intended pages reliably.
- Manual donor links can drift if not kept minimal.

### Milestone guardrails

- Prefer a few strong links over many weak links.
- Use explicit anchor text that names the tool or problem clearly.
- Do not rely on noindex tag pages as the main discovery layer.

### Stop-and-fix rule

If any Batch A or Batch B page still fails `check-target-links`, fix discoverability before M5.

---

## M5 — Search-fit tuning for Batch A

Status: `[x]`

### Goal

Improve the two strongest older candidates that should be indexed first.

### Tasks

- [x] Tune `content/blog/github-projects-ai-agent-memory.md`:
  - sharpen title to tool + problem + outcome,
  - tighten description,
  - tighten the first `120` words,
  - align at least one H2 to likely search language.
- [x] Tune `content/blog/agent-teams-opus-4-6.md` with the same treatment.
- [x] Add or strengthen contextual internal links out of each page to close cluster neighbors.

### Definition of done

- Both pages keep the same slug.
- Titles and descriptions are more explicit for search intent.
- Openings explain the concrete use case quickly.
- Build passes and pages render cleanly.

### Validation commands

```bash
hugo build
hugo server -D --bind 127.0.0.1 --baseURL http://127.0.0.1:1313
```

### Known risks

- Over-optimizing titles can make them worse editorially.
- H2 rewrites can create content drift if too aggressive.
- Opening edits can break tone if they become too SEO-ish.

### Milestone guardrails

- No slug changes.
- No full article rewrites.
- Keep the author voice; improve search-fit clarity only.

### Stop-and-fix rule

If a rewrite weakens clarity or breaks tone, repair the opening or title before moving to M6.

---

## M6 — Search-fit tuning for Batch B

Status: `[x]`

### Goal

Tune the next best search-shaped candidates after Batch A is clean.

### Tasks

- [x] Tune `content/blog/homebrew-cli-vibecoding.md`
- [x] Tune `content/blog/chrome-devtools-mcp-setup.md`
- [x] Tune `content/blog/claude-code-token-optimization.md`

For each page:

- make the title explicit,
- tighten the description,
- improve the first `120` words,
- align one or two headings with likely user phrasing,
- keep the slug unchanged.

### Definition of done

- All three pages have clearer search-fit without slug changes.
- Edits stay scoped to metadata, intro, and targeted headings.
- Build passes.

### Validation commands

```bash
hugo build
hugo server -D --bind 127.0.0.1 --baseURL http://127.0.0.1:1313
```

### Known risks

- Batch B can sprawl into broad copyediting if not contained.
- Some pages may benefit more from discoverability than copy changes.
- Tone drift remains a risk.

### Milestone guardrails

- No article-wide rewrites.
- No taxonomy changes as a shortcut.
- No CTR experiments outside these files.

### Stop-and-fix rule

If the diff grows beyond targeted metadata, intro, and heading changes, stop, trim the diff, and validate again.

---

## M7 — Final validation and handoff

Status: `[x]`

### Goal

Leave the repo in a deploy-ready, inspectable, resumable state.

### Tasks

- [x] Run the full local validation stack.
- [x] Update `docs/STATUS.md` with:
  - what changed,
  - what validations passed,
  - unresolved manual follow-ups,
  - post-deploy checks.
- [x] Best-effort tracker or board sync; do not block on failure.
- [x] Prepare a short manual post-deploy checklist for:
  - production URL spot checks,
  - GSC inspection of Batch A and Batch B pages,
  - request indexing only after deploy.

### Definition of done

- All milestone validations are green.
- `docs/STATUS.md` is current.
- Manual post-deploy follow-ups are listed.
- Repo is left resumable without hidden context.

### Validation commands

```bash
hugo build
python3 scripts/seo/url_audit.py summary
python3 scripts/seo/url_audit.py check-ghosts
python3 scripts/seo/url_audit.py check-canonical
python3 scripts/seo/url_audit.py check-sitemap
python3 scripts/seo/url_audit.py check-target-links
```

### Known risks

- Local checks cannot confirm actual GSC state.
- Production redirect behavior still requires post-deploy verification.
- Board sync may fail if `gh` auth is missing.

### Milestone guardrails

- Do not invent production success metrics.
- Separate local success from post-deploy Search Console follow-up.
- Keep final docs concise and operational.

### Stop-and-fix rule

If any validation command fails, return to the smallest failing scope and repair before declaring handoff-ready.

---

## M8 — Deploy and production smoke

Status: `[x]`

### Goal

Move the validated local diff to production and confirm that live URL behavior matches the intended canonical policy.

### Tasks

- [x] Deploy the validated indexation diff.
- [x] Verify production `200` responses for `/`, `/blog/`, `/about/`, the 5 priority posts, and the 2 restored pages:
  - `/blog/subagent-model-cost/`
  - `/blog/remotion-programmatic-video-vibecoding/`
- [x] Verify non-slash blog URLs redirect to the slash canonical.
- [x] Verify the clear alias redirects still resolve to the intended canonical targets:
  - `/blog/llms.txt`
  - `/blog/data-layer`
  - `/blog/github-projects-ai-memory`
  - `/blog/sync-claude-code`
  - `/blog/superpowers`
- [x] Verify the production sitemap excludes ghost URLs, malformed URLs, and noindex surfaces.
- [x] Record the production smoke result in `docs/STATUS.md` and issue `#69`.

### Definition of done

- Production slash URLs return `200`.
- Non-slash and alias routes resolve to the expected canonical destinations.
- Production sitemap and canonicals match the intended policy.
- Any production-only regression is either fixed or split into a follow-up issue before continuing.

### Validation commands

```bash
curl -I https://sereja.tech/
curl -I https://sereja.tech/blog/
curl -I https://sereja.tech/about/
curl -I https://sereja.tech/blog/github-projects-ai-agent-memory/
curl -I https://sereja.tech/blog/agent-teams-opus-4-6/
curl -I https://sereja.tech/blog/homebrew-cli-vibecoding/
curl -I https://sereja.tech/blog/chrome-devtools-mcp-setup/
curl -I https://sereja.tech/blog/claude-code-token-optimization/
curl -I https://sereja.tech/blog/subagent-model-cost/
curl -I https://sereja.tech/blog/remotion-programmatic-video-vibecoding/
curl -I https://sereja.tech/blog/github-projects-ai-memory
curl -I https://sereja.tech/blog/data-layer
curl -I https://sereja.tech/blog/llms.txt
curl -s https://sereja.tech/sitemap.xml
```

### Known risks

- CDN or deploy propagation can briefly mask the new redirect behavior.
- A Vercel-only config mismatch can pass locally and fail on the live domain.
- Sitemap or canonical mismatches on production should block GSC requests.

### Milestone guardrails

- Do not request indexing before production smoke is green.
- Treat live-domain regressions as higher priority than any new SEO ideas.
- Keep the result inspectable in GitHub and `docs/STATUS.md`.

### Stop-and-fix rule

If any production URL or redirect deviates from the intended policy, stop and fix rollout behavior before M9.

---

## M9 — GSC inspection and request indexing

Status: `[x]`

### Goal

Confirm how Google sees the changed priority pages after rollout and request re-crawl only when production behavior is correct.

### Tasks

- [x] Run URL Inspection in GSC for all 5 priority pages.
- [x] Record the indexing state, Google-selected canonical, last crawl date, and any fetch or render issues.
- [x] Request indexing only for changed priority pages that passed M8.
- [x] Record the outcome in `docs/STATUS.md` and issue `#70`.

### Definition of done

- All 5 priority pages have an inspection result.
- The selected canonical is known for each inspected page.
- Request indexing was sent only after production validation.
- Remaining unknowns are written down without chat-only context.

### Validation commands

```bash
# Manual in Google Search Console:
# inspect the 5 priority URLs and record the result in issue #70
```

### Known risks

- GSC can lag behind production state.
- Search Console access is manual and cannot be validated from the repo.
- A page can be technically correct in production and still remain pending recrawl.

### Milestone guardrails

- Do not mix this step with Yandex.Webmaster work from issue `#35`.
- Do not request indexing for unchanged pages just to inflate activity.
- Capture page-level outcomes, not only a generic summary.

### Stop-and-fix rule

If GSC shows the wrong canonical or fetch issues for a priority page, return to the smallest production or template cause before M10.

---

## M10 — KPI refresh after recrawl window

Status: `[x]`

### Goal

Measure whether canonical index coverage actually improved after the rollout and recrawl window.

### Tasks

- [x] Freeze the current eligible canonical slug count with the local helper.
- [x] Pull refreshed GSC data after the recrawl window.
- [x] Compare indexed canonical slugs against the baseline from issues `#32` and `#33`.
- [x] Break out results for Batch A, Batch B, and the restored pages.
- [x] Record the updated KPI and the next iteration scope in `docs/STATUS.md` and issue `#71`.

### Definition of done

- The KPI `indexed canonical blog slugs / eligible canonical blog slugs` is updated.
- Page-level winners and stuck pages are called out explicitly.
- The next SEO iteration is based on data, not on vague follow-up ideas.

### Validation commands

```bash
python3 scripts/seo/url_audit.py summary
# Manual: compare the refreshed GSC indexed canonical slug count against the baseline from #32 and #33
```

### Known risks

- GSC refresh can lag several days behind the deploy.
- Eligible local slugs can change if new posts land before measurement.
- A small sample of inspected pages can look better than the whole canonical set.

### Milestone guardrails

- Do not declare success from a handful of pages alone.
- Recompute the eligible denominator before interpreting the KPI.
- Keep measurement separate from the next implementation batch.

### Stop-and-fix rule

If the denominator or indexed count is ambiguous, resolve the measurement method before opening a new implementation milestone.

---

## M11 — Self-improving analytics pipeline

Status: `[x]`

### Goal

Make each site analytics run produce a dated snapshot, an actionable diagnosis, and a GitHub-tracked next step.

### Tasks

- [x] Document the analytics run contract in `docs/analytics-pipeline.md`.
- [x] Normalize recent live dashboard captures into `research/analytics-runs/YYYY-MM-DD.json`.
- [x] Add a repo-local generator that converts a snapshot into review JSON, review Markdown, and issue-body Markdown.
- [x] Add validation that every generated run has concrete tasks with evidence and next steps.
- [x] Add a reusable automation prompt for the next recurring run.
- [x] Generate the `2026-05-05` analytics review.
- [x] Create GitHub issue `#97` from the generated issue body and add it to Project `4`.
- [x] Record the result in `docs/STATUS.md`.

### Definition of done

- The next analytics run has a documented command to execute.
- The generated review contains at least one concrete task and no metric-only report.
- Every task has evidence, recommendation, and next step fields.
- The current run is visible in GitHub as a parent issue with checkboxes.
- The issue body tells the next run to revisit previous checkboxes before creating new work.

### Validation commands

```bash
python3 scripts/analytics/site_review.py research/analytics-runs/2026-05-05.json --check
python3 scripts/analytics/check_site_review.py
python3 -m py_compile scripts/analytics/site_review.py scripts/analytics/check_site_review.py
python3 -m json.tool research/analytics-runs/2026-05-03.json
python3 -m json.tool research/analytics-runs/2026-05-04.json
python3 -m json.tool research/analytics-runs/2026-05-05.json
hugo build
```

### Known risks

- Live PostHog still requires a logged-in browser session or API token.
- This is repo-local first; it does not yet configure a GitHub Actions cron.
- Generated tasks are only useful if the next run reads the prior issue before creating more tasks.

### Milestone guardrails

- Do not invent metrics when a dashboard is blocked; record the blocker and use the newest repo snapshot as fallback.
- Keep one parent issue per analytics run.
- Prefer linking to existing issues before creating duplicates.

### Stop-and-fix rule

If a generated review has no concrete tasks, treat the analytics run as failed even if snapshot capture succeeded.

---

## M12 — GSC redirect source cleanup and guardrail

Status: `[x]`

### Goal

Stop feeding Google redirecting blog URLs from repo-maintained sources and make the regression locally detectable.

### Tasks

- [x] Normalize internal markdown links from slashless `/blog/<slug>` URLs to canonical `/blog/<slug>/` URLs.
- [x] Replace repo-maintained links to old redirect aliases with final canonical targets.
- [x] Add `python3 scripts/seo/url_audit.py check-redirect-sources`.
- [x] Add the new helper to the regular validation command list.
- [x] Record the result in `docs/STATUS.md`.

### Definition of done

- Source links no longer point at known redirect aliases.
- Source links to existing blog posts use the canonical trailing-slash route.
- The helper fails on future slashless internal blog links and known alias links.
- Local validation passes.

### Validation commands

```bash
hugo build
python3 scripts/seo/url_audit.py summary
python3 scripts/seo/url_audit.py check-ghosts
python3 scripts/seo/url_audit.py check-canonical
python3 scripts/seo/url_audit.py check-sitemap
python3 scripts/seo/url_audit.py check-target-links
python3 scripts/seo/url_audit.py check-redirect-sources
```

### Known risks

- GSC `Page with redirect` can lag behind production by several days.
- Host and protocol redirects can remain in GSC and are not a source-link failure.
- This milestone fixes redirect hygiene, not the whole `Crawled - currently not indexed` backlog.

### Milestone guardrails

- Do not flip trailing-slash policy.
- Do not remove redirects that protect old public URLs.
- Do not treat redirect cleanup as a replacement for the canonical indexing work.

### Stop-and-fix rule

If `check-redirect-sources` fails, fix the source URL first before changing sitemap, canonical, or redirect policy.

---

## M13 — GSC canonical backlog classification and conservative fixes

Status: `[x]`

### Goal

Work issue `#102` as a controlled SEO iteration for these GSC rows:

- `Crawled - currently not indexed`
- `Duplicate, Google chose different canonical than user`
- `Discovered - currently not indexed`

### Tasks

- [x] Work from a clean worktree based on `origin/main`.
- [x] Capture full GSC inventory for the three rows in `research/gsc-live/2026-05-07-gsc-backlog-inventory.json`.
- [x] Inspect `/blog/document-conversations-not-code/` in GSC and record Google-selected canonical.
- [x] Add `python3 scripts/seo/url_audit.py classify-gsc-backlog`.
- [x] Classify GSC examples by host, route type, local render state, canonical, sitemap membership, `noindex`, and donor count.
- [x] Split `live.sereja.tech` and `ai-corp.sereja.tech` examples out of this Hugo repo scope.
- [x] Add conservative internal donor links for repo-controlled backlog URLs with fewer than 3 unique indexable donor pages.
- [x] Record the audit and final decision table in `research/gsc-live/2026-05-07-gsc-backlog-audit.md`.
- [x] Add the new helper to the regular validation command list.
- [x] Record the result in `docs/STATUS.md`.

### Definition of done

- The GSC inventory is saved as an inspectable artifact.
- Repo-controlled examples pass local technical checks.
- Low-donor repo-controlled backlog routes are no longer below 3 unique donor pages.
- Out-of-scope hosts are not silently fixed in this Hugo repo.
- The next step is Git-connected deploy, production smoke, and GSC validation/request indexing.

### Validation commands

```bash
hugo build
python3 scripts/seo/url_audit.py summary
python3 scripts/seo/url_audit.py check-ghosts
python3 scripts/seo/url_audit.py check-canonical
python3 scripts/seo/url_audit.py check-sitemap
python3 scripts/seo/url_audit.py check-target-links
python3 scripts/seo/url_audit.py check-redirect-sources
python3 scripts/seo/url_audit.py classify-gsc-backlog research/gsc-live/2026-05-07-gsc-backlog-inventory.json
```

### Known risks

- GSC validation can lag for days after a production fix.
- Slashless and host-variant rows can remain in GSC even after repo source cleanup.
- Internal links improve discovery but do not guarantee indexing.
- URL Inspection can show a stale Google-selected canonical until recrawl.

### Milestone guardrails

- Do not deploy with local Vercel CLI.
- Do not push or merge to `main` directly.
- Do not change the trailing-slash canonical policy.
- Do not widen the indexable surface.
- Do not rewrite articles broadly just to satisfy GSC.

### Stop-and-fix rule

If `classify-gsc-backlog` reports a repo-controlled canonical page missing from render output, sitemap, self-canonical, or indexability, fix that technical cause before adding more donor links.
