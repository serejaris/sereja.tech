# Hugo Migration Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Migrate sereja.tech blog from manual HTML files to Hugo static site generator for faster content creation.

**Architecture:** Hugo generates static HTML from Markdown + frontmatter. Templates handle SEO meta, JSON-LD, Open Graph. Shortcodes handle custom callout blocks. Vercel builds on push.

**Tech Stack:** Hugo v0.154.5, Vercel, PostHog analytics

---

## Task 1: Initialize Hugo Project

**Files:**
- Create: `hugo.toml`
- Create: `.gitignore` (add public/)

**Step 1: Initialize Hugo in existing directory**

```bash
cd /Users/ris/Documents/GitHub/sereja.tech
hugo new site . --force
```

**Step 2: Verify Hugo created structure**

Run: `ls -la`
Expected: `archetypes/`, `content/`, `layouts/`, `static/`, `hugo.toml`

**Step 3: Configure hugo.toml**

Replace generated `hugo.toml` with:

```toml
baseURL = 'https://sereja.tech/'
languageCode = 'ru'
title = 'Сережа Рис'
defaultContentLanguage = 'ru'

[permalinks]
  blog = '/blog/:filename'

[params]
  author = 'Сережа Рис'
  description = 'Статьи про вайбкодинг, Claude Code и AI-инструменты'
  twitter = '@riiiiiiiiss'

[markup]
  [markup.goldmark]
    [markup.goldmark.renderer]
      unsafe = true
  [markup.highlight]
    codeFences = true
    guessSyntax = true
    lineNos = false
    style = 'github'

[outputs]
  home = ['HTML']
  section = ['HTML', 'RSS']

[sitemap]
  changefreq = 'weekly'
  priority = 0.5
```

**Step 4: Add public/ to .gitignore**

```bash
echo "public/" >> .gitignore
```

**Step 5: Verify config works**

Run: `hugo config`
Expected: Shows config without errors

**Step 6: Commit**

```bash
git add hugo.toml .gitignore archetypes/
git commit -m "chore: initialize Hugo project structure"
```

---

## Task 2: Create Base Template

**Files:**
- Create: `layouts/_default/baseof.html`

**Step 1: Create layouts directory structure**

```bash
mkdir -p layouts/_default layouts/blog layouts/partials
```

**Step 2: Create baseof.html**

Create `layouts/_default/baseof.html`:

```html
<!DOCTYPE html>
<html lang="{{ .Site.LanguageCode }}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{ if .IsHome }}{{ .Site.Title }}{{ else }}{{ .Title }} | {{ .Site.Title }}{{ end }}</title>

  {{- partial "seo.html" . -}}

  <style>
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
    h1 { font-size: 24px; margin-bottom: 8px; line-height: 1.3; }
    h2 { font-size: 18px; margin-top: 30px; margin-bottom: 10px; }
    h3 { font-size: 16px; margin-top: 24px; margin-bottom: 8px; }
    p { margin-bottom: 15px; }
    .author { color: #666; font-size: 13px; margin-bottom: 24px; }
    .intro { color: #666; margin-bottom: 8px; }

    .callout {
      border: 1px solid #000;
      padding: 12px 16px;
      margin: 20px 0;
    }
    .callout.warning { border-left: 3px solid #c00; }
    .callout.insight { border-left: 3px solid #060; }
    .callout strong { display: block; margin-bottom: 4px; }
    .callout p { margin-bottom: 0; }

    pre {
      background: #f8f8f8;
      border: 2px solid #000;
      padding: 16px;
      overflow-x: auto;
      font-size: 13px;
      line-height: 1.5;
      margin: 24px 0;
    }
    code { font-family: monospace; background: #eee; padding: 1px 4px; }
    pre code { background: none; padding: 0; }

    table { width: 100%; border-collapse: collapse; margin: 20px 0; }
    th, td { border: 1px solid #000; padding: 8px; text-align: left; vertical-align: top; }
    th { background: #f5f5f5; }

    ul, ol { margin: 12px 0; padding: 0 0 0 1.2em; }
    li { margin-bottom: 4px; }

    blockquote {
      border-left: 3px solid #000;
      margin: 20px 0;
      padding: 8px 16px;
      font-style: italic;
      background: #f8f8f8;
    }
    blockquote p { margin: 0; }

    .sources { margin-top: 40px; padding-top: 20px; border-top: 1px solid #000; }
    .sources h3 { font-size: 14px; margin-bottom: 8px; }
    .sources ul { list-style: none; padding: 0; }
    .sources li { margin-bottom: 4px; }

    footer { margin-top: 30px; text-align: center; font-size: 13px; color: #666; }

    /* Blog list styles */
    .posts { list-style: none; padding: 0; }
    .posts li { margin-bottom: 12px; }
    .date { color: #666; font-size: 13px; margin-right: 8px; }
  </style>
</head>
<body>
  {{ block "main" . }}{{ end }}

  <script defer src="/_vercel/insights/script.js"></script>
  {{ if .IsPage }}<script src="/analytics.js"></script>{{ end }}
</body>
</html>
```

**Step 3: Test template syntax**

Run: `hugo --templateMetrics 2>&1 | head -20`
Expected: No template errors

**Step 4: Commit**

```bash
git add layouts/_default/baseof.html
git commit -m "feat: add base HTML template with styles"
```

---

## Task 3: Create SEO Partial

**Files:**
- Create: `layouts/partials/seo.html`

**Step 1: Create SEO partial with all meta tags**

Create `layouts/partials/seo.html`:

```html
<!-- SEO -->
<meta name="description" content="{{ .Description | default .Site.Params.description }}">
<meta name="author" content="{{ .Site.Params.author }}">
{{ with .Keywords }}<meta name="keywords" content="{{ delimit . ", " }}">{{ end }}
<link rel="canonical" href="{{ .Permalink }}">

<!-- Open Graph -->
<meta property="og:title" content="{{ .Title }}">
<meta property="og:description" content="{{ .Description | default .Site.Params.description }}">
<meta property="og:type" content="{{ if .IsPage }}article{{ else }}website{{ end }}">
<meta property="og:locale" content="ru_RU">
<meta property="og:url" content="{{ .Permalink }}">
<meta property="og:site_name" content="{{ .Site.Title }}">
{{ if .IsPage }}
<meta property="article:author" content="{{ .Site.Params.author }}">
<meta property="article:published_time" content="{{ .Date.Format "2006-01-02T15:04:05-07:00" }}">
{{ with .Params.section }}<meta property="article:section" content="{{ . }}">{{ end }}
{{ range .Params.tags }}<meta property="article:tag" content="{{ . }}">{{ end }}
{{ end }}

<!-- Twitter -->
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="{{ .Title }}">
<meta name="twitter:description" content="{{ .Description | default .Site.Params.description }}">
<meta name="twitter:creator" content="{{ .Site.Params.twitter }}">

<!-- JSON-LD -->
{{ if .IsPage }}
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "{{ .Title }}",
  "description": "{{ .Description }}",
  "author": {
    "@type": "Person",
    "name": "{{ .Site.Params.author }}",
    "url": "{{ .Site.BaseURL }}"
  },
  "publisher": {
    "@type": "Person",
    "name": "{{ .Site.Params.author }}",
    "url": "{{ .Site.BaseURL }}"
  },
  "datePublished": "{{ .Date.Format "2006-01-02" }}",
  "dateModified": "{{ .Lastmod.Format "2006-01-02" }}",
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "{{ .Permalink }}"
  },
  "wordCount": {{ .WordCount }},
  {{ with .Params.section }}"articleSection": "{{ . }}",{{ end }}
  "keywords": [{{ range $i, $tag := .Params.tags }}{{ if $i }}, {{ end }}"{{ $tag }}"{{ end }}],
  "inLanguage": "ru-RU"
}
</script>
{{ else }}
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Blog",
  "name": "{{ .Title }}",
  "description": "{{ .Site.Params.description }}",
  "url": "{{ .Permalink }}",
  "author": {
    "@type": "Person",
    "name": "{{ .Site.Params.author }}",
    "url": "{{ .Site.BaseURL }}"
  },
  "inLanguage": "ru-RU"
}
</script>
{{ end }}
```

**Step 2: Commit**

```bash
git add layouts/partials/seo.html
git commit -m "feat: add SEO partial with OG, Twitter, JSON-LD"
```

---

## Task 4: Create Blog Single Template

**Files:**
- Create: `layouts/blog/single.html`

**Step 1: Create single post template**

Create `layouts/blog/single.html`:

```html
{{ define "main" }}
<p><a href="/blog/">&larr; Блог</a></p>
<article>
  <h1>{{ .Title }}</h1>
  <p class="author">{{ .Site.Params.author }} · {{ .Date.Format "2 January 2006" }}</p>

  {{ with .Params.intro }}
  <p class="intro">{{ . }}</p>
  {{ end }}

  {{ .Content }}

  {{ with .Params.sources }}
  <div class="sources">
    <h3>Источники</h3>
    <ul>
      {{ range . }}
      <li><a href="{{ .url }}" target="_blank">{{ .title }}</a>{{ with .note }} — {{ . }}{{ end }}</li>
      {{ end }}
    </ul>
  </div>
  {{ end }}

  <footer>
    {{ .Date.Format "January 2006" }}
  </footer>
</article>
{{ end }}
```

**Step 2: Commit**

```bash
git add layouts/blog/single.html
git commit -m "feat: add blog single post template"
```

---

## Task 5: Create Blog List Template

**Files:**
- Create: `layouts/blog/list.html`
- Create: `content/blog/_index.md`

**Step 1: Create list template**

Create `layouts/blog/list.html`:

```html
{{ define "main" }}
<p><a href="/">&larr; sereja.tech</a></p>
<h1>Блог</h1>
<p class="intro">{{ .Site.Params.description }}</p>

<ul class="posts">
  {{ range .Pages.ByDate.Reverse }}
  <li>
    <span class="date">{{ .Date.Format "2 Jan 2006" }}</span>
    <a href="{{ .Permalink }}">{{ .Title }}</a>
  </li>
  {{ end }}
</ul>
{{ end }}
```

**Step 2: Create blog section index**

Create `content/blog/_index.md`:

```markdown
---
title: "Блог"
description: "Статьи про вайбкодинг, Claude Code и AI-инструменты"
---
```

**Step 3: Commit**

```bash
git add layouts/blog/list.html content/blog/_index.md
git commit -m "feat: add blog list template and section index"
```

---

## Task 6: Create Callout Shortcodes

**Files:**
- Create: `layouts/shortcodes/callout.html`

**Step 1: Create callout shortcode**

Create `layouts/shortcodes/callout.html`:

```html
{{ $type := .Get 0 | default "default" }}
<div class="callout {{ $type }}">
  {{ if .Get 1 }}<strong>{{ .Get 1 }}</strong>{{ end }}
  {{ .Inner | markdownify }}
</div>
```

**Step 2: Commit**

```bash
git add layouts/shortcodes/callout.html
git commit -m "feat: add callout shortcode for insight/warning blocks"
```

---

## Task 7: Move Static Assets

**Files:**
- Move: `blog/analytics.js` → `static/analytics.js`

**Step 1: Move analytics.js to static folder**

```bash
mv blog/analytics.js static/analytics.js
```

**Step 2: Verify static folder**

Run: `ls static/`
Expected: `analytics.js`

**Step 3: Commit**

```bash
git add static/analytics.js
git commit -m "chore: move analytics.js to static folder"
```

---

## Task 8: Migrate First Test Article

**Files:**
- Create: `content/blog/hooks-that-work-2026.md`

**Step 1: Create test article in Markdown**

Create `content/blog/hooks-that-work-2026.md`:

```markdown
---
title: "Хуки, которые работают: психология первых 15 секунд"
date: 2026-01-18
description: "Почему статьи открывают, но не читают. Исследование психологических триггеров, типов лидов и формул, которые удерживают внимание."
tags: ["copywriting", "хуки", "лиды", "психологические триггеры", "контент"]
section: "Copywriting"
intro: "Пишу статьи. Статьи открывают. Статьи закрывают. Где-то между заголовком и третьим абзацем теряется большинство."
sources:
  - title: "Animalz: Hook Examples"
    url: "https://www.animalz.co/blog/hook-examples/"
    note: "типы лидов и примеры"
  - title: "Copyblogger: Headlines That Work"
    url: "https://copyblogger.com/how-to-write-headlines-that-work/"
    note: "психология заголовков"
  - title: "Nielsen Norman Group: How Users Read"
    url: "https://www.nngroup.com/articles/how-users-read-on-the-web/"
    note: "исследование поведения читателей"
---

## Проблема

15 секунд — столько времени у тебя есть, чтобы удержать читателя. После этого он решает: скроллить дальше или закрыть вкладку.

Мои технические статьи собирают клики, но не дочитывания. Заголовок работает, а первый абзац — нет.

## Делегирую исследование агенту

Вместо того чтобы гуглить «how to write hooks» — попросил Claude Code провести исследование:

{{</* callout insight */>}}
«Найди психологические триггеры, типы лидов, формулы хуков. Обнови мой blog-post skill результатами.»
{{</* /callout */>}}

Агент прошёлся по источникам и структурировал находки.

Шесть триггеров, которые работают на первых строках:

## Психологические триггеры

| Триггер | Механика | Пример |
|---------|----------|--------|
| **Curiosity Gap** | Недосказанность создаёт напряжение — мозг требует закрытия гештальта | «Думал, делаю всё правильно — пока не увидел эту метрику» |
| **Identity** | Обращение к «своим» — читатель узнаёт себя | «Если твои первые проекты провалились — добро пожаловать» |
| **Tension** | Противоречие требует объяснения | «Удвоил продуктивность — и стало хуже» |
| **ROMO** | Relief of Missing Out — валидация отказа от хайпа | «Не нужно учить код — вот что я делаю вместо» |
| **FOMO** | Страх упустить — срочность | «Только 2% разработчиков делают это» |
| **Social Proof** | Цифры и авторитеты | «100,000 разработчиков используют этот инструмент» |

## Типы лидов

| Тип | Когда использовать | Пример |
|-----|-------------------|--------|
| **Zinger** | Провокация, шок | «Твой CLAUDE.md — мусор» |
| **First-Person** | Личный опыт, история | «Попросил агента настроить — он сломал всё» |
| **Question** | Диагностика проблемы | «Почему Claude Code тормозит после 50 сообщений?» |
| **Scene** | Конкретный момент, визуализация | «Открыл терминал. Написал промпт. Три часа спустя — готовый продукт» |

## Формулы

### SPY: Short — Pain — Yay

Короткое утверждение. Боль. Решение.

> «Документация устарела. Каждый раз гуглишь одно и то же. Вот скрипт, который парсит актуальные доки.»

### PAS: Problem — Agitate — Solution

Проблема. Усиление боли. Решение.

> «Статьи не дочитывают. Ты тратишь часы на контент, который закрывают через 10 секунд. Хуки решают это.»

### APP: Agree — Promise — Preview

Согласие с читателем. Обещание. Превью содержания.

> «AI меняет разработку. Покажу, как использовать агентов для рутины. Три паттерна из моей практики.»

## Антипаттерны

{{</* callout warning "Никогда не начинай статью с:" */>}}
«В современном мире AI...»
«Многие разработчики сталкиваются...»
«Сегодня мы рассмотрим...»
{{</* /callout */>}}

## Метрики

- **15 секунд** — время на решение читать или закрыть
- **30 слов** — максимум на хук
- **20%** — столько текста реально читают на странице ([Nielsen Norman Group](https://www.nngroup.com/articles/how-users-read-on-the-web/))

## Результат

Агент добавил эти паттерны в blog-post skill. Теперь при создании статьи он:

1. Предлагает хук на основе триггера (Identity, Tension, Curiosity Gap)
2. Проверяет лид на антипаттерны
3. Форматирует по формуле (SPY, PAS, APP)

Эта статья — первый тест. Лид использует Identity («пишу статьи, статьи не читают»). Intro — Tension («открывают, но закрывают»).

Через месяц сравню метрики с предыдущими статьями:

- **Scroll depth > 50%** — читают, а не сканируют
- **Время на странице > 2 мин** — дочитывают
- **Bounce rate < 60%** — не уходят с первого экрана
```

**Step 2: Build and verify**

Run: `hugo server -D`
Expected: Server starts, visit http://localhost:1313/blog/hooks-that-work-2026

**Step 3: Verify in browser**

- Check title renders correctly
- Check callout blocks styled
- Check tables render
- Check sources section appears

**Step 4: Stop server, commit**

```bash
git add content/blog/hooks-that-work-2026.md
git commit -m "feat: migrate first test article to Hugo markdown"
```

---

## Task 9: Create HTML-to-MD Conversion Script

**Files:**
- Create: `scripts/convert-html-to-md.sh`

**Step 1: Create conversion script**

Create `scripts/convert-html-to-md.sh`:

```bash
#!/bin/bash
# Convert existing HTML blog posts to Hugo Markdown
# Usage: ./scripts/convert-html-to-md.sh blog/article.html

set -e

INPUT="$1"
FILENAME=$(basename "$INPUT" .html)
OUTPUT="content/blog/${FILENAME}.md"

if [ -z "$INPUT" ]; then
  echo "Usage: $0 <html-file>"
  exit 1
fi

echo "Converting: $INPUT -> $OUTPUT"

# Extract metadata using grep/sed
TITLE=$(grep -o '<title>[^<]*</title>' "$INPUT" | sed 's/<[^>]*>//g' | sed 's/ | Сережа Рис//')
DATE=$(grep -o 'datePublished.*"[0-9-]*"' "$INPUT" | grep -o '[0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\}' | head -1)
DESC=$(grep 'name="description"' "$INPUT" | grep -o 'content="[^"]*"' | sed 's/content="//;s/"$//')

# Extract tags from article:tag
TAGS=$(grep 'article:tag' "$INPUT" | grep -o 'content="[^"]*"' | sed 's/content="//;s/"$//' | tr '\n' ',' | sed 's/,$//')

# Create frontmatter
cat > "$OUTPUT" << EOF
---
title: "$TITLE"
date: $DATE
description: "$DESC"
tags: [$(echo "$TAGS" | sed 's/,/", "/g' | sed 's/^/"/;s/$/"/' | sed 's/""/"/g')]
---

EOF

# Extract body content (simplified - manual review needed)
echo "# Manual conversion needed for content body"
echo "# Check: $OUTPUT"

echo "Created: $OUTPUT (frontmatter only, content needs manual migration)"
```

**Step 2: Make executable**

```bash
chmod +x scripts/convert-html-to-md.sh
```

**Step 3: Test on one file**

Run: `./scripts/convert-html-to-md.sh blog/midi-obs-claude-code.html`
Expected: Creates `content/blog/midi-obs-claude-code.md` with frontmatter

**Step 4: Commit**

```bash
git add scripts/convert-html-to-md.sh
git commit -m "chore: add HTML to Markdown conversion script"
```

---

## Task 10: Configure Vercel for Hugo

**Files:**
- Modify: `vercel.json`

**Step 1: Update vercel.json for Hugo build**

Replace `vercel.json`:

```json
{
  "build": {
    "env": {
      "HUGO_VERSION": "0.154.5"
    }
  },
  "framework": "hugo",
  "outputDirectory": "public",
  "cleanUrls": true
}
```

**Step 2: Test build locally**

Run: `hugo --minify`
Expected: Site built in `public/` folder

**Step 3: Verify output structure**

Run: `ls public/blog/`
Expected: `hooks-that-work-2026/index.html` (or similar)

**Step 4: Commit**

```bash
git add vercel.json
git commit -m "chore: configure Vercel for Hugo build"
```

---

## Task 11: Batch Convert Remaining Articles

**Files:**
- Create: `content/blog/*.md` (28 files)
- Delete: `blog/*.html` (after verification)

**Step 1: List all articles to convert**

```bash
ls blog/*.html | grep -v index.html | wc -l
```
Expected: 29 files (minus already converted)

**Step 2: Convert frontmatter for all**

```bash
for f in blog/*.html; do
  [ "$f" = "blog/index.html" ] && continue
  ./scripts/convert-html-to-md.sh "$f"
done
```

**Step 3: Manually migrate content**

For each file in `content/blog/`:
- Copy article body from HTML
- Convert HTML to Markdown
- Replace `<div class="callout insight">` with `{{</* callout insight */>}}`
- Replace `<div class="callout warning">` with `{{</* callout warning */>}}`

**Step 4: Verify all articles render**

Run: `hugo server`
Visit: http://localhost:1313/blog/
Expected: All articles listed and render correctly

**Step 5: Remove old HTML files**

```bash
rm blog/*.html
rm blog/sitemap.xml
rmdir blog/
```

**Step 6: Commit**

```bash
git add content/blog/
git rm -r blog/
git commit -m "feat: migrate all articles to Hugo markdown"
```

---

## Task 12: Final Verification and Deploy

**Step 1: Full build test**

Run: `hugo --minify`
Expected: No errors, site built

**Step 2: Verify sitemap generated**

Run: `cat public/sitemap.xml | head -20`
Expected: Valid XML with blog URLs

**Step 3: Verify RSS feed**

Run: `cat public/blog/index.xml | head -20`
Expected: Valid RSS feed

**Step 4: Push to deploy**

```bash
git push
```

**Step 5: Verify on production**

Visit: https://sereja.tech/blog/
Expected: Blog renders, all articles accessible

---

## Post-Migration: New Article Workflow

After migration, creating new articles:

```bash
# Create new article
hugo new blog/my-new-article.md

# Edit content
vim content/blog/my-new-article.md

# Preview
hugo server -D

# Deploy
git add -A && git commit -m "feat: add article about X" && git push
```

---

**Plan complete and saved to `docs/plans/2026-01-18-hugo-migration-plan.md`. Two execution options:**

**1. Subagent-Driven (this session)** - I dispatch fresh subagent per task, review between tasks, fast iteration

**2. Parallel Session (separate)** - Open new session with executing-plans, batch execution with checkpoints

**Which approach?**
