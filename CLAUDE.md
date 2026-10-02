# sereja.tech Agent Guide

## Purpose and scope

- This repo is a single Hugo blog deployed to Vercel.
- Default work is article editing, metadata updates, and OG preview generation.
- Keep instructions operational and verified against the current repo layout.

## Canonical paths and services

- `content/blog/` — blog posts.
- `content/about/` — standalone about-page content.
- `layouts/` — Hugo templates, SEO partials, and shortcodes.
- `static/images/blog/` — OG preview images used by post frontmatter.
- `static/analytics.js`, `static/robots.txt`, `static/llms.txt`, `static/llms-full.txt` — static site assets.
- `scripts/og-preview/generate.sh` and `scripts/og-preview/template.html` — OG preview generator.
- `hugo.toml` — site config and permalinks.
- `vercel.json` and `.github/workflows/` — deployment and automation config.
- `public/` — generated output only.

## System boundaries

- Treat the repo as a static site; there is no app server, database, or migration layer here.
- Vercel deploys the generated Hugo output. Do not treat `public/` as source.
- Blog permalinks come from `hugo.toml` and resolve to `/blog/:contentbasename`.

## Safe defaults

- Prefer editing `content/blog/*.md` for content work.
- Before content, SEO, or analytics work, check repo issues and GitHub Project `ris © corp` (`gh issue list --repo serejaris/sereja.tech`, `gh project item-list 4 --owner serejaris`) for existing tasks, snapshots, and constraints.
- For new or updated posts, keep frontmatter explicit: `title`, `date`, `description`, `tags`, `image`.
- Generate OG images with `./scripts/og-preview/generate.sh`; do not hand-edit PNG files unless asked.
- Ignore `public/`, `.playwright-mcp/`, and ad hoc screenshots unless the task explicitly targets them.
- Verify repo reality before documenting paths; do not rely on stale assumptions.

## Allowed actions

- Add or update blog posts, frontmatter, links, and copy in content files.
- Generate or refresh OG preview images under `static/images/blog/`.
- Update safe static text assets when the task is clearly scoped to them.
- Run `hugo build` and short-lived `hugo server -D` checks.

## Confirmation-required actions

- Any change under `layouts/`.
- Changes to `hugo.toml`, `vercel.json`, or `.github/workflows/`.
- Deleting or renaming posts, changing filenames, or changing published slugs.
- Adding or changing analytics behavior in `static/analytics.js`.
- Pushing to a remote, merging, or deleting local user artifacts outside the task scope.

## Forbidden actions

- Never edit `public/` by hand.
- Never push directly to `main` without explicit confirmation.
- Never claim success without running the narrowest relevant validation.
- Never document nonexistent topology; for example, do not reference a root `index.html` unless it is actually present.

## Validation commands

- Content or metadata change: `hugo build`
- Local smoke test: `hugo server -D --bind 127.0.0.1 --baseURL http://127.0.0.1:1313`
- OG preview smoke test: `./scripts/og-preview/generate.sh --title "..." --output /tmp/preview.png`
- Approved layout or SEO change: `hugo build` plus a browser check on the affected page via local server

## Execution contract

- Report which files changed and why.
- Report which validations actually ran and which were skipped.
- Keep edits focused; do not clean up unrelated content or generated artifacts.
- These instructions apply on the next Codex or agent session after the file is saved.

## References

- `README.md`
- `hugo.toml`
- `vercel.json`
- `scripts/og-preview/generate.sh`
