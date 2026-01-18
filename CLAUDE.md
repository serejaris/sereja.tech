# sereja.tech

Персональный сайт и блог на Hugo.

## Commands

```bash
hugo server -D          # Dev с черновиками
hugo build              # Production → public/
python3 -m http.server  # Статика без Hugo
```

## Architecture

| Path | Purpose |
|------|---------|
| `content/blog/*.md` | Статьи в markdown |
| `layouts/` | Hugo шаблоны |
| `static/` | Статические файлы (JS, images) |
| `public/` | Собранный сайт (gitignored) |
| `docs/plans/` | Планы реализации |
| `docs/research/` | Research notes |
| `index.html` | Legacy главная (вне Hugo) |

## Blog

Статьи создаются через скилл `blog-post`:
1. Создаёт `content/blog/{slug}.md` с frontmatter
2. `hugo build` генерирует HTML в `public/`

Frontmatter: title, date, description, tags.

## Hugo Config

- Permalinks: `/blog/:filename`
- Syntax highlighting: github style
- RSS: только для blog section

## Deployment

Vercel собирает Hugo при пуше в main.

## Related Skills

| Skill | Триггер |
|-------|---------|
| `blog-post` | "статья", "блог" |
| `deaify-text` | "убери аишность" |
| `claude-md-writer` | "обнови CLAUDE.md" |
| `readme-generator` | "напиши README" |
