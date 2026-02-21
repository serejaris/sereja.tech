---
title: "Как научить Claude Code управлять твоим Chrome"
date: 2026-02-20
description: "Claude Code настройка Chrome DevTools MCP за 3 шага: агент управляет реальным Chrome с залогиненными сервисами."
tags: ["claude code", "mcp", "devtools"]
section: "Claude Code"
image: "/images/blog/chrome-devtools-mcp-setup-preview.png"
sources:
  - title: "Chrome DevTools MCP — GitHub"
    url: "https://github.com/anthropics/anthropic-tools/tree/main/chrome-devtools-mcp"
    note: "официальный репозиторий, 25 542 stars"
  - title: "Chrome DevTools MCP — анонс Google"
    url: "https://developer.chrome.com/blog/chrome-devtools-mcp"
    note: "блог Chrome DevTools"
  - title: "Remote Debugging Port — изменения в Chrome 136+"
    url: "https://developer.chrome.com/blog/remote-debugging-port"
    note: "ограничения безопасности"
  - title: "Chrome Debugging Profile for MCP"
    url: "https://raf.dev/blog/chrome-debugging-profile-mcp/"
    note: "гайд от Rafael Camargo"
  - title: "Claude in Chrome — баг #21371"
    url: "https://github.com/anthropics/claude-code/issues/21371"
    note: "52+ upvotes, без фикса"
---

Claude in Chrome сломан с января 2026, а Playwright MCP запускает чистый браузер без логинов. Chrome DevTools MCP от Google решает обе проблемы: три команды в терминале — и агент ходит по залогиненным сервисам в твоём реальном Chrome.

## Проблема: агент слепой в вебе

Claude Code живёт в терминале: пишет код, запускает тесты, правит файлы. Но открыть Google Search Console и проверить покрытие индекса — не может.

Мне нужно было проверить SEO-здоровье sereja.tech. Агент должен зайти в Search Console, найти проблемы, перейти в код, исправить, вернуться в Search Console — четыре перехода между средами. Руками это час копипасты между вкладками.

Посмотрел на варианты.

**Claude in Chrome** — расширение от Anthropic. Красивая идея: агент прямо в браузере. На практике — [сломано с января 2026](https://github.com/anthropics/claude-code/issues/21371). Конфликт native messaging host, 52+ upvotes на issue, фикса нет.

**Playwright MCP** — запускает чистый Chromium. Без логинов, без кук, без сессий. Про [браузерную автоматизацию с Playwright](/blog/playwright-e2e-with-ai-agent) писал отдельно — для E2E-тестов он отличный. Но для работы с Google Search Console, Vercel Dashboard или любым залогиненным сервисом — бесполезен.

Нужен доступ к реальному браузеру. Тому, где ты уже залогинен.

## Решение: Chrome DevTools MCP

[Chrome DevTools MCP](https://github.com/anthropics/anthropic-tools/tree/main/chrome-devtools-mcp) — MCP-сервер от Google. Проект с открытым кодом: 25 000+ stars на GitHub, Apache 2.0 лицензия, 60 contributors. Подключается к Chrome через DevTools Protocol (CDP). 26 инструментов: DOM, консоль, сеть, скриншоты, клики, навигация.

Ключевое — флаг `--browserUrl`. Он говорит MCP-серверу подключаться к уже запущенному Chrome вместо запуска нового.

Вот как это работает:

```
┌─────────────────────────────────────────────────────────┐
│                    Claude Code (терминал)                │
│                                                         │
│  Промпт → Агент решает: файл? терминал? браузер?        │
│                  │                                       │
│     ┌────────────┼────────────┐                          │
│     ▼            ▼            ▼                          │
│  Read/Edit    Bash      Chrome DevTools MCP              │
│  (файлы)    (команды)        │                           │
│                              │ CDP (port 9222)           │
│                              ▼                           │
│                    ┌──────────────────┐                  │
│                    │  Chrome (реальный)│                  │
│                    │  ├─ Search Console│                  │
│                    │  ├─ Vercel        │                  │
│                    │  └─ Любой сервис  │                  │
│                    └──────────────────┘                  │
└─────────────────────────────────────────────────────────┘
```

Агент сам решает когда идти в браузер, когда в файл, когда в терминал. Один промпт — все три среды.

## Настройка за 3 шага

### Шаг 1: алиас для Chrome с debug-портом

```bash
# Добавить в ~/.zshrc
alias chrome-debug='/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --user-data-dir="$HOME/.chrome-debug-profile" > /dev/null 2>&1 &'
```

Два флага, оба обязательны:

- `--remote-debugging-port=9222` — открывает CDP-порт для MCP
- `--user-data-dir` — отдельная директория профиля

{{< callout insight >}}
Chrome 136+ [заблокировал](https://developer.chrome.com/blog/remote-debugging-port) `--remote-debugging-port` с дефолтной data directory. Причина — рост атак через remote debugging для кражи cookies. Нельзя просто добавить флаг к обычному Chrome. Нужен отдельный `--user-data-dir`.
{{< /callout >}}

`~/.chrome-debug-profile` — это отдельный профиль. При первом запуске он пустой: нужно залогиниться в сервисы один раз. Дальше логины сохраняются между перезапусками.

Нельзя указывать `~/Library/Application Support/Google/Chrome` — это дефолтная директория, Chrome откажется запускаться с debug-портом. Это не баг, это защита. Google закрыл лазейку, которую использовали вредоносные программы.

### Шаг 2: добавить MCP-сервер

```bash
claude mcp add chrome-devtools \
  --scope user \
  -- npx -y chrome-devtools-mcp@latest \
  --browserUrl=http://127.0.0.1:9222
```

- `--browserUrl` — **критично**. Без этого флага MCP запустит свой чистый Chrome, и смысл теряется
- `--scope user` — сервер доступен во всех проектах

### Шаг 3: порядок запуска

```bash
# 1. Chrome с debug-портом
chrome-debug

# 2. Проверить что порт открыт
curl -s http://127.0.0.1:9222/json/version

# 3. Запустить Claude Code
claude
```

Порядок важен. Если запустить Claude Code до Chrome — MCP не найдёт браузер и молча упадёт.

Три команды. Готово.

## Кейс: SEO-аудит через агента

Настроил Chrome DevTools MCP и решил проверить на реальной задаче. Мне нужно было найти проблемы индексации на sereja.tech и починить их. Раньше это выглядело так: открыть Search Console, найти ошибку, переключиться в редактор, найти файл, исправить, вернуться в Search Console, проверить. Десять переключений контекста на каждую проблему.

Теперь — один промпт за другим. Четыре промпта, одна сессия, ноль копипасты.

### Шаг 1: найти проблемы

Попросил Claude Code на Opus 4.6:

{{< callout insight >}}
Открой Google Search Console для sereja.tech, найди страницы с ошибками индексации и перечисли их.
{{< /callout >}}

Агент открыл Search Console через Chrome DevTools MCP. Перешёл в раздел покрытия индекса. Нашёл страницы со статусом "Crawled — currently not indexed". Вернул список с URL и причинами. Я не переключался ни в одну вкладку — всё в терминале.

### Шаг 2: диагностика конкретной страницы

{{< callout insight >}}
Перейди на страницу /blog/chrome-devtools-mcp, проверь meta title и description в коде страницы. Сравни с тем что показывает Search Console.
{{< /callout >}}

Агент перешёл на страницу в Chrome, прочитал DOM — нашёл meta-теги. Потом вернулся в Search Console и сравнил с тем, что видит Google. Нашёл расхождение: description в HTML не совпадал с тем, что был в frontmatter Hugo-файла.

### Шаг 3: починить в коде

{{< callout insight >}}
В терминале открой файл content/blog/chrome-devtools-mcp.md, обнови description чтобы соответствовал требованиям.
{{< /callout >}}

Агент переключился из браузера в терминал. Открыл файл, обновил frontmatter. Без копипасты — он уже знал что нужно исправить из предыдущего шага.

### Шаг 4: запросить переиндексацию

{{< callout insight >}}
Вернись в Search Console, запроси переиндексацию страницы /blog/chrome-devtools-mcp.
{{< /callout >}}

Агент вернулся в Search Console, нашёл поле для проверки URL, вставил адрес, запросил переиндексацию. Весь цикл — от обнаружения проблемы до запроса переиндексации — без единого переключения вкладок.

Подробнее про весь SEO-аудит писал в [SEO-аудит блога за одну сессию Claude Code](/blog/seo-audit-hugo-vercel-checklist).

### Что произошло

Четыре промпта. Агент прошёл через три среды:

```
Промпт 1 → Search Console → список проблем
                                    │
Промпт 2 → Сайт (DOM) ←────────────┘
              │
              ▼ сравнил meta-теги
Промпт 3 → Терминал (Edit файла)
              │
              ▼ description обновлён
Промпт 4 → Search Console → переиндексация
```

Раньше это четыре вкладки, десять переключений и полчаса. Теперь — одно окно терминала и пять минут.

## Альтернативы: что ещё есть

| Инструмент | Твой браузер? | Логины? | Настройка | Статус |
|---|---|---|---|---|
| **Chrome DevTools MCP** (Google) | Да | Да (отдельный профиль) | 3 команды | Работает |
| **Playwright MCP** (Microsoft) | Нет (чистый) | Нет | 1 команда | Работает |
| **Playwright MCP + Extension** | Да | Да | 5+ шагов | Работает |
| **Browser MCP** (browsermcp.io) | Да | Да | 3 команды | Работает |
| **Claude in Chrome** (Anthropic) | Да | Да | Расширение | Сломан (Feb 2026) |

Chrome DevTools MCP выигрывает по простоте. Три команды — и работает. Playwright MCP с расширением тоже подключается к реальному Chrome, но настройка сложнее: нужно установить расширение, настроить профиль, прописать путь. Browser MCP — близкий конкурент, но менее популярен.

Про [основы Chrome DevTools MCP](/blog/chrome-devtools-mcp) — настройку без привязки к реальному браузеру — писал в отдельной статье.

## Подводные камни

**Chrome 136+ блокирует debug-порт с дефолтной директорией** — если не указать `--user-data-dir`, Chrome просто проигнорирует `--remote-debugging-port` без ошибок и предупреждений. Порт не откроется, MCP не подключится. Проверяй через `curl -s http://127.0.0.1:9222/json/version` — если пусто, дело в профиле.

**Без `--browserUrl` теряется весь смысл.** MCP запустит свой отдельный Chrome. Ты логинишься в одном браузере, агент работает в другом — пустом. Самая частая ошибка при настройке.

**Порядок запуска: сначала Chrome, потом Claude Code.** Иначе MCP не найдёт endpoint. Если забыл — перезапусти Claude Code после запуска Chrome.

**Первый запуск — пустой профиль.** `~/.chrome-debug-profile` — отдельная директория. В ней нет твоих логинов, кук, расширений. Первый раз нужно залогиниться вручную. Дальше всё сохраняется между сессиями.

**Не используй дефолтную директорию Chrome.** `~/Library/Application Support/Google/Chrome` — это директория твоего обычного Chrome. Если указать её в `--user-data-dir`, может возникнуть конфликт с запущенным браузером. Всегда создавай отдельную.

## FAQ

### Chrome DevTools MCP работает только с Claude Code?

Нет. Chrome DevTools MCP — стандартный MCP-сервер. Он работает с любым MCP-клиентом: Claude Code, Cursor, Windsurf, OpenCode. Настройка отличается синтаксисом конфига, но принцип тот же — указать `--browserUrl` на debug-порт Chrome.

### Нужно ли каждый раз залогиниваться?

Нет. Логины сохраняются в `~/.chrome-debug-profile` между перезапусками. Залогинился один раз — дальше куки живут как в обычном Chrome. Если почистишь директорию — придётся логиниться заново.

### Это безопасно? Debug-порт же открыт.

Debug-порт слушает только `127.0.0.1` — локальный интерфейс. Извне к нему не подключиться. Но любой процесс на твоей машине может. Поэтому Google и потребовал отдельный `--user-data-dir` начиная с Chrome 136 — чтобы вредоносные программы не могли подключиться к твоему основному профилю.

### А если я уже использую Playwright MCP?

Они не конфликтуют. Playwright MCP запускает отдельный Chromium, Chrome DevTools MCP подключается к твоему Chrome. Можно держать оба: Playwright для тестов, DevTools для работы с залогиненными сервисами.

---

## Источники

- [Chrome DevTools MCP — GitHub](https://github.com/anthropics/anthropic-tools/tree/main/chrome-devtools-mcp) — 25 542 stars, Apache 2.0
- [Chrome DevTools MCP — анонс Google](https://developer.chrome.com/blog/chrome-devtools-mcp)
- [Remote Debugging Port — Chrome 136+ изменения](https://developer.chrome.com/blog/remote-debugging-port) — почему нужен отдельный профиль
- [Chrome Debugging Profile for MCP — гайд](https://raf.dev/blog/chrome-debugging-profile-mcp/)
- [Claude in Chrome — баг #21371](https://github.com/anthropics/claude-code/issues/21371) — 52+ upvotes, без фикса
