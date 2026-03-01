---
title: "Как делиться скиллами Claude Code"
date: 2026-01-16
description: "Три способа распространять скиллы Claude Code: плагины, комьюнити-реестр и свой маркетплейс. Разбираю что выбрать и как настроить."
tags: ["claude code", "skills"]
section: "Claude Code"
knowledge:
  problem: "Делиться скиллами Claude Code можно только копированием папок — не масштабируется"
  solution: "Три способа: плагин с манифестом, комьюнити-реестр claude-plugins.dev, свой маркетплейс для команды"
  pattern: "skills-distribution-methods"
  tools: ["Claude Code", "claude-plugins.dev", "GitHub", "npx"]
  takeaways:
    - "Манифест плагина — 5 строк JSON в .claude-plugin/plugin.json"
    - "Публичный репо + манифест = автоиндексация в claude-plugins.dev"
    - "Установка одной командой: npx claude-plugins install @username/repo"
    - "15 скиллов за полгода — каждый экономит 15 минут на установку"
    - "Нужна Claude Code версия 2.0.12 или выше"
  metrics:
    skills_count: 15
    manifest_lines: 5
    min_version: "2.0.12"
    time_saved_per_user: "15 минут"
  prerequisites: ["Claude Code 2.0.12+", "GitHub репозиторий"]
---

15 скиллов за полгода. gh-issues, cc-analytics, blog-post...

Каждый раз когда кто-то спрашивает — кидаю ссылку на GitHub и говорю «скопируй папку».

Надоело. Разобрался как делиться нормально.

## Проблема

Скиллы лежат в `~/.claude/skills/`. Хочешь поделиться — копируй руками. Для себя норм. Для десяти человек — уже нет.

В октябре 2025 Anthropic выкатили плагины. Упаковываешь скиллы, команды и хуки в один пакет — установка одной командой.

## Три варианта

| Способ | Для кого | Сложность |
|--------|----------|-----------|
| Плагин + маркетплейс | Публичное распространение | Средняя |
| claude-plugins.dev | Авто-индексация из GitHub | Низкая |
| Свой маркетплейс | Команда / организация | Средняя |

## Вариант 1: Плагин

Папка с манифестом — вот и весь плагин. Структура:

```
my-skills/
├── .claude-plugin/
│   └── plugin.json      # манифест
├── skills/
│   ├── cc-analytics/
│   │   └── SKILL.md
│   └── gh-issues/
│       └── SKILL.md
└── README.md
```

Манифест — пять строк JSON:

```json
{
  "name": "my-skills",
  "description": "Мои скиллы для вайбкодинга",
  "version": "1.0.0",
  "author": { "name": "Your Name" }
}
```

Пять строк — готово.

{{< callout insight >}}
**Структура**

Манифест — в `.claude-plugin/`. Всё остальное (`skills/`, `commands/`, `hooks/`) — в корне. Я сначала положил всё в .claude-plugin и час искал почему не работает.
{{< /callout >}}

## Вариант 2: Комьюнити-реестр

По-моему, самый простой путь — [claude-plugins.dev](https://claude-plugins.dev). Комьюнити-реестр, сканирует публичные GitHub репо автоматически.

Публичный репо + `.claude-plugin/plugin.json` = появишься в реестре. Без заявок.

Установка для пользователей:

```
npx claude-plugins install @username/repo-name
```

CLI добавляет маркетплейс и ставит плагин. Одна команда вместо двух.

## Вариант 3: Свой маркетплейс

Команде нужен контроль — свой маркетплейс. JSON со списком плагинов:

```json
{
  "name": "team-plugins",
  "owner": { "name": "Team Name" },
  "plugins": [
    {
      "name": "code-review",
      "source": "./plugins/code-review",
      "description": "Скилл для код-ревью"
    },
    {
      "name": "deploy-tools",
      "source": {
        "source": "github",
        "repo": "team/deploy-plugin"
      }
    }
  ]
}
```

Хостишь на GitHub. Команда добавляет маркетплейс:

```
/plugin marketplace add team-org/plugins-repo
```

Приватные репозитории тоже работают — нужен `GITHUB_TOKEN`.

## Что выбрать

Один человек? Копируй плагин в `~/.claude/plugins/` — работает сразу.

Хочешь чтобы использовали другие? Публичный репо на GitHub. Реестр найдёт сам.

Команда с приватными репо? Свой маркетплейс — версионирование и контроль доступа.

{{< callout warning "Версия Claude Code" >}}
Нужна 2.0.12 или выше. Проверь: `claude --version`. Нет команды `/plugin` — обновляй.
{{< /callout >}}

## Мой сетап

Репо [ris-claude-code](https://github.com/serejaris/ris-claude-code) — 10 скиллов для вайбкодинга. Добавил манифест, жду индексации в реестре.

Скоро установка будет такой:

```
npx claude-plugins install @serejaris/ris-claude-code
```

Раньше объяснял как копировать 10 папок. Теперь одна команда. Экономит минут 15 на каждого нового пользователя.

---

## Источники

- [Create plugins — Claude Code Docs](https://code.claude.com/docs/en/plugins)
- [Plugin marketplaces — Claude Code Docs](https://code.claude.com/docs/en/plugin-marketplaces)
- [claude-plugins.dev — Community Registry](https://claude-plugins.dev/)
- [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official)
- [Claude Code Must-Haves — January 2026](https://dev.to/valgard/claude-code-must-haves-january-2026-kem)
