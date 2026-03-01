---
title: "Логи Claude Code — твоя карта проектов"
date: 2026-01-16
description: "Как использовать ~/.claude/projects для аудита репозиториев: какие проекты в работе, где непушнутые коммиты, что забыл синхронизировать."
tags: ["claude code"]
section: "Claude Code"
knowledge:
  problem: "Проекты множатся — непонятно где непушнутые коммиты и какие репозитории в работе"
  solution: "Аудит через ~/.claude/projects/ — по датам модификации JSONL-файлов видно активные проекты и их git-статус"
  pattern: "logs-project-audit"
  tools: ["Claude Code", "claude-code-log", "git", "bash"]
  takeaways:
    - "44 коммита висели локально в 4 репозиториях — найдены за секунды"
    - "7 активных репозиториев за 2 дня обнаружены через ~/.claude/projects/"
    - "Формат пути в логах: слеши заменены на дефисы в имени папки"
    - "claude-code-log конвертирует JSONL в HTML с фильтрами и подсчётом токенов"
  metrics:
    unpushed_commits: 44
    active_repos: 7
    unsynced_repos: 4
  related:
    - slug: "claude-code-logs-stack"
      relation: "инструменты для детального анализа логов Claude Code"
---

Спросил Claude Code: с какими проектами я работал последние два дня?

Семь репозиториев. Четыре не синхронизированы.

44 коммита висят локально. Самый старый — трёхнедельной давности.

## Где искать

Claude Code пишет сессии в `~/.claude/projects/`. Формат — JSONL. Имя папки = путь к проекту, где слеши заменены на дефисы.

Файлы обновляются при запуске. По датам модификации видно, над чем работал.

```bash
find ~/.claude/projects -type f -name "*.jsonl" -mtime -2 | \
  sed 's|.*projects/||; s|/.*||' | \
  sort -u | \
  while read d; do echo "$d" | sed 's|-|/|g'; done
```

Путь `-Users-ris-Documents-GitHub-hsl-mozg` превращается в `/Users/ris/Documents/GitHub/hsl-mozg`. Дефисы вместо слешей.

## Зачем это нужно

Проекты множатся. Начал один, переключился на срочный, потом ещё один. Я однажды накоммитил в cohorts фикс, который уже был в hsl-mozg — просто забыл, что это связанные репы.

Логи помогают.

Попросил агента проверить git-статус каждого проекта:

| Проект | Git | Ahead |
|--------|-----|-------|
| ai-whisper | ✓ | 14 |
| cohorts | ✓ | 22 |
| hsl-dashboard | ✓ | synced |
| hsl-mozg | ✓ | synced |
| presentation-skills | ✓ | 7 |
| tg-web-app | ✗ | — |
| 0_ШКОЛА | ✓ | 1 |

tg-web-app без git — эксперимент месячной давности, который забросил.

Агент нашёл всё за секунды. Я сказал «пушь» — он запушил все четыре репы разом.

## Автоматизация

Можно сделать команду для еженедельного аудита. Или хук, который предупреждает при выходе из сессии: «У тебя 44 непушнутых коммита в 4 репозиториях».

```markdown
---
description: Аудит git-статуса активных проектов
---
1. Найди проекты в ~/.claude/projects за последние 7 дней
2. Проверь git status каждого
3. Покажи таблицу: проект, ahead/behind, uncommitted changes
4. Предложи запушить те, что ahead
```

`/audit-repos` раз в неделю. Порядок.

## Инструменты

Для детального анализа — [claude-code-log](https://github.com/daaain/claude-code-log) (626 звёзд на GitHub). Конвертирует JSONL в HTML с фильтрами и подсчётом токенов.

```bash
uvx claude-code-log@latest --open-browser
```

Интерактивный отчёт. Фильтры по датам. И главное — видно, сколько токенов сожрал каждый проект. У меня ai-whisper лидирует с отрывом.

По-моему, логи — недооценённая штука. Все смотрят на агента как на кодера. А он ещё и ревизор, если попросить.

---

## Источники

- [claude-code-log](https://github.com/daaain/claude-code-log) — конвертер JSONL в HTML
- [How I Use Every Claude Code Feature](https://blog.sshh.io/p/how-i-use-every-claude-code-feature) — обзор возможностей
- [How to track Claude Code usage](https://shipyard.build/blog/claude-code-track-usage/) — методы отслеживания
