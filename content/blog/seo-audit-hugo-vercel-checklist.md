---
title: "SEO-аудит блога за одну сессию Claude Code"
date: 2026-02-07
description: "Открыл Google Search Console — 0 sitemap, 307 redirect, 0 видео. За сессию Claude Code нашёл 5 проблем. Чеклист для Hugo+Vercel."
tags: ["seo", "hugo", "claude code"]
image: "/images/blog/seo-audit-hugo-vercel-checklist-preview.png"
---

Открыл Google Search Console — ноль сабмитнутых sitemap, 307 redirect на каждом запросе, ноль discovered videos. Три красных флага на пустом месте.

За одну сессию агент нашёл и починил пять проблем. Некоторые я бы не заметил ещё полгода.

## Как началось

Захотел понять, индексирует ли Google мой блог нормально. Зашёл в Search Console. Увидел пустоту.

Написал Claude Code на Opus 4.6:

{{< callout insight >}}
Мне нужно сабмитить sitemap? Проведи комплексное исследование лучших практик для этой проблемы, используя Exa MCP.
{{< /callout >}}

Агент начал копать. Проверил sitemap, robots.txt, редиректы, structured data. Каждая проверка вскрывала новую проблему.

## 1. Sitemap: 157 мусорных URL

Hugo по умолчанию тащит в sitemap всё подряд. Каждый тег — отдельный URL. Страница таксономии — URL. Пустые разделы — URL. В моём sitemap оказалось 157 адресов. Реальных статей — 63.

Почему это плохо? Google имеет crawl budget — количество страниц, которые бот готов обойти за визит. Если 60% sitemap — мусор, бот тратит ресурсы на пустые страницы тегов вместо контента.

Масштаб проблемы видно по чужим кейсам. [Маркетплейс удалил 600 тысяч](https://blog.seocopilot.com/p/case-study-how-this-brand-removed-600k-pages-and-traffic-went-up) low-value страниц из индекса — +30% кликов, количество страниц в ТОП-3 удвоилось за четыре месяца. [Страховая компания](https://www.seerinteractive.com/work/case-studies/content-pruning-efforts-help-reverse-traffic-loss) убрала 14 тысяч thin content страниц — +23% органического трафика и +8% crawl budget на важные секции. У меня масштаб скромнее, но пропорция та же: 60% sitemap — мусор.

Агент настроил Hugo генерировать sitemap только для blog section. 157 стало 63.

## 2. robots.txt без Sitemap:

Hugo генерирует robots.txt. Но по умолчанию там только `User-agent: *` и `Allow: /`. Директивы `Sitemap:` нет.

Google умеет находить sitemap без подсказки — проверяет стандартные пути. Но зачем полагаться на угадывание? Явная директива `Sitemap: https://sereja.tech/sitemap.xml` в robots.txt — рекомендация из документации Google Search Central.

Агент добавил. Мелочь, но из таких мелочей складывается технический SEO.

## 3. Redirect: 307 вместо 308

Это было самое неочевидное. В Vercel у меня настроен primary domain `sereja.tech`. Запросы на `www.sereja.tech` идут через redirect. Логично.

Проблема: Vercel по умолчанию отдавал 307 — temporary redirect. Temporary значит временный. Google видит 307 и думает: "окей, это временно, link equity не передаю". Каждый запрос — потеря SEO-веса.

308 — permanent redirect. Передаёт link equity, Google понимает что это навсегда. Разница в одну цифру, а последствия — на всё время жизни домена.

Тут пригодился ещё один инструмент. Попросил [Comet от Perplexity](https://comet.perplexity.ai/) зайти в админку Vercel и поменять настройку. Он сам нашёл Domains, переключил redirect type на 308 Permanent. Две минуты — и я даже не открывал дашборд.

## 4. VideoObject: 0 discovered videos

В блоге несколько постов с YouTube-видео. Вставляю через iframe. Google Search Console показывает: discovered videos — 0.

Причина: Google не распознаёт видео без structured data. iframe сам по себе — просто блок HTML. Без JSON-LD разметки VideoObject поисковик не знает что на странице есть видео.

По [schema.org](https://schema.org/VideoObject) обязательные поля VideoObject — `name`, `description`, `thumbnailUrl`, `uploadDate`. Для YouTube-видео стоит добавить ещё `contentUrl` и `embedUrl` — они опциональные, но дают Google больше контекста. Агент добавил JSON-LD в Hugo-шаблон для постов с видео.

Про JSON-LD и structured data подробнее — в [SEO для блога в эру AI](/blog/seo-for-ai-era). VideoObject добавил для постов с видео из [видео-пайплайна](/blog/video-pipeline-claude-code).

## 5. changefreq и priority: бесполезные поля

В сгенерированном Hugo sitemap были поля `changefreq` и `priority`. Классический совет из 2015 года: поставь `changefreq: weekly` и `priority: 0.8`.

Google эти поля [официально игнорирует](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap). Не "иногда учитывает". Не "частично влияет". Игнорирует полностью.

Агент убрал оба поля из конфига Hugo. Sitemap стал чище, без лишнего шума.

## До и после

```
BEFORE:                              AFTER:
┌──────────────┐                     ┌──────────────┐
│ sitemap.xml  │ 157 URLs            │ sitemap.xml  │ 63 URLs
│ tags + empty │                     │ blog only    │
├──────────────┤                     ├──────────────┤
│ robots.txt   │ no Sitemap:         │ robots.txt   │ Sitemap: ✓
├──────────────┤                     ├──────────────┤
│ sereja.tech  │ 307 → www           │ sereja.tech  │ 308 redirect
├──────────────┤                     ├──────────────┤
│ YouTube      │ 0 VideoObject       │ YouTube      │ VideoObject ✓
├──────────────┤                     ├──────────────┤
│ changefreq   │ weekly              │ changefreq   │ removed
└──────────────┘                     └──────────────┘
```

## Промпт как мост между инструментами

Когда агент исследовал лучшие практики через Exa MCP, он сформулировал поисковые запросы — конкретные, с контекстом. Я взял один из них и вставил в Perplexity browser.

Получил другой срез. Exa выдаёт технические статьи и документацию. Perplexity — обобщения и свежие дискуссии. Промпт одного инструмента как вход для другого. Раньше я бы гуглил сам и читал десять вкладок. Тут — два инструмента покрыли тему за минуты.

## Агент как SEO-аудитор

Я бы сам проверил sitemap. Может быть, заметил бы 307. Но VideoObject? changefreq? Пустой robots.txt?

Агент проверяет методично. Открывает файл, читает каждое поле, сравнивает с документацией. Не торопится. Не пропускает "мелочи". Я бы в 80% случаев остановился после первых двух проблем — когда видишь один фикс, кажется что остальное в порядке. Агент так не думает. Он проверяет всё.

Этот подход — часть моего [воркфлоу публикации статей](/blog/blog-post-pipeline), где агенты делают research и черновик, а я направляю.

{{< callout insight >}}
SEO-аудит персонального блога — конечный список проверок, документация в открытом доступе, результат сразу виден в Search Console. Если ещё не прогонял свой сайт — попробуй. Одна сессия с агентом заменяет вечер гугления.
{{< /callout >}}

Google Search Console обновляется не мгновенно. Но технически всё на месте: sitemap чистый, redirect правильный, видео размечены. Пять проблем за одну сессию.
