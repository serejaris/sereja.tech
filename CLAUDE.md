# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Персональный сайт-визитка sereja.tech — статическая страница без билд-процесса.

## Development

Локальный сервер:
```bash
python3 -m http.server 8000
# или
npx serve .
```

Открыть http://localhost:8000

## Architecture

- `index.html` — главная страница с встроенными стилями (минималистичный monospace-дизайн)
- `style.css` — расширенные стили (не подключен)
- `blog/` — SEO-блог для экспертизы "Сережа Рис"
  - `index.html` — список статей (маркеры `<!-- POSTS_START/END -->`)
  - `sitemap.xml` — карта сайта (маркеры `<!-- SITEMAP_POSTS_START/END -->`)
  - `{slug}.html` — статьи с inline CSS, dark theme

## Blog

Статьи создаются через скилл `blog-post` из любого проекта. Скилл пишет напрямую в этот репозиторий.

Шаблон статьи: dark theme, Inter font, JSON-LD для SEO, обязательная секция Sources.

Референс: `~/Documents/GitHub/ai-whisper/blog/slash-commands-subagents.html`

## Deployment

Сайт деплоится автоматически через GitHub Pages при пуше в main.
