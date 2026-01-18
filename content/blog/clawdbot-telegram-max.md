---
title: "Clawdbot: Claude Code с телефона через Telegram"
date: 2026-01-18
description: "Self-hosted бот для управления Claude Code через Telegram. Делегируем настройку агенту — он сам разберётся с OAuth, Keychain и синхронизацией."
tags:
  - Clawdbot
  - Telegram
  - Claude Code
section: "AI Tools"
---

Claude Code живёт в терминале. Терминал — на компе дома. А ты в кофейне, в метро, на созвоне.

## Проблема

Хочется: написать в Telegram «создай landing page для проекта X» — и получить готовый код в репозитории.

Clawdbot — self-hosted бот, который превращает Telegram в интерфейс к AI. Запускается на компьютере, читает сообщения из Telegram, выполняет команды локально. Через скилл `coding-agent` управляет Claude Code в фоне.

## Как это работает

```
[Телефон] → Telegram API → [Clawdbot на компе] → [Claude Code / терминал / файлы]
```

**Workspace как системный промпт.** Clawdbot читает markdown-файлы из `~/clawd/` и инъецирует в system prompt. Вот реальный пример `SOUL.md`:

```markdown
# SOUL.md - Persona & Boundaries

- Keep replies concise and direct.
- Ask clarifying questions when needed.
- Never send streaming/partial replies to external messaging surfaces.
```

Другие файлы: `AGENTS.md` (правила поведения), `IDENTITY.md` (имя и emoji), `USER.md` (профиль владельца). Скиллы загружаются лениво — агент читает нужный только когда задача соответствует описанию.

**Скиллы из коробки:** GitHub, Apple Notes, Notion, Whisper, tmux, coding-agent.

## Делегируем настройку агенту

Проблема: залогинился в Clawdbot — разлогинило из Claude Code. Подписка одна, клиенты конфликтуют.

Что я сделал — написал в Claude Code:

{{< callout insight >}}
«Clawdbot разлогинивает меня из Claude Code. Нужно чтобы оба работали на одной Max подписке. Сделай сам.»
{{< /callout >}}

Что агент сделал:

1. Нашёл OAuth-токен в macOS Keychain:

```bash
security find-generic-password -s "Claude Code-credentials" -w
```

2. Добавил профиль в `~/.clawdbot/agents/main/agent/auth-profiles.json`:

```json
{
  "version": 1,
  "profiles": {
    "anthropic:claude-cli": {
      "type": "oauth",
      "provider": "anthropic",
      "access": "sk-ant-oat01-...",
      "refresh": "sk-ant-ort01-...",
      "expires": 1768759670699,
      "scopes": ["user:inference", "user:profile", "user:sessions:claude_code"],
      "subscriptionType": "max",
      "rateLimitTier": "default_claude_max_5x"
    }
  }
}
```

3. Проверил статус:

```bash
clawdbot models status
# anthropic:claude-cli=OAuth, subscriptionType=max
```

Ни одного запроса в Google. Агент нашёл токен, понял формат, записал куда нужно.

## Риски и ограничения

{{< callout warning "Серая зона" >}}
Max через сторонние клиенты не поддерживается официально. 9 января 2026 Anthropic заблокировал OAuth в сторонних приложениях. Clawdbot обходит через tool-name bypass.
{{< /callout >}}

**Лимиты делятся.** Max 5x — ~45 сообщений Opus в час суммарно на все клиенты.

**Официальная альтернатива:** API с оплатой по токенам. Дороже в 10+ раз, но без рисков.

**Что может сломаться:** обновление Anthropic API, refresh токена, версия Clawdbot.

## Результат

| Инструмент | Где | Подписка |
|------------|-----|----------|
| Claude Code | Терминал | Max |
| Clawdbot | Telegram | та же Max |

Один аккаунт. Два клиента. Лимиты общие. Эта статья тоже написана через Claude Code.

---

## Источники

- [Clawdbot Getting Started](https://docs.clawd.bot/getting-started) — установка и настройка
- [Clawdbot OAuth Documentation](https://docs.clawd.bot/concepts/oauth) — bidirectional sync
