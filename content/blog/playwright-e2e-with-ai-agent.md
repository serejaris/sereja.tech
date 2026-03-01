---
title: "E2E тесты пишет агент: Playwright + Claude Code"
date: 2026-01-23
description: "Как AI-агент генерирует Playwright тесты из описания сценариев. Три встроенных агента — planner, generator, healer — и реальный опыт."
tags: ["claude code", "playwright", "тестирование"]
knowledge:
  problem: "E2E тесты жрут время на написание и ломаются при каждом обновлении UI из-за изменения локаторов."
  solution: "Три встроенных агента Playwright — Planner, Generator, Healer — генерируют тесты из описания и автоматически чинят сломанные."
  pattern: "ai-generated-e2e-tests"
  tools: ["Playwright", "Claude Code", "Playwright MCP", "Chrome"]
  takeaways:
    - "70 тестов (47 + 23) за два вечера вместо пяти дней ручной работы"
    - "Три агента: Planner кликает UI и строит план, Generator пишет код, Healer чинит локаторы"
    - "Агенты плохо справляются со сложной бизнес-логикой и API-тестами"
    - "Playwright MCP даёт Claude Code прямой доступ к браузеру для проверки в реальном Chrome"
  metrics:
    tests_admin: 47
    tests_bot: 23
    time_saved_days: 3
---

Локатор поменялся — тест сломался. Фронтендер обновил форму — опять всё красное. Я переписывал один и тот же тест для регистрации раз шесть за квартал.

А потом Playwright добавил агентов.

## Проблема

Тесты жрут время. Писать скучно. Поддерживать — ад.

Каждый релиз превращается в археологические раскопки: где сломалось, почему `data-testid` больше не работает, куда делась кнопка. При этом без тестов я просто боюсь деплоить.

## Решение

В октябре 2025 (Playwright 1.56) появились три встроенных агента:

1. **Planner** — открывает приложение в браузере, кликает по интерфейсу, генерирует Markdown-план тестов
2. **Generator** — читает план и пишет код с локаторами через `getByRole`, `getByLabel`
3. **Healer** — запускает тесты, ловит падения, сам правит сломанные локаторы

Одна команда для Claude Code:

```bash
npx playwright init-agents --loop=claude
```

{{< callout type="insight" >}}
Исследуй приложение на localhost:3000 и напиши план тестов для авторизации: вход, выход, ошибка при неверном пароле.
{{< /callout >}}

Planner открыл браузер, потыкал формы, нашёл все поля. Минута — и готов Markdown с планом на 12 сценариев.

{{< callout type="insight" >}}
Сгенерируй тесты по этому плану.
{{< /callout >}}

Generator выдал три файла. Локаторы — accessibility-first, как любит Playwright.

## Сдвиг в голове

Раньше я тратил время на вопросы реализации. Какой локатор надёжнее? Нужен Page Object или нет? Мокать API или поднимать тестовую базу?

Теперь формулирую только: "Что должно работать?" Детали — на агенте.

Healer отдельно радует. Тест упал после обновления UI? Healer смотрит ошибку, находит элемент по новому селектору, правит файл. Я узнаю об этом из диффа в PR.

## Где не работает

По-моему, агенты плохо справляются с тремя вещами:
- Сложная бизнес-логика — её всё равно нужно объяснять словами, агент не угадает edge cases
- Генерация избыточных тестов — иногда создаёт 20 проверок там, где хватило бы 5
- API-тесты — для них я до сих пор пишу руками, агенты заточены под UI

Но для форм, навигации, CRUD — работает.

## Результат

Покрыл тестами админку онлайн-курса (47 тестов) и Telegram-бота для заявок (23 теста). Руками это заняло бы дней пять. С агентами — два вечера, и то большую часть времени ждал, пока Planner накликает интерфейс.

Playwright MCP даёт Claude Code прямой доступ к браузеру. Агент видит страницу, кликает, проверяет результат. Тесты проходят в реальном Chrome ещё до коммита — не в абстрактном окружении.

## Источники

- [Playwright Test Agents](https://playwright.dev/docs/test-agents) — официальная документация
- [The Complete Playwright End-to-End Story](https://developer.microsoft.com/blog/the-complete-playwright-end-to-end-story-tools-ai-and-real-world-workflows) — Microsoft DevBlog
- [Generating E2E Tests with Playwright MCP](https://www.browserstack.com/guide/playwright-ai-test-generator) — BrowserStack
- [Claude Code: Best practices for agentic coding](https://www.anthropic.com/engineering/claude-code-best-practices) — Anthropic
