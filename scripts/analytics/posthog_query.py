#!/usr/bin/env python3
"""Pull a sereja.tech analytics snapshot from PostHog via the Query (HogQL) API.

Reads the Personal API key from POSTHOG_PERSONAL_API_KEY (or a local
.env.analytics file). Writes a dated snapshot JSON to research/analytics-runs/
that site_review.py consumes. No web UI, no browser session — just the key.

Get a key once at https://us.posthog.com/settings/user-api-keys
(scope: "Query Read" + "Project Read"), then:

    echo 'POSTHOG_PERSONAL_API_KEY=phx_...' >> .env.analytics
    python3 scripts/analytics/posthog_query.py
"""
import json
import os
import sys
import urllib.request
import urllib.error
from datetime import date, datetime, timezone
from pathlib import Path

HOST = "https://us.posthog.com"
REPO = Path(__file__).resolve().parents[2]
RUNS_DIR = REPO / "research" / "analytics-runs"
ENV_FILE = REPO / ".env.analytics"


def load_key() -> str:
    key = os.environ.get("POSTHOG_PERSONAL_API_KEY", "").strip()
    if not key and ENV_FILE.exists():
        for line in ENV_FILE.read_text().splitlines():
            line = line.strip()
            if line.startswith("POSTHOG_PERSONAL_API_KEY="):
                key = line.split("=", 1)[1].strip().strip('"').strip("'")
                break
    if not key:
        sys.exit(
            "No POSTHOG_PERSONAL_API_KEY. Create one at "
            "https://us.posthog.com/settings/user-api-keys (scopes: Query Read, "
            f"Project Read), then add it to {ENV_FILE} or export it."
        )
    return key


def api(path: str, key: str, method: str = "GET", body: dict | None = None) -> dict:
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(f"{HOST}{path}", data=data, method=method)
    req.add_header("Authorization", f"Bearer {key}")
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        sys.exit(f"PostHog API {e.code} on {path}: {e.read().decode()[:300]}")
    except urllib.error.URLError as e:
        sys.exit(f"PostHog API unreachable: {e}")


def first_project_id(key: str) -> int:
    res = api("/api/projects/", key)
    projects = res.get("results", [])
    if not projects:
        sys.exit("No projects visible to this key (needs Project Read scope).")
    return projects[0]["id"]


def hogql(project_id: int, key: str, query: str) -> list:
    res = api(
        f"/api/projects/{project_id}/query/",
        key,
        method="POST",
        body={"query": {"kind": "HogQLQuery", "query": query}},
    )
    return res.get("results", [])


def main() -> None:
    key = load_key()
    pid = first_project_id(key)

    # Pageviews per blog path, last 7 days.
    pageviews = hogql(
        pid,
        key,
        """
        SELECT properties.$pathname AS path, count() AS views
        FROM events
        WHERE event = '$pageview'
          AND timestamp > now() - INTERVAL 7 DAY
          AND properties.$pathname LIKE '/blog/%'
        GROUP BY path ORDER BY views DESC LIMIT 30
        """,
    )

    # article_read completion + read score per path, last 7 days.
    reads = hogql(
        pid,
        key,
        """
        SELECT properties.path AS path,
               count() AS reads,
               round(avg(toFloat(properties.read_score)), 1) AS avg_read_score,
               round(avg(toFloat(properties.max_scroll_depth)), 1) AS avg_scroll,
               round(100.0 * countIf(properties.completed = true) / count(), 1) AS completion_pct
        FROM events
        WHERE event = 'article_read'
          AND timestamp > now() - INTERVAL 7 DAY
        GROUP BY path ORDER BY reads DESC LIMIT 30
        """,
    )

    # Totals.
    totals = hogql(
        pid,
        key,
        """
        SELECT
          countIf(event = '$pageview') AS pageviews,
          countIf(event = 'article_read') AS article_reads,
          uniqIf(person_id, event = '$pageview') AS visitors
        FROM events
        WHERE timestamp > now() - INTERVAL 7 DAY
        """,
    )
    t = totals[0] if totals else [0, 0, 0]

    snapshot = {
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "window_days": 7,
        "source": "posthog_query_api",
        "project_id": pid,
        "totals": {
            "pageviews_7d": t[0],
            "article_reads_7d": t[1],
            "visitors_7d": t[2],
        },
        "blog_pageviews": [{"path": r[0], "views": r[1]} for r in pageviews],
        "article_reads": [
            {
                "path": r[0],
                "reads": r[1],
                "avg_read_score": r[2],
                "avg_scroll": r[3],
                "completion_pct": r[4],
            }
            for r in reads
        ],
    }

    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    # Date is passed in so the script stays deterministic under automation.
    run_date = os.environ.get("ANALYTICS_RUN_DATE") or date.today().isoformat()
    out = RUNS_DIR / f"{run_date}.json"
    out.write_text(json.dumps(snapshot, indent=2, ensure_ascii=False))
    print(f"Wrote {out.relative_to(REPO)}")
    print(
        f"  visitors_7d={snapshot['totals']['visitors_7d']} "
        f"pageviews_7d={snapshot['totals']['pageviews_7d']} "
        f"article_reads_7d={snapshot['totals']['article_reads_7d']}"
    )


if __name__ == "__main__":
    main()
