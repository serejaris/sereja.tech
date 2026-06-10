#!/usr/bin/env python3
"""Turn a dated PostHog snapshot into a review with concrete action tasks.

    python3 scripts/analytics/site_review.py research/analytics-runs/YYYY-MM-DD.json

Writes <date>-review.md and <date>-issue.md alongside the snapshot. The issue
body lists action tasks as checkboxes; the next run revisits them before
creating new work (see docs/analytics-pipeline.md).
"""
import json
import sys
from pathlib import Path

LOW_COMPLETION = 50.0   # % — below this an article is "low completion"
LOW_SCROLL = 60.0       # % avg scroll depth


def load(path: Path) -> dict:
    if not path.exists():
        sys.exit(f"Snapshot not found: {path}")
    return json.loads(path.read_text())


def build(snap: dict) -> tuple[str, str]:
    t = snap.get("totals", {})
    reads = snap.get("article_reads", [])
    views = snap.get("blog_pageviews", [])

    low = [
        r for r in reads
        if r.get("reads", 0) >= 3
        and (r.get("completion_pct") or 0) < LOW_COMPLETION
    ]
    top_views = views[:5]

    review = [f"# Analytics review — {snap.get('captured_at', '')[:10]}", ""]
    review.append("## Totals (7d)")
    review.append(f"- Visitors: {t.get('visitors_7d', '?')}")
    review.append(f"- Pageviews: {t.get('pageviews_7d', '?')}")
    review.append(f"- Article reads: {t.get('article_reads_7d', '?')}")
    review.append("")
    review.append("## Top blog entry routes")
    for r in top_views:
        review.append(f"- {r['path']} — {r['views']} views")
    review.append("")
    review.append("## Low-completion articles (≥3 reads, completion < %.0f%%)" % LOW_COMPLETION)
    if low:
        for r in sorted(low, key=lambda x: x.get("completion_pct") or 0):
            review.append(
                f"- {r['path']} — completion {r.get('completion_pct')}%, "
                f"avg_scroll {r.get('avg_scroll')}%, reads {r['reads']}"
            )
    else:
        review.append("- none over the read threshold")
    review.append("")

    # Action tasks for the issue body.
    tasks = []
    if low:
        worst = sorted(low, key=lambda x: x.get("completion_pct") or 0)[0]
        tasks.append(
            f"**P2 Repack low-completion article** (`content_repack`) — "
            f"start with `{worst['path']}` (completion {worst.get('completion_pct')}%). "
            f"Tighten intro + first screen, then compare after next snapshot."
        )
    if t.get("visitors_7d", 0) and top_views:
        tasks.append(
            "**P1 Refresh top entry routes** (`traffic`) — open the top-5 routes "
            "above, check above-the-fold promise and CTA, patch smallest copy/links."
        )
    tasks.append(
        "**P2 Publish on cadence** (`cadence`) — keep 2 posts/week from strong "
        "clusters (agent memory, Claude Code workflows, releases)."
    )

    issue = ["## Analytics site review — " + snap.get("captured_at", "")[:10], ""]
    issue.append(f"Source snapshot: `research/analytics-runs/{snap.get('captured_at','')[:10]}.json`")
    issue.append("")
    issue.append("### Summary")
    issue.append(f"- Visitors 7d: {t.get('visitors_7d','?')} / Pageviews: {t.get('pageviews_7d','?')} / Reads: {t.get('article_reads_7d','?')}")
    issue.append(f"- Low-completion articles: {len(low)}")
    issue.append("")
    issue.append("### Action tasks")
    for task in tasks:
        issue.append(f"- [ ] {task}")
    issue.append("")
    issue.append("### Run rule")
    issue.append(
        "Next run revisits these checkboxes before creating new tasks. If an item "
        "improved, comment with the metric change. If it did not improve twice, "
        "raise priority or split into a focused issue."
    )
    return "\n".join(review) + "\n", "\n".join(issue) + "\n"


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit("usage: site_review.py research/analytics-runs/YYYY-MM-DD.json [--check]")
    path = Path(sys.argv[1])
    snap = load(path)
    review_md, issue_md = build(snap)

    if "--check" in sys.argv:
        if "- [ ]" not in issue_md:
            sys.exit("FAIL: review produced no action tasks")
        print("ok: review has action tasks")
        return

    stem = path.with_suffix("")
    (Path(str(stem) + "-review.md")).write_text(review_md)
    (Path(str(stem) + "-issue.md")).write_text(issue_md)
    print(f"Wrote {stem.name}-review.md and {stem.name}-issue.md")


if __name__ == "__main__":
    main()
