# Evidence pack: реальный стек Серёжи Риса

Дата среза: **2026-07-09**. Цель: дать фактическую основу для публичной страницы `tech.sereja.tech`, отделив рабочий контур от тестов и просто оплаченного доступа.

## Короткий вердикт

Сейчас стек Серёжи — это не один AI-редактор. Это ролевая система:

1. **Codex App / Codex CLI** — основной исполнитель: длинные задачи, код, ревью, работа с GitHub и несколькими репозиториями.
2. **Claude Code** — проектирование и разрешение сложных развилок; в июле на этой роли используется Fable/Opus.
3. **GPT-5.5 / Codex** — советник и исполнитель; **GLM 5.2** и Sonnet — более дешёвые руки.
4. **OMP + Orca** — слой оркестрации агентов разных провайдеров и изолированных worktree/терминалов.
5. **GitHub Issues + Markdown + `AGENTS.md` / `CLAUDE.md`** — очередь, спецификации и долговременный контекст.
6. **Chrome/Playwright/Telethon + CLI** — проверка результата и работа с реальными веб- и Telegram-поверхностями.
7. **Vercel, Railway, OVH/Proxmox** — доставка сайтов, ботов, баз и контейнеров.

На 9 июля в локальном Codex-конфиге уже выставлен `gpt-5.6-sol`, однако это изменение того же дня. В публичном тексте его следует показывать как **текущий тест**, пока нет недельного evidence использования и итогового вердикта.

## Как установлен автор сообщений

Источник: `/Users/ris/Documents/GitHub/tg-telethon/data/telegram.db`, чат `@vibecod3rs`:

- `chats.id = -1001187714594`, `title = вайбкодеры`, `username = vibecod3rs`;
- автор `sender_id = 95450323`, `sender_name = Сережа Рис`, handle `@serejaris`;
- в архиве 4 040 сообщений этого sender именно в `@vibecod3rs` с 2025-09-16 по 2026-07-08;
- тот же user id подтверждён как владелец в E2E Hermes/Telegram: `/Users/ris/Documents/GitHub/corp-dot-hermes/docs/status.md:37`.

Связка `95450323 → @serejaris` также зафиксирована в `/Users/ris/Documents/GitHub/tg-telethon/config/accounts/profiles.json` и `/Users/ris/Documents/GitHub/tg-telethon/config/accounts/README.md`; `/Users/ris/Documents/GitHub/corp-community/description.md` называет `@serejaris` админом комьюнити. Канал `@ris_ai` имеет отдельный sender id `-1001497220445`; его автофорварды не считались личными сообщениями Серёжи.

Проверочная SQL-логика:

```sql
SELECT sender_id, sender_name, COUNT(*), MIN(date), MAX(date)
FROM messages
WHERE chat_id = -1001187714594
GROUP BY sender_id, sender_name
ORDER BY COUNT(*) DESC;
```

Это исключает смешение слов Серёжи с сообщениями других участников и с ботом Нейрочел.

## 1. Ежедневное ядро

| Компонент | Что доказано | Первичные источники |
|---|---|---|
| **Codex App / CLI** | 2 июня Серёжа пишет, что практически перестал использовать CLI и проводит 90% времени в Codex App. На 9 июля `codex-cli 0.142.5` установлен; локально есть Codex-сессии каждый день 24.06–09.07, включая 14 файлов сессий за 09.07. | [Сообщение 75545, 2026-06-02](https://t.me/vibecod3rs/75545); [эфир о GPT-5.4 + Codex, 2026-03-06](https://youtube.com/watch?v=OtA-P95JnY8); `/Users/ris/.codex/sessions/`; `/Users/ris/.local/bin/codex`. |
| **Claude Code** | Остаётся вторым ядром: проектирование, планирование, дорогие развилки. 30 июня Серёжа формулирует свой процесс как «Opus пишет планы, Sonnet исполняет и проверяет». Текущий `~/.claude/settings.json` использует `claude-fable-5[1m]`, Codex-плагин и Orca hooks. | [Эфир Sonnet 5, 2026-06-30](https://youtube.com/watch?v=L_W3FTVEa2c); [сообщение 82517, 2026-06-27](https://t.me/vibecod3rs/82517); `/Users/ris/.claude/settings.json:31,50,150-160` (mtime 2026-07-09). |
| **Ролевая схема моделей** | Самая свежая явная формула: «Fable (архитектор) + GPT 5.5 (Советник) + GLM (воркер)». На опубликованном эфире 4 июля Fable пишет спеки и раздаёт задачи, руками работают Sonnet, Codex и GLM. Это точнее общего списка моделей. | [Сообщение 86398, 2026-07-06](https://t.me/vibecod3rs/86398); [эфир «карта агентов», 2026-07-04](https://youtube.com/watch?v=Nh6Qui9VSUk). |
| **OMP + Orca** | 5 июля Серёжа пишет, что полностью перешёл на OMP для оркестрации агентов разных провайдеров. Orca используется для нескольких CLI-агентов, worktree, терминалов, задач и ревью. Локально установлены `omp 16.3.12` и `orca`; Claude Code подключён к Orca hooks. | [Сообщение 86021, 2026-07-05](https://t.me/vibecod3rs/86021); [эфир «GLM + Orca: мой AI-сетап», 2026-06-30](https://youtube.com/watch?v=ocbtH4-FttI); `/Users/ris/.bun/bin/omp`; `/usr/local/bin/orca`; `/Users/ris/.claude/settings.json:50`. |
| **GitHub Issues / Projects + Git** | GitHub — фактическое хранилище задач и внешняя память агентов. 4 июля Серёжа прямо пишет «я использую гитхаб»; в мартовском эфире показывает Issues/Projects как память и полный путь PRD → issues → выполнение. | [Сообщение 85557, 2026-07-04](https://t.me/vibecod3rs/85557); [эфир GPT-5.4 + Codex, таймкоды 11:12 и 45:25, 2026-03-06](https://youtube.com/watch?v=OtA-P95JnY8); `/Users/ris/Documents/GitHub/personal-corp/CLAUDE.md:37-48`. |
| **Markdown + repo rules** | Claude Code и Codex/OMP читают один канон через `CLAUDE.md` и symlink `AGENTS.md`; facts, решения и правила живут в Markdown/YAML в репозиториях. | `/Users/ris/Documents/GitHub/personal-corp/CLAUDE.md:3`; `/Users/ris/Documents/GitHub/hq/AGENTS.md`; [эфир Fable day 1, AGENTS.md в публичном репо, 2026-06-09](https://youtube.com/watch?v=eguZQ4MAh8U). |
| **Skills-пайплайн** | Свежая формула coding-flow: `/grill-me → /to-prd → /to-issues`, затем задача отдаётся Opus + GLM + GPT-5.5. Основная папка skills — Git-репозиторий, глобальных skills оставлено немного. | [87428, 2026-07-08](https://t.me/vibecod3rs/87428), [87388](https://t.me/vibecod3rs/87388), [87393](https://t.me/vibecod3rs/87393). |

### Важная оговорка по моделям

- `GPT-5.5` — доказанный daily baseline в июне и начале июля.
- `gpt-5.6-sol` — текущий локальный default в `/Users/ris/.codex/config.toml:3` с mtime `2026-07-09 15:24 ART`; это evidence активного теста в день релиза, не накопленная история.
- `Fable 5` — текущий архитектор в Claude Code, но модель и лимиты меняются быстро. На странице лучше показывать роль «архитектор / план», а конкретную модель — как live label с датой обновления.

## 2. Регулярный рабочий стек

| Компонент | Реальное использование | Источники |
|---|---|---|
| **GLM 5.2 / Z.ai** | Дешёвый worker под постановкой/steering GPT-5.5; 6 июля Серёжа называет связку удачной. Это регулярные руки, а не полный переход: 17 июня после теста он отдельно зафиксировал, что GLM слабее в играх и DevOps. | [85669, 2026-07-05](https://t.me/vibecod3rs/85669), [86489, 2026-07-06](https://t.me/vibecod3rs/86489), [эфир GLM 5.2, 2026-06-17](https://youtube.com/watch?v=BYjvQ3hZ6_Q), [эфир сетапа, 2026-06-30](https://youtube.com/watch?v=ocbtH4-FttI). |
| **Grok Composer** | Серёжа использует Composer внутри Grok для повседневных офисных задач: почта, Telegram, драфты, брифы; 4 июля уточняет: «в гроке только композер использую». Новый SuperGrok Heavy куплен 7 июля, однако использование именно Heavy/Grok Build ещё не доказано. | [77600, 2026-06-10](https://t.me/vibecod3rs/77600), [85505, 2026-07-04](https://t.me/vibecod3rs/85505), `/Users/ris/Documents/GitHub/hq/subscriptions.md:18,53`. |
| **ChatGPT + Grok search** | Для общего поиска Серёжа предпочитает ChatGPT; Grok держит ради уникального поиска по X. 7 июля Grok Max был взят именно «для тестов (и для OMP)», поэтому его корректнее показывать как scout/research + эксперимент, не как основной coding worker. | [86817, 2026-07-07](https://t.me/vibecod3rs/86817), [86811](https://t.me/vibecod3rs/86811). |
| **Cursor / Composer / Sonnet** | Альтернативный execution/UI-контур и площадка для сравнений. В июне использовался для Sonnet 5 High, дизайна, ревью и сравнения с GLM. Evidence регулярного daily-default слабее, чем у Codex. | [эфир Sonnet 5, 2026-06-30](https://youtube.com/watch?v=L_W3FTVEa2c); [эфир GLM 5.2, 2026-06-17](https://youtube.com/watch?v=BYjvQ3hZ6_Q). |
| **Chrome, браузерные агенты, Playwright** | Codex/агенты проверяют интерфейсы и авторизованные сервисы. Серёжа пишет, что «половина таких вещей» работает через Codex + `$chrome`: LinkedIn, X, Instagram, картинки/видео и запросы в ChatGPT Pro. В конфиге есть Chrome, Playwright, in-app browser и Computer Use; Playwright установлен (`1.58.0`). | [78264, 2026-06-11](https://t.me/vibecod3rs/78264); [эфир GPT-5.4 + Codex, 2026-03-06](https://youtube.com/watch?v=OtA-P95JnY8); `/Users/ris/.codex/config.toml:24-57,74-77,103-126`; `/opt/homebrew/bin/playwright`. Конкретные MCP могут быть выключены между сессиями, поэтому формулировать как доступный проверочный контур. |
| **Telegram + Telethon** | Telegram — продуктовая поверхность, поддержка, CRM, боты и уведомления. Telethon используется для E2E и архива; текущий `tg-telethon` repo активен и имеет MCP/server scripts. | [эфир GPT-5.4 + Codex, таймкод 49:48, 2026-03-06](https://youtube.com/watch?v=OtA-P95JnY8); `/Users/ris/Documents/GitHub/tg-telethon/requirements.txt`; `/Users/ris/Documents/GitHub/hq/CLAUDE.md:90-101`. |
| **Vercel** | Сайты, фронтенды и быстрые публичные демо. Прямые live-примеры: Fable арканоид опубликован на Vercel; блог `sereja.tech` — Hugo + Vercel. | [сообщение 77447, 2026-06-09](https://t.me/vibecod3rs/77447); `/Users/ris/Documents/GitHub/sereja.tech/hugo.toml`; `/Users/ris/Documents/GitHub/sereja.tech/vercel.json`. |
| **Railway + PostgreSQL** | Боты, API, базы и игровые демо. Dust Arena и GLM-игры разворачивались на Railway; `hsl-mozg` использует Python, SQLAlchemy/Alembic и PostgreSQL. | [сообщение 77441, 2026-06-09](https://t.me/vibecod3rs/77441); [эфир GLM 5.2, 2026-06-17](https://youtube.com/watch?v=BYjvQ3hZ6_Q); `/Users/ris/Documents/GitHub/hsl-mozg/Procfile`; `/Users/ris/Documents/GitHub/hsl-mozg/requirements.txt`. |
| **OVH + Proxmox** | Собственный серверный слой для контейнеров и учебного runtime. Оплата и установка Proxmox зафиксированы, но публичного недавнего рассказа о daily-использовании меньше. На странице держать в «инфраструктуре», не в центре AI-схемы. | `/Users/ris/Documents/GitHub/hq/subscriptions.md:28`; `/Users/ris/Documents/GitHub/hq/CLAUDE.md` (маршрутизация server/runtime). |
| **Obsidian** | Человеческий интерфейс к тому же Git-backed Markdown HQ: `/Users/ris/Documents/obsidian/0_hq` — symlink на `/Users/ris/Documents/GitHub/hq` с 7 июля. Это локальная дополнительная проверка; свежего публичного сообщения о daily-use в текущем окне не найдено. | Локальный symlink; старый публичный контекст: [видео про Obsidian AI-мозг, 2025-07-14](https://youtube.com/watch?v=U-b3uFfrfdA). |

## 3. Языки, фреймворки и данные

Это устойчивее моделей и подходит для отдельного блока страницы:

| Слой | Evidence |
|---|---|
| **Python** | `hsl-mozg` — `python-telegram-bot`, SQLAlchemy, Alembic, APScheduler, psycopg2; `tg-telethon` — Telethon, MCP, pytest. Источники: `/Users/ris/Documents/GitHub/hsl-mozg/requirements.txt`, `/Users/ris/Documents/GitHub/tg-telethon/requirements.txt`. |
| **TypeScript/JavaScript + React** | `live-sereja-tech` — React 19, TypeScript 6, Vite 8, Tailwind 4; `cohorts/frontend` — React 19, TypeScript, Vite, Playwright, Vitest. Источники: соответствующие `package.json`. |
| **Hugo + Markdown** | Публичный блог `sereja.tech`: `/Users/ris/Documents/GitHub/sereja.tech/hugo.toml`, контент в `content/**/*.md`, доставка через `vercel.json`. |
| **Данные** | PostgreSQL для production-сервисов; SQLite для локальных архивов/аналитики; JSON/YAML/Markdown для переносимого канона. Источники: `hsl-mozg/requirements.txt`, `tg-telethon/data/telegram.db`, `personal-corp/ops/registry/*.yaml`, `hq/*.md`. |

Формулировка «React/Vite + Hugo» точнее текущего ядра, чем «React/Next.js»: Next.js есть в ряде старых и экспериментальных репозиториев, но текущие `cohorts` и `live-sereja-tech` используют Vite.

## 4. Контент- и стриминг-стек

Это отдельный регулярный рабочий контур, достойный визуального блока:

- **OBS → YouTube RTMP**;
- **undercast (`obs-overlay`)** — локальный Node overlay server, SSE ticker, prompt widget, screens;
- **Granola → companion daemon** — live-транскрипт и автоматическое обновление текущего этапа;
- **YouTube live chat → chatfeed**;
- **Claude Code hook → prompt-to-overlay**;
- **ElevenLabs** — голоса/озвучка; фактические демо 9 июня и 4 июля;
- **ai-whisper + `yt-dlp` + YouTube API** — транскрипция, главы, описание и публикация.

Источники: [эфир Fable day 3, 2026-06-13](https://youtube.com/watch?v=TPGyDvxL9fQ), [эфир «карта агентов», 2026-07-04](https://youtube.com/watch?v=Nh6Qui9VSUk), `/Users/ris/Documents/GitHub/corp-streaming/lives-analysis.md:74-89`, `/Users/ris/Documents/GitHub/corp-youtube/CLAUDE.md:58-75`.

## 5. Эксперименты и бенчмарки

| Инструмент | Статус по evidence |
|---|---|
| **GPT-5.6 Sol** | Активно выставлен в Codex 9 июля; слишком свежо для daily label. Показать как «тестирую сейчас». |
| **Factory / Droid / Mission Control** | Реально тестировался 18 июня и 1–4 июля, использовался для обкатки skill/оркестрации. Это лаборатория, не ядро. Источники: [80194](https://t.me/vibecod3rs/80194), [эфир Fable 1 июля](https://youtube.com/watch?v=FqxeJHDuJ1U), [эфир 4 июля](https://youtube.com/watch?v=Nh6Qui9VSUk). |
| **Fable 5** | В июне–июле используется как архитектор; одновременно это модель под активным бенчмарком и ограниченными лимитами. На странице лучше показать роль, не обещать постоянство конкретной модели. |
| **OpenCode** | Установлен (`1.17.7`) и регулярно участвует в сравнительных прогонах; 15 июня Серёжа хвалил лимиты, но 17 июня не перешёл на GLM/OpenCode как основной контур. Источники: [79147](https://t.me/vibecod3rs/79147), [эфир GLM](https://youtube.com/watch?v=BYjvQ3hZ6_Q). |
| **v0, Lovable, Claude Design** | Используются для дизайн-вариантов и быстрых UI-тестов. Пример: гайд Fable собран в v0; Lovable сравнивался с Sonnet 5. Это builders/дизайн-лаборатория. Источники: [84885](https://t.me/vibecod3rs/84885), [эфир Sonnet 5](https://youtube.com/watch?v=L_W3FTVEa2c), [70676](https://t.me/vibecod3rs/70676). |
| **Paperclip** | Реально тестировался как система AI-компании; в июньском сетапе Серёжа показывает собственную систему отделов и задач «вместо Paperclip». Это исследованный инструмент, не текущая основа. Источники: [эфир Paperclip, 2026-03-27](https://youtube.com/watch?v=O4KwzNZuaB8), [эфир сетапа, 2026-06-30](https://youtube.com/watch?v=ocbtH4-FttI). |
| **Devin** | Есть Core/credits и исследование Fusion, но в отобранных сообщениях и опубликованных эфирах нет достаточного доказательства регулярной фактической работы. |

## 6. Активные подписки без доказанного регулярного использования

`/Users/ris/Documents/GitHub/hq/subscriptions.md` — реестр доступа и биллинга, не usage telemetry. Сам файл содержит много пометок `needs ... verification`, failed payment и Product Pass promo. Поэтому список подписок нельзя публиковать под заголовком «чем я пользуюсь каждый день».

### Есть доступ, но в первичных публичных источниках текущего окна usage не доказан

- **Manus Pro**
- **Google AI Pro**
- **Canva Business**
- **GitHub Copilot Pro** — плюс неразрешённый billing status
- **Warp Pro**
- **Replit Core** — есть account usage за май, текущий публичный workflow не найден
- **Bolt.new Pro**
- **Magic Patterns Pro** — в реестре написано «используется в проектах», конкретного свежего первичного примера не найдено
- **Raycast Pro**
- **Descript Creator** — майский snapshot показывал 0 использованных AI credits и media minutes
- **Wispr Flow Pro**
- **Notion AI** — доступ есть, а 4 июля Серёжа прямо называет GitHub своим task store и говорит, что Notion только пробовал
- **Zoom Workplace Pro** — используется как операционный сервис для созвонов, но billing status требует проверки; не часть coding core

### Есть реальное использование, но это не daily-core

- **Factory Pro**, **Cursor Pro**, **v0 Premium**, **Lovable**, **ElevenLabs Creator** — подтверждённые тесты/дизайн/медиа.
- **SuperGrok Heavy** — покупка 7 июля подтверждена, Composer использовался и раньше; usage именно нового Heavy/Grok Build пока не доказан.
- **Railway Hobby**, **OVHcloud SYS-2** — реальная инфраструктура, даже если биллинг/следующая дата требуют сверки.
- **Anthropic Max 20x**, **ChatGPT Pro/Codex**, **Z.ai GLM Coding Pro** — реальное использование доказано; provider billing по отдельным строкам не полностью проверен.

Источник для всех billing caveats: `/Users/ris/Documents/GitHub/hq/subscriptions.md:12-38`, snapshot 2026-07-07.

## 7. Что безопасно написать на публичной странице

Рекомендуемая центральная формула:

> Codex делает длинную работу, Claude проектирует сложные куски, GLM/Sonnet помогают руками. OMP и Orca раздают задачи, GitHub хранит очередь и решения, Markdown держит контекст. Браузер и Telegram проверяются агентами, результат уезжает на Vercel, Railway или свой сервер.

Удобная ролевая карта:

| Роль | Текущий выбор | Запасной/дополнительный слой |
|---|---|---|
| Архитектор / план | Claude Fable / Opus | GPT-5.5 advisor |
| Исполнитель / ревью | Codex | Sonnet, GLM |
| Дешёвые параллельные руки | GLM 5.2 | OpenCode / внешние worker terminals |
| Оркестрация | OMP + Orca | Claude Code subagents |
| Память / очередь | GitHub Issues + Markdown | Obsidian как human UI |
| Проверка | тесты + Chrome/Playwright + Telethon | отдельный agent-reviewer |

## 8. Что не стоит утверждать

- «Все перечисленные подписки используются регулярно» — неверно по evidence.
- «GPT-5.6 Sol — новый daily default» — на 9 июля доказан только свежий локальный switch.
- «Notion — система задач» — текущий task store у Серёжи GitHub.
- «Next.js — основной веб-фреймворк» — текущие ключевые приложения чаще React/Vite; Next.js есть в части проектов.
- «Fable сам пишет весь код» — текущий workflow специально отдаёт исполнение Codex/Sonnet/GLM.
- «GLM заменил Codex/Claude» — Серёжа использует GLM как worker и публично отказался от полного перехода после слабых игр/DevOps.
- «Cursor — основной редактор» — текущая доказательная база сильнее у Codex App/Claude Code и терминального workflow.
- Точные цены/лимиты без даты — модельные тарифы и Product Pass статусы быстро меняются.

## 9. Железо

Локальная проверка 2026-07-09: MacBook Pro `MacBookPro18,1`, Apple M1 Pro, 10 CPU cores, 16 GB RAM. Для публикации достаточно «MacBook Pro M1 Pro, 16 GB»; серийные номера и hardware UUID не публиковать.

Дополнительное фактическое железо:

- Arch Linux ноутбук с 8 GB RAM для Linux/Docker-задач — [83735, 2026-07-01](https://t.me/vibecod3rs/83735).
- Выделенный Kimsufi/OVH сервер с 128 GB RAM примерно за $40/мес — [83736, 2026-07-01](https://t.me/vibecod3rs/83736) и `/Users/ris/Documents/GitHub/hq/subscriptions.md:28`.
- Codex App используется как клиент к серверному Codex CLI по SSH; сессия доступна с телефона — [74827, 2026-05-29](https://t.me/vibecod3rs/74827).

Источник: `system_profiler SPHardwareDataType`, выполнено локально 2026-07-09.

## 10. Свежесть и ограничения

- Telegram archive свежий до 2026-07-09, последняя запись Серёжи в `@vibecod3rs` — 2026-07-08 19:12 UTC.
- YouTube source: `/Users/ris/Documents/GitHub/stats-youtube/videos.json`; последние опубликованные видео, использованные здесь, датированы 2026-07-04.
- `corp-youtube/streams/011-gpt-5-6-orchestrate/` — план стрима 9 июля, а не доказательство завершённого использования; из фактических выводов он исключён.
- Локальные конфиги и session file activity использованы как дополнительная проверка частоты, без чтения приватных промптов и без публикации секретов.
- Стек меняется еженедельно; на странице нужен `updated_at` и разделение «ядро / рабочие инструменты / сейчас тестирую / есть доступ».
