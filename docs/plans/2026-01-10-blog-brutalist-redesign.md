# Blog Brutalist Redesign Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Convert blog from dark theme to minimalist brutalist style matching main page.

**Architecture:** Replace Inter font + dark theme with monospace + white background. Keep SEO meta-tags intact. Add Prism.js for syntax highlighting. Simplify callouts to bordered boxes.

**Tech Stack:** HTML, CSS, Prism.js (CDN)

---

### Task 1: Rewrite blog/index.html to brutalist style

**Files:**
- Modify: `blog/index.html`

**Step 1: Replace entire style block**

Remove lines 45-134 (Inter font link + entire `<style>` block) and replace with:

```html
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
    h1 { font-size: 24px; margin-bottom: 10px; }
    .intro { color: #666; margin-bottom: 30px; }
    .posts { list-style: none; padding: 0; }
    .posts li { margin-bottom: 12px; }
    .posts a { display: block; }
    .date { color: #666; font-size: 14px; }
    .title { display: block; }
  </style>
```

**Step 2: Simplify body structure**

Replace body content (lines 136-151) with:

```html
<body>
  <p><a href="/">&larr; sereja.tech</a></p>
  <h1>Блог</h1>
  <p class="intro">Статьи про вайбкодинг, Claude Code и AI-инструменты</p>

  <ul class="posts">
    <!-- POSTS_START -->
    <li>
      <a href="/blog/slash-commands-subagents">
        <span class="date">9 янв 2026</span>
        <span class="title">Почему model: в slash-командах — это ловушка</span>
      </a>
    </li>
    <!-- POSTS_END -->
  </ul>
</body>
```

**Step 3: Test locally**

Run: `cd /Users/ris/Documents/GitHub/sereja.tech && python3 -m http.server 8000`
Open: http://localhost:8000/blog/
Expected: White background, monospace font, blue links

**Step 4: Commit**

```bash
git add blog/index.html
git commit -m "feat(blog): convert index to brutalist style"
```

---

### Task 2: Rewrite blog article to brutalist style with Prism.js

**Files:**
- Modify: `blog/slash-commands-subagents.html`

**Step 1: Replace font link and add Prism.js**

Remove line 70 (Inter font) and add Prism.js:

```html
  <link href="https://unpkg.com/prismjs@1.29.0/themes/prism.css" rel="stylesheet">
```

Add before `</body>`:

```html
  <script src="https://unpkg.com/prismjs@1.29.0/prism.min.js"></script>
  <script src="https://unpkg.com/prismjs@1.29.0/components/prism-bash.min.js"></script>
  <script src="https://unpkg.com/prismjs@1.29.0/components/prism-markdown.min.js"></script>
```

**Step 2: Replace entire style block (lines 71-254)**

```html
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
    h1 { font-size: 24px; margin-bottom: 10px; line-height: 1.3; }
    h2 { font-size: 18px; margin-top: 30px; margin-bottom: 10px; }
    p { margin-bottom: 15px; }
    .intro { color: #666; }
    .author { color: #666; font-size: 14px; margin-bottom: 30px; }

    /* Callouts */
    .callout {
      border: 1px solid #000;
      padding: 12px 16px;
      margin: 20px 0;
    }
    .callout.warning { border-left: 3px solid #c00; }
    .callout.insight { border-left: 3px solid #060; }
    .callout strong { display: block; margin-bottom: 4px; }
    .callout p { margin-bottom: 0; }

    /* Code */
    pre[class*="language-"] {
      background: #f5f5f5;
      border: 1px solid #ddd;
      padding: 12px;
      overflow-x: auto;
      font-size: 14px;
      margin: 20px 0;
    }
    code { font-family: monospace; background: #f5f5f5; padding: 2px 4px; }
    pre code { background: none; padding: 0; }

    /* Table */
    table { width: 100%; border-collapse: collapse; margin: 20px 0; }
    th, td { border: 1px solid #000; padding: 8px; text-align: left; }
    th { background: #f5f5f5; }
    .yes { color: #060; }
    .no { color: #c00; }

    /* ASCII diagrams */
    .ascii {
      font-family: monospace;
      background: #f5f5f5;
      padding: 12px;
      margin: 20px 0;
      text-align: center;
      border: 1px solid #ddd;
    }

    ul { margin: 15px 0 15px 20px; }
    li { margin-bottom: 8px; }

    .sources { margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; }
    .sources h3 { font-size: 14px; color: #666; margin-bottom: 10px; }
    .sources ul { list-style: none; margin-left: 0; }
    .sources li { font-size: 14px; margin-bottom: 6px; }

    footer { margin-top: 30px; text-align: center; font-size: 13px; color: #666; }
  </style>
```

**Step 3: Simplify back link and author block**

Replace line 257 (back link) with:
```html
  <p><a href="/blog/">&larr; Блог</a></p>
```

Replace author div (lines 261-266) with:
```html
    <p class="author">Сережа Рис · 9 января 2026</p>
```

**Step 4: Add language classes to code blocks**

Change `<pre><code>` block (lines 331-344) to:
```html
    <pre><code class="language-markdown"># ~/.claude/commands/readme.md
---
description: Генерация README через Haiku
---
Немедленно запусти субагента.

**Параметры Task tool:**
- subagent_type: "readme-writer"
- model: "haiku"
- prompt: "Сгенерируй README.md"

**Правила:**
1. Сам ничего не генерируй
2. Только запусти агента и верни результат</code></pre>
```

**Step 5: Test locally**

Run: `python3 -m http.server 8000`
Open: http://localhost:8000/blog/slash-commands-subagents
Expected:
- White background, monospace font
- Code blocks with syntax highlighting
- Callouts with borders (red left border for warning, green for insight)
- Table with black borders

**Step 6: Commit**

```bash
git add blog/slash-commands-subagents.html
git commit -m "feat(blog): convert article to brutalist style with Prism.js"
```

---

### Task 3: Update blog-post skill with new style

**Files:**
- Modify: `~/.claude/skills/blog-post/SKILL.md`

**Step 1: Update CSS Variables section**

Replace the CSS Variables section with brutalist styles:

```markdown
### CSS (Brutalist)

\`\`\`css
body {
  font-family: monospace;
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  line-height: 1.6;
  background: #fff;
  color: #000;
}
a { color: #0000EE; }
.callout { border: 1px solid #000; padding: 12px 16px; margin: 20px 0; }
.callout.warning { border-left: 3px solid #c00; }
.callout.insight { border-left: 3px solid #060; }
\`\`\`

### Prism.js для подсветки

\`\`\`html
<link href="https://unpkg.com/prismjs@1.29.0/themes/prism.css" rel="stylesheet">
<script src="https://unpkg.com/prismjs@1.29.0/prism.min.js"></script>
\`\`\`
```

**Step 2: Commit**

```bash
git add ~/.claude/skills/blog-post/SKILL.md
git commit -m "docs(skill): update blog-post skill with brutalist style"
```

---

### Task 4: Final verification

**Step 1: Start local server**

Run: `cd /Users/ris/Documents/GitHub/sereja.tech && python3 -m http.server 8000`

**Step 2: Verify all pages**

Check:
- http://localhost:8000/ — main page (should be unchanged)
- http://localhost:8000/blog/ — blog index (brutalist style)
- http://localhost:8000/blog/slash-commands-subagents — article (brutalist + Prism.js)

**Step 3: Verify consistency**

Expected:
- Same monospace font across main, blog index, and article
- Same blue link color (#0000EE)
- Same white background
- Syntax highlighting works in article
- Callout boxes have visible borders

**Step 4: Push all changes**

```bash
git push origin main
```
