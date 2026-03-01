---
title: "Массовая рассылка в Telegram: почему альбом на 800 юзеров шёл 30 минут"
date: 2026-01-25
description: "Как ускорить отправку медиа-альбомов в Telegram Bot API с 30 минут до 60 секунд, используя file_id вместо повторной загрузки файлов"
tags: ["telegram bot", "python"]
knowledge:
  problem: "Массовая рассылка медиа-альбомов в Telegram занимает 30+ минут из-за повторной загрузки файлов"
  solution: "Использование file_id после однократной загрузки сокращает трафик с 15 ГБ до 5 МБ и время с 30 минут до 60 секунд"
  pattern: "telegram-file-id-caching"
  tools: ["Telegram Bot API", "Python", "asyncio"]
  takeaways:
    - "Повторная загрузка 6 картинок × 3 МБ на 871 юзера = 15 ГБ трафика"
    - "file_id после однократной загрузки снижает трафик до ~5 МБ"
    - "Лимит Telegram — 30 сообщений/секунду на токен"
    - "file_id персистентный — можно хранить в базе и использовать повторно"
  metrics:
    users: 871
    upload_before_gb: 15
    upload_after_mb: 5
    time_before_min: 30
    time_after_sec: 60
  related:
    - slug: "telegram-broadcast-slow"
      relation: "проблема медленной синхронной рассылки без file_id"
---

Написал рассылку альбома из 6 картинок на 871 пользователя `@hashslash_bot`. Ожидал минуту-две. Полчаса — 100 человек.

Я загружал 18 мегабайт 871 раз.

## Что пошло не так

Попросил Claude Code на Opus 4.5 написать скрипт:

{{< callout type="insight" >}}
Напиши broadcast.py для @hashslash_bot. Отправь альбом из 6 картинок с caption, следом — сообщение с inline-кнопкой. Используй asyncio.
{{< /callout >}}

Агент выдал код. Выглядит правильно: `sendMediaGroup`, `asyncio.gather`. Запустил.

50 юзеров — минута. 100 — две. На 871 это 17+ минут.

## Почему так медленно

Вот что делал мой код:

```python
# НЕПРАВИЛЬНО — upload каждый раз
for user_id in users:
    files = {f"photo{i}": open(path, 'rb') for i, path in enumerate(images)}
    requests.post(f"{API}/sendMediaGroup", files=files, data={"chat_id": user_id})
```

6 картинок × 3 МБ = 18 МБ на юзера. 871 человек — 15 гигабайт upload.

Параллельность не помогает. Упираешься в скорость сети. Telegram ждёт файлы, потом отправляет.

## Решение: file_id

Telegram хранит файлы на своих серверах. При отправке возвращается `file_id`. Дальше можно использовать его вместо файла.

Отправляю альбом себе один раз:

```python
resp = requests.post(f"{API}/sendMediaGroup", files=files, data={
    "chat_id": MY_ID,
    "media": json.dumps([{"type": "photo", "media": f"attach://photo{i}"} for i in range(6)])
})

file_ids = [msg['photo'][-1]['file_id'] for msg in resp.json()['result']]
```

Теперь рассылка — это JSON без загрузки:

```python
for user_id in users:
    media = [{"type": "photo", "media": fid} for fid in file_ids]
    media[0]["caption"] = "Текст подписи"
    requests.post(f"{API}/sendMediaGroup", json={"chat_id": user_id, "media": media})
```

Килобайты вместо мегабайт.

## Разница

| Способ | Трафик | Время |
|--------|--------|-------|
| Upload каждый раз | ~15 ГБ | 30+ мин |
| file_id | ~5 МБ | ~60 сек |

Лимит Telegram — 30 сообщений/секунду на токен. 871 × 2 запроса = меньше минуты.

## Три правила

1. **Загружай один раз** — отправь себе, сохрани `file_id`
2. **Рассылай через file_id** — мгновенно, без upload
3. **file_id персистентный** — храни в базе, используй повторно

По-моему, это самая недооценённая фича Bot API. Я раньше пролистывал эту секцию в доках. Оказалось — критическая оптимизация для любой рассылки с медиа.

## Источники

- [Telegram Bot API: Sending files](https://core.telegram.org/bots/api#sending-files)
- [grammY: File Handling](https://grammy.dev/guide/files.html)
- [Telegram Bots FAQ](https://core.telegram.org/bots/faq#can-i-count-on-file_ids-to-be-persistent)
