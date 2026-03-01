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

Frontmatter: title, date, description, tags, image, knowledge.
SEO: title ≤60 chars, description ≤160 chars.

### knowledge блок (обязателен для каждой статьи)

```yaml
knowledge:
  problem: "Какую проблему решает статья (1 предложение)"
  solution: "Как решает (1 предложение)"
  pattern: "slug-format-pattern-name"
  tools: ["Tool1", "Tool2"]
  takeaways:
    - "Ключевой вывод 1 с конкретными числами"
    - "Ключевой вывод 2"
    - "Ключевой вывод 3"
  metrics:           # опционально
    key: value
  prerequisites:     # опционально
    - "Что нужно знать/иметь"
  related:           # опционально
    - slug: "other-article-slug"
      relation: "тип связи"
```

Обязательные поля: `problem`, `solution`, `pattern`, `tools`, `takeaways`.
Опциональные: `metrics`, `prerequisites`, `related`.
Язык: русский. Pattern: slug формат (lowercase, hyphens).

OG Preview: всегда генерировать через `scripts/og-preview/generate.sh`. Опции: `--title` (обязательно), `--subtitle`, `--command`, `--tools` (через запятую), `--visual` (эмодзи). Результат: 1200×630 PNG.

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
