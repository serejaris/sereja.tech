# Index Coverage PRD for sereja.tech

## Goal

Increase the share of canonical blog posts that can be indexed on `sereja.tech`.

Primary KPI:

`indexed canonical blog slugs / eligible canonical blog slugs`

## Verified context

- Issue `#32` documents the 2026-02-16 Search Console snapshot: `61/91` pages were not indexed.
- Issue `#33` documents the `12` posts in `Crawled - currently not indexed`; two of them are current Batch A targets:
  - `github-projects-ai-agent-memory`
  - `agent-teams-opus-4-6`
- Issue `#66` documents current SEO backlog priorities and ghost URLs based on the popularity snapshot from 2026-03-10.
- Issue `#34` is the referenced GSC snapshot source used by issue `#66`.
- Repo reality on 2026-03-11:
  - `88` blog post markdown files exist under `content/blog/`
  - homepage content exists in `content/_index.md`
  - about page exists in `content/about/index.md`

## Scope

Fix index coverage in dependency order:

1. baseline inventory and helper checks,
2. live/repo drift and stale URLs,
3. canonical, robots, and sitemap consistency,
4. internal discoverability for priority posts,
5. narrow search-fit tuning for selected posts.

## Non-negotiables

- Keep trailing-slash canonical policy for blog posts.
- Do not widen the indexable surface.
- Keep taxonomy and term pages `noindex, follow` unless explicitly re-scoped.
- Do not edit `public/`.
- Do not push or merge to `main`.
- Prefer working redirects or restored source over undocumented URL drift.
- Do not block execution on board or issue sync.

## Priority batches

### Batch A

- `github-projects-ai-agent-memory`
- `agent-teams-opus-4-6`

### Batch B

- `homebrew-cli-vibecoding`
- `chrome-devtools-mcp-setup`
- `claude-code-token-optimization`

## Known ghost URLs from issue #66

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

## Malformed or garbage URLs to classify separately

- `/blog/%20open%20router`
- `/blog/openclaw-vps-6-kimi.com/code/console`
- `/blog/data-layer-for-agents/)`

## Expected outcomes

- Every known ghost URL has an explicit fate: `restore`, `redirect`, or `410/404`.
- Canonical pages emit one stable canonical URL and sitemap entry.
- Priority posts are easier for crawlers to discover through indexable internal links.
- Batch A gets tuned before Batch B.

## Out of scope for this run

- Vanity metric optimization without indexation impact.
- Broad article rewrites outside the named batches.
- Analytics rework, CTA experiments, or unrelated layout cleanup.
- Production-only actions that require secrets or dashboard access.
