# sereja.tech

Персональный блог про вайбкодинг и Claude Code. Hugo + Vercel.

## Boundaries

| | Rule |
|---|------|
| ✅ Always | Проверять `hugo server -D` перед коммитом |
| ⚠️ Ask | Изменения в layouts/, удаление статей |
| 🚫 Never | Редактировать public/ напрямую, пушить в main без проверки |

## Commands

| Task | Command |
|------|---------|
| Dev | `hugo server -D` |
| Build | `hugo build` |
| OG preview | `./scripts/og-preview/generate.sh --title "..." --output static/images/blog/{slug}-preview.png` |
| Static preview | `python3 -m http.server` |

## Architecture

| Path | Purpose |
|------|---------|
| `content/blog/*.md` | Статьи |
| `layouts/` | Hugo шаблоны |
| `static/` | JS, images |
| `scripts/og-preview/` | OG-превью генератор (HTML → Playwright → PNG 1200×630) |
| `hugo.toml` | Конфиг Hugo |
| `index.html` | Legacy главная (вне Hugo) |

## Blog Workflow

Статьи через skill `blog-post`:
1. `content/blog/{slug}.md` + frontmatter
2. OG-превью: `./scripts/og-preview/generate.sh --title "..." [--command "..." --tools "a,b,c" --subtitle "..."] --output static/images/blog/{slug}-preview.png`
3. `hugo build` → `public/`

Frontmatter: title, date, description, tags, image.
SEO: title ≤60 chars, description ≤160 chars.

OG Preview: всегда генерировать через `scripts/og-preview/generate.sh`. Опции: `--title` (обязательно), `--subtitle`, `--command`, `--tools` (через запятую), `--visual` (эмодзи). Результат: 1200×630 PNG.

Permalinks: `/blog/:filename`. RSS только для blog.

## Pre-commit Hook

Validates staged `content/blog/*.md` files before commit:
- `title` ≤60 chars (required)
- `description` ≤160 chars (required)
- `date` present and YYYY-MM-DD format (required)
- `tags` non-empty array (required)
- `image` points to existing file in `static/` (warning if missing)

Install after cloning: `./scripts/install-hooks.sh`
Run standalone: `./scripts/validate-blog-post.sh [file ...]`
Skip: `git commit --no-verify`

## Testing

| Check | Command |
|-------|---------|
| Dev server | `hugo server -D` → localhost:1313 |
| Build | `hugo build` (no errors) |
| Links | Manual check in browser |

## Deployment

Vercel: auto-deploy on push to main.

## Skills

| Skill | Trigger |
|-------|---------|
| `blog-post` | "статья", "блог" |
| `deaify-text` | "убери аишность" |
