# GSC Page Indexing Reason Audit — 2026-05-07

Source: live Google Search Console browser session for `sc-domain:sereja.tech`.

Report state:

- Report: `Page indexing`
- Filter: `All known pages`
- Last update: `2026-05-03`
- Indexed: `75`
- Not indexed: `207`

## Reason-by-reason result

| GSC reason | Pages | Browser evidence | Decision | Covered by PR #99 |
| --- | ---: | --- | --- | --- |
| Excluded by `noindex` tag | 86 | Examples are tag/taxonomy pages such as `/tags/context-engineering/`, `/tags/vibe-coding/`, `/tags/claude.md/`. | Expected policy. Taxonomy and term pages stay `noindex, follow`; do not widen indexable surface. | No code change needed. Existing `check-sitemap` verifies noindex pages are not in sitemap. |
| Page with redirect | 34 | Drilldown shows first detected `2026-01-24`, affected pages `34`, and slashless/alias examples such as `/blog/telegram-api-vs-json-export`, `/blog/pipeline-reliability-state-persistence`, `/blog/blog-post-pipeline`, plus host/protocol variants. | Actionable source hygiene issue. Stop repo sources from feeding slashless blog URLs and old redirect aliases. | Yes. PR #99 normalizes internal blog links, fixes maintained `llms` aliases, adds `check-redirect-sources`, and keeps redirects. |
| Not found (404) | 2 | Examples are `https://sereja.tech/blog/{slug}` and `https://sereja.tech/tags/brainstorming/`. | `{slug}` is a repo-source leak from a literal prompt template and should be removed. `/tags/brainstorming/` has no current repo source and is an old/stale tag URL; do not redirect without a clear successor. | Partly. PR #99 replaces the crawlable-looking `{slug}` URL with `CANONICAL_ARTICLE_URL` and extends `check-redirect-sources` to catch template-looking internal URLs. The stale tag URL remains no-action. |
| Crawled - currently not indexed | 74 | Examples include canonical blog URLs such as `/blog/llms-txt-agent-readable-web/`, `/blog/midi-obs-claude-code/`, `/blog/blog-to-telegram-skill/`, plus `live.sereja.tech` URLs and one slashless `/blog/video-pipeline-claude-code`. | Main canonical coverage backlog. Do not treat redirect cleanup as sufficient. Needs separate page-level prioritization, URL inspection, internal discovery, and content/search-fit work. | No, except incidental cleanup for slashless source leaks. This remains separate work. |
| Duplicate, Google chose different canonical than user | 9 | Examples include `/blog/document-conversations-not-code/`, slashless `/blog/personal-os-project-audit`, `/blog/skills-knowledge-transfer`, `/blog/agent-swarm-frontend`, `/blog/blog-to-telegram-skill`, `/blog/react-presentation-no-build`, `/blog/dev-script-health-checks`, `/blog/content-plan-subagents-exa`, `/blog/github-issues-project-context`. | Do not guess. Needs URL Inspection for Google-selected canonical before changing canonical or redirect behavior. Slashless examples may improve after source cleanup, but full fix is separate. | No, except incidental source-link normalization. |
| Discovered - currently not indexed | 1 | Example is `/blog/remotion-programmatic-video-vibecoding/`, last crawled `N/A`; validation was already started on `2026-02-19`. | Separate recrawl/discovery issue. This restored page may need stronger internal links and post-deploy request indexing, but not as part of redirect-source cleanup. | No. |
| Alternate page with proper canonical tag | 1 | Overview row shows validation `Passed`. | No fix needed. | No code change needed. |

## Completion boundary

PR #99 fixes the source-hygiene issues that can be changed safely from the repo:

- `Page with redirect` source leaks.
- The crawlable-looking `/blog/{slug}` 404 source.
- Local guardrails that prevent these regressions.

PR #99 does not claim to fix all canonical indexing issues. The remaining `Crawled - currently not indexed`, `Duplicate`, and `Discovered` rows need a separate post-merge GSC pass after production deploy.
