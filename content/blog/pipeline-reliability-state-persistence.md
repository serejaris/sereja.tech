---
title: "Пайплайны на скиллах падают. Вот как это исправить"
date: 2026-01-27
description: "Почему AI-пайплайны прерываются на середине и как state persistence решает проблему для Claude Code"
tags: ["claude code", "пайплайны"]
---

Вчера запустил видео-пайплайн для урока. Субтитры сгенерились за 20 минут. Метаданные — ещё 5. На 47-й минуте Claude Code упал на генерации слайдов. Контекст переполнился.

20 минут субтитров — в мусорку.

## Почему пайплайны падают

Пайплайн на скиллах — цепочка. Субтитры → метаданные → слайды → превью → YouTube. Каждый шаг зависит от предыдущего.

Claude Code не помнит, что уже сделал. Упал на третьем шаге — начинай сначала. Rate limit? Весь прогресс потерян.

На GitHub [issue #21181](https://github.com/anthropics/claude-code/issues/21181): агенты при resume перезапускают уже сделанную работу вместо возврата результата. Открыт 27 января 2026 — по-моему, это ключевая проблема для долгих воркфлоу.

## Решение: state file

Записывать состояние после каждого шага.

{{< callout type="insight" >}}
Создай Python-скрипт для video publishing pipeline. После каждого шага сохраняй состояние в JSON. При падении — продолжить с того же места через --resume.
{{< /callout >}}

Opus 4.5 сделал скрипт с пятью шагами:
1. Субтитры через ai-whisper API
2. Метаданные через Claude Code
3. Chapter slides (ffmpeg)
4. Thumbnail (Playwright)
5. Загрузка на YouTube

state.json сохраняется после КАЖДОГО шага:

```json
{
  "steps": {
    "subtitles": {"status": "completed"},
    "metadata": {"status": "completed"},
    "chapter_slides": {"status": "in_progress"},
    "thumbnail": {"status": "pending"},
    "upload": {"status": "pending"}
  }
}
```

Упал на слайдах? `--resume pipeline.json` — продолжает с того же места.

## Паттерн durable execution

Не я придумал. Temporal, Restate, LangGraph делают то же — они называют это durable execution. Состояние в хранилище, при падении восстановление из checkpoint, шаги идемпотентны.

Для AI-агентов это критичнее, чем для обычных сервисов: каждый LLM-вызов стоит денег, а контекст ограничен 200k токенов. Потерял контекст — потерял и работу, и бюджет.

## Бонусы

**Параллельные шаги.** Thumbnail и chapter slides независимы — ThreadPoolExecutor запускает их одновременно.

**Graceful shutdown.** Ctrl+C ловится, состояние сохраняется. Можно прервать и продолжить.

**Dry run.** `--dry-run` проверяет ffmpeg, backend, playwright до старта.

## Источники

- [Persistence in LangGraph — Deep, Practical Guide](https://medium.com/towards-artificial-intelligence/persistence-in-langgraph-deep-practical-guide-36dc4c452c3b)
- [Build durable AI agents with Pydantic AI and Temporal](https://temporal.io/blog/build-durable-ai-agents-pydantic-ai-and-temporal)
- [Temporal Workflow Orchestration for Agentic AI](https://dev.to/akki907/temporal-workflow-orchestration-building-reliable-agentic-ai-systems-3bpm)
- [GitHub Issue #21181: Claude Code resume problems](https://github.com/anthropics/claude-code/issues/21181)
