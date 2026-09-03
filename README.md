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

119 статей о разработке с AI-агентами: практические кейсы, автоматизация, многоагентные системы.

## Последние статьи

| Дата | Статья |
|------|--------|
| 2026-09-03 | [GPT-6 Astra вышла. Переходить с Sol пока рано](https://sereja.tech/blog/gpt-6-astra/) |
| 2026-08-22 | [Повторил забег агентов: 11/18 стало 17/18](https://sereja.tech/blog/ox-alpha-yesterday-vs-today/) |
| 2026-08-22 | [ox-alpha: 6 агентов, 3 бенча](https://sereja.tech/blog/ox-alpha-harness-pool/) |
| 2026-08-18 | [Гайд по использованию Grok Bot](https://sereja.tech/blog/grok-bot-cloud-agents-guide/) |
| 2026-08-13 | [Grok 4.6 интересный. Гнаться незачем](https://sereja.tech/blog/grok-46-day-one/) |
| 2026-08-05 | [Какую подписку Claude выбрать для работы: $20, $100 или $200](https://sereja.tech/blog/claude-max-real-limits-api-cost/) |
| 2026-08-04 | [Как подключить подписку Anthropic к Hermes](https://sereja.tech/blog/claude-max-hermes-telegram/) |
| 2026-08-03 | [Почему агент не может выбрать лучший код](https://sereja.tech/blog/best-practices-code/) |
| 2026-07-18 | [Kimi K3 за 1:47: сильный агент с одной проблемой](https://sereja.tech/blog/kimi-k3-guide/) |
| 2026-07-18 | [База знаний для агентов: вход, слои и обслуживание](https://sereja.tech/blog/agent-knowledge-base/) |
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
