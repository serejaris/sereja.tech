# sereja.tech

Персональный сайт-визитка Сережи Риса — создателя школы вайбкодинга и сооснователя AI-студии HSL.

## Что внутри

- **Главная** — ссылки на проекты, соцсети и школу
- **Блог** — статьи про вайбкодинг, Claude Code и AI-инструменты

## Локальная разработка

```bash
python3 -m http.server 8000
```

Открыть http://localhost:8000

## Структура

```
├── index.html          # Главная страница
├── blog/
│   ├── index.html      # Список статей
│   ├── sitemap.xml     # SEO карта сайта
│   └── *.html          # Статьи
└── vercel.json         # cleanUrls
```

## Деплой

GitHub Pages при пуше в `main`.

## Ссылки

- [sereja.tech](https://sereja.tech) — сайт
- [vibecoding.phd](https://vibecoding.phd) — школа вайбкодинга
- [hsl.sh](https://hsl.sh) — AI-студия
