---
title: "Текст + картинка в одном сообщении Telegram"
date: 2026-01-17
description: "Как отправить длинный текст с картинкой в одном сообщении Telegram. LinkPreviewOptions, catbox.moe и почему нужна задержка перед отправкой."
tags: ["telegram", "bot api"]
section: Telegram
---

Бот для дайджестов. Текст + комикс снизу, в одном сообщении.

Публикую — картинки нет. Через 5 секунд обновляю чат — появилась.

Разбираюсь.

## Задача

Хочу отправить длинный текст (2000+ символов) с картинкой. Картинка должна быть под текстом, крупная.

Стандартный `sendPhoto` не подходит — у него лимит caption в 1024 символа. Для Premium — 2048, но всё равно мало.

| Метод | Лимит текста |
|-------|--------------|
| sendPhoto (caption) | 1024 / 2048 символов |
| sendMessage | 4096 символов |

## Решение: LinkPreviewOptions

В Bot API 7.0 добавили `LinkPreviewOptions`. Можно указать URL картинки, и Telegram покажет её как превью ссылки. Текст при этом полный — до 4096 символов.

```python
from telegram import LinkPreviewOptions

await bot.send_message(
    chat_id=channel_id,
    text=digest_text,  # до 4096 символов
    parse_mode="HTML",
    link_preview_options=LinkPreviewOptions(
        url=image_url,
        prefer_large_media=True,
        show_above_text=False  # картинка снизу
    )
)
```

Три параметра, которые нужны:

- `url` — куда смотреть за картинкой
- `prefer_large_media=True` — иначе будет миниатюра
- `show_above_text=False` — картинка снизу, не сверху

## Где хостить картинку

Первая мысль — Telegraph. Своя платформа, должно работать идеально. Но `telegra.ph/upload` возвращал 400 на PNG с альфа-каналом. Не стал разбираться.

Взял [catbox.moe](https://catbox.moe) — бесплатный хостинг, файлы до 200 МБ, без регистрации. Загружаешь картинку, получаешь прямую ссылку вида `https://files.catbox.moe/abc123.png`.

```python
async def upload_image(image_bytes: bytes) -> str:
    async with aiohttp.ClientSession() as session:
        data = aiohttp.FormData()
        data.add_field('reqtype', 'fileupload')
        data.add_field(
            'fileToUpload',
            image_bytes,
            filename='image.png',
            content_type='image/png'
        )
        async with session.post(
            "https://catbox.moe/user/api.php",
            data=data
        ) as resp:
            return (await resp.text()).strip()
```

## Проблема: картинка не появляется сразу

Вот тут меня и поймало.

Публикую сообщение — текст есть, картинки нет. Жду 5 секунд, обновляю — появилась. Что происходит?

{{< callout insight >}}
Когда бот отправляет сообщение с URL, Telegram должен скачать картинку, обработать и закэшировать. Это занимает время. Если картинка новая — превью появится не сразу.
{{< /callout >}}

Для Telegraph это работало мгновенно — у Telegram специальная обработка своего домена. А catbox.moe — внешний сервис, его нужно обойти и закэшировать.

## Фикс: задержка перед отправкой

Можно ли программно "прогреть" кэш? Изучил вопрос:

- `messages.getWebPagePreview` — MTProto метод, работает только для user accounts, боты не могут
- `@WebpageBot` — официальный бот Telegram, но только вручную

Программного способа для ботов нет. Решение тупое, но рабочее:

```python
import asyncio

# 1. Загружаем картинку
image_url = await upload_image(comic_image)

# 2. Даём Telegram время закэшировать
await asyncio.sleep(4)

# 3. Отправляем сообщение
await bot.send_message(...)
```

4 секунды — с запасом. Можно и 3, но стабильнее 4.

Почему 4 секунды? По обсуждениям на Stack Overflow — 2-3 секунды минимум. Я взял 4 с запасом. Дайджест публикуется раз в день, подождать не проблема.

## Итого

Если нужен длинный текст с картинкой в одном сообщении:

1. Хостишь картинку (catbox.moe, imgbb, свой сервер)
2. Используешь `sendMessage` + `LinkPreviewOptions`
3. Добавляешь задержку 3-4 секунды между загрузкой и отправкой

Костыль? Да. Работает? Тоже да.

## Источники

- [LinkPreviewOptions — Telegram Bot API](https://core.telegram.org/bots/api#linkpreviewoptions)
- [python-telegram-bot docs](https://docs.python-telegram-bot.org/en/v21.8/telegram.linkpreviewoptions.html)
- [Catbox.moe — хостинг](https://catbox.moe/)
- [Increase caption limit — Telegram Bugs](https://bugs.telegram.org/c/1022)
- [long-caption-bot — обход лимита](https://github.com/arashnm80/long-caption-bot)
