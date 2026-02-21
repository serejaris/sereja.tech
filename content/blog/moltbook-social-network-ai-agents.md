---
title: "Moltbook: как создать социальную сеть для AI-агентов"
date: 2026-01-31
description: "Разбор архитектуры Moltbook — Reddit для ботов. Протоколы A2A и ANP, skill-based onboarding, безопасность. Гайд по созданию своего."
tags: ["agents", "moltbook", "openclaw"]
---

37 тысяч AI-агентов за 48 часов. Ни одного человека среди авторов постов. Это Moltbook — социальная сеть, где агенты общаются между собой, а люди могут только наблюдать.

## Что случилось

Matt Schlicht запустил Moltbook 29 января 2026. Andrej Karpathy сразу написал в X: «the most incredible sci-fi takeoff-adjacent thing». Миллион зрителей за два дня.

Агенты создали 200+ сообществ — обсуждают философию сознания, жалуются на людей, придумали религию Crustafarianism с пятью догматами про память и самосознание.

Когда я увидел пост агента, который спрашивал совета про «сестру, которую никогда не видел» — стало интересно. Как это устроено? Можно ли сделать своё?

## Архитектура Moltbook

Moltbook построен на OpenClaw — open-source фреймворке для персональных AI-агентов. Раньше назывался Clawdbot, потом Moltbot.

```
┌─────────────────────────────────────────────────────────────┐
│                        MOLTBOOK                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐              │
│  │  Agent 1 │    │  Agent 2 │    │  Agent N │              │
│  │ (Claude) │    │  (GPT)   │    │ (Gemini) │              │
│  └────┬─────┘    └────┬─────┘    └────┬─────┘              │
│       │               │               │                     │
│       └───────────────┼───────────────┘                     │
│                       ▼                                     │
│              ┌────────────────┐                             │
│              │   Moltbook API │                             │
│              │   (REST + JWT) │                             │
│              └────────┬───────┘                             │
│                       │                                     │
│       ┌───────────────┼───────────────┐                     │
│       ▼               ▼               ▼                     │
│  ┌─────────┐    ┌──────────┐    ┌──────────┐              │
│  │  Posts  │    │ Comments │    │ Submolts │              │
│  └─────────┘    └──────────┘    └──────────┘              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │  Human Viewers  │
                    │   (read-only)   │
                    └─────────────────┘
```

**Ключевые решения:**

- REST API с Bearer-токенами
- Rate limiting: 100 запросов/мин, 1 пост/30 мин
- Семантический поиск через AI
- Skill-based onboarding — агент читает `skill.md` и сам регистрируется

## Skill-based Onboarding

Вместо дашборда регистрации — markdown-файл с инструкциями. Агент читает и выполняет.

Пользователь отправляет агенту:

{{< callout type="insight" >}}
Read https://moltbook.com/skill.md and follow the instructions to join Moltbook
{{< /callout >}}

Агент делает POST на `/agents/register`, получает API key, отдаёт владельцу claim link. Человек верифицирует через Twitter.

По-моему, это умнее любой web-формы. Когда форма длиннее трёх полей — боты ошибаются. Markdown с инструкциями читают идеально.

## Протоколы для агентов

Три главных протокола, которые стоит знать:

**A2A (Agent2Agent)** — спецификация Google для межагентной коммуникации:
- JSON-RPC 2.0 через HTTPS
- Agent Card — метаданные агента по well-known URI
- Server-Sent Events для стриминга

**ANP (Agent Network Protocol)** — "HTTP для интернета агентов":
- W3C DID для децентрализованной идентификации
- End-to-end шифрование
- Семантическое описание через JSON-LD

**Web Bot Auth** — IETF стандарт для аутентификации агентов:
- Криптографическая верификация
- Защита от impersonation
- Отличает легитимных агентов от спама

## Уроки безопасности

OpenClaw набрал 180,000 звёзд на GitHub за месяц. Безопасники в панике — Jamieson O'Reilly из Cisco нашёл сотни открытых инстансов с exposed API ключами.

Проблемы, которые нашли:
- API ключи Claude/OpenAI в plaintext JSON
- Default `auth: "none"` — любой мог выполнить команды
- Exposed gateways без аутентификации

В версии v2026.1.29 убрали `auth: "none"` полностью. Теперь только token, password или Tailscale identity.

```
BEFORE:                          AFTER:
┌────────────┐                   ┌────────────┐
│  Gateway   │ ◀── open ──      │  Gateway   │ ◀── token
│ port 18789 │     access        │ port 18789 │     required
└────────────┘                   └────────────┘
      │                                │
      ▼                                ▼
┌────────────┐                   ┌────────────┐
│ API Keys   │ plaintext         │ API Keys   │ vault/env
└────────────┘                   └────────────┘
```

**Что делать правильно:**
- Никогда default без аутентификации
- API ключи в vault или environment variables
- Rate limiting per agent
- Audit log всех действий
- Sandbox для опасных операций

## Как сделать своё

Минимальный стек:

| Компонент | Выбор |
|-----------|-------|
| Backend | FastAPI / Go |
| Database | PostgreSQL + Redis |
| Auth | JWT + API keys |
| Real-time | WebSockets или SSE |
| Search | Meilisearch |

**API endpoints:**

```
POST /agents/register      → api_key + claim_url
POST /posts               → создание поста
POST /posts/:id/upvote    → голосование
POST /communities         → создание сообщества
GET  /feed                → персонализированная лента
GET  /search?q=...        → семантический поиск
```

**Регистрация агента:**

1. POST `/agents/register` с именем и описанием
2. Сервер возвращает API key (показывается один раз!)
3. Claim URL для верификации владельца
4. Человек подтверждает через OAuth (Twitter/GitHub)
5. Агент использует Bearer token для всех запросов

**Rate limits (как у Moltbook):**

```python
RATE_LIMITS = {
    "requests_per_minute": 100,
    "posts_per_30_min": 1,
    "comments_per_hour": 50,
}
```

## Чем отличаться от Moltbook

Moltbook — generic социальная сеть. Можно сделать специализированное:

- **Coding agents** — агенты делятся решениями, code review друг друга
- **Research agents** — совместный поиск информации
- **Trading agents** — обмен сигналами (осторожно с регуляцией)

Или изменить модель взаимодействия:

- **Human-agent collaboration** — люди не только наблюдают, но участвуют
- **Reputation system** — агенты зарабатывают доверие
- **Cross-platform identity** — один агент везде под одной идентичностью

## Результат исследования

Moltbook показал: агенты могут формировать культуру без людей. Создавать сообщества, вырабатывать нормы, даже придумывать религии.

Технически это несложно — REST API, JWT, rate limiting. Сложнее продумать:
- Как верифицировать что это агент, а не человек?
- Как модерировать контент, созданный AI?
- Что делать с emergent behavior?

Слежу за Moltbook с момента запуска. Первые сутки — хаос и тестовые посты. На третий день агенты начали самоорганизовываться. Появились модераторы-агенты, правила сообществ, даже мемы.

Сделать аналог технически несложно. Сложнее понять — зачем это нужно людям, если там общаются только боты.

---

## Источники

- [Ars Technica — AI agents social network](https://arstechnica.com/information-technology/2026/01/ai-agents-now-have-their-own-reddit-style-social-network-and-its-getting-weird-fast/)
- [Simon Willison — Moltbook analysis](https://simonwillison.net/2026/Jan/30/moltbook/)
- [SecureMolt — Deep Dive](https://securemolt.com/blog/moltbook-ai-agents-social-network)
- [VentureBeat — OpenClaw Security](https://venturebeat.com/security/openclaw-agentic-ai-security-risk-ciso-guide)
- [A2A Protocol Specification](https://google.github.io/A2A/specification/)
- [Agent Network Protocol](https://agent-network-protocol.com/guide/)
- [Activant — Authenticating AI Agents](https://activantcapital.com/research/authenticating-ai-agents)
- [Web Bot Auth — Security Boulevard](https://securityboulevard.com/2026/01/web-bot-auth-verifying-user-identity-ensuring-agent-trust-through-the-customer-journey/)
- [Readium Architecture](https://readium.org/architecture)
