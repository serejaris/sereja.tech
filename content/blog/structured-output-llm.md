---
title: "Structured Output: почему текстовые промпты — это хрупко"
date: 2026-01-13
description: "Как я перешёл от текстовых инструкций в промпте к JSON-схемам. Реальный кейс: генерация дайджеста, когда модель забывала хештег."
tags:
  - LLM
  - structured output
  - Pydantic
section: LLM
---

У меня бот генерирует дайджесты чата. В промпте было написано: «завершай хештегом #дайджестчата».

Из 10 запусков 1-2 раза хештег пропадал.

Текстовые инструкции в промпте — это не гарантия. Это просьба.

## Проблема с текстовыми промптами

Мой промпт был на 47 строк. HTML-формат, секции, ссылки, что игнорировать. И да — хештег в конце.

Модель делала почти всё. Хештег появлялся в 8-9 случаях из 10. Ссылки иногда шли без `<a>`. Секции назывались то «Ресурсы», то «Полезные ссылки». Не сломано. Но и не надёжно.

Добавил «ОБЯЗАТЕЛЬНО: завершай хештегом». Капсом. С тремя восклицательными знаками. Помогло на неделю — потом снова пропустил.

{{< callout warning "Текстовые инструкции — это намёки" >}}
Модель их понимает, но не гарантирует выполнение. Чем длиннее промпт, тем выше шанс что что-то потеряется.
{{< /callout >}}

## Что такое structured output

Передаёшь модели схему — она физически не может вернуть другое. Не «постарается». Не может.

Gemini 2.0+, Claude 3.5, GPT-4o — все умеют. Передаёшь Pydantic-модель или JSON Schema, получаешь валидный объект.

```python
from pydantic import BaseModel, Field

class DigestItem(BaseModel):
    topic: str = Field(description="Тема (2-5 слов)")
    description: str = Field(description="Одно предложение")
    message_link: str
    external_url: str | None = None

class DigestContent(BaseModel):
    title: str = Field(description="Заголовок дня")
    resources: list[DigestItem] = Field(min_length=1)
    solutions: list[DigestItem] = Field(min_length=1)
    insights: list[DigestItem] = Field(min_length=1)
```

Заметь: в схеме нет хештега. Он добавляется в коде при форматировании. Программно. 100% надёжно.

## Как это работает в Gemini

```python
response = client.models.generate_content(
    model="gemini-3-pro-preview",
    contents=prompt,
    config=types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=DigestContent,
    )
)

# Парсинг в Pydantic
content = DigestContent.model_validate_json(response.text)

# Форматирование в HTML (хештег добавляется тут)
html = format_html(content) + "\n#дайджестчата"
```

Модель возвращает JSON. Pydantic валидирует — если схема нарушена, получаешь ошибку, а не мусор. Код форматирует в HTML и добавляет хештег. Надёжно.

## Что даёт

| Текстовый промпт | Structured output |
|------------------|-------------------|
| «Добавь хештег» — может забыть | Хештег в коде — 100% |
| Парсинг HTML регулярками | JSON в объект |
| Формат плавает | Схема гарантирует структуру |
| Сложно тестировать | JSON проверяется автоматически |

{{< callout insight >}}
Всё что можно сделать кодом — делай кодом. Модель генерирует контент. Код гарантирует структуру.
{{< /callout >}}

## Промпт становится проще

Было 47 строк с HTML-инструкциями. Стало 14 — только про контент:

```
Роль: Куратор полезного контента.

Задача: Дайджест чата за {date}.

ПРИОРИТЕТЫ:
1. Полезные ссылки и ресурсы
2. Решённые проблемы
3. Инсайты и открытия

ПРАВИЛА:
- Одно предложение на элемент, максимум 15 слов
- Минимум 1 элемент в каждой секции
```

Всё про формат ушло в код. Промпт теперь только про контент.

## Когда использовать

Structured output — когда нужна надёжность. Когда 10% сбоев это слишком много. Когда данные идут в следующий шаг пайплайна.

Текстовые промпты — когда прототипируешь. Когда формат не критичен. Когда пишешь для человека, а не для кода.

Мой дайджест публикуется каждый день. 10% сбоев — это 3 косяка в месяц. Перешёл на structured output.

## Источники

- [Gemini API: Structured Output](https://ai.google.dev/gemini-api/docs/structured-output)
- [LLM Structured Outputs: The Silent Hero of Production AI](https://www.decodingai.com/p/llm-structured-outputs-the-only-way)
- [The Guide to Structured Outputs and Function Calling](https://agenta.ai/blog/the-guide-to-structured-outputs-and-function-calling-with-llms)
- [Google Cloud: Control Generated Output](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/control-generated-output)
