# GSC Backlog Audit — 2026-05-07

Source: live Google Search Console browser session for `sc-domain:sereja.tech`.

Inventory source: `research/gsc-live/2026-05-07-gsc-backlog-inventory.json`.

Report state:

- Report: `Page indexing`
- Filter: `All known pages`
- Last update: `2026-05-03`
- Indexed: `75`
- Not indexed: `207`

## Rows in scope for issue #102

| GSC reason | Pages | Validation state in GSC | Decision |
| --- | ---: | --- | --- |
| `Crawled - currently not indexed` | 74 | `Not Started` | Fix repo-controlled canonical blog discoverability; classify slashless/www variants as canonical lag; split out non-Hugo hosts. |
| `Duplicate, Google chose different canonical than user` | 9 | `Not Started` | Treat slashless examples as validation-only after source cleanup; inspect `document-conversations-not-code/` before guessing. |
| `Discovered - currently not indexed` | 1 | `Started` on `2026-02-19` | Strengthen donor links for `/blog/remotion-programmatic-video-vibecoding/`; request indexing after production deploy or record existing state. |

## Local classifier result

Command:

```bash
python3 scripts/seo/url_audit.py classify-gsc-backlog research/gsc-live/2026-05-07-gsc-backlog-inventory.json
```

After the repo fixes:

```text
gsc-backlog-ok (examples=84)
by_reason=Crawled - currently not indexed:74, Discovered - currently not indexed:1, Duplicate, Google chose different canonical than user:9
by_route_type=blog-index:1, canonical-blog:35, out-of-scope-host:3, slashless-blog:42, www-host-variant:3
low_donor_routes=0
```

## Route classification

| Route type | Count | Decision |
| --- | ---: | --- |
| `canonical-blog` | 35 | Repo-controlled. Must render `200`, self-canonical, sitemap member, not `noindex`, and have at least 3 internal donor pages. |
| `slashless-blog` | 42 | Validation-only if production redirects to slash and repo sources do not link to slashless variants. |
| `www-host-variant` | 3 | Validation-only host variant after canonical/redirect smoke. |
| `blog-index` | 1 | Validation-only; `/blog/` is indexable and canonical. |
| `out-of-scope-host` | 3 | Out of this Hugo repo scope. Track separately if needed. |

Out-of-scope host examples:

- `https://live.sereja.tech/feed.xml`
- `https://live.sereja.tech/`
- `https://ai-corp.sereja.tech/`

## Duplicate URL inspection

Inspected URL:

- `https://sereja.tech/blog/document-conversations-not-code/`

GSC URL Inspection result:

- Status: `URL is not on Google`
- Page indexing: `Page is not indexed: Duplicate, Google chose different canonical than user`
- Last crawl: `Mar 30, 2026, 3:54:25 PM`
- Crawled as: `Googlebot smartphone`
- Page fetch: `Successful`
- Indexing allowed: `Yes`
- User-declared canonical: `https://sereja.tech/blog/document-conversations-not-code/`
- Google-selected canonical: `https://sereja.tech/blog/document-conversations-not-code`

Decision: technical slash/canonical lag, not a semantic duplicate. No redirect/merge/content split needed in this iteration.

## Repo fixes made

Conservative internal donor links were added for GSC backlog routes that had fewer than 3 unique indexable donor pages in rendered HTML.

| Target route | Pre-fix donors | Decision |
| --- | ---: | --- |
| `/blog/ai-student-progress-tracking/` | 2 | Fix: add contextual donor links from education/product pages. |
| `/blog/app-types-guide/` | 1 | Fix: add contextual donor links from product/learning/agent strategy pages. |
| `/blog/claude-code-logs-project-status/` | 2 | Fix: add contextual donor links from memory/hooks pages. |
| `/blog/claude-code-voice-assistant/` | 1 | Fix: add contextual donor links from automation/media pages. |
| `/blog/clawdbot-telegram-max/` | 2 | Fix: add contextual donor link from agent-interface content. |
| `/blog/context-lat-90-minutes/` | 2 | Fix: add contextual donor link from LLM workflow content. |
| `/blog/fact-checker-in-ai-workflow/` | 1 | Fix: add contextual donor links from planning/consilium content. |
| `/blog/hooks-that-work-2026/` | 1 | Fix: add contextual donor links from automation/memory content. |
| `/blog/local-rag-embeddings-m1/` | 2 | Fix: add contextual donor link from assistant-memory content. |
| `/blog/midi-obs-claude-code/` | 1 | Fix: add contextual donor links from video automation content. |
| `/blog/moltbook-social-network-ai-agents/` | 1 | Fix: add contextual donor links from agent-interface/front-end content. |
| `/blog/personal-os-project-audit/` | 1 | Fix: add contextual donor links from memory/consilium content. |
| `/blog/personalized-teaching-student-data/` | 2 | Fix: add contextual donor link from course-progress content. |
| `/blog/remotion-programmatic-video-vibecoding/` | 1 | Fix: add 3 relevant donor links from video/Playwright/content-pipeline pages. |
| `/blog/tailwind-layoffs-ai-impact/` | 1 | Fix: add contextual donor links from product/frontend/fact-check content. |
| `/blog/telegram-api-vs-json-export/` | 2 | Fix: add contextual donor links from Telegram/content-analysis pages. |
| `/blog/telegram-single-message-digest/` | 1 | Fix: add contextual donor links from Telegram/content-analysis pages. |
| `/blog/video-lesson-ux/` | 2 | Fix: add contextual donor links from video/education pages. |

No broad article rewrites, slug changes, taxonomy changes, or canonical policy changes were made.

## Final decision table

| Scope | URLs | Decision | Follow-up |
| --- | ---: | --- | --- |
| Repo-controlled canonical blog URLs with weak donors | 18 route targets | `fix` | Ship donor-link diff through Git-connected Vercel and run production smoke. |
| Slashless blog examples | 42 examples | `validate-only` | Confirm production redirects to slash and start GSC validation. |
| `www.sereja.tech` examples | 3 examples | `validate-only` | Confirm canonical host behavior; no Hugo content change. |
| `/blog` index example | 1 example | `validate-only` | Confirm `/blog/` canonical and sitemap state. |
| `live.sereja.tech` and `ai-corp.sereja.tech` | 3 examples | `out-of-scope` | Split into a separate issue if those hosts need SEO work. |
| True semantic duplicate | 0 confirmed | `split` only if discovered later | No split needed from current URL Inspection evidence. |

## Production/GSC handoff

After Git-connected production deploy:

1. Smoke changed canonical URLs and sitemap.
2. Start `VALIDATE FIX` for `Duplicate, Google chose different canonical than user`.
3. Start `VALIDATE FIX` for `Crawled - currently not indexed`.
4. Inspect `/blog/remotion-programmatic-video-vibecoding/` and request indexing, or record the existing validation state if GSC does not allow a new request.
