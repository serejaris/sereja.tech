# TEST_PLAN.md

## Test strategy

This repo is a static Hugo site. The test strategy is therefore layered around:

1. build correctness,
2. rendered HTML correctness,
3. URL-policy correctness,
4. internal discoverability correctness,
5. post-deploy production checks.

The target is not exhaustive testing.
The target is enough verification to improve canonical indexability safely.

---

## Test levels

## L0 — Static repo checks

Purpose:
- catch broken config or malformed helper artifacts before rendering.

Scope:
- `vercel.json` parses
- helper JSON files parse
- helper scripts run

Commands:

```bash
python3 -m json.tool vercel.json > /dev/null
python3 -m json.tool scripts/seo/url_policy.json > /dev/null
python3 scripts/seo/url_audit.py summary
```

Pass condition:

- all commands exit `0`

---

## L1 — Build and render checks

Purpose:

- ensure the site still builds and renders after every SEO change.

Commands:

```bash
hugo build
hugo server -D --bind 127.0.0.1 --baseURL http://127.0.0.1:1313
```

Pass condition:

- `hugo build` exits `0`
- sample routes render locally

Sample local routes:

- `/`
- `/blog/`
- `/about/`
- `/blog/github-projects-ai-agent-memory/`
- `/blog/agent-teams-opus-4-6/`
- `/blog/homebrew-cli-vibecoding/`
- `/blog/chrome-devtools-mcp-setup/`
- `/blog/claude-code-token-optimization/`

Known non-blocking local noise:

- `_vercel/insights/script.js` 404 on local Hugo server

---

## L2 — Canonical stack checks

Purpose:

- verify the repo emits one canonical URL per indexable page.

Checks:

- canonical tag on rendered blog posts uses trailing-slash URL
- no template-generated blog links intentionally point to the no-slash variant
- sitemap contains only intended canonical URLs
- taxonomy URLs are not in sitemap
- taxonomy pages remain `noindex, follow`

Commands:

```bash
python3 scripts/seo/url_audit.py check-canonical
python3 scripts/seo/url_audit.py check-sitemap
```

Pass condition:

- both commands exit `0`

Negative checks:

- canonical must not point to a redirect
- canonical must not point to a non-`200` target
- sitemap must not include:
  - ghost URLs
  - taxonomy URLs
  - noindex pages
  - redirected blog variants

---

## L3 — Ghost URL policy checks

Purpose:

- ensure no known live-only or stale public URL is left ambiguous.

Fixtures:

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
- `/blog/%20open%20router`
- `/blog/openclaw-vps-6-kimi.com/code/console`
- `/blog/data-layer-for-agents/)`

Checks:

- every fixture has explicit policy in `scripts/seo/url_policy.json`
- clear aliases have implemented redirects or restored source
- ambiguous mappings are not silently guessed

Commands:

```bash
python3 scripts/seo/url_audit.py check-ghosts
```

Pass condition:

- command exits `0`

Negative checks:

- no ghost URL may remain in `unknown` state
- no redirect may point to an obviously unrelated article
- no high-traffic ghost URL may be dropped without explicit rationale

---

## L4 — Internal discoverability checks

Purpose:

- make sure priority pages are not weakly linked.

Fixtures:

### Batch A

- `github-projects-ai-agent-memory`
- `agent-teams-opus-4-6`

### Batch B

- `homebrew-cli-vibecoding`
- `chrome-devtools-mcp-setup`
- `claude-code-token-optimization`

Checks:

- each target page has `>= 3` internal donor links from indexable pages
- each target page is reachable from homepage or `/blog/` or a curated hub block
- donor links use explicit anchor text, not vague `here`

Commands:

```bash
python3 scripts/seo/url_audit.py check-target-links
```

Pass condition:

- command exits `0`

Negative checks:

- no target page should remain effectively orphaned
- do not rely on noindex tag pages as the main discovery route
- do not sweep unrelated content just to inflate counts

---

## L4.5 — Redirect source hygiene checks

Purpose:

- prevent repo-maintained links from feeding GSC `Page with redirect` examples.

Checks:

- internal links to existing blog posts use `/blog/<slug>/`
- known redirect aliases are not used as source links
- maintained `llms` surfaces point to final canonical targets

Commands:

```bash
python3 scripts/seo/url_audit.py check-redirect-sources
```

Pass condition:

- command exits `0`

Negative checks:

- no markdown link like `](/blog/example)` for an existing post
- no source link to a known alias such as `/blog/data-layer`
- no static `llms` entry pointing to an old redirected URL

---

## L4.6 — GSC backlog classifier checks

Purpose:

- keep issue `#102` grounded in the live GSC inventory instead of manual guesses.

Fixtures:

- `research/gsc-live/2026-05-07-gsc-backlog-inventory.json`

Checks:

- GSC example counts match the captured row totals
- repo-controlled examples render locally after `hugo build`
- normalized canonical routes have self-canonical tags
- normalized canonical routes are in the sitemap unless they are `/blog/`
- normalized routes are not `noindex`
- repo-controlled canonical/slashless backlog routes have at least 3 unique indexable donor pages
- out-of-scope hosts are classified instead of silently treated as Hugo pages

Commands:

```bash
hugo build
python3 scripts/seo/url_audit.py classify-gsc-backlog research/gsc-live/2026-05-07-gsc-backlog-inventory.json
```

Pass condition:

- command exits `0`
- output includes `low_donor_routes=0`

Negative checks:

- do not use this helper as proof that GSC has reindexed the pages
- do not fix `live.sereja.tech` or sibling hosts inside this Hugo repo
- do not treat slashless examples as content duplicates without URL Inspection evidence

---

## L5 — Search-fit content checks

Purpose:

- ensure targeted copy changes are scoped and query-shaped.

Scope:

- Batch A and Batch B pages only

Checks:

- title remains clear and specific
- description remains clear and specific
- slug unchanged
- opening paragraph names tool, problem, and outcome quickly
- at least one heading reflects likely search wording
- tone is not degraded into keyword stuffing

Primary validation:

```bash
hugo build
```

Manual review checklist:

- [ ] title improved without becoming spammy
- [ ] description improved without becoming generic
- [ ] opening is more concrete
- [ ] no slug changes
- [ ] no accidental full-article rewrite

Negative checks:

- no gratuitous `best`, `ultimate`, or `complete guide` wording unless justified
- no silent slug rename
- no broken frontmatter
- no rewrites outside the named target pages

---

## Fixtures

## Canonical sample pages

- `/blog/telegram-autoposter/`
- `/blog/superpowers-brainstorming-workflow/`
- `/blog/openclaw-vps-6-dollars/`

## Priority indexing pages

- Batch A
- Batch B

## Ghost URLs

- listed in `context.md`, `docs/STATUS.md`, and `scripts/seo/url_policy.json`

---

## Acceptance gates

A milestone is accepted only if all of the following are true:

1. scoped implementation completed
2. milestone validation commands pass
3. `docs/PLAN.md` updated
4. `docs/STATUS.md` updated
5. repo left resumable

The whole run is accepted only if:

- `hugo build` passes
- helper checks pass
- ghost URL policy is explicit
- canonical and sitemap checks pass
- discoverability checks pass
- Batch A and Batch B target edits are complete
- post-deploy manual checklist is ready

---

## Negative test matrix

- [ ] malformed `vercel.json` is caught before continuing
- [ ] malformed `url_policy.json` is caught before continuing
- [ ] canonical pointing to a no-slash or redirected URL is caught
- [ ] sitemap containing taxonomy URL is caught
- [ ] missing donor links for Batch A and Batch B are caught
- [ ] ghost URL without policy is caught
- [ ] target page slug change is caught during review
- [ ] local `_vercel/insights` noise is ignored as non-blocking

---

## Release and demo readiness gates

## Local readiness

- [ ] `hugo build` green
- [ ] local homepage renders
- [ ] local `/blog/` renders
- [ ] local `/about/` renders
- [ ] all target pages render
- [ ] helper checks all green

## Production readiness

- [ ] deployable diff only; no generated files committed
- [ ] redirect map reviewed
- [ ] no accidental analytics or workflow changes

## Post-deploy manual gates

- [ ] verify slash URL is `200`
- [ ] verify non-slash blog URL redirects to slash
- [ ] verify production sitemap contents
- [ ] inspect Batch A in GSC
- [ ] inspect Batch B in GSC
- [ ] request indexing only for changed priority pages

## Demo checklist

- [ ] show homepage featured or hub section
- [ ] show improved `/blog/` discovery block
- [ ] show one restored or redirected ghost URL example
- [ ] show canonical tag on one priority page
- [ ] show sitemap sanity
