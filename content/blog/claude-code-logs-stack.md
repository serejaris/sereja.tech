---
title: "Мой стек для анализа логов Claude Code"
date: 2026-01-15
description: "Какие инструменты использую для анализа логов Claude Code: claude-code-transcripts, claude-code-log, структура JSONL и как превращать сессии в контент."
tags: ["claude code", "логи"]
section: "Claude Code"
knowledge:
  problem: "Рабочие сессии Claude Code содержат материал для туториалов и кейсов, но извлечь его сложно"
  solution: "Стек инструментов: claude-code-transcripts для HTML-экспорта, claude-code-log для фильтрации по датам"
  pattern: "logs-content-pipeline"
  tools: ["claude-code-transcripts", "claude-code-log", "cctrace", "vibe-log-cli", "uvx"]
  takeaways:
    - "5 инструментов протестированы для анализа логов Claude Code"
    - "Из полуторачасовой сессии получается 500-800 слов контента"
    - "claude-code-transcripts работает без установки через uvx"
    - "15 интересных сессий накоплено за январь для публикации"
  metrics:
    tools_tested: 5
    content_words_per_session: "500-800"
    sessions_collected: 15
  related:
    - slug: "claude-code-logs-project-status"
      relation: "практическое использование логов для аудита проектов"
---

Хочу превращать рабочие сессии в контент.

Туториалы, кейсы, метрики — всё лежит в логах.

Два часа копался в инструментах. Перепробовал пять штук.

## Где лежат логи

Claude Code пишет в `~/.claude/projects/`. Каждая сессия — отдельный JSONL файл:

```
~/.claude/projects/
└── -Users-ris-myproject/
    ├── 08fce8c2-8453-42da-a52c.jsonl
    └── settings.json
```

Путь к проекту закодирован: слеши становятся дефисами. Внутри — поток событий: сообщения, вызовы инструментов, результаты. Метаданные: стоимость, время, токены.

## Инструменты

Simon Willison выпустил `claude-code-transcripts` в декабре 2025. Конвертирует JSONL в интерактивный HTML. Можно сразу в Gist публиковать — удобно для шеринга.

Ещё нашёл:

- **claude-code-log** — терминальный интерфейс с фильтрами по датам. Мне зашёл больше всего для быстрого просмотра
- **cctrace** — экспорт в markdown и XML
- **claude-conversation-extractor** — вытаскивает диалоги без метаданных
- **vibe-log-cli** работает и с Cursor, не только Claude Code

## Что выбрал

Для старта — `claude-code-transcripts`. Без установки:

```bash
uvx claude-code-transcripts
```

Выбираешь сессию, получаешь HTML.

Для публикации в Gist:

```bash
uvx claude-code-transcripts web --gist
```

Нюанс: `web` режим требует API-ключ для summary. Без ключа работает, просто summary не будет. По-моему, для большинства случаев хватит базового режима.

Для фильтрации по датам использую `claude-code-log`:

```bash
uvx claude-code-log@latest --from-date "last week" --open-browser
```

## Зачем

**Туториалы.** Решил задачу — материал готов. Редактирую и публикую. Из полуторачасовой сессии получается 500-800 слов.

**Кейсы для кружка.** Показать студентам реальный процесс. Как формулировал промпты, где агент ошибался.

**Метрики.** Сколько токенов на типовые задачи. Какие инструменты вызываются чаще.

## Дальше

За январь накопилось 15 интересных сессий. План:

1. Отфильтровать публичные
2. Конвертировать в HTML, выложить на сайт
3. Написать скрипт для метрик — стоимость по проектам, топ инструментов

Если готовые инструменты не покроют — напишу свой парсер. JSONL читать несложно.

---

## Источники

- [claude-code-transcripts — Simon Willison](https://simonwillison.net/2025/Dec/25/claude-code-transcripts/)
- [claude-code-log — GitHub](https://github.com/daaain/claude-code-log)
- [cctrace — GitHub](https://github.com/jimmc414/cctrace)
- [vibe-log-cli — GitHub](https://github.com/vibe-log/vibe-log-cli)
