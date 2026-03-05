---
title: "Symphony: демон на Elixir раздаёт задачи Codex"
date: 2026-03-05
description: "Symphony от OpenAI — Elixir-демон, который читает задачи из Linear и запускает Codex автономно. Как устроен оркестратор и зачем нужен WORKFLOW.md."
tags: ["symphony", "codex", "agents", "orchestration", "elixir", "harness-engineering", "linear"]
image: "/images/blog/symphony-codex-orchestrator-preview.png"
---

Symphony — open-source демон на Elixir/OTP от OpenAI, который превращает управление кодинг-агентами в управление задачами. Поллит Linear, находит issue в статусе Todo, создаёт изолированный workspace через git clone, запускает Codex в режиме app-server и ведёт задачу по полному циклу — от первого коммита до мёржа — без участия человека. Не IDE-плагин и не чат-обёртка. Фоновый оркестратор, который работает пока ты спишь.

## Проблема: один человек — один агент — один таск

Я пользуюсь Claude Code каждый день. ~88 промптов в день, 40 скиллов в `~/.claude/skills/`, GitHub Issues как рабочая память агента. Работает отлично — для одного потока задач. Но масштабировать ручное управление агентом невозможно.

Проблема в трёх словах: **bottleneck — это ты**.

Когда у меня в Linear накапливается 8-10 задач, я всё равно беру их по одной. Попросил агента — подождал — проверил — попросил следующее. [Хуки Claude Code](/blog/claude-code-hooks-github-issues/) помогли сделать этот процесс реактивным: агент сам двигает статусы по событиям. Но хуки срабатывают только когда ты уже в сессии. Они не запустят агента на новую задачу сами.

Symphony решает эту проблему иначе: демон сам находит задачи, сам запускает агентов, сам ведёт их до завершения. Ты ставишь issue — демон подхватывает.

## Что такое Symphony

Четыре ключевых компонента:

```
┌─────────────┐     ┌──────────────────┐     ┌───────────────────┐     ┌─────────────┐
│  Linear API │ ──▶ │   Orchestrator   │ ──▶ │ Workspace Manager │ ──▶ │ Agent Runner│
│  (poll 5s)  │     │   (GenServer)    │     │  (git clone .)    │     │ (Codex CLI) │
└─────────────┘     └──────────────────┘     └───────────────────┘     └─────────────┘
       ▲                     │                                                │
       │                     ▼                                                ▼
       │            ┌──────────────────┐                              ┌─────────────┐
       │            │   WORKFLOW.md    │                              │ Linear API  │
       │            │  (config+prompt) │                              │ (status,    │
       │            └──────────────────┘                              │  comments)  │
       │                                                              └──────┬──────┘
       └─────────────────────────────────────────────────────────────────────┘
```

**Orchestrator** — фоновый процесс (GenServer) на виртуальной машине Erlang (BEAM/OTP). Владеет poll loop, решает кого запускать, кого остановить, кого перезапустить. Supervisor следит за процессами и перезапускает при крашах — без потери состояния остальных агентов.

**Workspace Manager** — создаёт изолированную директорию на каждый issue. `git clone --depth 1` в чистую папку. Каждый агент работает в своей копии репозитория — никаких конфликтов между параллельными задачами.

**Agent Runner** — запускает Codex CLI в режиме app-server: обмен JSON-сообщениями через стандартный ввод/вывод. Подставляет данные задачи в шаблон промпта из WORKFLOW.md, отправляет его Codex, обрабатывает tool calls, продолжает turns пока задача не завершена.

**WORKFLOW.md** — единственный конфиг. YAML front matter для настроек + Markdown тело как промпт. Prompt as code — версионируется вместе с репозиторием.

## Как работает цикл

```
Poll ──▶ Filter ──▶ Claim ──▶ Workspace ──▶ Prompt ──▶ Codex ──▶ Status
 │        (active     (max      (git clone   (Liquid    (app-     (Todo →
 │        states)     concur-    --depth 1)   render)    server)   In Progress →
 │                    rency)                                       Human Review →
 │                                                                 Merging →
 └──────────────────── retry/backoff ◀──── fail ◀──────────────── Done)
```

По умолчанию Orchestrator поллит Linear каждые 30 секунд (я выставил 5 в своём конфиге — `polling.interval_ms: 5000`). Находит issues в активных состояниях — `Todo`, `In Progress`, плюс кастомные `Merging` и `Rework`. Фильтрует уже запущенные, проверяет лимит concurrency (до 10 параллельных агентов), и для каждой новой задачи:

1. Создаёт workspace — изолированную директорию с `git clone`
2. Подставляет данные issue в Liquid-шаблон (библиотека Solid для Elixir): `{{ issue.identifier }}`, `{{ issue.title }}`, `{{ issue.description }}`
3. Запускает Codex app-server как subprocess через Erlang Port
4. Codex работает автономно: двигает статусы, пишет комментарии в Linear, создаёт PR, запускает тесты
5. Когда turn завершается, но issue ещё в активном состоянии — автоматически продолжает (до `max_turns: 20`)
6. При ошибке — exponential backoff с ретраями

Кастомные статусы Linear — ключевая часть воркфлоу. `Rework` означает: закрой PR, создай новую ветку, начни заново. `Human Review` — PR готов, ждём человека. `Merging` — человек одобрил, запускай land flow. Агент сам переключает задачу между этими состояниями.

## WORKFLOW.md: prompt as code

Фрагмент реального WORKFLOW.md из репозитория Symphony:

{{< callout insight >}}
You are working on a Linear ticket `{{ issue.identifier }}`

{% if attempt %}
Continuation context:
- This is retry attempt #{{ attempt }} because the ticket is still in an active state.
- Resume from the current workspace state instead of restarting from scratch.
{% endif %}

Issue context:
Identifier: {{ issue.identifier }}
Title: {{ issue.title }}
Current status: {{ issue.state }}
Labels: {{ issue.labels }}
URL: {{ issue.url }}
{{< /callout >}}

YAML front matter задаёт всю конфигурацию:

```yaml
tracker:
  kind: linear
  project_slug: "symphony-0c79b11b75ea"
  active_states: [Todo, In Progress, Merging, Rework]
polling:
  interval_ms: 5000
workspace:
  root: ~/code/symphony-workspaces
agent:
  max_concurrent_agents: 10
  max_turns: 20
codex:
  command: codex --model gpt-5.3-codex app-server
  approval_policy: never
  thread_sandbox: workspace-write
```

`approval_policy: never` — осознанный выбор полной автономии (дефолт Symphony строже — блокирует sandbox и MCP-запросы). Codex может запускать тесты и коммитить, но `thread_sandbox: workspace-write` ограничивает запись только рабочей директорией.

Промпт ниже YAML-блока — полный workflow контракт на 300+ строк: status map с маршрутизацией по состояниям, workpad template для Linear-комментариев, PR feedback sweep protocol, blocked-access escape hatch. Один конфиг определяет, как агент ведёт себя на любой задаче — [по тому же принципу, что и data layer для агентов](/blog/data-layer-for-agents/).

## Skills: инструменты агента

WORKFLOW.md ссылается на пять skills:

- **commit** — чистые, логичные коммиты
- **push** — пуш в remote
- **pull** — синхронизация с `origin/main`
- **land** — мёрж PR через специальный flow (не `gh pr merge` напрямую)
- **linear** — GraphQL-запросы к Linear через injected tool

Symphony инжектирует `linear_graphql` tool в app-server сессию как dynamic tool. Агент может делать произвольные GraphQL-запросы к Linear — всё через один tool.

## Как поставить

{{< callout insight >}}
git clone https://github.com/openai/symphony
cd symphony/elixir
mise trust && mise install
mise exec -- mix setup
mise exec -- mix build
mise exec -- ./bin/symphony ./WORKFLOW.md --port 4000
{{< /callout >}}

Перед запуском агенту понадобятся: Linear API key в переменной окружения `LINEAR_API_KEY`, WORKFLOW.md с вашим `project_slug`, кастомные статусы в Linear — Rework, Human Review, Merging (добавляются в Team Settings → Workflow).

`--port 4000` включает Phoenix LiveView дашборд — состояние оркестратора, retry pressure, token usage, статусы всех агентов. Обновляется в реальном времени.

## Мой опыт

Попросил агента склонировать репозиторий, настроить WORKFLOW.md под мой проект, запустить демон. Поставил `max_concurrent_agents: 3` (дефолт 10, но для начала хватит), `max_turns: 20`, sandbox `workspace-write`. Весь конфиг — 30 строк YAML.

Создал issue в Linear. Через 5 секунд Codex подхватил задачу — workspace создан, сессия стартовала, issue перешёл в In Progress. Работает.

Дашборд на Phoenix показывает какие агенты запущены, сколько tokens потрачено, retry queue, backoff таймеры. По-моему, это момент, когда перестаёшь чувствовать себя оператором агента и начинаешь чувствовать себя менеджером задач. Агенты — implementation detail.

## Harness Engineering: модель — commodity, инфраструктура — moat

OpenAI опубликовали вместе с Symphony статью про [harness engineering](https://openai.com/index/harness-engineering/). Цифры: 1 миллион строк кода, начали с 3 инженеров (потом выросли до 7), 5 месяцев, одна десятая времени по сравнению с ручной разработкой, ноль строк написано руками.

"Humans steer. Agents execute." — Ryan Lopopolo, OpenAI.

Aakash Gupta сформулировал ещё точнее: "The model is commodity. The harness is moat." Модель можно заменить. GPT-5.3-codex сегодня, что-то другое завтра. А вот инфраструктура вокруг модели — WORKFLOW.md, skills, status map, retry logic, workspace isolation — это то, что превращает Codex в агента, который сам доводит задачу до PR.

Это именно то, что я повторяю на "Кружке Вайбкодинга": не модель определяет полезность агента, а инфраструктура вокруг неё. Symphony — одна из первых open-source реализаций этого принципа на уровне оркестрации.

Спецификация Symphony language-agnostic — [`SPEC.md`](https://github.com/openai/symphony/blob/main/SPEC.md) описывает компоненты и контракты, а Elixir-реализация — одна из возможных. BEAM/OTP выбран не случайно: supervisor trees перезапускают упавших агентов без остановки остальных. А `WorkflowStore` поллит WORKFLOW.md каждую секунду и подхватывает изменения конфига без рестарта демона.

## Три уровня оркестрации

Я прошёл все три:

1. **Промпт в чат** — пишешь задачу руками, агент выполняет, ты проверяешь. Мои первые промпты в Claude Code.
2. **Issue как задача** — ставишь issue, [агент подхватывает через хуки](/blog/claude-code-hooks-github-issues/), но запуск всё ещё ручной. Мой этап с 40 скиллами и GitHub Issues.
3. **Оркестратор как менеджер** — ставишь issue, демон находит его, запускает агента, ведёт до мёржа. Полностью автономно. Symphony сейчас.

Разница между вторым и третьим — не в качестве ответов агента. В том, что я перестал быть event loop.

## Частые вопросы

### Можно ли использовать Symphony не с Codex?

Спецификация language-agnostic: она описывает интерфейсы, а не конкретную модель. Текущая Elixir-реализация заточена под Codex app-server, но `codex.command` в WORKFLOW.md — произвольная shell-команда. Теоретически можно подставить любой агент с совместимым протоколом.

### Насколько это безопасно для production?

Symphony — prototype software, как написано в README: "presented as-is, intended for evaluation only". OpenAI рекомендуют реализовать собственную hardened версию по SPEC.md. Для side-project — работает. Для production с чувствительным кодом — стоит добавить свои guardrails.

### Сколько агентов можно запускать параллельно?

По умолчанию `max_concurrent_agents: 10`. Реальный bottleneck — не оркестратор (BEAM держит тысячи процессов), а rate limits Codex API и стоимость токенов.
