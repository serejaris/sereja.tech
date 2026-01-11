# Blog Design for sereja.tech

SEO-блог для закрепления экспертизы "Сережа Рис" по ключевым словам: вайбкодинг, Claude Code, AI-инструменты.

## Architecture

```
sereja.tech/
├── index.html              # Главная (добавить ссылку на блог)
├── blog/
│   ├── index.html          # Список статей
│   ├── {slug}.html         # Статьи
│   └── sitemap.xml         # Для Google
└── CLAUDE.md
```

**Принципы:**
- Zero-build — чистый HTML
- Self-contained — CSS inline в каждой статье
- SEO-first — JSON-LD, OG-теги, canonical URLs

## URL Structure

`https://sereja.tech/blog/{article-slug}`

## Skill: blog-post

**Location:** `~/.claude/skills/blog-post/SKILL.md`

**Workflow:**
1. GATHER → контекст из сессии/промпта
2. RESEARCH → Exa MCP для источников
3. WRITE → HTML с SEO-оптимизацией
4. PUBLISH → запись в `/Users/ris/Documents/GitHub/sereja.tech/blog/`
5. UPDATE → добавить в blog/index.html + sitemap.xml

**Triggers:** "блог", "статья", "blog post", "article", "напиши статью", "публикация"

## SEO Template

Каждая статья содержит:

```html
<title>{Заголовок} | Сережа Рис</title>
<meta name="author" content="Сережа Рис">
<link rel="canonical" href="https://sereja.tech/blog/{slug}">

<!-- JSON-LD -->
{
  "@type": "BlogPosting",
  "author": { "@type": "Person", "name": "Сережа Рис", "url": "https://sereja.tech" },
  "publisher": { "@type": "Person", "name": "Сережа Рис" }
}
```

**Структура:**
- Hero + Author block (имя, дата)
- Intro (3 коротких абзаца — hook)
- H2 секции с code blocks
- Callout cards (warning/insight)
- Sources (обязательно)
- Footer

**Стиль:** Brutalist-гибрид (как главная страница)

## Visual Style (v2)

Минималистичный стиль, совпадающий с главной страницей.

### База

```css
body {
  font-family: monospace;
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  line-height: 1.6;
  background: #fff;
  color: #000;
}

a { color: #0000EE; text-decoration: underline; }
a:visited { color: #551A8B; }
```

### Callouts (минималистичные)

```css
.callout {
  border: 1px solid #000;
  padding: 12px 16px;
  margin: 20px 0;
}
.callout.warning { border-left: 3px solid #c00; }
.callout.insight { border-left: 3px solid #060; }
.callout strong { display: block; margin-bottom: 4px; }
```

### Подсветка синтаксиса

Prism.js с минималистичной темой:
```html
<link href="https://unpkg.com/prismjs/themes/prism.css" rel="stylesheet">
<script src="https://unpkg.com/prismjs"></script>
```

### Код

```css
pre {
  background: #f5f5f5;
  border: 1px solid #ddd;
  padding: 12px;
  overflow-x: auto;
}
code { font-family: monospace; }
```

## blog/index.html

```html
<h1>Блог</h1>
<p class="intro">Статьи про вайбкодинг, Claude Code и AI-инструменты</p>

<ul class="posts">
  <li>
    <a href="/blog/{slug}">
      <span class="date">DD MMM YYYY</span>
      <span class="title">Заголовок</span>
    </a>
  </li>
</ul>
```

Новые статьи добавляются в начало списка автоматически.

## sitemap.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://sereja.tech/blog/</loc></url>
  <url><loc>https://sereja.tech/blog/{slug}</loc></url>
</urlset>
```

Обновляется при каждой публикации.

## Implementation Steps

1. **Инфраструктура блога:**
   - Создать blog/index.html
   - Создать blog/sitemap.xml
   - Добавить ссылку "Блог" на главную
   - Обновить CLAUDE.md

2. **Создать скилл blog-post:**
   - Использовать superpowers:writing-skills
   - Шаблон на основе slash-commands-subagents.html
   - Логика автообновления index и sitemap

3. **Тест:**
   - Запустить скилл из другого проекта
   - Проверить публикацию

## Reference

Пример статьи: `~/Documents/GitHub/ai-whisper/blog/slash-commands-subagents.html`
