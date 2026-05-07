#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
import sys
import tomllib
import xml.etree.ElementTree as ET
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable
from urllib.parse import urljoin, urlparse


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[1]
POLICY_PATH = SCRIPT_DIR / "url_policy.json"
HUGO_CONFIG_PATH = REPO_ROOT / "hugo.toml"
VERCEL_CONFIG_PATH = REPO_ROOT / "vercel.json"
PUBLIC_DIR = REPO_ROOT / "public"
BLOG_DIR = REPO_ROOT / "content" / "blog"
ABOUT_DIR = REPO_ROOT / "content" / "about"
DEFAULT_GSC_BACKLOG_PATH = REPO_ROOT / "research" / "gsc-live" / "2026-05-07-gsc-backlog-inventory.json"
REQUIRED_COMMANDS = (
    "summary",
    "check-ghosts",
    "check-canonical",
    "check-sitemap",
    "check-target-links",
    "check-redirect-sources",
)
GSC_BACKLOG_COMMAND = "classify-gsc-backlog"
SOURCE_LINK_GLOBS = (
    "content/**/*.md",
    "layouts/**/*.html",
    "static/**/*.txt",
    "static/**/*.html",
)
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)\s]+)\)")
HTML_HREF_RE = re.compile(r"""href=["']([^"']+)["']""")
BARE_SITE_URL_RE = re.compile(r"https://sereja\.tech/[^\s<>'\"\)\]]+")
ALLOWED_GHOST_STATUSES = {"needs_policy", "restore", "redirect", "410_or_404"}
ALLOWED_MALFORMED_STATUSES = ALLOWED_GHOST_STATUSES | {"ignore"}


class AuditError(RuntimeError):
    pass


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.canonical_href: str | None = None
        self.robots: list[str] = []
        self.links: list[tuple[str, str]] = []
        self._anchor_href: str | None = None
        self._anchor_text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = {key.lower(): (value or "") for key, value in attrs}
        if tag == "link":
            rel_tokens = {token.strip().lower() for token in attr_map.get("rel", "").split()}
            if "canonical" in rel_tokens and attr_map.get("href"):
                self.canonical_href = attr_map["href"]
        elif tag == "meta":
            if attr_map.get("name", "").lower() == "robots" and attr_map.get("content"):
                self.robots.append(attr_map["content"])
        elif tag == "a" and attr_map.get("href"):
            self._anchor_href = attr_map["href"]
            self._anchor_text = []

    def handle_data(self, data: str) -> None:
        if self._anchor_href is not None:
            self._anchor_text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "a" and self._anchor_href is not None:
            anchor_text = re.sub(r"\s+", " ", "".join(self._anchor_text)).strip()
            self.links.append((self._anchor_href, anchor_text))
            self._anchor_href = None
            self._anchor_text = []


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise AuditError(f"missing required file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise AuditError(f"invalid json in {path}: {exc}") from exc


def load_toml(path: Path) -> dict:
    try:
        return tomllib.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise AuditError(f"missing required file: {path}") from exc
    except tomllib.TOMLDecodeError as exc:
        raise AuditError(f"invalid toml in {path}: {exc}") from exc


def existing_blog_slugs() -> set[str]:
    return {path.stem for path in BLOG_DIR.glob("*.md") if path.name != "_index.md"}


def normalize_route(value: str, *, allow_file_paths: bool = False) -> str | None:
    if not value:
        return None

    parsed = urlparse(value)
    path = parsed.path or value
    path = path.replace("\\)", ")").replace("\\(", "(")

    if parsed.scheme and parsed.scheme not in {"http", "https"}:
        return None

    if parsed.scheme in {"http", "https"} and parsed.netloc and parsed.netloc != site_netloc():
        return None

    if not path.startswith("/"):
        return None

    if path == "/":
        return "/"

    if allow_file_paths and "." in Path(path).name:
        return path

    if "." not in Path(path).name and not path.endswith("/"):
        return f"{path}/"

    return path


def site_base_url() -> str:
    config = load_toml(HUGO_CONFIG_PATH)
    base_url = config.get("baseURL")
    if not isinstance(base_url, str) or not base_url:
        raise AuditError("baseURL is missing from hugo.toml")
    if not base_url.endswith("/"):
        base_url = f"{base_url}/"
    return base_url


def site_netloc() -> str:
    return urlparse(site_base_url()).netloc


def route_to_public_file(route: str) -> Path:
    if route == "/":
        return PUBLIC_DIR / "index.html"

    normalized = normalize_route(route, allow_file_paths=True)
    if normalized is None:
        raise AuditError(f"cannot map route to public file: {route}")

    if normalized.endswith(".xml"):
        return PUBLIC_DIR / normalized.lstrip("/")

    if normalized.endswith(".html"):
        return PUBLIC_DIR / normalized.lstrip("/")

    return PUBLIC_DIR / normalized.strip("/") / "index.html"


def public_file_to_route(path: Path) -> str | None:
    relative = path.relative_to(PUBLIC_DIR)
    if relative.as_posix() == "index.html":
        return "/"
    if relative.name != "index.html":
        return None
    return f"/{'/'.join(relative.parts[:-1])}/"


def parse_html_page(path: Path) -> dict:
    parser = PageParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return {
        "canonical_href": parser.canonical_href,
        "robots": parser.robots,
        "links": parser.links,
    }


def build_page_index() -> dict[str, dict]:
    if not PUBLIC_DIR.exists():
        raise AuditError("public/ does not exist; run `hugo build` first")

    pages: dict[str, dict] = {}
    for path in sorted(PUBLIC_DIR.rglob("index.html")):
        route = public_file_to_route(path)
        if route is None:
            continue
        parsed = parse_html_page(path)
        pages[route] = {
            "file": path,
            "route": route,
            "canonical_href": parsed["canonical_href"],
            "robots": parsed["robots"],
            "links": parsed["links"],
        }
    return pages


def vercel_redirects() -> dict[str, str]:
    config = load_json(VERCEL_CONFIG_PATH)
    redirects: dict[str, str] = {}

    for item in config.get("redirects", []):
        source = normalize_route(item.get("source", ""), allow_file_paths=True)
        destination = normalize_route(item.get("destination", ""), allow_file_paths=True)
        if source and destination:
            redirects[source] = destination

    for item in config.get("routes", []):
        status_code = item.get("status") or item.get("statusCode")
        if status_code not in {301, 302, 307, 308}:
            continue
        source = normalize_route(item.get("src", ""), allow_file_paths=True)
        destination = normalize_route(item.get("dest", ""), allow_file_paths=True)
        if source and destination:
            redirects[source] = destination

    return redirects


def raw_config_route(value: str) -> str | None:
    if not value:
        return None
    parsed = urlparse(value)
    if parsed.scheme in {"http", "https"} and parsed.netloc and parsed.netloc != site_netloc():
        return None
    path = parsed.path if parsed.scheme else value.split("#", 1)[0].split("?", 1)[0]
    if not path.startswith("/"):
        return None
    return path.replace("\\)", ")").replace("\\(", "(")


def vercel_redirect_source_variants() -> dict[str, set[str]]:
    config = load_json(VERCEL_CONFIG_PATH)
    variants: dict[str, set[str]] = {}

    for item in config.get("redirects", []):
        raw_source = raw_config_route(item.get("source", ""))
        normalized_source = normalize_route(item.get("source", ""), allow_file_paths=True)
        if raw_source and normalized_source:
            variants.setdefault(normalized_source, set()).add(raw_source)

    for item in config.get("routes", []):
        status_code = item.get("status") or item.get("statusCode")
        if status_code not in {301, 302, 307, 308}:
            continue
        raw_source = raw_config_route(item.get("src", ""))
        normalized_source = normalize_route(item.get("src", ""), allow_file_paths=True)
        if raw_source and normalized_source:
            variants.setdefault(normalized_source, set()).add(raw_source)

    return variants


def target_route_for_slug(slug: str) -> str:
    return f"/blog/{slug}/"


def current_canonical_routes() -> set[str]:
    routes = {"/", "/about/", "/blog/"}
    routes.update(target_route_for_slug(slug) for slug in existing_blog_slugs())
    return routes


def ensure_policy_shape(policy: dict) -> None:
    missing_keys = [
        key
        for key in ("ghost_policy_stage", "canonical_policy", "priority_batches", "discoverability", "ghost_urls", "malformed_urls")
        if key not in policy
    ]
    if missing_keys:
        raise AuditError(f"url_policy.json is missing keys: {', '.join(missing_keys)}")

    for command in REQUIRED_COMMANDS:
        if not isinstance(command, str):
            raise AuditError("invalid required command configuration")


def all_target_slugs(policy: dict) -> list[str]:
    targets: list[str] = []
    for batch in ("batch_a", "batch_b"):
        targets.extend(policy["priority_batches"].get(batch, []))
    return targets


def ensure_known_slugs_exist(policy: dict) -> list[str]:
    slugs = existing_blog_slugs()
    missing: list[str] = []
    for slug in all_target_slugs(policy):
        if slug not in slugs:
            missing.append(slug)
    for slug in policy["discoverability"].get("donor_pages", []):
        if slug not in slugs:
            missing.append(slug)
    return sorted(set(missing))


def iter_policy_entries(policy: dict) -> Iterable[tuple[str, dict]]:
    for key in ("ghost_urls", "malformed_urls"):
        for entry in policy.get(key, []):
            yield key, entry


def ensure_policy_entries_unique(policy: dict) -> None:
    seen: set[str] = set()
    duplicates: list[str] = []
    for _, entry in iter_policy_entries(policy):
        path = entry.get("path")
        if not isinstance(path, str):
            raise AuditError("each policy entry must contain a string `path`")
        if path in seen:
            duplicates.append(path)
        seen.add(path)
    if duplicates:
        raise AuditError(f"duplicate policy paths: {', '.join(sorted(duplicates))}")


def command_summary(policy: dict) -> int:
    missing_slugs = ensure_known_slugs_exist(policy)
    blog_slugs = existing_blog_slugs()
    clear_aliases = sum(1 for entry in policy["ghost_urls"] if entry.get("status") == "redirect" and entry.get("must_implement"))
    unresolved_ghosts = sum(1 for entry in policy["ghost_urls"] if entry.get("status") == "needs_policy")
    unresolved_malformed = sum(1 for entry in policy["malformed_urls"] if entry.get("status") == "needs_policy")

    print(f"blog_posts={len(blog_slugs)}")
    print(f"batch_a={len(policy['priority_batches'].get('batch_a', []))}")
    print(f"batch_b={len(policy['priority_batches'].get('batch_b', []))}")
    print(f"ghost_urls={len(policy['ghost_urls'])}")
    print(f"malformed_urls={len(policy['malformed_urls'])}")
    print(f"ghost_policy_stage={policy['ghost_policy_stage']}")
    print(f"clear_aliases={clear_aliases}")
    print(f"unresolved_ghosts={unresolved_ghosts}")
    print(f"unresolved_malformed={unresolved_malformed}")
    print(f"site_base_url={policy['canonical_policy']['site_base_url']}")

    if missing_slugs:
        print(f"missing_slugs={', '.join(missing_slugs)}", file=sys.stderr)
        return 1

    return 0


def check_policy_entry_statuses(policy: dict) -> list[str]:
    issues: list[str] = []

    for group, entry in iter_policy_entries(policy):
        path = entry["path"]
        status = entry.get("status")
        allowed = ALLOWED_GHOST_STATUSES if group == "ghost_urls" else ALLOWED_MALFORMED_STATUSES
        if status not in allowed:
            issues.append(f"{path}: invalid status `{status}`")
            continue

        target = entry.get("target")
        if status in {"redirect", "restore"}:
            if not isinstance(target, str) or not normalize_route(target, allow_file_paths=True):
                issues.append(f"{path}: status `{status}` requires a valid `target`")

        if status == "redirect" and isinstance(target, str):
            target_slug = target.strip("/").split("/")[-1]
            if target.startswith("/blog/") and target_slug not in existing_blog_slugs():
                issues.append(f"{path}: redirect target does not exist in content/blog ({target})")

    return issues


def is_redirect_implemented(entry: dict, redirects: dict, source_variants: dict[str, set[str]]) -> bool:
    source = normalize_route(entry["path"], allow_file_paths=True)
    target = normalize_route(entry.get("target", ""), allow_file_paths=True)
    if source is None or target is None:
        return False
    return redirects.get(source) == target and source in source_variants.get(source, set())


def is_restore_implemented(entry: dict) -> bool:
    target = normalize_route(entry.get("target", ""), allow_file_paths=True)
    if target is None or not target.startswith("/blog/"):
        return False
    return target.strip("/").split("/")[-1] in existing_blog_slugs()


def command_check_ghosts(policy: dict) -> int:
    issues = check_policy_entry_statuses(policy)
    ensure_policy_entries_unique(policy)

    stage = policy["ghost_policy_stage"]
    redirects = vercel_redirects()
    source_variants = vercel_redirect_source_variants()

    if stage not in {"inventory", "decisioned", "implemented"}:
        issues.append(f"unknown ghost_policy_stage `{stage}`")

    if stage in {"decisioned", "implemented"}:
        unresolved = [
            entry["path"]
            for entry in policy["ghost_urls"]
            if entry.get("status") == "needs_policy"
        ]
        if unresolved:
            issues.append(f"ghost URLs still unresolved: {', '.join(unresolved)}")

    for group, entry in iter_policy_entries(policy):
        if not entry.get("must_implement"):
            continue

        if stage == "inventory":
            continue

        status = entry.get("status")
        path = entry["path"]
        implemented_flag = bool(entry.get("implemented"))

        if not implemented_flag:
            issues.append(f"{path}: must_implement is true but implemented is false")
            continue

        if status == "redirect" and not is_redirect_implemented(entry, redirects, source_variants):
            issues.append(f"{path}: redirect marked implemented but not found in vercel.json")
        elif status == "restore" and not is_restore_implemented(entry):
            issues.append(f"{path}: restore marked implemented but target content is missing")

    if issues:
        for issue in issues:
            print(issue, file=sys.stderr)
        return 1

    print(
        "ghost-url-policy-ok "
        f"(stage={stage}, ghosts={len(policy['ghost_urls'])}, malformed={len(policy['malformed_urls'])})"
    )
    return 0


def command_check_canonical(policy: dict) -> int:
    base_url = policy["canonical_policy"]["site_base_url"].rstrip("/")
    pages = build_page_index()
    issues: list[str] = []
    blog_routes = sorted(route for route in current_canonical_routes() if route.startswith("/blog/") and route != "/blog/")

    for route in blog_routes:
        page = pages.get(route)
        if page is None:
            issues.append(f"{route}: rendered page is missing from public/")
            continue

        canonical_href = page["canonical_href"]
        expected = f"{base_url}{route}"

        if canonical_href != expected:
            issues.append(f"{route}: canonical mismatch ({canonical_href!r} != {expected!r})")

    if issues:
        for issue in issues:
            print(issue, file=sys.stderr)
        return 1

    print(f"canonical-ok (checked={len(blog_routes)})")
    return 0


def route_exists_in_public(route: str) -> bool:
    return route_to_public_file(route).exists()


def command_check_sitemap(policy: dict) -> int:
    sitemap_path = PUBLIC_DIR / "sitemap.xml"
    if not sitemap_path.exists():
        raise AuditError("public/sitemap.xml does not exist; run `hugo build` first")

    root = ET.fromstring(sitemap_path.read_text(encoding="utf-8"))
    namespace = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = [element.text or "" for element in root.findall("sm:url/sm:loc", namespace)]
    routes = [normalize_route(url, allow_file_paths=True) for url in urls]
    issues: list[str] = []
    forbidden_ghost_routes = {
        normalize_route(entry["path"], allow_file_paths=True)
        for entry in policy["ghost_urls"]
        if entry.get("status") != "restore"
    }

    if "/" not in routes:
        issues.append("sitemap is missing /")
    if "/about/" not in routes:
        issues.append("sitemap is missing /about/")

    for route in routes:
        if route is None:
            issues.append("sitemap contains an invalid URL")
            continue
        if route.startswith("/tags/"):
            issues.append(f"sitemap should not include taxonomy route {route}")
        if route.startswith("/blog/") and route != "/blog/" and not route.endswith("/"):
            issues.append(f"sitemap contains a non-canonical blog route {route}")
        if route in forbidden_ghost_routes:
            issues.append(f"sitemap contains ghost URL {route}")
        if not route_exists_in_public(route):
            issues.append(f"sitemap route does not exist in public/: {route}")

    pages = build_page_index()
    for route in routes:
        if route in pages:
            robots_values = " ".join(pages[route]["robots"]).lower()
            if "noindex" in robots_values:
                issues.append(f"sitemap includes noindex page {route}")

    if issues:
        for issue in issues:
            print(issue, file=sys.stderr)
        return 1

    print(f"sitemap-ok (urls={len(routes)})")
    return 0


def sitemap_routes() -> set[str]:
    sitemap_path = PUBLIC_DIR / "sitemap.xml"
    if not sitemap_path.exists():
        raise AuditError("public/sitemap.xml does not exist; run `hugo build` first")

    root = ET.fromstring(sitemap_path.read_text(encoding="utf-8"))
    namespace = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    return {
        route
        for route in (normalize_route(element.text or "", allow_file_paths=True) for element in root.findall("sm:url/sm:loc", namespace))
        if route
    }


def indexable_pages(pages: dict[str, dict]) -> dict[str, dict]:
    result: dict[str, dict] = {}
    for route, page in pages.items():
        robots_values = " ".join(page["robots"]).lower()
        if "noindex" in robots_values:
            continue
        result[route] = page
    return result


def normalize_internal_link(href: str, route: str) -> str | None:
    if not href or href.startswith("#"):
        return None
    parsed = urlparse(href)
    if parsed.scheme in {"http", "https"} and parsed.netloc and parsed.netloc != site_netloc():
        return None
    absolute = href if href.startswith("/") else urlparse(urljoin(route, href)).path
    return normalize_route(absolute, allow_file_paths=True)


def command_check_target_links(policy: dict) -> int:
    pages = {
        route: page
        for route, page in indexable_pages(build_page_index()).items()
        if route in current_canonical_routes()
    }
    hub_routes = {normalize_route(route, allow_file_paths=True) for route in policy["discoverability"].get("hub_routes", [])}
    vague_anchor_texts = {text.lower() for text in policy["discoverability"].get("vague_anchor_texts", [])}
    min_links = int(policy["discoverability"].get("min_internal_donor_links", 0))
    target_routes = {target_route_for_slug(slug): slug for slug in all_target_slugs(policy)}
    donors_for_target: dict[str, set[str]] = {route: set() for route in target_routes}
    hub_hits: dict[str, set[str]] = {route: set() for route in target_routes}
    explicit_anchor_seen: dict[str, bool] = {route: False for route in target_routes}

    for route, page in pages.items():
        for href, anchor_text in page["links"]:
            normalized = normalize_internal_link(href, route)
            if normalized not in target_routes:
                continue

            if route == normalized:
                continue

            donors_for_target[normalized].add(route)
            if route in hub_routes:
                hub_hits[normalized].add(route)
            if anchor_text and anchor_text.lower() not in vague_anchor_texts:
                explicit_anchor_seen[normalized] = True

    issues: list[str] = []
    for route, slug in target_routes.items():
        donor_count = len(donors_for_target[route])
        if donor_count < min_links:
            issues.append(f"{slug}: only {donor_count} donor links found (need {min_links})")
        if not hub_hits[route]:
            issues.append(f"{slug}: missing link from homepage, /blog/, or another configured hub route")
        if not explicit_anchor_seen[route]:
            issues.append(f"{slug}: no explicit anchor text found in donor links")

    if issues:
        for issue in issues:
            print(issue, file=sys.stderr)
        return 1

    print(f"target-links-ok (targets={len(target_routes)}, min_links={min_links})")
    return 0


def iter_source_files() -> Iterable[Path]:
    seen: set[Path] = set()
    for pattern in SOURCE_LINK_GLOBS:
        for path in REPO_ROOT.glob(pattern):
            if path.is_file() and path not in seen:
                seen.add(path)
                yield path


def source_link_hrefs(text: str) -> Iterable[tuple[int, str]]:
    for line_number, line in enumerate(text.splitlines(), start=1):
        for regex in (MARKDOWN_LINK_RE, HTML_HREF_RE):
            for match in regex.finditer(line):
                yield line_number, match.group(1)
        for match in BARE_SITE_URL_RE.finditer(line):
            yield line_number, match.group(0).rstrip(".,;:")


def href_to_internal_path(href: str) -> str | None:
    if not href or href.startswith("#"):
        return None

    parsed = urlparse(href)
    if parsed.scheme and parsed.scheme not in {"http", "https"}:
        return None
    if parsed.scheme in {"http", "https"} and parsed.netloc and parsed.netloc != site_netloc():
        return None

    path = parsed.path if parsed.scheme else href.split("#", 1)[0].split("?", 1)[0]
    if not path.startswith("/"):
        return None
    return path.replace("\\)", ")").replace("\\(", "(")


def redirect_source_routes(policy: dict) -> set[str]:
    routes = set(vercel_redirects())
    for _, entry in iter_policy_entries(policy):
        if entry.get("status") == "redirect":
            route = normalize_route(entry.get("path", ""), allow_file_paths=True)
            if route:
                routes.add(route)
    return routes


def command_check_redirect_sources(policy: dict) -> int:
    existing_routes = {target_route_for_slug(slug) for slug in existing_blog_slugs()}
    redirect_routes = redirect_source_routes(policy)
    issues: list[str] = []

    for path in sorted(iter_source_files()):
        text = path.read_text(encoding="utf-8")
        relative_path = path.relative_to(REPO_ROOT)
        for line_number, href in source_link_hrefs(text):
            internal_path = href_to_internal_path(href)
            if internal_path is None:
                continue

            normalized = normalize_route(internal_path, allow_file_paths=True)
            if "{" in internal_path or "}" in internal_path:
                issues.append(
                    f"{relative_path}:{line_number}: template-looking internal URL `{href}`; do not expose placeholders as crawlable URLs"
                )
                continue

            if normalized in redirect_routes:
                issues.append(
                    f"{relative_path}:{line_number}: links to redirect source `{href}`; use final canonical target"
                )
                continue

            if (
                internal_path.startswith("/blog/")
                and not internal_path.endswith("/")
                and "." not in Path(internal_path).name
                and normalized in existing_routes
            ):
                issues.append(
                    f"{relative_path}:{line_number}: slashless internal blog link `{href}`; use `{normalized}`"
                )

    if issues:
        for issue in issues:
            print(issue, file=sys.stderr)
        return 1

    print("redirect-sources-ok")
    return 0


def blog_slug_from_route(route: str | None) -> str | None:
    if not route or not route.startswith("/blog/") or route == "/blog/":
        return None
    return route.strip("/").split("/")[-1]


def donor_counts_for_pages(pages: dict[str, dict]) -> Counter[str]:
    indexable = {
        route: page
        for route, page in indexable_pages(pages).items()
        if route in current_canonical_routes()
    }
    donors_by_target: dict[str, set[str]] = {}

    for source_route, page in indexable.items():
        for href, _ in page["links"]:
            normalized = normalize_internal_link(href, source_route)
            if normalized is None or normalized == source_route:
                continue
            donors_by_target.setdefault(normalized, set()).add(source_route)

    return Counter({route: len(donors) for route, donors in donors_by_target.items()})


def route_type_for_gsc_url(url: str, redirect_routes: set[str]) -> tuple[str, str | None, str | None]:
    parsed = urlparse(url)
    host = parsed.netloc
    path = parsed.path

    if host and host != site_netloc():
        if host == f"www.{site_netloc()}":
            normalized = normalize_route(path, allow_file_paths=True)
            return "www-host-variant", normalized, blog_slug_from_route(normalized)
        return "out-of-scope-host", None, None

    if path in {"/blog", "/blog/"}:
        return "blog-index", "/blog/", None

    raw_path = path.replace("\\)", ")").replace("\\(", "(")
    normalized = normalize_route(raw_path, allow_file_paths=True)
    slug = blog_slug_from_route(normalized)

    if raw_path.startswith("/tags/"):
        return "taxonomy-noindex", normalized, None
    if normalized in redirect_routes:
        return "alias-or-redirect-source", normalized, slug
    if raw_path.startswith("/blog/") and not raw_path.endswith("/") and "." not in Path(raw_path).name and slug in existing_blog_slugs():
        return "slashless-blog", normalized, slug
    if normalized in current_canonical_routes():
        if normalized.startswith("/blog/") and normalized != "/blog/":
            return "canonical-blog", normalized, slug
        return "canonical-page", normalized, None
    return "unknown", normalized, slug


def local_status_for_gsc_url(url: str, pages: dict[str, dict], sitemap: set[str], donor_counts: Counter[str], redirect_routes: set[str]) -> dict:
    route_type, route, slug = route_type_for_gsc_url(url, redirect_routes)
    page = pages.get(route or "")
    robots_values = " ".join(page["robots"]).lower() if page else ""
    expected_canonical = f"{site_base_url().rstrip('/')}{route}" if route else None

    return {
        "url": url,
        "host": urlparse(url).netloc,
        "route": route,
        "slug": slug,
        "route_type": route_type,
        "content_exists": bool(slug and slug in existing_blog_slugs()),
        "rendered": bool(page),
        "canonical_self": bool(page and page["canonical_href"] == expected_canonical),
        "canonical_href": page["canonical_href"] if page else None,
        "in_sitemap": bool(route and route in sitemap),
        "noindex": "noindex" in robots_values,
        "donor_count": int(donor_counts[route]) if route else 0,
    }


def command_classify_gsc_backlog(policy: dict, inventory_path: Path) -> int:
    inventory = load_json(inventory_path)
    pages = build_page_index()
    sitemap = sitemap_routes()
    donor_counts = donor_counts_for_pages(pages)
    redirect_routes = redirect_source_routes(policy)
    issues: list[str] = []
    route_type_counts: Counter[str] = Counter()
    reason_counts: Counter[str] = Counter()
    low_donor_routes: set[str] = set()

    reasons = inventory.get("reasons")
    if not isinstance(reasons, list):
        raise AuditError(f"{inventory_path}: expected `reasons` list")

    total_examples = 0
    for reason in reasons:
        reason_name = reason.get("reason", "unknown")
        examples = reason.get("examples", [])
        if not isinstance(examples, list):
            issues.append(f"{reason_name}: expected examples list")
            continue

        affected = reason.get("affected_pages")
        if isinstance(affected, int) and affected != len(examples):
            issues.append(f"{reason_name}: affected_pages={affected} but examples={len(examples)}")

        for example in examples:
            url = example.get("url")
            if not isinstance(url, str):
                issues.append(f"{reason_name}: example is missing url")
                continue
            total_examples += 1
            reason_counts[reason_name] += 1
            status = local_status_for_gsc_url(url, pages, sitemap, donor_counts, redirect_routes)
            route_type_counts[status["route_type"]] += 1

            route_type = status["route_type"]
            if route_type in {"canonical-blog", "canonical-page", "slashless-blog", "www-host-variant", "blog-index"}:
                route = status["route"]
                if not status["rendered"]:
                    issues.append(f"{url}: normalized route is not rendered locally ({route})")
                if route_type != "blog-index" and not status["in_sitemap"]:
                    issues.append(f"{url}: normalized route is missing from sitemap ({route})")
                if status["rendered"] and not status["canonical_self"]:
                    issues.append(f"{url}: canonical mismatch ({status['canonical_href']} != {site_base_url().rstrip('/')}{route})")
                if status["noindex"]:
                    issues.append(f"{url}: normalized route is noindex ({route})")
                if route_type in {"canonical-blog", "slashless-blog"} and status["donor_count"] < 3 and route:
                    low_donor_routes.add(route)

    if issues:
        for issue in issues:
            print(issue, file=sys.stderr)
        return 1

    print(f"gsc-backlog-ok (examples={total_examples})")
    print("by_reason=" + ", ".join(f"{reason}:{count}" for reason, count in sorted(reason_counts.items())))
    print("by_route_type=" + ", ".join(f"{route_type}:{count}" for route_type, count in sorted(route_type_counts.items())))
    print(f"low_donor_routes={len(low_donor_routes)}")
    for route in sorted(low_donor_routes):
        print(f"low_donor {route} donors={donor_counts[route]}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="SEO audit helpers for sereja.tech")
    subparsers = parser.add_subparsers(dest="command", required=True)

    for command in REQUIRED_COMMANDS:
        subparsers.add_parser(command)

    gsc_backlog_parser = subparsers.add_parser(GSC_BACKLOG_COMMAND)
    gsc_backlog_parser.add_argument(
        "inventory_path",
        nargs="?",
        default=str(DEFAULT_GSC_BACKLOG_PATH),
        help="Path to a GSC backlog inventory JSON file",
    )

    args = parser.parse_args()
    policy = load_json(POLICY_PATH)
    ensure_policy_shape(policy)

    if args.command == "summary":
        return command_summary(policy)
    if args.command == "check-ghosts":
        return command_check_ghosts(policy)
    if args.command == "check-canonical":
        return command_check_canonical(policy)
    if args.command == "check-sitemap":
        return command_check_sitemap(policy)
    if args.command == "check-target-links":
        return command_check_target_links(policy)
    if args.command == "check-redirect-sources":
        return command_check_redirect_sources(policy)
    if args.command == GSC_BACKLOG_COMMAND:
        return command_classify_gsc_backlog(policy, Path(args.inventory_path))

    raise AuditError(f"unsupported command: {args.command}")


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AuditError as exc:
        print(exc, file=sys.stderr)
        raise SystemExit(1)
