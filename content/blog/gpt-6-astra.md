---
title: "GPT-6 Astra: общий тест дороже Sol на 75%"
slug: "gpt-6-astra"
date: 2026-09-03
lastmod: 2026-09-03
description: "GPT-6 Astra получила 67 за код и 61 за интеллект. Разбираю цену, доступ и живую задачу, которая покажет реальную пользу модели."
tags: ["gpt-6-astra", "openai", "codex", "ai-агенты", "вайбкодинг"]
cta: kruzhok
cta_code: blog_gpt_6_astra
image: "/images/blog/gpt-6-astra-day-one-preview.png"
faq:
  - q: "GPT-6 Astra уже доступна всем?"
    a: "3 сентября 2026 года OpenAI начала развёртывание для предприятий в Trusted Access Program. API и тарифы Plus, Pro, Business и Enterprise заявлены на ближайшие дни."
  - q: "Сколько стоит GPT-6 Astra в API?"
    a: "При коротком контексте OpenAI указывает 10 долларов за миллион входных токенов, 1 доллар за кэшированный ввод, 12 долларов 50 центов за запись кэша и 50 долларов за вывод."
  - q: "GPT-6 Astra лучше GPT-5.6 Sol?"
    a: "В тесте Artificial Analysis кодовый агент Astra получил 67 и использовал примерно треть токенов Sol. Общий Intelligence Index у обеих моделей равен 61. Задача Astra стоила на 75 процентов дороже."
  - q: "Что нужно проверить перед переходом на Astra?"
    a: "Дайте Astra одну нужную задачу из живого бэклога. Сравните принятый результат, время, токены, стоимость, ручные подсказки и остановки мониторинга с текущей рабочей моделью."
sources:
  - title: "OpenAI: GPT-6 Astra"
    url: "https://openai.com/index/gpt-6-astra/"
  - title: "OpenAI: каталог моделей"
    url: "https://developers.openai.com/api/docs/models"
  - title: "OpenAI: цены API"
    url: "https://developers.openai.com/api/docs/pricing"
  - title: "OpenAI: руководство по GPT-6 Astra"
    url: "https://developers.openai.com/api/docs/guides/latest-model"
  - title: "OpenAI: Path to Astra"
    url: "https://openai.com/index/path-to-astra/"
  - title: "Artificial Analysis: тред с измерениями"
    url: "https://x.com/ArtificialAnlys/status/2095595489031000350"
  - title: "Artificial Analysis: карточка GPT-6 Astra"
    url: "https://artificialanalysis.ai/models/gpt-6-astra"
---

GPT-6 Astra вышла 3 сентября 2026 года. Переносить на неё весь рабочий поток сегодня рано. OpenAI ещё разворачивает доступ. Независимые измерения дают два сигнала. Astra сильна как кодовый агент. В Intelligence Index она стоит заметно дороже GPT-5.6 Sol. Главный практический вопрос: доведёт ли Astra одну нужную задачу до рабочего результата быстрее, дешевле и с меньшим числом ручных подсказок? Это и станет главным тестом в эфире.

## Релиз состоялся, доступ приходит постепенно

В [официальном каталоге OpenAI](https://developers.openai.com/api/docs/models) уже есть модель `gpt-6-astra`. Контекст составляет 1,05 миллиона токенов, максимальный ответ вмещает 128 тысяч. Срез знаний заканчивается 30 апреля 2026 года. Доступны уровни рассуждения `low`, `medium`, `high`, `xhigh` и `max`. Режима `none` у Astra нет.

3 сентября доступ начали открывать предприятиям из Trusted Access Program. API и тарифы Plus, Pro, Business и Enterprise заявлены на ближайшие дни. Факт релиза уже подтверждён. Наличие модели в конкретном аккаунте пока нужно проверять отдельно.

Цена короткого контекста за миллион токенов: $10 за ввод, $1 за кэшированный ввод, $12,50 за запись кэша и $50 за вывод. Для длинного контекста ставки растут до $20, $2, $25 и $75. Окно в 1,05 миллиона токенов окупится, если агент сможет закончить задачу без повторных запусков и постоянной помощи.

<figure id="official-release-card">
<img src="/images/blog/gpt-6-astra/openai/launch-card.jpg" alt="Официальная карточка GPT-6 Astra с ценами API" width="1200" height="675" loading="lazy" decoding="async">
<figcaption>Официальная карточка релиза GPT-6 Astra. Источник: <a href="https://x.com/OpenAI/status/2095595741528125780">OpenAI</a>.</figcaption>
</figure>

{{< youtube 1QNsdr-Qx_I >}}

Официальный ролик OpenAI показывает релиз Astra и новые сценарии длинной агентной работы.

<details>
<summary>Все официальные изображения OpenAI</summary>

<figure>
<img src="/images/blog/gpt-6-astra/openai/launch-chart-1.png" alt="График OpenAI с результатами GPT-6 Astra в AutomationBench" width="1492" height="1274" loading="lazy" decoding="async">
<figcaption>AutomationBench: данные OpenAI из официального треда о релизе.</figcaption>
</figure>

<figure>
<img src="/images/blog/gpt-6-astra/openai/launch-chart-2.png" alt="График OpenAI с результатами GPT-6 Astra в ExploitGym" width="1200" height="744" loading="lazy" decoding="async">
<figcaption>ExploitGym: данные OpenAI из официального треда о релизе.</figcaption>
</figure>

<figure>
<img src="/images/blog/gpt-6-astra/openai/launch-chart-3.png" alt="Сводный график OpenAI с оценками GPT-6 Astra" width="1200" height="675" loading="lazy" decoding="async">
<figcaption>Сводка собственных оценок OpenAI для Astra, Sol и Fable 5.1.</figcaption>
</figure>
</details>

## В коде Astra экономит токены

Самый заметный результат Astra показала в [треде Artificial Analysis](https://x.com/ArtificialAnlys/status/2095595489031000350). Coding Agent Index равен 67. Это на два пункта выше GPT-5.6 Sol в их Codex-харнесе и на три пункта ниже Fable 5.1 с fallback.

На уровне `max` Astra использовала примерно треть токенов Sol. Более высокая цена токена съела часть экономии, поэтому стоимость одного кодового прогона осталась около уровня Sol. Рабочая гипотеза: Astra может дольше держать направление и тратить меньше токенов на путь к результату.

<figure id="aa-overview">
<img src="/images/blog/gpt-6-astra/aa/overview.jpg" alt="Artificial Analysis сравнивает GPT-6 Astra с другими моделями по Intelligence Index и Coding Agent Index" width="1200" height="943" loading="lazy" decoding="async">
<figcaption>GPT-6 Astra получила 61 в Intelligence Index и 67 в Coding Agent Index. Источник: Artificial Analysis.</figcaption>
</figure>

<figure>
<img src="/images/blog/gpt-6-astra/aa/coding-token-efficiency.jpg" alt="Coding Agent Index GPT-6 Astra в сравнении с числом использованных токенов" width="1200" height="1126" loading="lazy" decoding="async">
<figcaption>В кодовом тесте Astra расходует примерно треть токенов GPT-5.6 Sol на уровне max. Источник: Artificial Analysis.</figcaption>
</figure>

## Общие задачи стоят дороже

В Intelligence Index результат Astra равен 61. Столько же получила Sol. Astra использовала примерно на 10% меньше выходных токенов. Задача обошлась на 75% дороже: по подсчёту Artificial Analysis, токен Astra стоит в 2,5 раза больше.

В тесте AA-Omniscience доля галлюцинаций снизилась с 92% у Sol до 51% у Astra. Точность выросла с 59% до 63%. В AA-Briefcase Astra прибавила 76 Elo относительно Sol; в GDPval-AA v2 она уступила Sol 81 пункт. Один средний индекс скрывает сильные и слабые режимы, поэтому выбирать Astra только по месту в таблице опасно.

Пока Astra убедительнее всего выглядит в коде. В общих задачах явного преимущества над Sol нет. Я уже разбирал [роль Sol, Terra и Luna](/blog/gpt-5-6-review/): название флагмана само по себе рабочую роль модели не определяет.

<figure>
<img src="/images/blog/gpt-6-astra/aa/intelligence-cost.jpg" alt="Стоимость задач GPT-6 Astra и GPT-5.6 Sol при одинаковом Intelligence Index" width="1200" height="911" loading="lazy" decoding="async">
<figcaption>Одинаковый Intelligence Index при большей стоимости задачи Astra. Источник: Artificial Analysis.</figcaption>
</figure>

<details>
<summary>Остальные графики Artificial Analysis</summary>

<figure><img src="/images/blog/gpt-6-astra/aa/coding-cost.jpg" alt="Coding Agent Index в сравнении со стоимостью задачи" width="1200" height="1055" loading="lazy" decoding="async"><figcaption>Кодовый индекс и стоимость задачи.</figcaption></figure>
<figure><img src="/images/blog/gpt-6-astra/aa/intelligence-output-tokens.jpg" alt="Intelligence Index в сравнении с выходными токенами" width="1200" height="946" loading="lazy" decoding="async"><figcaption>Общий индекс и выходные токены.</figcaption></figure>
<figure><img src="/images/blog/gpt-6-astra/aa/omniscience-hallucinations.jpg" alt="AA-Omniscience сравнивает точность и долю галлюцинаций GPT-6 Astra" width="1086" height="1200" loading="lazy" decoding="async"><figcaption>AA-Omniscience: точность и доля галлюцинаций.</figcaption></figure>
<figure><img src="/images/blog/gpt-6-astra/aa/briefcase-gdpval.jpg" alt="Результаты GPT-6 Astra в AA-Briefcase и GDPval-AA v2" width="1200" height="1084" loading="lazy" decoding="async"><figcaption>Рост в AA-Briefcase и падение в GDPval-AA v2.</figcaption></figure>
<figure><img src="/images/blog/gpt-6-astra/aa/index-breakdown.jpg" alt="Разбивка Intelligence Index GPT-6 Astra по отдельным тестам" width="839" height="1200" loading="lazy" decoding="async"><figcaption>Разбивка Intelligence Index по тестам.</figcaption></figure>
</details>

## Длинный прогон теперь можно направлять

В API появились асинхронные вызовы инструментов, управление агентом в середине хода и `configuration_update`. Во время длинной задачи можно уточнить направление и изменить уровень рассуждения. Агенту уже не обязательно заканчивать текущий ход перед каждой корректировкой.

Для меня это важнее ещё одного красивого ответа в чате. Код пишут агенты под моим управлением: я задаю цель, слежу за направлением и принимаю результат.

В Astra также работает мониторинг действий вне разрешённой области. API может остановить задачу, ChatGPT и Codex могут запросить проверку. В тесте я отдельно запишу каждую такую остановку. Частые остановки увеличат время прогона и потребуют больше ручного контроля.

## Чего зрители ждут от эфира

В обсуждениях вайбкодеров и X повторяются шесть ожиданий: доступ, длинный контекст, способность закончить задачу, скорость, качество интерфейсов и цена. Сравнение с Fable 5.1 тоже звучит часто. Большая таблица моделей не даст ответа владельцу конкретного проекта.

В эфир нужно взять одну issue из живого бэклога. Она уже нужна продукту, живёт в существующем репозитории и заканчивается результатом, который можно открыть и проверить. Точную задачу ещё выбираем в [рабочей заявке corp-content](https://github.com/serejaris/corp-content/issues/49).

До запуска я зафиксирую:

1. Ссылку на issue и исходный коммит.
2. Один запрос, одинаковые инструменты и одинаковое время.
3. Что должно заработать к концу.
4. Как именно проверяется результат.
5. Предел стоимости, подсказок и допустимых остановок.

Сначала агент получит задачу на текущей рабочей модели. Затем тот же вход получит Astra. Код руками я не правлю. Обе модели должны разобраться в проекте, выполнить issue и доказать готовность запуском, тестами или пользовательским сценарием.

Во время прогона считаю принятый результат, минуты, токены, стоимость, ручные подсказки и остановки мониторинга. Сравнение двух агентных запусков через сутки уже разобрано [в отдельной статье](/blog/ox-alpha-yesterday-vs-today/).

## Какое решение останется после эфира

Быстрый и дешёвый прогон засчитаю только при выполненных условиях задачи. Отчёта агента недостаточно. Результат нужно открыть и пройти глазами. В [разборе приёмки кода от агента](/blog/best-practices-code/) видно, почему одного красивого ответа недостаточно.

Успешный прогон с редкими вмешательствами сделает Astra кандидатом на ежедневную работу. Преимущество в одном классе задач даст ей отдельную роль. Провал проверки оставит модель в экспериментальном наборе до следующего теста.

После первой issue выберу роль для Astra. Следующий прогон проверит её на другом проекте и другом типе задачи. Так релиз превращается в рабочее решение с понятной ценой.

Хотите смотреть такие проверки и собирать собственную систему агентов, приходите в [Кружок вайбкодинга](https://t.me/hashslash_bot?start=blog_gpt_6_astra). Код пишут агенты, управляете вы.
