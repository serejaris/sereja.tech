---
title: "Symphony: демон на Elixir раздаёт задачи Codex"
date: 2026-03-05
description: "Symphony от OpenAI — Elixir-демон, который читает задачи из Linear и запускает Codex автономно. Как устроен оркестратор и зачем нужен WORKFLOW.md."
tags: ["symphony", "codex", "agents", "orchestration", "elixir", "harness-engineering", "linear"]
image: "/images/blog/symphony-codex-orchestrator-preview.png"
---

Symphony — open-source демон на Elixir/OTP от OpenAI, который превращает управление кодинг-агентами в управление задачами. Поллит Linear, находит issue в статусе Todo, создаёт изолированный workspace через git clone, запускает Codex в режиме app-server и ведёт задачу по полному циклу — от первого коммита до мёржа — без участия человека. Не IDE-плагин и не чат-обёртка. Фоновый оркестратор, который работает пока ты спишь.

## Под капотом: кто на самом деле писал Symphony

Мне стало интересно, кто стоит за проектом. Попросил агента покопаться в git history — и провалился в кроличью нору.

Автор практически один — [Alex Kotliarskyi](https://github.com/frantic). Из 30 коммитов 29 его, один от коллеги tiago-oai. Alex — не случайный человек. За плечами Facebook (React Native), Replit, собственный стартап [Secta AI](https://secta.ai). Больше 15 лет в индустрии. Сейчас инженер в OpenAI.

Но самое интересное — первый коммит.

26 февраля 2026, 13:58 по Тихоокеанскому времени. Один коммит. Сообщение — эмодзи ноты: `:musical_score:`. Внутри — 17 743 строки кода в 72 файлах. Весь проект целиком.

Расклад: ~8 900 строк в `lib/` (ядро приложения), ~7 900 строк тестов, 2 110 строк `SPEC.md` (спецификация, по сути RFC), 326 строк `WORKFLOW.md`, CI, Makefile, навыки для Codex. Всё за один присест.

В тот же день — PR #1 и PR #2 от Codex-агентов. На следующий день, 27 февраля — 19 коммитов за сутки. В сообщениях мелькают тикеты `MT-703`, `MT-718` — это Linear-тикеты. Symphony писал сам себя через себя. Оркестратор задач раздавал задачи по собственной разработке.

OpenAI в блоге [Harness Engineering](https://openai.com/index/harness-engineering/) описывает внутренний проект на миллион строк, написанный с нулём ручного кода. Symphony — публичная демонстрация того же подхода.

А теперь парадокс: код при этом качественный. Идиоматичный Elixir. OTP-паттерны. `@spec` на функциях. Dialyzer. Почти 8 000 строк тестов в первом же коммите. Не черновик — рабочий проект с покрытием. По-моему, это один из первых публичных проектов, где Codex-агенты выдали код, неотличимый от senior Elixir-разработчика.

`SPEC.md` — отдельная история. 2 110 строк детальной спецификации: архитектура, состояния, переходы, edge-кейсы. Написано человеком. Читается как настоящий RFC.

При этом — файл `NOTICE` содержит ошибки форматирования. В стандартном тексте Apache 2.0 должно быть строчное "distributed under the License". В Symphony — "Distributed" с заглавной. Мелочь, но характерный AI-артефакт. Модель скопировала текст лицензии и "улучшила" заглавные буквы.

README прямо предупреждает: "prototype software intended for evaluation only". Не продукт. Демонстрация подхода.

{{< callout insight >}}
Harness engineering — это не вайбкодинг. Разница — в спеке. Alex написал 2 110 строк спецификации до того, как агенты написали первую строку кода. Спека — человеческая. Код — машинный. Качество — высокое. Один опытный инженер + AI-агенты = 17 000 строк идиоматичного Elixir за несколько дней. Без спеки этого бы не случилось.
{{< /callout >}}

Подробнее про разницу между уровнями оркестрации — в посте про [личную корпорацию](/blog/personal-corporation-event-driven-agents/), где агенты работают как сотрудники по чётким инструкциям.

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

## Мой провал: как я потерял отчёт

После настройки решил дать Symphony настоящую задачу. Не игрушечную — реальный аудит кодовой базы.

Взял `WORKFLOW.md` из README-примера. Подставил свои значения:

{{< callout insight >}}
Мой WORKFLOW.md — почти дословно из README:

```yaml
tracker:
  kind: linear
  project_slug: "my-project-slug"
workspace:
  root: ~/code/symphony-workspaces
hooks:
  after_create: |
    git clone --depth 1 https://github.com/my-org/my-repo.git .
agent:
  max_concurrent_agents: 3
  max_turns: 20
codex:
  command: codex app-server
  approval_policy: never
  thread_sandbox: workspace-write
```

А промпт — три строки:

```
You are working on a Linear ticket {{ issue.identifier }}
Title: {{ issue.title }}
Body: {{ issue.description }}
```
{{< /callout >}}

Создал в Linear issue: "Code analysis: find problems and improvement areas". Запустил Symphony.

Пять секунд — Codex подхватил задачу. Workspace создан. Issue → In Progress. Красота.

Через пятнадцать минут — Done. В Linear-комментарии подробный саммари на полстраницы. Codex нашёл реальные проблемы:

- **Critical:** пропущенная таблица в миграциях
- **High:** API без аутентификации, CORS открыт на `*`
- **Medium:** четыре красных теста
- **Medium:** unescaped user data в HTML-шаблонах

В конце комментария: "Детальный отчёт сохранён в `docs/reports/code-analysis.md`".

Иду смотреть файл. Его нет. Workspace удалён.

Symphony чистит workspace после того, как issue переходит в терминальное состояние. Отчёт существовал только внутри workspace. Агент его не запушил. Никуда.

```
Что я ожидал:              Что произошло:

Issue ──▶ Codex ──▶ Push   Issue ──▶ Codex ──▶ Comment
           │        ──▶ PR            │          (summary)
           ▼                          ▼
        Report                     Report
       (в репо)                 (в workspace)
                                      │
                                 Workspace
                                  deleted
                                      │
                                     💀
```

Ну и кто тут вайбкодер — я или Symphony?

Причина оказалась простой. Минимальный пример из README — ~20 строк YAML и 3 строки промпта. Рабочий `WORKFLOW.md` из самого Symphony — 326 строк. Между ними — пропасть.

Рабочий WORKFLOW содержит полный цикл: commit → push → PR → Human Review → Merging → land flow. Там прописаны навыки `commit`, `push`, `pull`, `land`. Есть "PR feedback sweep protocol" и 287 строк инструкций о том, *как именно* довести задачу до мержа.

В минимальном примере ничего этого нет. Нет инструкции пушить. Нет инструкции создавать PR. Нет инструкции сохранять артефакты за пределами workspace. Агент сделал ровно то, что его попросили: поработал и отчитался в комментарий. А пушить никто не просил.

{{< callout insight >}}
Prompt body в WORKFLOW.md — это не конфиг. Это ТЗ для агента. Что написал — то и получишь. Буквально. Если в ТЗ нет слова "push" — агент не будет пушить. Если нет слова "PR" — не будет создавать PR.
{{< /callout >}}

Ирония: я учу вайбкодеров писать хорошие промпты. Провёл девять потоков кружка. А сам дал агенту "сделай задачу" без "и сохрани результат".

Урок здесь не про Symphony. Symphony сработал идеально — точно по инструкции. Урок про разрыв между документацией и реальностью в AI-generated кодовых базах. Код генерится отлично — 8 000 строк тестов в первом коммите. А документация для внешних пользователей? "Minimal example" — и разбирайся сам.

Это не баг проекта. Это слабое место подхода. Когда весь код пишут агенты, некому сесть и подумать: а что увидит новый пользователь? Какие грабли его ждут? Спека есть — для агентов. README есть — для быстрого старта. Мостик между ними — нет.

Теперь в моём WORKFLOW.md есть явная инструкция: "Commit and push all artifacts before marking the issue as Done." Двенадцать слов. Пятнадцать минут потерянного отчёта.

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

