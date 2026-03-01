---
title: "Chrome DevTools MCP: даём агенту глаза в браузер"
date: 2026-01-20
description: "Как подключить AI-агента к Chrome DevTools через MCP. Реальный кейс отладки формы авторизации в student-portal."
tags: ["claude code", "mcp", "devtools"]
section: "Claude Code"
knowledge:
  problem: "AI-агент пишет код, но не видит что сломал в браузере — отладка через копипасту ошибок"
  solution: "Chrome DevTools MCP даёт агенту прямой доступ к браузеру: скриншоты, DOM, консоль, сеть"
  pattern: "mcp-browser-debugging"
  tools: ["Chrome DevTools MCP", "Claude Code", "OpenCode", "Playwright MCP", "Midscene"]
  takeaways:
    - "6 команд покрывают 80% frontend-багов: screenshot, snapshot, fill, click, console, network"
    - "Баг с Input-компонентом в student-portal найден и починен одним промптом"
    - "evaluate позволяет выполнить JS в контексте страницы"
    - "DevTools MCP для отладки, Playwright MCP для E2E-тестов — не конфликтуют"
  related:
    - slug: "chrome-devtools-mcp-setup"
      relation: "продвинутая настройка с подключением к реальному Chrome"
---

Агент пишет код. Но не видит что сломал.

Я описываю баг словами, агент гадает. Делаю скриншот, кидаю в чат, жду пока распарсит. Console.log, F12, копипаста ошибок — цикл на 20 минут ради одного бага.

Chrome DevTools MCP даёт агенту прямой доступ к браузеру. Он сам смотрит, сам кликает, сам читает консоль.

## Установка

```bash
npx chrome-devtools-mcp@latest
```

OpenCode (`~/.config/opencode/opencode.json`):

```json
{
  "mcp": {
    "chrome-devtools": {
      "type": "local",
      "command": ["npx", "-y", "chrome-devtools-mcp@latest"],
      "enabled": true
    }
  }
}
```

Claude Code (`~/.claude/settings.json`):

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["chrome-devtools-mcp@latest"]
    }
  }
}
```

## Кейс: student-portal

Баг: ввод пароля не работает. Пользователь печатает — поле пустое. Три студента написали в саппорт за час.

Написал агенту: "Проведи E2E через devtools mcp".

Он запустил Chrome. Нашёл форму. Попробовал ввести текст — увидел что `value` не обновляется. Полез в React state, нашёл что `onChange` не триггерится.

Диагноз: кастомный Input-компонент не прокидывал пропс. Исправил одну строку.

Раньше я бы сам открывал DevTools, ставил брейкпоинты, гуглил "react input value not updating". А тут — промпт и ответ.

## Инструменты

**screenshot** — скриншот. Когда нужно увидеть что рендерится.

**snapshot** — DOM без стилей. Агент ищет элементы, анализирует структуру. Быстрее чем парсить скриншот.

**fill, click** — взаимодействие. Заполнить форму, нажать кнопку, пройти flow.

**console** — ошибки, warnings, логи. То что я раньше копировал руками.

**network** — запросы к API. Статусы, payload, тайминги.

**evaluate** — выполнить JS в контексте страницы. Посмотреть window, проверить глобальные переменные.

## Когда полезно

Стили поехали — агент делает скриншот и видит проблему. Форма не сабмитится — тестирует flow сам. Hydration mismatch — смотрит консоль и сравнивает DOM. API молчит — проверяет network.

По-моему, 80% frontend-багов можно диагностировать через эти шесть команд.

## Альтернативы

**@playwright/mcp** от Microsoft — полноценная автоматизация. Тяжелее, зато тесты можно генерить.

**Midscene** — vision-based. Не парсит DOM, смотрит на скриншоты. Работает с любым UI, даже нативным.

Я использую DevTools MCP для быстрой отладки. Playwright — когда нужны E2E тесты.

---

## Источники

- [chrome-devtools-mcp — npm](https://www.npmjs.com/package/chrome-devtools-mcp)
- [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/)
- [@playwright/mcp — npm](https://www.npmjs.com/package/@playwright/mcp)
- [Midscene.js](https://midscenejs.com/)
