#!/usr/bin/env python3
"""Regenerate the "Последние статьи" table and post count in README.md.

Source of truth: content/blog/*.md frontmatter (title, date, draft).
Idempotent. Run standalone or from the pre-commit hook.

Anchors (structural, no special markers needed):
  - count line: the sentence containing "статей о разработке" — leading number is replaced.
  - table: between the "## Последние статьи" heading and the "[Все статьи →]" line.

Missing anchors / no posts are a HARD FAILURE (exit 1) so the pre-commit hook
blocks stale metadata instead of silently letting README drift. If README
structure changed intentionally, fix the anchors here (or `git commit --no-verify`
to bypass once, same escape hatch as validate-blog-post.sh).
"""
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(subprocess.run(["git", "rev-parse", "--show-toplevel"],
                           capture_output=True, text=True, check=True).stdout.strip())
BLOG_DIR = REPO / "content" / "blog"
README = REPO / "README.md"
BASE_URL = "https://sereja.tech/blog"
LATEST_N = 10


def fail(msg: str) -> int:
    print(f"update-readme: ERROR {msg}", file=sys.stderr)
    print("update-readme: fix scripts/update-readme.py anchors or 'git commit --no-verify' to bypass once.",
          file=sys.stderr)
    return 1


def parse_frontmatter(text: str) -> dict:
    """Return {title, date, draft} from the first --- ... --- block."""
    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    fm = {}
    if not m:
        return fm
    for line in m.group(1).splitlines():
        mm = re.match(r"^(title|date|draft):\s*(.*)$", line)
        if mm:
            k, v = mm.group(1), mm.group(2).strip()
            v = re.sub(r'^"(.*)"$', r"\1", v)
            v = re.sub(r"^'(.*)'$", r"\1", v)
            fm[k] = v
    return fm


def collect_posts():
    posts = []
    for f in sorted(BLOG_DIR.glob("*.md")):
        if f.name == "_index.md":
            continue
        fm = parse_frontmatter(f.read_text(encoding="utf-8"))
        if str(fm.get("draft", "")).lower() == "true":
            continue
        title = fm.get("title", "").strip()
        date = fm.get("date", "").strip()
        if not title or not date:
            continue
        posts.append({"slug": f.stem, "title": title, "date": date[:10], "sort": date})
    return posts


def build_table(posts) -> str:
    rows = ["| Дата | Статья |", "|------|--------|"]
    for p in sorted(posts, key=lambda x: (x["sort"], x["slug"]), reverse=True)[:LATEST_N]:
        title = p["title"].replace("|", r"\|")
        rows.append(f"| {p['date']} | [{title}]({BASE_URL}/{p['slug']}/) |")
    return "\n".join(rows)


def main():
    if not README.exists():
        return fail("README.md not found")
    posts = collect_posts()
    if not posts:
        return fail("no published posts found in content/blog/")
    count = len(posts)
    text = README.read_text(encoding="utf-8")
    original = text

    # 1) count in the intro sentence
    text, n_count = re.subn(r"\d+\+?\s+статей о разработке",
                            f"{count} статей о разработке", text)
    if n_count == 0:
        return fail("count anchor 'N статей о разработке' not found in README.md")

    # 2) latest-posts table between the heading and the "[Все статьи →]" line
    lines = text.splitlines()
    try:
        head = next(i for i, l in enumerate(lines) if l.strip() == "## Последние статьи")
        tbl_start = next(i for i in range(head, len(lines)) if lines[i].startswith("| Дата | Статья |"))
        all_link = next(i for i in range(tbl_start, len(lines)) if lines[i].lstrip().startswith("[Все статьи"))
    except StopIteration:
        return fail("latest-posts table anchors ('## Последние статьи' / '| Дата | Статья |' / '[Все статьи') not found")

    new_lines = lines[:tbl_start] + build_table(posts).splitlines() + lines[all_link:]
    text = "\n".join(new_lines) + ("\n" if original.endswith("\n") else "")

    if text != original:
        README.write_text(text, encoding="utf-8")
        print(f"update-readme: README regenerated ({count} posts, latest {LATEST_N})")
    else:
        print("update-readme: README already up to date")
    return 0


if __name__ == "__main__":
    sys.exit(main())
