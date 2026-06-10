# Analytics pipeline

Repo-local loop for sereja.tech reader analytics. No web UI, no browser session —
a PostHog Personal API key in `.env.analytics` is the only secret.

## One-time setup

1. Create a Personal API key at <https://us.posthog.com/settings/user-api-keys>.
   Scopes: **Query Read** + **Project Read**. The value is shown once.
2. `cp .env.analytics.example .env.analytics` and paste the key.
   `.env.analytics` is gitignored — the key never gets committed.

## Each run

```bash
python3 scripts/analytics/posthog_query.py                       # → research/analytics-runs/YYYY-MM-DD.json
python3 scripts/analytics/site_review.py research/analytics-runs/YYYY-MM-DD.json   # → -review.md + -issue.md
python3 scripts/analytics/site_review.py research/analytics-runs/YYYY-MM-DD.json --check   # gate: must produce action tasks
```

The snapshot captures a 7-day window: visitors, blog pageviews per path, and
`article_read` completion/scroll per path (the events `static/analytics.js`
emits). The review derives concrete action tasks (repack low-completion
articles, refresh top entry routes, keep cadence).

## Contract

- One dated snapshot per run → one review → one issue body with **checkbox** tasks.
- The **next run revisits the prior issue's checkboxes before creating new tasks.**
  If an item improved, comment the metric change; if it stalls twice, raise
  priority or split it into a focused issue.
- Tracking issue: `serejaris/sereja.tech#107` (restore + pipeline), under epic `#104`.
  Analytics action-task home: `#97`.

## Cadence

Run every two weeks (per the month strategy in `#105`), or after publishing a
batch of posts. The recurring prompt is `prompts/analytics-site-run.md`.
