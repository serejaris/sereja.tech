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
| Static preview | `python3 -m http.server` |

## Architecture

| Path | Purpose |
|------|---------|
| `content/blog/*.md` | Статьи |
| `layouts/` | Hugo шаблоны |
| `static/` | JS, images |
| `hugo.toml` | Конфиг Hugo |
| `index.html` | Legacy главная (вне Hugo) |

## Blog Workflow

Статьи через skill `blog-post`:
1. `content/blog/{slug}.md` + frontmatter
2. `hugo build` → `public/`

Frontmatter: title, date, description, tags.
SEO: title ≤60 chars, description ≤160 chars.

Permalinks: `/blog/:filename`. RSS только для blog.

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
