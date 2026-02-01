---
title: "Правка → Правило: как научить агента не повторять ошибки"
date: 2026-02-01
description: "Паттерн для работы с AI-агентами: исправил ошибку — записал правило — больше не повторится. Fix once, remember forever."
tags: ["claude-code", "вайбкодинг", "agents", "cursor"]
---

Сегодня агент забыл обновить exports в index.ts. Снова. Третий раз за неделю.

Раньше я бы просто исправил. Открыл файл, добавил строчку, продолжил работу. Через день — та же проблема.

Теперь другой подход: исправил → записал правило → больше не повторится.

## Проблема: агенты забывают

AI-агенты не помнят ошибки между сессиями. Claude Code забывает что делал вчера. Cursor не знает какие грабли ты наступал в прошлом проекте.

Каждая сессия — чистый лист. Агент читает код, видит контекст, выполняет задачу. Но его память заканчивается на границе окна в 200k токенов.

Исправил ошибку — записал коммент в коде? Агент может его пропустить. Сказал устно "не делай так"? Через час забудет.

Нужен способ накапливать опыт. Превращать правки в правила.

## Решение: файлы правил

Все современные агенты читают правила проекта из файлов:

- Claude Code — `CLAUDE.md` и `.claude/rules/`
- Cursor — `.cursorrules` или `.cursor/rules/`
- Windsurf — `.windsurfrules`
- Copilot — custom instructions

Паттерн один: исправил ошибку → добавь правило в файл → больше не повторится.

```
ОШИБКА                    ПРАВИЛО                   РЕЗУЛЬТАТ
   │                          │                          │
   │ Забыл обновить      →    │ "Always update        →  │ Больше
   │ index.ts                 │  exports in              │ не забывает
   │                          │  index.ts"               │
```

## Compound effect

Каждое правило — крошечное улучшение. Одно правило даёт +1% качества. Но правила накапливаются.

Через месяц у тебя 20 правил. Через год — 200. Агент становится идеально настроенным под твой проект.

```
День 1: база                День 30: +20 правил         День 365: +200 правил
────────────────            ────────────────────        ─────────────────────
│ CLAUDE.md  │              │ CLAUDE.md        │        │ CLAUDE.md         │
│ - команды  │      →       │ - команды        │   →    │ - команды         │
│ - структура│              │ - структура      │        │ - структура       │
└────────────┘              │                  │        │                   │
                            │ .claude/rules/   │        │ .claude/rules/    │
                            │ ├── exports.md   │        │ ├── exports.md    │
                            │ ├── testing.md   │        │ ├── testing.md    │
                            │ └── commits.md   │        │ ├── commits.md    │
                            └──────────────────┘        │ ├── database.md   │
                                                        │ ├── api.md        │
                                                        │ └── ... (10 more) │
                                                        └───────────────────┘

Качество работы агента:      Качество +20%              Качество +80%
```

Research показывает: prompt optimization даёт +5.19% улучшение метрик. Это измеримо. Compound effect работает.

## Claude Code: модульные правила

В корне проекта — `CLAUDE.md`. Навигация, команды запуска, критичные правила.

Детали выносятся в `.claude/rules/`:

```
.claude/
├── rules/
│   ├── database.md      # схема БД, частые ошибки SQL
│   ├── testing.md       # как запускать тесты, фикстуры
│   ├── frontend/
│   │   └── exports.md   # правила для index.ts
│   └── commits.md       # conventional commits, стиль
└── skills/
    └── ...
```

Агент забыл обновить index.ts? Создаю `.claude/rules/frontend/exports.md`:

```markdown
# Frontend Exports

## index.ts Updates

When creating new components, ALWAYS update `index.ts`:

1. Add component to exports
2. Maintain alphabetical order
3. Group by type (components, hooks, utils)

Common mistake: creating component without export.
```

Следующий раз агент читает это правило перед работой с фронтендом. Ошибка не повторяется.

## Path-targeted rules

В начале файла правил можно указать когда их применять:

```markdown
---
paths: frontend/**/*.ts, frontend/**/*.tsx
---

# Frontend Rules
...
```

Теперь эти правила подгружаются только при работе с фронтендом. Бэкендер их не видит — контекст не засоряется.

## Cursor: от .cursorrules к .cursor/rules/

Cursor изначально поддерживал один файл — `.cursorrules`. Все правила в одном месте.

Проблема та же что и с CLAUDE.md: файл раздувается до 500+ строк. Агент читает всё, но применяет выборочно.

С января 2026 Cursor поддерживает `.cursor/rules/` — модульную структуру как в Claude Code.

Переход простой:
1. Создаёшь `.cursor/rules/`
2. Разбиваешь `.cursorrules` по доменам
3. Добавляешь `paths:` для фильтрации

Старый `.cursorrules` можно оставить — он работает как fallback.

## AGENTS.md: универсальный стандарт

Появился новый формат — `AGENTS.md`. Это попытка стандартизировать правила между разными AI-инструментами.

Идея: один файл работает в Claude Code, Cursor, Windsurf, Copilot. Пишешь раз, применяется везде.

Структура похожа на CLAUDE.md:
- Команды запуска
- Архитектура проекта
- Правила стиля
- Частые ошибки

Формат пока не финализирован. Но направление правильное: правила должны быть переносимыми.

## Reflection hooks: учись у агента

В конце сессии спроси агента:

> "Какие проблемы ты заметил? Что можно добавить в правила?"

Агент видит паттерны которые ты можешь пропустить:
- "Три раза пришлось уточнять формат дат — стоит добавить в правила"
- "База данных использует snake_case, но я генерил camelCase — нужно явно указать"
- "Тесты падали из-за отсутствующих фикстур — добавь секцию про setup"

Это обратная связь. Используй её.

## Практический workflow

1. **Агент ошибся** — исправляешь руками или через промпт
2. **Анализируешь** — это разовое или повторяющееся?
3. **Формулируешь правило** — короткое, конкретное
4. **Добавляешь в нужный файл** — database.md, testing.md, exports.md
5. **Тестируешь** — следующая сессия, агент следует правилу?

Правило работает — оставляешь. Не работает — уточняешь формулировку.

## Примеры правил

### Частые ошибки БД

```markdown
## Before Querying

Check schema first:

\`\`\`bash
sqlite3 backend/cohorts.db ".schema lessons"
\`\`\`

Common mistakes:
- lesson_date → date
- title, topic → summary
- name → first_name, last_name
```

### Тесты перед коммитом

```markdown
## Testing Before Commit

ALWAYS run tests before git commit:

\`\`\`bash
cd backend && pytest tests/ -v
\`\`\`

If tests fail — fix, don't skip.
```

### Conventional commits

```markdown
## Commit Messages

Use conventional commits:
- feat: new feature
- fix: bug fix
- refactor: code change without behaviour change
- docs: documentation only
- chore: tooling, dependencies

Example: `feat(frontend): add dark mode toggle`
```

## Когда НЕ добавлять правила

Не всё должно быть правилом:

- **Разовые кейсы** — не пригодятся снова
- **Очевидные вещи** — "пиши читаемый код"
- **Слишком специфичное** — "в файле X на строке 42 не трогай"

Правила для паттернов. Если видишь проблему второй раз — пора записать.

## Главный вывод

Fix once, remember forever. Агент учится твоим правилам.

Каждая правка — возможность улучшить систему. Превращай ошибки в правила. Со временем агент становится идеальным под тебя.

Compound effect работает. Через месяц заметишь разницу. Через год будет казаться что агент читает мысли.

Он не читает. Он читает твои правила.

## Источники

- [The Complete Guide to CLAUDE.md — Builder.io](https://www.builder.io/blog/claude-md-guide)
- [Creating the Perfect CLAUDE.md — Dometrain](https://dometrain.com/blog/creating-the-perfect-claudemd-for-claude-code/)
- [Cursor Rules Directory](https://cursor.directory/)
- [AGENTS.md Standard Proposal — GitHub](https://github.com/collective-agents/AGENTS.md)
- [Prompt Optimization for LLMs: +5.19% improvement](https://arxiv.org/abs/2401.12345)
- [Using AI Coding Assistants — Modular Docs](https://docs.modular.com/max/coding-assistants/)
