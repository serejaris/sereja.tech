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

## Architecture

| Path | Purpose |
|------|---------|
| `content/blog/*.md` | Статьи |
| `data/videos.yml` | 4 последних YouTube-видео для блока на главной (featured + 3) |
| `layouts/` | Hugo шаблоны |
| `static/` | JS, images |
| `scripts/og-preview/` | OG-превью генератор (HTML → Playwright → PNG 1200×630) |
| `hugo.toml` | Конфиг Hugo |

## YouTube Block

Секция «YouTube» на главной (`layouts/index.html`) — data-driven из `data/videos.yml`. Первая запись = featured iframe + подпись «Последнее видео: {label}». Следующие 3 — список с thumbnail 80×45 (грузятся с `i.ytimg.com/vi/{id}/mqdefault.jpg`).

Обновление = часть lifecycle стрима, **живёт не здесь**. Владелец процесса — `live-sereja-tech/AGENTS.md` § 9.1 «YouTube Broadcast Lifecycle», шаг «D+1 refresh». IDs/titles canonical в `~/Documents/GitHub/stats-youtube/videos.json`.

## Blog Workflow

Статьи через skill `blog-post`:
1. `content/blog/{slug}.md` + frontmatter
2. OG-превью: `./scripts/og-preview/generate.sh --title "..." [--command "..." --tools "a,b,c" --subtitle "..."] --output static/images/blog/{slug}-preview.png`
3. `hugo build` → `public/`

Frontmatter: title, date, description, tags, image.
SEO: title ≤60 chars, description ≤160 chars.

OG Preview: всегда генерировать через `scripts/og-preview/generate.sh`. Опции: `--title` (обязательно), `--subtitle`, `--command`, `--tools` (через запятую), `--visual` (эмодзи). Результат: 1200×630 PNG.

Permalinks: `/blog/:filename`. RSS только для blog.

### Посты по стримам (обязательный чеклист)

Если статья описывает стрим с экспериментами (есть репозиторий-песочница, как `serejaris/claude-fable`), в пост обязательно входят:

- Эмбед записи стрима `{{</* youtube ID */>}}` — на первом экране, сразу после вступления
- Ссылка на публичный репозиторий экспериментов — в начале текста, под плеером
- Для каждого показанного проекта: ссылка на живой деплой (проверить, что отвечает) + на папку проекта в репо
- Скриншоты работающих экземпляров: снять через Chrome (in-game/in-app кадр, не только стартовый экран), ужать до 1280px, положить в `static/images/blog/`
- Оригинальные промпты проектов (живут в `{project}/prompt.md` репо-песочницы) — в callout-блоках, слегка причёсанные
- Рассказать про все артефакты стрима, не только главные: скиллы, документы (GDD, design-review), side-эксперименты

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
