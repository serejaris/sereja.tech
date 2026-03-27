---
title: "Skill для автопостинга в Telegram: завайбкодил за стрим"
date: 2026-01-23
description: "Создал Claude Code skill который генерирует превью статьи и публикует в Telegram канал. Haiku пишет текст, Python отправляет."
tags: ["claude code", "telegram", "skills"]
youtube_id: "BxkAfHxQ9BU"
image: /images/blog/blog-to-telegram-skill-preview.png
---

Написал статью — копирую текст в Telegram. Надоело. За 2 часа стрима сделал skill.

{{< youtube BxkAfHxQ9BU >}}

## Проблема

После каждой публикации — четыре клика. Telegram. Превью. Ссылка. Отправить.

## Решение

{{< callout type="insight" >}}
Создай skill blog-to-telegram. Находит последнюю статью через git log, генерирует превью через Haiku субагента, отправляет в Telegram через Python скрипт.
{{< /callout >}}

Claude Code на Opus 4.5 выдал рабочий код за 8 минут.

## До и после: зачем нужен skill

Сначала я просто попросил Haiku написать превью без инструкций. Вот что получилось:

```
❌ Haiku без skill:

💰 Платили $87 в месяц за AI дайджесты...
🔍 Stage 1 (Fast): Flash-модель фильтрует нерелевантное...
📊 Stage 2 (Pro): Опус пишет финальный текст...
💡 Результат: расходы снизились до $35!

#ai #optimization #telegram #vibe
```

Emoji в каждой строке. Хештеги. 17 строк вместо 5. Это не мой стиль.

После трёх итераций с правилами:

```
✅ С skill:

<b>$87 → $35 в месяц на AI дайджесты</b>

Разделил LLM-запросы на два этапа: дешёвая модель фильтрует,
дорогая пишет. Половина расходов — на мусорных токенах.

→ <a href="...">Читать</a>
```

Чистый HTML. Личный тон. Пять строк. То что нужно.

## Зачем субагент

Opus 4.5 стоит $5 за миллион входных токенов. Для генерации 5 строк превью — overkill.

Haiku 4.5 стоит $1 за миллион токенов. Для простых задач качество одинаковое.

Claude Code позволяет делегировать работу дешёвой модели через Task tool:

```
Task(model="haiku", prompt="Напиши превью...")
```

Результат: основной агент (Opus) занимается оркестрацией, а рутинную генерацию делает Haiku.

## Как я тестирую инструкции для агентов

Не "TDD для skills", а итеративная отладка промпта:

1. **Запускаю без правил** — фиксирую что ломается (emoji, хештеги, много текста)
2. **Пишу правила** — проверяю что косяки ушли
3. **Нахожу новые лазейки** — закрываю

Три итерации — и Haiku выдаёт ровно то, что нужно.

Ключевые правила из skill.md:

```markdown
ПРАВИЛА:
- МАКСИМУМ 5 строк (hook + 1-2 предложения + ссылка)
- HTML теги: <b> для заголовка, <a href="..."> для ссылки
- НИКАКИХ emoji, хештегов, markdown
- Личный тон (я сделал, я понял)
```

## Структура skill

```
blog-to-telegram/
├── skill.md    # инструкции когда и как использовать
├── send.py     # отправка в Telegram (50 строк, stdlib)
└── .env        # токены (не в git)
```

### skill.md — инструкции для агента

Содержит workflow (git log → read → Task Haiku → send.py) и промпт для субагента с жёсткими правилами форматирования.

### send.py — отправка без зависимостей

```python
import json
import urllib.request

def send(text: str) -> dict:
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = json.dumps({
        "chat_id": CHANNEL,
        "text": text,
        "parse_mode": "HTML",
    }).encode()

    req = urllib.request.Request(url, data=data,
        headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())
```

Никакого `pip install`. Только stdlib.

## Результат

`/blog-to-telegram` — превью в канале за 10 секунд.

![Пост в Telegram канале](/images/blog/telegram-preview.png)

## Workflow

```
┌─────────────────┐     ┌──────────────┐     ┌─────────────┐
│  git log        │────▶│  Read post   │────▶│  Task       │
│  latest post    │     │  frontmatter │     │  (Haiku)    │
└─────────────────┘     └──────────────┘     └──────┬──────┘
                                                   │
                                                   ▼
                                            ┌──────────────┐
                                            │  send.py     │
                                            │  → Telegram  │
                                            └──────────────┘
```

## Смотри также

- [Пайплайн для статей: 5 фаз от идеи до Telegram](/blog/blog-post-pipeline/) — полный цикл, в котором этот skill — финальная фаза
- [Мой редотдел из трёх промптов](/blog/telegram-autopublisher/) — как работает система автопубликации в целом

## Источники

- [Claude Skills — документация](https://code.claude.com/docs/en/skills)
- [Claude Skills: Build repeatable workflows](https://zapier.com/blog/claude-skills/) — Zapier
- [Стрим](https://youtube.com/live/BxkAfHxQ9BU)
