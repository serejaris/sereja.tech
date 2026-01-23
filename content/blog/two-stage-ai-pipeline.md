---
title: "Two-Stage AI Pipeline: как платить вдвое меньше за генерацию"
date: 2026-01-23
description: "Паттерн разделения LLM-запросов на быструю модель для извлечения и качественную для генерации. Реальный пример из Telegram-бота дайджестов."
tags: ["llm", "gemini", "оптимизация", "вайбкодинг"]
---

$87 в месяц на дайджесты чата. Посмотрел логи — Pro-модель тратит 80% токенов на поиск тем в JSON. Разделил на два этапа. Теперь $35.

## Проблема

Делаю бота для дайджестов чата @vibecod3rs. 200-400 сообщений в день. На выходе — структурированный дайджест с ресурсами, решениями, инструментами.

Первая версия: всё в Pro. Она и темы извлекает, и текст пишет. Работает, но счёт за январь:

- 80-120K токенов на вход (зависит от активности чата)
- $2.5-3.5 за дайджест
- 30 дайджестов → $87

Pro отлично пишет. Но $2/1M токенов за то, чтобы найти в JSON нужные поля и сгруппировать? Дорого.

## Решение

Два этапа вместо одного:

{{< callout type="insight" >}}
Stage 1 (Flash): найди все темы в сообщениях, верни JSON.
Stage 2 (Pro): вот 12 тем — напиши из них дайджест.
{{< /callout >}}

Flash стоит $0.50/1M — в 4 раза дешевле Pro. Справляется с extraction без проблем. Structured output через Pydantic гарантирует формат — Gemini API поддерживает `response_schema` с ноября 2025.

Pro получает готовый список из 10-15 тем вместо сотен сообщений. Контекст сжался с 100K до 8-12K токенов.

## Реализация

```python
EXTRACTION_MODEL = "gemini-3-flash-preview"  # Fast & cheap
GENERATION_MODEL = "gemini-3-pro-preview"    # Quality output

async def generate(self, messages: list[dict]) -> DigestResult:
    # Stage 1: Extract topics (Flash)
    topics, extraction_tokens = await self._extract_topics(messages_json)

    # Stage 2: Generate digest (Pro)
    response = await self.client.generate_text(
        model=GENERATION_MODEL,
        prompt=DIGEST_PROMPT.format(topics_json=topics_json),
    )
```

Схема для structured output:

```python
class Topic(BaseModel):
    category: str  # resource|solution|insight|tool
    title: str
    summary: str
    url: str | None
    message_link: str | None

class TopicsResponse(BaseModel):
    topics: list[Topic]
```

Gemini API с параметром `response_schema` гарантирует валидный JSON. Никакого парсинга регулярками.

## Retry с эскалацией лимитов

Flash иногда обрезает JSON на больших входах. Лечится эскалацией:

```python
token_limits = [16384, 32768, 65536]

for attempt, max_tokens in enumerate(token_limits):
    try:
        result = await self.client.generate_structured(
            model=EXTRACTION_MODEL,
            response_schema=TopicsResponse,
            max_tokens=max_tokens,
        )
        return result
    except TokenLimitExceeded:
        if attempt < len(token_limits) - 1:
            continue
        raise
```

16K → 32K → 65K. За месяц работы бота (31 дайджест) retry сработал 2 раза. Оба на 32K — 65K не понадобился.

## Результат

| Метрика | До | После |
|---------|-----|-------|
| Токены Pro | 80-120K | 8-12K |
| Стоимость/дайджест | $2.5-3.5 | $1.0-1.2 |
| Январь 2026 | $87 | $35 |

Бонус: Pro пишет чище с готовыми данными. Без шума из 300 сообщений — меньше "воды" в итоговом тексте.

## Когда применять

Паттерн работает если:

1. **Extraction отделим от generation** — сначала найти, потом написать
2. **Входные данные большие** — сотни документов, логи, чаты
3. **Структура известна** — опишешь Pydantic-моделью

Не подходит для суммаризации (нужен весь контекст) и коротких запросов (overhead не окупится).

## Источники

- [OverFill: Two-Stage Models for Efficient LLM Decoding](https://arxiv.org/abs/2508.08446) — академический подход к разделению prefill и decode
- [xRouter: Cost-Aware LLM Orchestration](https://arxiv.org/html/2510.08439v1) — RL для выбора модели под задачу
- [The Economics of RAG: Cost Optimization](https://thedataguy.pro/blog/2025/07/the-economics-of-rag-cost-optimization-for-production-systems/) — стратегии оптимизации затрат в RAG
