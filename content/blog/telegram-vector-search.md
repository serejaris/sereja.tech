---
title: "Семантический поиск по Telegram: мой second brain из чатов"
date: 2026-01-26
description: "Как я сделал поиск по смыслу в своих Telegram-переписках. Telethon, sqlite-vec, OpenAI embeddings — и больше никаких ctrl+F по 50 чатам."
tags:
  - вайбкодинг
  - Telegram
  - RAG
  - sqlite-vec
section: "Проекты"
---

Вася три месяца назад скинул решение бага с async — помню точно. В каком из 47 чатов — уже нет.

Пробовал Ctrl+F: "async", "await", "баг". Telegram выдал 200+ совпадений. Половина — про что угодно, только не то. Стандартный поиск ищет слова. Мне нужен смысл.

Написал инструмент за вечер: качаю сообщения, генерирую эмбеддинги, ищу по семантике. Теперь пишу "то решение с concurrent requests" — нахожу за секунду.

## Проблема

Telegram-поиск работает по ключевым словам. Если забыл конкретное слово — не найдёшь. А я забываю.

Хотел систему, которая понимает контекст:
- "что обсуждали про деплой" — даже если слова "деплой" нет
- "рекомендация книги от Пети" — без поиска по "книга"
- "тот прикольный скрипт" — и оно понимает что "прикольный" = полезный

## Решение

{{< callout type="insight" >}}
Сделай CLI для семантического поиска по Telegram. Скачивай сообщения через Telethon, храни в SQLite с векторами через sqlite-vec, генерируй эмбеддинги через OpenAI.
{{< /callout >}}

Claude Code на Opus 4.5 собрал за вечер. Удивило, что rate limiting не пришлось переделывать — сразу рабочий:

1. **sync.py** — качает сообщения через Telethon. Rate limiting из коробки.

2. **db.py** — SQLite + sqlite-vec. Один файл, никаких внешних баз.

3. **embed.py** — батчами по 100 генерирует эмбеддинги через OpenAI.

4. **search.py** — CLI для поиска. Топ-10 релевантных сообщений с контекстом.

## Rate limiting

Telegram банит за спам к API. Агент сразу заложил защиту:

- Задержка между чатами (1-3 сек)
- Задержка между батчами сообщений
- Обработка FloodWaitError — если Telegram говорит "подожди", ждём

За ночь синхронизировал 60 дней переписки — примерно 15k сообщений из рабочих чатов. По 5-10 чатов за раз, чтобы не нарваться.

## sqlite-vec

Выбрал sqlite-vec вместо Pinecone/Weaviate. Причины:

- Один файл. База данных в `data/messages.db`. Бэкап = копирование файла.
- Нет сервера. Не нужен Docker, не нужен localhost:6333.
- KNN из коробки. `WHERE embedding MATCH ? AND k = 10` — и готово.

По-моему, для личного архива на 50k сообщений — за глаза. Миллионы? Тогда pgvector.

## Как пользуюсь

```bash
# Синхронизация новых сообщений
python sync.py --days 7

# Генерация эмбеддингов для новых
python embed.py --batch 100

# Поиск
python search.py "решение с rate limiting в телеграме"
```

Результат: сообщения отсортированы по релевантности, с датой, именем отправителя и ссылкой на чат.

## Что дальше

Планирую:

- **MCP-сервер** — чтобы Claude Code мог искать по моей переписке прямо из терминала
- **Hybrid search** — векторы + FTS5 для точных совпадений
- **Локальные эмбеддинги** — ollama вместо OpenAI, для приватности

Пока работает в CLI. Хватает.

---

## Источники

- [telegram-search](https://github.com/groupultra/telegram-search) — похожий проект с 3.7k звёзд
- [sqlite-vec](https://github.com/asg017/sqlite-vec) — векторное расширение для SQLite
- [How sqlite-vec Works](https://medium.com/@stephenc211/how-sqlite-vec-works-for-storing-and-querying-vector-embeddings-165adeeeceea) — подробный разбор
- [RAG in SQLite](https://towardsdatascience.com/retrieval-augmented-generation-in-sqlite/) — туториал по RAG на sqlite-vec
- [Telegram 429 handling](https://pcg-telegram.com/blogs/893) — rate limiting в 2025-2026
