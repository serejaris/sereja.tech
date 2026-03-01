---
title: "SEO для блога в эру AI: что реально работает в 2026"
date: 2026-01-10
description: "Разбираю SEO для персонального блога в 2026. JSON-LD Schema, Person vs Organization, structured data — что критично для AI-поисковиков."
tags: ["seo", "json-ld"]
section: SEO
knowledge:
  problem: "Классический SEO с meta-тегами недостаточен для AI-поисковиков в 2026 году"
  solution: "Использовать трёхуровневый SEO: базовые мета-теги, социальные карточки и JSON-LD structured data"
  pattern: "json-ld-structured-seo"
  tools: ["JSON-LD", "Schema.org", "Google Rich Results Test"]
  takeaways:
    - "SEO в 2026 — три слоя: basic meta, social cards, JSON-LD structured data"
    - "Для персонального блога publisher должен быть Person, не Organization"
    - "BlogPosting лучше Article для личного блога — помогает с E-E-A-T"
    - "Person Schema на главной связывает профили через sameAs и показывает экспертизу"
  prerequisites: ["Hugo или другой SSG"]
---

Переделывал SEO на своём сайте. Думал — добавлю meta description и хватит.

Оказалось, в 2026 году этого мало.

AI-поисковики хотят structured data, а не просто текст в тегах.

## Почему старый SEO не работает

Классический подход: title, description, keywords. Google читает HTML, индексирует текст, показывает в результатах.

Проблема: AI-поисковики (Perplexity, SearchGPT, Gemini) работают иначе. Им нужен контекст. Кто автор? Какой тип контента? Как связан с другими страницами?

Без structured data AI видит просто текст. С ним — понимает структуру.

{{< callout insight >}}
SEO в 2026 — это не оптимизация под алгоритмы. Это разметка данных так, чтобы любая система (Google, AI, RSS) понимала контент одинаково.
{{< /callout >}}

## Три уровня SEO

| Уровень | Что включает | Критичность |
|---------|--------------|-------------|
| Basic | title, description, canonical | Обязательно |
| Social | Open Graph, Twitter Cards | Для шеринга |
| Structured | JSON-LD Schema | Критично для AI |

## JSON-LD: главное оружие

JSON-LD — это способ сказать поисковику: «вот структурированные данные о странице». Не в HTML-атрибутах, а в чистом JSON.

```json
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "Заголовок статьи",
  "author": {
    "@type": "Person",
    "name": "Имя Автора",
    "url": "https://site.com"
  },
  "publisher": {
    "@type": "Person",
    "name": "Имя Автора"
  },
  "datePublished": "2026-01-10"
}
```

{{< callout warning "Publisher = Person, не Organization" >}}
Для персонального блога publisher должен быть Person. Organization — для компаний с логотипом и юрлицом. Google это различает.
{{< /callout >}}

## Person Schema для главной

На главной странице личного сайта нужна отдельная Person schema. Она связывает все ваши профили и показывает экспертизу.

```json
{
  "@type": "Person",
  "name": "Имя",
  "url": "https://site.com",
  "jobTitle": "Должность",
  "sameAs": [
    "https://twitter.com/username",
    "https://t.me/channel"
  ],
  "knowsAbout": ["тема 1", "тема 2"],
  "alumniOf": [
    {"@type": "Organization", "name": "Компания"}
  ]
}
```

Поля `sameAs` связывают профили. `knowsAbout` показывает экспертизу. `alumniOf` — прошлый опыт.

## Какой тип для какой страницы

Не все страницы одинаковые. Каждая требует свой тип schema:

| Страница | Schema Type | Зачем |
|----------|-------------|-------|
| Главная | Person | E-E-A-T сигналы, связь профилей |
| Список блога | Blog | Контекст для коллекции статей |
| Статья | BlogPosting | Rich snippets, автор, дата |

## BlogPosting vs Article

Оба работают, но есть разница:

- `BlogPosting` — для блогов, личного контента, неформальных статей
- `Article` — для новостей, формального контента

Для персонального блога всегда используй `BlogPosting`. Он лучше показывает авторство и помогает с E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness).

{{< callout insight >}}
Google оценивает авторитетность через связи: author → sameAs → социальные профили. Чем больше связей, тем выше доверие. Person schema на главной + BlogPosting с автором = максимум E-E-A-T сигналов.
{{< /callout >}}

## Чеклист для блога

Минимум для каждой страницы:

- `title` — уникальный, до 60 символов
- `meta description` — до 160 символов
- `canonical` — абсолютный URL
- `og:title`, `og:description`, `og:type`
- `twitter:card`, `twitter:site`
- JSON-LD с правильным @type

Для главной добавь:

- Person schema с sameAs
- `og:site_name`

## Как проверить

Google предоставляет инструменты:

- [Rich Results Test](https://search.google.com/test/rich-results) — проверка structured data
- [Schema Validator](https://validator.schema.org/) — валидация JSON-LD

Вставляешь URL или код — видишь ошибки и warnings.

## Итого

SEO в 2026 — это три слоя: базовые мета-теги, социальные карточки, structured data. Без JSON-LD AI-поисковики видят просто текст. С ним — понимают контекст, авторство, связи.

Для персонального блога: Person schema на главной, BlogPosting на статьях, publisher = Person (не Organization).

## Источники

- [Article structured data](https://developers.google.com/search/docs/appearance/structured-data/article) — Google Search Central
- [Schema Markup Guide 2026](https://backlinko.com/schema-markup-guide) — Backlinko
- [Structured data for search and AI](https://yoast.com/structured-data-schema-ultimate-guide/) — Yoast
- [Schema Markup: Critical for SERP Visibility](https://almcorp.com/blog/schema-markup-detailed-guide-2026-serp-visibility/) — ALM Corp
- [BlogPosting Schema: Usage and Formatting](https://schemascalpel.com/the-importance-of-blogposting-schema-usage-and-formatting/) — Schema Scalpel
- [BlogPosting Schema Validator](https://www.schemavalidator.com/validate/article/blog) — Schema Validator
- [Person Schema](https://schema.org/Person) — Schema.org
