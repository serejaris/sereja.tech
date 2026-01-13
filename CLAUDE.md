# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Персональный сайт-визитка sereja.tech — статическая страница без билд-процесса.

## Development

```bash
python3 -m http.server 8000
# или
npx serve .
```

## Architecture

- `index.html` — главная страница (monospace-дизайн, inline CSS)
- `vercel.json` — cleanUrls для URL без .html
- `blog/` — SEO-блог
  - `index.html` — список статей между `<!-- POSTS_START/END -->`
  - `sitemap.xml` — карта сайта между `<!-- SITEMAP_POSTS_START/END -->`
  - `{slug}.html` — статьи (light theme, monospace, Prism.js для кода)

## Blog

Статьи создаются через скилл `blog-post`. При добавлении статьи обновлять:
1. `blog/index.html` — добавить `<li>` внутри POSTS маркеров
2. `blog/sitemap.xml` — добавить `<url>` внутри SITEMAP_POSTS маркеров

Шаблон статьи: monospace font, JSON-LD schema, Open Graph мета-теги, секция Sources.
Референс: `blog/slash-commands-subagents.html`

## Deployment

GitHub Pages при пуше в main.

## Related Skills

| Skill | Триггер | Назначение |
|-------|---------|------------|
| `blog-post` | "статья", "блог" | Создание статей для блога |
| `deaify-text` | "убери аишность", "humanize" | Убрать AI-паттерны из текста |
| `claude-md-writer` | "создай CLAUDE.md" | Создание/рефакторинг CLAUDE.md |
| `readme-generator` | "напиши README" | Генерация README.md |
