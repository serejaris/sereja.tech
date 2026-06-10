# Recurring prompt: analytics site run

Run the sereja.tech analytics loop and turn the result into tracked work.

## Steps

1. Ensure `.env.analytics` has `POSTHOG_PERSONAL_API_KEY` (see `docs/analytics-pipeline.md`).
2. Capture a fresh snapshot:
   `python3 scripts/analytics/posthog_query.py`
3. Build the review:
   `python3 scripts/analytics/site_review.py research/analytics-runs/<today>.json`
4. **Before creating new tasks**, open the previous analytics issue (`#97` /
   the latest analytics review issue) and revisit its checkboxes:
   - improved → comment the metric delta;
   - stalled twice → raise priority or split into a focused issue.
5. Post the generated `-issue.md` as a comment/new issue only for genuinely new
   findings. Keep one analytics review thread, don't fan out duplicates.

## Guardrails

- Never invent metrics. If the key is missing or the API is blocked, record the
  blocker and stop — do not fabricate a snapshot.
- The snapshot JSON is the source of truth; the review must cite it.
- Keep the loop repo-local: no manual dashboard scraping, no browser session.
