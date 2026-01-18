# AI Writing Pipelines: Research Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development to execute this plan task-by-task with fresh subagents.

**Goal:** Провести глубокое исследование AI writing pipelines и content repurposing, собрать 50+ источников, написать блог-пост 6000+ слов.

**Architecture:** 4 параллельных research-блока через Exa MCP → синтез находок → написание статьи → deaify → публикация.

**Tech Stack:** Exa MCP (web_search_exa), markdown для заметок, HTML для финальной статьи.

---

## Task 1: Research Block 1 — LLM Writing Pipelines

**Files:**
- Create: `docs/research/2026-01-11-ai-writing-pipelines/block-1-llm-pipelines.md`

**Step 1: Execute Exa searches**

Запросы (выполнить все):
```
"LLM prompt chaining content creation" 2024-2026
"multi-agent writing system architecture"
"AI content quality gates automated"
"chain of thought vs chain of prompts writing"
"Claude prompt engineering long-form content"
"iterative refinement LLM writing workflow"
```

**Step 2: Process and save findings**

Для каждого источника записать:
- URL и title
- Ключевые идеи (2-3 bullet points)
- Релевантность: high/medium/low
- Связь с текущими скиллами (deaify, blog-post, atom-generation)

**Step 3: Summarize block**

В конце файла добавить:
- Топ-5 инсайтов блока
- Паттерны которые повторяются
- Что применимо к моим проектам

**Expected output:** 15+ источников, структурированные заметки, summary.

---

## Task 2: Research Block 2 — Human-in-the-Loop

**Files:**
- Create: `docs/research/2026-01-11-ai-writing-pipelines/block-2-human-in-loop.md`

**Step 1: Execute Exa searches**

Запросы:
```
"human in the loop AI content creation"
"approval workflow LLM generated content"
"AI writing feedback loop improvement"
"when to intervene AI writing process"
"hybrid human AI content workflow"
```

**Step 2: Process and save findings**

Формат тот же: URL, title, ключевые идеи, релевантность, связь со скиллами.

Особый фокус на:
- Точки принятия решений в pipeline
- Batch vs inline approval
- Как собирать feedback

**Step 3: Summarize block**

**Expected output:** 12+ источников, структурированные заметки, summary.

---

## Task 3: Research Block 3 — Content Repurposing

**Files:**
- Create: `docs/research/2026-01-11-ai-writing-pipelines/block-3-content-repurposing.md`

**Step 1: Execute Exa searches**

Запросы:
```
"COPE create once publish everywhere AI"
"atomic content strategy LLM"
"single source publishing automation"
"content repurposing framework AI assisted"
"transcript to blog post pipeline"
"modular content architecture"
```

**Step 2: Process and save findings**

Особый фокус на:
- Как разбивать контент на атомарные единицы
- Трансформации между форматами
- Single-source publishing паттерны

**Step 3: Summarize block**

**Expected output:** 12+ источников, структурированные заметки, summary.

---

## Task 4: Research Block 4 — Industry Practices

**Files:**
- Create: `docs/research/2026-01-11-ai-writing-pipelines/block-4-industry-practices.md`

**Step 1: Execute Exa searches**

Запросы:
```
"Anthropic documentation workflow"
"cohort based course content creation"
"developer education content pipeline"
"technical writing AI workflow 2025 2026"
"indie creator AI content system"
"automated content generation evaluation metrics"
```

**Step 2: Process and save findings**

Особый фокус на:
- Конкретные примеры компаний
- Что работает в production
- Метрики качества

**Step 3: Summarize block**

**Expected output:** 15+ источников, структурированные заметки, summary.

---

## Task 5: Synthesis

**Files:**
- Read: все 4 block-*.md файла
- Create: `docs/research/2026-01-11-ai-writing-pipelines/synthesis.md`

**Step 1: Identify cross-block patterns**

Найти паттерны которые повторяются в нескольких блоках:
- Архитектурные паттерны
- Quality gates
- Human intervention points
- Content transformation patterns

**Step 2: Map to current workflows**

Сравнить с текущими скиллами:
- sereja.tech: blog-post, deaify-text
- mentor: session-student-page
- cohorts: atom-research, atom-generation, lesson-plan

Записать:
- Что уже реализовано
- Что можно улучшить
- Что стоит добавить

**Step 3: Create recommendations**

Конкретные рекомендации для каждого проекта.

**Expected output:** Synthesis document с паттернами, маппингом и рекомендациями.

---

## Task 6: Write Blog Post Draft

**Files:**
- Read: `docs/research/2026-01-11-ai-writing-pipelines/synthesis.md`
- Create: `blog/ai-writing-pipelines.html`

**Step 1: Write structure**

Использовать структуру из дизайна:
1. Введение (~300 слов)
2. Анатомия LLM Writing Pipeline (~1500 слов)
3. Human-in-the-Loop (~1000 слов)
4. Content Repurposing с AI (~1200 слов)
5. Как это делают другие (~1000 слов)
6. Анализ моих текущих workflows (~700 слов)
7. Sources

**Step 2: Write each section**

Использовать:
- Шаблон из `blog/slash-commands-subagents.html`
- Brutalist style, monospace
- JSON-LD schema, Open Graph
- Prism.js для кода
- Mermaid или ASCII для диаграмм

**Step 3: Add all sources**

Все 50+ источников с краткими аннотациями.

**Expected output:** Полный HTML файл статьи.

---

## Task 7: Deaify and Publish

**Files:**
- Modify: `blog/ai-writing-pipelines.html`
- Modify: `blog/index.html` (добавить в список)
- Modify: `blog/sitemap.xml` (добавить URL)

**Step 1: Run deaify-text skill**

Прогнать статью через 4 критиков:
- generic-critic
- rhythm-critic
- specifics-critic
- fact-checker

**Step 2: Rewrite based on feedback**

Исправить найденные проблемы.

**Step 3: Update blog index and sitemap**

Добавить статью в `blog/index.html` между POSTS маркерами.
Добавить URL в `blog/sitemap.xml` между SITEMAP_POSTS маркерами.

**Expected output:** Финальная статья готова к публикации.

---

## Execution Notes

**Subagent configuration for research tasks (1-4):**
- subagent_type: `general-purpose`
- Tools needed: `mcp__exa__web_search_exa`, `Write`, `Read`
- Each task is independent — можно запускать параллельно

**Subagent configuration for synthesis (5):**
- subagent_type: `general-purpose`
- Depends on: Tasks 1-4 complete
- Tools needed: `Read`, `Write`

**Subagent configuration for writing (6):**
- subagent_type: `general-purpose`
- Depends on: Task 5 complete
- Tools needed: `Read`, `Write`
- Reference: `blog/slash-commands-subagents.html`

**Subagent configuration for deaify (7):**
- Use Skill tool with `deaify-text`
- Depends on: Task 6 complete

---

## Checkpoints

- [ ] После Tasks 1-4: Review research quality, достаточно ли источников?
- [ ] После Task 5: Review synthesis, все ли паттерны найдены?
- [ ] После Task 6: Review draft, структура и глубина ок?
- [ ] После Task 7: Final review перед публикацией
