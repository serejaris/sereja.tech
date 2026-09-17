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

Программа получила обращение: "Платёж не проходит третий день". Ей нужно выбрать отдел и решить, срочен ли вопрос. Jev умеет возвращать выбор из заданных вариантов и вероятности, с которыми код может работать дальше.

15 сентября 2026 [TypeSafe представила Jev](https://typesafe.ai/blog/introducing-system-one-models-and-jev). Модель рассчитана на такие короткие решения внутри приложений. Её стоит проверять на повторяющихся выборах с известным правильным ответом.

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

Вызов состоит из двух частей. Состояние описывает происходящее: текст обращения, данные заказа или текущую страницу браузера. Вопрос задаёт, что нужно решить и какие ответы разрешены. [Документация API](https://docs.typesafe.ai/api) называет эти части `state` и `questions`; результат приходит в `answers`.

Три типа вопросов:

| Тип | Пример вопроса | Что получает программа |
|---|---|---|
| Choice, выбор | В какой отдел передать обращение? | Вариант из списка и вероятности всех вариантов |
| Noul, да/нет | Сообщает ли человек о срочной проблеме? | Вероятность ответа "да" от 0 до 1 |
| Score, оценка | Насколько человек недоволен по заданной шкале? | Оценку, вычисленную по вероятностям уровней |

В этом примере приложение задаёт критерии и решает, что делать с ответом.

TypeSafe называет свой класс моделей System One, а обучение RLCD: обучение с подкреплением для калиброванных решений. Названия описывают подход команды. Внешний контракт: состояние, вопросы и ответы по схеме; внутреннюю архитектуру он не доказывает.

## Заданный тип ответа помогает коду, правильность проверяется отдельно

Если приложение разрешило три отдела, ответ должен содержать один из этих вариантов. TypeSafe заявляет гарантию соответствия схеме. Модель при этом способна выбрать неверный отдел: допустимое значение ещё может быть смысловой ошибкой.

Языковые модели тоже умеют возвращать структурированные данные. Для сравнения нужны одинаковые задачи, разрешённые ответы, настройки и проверка результата.

[Показатель confidence](https://docs.typesafe.ai/confidence) у Choice и Score вычисляется из распределения вероятностей; Noul его отдельно не возвращает. Хорошая калибровка означает соответствие вероятностей фактической частоте правильных ответов на проверочной выборке. Её нужно измерять на своих данных.

## Множители TypeSafe относятся к четырём собственным тестам

В [анонсе TypeSafe](https://typesafe.ai/blog/introducing-system-one-models-and-jev) команда заявляет 193,6× ускорения и 444,6× снижения стоимости в своих workflow evals, то есть проверках целых процессов. Описание не раскрывает точный знаменатель и расчёт обоих множителей. Универсального выигрыша эти числа не обещают.

На [странице тестов](https://evals.typesafe.ai/) показаны четыре процесса: разбор инцидента безопасности, проверка работы агента поддержки, обработка счёта и обслуживание клиента. Код выполняет фиксированные правила, модель отвечает на отдельные вопросы. График усредняет точность, цену и время четырёх процессов с равным весом.

[Ориентир для ответов](https://evals.typesafe.ai/) получен усреднением GPT-6 Astra и Fable 5.1 с высоким уровнем размышления. Остальные модели оцениваются с настройками размышления по умолчанию у провайдера. Этот эталон ответов не задаёт базу множителей скорости и цены. Модели LLM в этих проверках используют обёртку для структурированных вероятностных ответов.

Для сравнения нужны время и полная стоимость одинаковых задач, включая дополнительные модели. Цена за миллион токенов не даёт множителя стоимости процесса. [Тесты](https://evals.typesafe.ai/) подготовила команда TypeSafe; в [анонсе](https://typesafe.ai/blog/introducing-system-one-models-and-jev) она также отмечает возможное смещение и запуск с ноутбуков на западном побережье США.

## Применение начинается с повторяющегося выбора

[Карта сценариев TypeSafe](https://docs.typesafe.ai/concepts/use-case-map) предлагает выбор инструмента агентом, маршрутизацию, оценку срочности и проверку ответов. Это направления для эксперимента. Для каждого требуется отдельная проверка данных, правильности решения и допустимого риска.

<figure class="ts-fig">
<svg viewBox="0 0 960 480" role="img" aria-labelledby="ts-diag-t ts-diag-d" xmlns="http://www.w3.org/2000/svg">
  <title id="ts-diag-t">Вызов Jev внутри обычного кода</title>
  <desc id="ts-diag-d">Предложенные TypeSafe сценарии. Состояние поступает в Jev, ответ по заданной схеме возвращается в код. Примеры: выбор инструмента, развилка выполнения, оценка срочности и проверка ответов. Смысловая правильность каждого решения требует проверки.</desc>
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

В [демо Doom команды TypeSafe](https://x.com/CompleteSkeptic/status/2099925687465570372) Jev получает структурированное текстовое состояние игры и выбирает действия бота. Из него выбираются действия; распознавание пикселей этим демо не показано. Десять вызовов в секунду и около семи долларов в час являются оценками команды. Их нельзя перенести на другую задачу без размера входа, частоты запросов и дополнительных расходов.

В [Wikiracing команды TypeSafe](https://x.com/CompleteSkeptic/status/2099925688925184171) Jev выбирает ссылку для перехода от одной статьи Wikipedia к другой. Время модели исключает загрузку страницы; при более 255 ссылках нужен двухэтапный выбор с дополнительным вызовом. Демо показывает навигацию, гарантия оптимального маршрута отсутствует.

## Первые проверки имеют собственные условия

В [раннем внутреннем тесте команды fx](https://x.com/fazxes/status/2100300097695232164) проверяли 70 размеченных случаев классификации команд по три раза. Jev дала 207 верных решений из 210, GPT-5.6 Luna дала 203. Медиана задержки составила 312 мс против 1458 мс, около 4,7× на этой выборке. Повторы одного случая не превращают его в три независимые задачи. Этот тест не воспроизводит маркетинговые 193,6× и 444,6×.

В [демо Browser Use](https://github.com/browser-use/jev-ultrafast/blob/main/docs/performance.md) поиск рейсов Цюрих → Лондон занял 7,073 секунды. По описанию измерения таймер начинается после первичного наблюдения страницы; начальная навигация и независимая проверка результата находятся за его пределами. Jev выбирает действие и элемент, Mercury генерирует строки с городами. Бронирование и покупка в задачу не входят.

[Авторы](https://github.com/browser-use/jev-ultrafast/blob/main/docs/performance.md) ограничивают статистические выводы сравнения трёх пар прогонов. Этот ранний сценарий с двумя моделями не устанавливает надёжность для произвольных сайтов.

## У модели есть ограничения, у цены есть дата

TypeSafe описывает [ограничения Jev 1.13](https://docs.typesafe.ai/model-jaggedness/jev-1.13): математика, даты, косвенные связи, противоречивые критерии и длинное нерелевантное состояние могут приводить к ошибкам. Несколько зависимых решений требуют проверки всего процесса, включая поведение после неверного ответа.

[Цена прямого API](https://docs.typesafe.ai/models) на 17 сентября: $0,042 за миллион входных токенов, выход бесплатный. Диапазон 70-500 мс за вызов является [заявлением TypeSafe](https://typesafe.ai/blog/introducing-system-one-models-and-jev) о задержке. Долгосрочная устойчивость цены независимо не установлена. Компания сама признаёт, что пока не может доказать отсутствие субсидии.

## Проверка на своей задаче даёт основание для внедрения

В [разборе голосового браузера](/blog/jev-voice-browser/) Jev выбирает действие по распознанной команде и подписям элементов страницы.

Начни с одного повторяющегося решения и набора случаев с известными ответами. Сравни Jev и текущую модель на этих же данных: долю ошибок, задержку, полную стоимость и последствия неверного выбора. Учти дополнительные модели и обращения к человеку, если они нужны процессу.

До автоматического действия задай условия остановки. При неоднозначном ответе система может запросить данные или передать решение человеку. Высокая уверенность тоже требует проверки на фактических ошибках: нужный порог определяется задачей и её риском.

Пригодность Jev определяется скоростью и ценой конкретного процесса при допустимом числе ошибок.
