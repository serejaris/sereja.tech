---
title: "Пайплайн для статей: 5 фаз от идеи до Telegram"
date: 2026-02-03
description: "Как я делегировал написание блога агентам Claude Code через sequential pipeline из 5 фаз: вопросы, research, черновик, деаификация, публикация."
tags: ["claude-code", "вайбкодинг", "автоматизация"]
---

Постить регулярно — тяжело. Нашёл тему, написал черновик, отредактировал, залил в git, запостил в Telegram. Вечер ушёл. На следующий день — то же самое. Через неделю — выгорание.

У меня в блоге 55 статей. Каждая проходит через один и тот же пайплайн: агенты делают research, пишут черновик, убирают AI-отпечатки, пушат в git и ставят пост в очередь для [Telegram-канала](https://t.me/sereja_tech). Я задаю тему и отвечаю на уточняющие вопросы — остальное автоматика.

## Для кого это

Я вайбкодер. Код пишут агенты, я направляю. Блог — для таких же: людей, которые используют Claude Code для решения задач, но не программисты в классическом смысле.

Поэтому в промптах нет терминальных команд как инструкций. Вайбкодер не набирает `git commit && git push` — он пишет агенту "закоммить и запуши". Команды — детали реализации, которые агент знает сам.

В статьях концепции важнее деталей:

| Плохо | Хорошо |
|-------|--------|
| launchd с StartCalendarInterval | планировщик, который запускает скрипт в нужное время |
| JSON с полями id, status, scheduled_date | очередь постов — список с датами публикации |
| chmod +x для executable | сделать скрипт запускаемым |

Промпты в этой статье — не технические спецификации. Это разговор с агентом.

## Общая схема

```
┌───────────────┐     ┌───────────────┐     ┌───────────────┐
│  1. Questions │────▶│  2. Research  │────▶│  3. Draft     │
│  (User input) │     │  (Exa+Sonnet) │     │  (Sonnet)     │
└───────────────┘     └───────────────┘     └───────────────┘
                                                     │
                      ┌───────────────┐              │
                      │  5. Deploy +  │◀─────────────┘
                      │  Telegram     │
                      └───────────────┘
                             ▲
                             │
                      ┌───────────────┐
                      │  4. Deaify    │
                      │  (4 Critics)  │
                      └───────────────┘
```

Каждая фаза делает одно дело. Никаких откатов назад — только вперёд. Sequential pipeline, классика. Похож на подход [n8n для content workflows](https://n8n.io/workflows/), но заточен под мой блог.

## Phase 1: Questions

Перед любым research агент спрашивает через `AskUserQuestion`:
- Какой угол для статьи? (личный опыт / tutorial / концепция)
- Кто читатель? (вайбкодеры / разработчики / новички)
- Ключевой takeaway — что читатель должен вынести?

Andrej Karpathy называет это [Context Engineering](https://x.com/karpathy/status/1917554028156043283) — вместо написания длинных промптов агент сам собирает нужный контекст через структурированные вопросы.

{{< callout type="insight" >}}
ВСЕГДА начинай с уточняющих вопросов через AskUserQuestion. Не запускай research пока не получишь ответы.

Минимальные вопросы:
1. Тема/угол — о чём конкретно? какой аспект?
2. Контекст — личный опыт? решённая проблема? концепция?
3. Аудитория — новички/продвинутые? вайбкодеры/разработчики?
4. Ключевой takeaway — что читатель должен вынести?
{{< /callout >}}

Я отвечаю через интерфейс Claude Code — выбираю опции или пишу текст. Агент получает структурированные данные и передаёт их дальше в пайплайн.

## Phase 2: Research

После получения ответов запускается субагент на Sonnet 4.5. Ему передаются все ответы из Phase 1 плюс промпт:

{{< callout type="insight" >}}
Research для блог-поста на тему: {тема}

Контекст от пользователя:
- Угол: {ответ}
- Аудитория: {ответ}
- Takeaway: {ответ}

Задачи:
1. Exa search по теме (3-5 источников)
2. Найти конкретные примеры, цифры, кейсы
3. Проверить актуальность информации (2026 год)

Верни структурированный research с источниками.
{{< /callout >}}

Субагент использует [Exa AI](https://exa.ai/) — поиск по смыслу, не по ключевым словам. Google для AI-тем часто выдаёт устаревшие результаты 2024 года.

Результат Phase 2 — структурированные заметки: источники, цитаты, цифры, ссылки. Всё это передаётся в Phase 3.

## Phase 3: Write Draft

Второй субагент (тоже Sonnet 4.5) получает research и пишет черновик:

{{< callout type="insight" >}}
Напиши черновик блог-поста для sereja.tech.

Тема: {тема}
Research: {результат Phase 2}

Требования:
- Минимум 600 слов
- Личный тон ("я сделал", "я понял")
- ASCII диаграмма обязательна
- Инлайн-ссылки в тексте (НЕ секция "Источники" в конце)
- Frontmatter: title ≤60, description ≤160, date, tags

Аудитория — вайбкодеры:
- НЕ показывай команды как инструкции ("запусти X") — пиши "прошу агента сделать X"
- Концепции важнее деталей: "планировщик" вместо "launchd с StartCalendarInterval"
- Структура: концепция → зачем → как сделал → альтернативы

Прочитай writing-guide.md и ai-terms-ru.md для стиля.

Верни готовый markdown.
{{< /callout >}}

Агент читает два файла:
- `writing-guide.md` — стилистика, тон, структура хука
- `ai-terms-ru.md` — как переводить AI-термины на русский

Без этих руководств агент пишет как технический писатель: "В современном мире AI... Рассмотрим подход... Данная методика позволяет...". С руководствами текст звучит как я — короткие предложения, личный тон, конкретика вместо абстракций.

## Phase 4: Deaify

Самая интересная фаза. Черновик проходит через skill `deaify-text`, который запускает четырёх параллельных критиков. Все четыре работают одновременно через Task API — [parallelization pattern](https://www.anthropic.com/engineering/building-effective-agents) из гайда Anthropic.

### Critic A — Generic Detector

{{< callout type="insight" >}}
Find AI-typical phrases in this text:
- "важно понимать", "следует отметить", "в заключение"
- "Это не X — это Y" dramatic contrasts
- Sentences without specific names/numbers/dates
- Abstract claims without examples

Output: numbered list with exact quotes and line references.
{{< /callout >}}

### Critic B — Rhythm Analyzer

{{< callout type="insight" >}}
Analyze text rhythm:
- Find 3+ consecutive sentences of similar length
- Find paragraphs where all sentences start similarly
- Check burstiness: ratio of shortest to longest sentence

EXCEPTION: Do NOT flag sequential/step lists. They help readers scan.

Output: specific locations that need rhythm variation.
{{< /callout >}}

### Critic C — Specificity Checker

{{< callout type="insight" >}}
Where could author add:
- Personal experience ("I tried this and...")
- Specific number or statistic
- Name/company/date reference
- Opinion marker ("я думаю", "по-моему")

Output: 3-5 specific suggestions with WHERE to insert.
{{< /callout >}}

### Critic D — Fact Checker

{{< callout type="insight" >}}
Extract all verifiable claims from this text:
- Software/model versions (GPT-4, Claude 3, React 18)
- Release dates and timelines
- Statistics, percentages, numbers

For each claim, flag if:
- Model/version might be outdated (AI models older than 6 months)
- Statistic seems made up (round numbers, no source)

Output: "[CLAIM]: {exact quote}" + "[FLAG]: {why suspicious}"
{{< /callout >}}

После критики основной агент переписывает текст с учётом замечаний. Обычно хватает одного прохода.

## Phase 5: Deploy + Telegram

Финальная фаза выполняется автоматически. Я не нажимаю кнопку "опубликовать" — агент делает всё сам:

1. Сохраняет markdown в `content/blog/{slug}.md`
2. Проверяет frontmatter (title ≤60, description ≤160)
3. Коммитит и пушит в git
4. Генерирует превью для Telegram
5. Добавляет пост в очередь
6. Сообщает мне дату публикации

Превью генерирует субагент на Haiku — быстрая и дешёвая модель для простых задач:

{{< callout type="insight" >}}
Напиши превью статьи для Telegram канала.

URL: https://sereja.tech/blog/{slug}

ФОРМАТ:
&lt;b&gt;Hook — цепляющая фраза про боль/результат&lt;/b&gt;

Тезис — что получит читатель, 1-2 предложения.

→ &lt;a href="URL"&gt;Читать&lt;/a&gt;

ПРАВИЛА:
- МАКСИМУМ 5 строк
- HTML теги: &lt;b&gt; для заголовка, &lt;a href&gt; для ссылки
- НИКАКИХ emoji, хештегов, markdown
- Личный тон (я сделал, я понял)

Верни ТОЛЬКО готовый HTML текст.
{{< /callout >}}

Посты публикуются в [@sereja_tech](https://t.me/sereja_tech) автоматически в 19:00 МСК — по одному в день из очереди. Пишу несколько статей подряд, они встают в очередь и выходят равномерно. Очередь управляется через launchd на маке — планировщик запускает скрипт по расписанию.

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ Git Push    │────▶│ Queue Add   │────▶│ Scheduled   │
│ (automatic) │     │ (automatic) │     │ 19:00 MSK   │
└─────────────┘     └─────────────┘     └─────────────┘
```

## Почему это работает

Раньше я писал промпты на три экрана: примеры, шаблоны, исключения. Теперь агент сам собирает контекст:

1. Спрашивает через structured questions
2. Читает writing guides
3. Делает research через Exa
4. Получает критику от параллельных агентов

Я задаю направление. Остальное — автоматика.

Похожий подход использует [CrewAI](https://www.crewai.com/) для multi-agent workflows. [Manubot](https://manubot.org/) делает то же самое для академических статей — несколько агентов работают последовательно, каждый делает свою задачу.

## Extensibility через Skills

Весь этот пайплайн лежит в папке `~/.claude/skills/blog-post/`. [Skills в Claude Code](https://support.anthropic.com/en/articles/10333944-what-is-a-skill) — это просто папки с markdown-инструкциями.

```
~/.claude/skills/
└── blog-post/
    ├── skill.md           # главный prompt
    ├── writing-guide.md   # стилистика
    ├── ai-terms-ru.md     # терминология
    └── screenshot.py      # ASCII preview
```

Когда я пишу "напиши статью" или "блог пост", Claude Code автоматически загружает skill и следует инструкциям из `skill.md`.

Skills — это extensibility паттерн. Вместо того чтобы каждый раз объяснять "напиши как я", я один раз описал процесс в markdown. Теперь любой Claude Code (у меня их несколько на разных машинах) работает одинаково.

## Результат

55 статей в блоге. Каждая прошла через этот пайплайн. Моё участие — задать тему, ответить на вопросы, проверить финальный текст.

Агенты пишут за меня. Я направляю.

Пайплайн лежит в `~/.claude/skills/blog-post/` — можно посмотреть и адаптировать под себя. Sequential workflows работают для любого контента, не только блогов.
