# AI Writing Pipelines: Дизайн исследования

**Дата:** 2026-01-11
**Автор:** Сережа Рис
**Статус:** Готов к исследованию

---

## 1. Цель и scope

**Цель:** Создать глубокий технический разбор современных практик AI-assisted content creation с фокусом на:
- LLM writing pipelines (промпт-цепочки, multi-agent системы, quality gates)
- Content repurposing (как из одного источника делать разные форматы)

**Что НЕ входит:**
- Knowledge management системы (Zettelkasten, PKM)
- Конкретные инструменты (Notion AI, Jasper) — только концепции
- SEO-оптимизация контента

**Результат:**
- Блог-пост ~6000 слов для sereja.tech
- Аудитория: для себя (глубокий технический разбор)
- С диаграммами workflow'ов
- С рекомендациями для своих проектов (mentor, cohorts, sereja.tech)

**Критерий успеха:**
После прочтения должно быть понятно:
1. Какие паттерны LLM-пайплайнов существуют и когда какой применять
2. Как построить quality gates для AI-контента
3. Как переиспользовать контент между форматами
4. Что из этого уже есть в моих скиллах и что стоит добавить

---

## 2. Структура исследования (4 блока)

### Блок 1: LLM Writing Pipelines (~15 источников)

Ключевые вопросы:
- Какие архитектуры промпт-цепочек существуют (linear, branching, iterative)?
- Как устроены multi-agent системы для написания (writer → critic → rewriter)?
- Какие quality gates применяют (fact-checking, style checking, deaification)?
- Chain-of-thought vs chain-of-prompts — когда что?

### Блок 2: Human-in-the-Loop (~12 источников)

Ключевые вопросы:
- На каких этапах человек должен вмешиваться?
- Approval flows: batch vs inline approval
- Как собирать feedback для улучшения промптов?
- Автоматизация vs контроль — где граница?

### Блок 3: Content Repurposing (~12 источников)

Ключевые вопросы:
- COPE (Create Once Publish Everywhere) — как это работает с AI?
- Atomic content — как разбивать на переиспользуемые единицы?
- Single-source publishing — какие форматы источника лучше?
- Трансформации: урок → статья, сессия → homework, атом → пост

### Блок 4: Практики индустрии (~15 источников)

Ключевые вопросы:
- Как Anthropic/OpenAI документируют свои подходы?
- Cohort-based курсы (Maven, On Deck) — их content pipelines
- Developer education (Vercel, Supabase) — как делают туториалы
- Независимые creators — их workflows

---

## 3. Поисковые запросы для Exa

### Блок 1: LLM Writing Pipelines
```
- "LLM prompt chaining content creation" 2024-2026
- "multi-agent writing system architecture"
- "AI content quality gates automated"
- "chain of thought vs chain of prompts writing"
- "Claude prompt engineering long-form content"
- "iterative refinement LLM writing workflow"
```

### Блок 2: Human-in-the-Loop
```
- "human in the loop AI content creation"
- "approval workflow LLM generated content"
- "AI writing feedback loop improvement"
- "when to intervene AI writing process"
- "hybrid human AI content workflow"
```

### Блок 3: Content Repurposing
```
- "COPE create once publish everywhere AI"
- "atomic content strategy LLM"
- "single source publishing automation"
- "content repurposing framework AI assisted"
- "transcript to blog post pipeline"
- "modular content architecture"
```

### Блок 4: Практики индустрии
```
- "Anthropic documentation workflow"
- "cohort based course content creation"
- "developer education content pipeline"
- "technical writing AI workflow 2025 2026"
- "indie creator AI content system"
- site:maven.com OR site:beehiiv.com content workflow
```

### Академические запросы
```
- "automated content generation evaluation metrics"
- "LLM writing quality assessment research"
```

---

## 4. Структура итоговой статьи

```
# AI Writing Pipelines: Глубокий разбор для практиков

## 1. Введение (~300 слов)
- Зачем это исследование
- Мой контекст: 3 проекта, 3 разных workflow
- Что искал и что нашёл

## 2. Анатомия LLM Writing Pipeline (~1500 слов)
- Архитектуры: linear → branching → iterative
- Multi-agent patterns: writer/critic/rewriter
- Quality gates: типы и когда применять
- Диаграмма: обобщённый pipeline

## 3. Human-in-the-Loop: Где вмешиваться (~1000 слов)
- Точки принятия решений
- Approval flows: batch vs inline
- Feedback loops для улучшения промптов
- Диаграмма: decision points в pipeline

## 4. Content Repurposing с AI (~1200 слов)
- COPE в эпоху LLM
- Atomic content: что это и как разбивать
- Трансформации между форматами
- Диаграмма: content graph

## 5. Как это делают другие (~1000 слов)
- Паттерны из индустрии
- Что работает, что нет
- Неожиданные находки

## 6. Анализ моих текущих workflows (~700 слов)
- Что уже хорошо
- Что стоит изменить
- Конкретные рекомендации

## 7. Sources
- Все 50+ источников с краткими аннотациями
```

**Формат:** HTML для sereja.tech/blog/, brutalist style, Prism.js для кода, диаграммы через Mermaid или ASCII.

---

## 5. Методология и критерии качества

### Критерии отбора источников
- Дата: 2024-2026 (предпочтительно), классика допускается
- Глубина: практические кейсы > теоретические рассуждения
- Авторитетность: компании (Anthropic, Vercel) > блогеры, но хорошие indie-посты включаем
- Конкретика: статьи с примерами промптов/кода > абстрактные советы

### Что исключаем
- Маркетинговые посты про AI-инструменты
- Поверхностные "10 tips for AI writing"
- Устаревшее (GPT-3 эра без обновлений)

### Процесс обработки источника
```
1. Прочитать → извлечь ключевые идеи
2. Классифицировать по блоку (1-4)
3. Оценить релевантность (high/medium/low)
4. Записать цитаты и инсайты
5. Отметить связи с моими текущими скиллами
```

### Формат сохранения находок
Папка `docs/research/2026-01-11-ai-writing-pipelines/`:
- `block-1-llm-pipelines.md`
- `block-2-human-in-loop.md`
- `block-3-content-repurposing.md`
- `block-4-industry-practices.md`
- `synthesis.md` — связи и выводы

---

## 6. Контекст: мои текущие workflows

### sereja.tech (блог)
```
Тема → Exa research → Написать HTML → Deaify (4 критика) → Publish
```

### mentor (сессии)
```
API data → Generate HTML с табами → Verify
```

### cohorts (knowledge atoms)
```
Lesson → 5-pass extraction → Approve → Generate atoms → Enrich relations
```

**Общие паттерны:**
- Research-first подход
- Языковые правила (избегать англицизмов)
- Обязательные Sources
- Итеративное улучшение

---

## Next steps

1. Провести research по 4 блокам
2. Сохранить находки в docs/research/
3. Написать synthesis.md
4. Написать блог-пост
5. Прогнать через deaify
6. Опубликовать
