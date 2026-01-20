# sereja.tech

**Персональный блог про вайбкодинг, Claude Code и AI-инструменты.**

Сайт с 30+ статьями о разработке с AI, автоматизации рабочего процесса и инженерии многоагентных систем. Собирается Hugo, деплоится на Vercel.

## Что внутри

- **Статьи про Claude Code** — как использовать Claude Code для реальных задач, примеры скиллов
- **AI-рабочие процессы** — video pipelines, RAG с embeddings, Telegram боты, многоагентные системы
- **Инженерия** — автоматизация, видеобработка, MIDI-контроль, навигация в терминале
- **Практические решения** — от SEO для AI-эры до health checks для скриптов

## Быстрый старт

```bash
# Разработка с черновиками
hugo server -D

# Открыть http://localhost:1313

# Production build
hugo build

# Собранный сайт в public/
```

## Структура

| Путь | Назначение |
|------|-----------|
| `content/blog/*.md` | Статьи в markdown |
| `layouts/` | Hugo шаблоны и компоненты |
| `static/` | JS, CSS, изображения |
| `public/` | Собранный сайт (gitignored) |
| `hugo.toml` | Конфиг Hugo |

## Технология

| Слой | Стек |
|------|------|
| SSG | Hugo 0.154.5 |
| Хостинг | Vercel |
| Синтаксис | GitHub style highlighting |
| Фид | RSS для blog section |
| SEO | robots.txt, Open Graph, JSON-LD |

## Ссылки

- **Блог:** https://sereja.tech
- **Telegram:** https://t.me/ris_ai (личные заметки)
- **Комьюнити:** https://t.me/vibecod3rs (вайбкодеры)
- **YouTube:** https://www.youtube.com/@serejaris
- **Twitter:** https://x.com/riiiiiiiiss

## Скиллы Claude Code

Для быстрой работы с сайтом используй эти скиллы в Claude Code:

| Скилл | Триггер | Что делает |
|-------|---------|-----------|
| `blog-post` | "статья", "блог" | Создаёт новую статью с frontmatter |
| `deaify-text` | "убери аишность" | Делает текст более человечным |
| `claude-md-writer` | "обнови CLAUDE.md" | Обновляет инструкции для Claude |
| `readme-generator` | "напиши README" | Генерирует README |

## Разработка

```bash
# Локальный сервер с hot reload
hugo server -D

# Только статика (без Hugo)
python3 -m http.server

# Собрать для production
hugo build
```

Статьи пишутся в `content/blog/` markdown-ом. Hugo автоматически генерирует HTML с путями `/blog/:filename`.

## Лицензия

MIT
