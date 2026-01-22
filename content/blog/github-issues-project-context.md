---
title: "Контекст проекта в GitHub Issues: делегируй агенту"
date: 2026-01-21
description: "Как я делегировал Claude Code создание структурированного контекста проекта в GitHub Issues с mermaid-диаграммами"
tags: ["claude-code", "github", "вайбкодинг", "агенты"]
---

Вчера открыл репо для курса с Максом. Накидал контекст в заметки — аудитория, структура, цены, воронка. Через неделю буду искать это в пяти местах.

## Проблема

Нас двое. Контекст проекта — страница текста. Куда положить, чтобы версионировалось, читалось через API и не терялось в чатах?

docs/ в репо — нужен коммит для каждой правки. GitHub Wiki — отдельный клон, неудобно. Notion — нет нормального API для агентов. README — засоряется.

Решил не гадать.

## Что попросил

{{< callout type="insight" >}}
Проведи исследование лучших практик для хранения контекста проекта. Используй Exa. Нужно чтобы агент мог читать и обновлять через API.
{{< /callout >}}

Claude Code запустил три поиска параллельно: GitHub docs, knowledge management для стартапов, GitHub Projects для маленьких команд. Нашёл ADR — Architecture Decision Records, паттерн фиксации решений через Issues.

## Что вернул

| Подход | API | Версии | Обновление |
|--------|-----|--------|------------|
| docs/PROJECT.md | GitHub API | git history | коммит |
| **Pinned Issue** | **gh CLI** | **комментарии** | **мгновенно** |
| GitHub Wiki | ограничен | отдельный клон | средне |

По-моему, Pinned Issue — идеальный вариант для маленькой команды. `gh issue view` читает, `gh issue edit` обновляет. История в комментариях.

## Что сделал агент

Скинул ему контекст проекта текстом. За минуту:

- Создал label `context` (его не было)
- Создал issue со структурой: аудитория, курс, маркетинг, платежи, инфраструктура
- Закрепил его
- Добавил четыре mermaid-диаграммы в комментарий: воронка, техническая архитектура, стек участника, контент-пайплайн

Вручную это часа полтора. С диаграммами — все три.

## Как пользоваться

```bash
gh issue view 1 --repo user/project --json body
gh issue edit 1 --body "новый контекст"
gh issue list --label context
```

Минус один: надо приучить себя обновлять issue, а не кидать в чат. Но агенты теперь видят контекст без моего участия.

## Источники

- [GitHub Docs: Best practices for repositories](https://docs.github.com/en/repositories/creating-and-managing-repositories/best-practices-for-repositories)
- [Addy Osmani: My LLM coding workflow going into 2026](https://addyosmani.com/blog/ai-coding-workflow/)
- [Architecture Decision Records](https://github.com/adr)
