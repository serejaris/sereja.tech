---
title: "Как мой AI-агент отправил 717 сообщений за 8 минут"
date: 2026-01-13
description: "Попросил Claude Code сделать рассылку — он использовал синхронный скрипт и ждали 8 минут вместо 30 секунд. Как AI-агенты учатся на своих ошибках."
tags: ["telegram", "python", "asyncio"]
section: Python
knowledge:
  problem: "Синхронный скрипт рассылки в Telegram отправлял 717 сообщений за 8 минут вместо 30 секунд"
  solution: "Замена синхронного requests на asyncio + aiohttp с батчами по 30 сообщений в секунду"
  pattern: "sync-to-async-broadcast"
  tools: ["Python", "asyncio", "aiohttp", "Telegram Bot API"]
  takeaways:
    - "Синхронный requests на 717 юзеров = 487 секунд (~8 минут)"
    - "asyncio.gather с батчами по 30 = 24 секунды"
    - "Telegram Bot API позволяет ~30 сообщений/секунду в разные чаты"
    - "80% доставляемость — норма для Telegram (576 из 717)"
    - "При 429 ошибке использовать retry_after из ответа API"
  metrics:
    recipients: 717
    delivered: 576
    blocked: 141
    delivery_rate_pct: 80
    sync_time_min: 8
    async_time_sec: 30
  related:
    - slug: "telegram-broadcast-file-id"
      relation: "оптимизация рассылки медиа через file_id"
---

Попросил Claude Code сделать рассылку в Telegram-боте. 717 получателей.

Смотрю на прогресс — обновляется каждые 25 сообщений. Медленно.

8 минут на то, что должно было занять полминуты. Спрашиваю агента: почему так долго?

## Что агент использовал

Claude запустил скрипт broadcast.py, который я когда-то написал для небольших рассылок:

```python
for user in users:
    resp = requests.post(API_URL, json=payload)

    if (i + 1) % 25 == 0:
        time.sleep(1)
```

Синхронный запрос — ждём ответа — следующий запрос. Пауза каждые 25, "чтобы не получить 429".

Число 25 было выбрано произвольно. На 50 получателях работало нормально. На 717 — нет.

## Что выяснил агент

Спросил Claude, почему так долго. Он полез искать через Exa MCP — нашёл документацию по rate limits.

Telegram Bot API позволяет ~30 сообщений в секунду при отправке в разные чаты.

717 ÷ 30 = 24 секунды. С буфером на сеть — 30-40 секунд.

Синхронный скрипт делал так:

- 29 пауз по секунде (717 ÷ 25)
- requests.post блокирует на 100-300мс каждый раз
- Итого: 487 секунд

Разница в 16 раз. Claude сразу предложил переписать на asyncio.

## Как агент должен был сделать

Claude показал правильный подход:

```python
async def send_batch(users, message, batch_size=30):
    async with aiohttp.ClientSession() as session:
        for i in range(0, len(users), batch_size):
            batch = users[i:i+batch_size]
            tasks = [send_one(session, u, message) for u in batch]
            await asyncio.gather(*tasks)
            await asyncio.sleep(1)
```

`asyncio.gather` отправляет 30 запросов параллельно. Один батч в секунду. 717 ÷ 30 = 24 батча = 24 секунды.

## Реальный результат

Итог рассылки (несмотря на медленность):

- 576 доставлено
- 141 заблокировали бота
- 80% доставляемость

Норма для Telegram. Но ждать 8 минут — не норма. В следующий раз попрошу агента сначала переписать скрипт.

## Если получил 429

Claude также напомнил про обработку ошибок. Telegram возвращает `retry_after` — сколько секунд ждать:

```python
if error_code == 429:
    retry_after = data['parameters']['retry_after']
    await asyncio.sleep(retry_after)
```

python-telegram-bot имеет встроенный AIORateLimiter. aiogram тоже. Своё писать не надо — агент знает про эти библиотеки.

## Итог

| Подход | Время |
|--------|-------|
| Синхронный requests | ~8 минут |
| asyncio + aiohttp | ~30 секунд |

Работая с AI-агентом, легко забыть проверить качество старого кода. Агент выполнит что дали. Переписывать скрипт надо было раньше — когда аудитория была 100 человек, а не 700.

Урок: перед запуском больших операций — просить агента сначала проанализировать, потом делать.

## Источники

- [Avoiding flood limits](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Avoiding-flood-limits) — wiki python-telegram-bot
- [AIORateLimiter](https://docs.python-telegram-bot.org/en/v22.5/telegram.ext.aioratelimiter.html) — документация
- [Fixing 429 Errors](https://telegramhpc.com/news/574) — retry policies
- [Bots FAQ](https://core.telegram.org/bots/faq) — официальная документация Telegram
