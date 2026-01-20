---
title: "Почему GPT не умеет искать: эмбединги для тех, кто не ML-инженер"
date: 2026-01-20
description: "Локальный RAG на M1: ChromaDB, эмбединги и почему генеративная модель не заменит поиск"
tags: ["rag", "embeddings", "claude-code", "вайбкодинг"]
---

Спросил у Claude: "это тоже AI? почему генеративная модель не может делать эмбединги?"

Может. Но не должна.

## Проблема

У меня накопились транскрипты менторских сессий. Часы записей. Хочу спросить "что я обещал Лене по домашке?" — и получить цитату, а не пересказ.

Первая мысль: закинуть в Claude Code. Но один транскрипт — 15000 слов. Десять сессий — 150000 слов, примерно 100K токенов. Контекст Claude — 200K. На второй вопрос уже не хватит.

Нужен RAG.

## Что такое эмбединги

Координаты смысла.

Каждое предложение — точка в пространстве. "Кот спит на диване" и "Кошка лежит на софе" — рядом. "Квантовая механика" — далеко.

Задаёшь вопрос — он тоже становится точкой. Поиск находит ближайшие. Это и есть релевантные куски.

## Почему LLM не заменит эмбединг-модель

Генеративная модель продолжает текст, отвечает на вопросы, пишет код.

Для поиска нужно другое: быстро превратить текст в вектор чисел. Тысячи раз.

Эмбединги работают в 10-100 раз быстрее. На моём M1 Pro all-MiniLM прожёвывает 150K слов за 30 секунд. GPT-5 на ту же задачу потратит минуты — если вообще справится.

Локальная модель бесплатна. API эмбедингов OpenAI (text-embedding-3-small) — $0.02 за миллион токенов. GPT-5 — $1.75 за миллион. Разница в 87 раз.

И качество: эмбединг-модели натренированы именно на поиск похожего. LLM — нет.

По-моему, использовать GPT для эмбедингов — как нанимать хирурга резать хлеб. Справится. Но зачем?

## Решение: ChromaDB + sentence-transformers на M1

Написал агенту:

{{< callout type="insight" >}}
Сделай локальный RAG для папки с транскриптами. M1 Pro, без внешних API. Хочу задавать вопросы по содержимому.
{{< /callout >}}

Что агент собрал:

```python
import chromadb
from chromadb.utils import embedding_functions

# Локальная модель — работает на M1 без GPU
embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

# Персистентное хранилище
client = chromadb.PersistentClient(path="./transcripts_db")
collection = client.get_or_create_collection(
    name="mentor_sessions",
    embedding_function=embed_fn
)
```

Загрузка транскриптов:

```python
from pathlib import Path

for transcript in Path("transcripts").glob("*.txt"):
    text = transcript.read_text()
    # Разбиваем на куски по 500 слов
    chunks = [text[i:i+2000] for i in range(0, len(text), 1800)]

    collection.add(
        documents=chunks,
        ids=[f"{transcript.stem}_{i}" for i in range(len(chunks))],
        metadatas=[{"source": transcript.name}] * len(chunks)
    )
```

Поиск:

```python
results = collection.query(
    query_texts=["что обещал Лене по домашке"],
    n_results=3
)

for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
    print(f"[{meta['source']}]")
    print(doc[:300], "...")
```

## Результат

Вчера спросил "что Лена делала с видеоредактором на третьей сессии" — ответ с цитатой за 0.2 секунды. Раньше искал бы вручную минут десять.

Модель `all-MiniLM-L6-v2` весит 80 МБ и работает на CPU. Выбрал её вместо более тяжёлых (e5-large — 350 МБ) потому что разница в качестве поиска 2-3%, а скорость втрое выше.

## Когда что использовать

Эмбединги — для поиска. LLM — для ответов. RAG связывает их: сначала находим релевантные куски, потом скармливаем модели.

## Источники

- [OpenAI Embeddings Pricing](https://platform.openai.com/docs/pricing) — актуальные цены
- [Sentence Transformers: Pretrained Models](https://www.sbert.net/docs/sentence_transformer/pretrained_models.html) — список моделей
- [ChromaDB Tutorial](https://www.datacamp.com/tutorial/chromadb-tutorial-step-by-step-guide) — DataCamp
- [LLMs are Also Effective Embedding Models](https://arxiv.org/pdf/2412.12591) — почему можно, но не нужно
