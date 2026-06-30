<!-- hq-readme-ru: 2026-05-09 -->
# sereja.tech

Коротко: Блог про AI-агентов, вайбкодинг и паттерны Claude Code.

## Что здесь

- Назначение: Блог про AI-агентов, вайбкодинг и паттерны Claude Code.
- Основной стек: HTML.
- Видимость: публичный репозиторий.
- Статус: активный репозиторий; актуальность проверять по issues и последним коммитам.

## Где смотреть работу

- Задачи и текущие решения: GitHub Issues этого репозитория.
- Код и материалы: файлы в корне и профильные папки проекта.
- Связь с HQ: если проект влияет на продукт, контент или воронку, сверяйте канон в `0_hq` и репозитории-владельце.

## Для агентов

- Сначала прочитайте этот README и открытые issues.
- Не переносите сюда канон соседних проектов без ссылки на источник.
- Перед правками проверьте существующие scripts, package.json/pyproject и локальные инструкции.

---

## Исходный README

# sereja.tech

**Блог про вайбкодинг и Claude Code.**

98+ статей о разработке с AI-агентами: практические кейсы, автоматизация, многоагентные системы.

## Последние статьи

| Дата | Статья |
|------|--------|
| 2026-06-30 | [Сто агентов, ноль результата](https://sereja.tech/blog/orchestration-without-goals/) |
| 2026-06-29 | [Orca вместо четырёх терминалов](https://sereja.tech/blog/orca-menedzher-agentov/) |
| 2026-06-13 | [Генерируем таймкоды для YouTube из транскрипта с помощью AI](https://sereja.tech/blog/youtube-chapters-split-concern/) |
| 2026-06-13 | [undercast: оверлей для OBS, сделанный Fable 5](https://sereja.tech/blog/undercast-obs-overlay-fable-5/) |
| 2026-06-12 | [Запустил AI-радио, которое делают агенты](https://sereja.tech/blog/ai-radio-agents/) |
| 2026-06-10 | [Перешёл на Claude Fable 5: цены, effort, кейсы](https://sereja.tech/blog/claude-fable-5-review/) |
| 2026-04-30 | [OTel для Claude Code — рентген твоих скиллов](https://sereja.tech/blog/claude-code-skills-grafana/) |
| 2026-04-27 | [Свой Miro за 30 минут вместо подписки](https://sereja.tech/blog/svoy-miro-za-30-minut/) |
| 2026-04-22 | [Как я научил Claude Code писать техно-музыку](https://sereja.tech/blog/claude-code-techno-strudel-mcp/) |
| 2026-04-22 | [Как трекать задачи агентом в нескольких репо](https://sereja.tech/blog/tracking-tasks-agent-multi-repo/) |
[Все статьи →](https://sereja.tech/blog/)

## Быстрый старт

```bash
git clone https://github.com/serejaris/sereja.tech.git
cd sereja.tech
hugo server -D
# → http://localhost:1313/blog
```

## Что внутри

- **Claude Code** — скиллы, хуки, воркфлоу
- **Пайплайны** — видео, RAG, Telegram боты
- **Автоматизация** — MIDI-контроль OBS, терминал, CI/CD
- **Практика** — SEO, health checks, многоагентные системы

## Структура

```
sereja.tech/
├── content/blog/    # Статьи (Markdown)
├── layouts/         # Hugo шаблоны
├── static/          # JS, картинки
└── hugo.toml        # Конфиг
```

## Стек

| Компонент | Технология |
|-----------|------------|
| SSG | Hugo |
| Хостинг | Vercel |
| SEO | JSON-LD, Open Graph |

## Ссылки

| Ресурс | URL |
|--------|-----|
| Блог | [sereja.tech](https://sereja.tech) |
| Telegram | [@ris_ai](https://t.me/ris_ai) |
| Комьюнити | [@vibecod3rs](https://t.me/vibecod3rs) |
| YouTube | [@serejaris](https://youtube.com/@serejaris) |

## Лицензия

Контент © Сережа Рис. Код — MIT.
