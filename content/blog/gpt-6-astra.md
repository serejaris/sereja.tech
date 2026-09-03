---
title: "GPT-6 Astra: общий тест дороже Sol на 75%"
slug: "gpt-6-astra"
date: 2026-09-03
lastmod: 2026-09-03
description: "GPT-6 Astra получила 67 за код и 61 за интеллект. Разбираю цену, доступ, новые функции и первые пользовательские 3D-демо."
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
    a: "Авторы первых пользовательских демо приписывают Astra сильные результаты в коде и 3D. Эти посты не показывают повторяемость. Перед переходом проверьте Astra на собственной задаче и сравните итоговую стоимость с текущей моделью."
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
  - title: "Theo: браузерная 3D-игра от GPT-6 Astra"
    url: "https://x.com/theo/status/2095599934766764338"
  - title: "Matt Wolfe: три ранних теста GPT-6 Astra"
    url: "https://x.com/mreflow/status/2095601201958309895"
---

GPT-6 Astra вышла 3 сентября 2026 года. OpenAI ещё разворачивает доступ. Независимые измерения дают два сигнала. Astra сильна как кодовый агент. В Intelligence Index она стоит заметно дороже GPT-5.6 Sol. Первые пользователи уже показывают браузерные игры и 3D-сцены, которые приписывают одному запросу или нескольким минутам работы Astra. Эти демо объясняют интерес к модели лучше ещё одной таблицы бенчмарков.

## Релиз состоялся, доступ приходит постепенно

В [официальном каталоге OpenAI](https://developers.openai.com/api/docs/models) уже есть модель `gpt-6-astra`. Контекст составляет 1,05 миллиона токенов, максимальный ответ вмещает 128 тысяч. Срез знаний заканчивается 30 апреля 2026 года. Доступны уровни рассуждения `low`, `medium`, `high`, `xhigh` и `max`. Режима `none` у Astra нет.

3 сентября доступ начали открывать предприятиям из Trusted Access Program. API и тарифы Plus, Pro, Business и Enterprise заявлены на ближайшие дни. Факт релиза уже подтверждён. Наличие модели в конкретном аккаунте пока нужно проверять отдельно.

Цена короткого контекста за миллион токенов: $10 за ввод, $1 за кэшированный ввод, $12,50 за запись кэша и $50 за вывод. Для длинного контекста ставки растут до $20, $2, $25 и $75. Большое окно полезно, если снижает число повторных запусков и ручных подсказок.

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

В Astra также работает мониторинг действий вне разрешённой области. API может остановить задачу, ChatGPT и Codex могут запросить проверку. Частые остановки увеличивают время прогона и требуют больше ручного контроля.

## Theo показал 3D-игру Astra менее чем через 17 минут после анонса

Менее чем через 17 минут после анонса разработчик [Theo показал](https://x.com/theo/status/2095599934766764338) 32-секундную запись игры Fishslop. В ней игрок управляет подводным аппаратом, кормит рыб, использует сонар и перемещается по трёхмерному аквариуму. По словам автора, Astra собрала игру за один запрос; весь результат работает в браузере.

<figure class="tw-media" id="theo-fishslop-astra">
<video width="1156" height="720" controls preload="none" poster="/images/blog/gpt-6-astra/community/theo-fishslop-astra.webp" src="/images/blog/gpt-6-astra/community/theo-fishslop-astra.mp4"></video>
<figcaption>Fishslop: браузерная 3D-игра, которую Theo приписывает одному запуску GPT-6 Astra. Видео: <a href="https://x.com/theo/status/2095599934766764338">@theo в X</a>.</figcaption>
</figure>

В ролике есть управление, интерфейс и 3D-сцена. Исходного промпта, кода и истории правок в посте нет. Это демонстрация результата автора. Воспроизвести тест по посту нельзя. Artificial Analysis отдельно подтверждает высокий результат Astra в тесте кодового агента. Два пользовательских поста дают ранний сигнал о 3D и интерфейсах.

Почти одновременно [Matt Wolfe опубликовал](https://x.com/mreflow/status/2095601201958309895) ещё три примера из раннего доступа. По его словам, Astra за восемь минут сделала человекоподобного волка в Blender через управление компьютером. За 12 минут в режиме Ultra она собрала клон Mega Bonk. За 17 минут сделала симулятор Земли с погодой, лесами и населением. Скорость здесь заявлена самим автором; независимого замера в посте нет.

Эти два поста показывают направления ранних демонстраций: 3D, игры и интерфейсы. Судить по ним о массовом спросе и типичном качестве пока рано. Похожая волна пользовательских игр сопровождала [выход Fable 5.1](/blog/claude-fable-5-1/).

## Что видно в день релиза

Artificial Analysis показывает высокий результат Astra в кодовом агенте. Пользовательские ролики добавляют отдельный ранний сигнал по интерфейсам и 3D. Управление в середине хода позволяет корректировать длинный прогон; практическую пользу этой функции ещё предстоит измерить.

В API Astra стоит дорого. В Intelligence Index она набрала столько же, сколько Sol. Задача обошлась дороже. Ролики показывают рабочие демо. По ним пока нельзя оценить повторяемость и стоимость результата на реальном проекте.

Первый контролируемый тест логично провести на кодовой задаче. Прототипы и 3D пока подходят для отдельных экспериментов. Для повседневных общих задач Sol остаётся более понятной точкой отсчёта до широкого доступа и новых независимых замеров.

На сегодня Astra подходит для контролируемых кодовых прогонов. Решение о ежедневной модели требует собственных замеров качества, вмешательств и итоговой стоимости.

Хотите смотреть такие проверки и собирать собственную систему агентов, приходите в [Кружок вайбкодинга](https://t.me/hashslash_bot?start=blog_gpt_6_astra). Код пишут агенты, управляете вы.
