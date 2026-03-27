#!/usr/bin/env python3
"""
Cross-domain link generator for the sereja.tech ecosystem.

Analyzes content across 4 sites and generates data/cross_links.json
for each Hugo site, enabling automatic cross-domain "Related" blocks.

Sites:
  sereja.tech   — personal blog (/blog/:slug/)
  context.lat   — AI tools reference (/tools/:slug/, /mcp/:slug/, etc.)
  vibecoded.pro — community Q&A (/q/:slug/)
  vibecoding.phd — landing page (static, separate integration)

Usage:
  python3 scripts/cross-domain-linking/generate.py
  python3 scripts/cross-domain-linking/generate.py --dry-run
"""

import json
import re
import sys
from pathlib import Path
from collections import defaultdict

# ── Config ──────────────────────────────────────────────────────────────────

BASE = Path(__file__).resolve().parent.parent.parent  # sereja.tech root
REPOS = {
    "sereja.tech": BASE,
    "context.lat": BASE.parent / "context.lat",
    "vibecoded.pro": BASE.parent / "vibecoded.pro",
}

SITE_URLS = {
    "sereja.tech": "https://sereja.tech",
    "context.lat": "https://context.lat",
    "vibecoded.pro": "https://vibecoded.pro",
}

SITE_LABELS = {
    "sereja.tech": "Блог",
    "context.lat": "Справочник",
    "vibecoded.pro": "Вайбкодеры",
}

# Section labels for context.lat
SECTION_LABELS = {
    "tools": "Инструменты",
    "mcp": "MCP серверы",
    "models": "Модели",
    "concepts": "Концепции",
    "guides": "Гайды",
    "skills": "Скиллы",
    "q": "Q&A",
    "blog": "Статья",
}

# Max cross-domain links per page
MAX_LINKS = 3

# Minimum tag overlap score to create a link
MIN_SCORE = 1

# ── Keyword normalization ────────────────────────────────────────────────────

def normalize_tag(tag: str) -> str:
    """Normalize tag for comparison: lowercase, strip, unify hyphens/spaces."""
    return re.sub(r"[-\s]+", "-", tag.strip().lower())


def extract_keywords(text: str) -> set[str]:
    """Extract significant keywords from text (title + description)."""
    text = text.lower()
    # Remove punctuation except hyphens
    text = re.sub(r"[^\w\s\-]", " ", text)
    words = set(text.split())
    # Filter short/common words
    stopwords = {
        "для", "это", "как", "что", "или", "через", "при", "но", "не",
        "и", "в", "на", "с", "по", "от", "до", "из", "за", "к", "у",
        "the", "and", "for", "with", "from", "how", "why", "что", "где",
        "a", "an", "to", "of", "in", "is", "are", "was", "be", "can",
    }
    return {w for w in words if len(w) > 3 and w not in stopwords}


# ── Frontmatter parser ──────────────────────────────────────────────────────

def parse_frontmatter(path: Path) -> dict:
    """Extract YAML frontmatter from a markdown file."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    fm_text = parts[1]
    body = parts[2]

    fm: dict = {}
    # Parse title
    m = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', fm_text, re.MULTILINE)
    if m:
        fm["title"] = m.group(1).strip().strip('"\'')
    # Parse description
    m = re.search(r'^description:\s*["\']?(.+?)["\']?\s*$', fm_text, re.MULTILINE)
    if m:
        fm["description"] = m.group(1).strip().strip('"\'')
    # Parse tags (array format: ["a", "b"] or [a, b])
    m = re.search(r'^tags:\s*\[(.+?)\]', fm_text, re.MULTILINE | re.DOTALL)
    if m:
        raw = m.group(1)
        tags = re.findall(r'["\']([^"\']+)["\']|(\b[a-zа-яёА-ЯЁA-Z][^\s,\]]+\b)', raw)
        fm["tags"] = [t[0] or t[1] for t in tags if (t[0] or t[1]).strip()]
    else:
        fm["tags"] = []
    # Parse draft
    m = re.search(r'^draft:\s*(true|false)', fm_text, re.MULTILINE)
    fm["draft"] = m.group(1) == "true" if m else False
    # Body excerpt for keyword matching
    fm["body_excerpt"] = body[:2000].lower()
    return fm


# ── Content index ────────────────────────────────────────────────────────────

class Page:
    def __init__(self, site: str, section: str, slug: str, fm: dict):
        self.site = site
        self.section = section
        self.slug = slug
        self.title = fm.get("title", slug)
        self.description = fm.get("description", "")
        self.tags = [normalize_tag(t) for t in fm.get("tags", [])]
        self.draft = fm.get("draft", False)
        self.body_excerpt = fm.get("body_excerpt", "")
        self.key = f"{section}/{slug}"
        # Keywords from title + description
        self.keywords = extract_keywords(f"{self.title} {self.description}")

    @property
    def url(self) -> str:
        base = SITE_URLS[self.site]
        return f"{base}/{self.section}/{self.slug}/"

    @property
    def domain_label(self) -> str:
        return SITE_LABELS[self.site]

    @property
    def section_label(self) -> str:
        return SECTION_LABELS.get(self.section, self.section.capitalize())


def index_site(site: str, repo: Path) -> list[Page]:
    """Index all content pages for a site."""
    pages = []
    content_dir = repo / "content"
    if not content_dir.exists():
        print(f"  WARNING: {content_dir} not found", file=sys.stderr)
        return pages

    for md_file in content_dir.rglob("*.md"):
        if md_file.name == "_index.md":
            continue
        # Derive section and slug from path
        rel = md_file.relative_to(content_dir)
        parts = rel.parts
        if len(parts) == 1:
            # Top-level file (e.g., content/index.md)
            section = "blog" if site == "sereja.tech" else "pages"
            slug = parts[0].replace(".md", "")
        else:
            section = parts[0]
            slug = parts[-1].replace(".md", "")

        fm = parse_frontmatter(md_file)
        if not fm or fm.get("draft"):
            continue
        if not fm.get("title"):
            continue

        page = Page(site, section, slug, fm)
        pages.append(page)

    return pages


# ── Scoring ──────────────────────────────────────────────────────────────────

def score_pair(source: Page, target: Page) -> float:
    """
    Score relevance between two pages from different sites.
    Higher = more relevant.
    """
    if source.site == target.site:
        return 0.0

    score = 0.0

    # Exact tag overlap (normalized)
    source_tags = set(source.tags)
    target_tags = set(target.tags)
    shared_tags = source_tags & target_tags
    score += len(shared_tags) * 2.0

    # Tool name mention: target title words appear in source body
    target_title_words = set(target.title.lower().split())
    significant_title_words = {w for w in target_title_words if len(w) > 3}
    for word in significant_title_words:
        if word in source.body_excerpt:
            score += 1.5
            break  # count once per target title

    # Keyword overlap between titles/descriptions
    shared_kw = source.keywords & target.keywords
    score += len(shared_kw) * 0.5

    # Boost: context.lat is more specific (reference site) — prioritize linking to it
    if target.site == "context.lat":
        score *= 1.2

    return score


# ── Link generation ──────────────────────────────────────────────────────────

def generate_cross_links(all_pages: list[Page]) -> dict[str, dict[str, list[dict]]]:
    """
    Generate cross-domain links for all pages.
    Returns: {site: {page_key: [link, ...]}}
    """
    result: dict[str, dict[str, list[dict]]] = {site: {} for site in REPOS}

    for source in all_pages:
        candidates = []
        for target in all_pages:
            if target.site == source.site:
                continue
            s = score_pair(source, target)
            if s >= MIN_SCORE:
                candidates.append((s, target))

        # Sort by score desc, take top MAX_LINKS
        candidates.sort(key=lambda x: -x[0])
        top = candidates[:MAX_LINKS]

        if top:
            result[source.site][source.key] = [
                {
                    "title": t.title,
                    "url": t.url,
                    "domain": t.site,
                    "domain_label": t.domain_label,
                    "section_label": t.section_label,
                    "description": t.description[:100] if t.description else "",
                }
                for _, t in top
            ]

    return result


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    dry_run = "--dry-run" in sys.argv
    verbose = "--verbose" in sys.argv

    print("Indexing content...")
    all_pages: list[Page] = []
    for site, repo in REPOS.items():
        if not repo.exists():
            print(f"  SKIP {site}: repo not found at {repo}")
            continue
        pages = index_site(site, repo)
        all_pages.extend(pages)
        print(f"  {site}: {len(pages)} pages")

    print(f"\nTotal pages: {len(all_pages)}")
    print("Generating cross-domain links...")

    cross_links = generate_cross_links(all_pages)

    # Stats
    total_links = sum(
        sum(len(v) for v in site_map.values())
        for site_map in cross_links.values()
    )
    print(f"Total cross-links generated: {total_links}")

    if verbose:
        for site, site_map in cross_links.items():
            print(f"\n{site}:")
            for key, links in site_map.items():
                print(f"  {key}:")
                for link in links:
                    print(f"    → {link['domain']}: {link['title']}")

    if dry_run:
        print("\nDry run — no files written.")
        return

    # Write data files
    for site, site_map in cross_links.items():
        repo = REPOS.get(site)
        if not repo or not repo.exists():
            continue
        data_dir = repo / "data"
        data_dir.mkdir(exist_ok=True)
        out_path = data_dir / "cross_links.json"
        out_path.write_text(json.dumps(site_map, ensure_ascii=False, indent=2))
        print(f"\nWritten: {out_path} ({len(site_map)} entries)")

    # Also write a combined file for vibecoding.phd
    phd_repo = BASE.parent / "vibecoding.phd"
    if phd_repo.exists():
        phd_out = phd_repo / "public" / "cross_links.json"
        phd_out.parent.mkdir(exist_ok=True)
        # Collect all links pointing TO vibecoding.phd pages (currently none since
        # vibecoding.phd isn't indexed) and links FROM other sites.
        # For now, export a flat list of all pages for phd to consume.
        all_export = [
            {
                "site": p.site,
                "key": p.key,
                "title": p.title,
                "url": p.url,
                "tags": p.tags,
                "description": p.description,
            }
            for p in all_pages
        ]
        phd_out.write_text(json.dumps(all_export, ensure_ascii=False, indent=2))
        print(f"Written: {phd_out} (content catalog for vibecoding.phd)")

    print("\nDone.")


if __name__ == "__main__":
    main()
