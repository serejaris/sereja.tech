---
title: "TypeSafe выпустила Jev для быстрых решений в программах"
date: 2026-09-17
description: "Jev выбирает действия и возвращает вероятности. Как устроен интерфейс TypeSafe, что показали первые тесты и как проверить модель на своей задаче."
tags: ["LLM", "автоматизация", "агенты"]
image: /images/blog/typesafe-system-one-jev-preview.png
intro: "Программа получила обращение и должна выбрать отдел: поддержка, продажи или платежи. Jev возвращает выбранный вариант и вероятности. Это модель TypeSafe для решений внутри приложений."
cta: none
cta_reason: "Разбор раннего инструмента и границ доказательств; продуктовый переход здесь не требуется."
sources:
  - url: https://typesafe.ai/blog/introducing-system-one-models-and-jev
    title: "TypeSafe: анонс Jev 15 сентября 2026"
    note: "Заявления команды о механизме, задержке, цене и workflow evals"
  - url: https://docs.typesafe.ai/api
    title: "TypeSafe API reference"
    note: "state/questions/answers и три типа вопросов"
  - url: https://docs.typesafe.ai/confidence
    title: "TypeSafe confidence"
    note: "Вероятности, уверенность и ограничения автоматического действия"
  - url: https://evals.typesafe.ai/
    title: "TypeSafe workflow evals"
    note: "Четыре процесса, reference probabilities и режимы сравнения"
  - url: https://x.com/fazxes/status/2100300097695232164
    title: "Ранний внутренний тест команды fx"
    note: "70 случаев, три повтора; Jev и GPT-5.6 Luna"
  - url: https://github.com/browser-use/jev-ultrafast/blob/main/docs/performance.md
    title: "Browser Use: методика Jev Ultrafast"
    note: "Границы таймера, текстовая модель Mercury и ограничения сценария"
  - url: https://docs.typesafe.ai/model-jaggedness/jev-1.13
    title: "TypeSafe: ограничения Jev 1.13"
    note: "Ошибки интерпретации и задачи, требующие отдельной проверки"
---

<style>
@import url('https://fonts.googleapis.com/css2?family=Host+Grotesk:wght@500;600;700;800&family=PT+Mono&display=swap');
.ts-hero { margin: 30px 0 6px; }
.ts-hero svg, .ts-fig svg { display: block; width: 100%; height: auto; }
.ts-fig { margin: 34px 0 10px; }
.ts-cap {
  font-family: 'PT Mono', ui-monospace, Menlo, monospace;
  font-size: 14px; line-height: 1.75;
  color: #a7b1ad; text-align: center;
  max-width: 46em; margin: 10px auto 0;
}
table.ts-table { width: 100%; border-collapse: collapse; font-size: 15px; margin: 26px 0 10px; line-height: 1.5; }
.content table.ts-table th, .content table.ts-table td { border: 1px solid rgba(30,30,30,.2); padding: 10px 12px; vertical-align: top; text-align: left; background: #fffef9; color: #1e1e1e; }
.content table.ts-table thead tr th { background: #abbab9; color: #1e1e1e; font-weight: 700; font-size: 14.5px; }
.content table.ts-table td.rowlabel { width: 118px; font-weight: 600; background: #c9d3d1; color: #1e1e1e; }
@media (max-width: 720px) {
  .ts-tablewrap { overflow-x: auto; }
  table.ts-table { min-width: 620px; }
  .ts-fig, .ts-hero { overflow-x: auto; }
  .ts-fig svg, .ts-hero svg { min-width: 640px; }
}
</style>

Обращение: "Платёж не проходит третий день". Программа выбирает отдел и срочность. Jev возвращает заданный вариант и вероятности для дальнейших действий кода.

15 сентября 2026 [TypeSafe представила Jev](https://typesafe.ai/blog/introducing-system-one-models-and-jev) для коротких решений внутри приложений.

<div class="ts-hero">
<svg viewBox="0 0 960 280" role="img" aria-labelledby="ts-hero-t ts-hero-d" xmlns="http://www.w3.org/2000/svg">
  <title id="ts-hero-t">Jev: состояние на входе, решения на выходе</title>
  <desc id="ts-hero-d">Стилизованная перфокарта Jev: неструктурированное состояние входит слева, из карты выходят выбор и вероятности.</desc>
  <defs>
    <marker id="ts-a-ink" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0, 8 3, 0 6" fill="#1e1e1e"/></marker>
  </defs>
  <rect width="960" height="280" fill="#abbab9"/>
  <g stroke="rgba(30,30,30,.75)" stroke-width="1"><path d="M 26,38 V 26 H 38" fill="none"/><path d="M 922,26 H 934 V 38" fill="none"/></g>
  <rect x="330" y="30" width="300" height="22" fill="#1e1e1e"/>
  <a href="https://typesafe.ai/blog/introducing-system-one-models-and-jev"><text x="480" y="45" font-family="'PT Mono', Menlo, monospace" font-size="18" fill="#fefefe" text-anchor="middle">АНОНС TYPESAFE · 15.09.2026</text></a>
  <path d="M 60,158 H 240" fill="none" stroke="#1e1e1e" stroke-width="1.4" marker-end="url(#ts-a-ink)"/>
  <text x="150" y="146" font-family="'PT Mono', Menlo, monospace" font-size="18" fill="rgba(30,30,30,.8)" text-anchor="middle">состояние</text>
  <rect x="248" y="72" width="464" height="176" rx="10" fill="#12b3a2"/>
  <rect x="270" y="94" width="78" height="34" rx="5" fill="#fefefe"/>
  <text x="309" y="117" font-family="'PT Mono', Menlo, monospace" font-size="19" font-weight="bold" fill="#1e1e1e" text-anchor="middle">JEV</text>
  <g>
    <ellipse cx="392" cy="111" rx="7" ry="11" fill="#0c7f70"/><ellipse cx="418" cy="111" rx="7" ry="11" fill="#fefefe"/><ellipse cx="444" cy="111" rx="7" ry="11" fill="#0c7f70"/><ellipse cx="470" cy="111" rx="7" ry="11" fill="#fefefe"/><ellipse cx="496" cy="111" rx="7" ry="11" fill="#0c7f70"/><ellipse cx="522" cy="111" rx="7" ry="11" fill="#fefefe"/><ellipse cx="548" cy="111" rx="7" ry="11" fill="#0c7f70"/><ellipse cx="574" cy="111" rx="7" ry="11" fill="#fefefe"/><ellipse cx="600" cy="111" rx="7" ry="11" fill="#0c7f70"/><ellipse cx="626" cy="111" rx="7" ry="11" fill="#fefefe"/><ellipse cx="652" cy="111" rx="7" ry="11" fill="#0c7f70"/><ellipse cx="678" cy="111" rx="7" ry="11" fill="#fefefe"/>
  </g>
  <g font-family="'PT Mono', Menlo, monospace" font-size="24" fill="#1e1e1e" text-anchor="middle">
    <text x="360" y="168">0 1 1 0 0 1 1 0</text>
    <text x="360" y="204">1 0 0 1 1 0 0 1</text>
    <text x="360" y="240">0 1 0 1 0 1 1 0</text>
    <text x="580" y="168">1 1 0 0 0 1</text>
    <text x="580" y="204">0 0 1 1 1 0</text>
    <text x="580" y="240">1 0 1 0 0 1</text>
  </g>
  <path d="M 718,158 H 898" fill="none" stroke="#1e1e1e" stroke-width="1.4" marker-end="url(#ts-a-ink)"/>
  <text x="808" y="146" font-family="'PT Mono', Menlo, monospace" font-size="18" fill="rgba(30,30,30,.8)" text-anchor="middle">решения</text>
  <text x="808" y="180" font-family="'PT Mono', Menlo, monospace" font-size="18" fill="rgba(30,30,30,.6)" text-anchor="middle">вариант</text>
  <text x="808" y="205" font-family="'PT Mono', Menlo, monospace" font-size="18" fill="rgba(30,30,30,.6)" text-anchor="middle">вероятности</text>
</svg>
</div>

## Jev получает состояние программы и вопросы

Состояние описывает происходящее: обращение, заказ или страницу браузера. Вопрос задаёт решение и разрешённые ответы. [Документация API](https://docs.typesafe.ai/api) называет эти части `state` и `questions`; результат приходит в `answers`.

Типы вопросов:

| Тип | Пример вопроса | Что получает программа |
|---|---|---|
| Choice, выбор | В какой отдел передать обращение? | Вариант из списка и вероятности всех вариантов |
| Noul, да/нет | Сообщает ли человек о срочной проблеме? | Вероятность ответа "да" от 0 до 1 |
| Score, оценка | Насколько человек недоволен по заданной шкале? | Оценку, вычисленную по вероятностям уровней |

[TypeSafe](https://typesafe.ai/blog/introducing-system-one-models-and-jev) называет подход System One, обучение RLCD: обучение с подкреплением для калиброванных решений. Контракт API не доказывает внутреннюю архитектуру.

## Заданный тип ответа помогает коду, правильность проверяется отдельно

Если приложение разрешило три отдела, ответ должен содержать один из этих вариантов. TypeSafe заявляет гарантию соответствия схеме. Модель при этом способна выбрать неверный отдел: допустимое значение ещё может быть смысловой ошибкой.

Другие языковые модели тоже возвращают данные по схеме. Сравнение требует одинаковых задач, схем и настроек.

[Показатель confidence](https://docs.typesafe.ai/confidence) у Choice и Score вычисляется из распределения вероятностей; Noul его отдельно не возвращает. [Калибровка](https://docs.typesafe.ai/concepts/system-one) означает соответствие вероятностей частоте верных ответов на выборке, требует проверки на своих данных и не гарантирует отдельного решения.

## Почему проверке агента нужен контекст всей работы

Классификатор выбирает заданную категорию по смыслу входа. Обещание отправить письмо ещё не подтверждает отправку: проверке агента нужны доказательства выполненных действий.

В [Agent Trace Observability от TypeSafe](https://evals.typesafe.ai/agent_trace_observability) проверяется журнал работы агента поддержки. На входе: инструкции, разговор, вызовы инструментов с аргументами и результатами, финальное сообщение и оставленный пользователем отзыв. Разбор начинается с необратимых действий: разрешение оценивается на момент каждого действия. Нарушение сразу вызывает дежурного. Затем отдельно определяются выполнение задачи и удовлетворённость пользователя. Дальнейший вопрос определяет маршрут: закрыть случай, поставить в очередь, завести ошибку или передать человеку.

[Обвязка приложения](https://raw.githubusercontent.com/typesafe-ai/skills/main/skills/typesafe-ai/SKILL.md) собирает достаточно релевантный контекст. Проверке отправки письма нужны просьба, действовавшие разрешения, адресат, аргументы и результат инструмента. Удовлетворённости: последующие сообщения и отзыв. Отдельные вопросы сохраняют необходимые связи и доказательства. Полный журнал служит источником этих связей; вход каждого вопроса определяется задачей.

[Недостающие данные](https://raw.githubusercontent.com/typesafe-ai/skills/main/skills/typesafe-ai/SKILL.md) нужно получить. Если необходимая цепочка не помещается во вход, [в приложении можно предусмотреть передачу модели с большим контекстом или человеку](https://docs.typesafe.ai/confidence). Отсутствующие доказательства исключают успешный вердикт.

[Тест TypeSafe](https://evals.typesafe.ai/agent_trace_observability) сравнивает ответы с эталоном. В одном примере все три модели расходятся с эталоном. Совпадение с разметкой не устанавливает фактическую правильность эталона: она требует проверки человеком.

## Множители TypeSafe относятся к четырём собственным тестам

В [анонсе TypeSafe](https://typesafe.ai/blog/introducing-system-one-models-and-jev) команда заявляет 193,6× ускорения и 444,6× снижения стоимости в своих workflow evals, то есть проверках целых процессов. Знаменатель и расчёт не раскрыты. Эти результаты не устанавливают выигрыш на других задачах.

На [странице тестов](https://evals.typesafe.ai/) показаны четыре процесса: разбор инцидента безопасности, проверка работы агента поддержки, обработка счёта и обслуживание клиента. Код выполняет фиксированные правила, модель отвечает на отдельные вопросы. График усредняет точность, цену и время четырёх процессов с равным весом.

[Ориентир для ответов](https://evals.typesafe.ai/) получен усреднением GPT-6 Astra и Fable 5.1 с высоким уровнем размышления. Остальные модели используют настройки размышления провайдера по умолчанию и обёртку для структурированных вероятностей. Эталон ответов не задаёт базу множителей скорости и цены.

Сравнение требует времени и полной стоимости одинаковых процессов, включая дополнительные модели. [Тесты](https://evals.typesafe.ai/) подготовила команда TypeSafe; в [анонсе](https://typesafe.ai/blog/introducing-system-one-models-and-jev) она также отмечает возможное смещение и запуск с ноутбуков на западном побережье США.

## Применение начинается с повторяющегося выбора

[Карта сценариев TypeSafe](https://docs.typesafe.ai/concepts/use-case-map) предлагает выбор инструмента агентом, маршрутизацию, оценку срочности и проверку ответов. Каждому сценарию нужна проверка данных, ошибок и риска.

<figure class="ts-fig">
<svg viewBox="0 0 960 480" role="img" aria-labelledby="ts-diag-t ts-diag-d" xmlns="http://www.w3.org/2000/svg">
  <title id="ts-diag-t">Вызов Jev внутри обычного кода</title>
  <desc id="ts-diag-d">Состояние поступает в Jev, решение возвращается в код: инструмент, развилка, срочность или проверка ответа.</desc>
  <defs>
    <marker id="ts-d-ink" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0, 8 3, 0 6" fill="#1e1e1e"/></marker>
    <marker id="ts-d-green" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0, 8 3, 0 6" fill="#03aa5c"/></marker>
  </defs>
  <rect width="960" height="504" fill="#f8fafc"/>
  <rect x="40" y="64" width="210" height="96" rx="6" fill="#ffffff" stroke="#1e1e1e" stroke-width="1"/>
  <text x="145" y="120" fill="#1e1e1e" font-size="20" font-weight="600" font-family="'Host Grotesk', system-ui, sans-serif" text-anchor="middle">Состояние</text>
  <text x="145" y="140" fill="#64748b" font-size="18" font-family="'PT Mono', Menlo, monospace" text-anchor="middle">текст или данные</text>
  <path d="M 250,112 H 352" fill="none" stroke="#1e1e1e" stroke-width="1.2" marker-end="url(#ts-d-ink)"/>
  <rect x="273" y="97" width="56" height="13" rx="2" fill="#f8fafc"/>
  <rect x="360" y="52" width="240" height="120" rx="6" fill="#ffffff" stroke="#03aa5c" stroke-width="1.4"/>
  <text x="480" y="102" fill="#1e1e1e" font-size="24" font-weight="600" font-family="'Host Grotesk', system-ui, sans-serif" text-anchor="middle">Jev</text>
  <text x="480" y="124" fill="#475569" font-size="18" font-family="'PT Mono', Menlo, monospace" text-anchor="middle">выбор и вероятности</text>
  <path d="M 600,112 H 702" fill="none" stroke="#1e1e1e" stroke-width="1.2" marker-end="url(#ts-d-ink)"/>
  <rect x="625" y="97" width="52" height="13" rx="2" fill="#f8fafc"/>
  <rect x="710" y="64" width="210" height="96" rx="6" fill="#ffffff" stroke="#1e1e1e" stroke-width="1"/>
  <text x="815" y="120" fill="#1e1e1e" font-size="20" font-weight="600" font-family="'Host Grotesk', system-ui, sans-serif" text-anchor="middle">Решение</text>
  <text x="815" y="140" fill="#64748b" font-size="18" font-family="'PT Mono', Menlo, monospace" text-anchor="middle">ответ по схеме</text>
  <path d="M 480,172 V 202" fill="none" stroke="#03aa5c" stroke-width="1.2"/>
  <path d="M 480,202 H 168 Q 160,202 160,210 V 264" fill="none" stroke="#03aa5c" stroke-width="1.2" marker-end="url(#ts-d-green)"/>
  <path d="M 480,202 H 381 Q 373,202 373,210 V 264" fill="none" stroke="#03aa5c" stroke-width="1.2" marker-end="url(#ts-d-green)"/>
  <path d="M 480,202 H 578 Q 586,202 586,210 V 264" fill="none" stroke="#03aa5c" stroke-width="1.2" marker-end="url(#ts-d-green)"/>
  <path d="M 480,202 H 791 Q 799,202 799,210 V 264" fill="none" stroke="#03aa5c" stroke-width="1.2" marker-end="url(#ts-d-green)"/>
  <rect x="40" y="232" width="880" height="228" rx="8" fill="rgba(30,30,30,0.025)" stroke="rgba(30,30,30,0.12)" stroke-width="0.8"/>
  <rect x="62" y="272" width="196" height="150" rx="6" fill="#ffffff" stroke="#1e1e1e" stroke-width="1"/>
  <text x="78" y="326" fill="#1e1e1e" font-size="20" font-weight="600" font-family="'Host Grotesk', system-ui, sans-serif">Инструмент</text>
  <text x="78" y="350" fill="#475569" font-size="18" font-family="'PT Mono', Menlo, monospace">выбор</text>
  <text x="78" y="366" fill="#475569" font-size="18" font-family="'PT Mono', Menlo, monospace">следующего шага</text>
  <rect x="275" y="272" width="196" height="150" rx="6" fill="#ffffff" stroke="#1e1e1e" stroke-width="1"/>
  <text x="291" y="326" fill="#1e1e1e" font-size="20" font-weight="600" font-family="'Host Grotesk', system-ui, sans-serif">Развилка</text>
  <text x="291" y="350" fill="#475569" font-size="18" font-family="'PT Mono', Menlo, monospace">продолжить или</text>
  <text x="291" y="366" fill="#475569" font-size="18" font-family="'PT Mono', Menlo, monospace">остановиться</text>
  <rect x="488" y="272" width="196" height="150" rx="6" fill="#ffffff" stroke="#1e1e1e" stroke-width="1"/>
  <text x="504" y="326" fill="#1e1e1e" font-size="20" font-weight="600" font-family="'Host Grotesk', system-ui, sans-serif">Оценка</text>
  <text x="504" y="350" fill="#475569" font-size="18" font-family="'PT Mono', Menlo, monospace">срочность и риск</text>
  <text x="504" y="366" fill="#475569" font-size="18" font-family="'PT Mono', Menlo, monospace">до действия</text>
  <rect x="701" y="272" width="196" height="150" rx="6" fill="#ffffff" stroke="#1e1e1e" stroke-width="1"/>
  <text x="717" y="326" fill="#1e1e1e" font-size="20" font-weight="600" font-family="'Host Grotesk', system-ui, sans-serif">Проверка</text>
  <text x="717" y="350" fill="#475569" font-size="18" font-family="'PT Mono', Menlo, monospace">качество ответа</text>
  <text x="717" y="366" fill="#475569" font-size="18" font-family="'PT Mono', Menlo, monospace">по критериям</text>

</svg>
<figcaption class="ts-cap"><a href="https://docs.typesafe.ai/api">Интерфейс Jev</a>: состояние программы, вопрос по заданной схеме и ответ для кода. Правильность выбора требует проверки на данных приложения.</figcaption>
</figure>

В [демо Doom команды TypeSafe](https://x.com/CompleteSkeptic/status/2099925687465570372) Jev выбирает действия по структурированному текстовому состоянию игры. Распознавание пикселей этим демо не показано. Десять вызовов в секунду и около семи долларов в час являются оценками команды. Перенос оценки требует учёта размера входа, частоты и дополнительных расходов.

<figure>
<video controls playsinline preload="metadata" style="display:block;width:100%;height:auto" aria-label="Оригинальная демонстрация Jev в Doom от TypeSafe">
<source src="/images/blog/typesafe-system-one-jev/doom-original.mp4" type="video/mp4">
<a href="https://x.com/CompleteSkeptic/status/2099925687465570372">Видео Jev в Doom от TypeSafe</a>
</video>
<figcaption class="ts-cap"><a href="https://x.com/CompleteSkeptic/status/2099925687465570372">TypeSafe / Diogo Almeida, 15 сентября</a>: Jev выбирает действия по текстовому состоянию Doom. Оригинальная запись, без сокращения.</figcaption>
</figure>

В [Wikiracing команды TypeSafe](https://x.com/CompleteSkeptic/status/2099925688925184171) Jev выбирает ссылку для перехода от одной статьи Wikipedia к другой. Таймер исключает загрузку страницы; более 255 ссылок требуют двухэтапного выбора. Оптимальный маршрут не гарантирован.

## Первые проверки имеют собственные условия

В [раннем внутреннем тесте команды fx](https://x.com/fazxes/status/2100300097695232164) проверяли 70 размеченных случаев классификации команд по три раза. Jev дала 207 верных решений из 210, GPT-5.6 Luna дала 203. Медиана задержки составила 312 мс против 1458 мс, около 4,7× на этой выборке. Повторы зависимы; маркетинговые 193,6× и 444,6× здесь не воспроизводятся.

В [демо Browser Use](https://github.com/browser-use/jev-ultrafast/blob/main/docs/performance.md) поиск рейсов Цюрих → Лондон занял 7,073 секунды. По описанию измерения таймер начинается после первичного наблюдения страницы; начальная навигация и независимая проверка результата находятся за его пределами. Jev выбирает действие и элемент, Mercury генерирует строки с городами. Покупки билетов нет.

[Авторы](https://github.com/browser-use/jev-ultrafast/blob/main/docs/performance.md) ограничивают статистические выводы сравнения трёх пар прогонов. Двухмодельный сценарий не устанавливает надёжность для произвольных сайтов.

## У модели есть ограничения, у цены есть дата

TypeSafe описывает [ограничения Jev 1.13](https://docs.typesafe.ai/model-jaggedness/jev-1.13): математика, даты, косвенные связи, противоречивые критерии и длинное нерелевантное состояние могут приводить к ошибкам. Несколько зависимых решений требуют проверки всего процесса, включая поведение после неверного ответа.

[Цена прямого API](https://docs.typesafe.ai/models) на 17 сентября: $0,042 за миллион входных токенов, выход бесплатный. Диапазон 70-500 мс за вызов является [заявлением TypeSafe](https://typesafe.ai/blog/introducing-system-one-models-and-jev) о задержке. Устойчивость цены не установлена; компания не исключает субсидию.

## Как попробовать через официальный skill

[TypeSafe skill](https://docs.typesafe.ai/agent-skill) даёт агенту для работы с проектом инструкции: читать документацию Jev, разбивать задачу на типизированные вопросы и добавлять вызовы API в приложение. Он полезен, если ты уже работаешь с таким агентом и хочешь встроить выбор или оценку в свой проект.

Для [Claude Code](https://docs.typesafe.ai/agent-skill) выполни в терминале две команды:

```bash
claude plugin marketplace add typesafe-ai/skills
claude plugin install typesafe@typesafe-ai
```

Для [Codex и других поддерживаемых агентов](https://docs.typesafe.ai/agent-skill) нужен Node.js с `npx`. Команда предложит выбрать агента; установка по умолчанию относится к текущему проекту:

```bash
npx skills add typesafe-ai/skills --skill typesafe-ai
```

[Официальный README](https://github.com/typesafe-ai/skills) предлагает распределять обращения поддержки по отделам, отправляя неоднозначные решения человеку. В Claude Code вызови [/typesafe:typesafe-ai](https://docs.typesafe.ai/agent-skill); в другом агенте обратись к skill по имени. Предложенный первый промпт:

> Используй skill typesafe-ai. Добавь маршрутизацию обращений: поддержка, продажи или платежи. Начни с текста "Платёж не проходит третий день". Jev должна вернуть выбранный отдел и вероятности вариантов. Неоднозначные случаи отправляй человеку; покажи, какие данные и разрешения нужны до подключения API.

Ожидаемый результат интеграции: [ответ Choice](https://docs.typesafe.ai/primitives/choice) с разрешённым вариантом и распределением вероятностей. [Skill](https://raw.githubusercontent.com/typesafe-ai/skills/main/skills/typesafe-ai/SKILL.md) не запускает контроль всех действий агента: порядок запросов, пороги, проверки и исполнение остаются в коде приложения.

Установка инструкций не выдаёт доступ к модели. Для первой пробы открой [playground TypeSafe](https://console.typesafe.ai/playground) и войди в аккаунт. Для [прямого API](https://docs.typesafe.ai/introduction/quickstart) нужен ключ из [настроек аккаунта](https://console.typesafe.ai/settings/keys); фактический доступ зависит от аккаунта. Другой [подтверждённый путь через Vercel AI Gateway](https://vercel.com/changelog/typesafe-ai-jev-now-available-on-ai-gateway) использует ключ Gateway или Vercel OIDC. Ключ TypeSafe и ключ Gateway относятся к разным сервисам. Попроси агента выбрать один маршрут и сверить актуальный quickstart перед интеграцией; ключ не вставляй в публичный код или промпт.

[Прямой API](https://docs.typesafe.ai/models) на 17 сентября стоит $0,042 за миллион входных токенов, выход бесплатный. [Карточка Gateway](https://vercel.com/ai-gateway/models/jev) указывает $0,04 за миллион входных токенов; цена выходных токенов здесь не указана. Расходы основного агента и дополнительных моделей оплачиваются отдельно.

## Проверка на своей задаче даёт основание для внедрения

В [разборе голосового браузера](/blog/jev-voice-browser/) Jev выбирает действие по распознанной команде и подписям элементов страницы.

Сравни Jev и текущую модель на одинаковых размеченных случаях: ошибки, задержку, полную стоимость и последствия неверного выбора. Учти дополнительные модели и обращения к человеку.

До автоматического действия задай условия остановки и передачи человеку. Порог уверенности проверь на фактических ошибках с учётом риска.
