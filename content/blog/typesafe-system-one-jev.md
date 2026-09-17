---
title: "Jev: модель, которая не пишет текст"
date: 2026-09-17
description: "TypeSafe выпустила Jev: модель не пишет текст, а отдаёт коду решения с вероятностями за 70–500 мс. Как это работает и откуда 193,6× и 444,6×."
tags: ["LLM", "автоматизация", "агенты"]
image: /images/blog/typesafe-system-one-jev-preview.png
intro: "LLM отвечают людям. TypeSafe построили модель, которая отвечает софту: не строками, а типизированными решениями с вероятностями. Разобрал их анонс, сверстал реплику страницы и проверил, откуда берутся заявленные 193,6× и 444,6×."
sources:
  - url: https://typesafe.ai/blog/introducing-system-one-models-and-jev
    title: "Introducing System One Models & Jev — TypeSafe AI Blog"
    note: "исходный анонс, все цифры и формулировки из него"
  - url: https://evals.typesafe.ai/
    title: "TypeSafe workflow evals"
    note: "методика оценок, воркфлоу, примеры и расхождения"
  - url: https://typesafe.ai/blog/bitterest-lesson
    title: "AI's Bitterest Lesson — TypeSafe AI Blog"
    note: "почему они оптимизируют под другую задачу"
  - url: https://typesafe.ai/blog/antibenchmaxxing
    title: "Lies, Damned Lies, and Benchmarks — TypeSafe AI Blog"
    note: "их философия отказа от публичных бенчмарков"
  - url: https://docs.typesafe.ai/concepts/use-case-map
    title: "TypeSafe docs: use case map"
    note: "карта сценариев применения"
  - url: https://x.com/fazxes/status/2100300097695232164
    title: "fx command-check test: Jev против GPT-5.6 Luna"
    note: "независимый замер: 312 мс против 1458 мс, 207/210 против 203/210"
  - url: https://github.com/browser-use/jev-ultrafast
    title: "Browser Use: Jev Ultrafast"
    note: "агент на Jev, рейсы за 7,1 секунды; методика и ограничения опубликованы"
  - url: https://github.com/AnotiaWang/awesome-jev
    title: "awesome-jev"
    note: "каталог ранних проектов с открытым кодом"
---

<style>
@import url('https://fonts.googleapis.com/css2?family=Host+Grotesk:wght@500;600;700;800&family=PT+Mono&display=swap');
.ts-hero { margin: 30px 0 6px; }
.ts-hero svg, .ts-fig svg { display: block; width: 100%; height: auto; }
.ts-fig { margin: 34px 0 10px; }
.ts-cap {
  font-family: 'PT Mono', ui-monospace, Menlo, monospace;
  font-size: 11.5px; line-height: 1.75;
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

LLM отвечают текстом. Хорошим, связным, со структурой и оговорками. Но софту текст нужен в последнюю очередь: приложению требуется решение, у которого есть тип и вероятность, а не абзац с рассуждением.

15 сентября TypeSafe выпустила Jev, первую публичную модель нового класса. Класс они называют System One Models: модели, которые принимают быстрые структурированные решения и отдают их программе напрямую. Основатель Диогу Алмейда (Diogo Almeida) раньше работал в OpenAI над методами, из которых вырос ChatGPT, два года провёл в стелс-режиме и теперь выпустил то, что называет недостающей частью автоматизации.

Я прочитал анонс, собрал реплику их страницы, чтобы посмотреть на цифры вблизи, и пересказал главное здесь: что такое System One, откуда берутся заявления про 193,6× скорости и 444,6× цены и где к этим цифрам вопросы.

<div class="ts-hero">
<svg viewBox="0 0 960 280" role="img" aria-labelledby="ts-hero-t ts-hero-d" xmlns="http://www.w3.org/2000/svg">
  <title id="ts-hero-t">Jev: состояние на входе, решения на выходе</title>
  <desc id="ts-hero-d">Стилизованная перфокарта Jev: неструктурированное состояние входит слева, из карты выходят типизированные вероятностные решения.</desc>
  <defs>
    <marker id="ts-a-ink" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0, 8 3, 0 6" fill="#1e1e1e"/></marker>
  </defs>
  <rect width="960" height="280" fill="#abbab9"/>
  <g stroke="rgba(30,30,30,.75)" stroke-width="1"><path d="M 26,38 V 26 H 38" fill="none"/><path d="M 922,26 H 934 V 38" fill="none"/></g>
  <rect x="404" y="30" width="152" height="22" fill="#1e1e1e"/>
  <text x="480" y="45" font-family="'PT Mono', Menlo, monospace" font-size="11" fill="#fefefe" text-anchor="middle">COMPANY NEWS · 15.09.2026</text>
  <path d="M 60,158 H 240" fill="none" stroke="#1e1e1e" stroke-width="1.4" marker-end="url(#ts-a-ink)"/>
  <text x="150" y="146" font-family="'PT Mono', Menlo, monospace" font-size="12" fill="rgba(30,30,30,.8)" text-anchor="middle">состояние</text>
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
  <text x="808" y="146" font-family="'PT Mono', Menlo, monospace" font-size="12" fill="rgba(30,30,30,.8)" text-anchor="middle">решения</text>
  <text x="808" y="180" font-family="'PT Mono', Menlo, monospace" font-size="11" fill="rgba(30,30,30,.6)" text-anchor="middle">typed, с вероятностями</text>
</svg>
</div>

## Что такое System One

Название отсылает к Канеману (Daniel Kahneman) и книге «Думай медленно… решай быстро». Система 1 (System 1) там отвечает за быстрое интуитивное узнавание, Система 2 (System 2) за медленное рассуждение. Чат-боты и копилоты построены вокруг Системы 2: модель рассуждает, перебирает варианты и объясняет. TypeSafe сделали ставку на Систему 1: модель, которая узнаёт ответ сразу и отдаёт его как вызов функции.

Формула из анонса: неструктурированное состояние на входе, типизированные вероятностные решения на выходе. Между входом и выходом нет ни одного сгенерированного токена.

Для софта это меняет всё. Текст надо парсить, валидировать и перепроверять, потому что модель может выдумать поле или отказаться отвечать. Значение с типом из заранее описанной схемы нельзя неправильно распарсить: несовпадение со схемой исключено устройством выхода. Отсюда их самое сильное заявление: Jev не допускает ошибок типов, и опровергнуть это можно было бы одним контрпримером.

## Чем Jev отличается от LLM

<div class="ts-tablewrap">
<table class="ts-table">
<thead>
<tr><th></th><th>Существующие LLM</th><th>System One + Jev</th></tr>
</thead>
<tbody>
<tr><td class="rowlabel">Обучение</td><td>RLHF (предпочтения людей) и RLVR (проверяемые награды)</td><td>RLCD: Reinforcement Learning for Calibrated Decisions, награда за калиброванную уверенность</td></tr>
<tr><td class="rowlabel">Выход</td><td>Строки: ответы, код, отказы, галлюцинации. Нужны парсинг и валидация</td><td>Значения с типами из схемы, каждое с вероятностью и оценкой уверенности</td></tr>
<tr><td class="rowlabel">Сэмплирование</td><td>Последовательное, по токену</td><td>Параллельное: все поля ответа одним запросом</td></tr>
<tr><td class="rowlabel">Цена</td><td>Вход от $0,20 до $10 за MTok, выход примерно в 5 раз дороже</td><td>Вход $0,042 за MTok, выход бесплатный</td></tr>
<tr><td class="rowlabel">Задержка</td><td>3–329 секунд у фронтирных моделей</td><td>70–500 мс</td></tr>
<tr><td class="rowlabel">Уверенность</td><td>Склонна к переоценке: если точность 95%, модель молчит об остальных 5%</td><td>Калибрована: выше уверенность, выше точность; одинаковые входы дают похожие ответы</td></tr>
</tbody>
</table>
</div>

<p class="ts-cap">Сокращённая версия их сравнительной таблицы; полная с формулировками про использование и сценарии есть в оригинальном анонсе.</p>

## Откуда цифры 193,6× и 444,6×

На главной странице TypeSafe пишет про 193,6× быстрее и 444,6× дешевле. Методика за этими числами интереснее самих чисел.

Они не сравнивают «вопрос в чате, ответ в тексте». Каждая задача оформлена как воркфлоу: граф вычислений в коде, где много независимых вопросов с вероятностными ответами. Эталоном служит не правильный ответ из учебника, а среднее предсказание крупнейших внешних моделей, на момент публикации GPT-6 Astra и Fable 5.1. Каждую модель меряют против этого эталона: точность, цена, задержка.

<figure class="ts-fig">
<svg viewBox="0 0 960 316" role="img" aria-labelledby="ts-num-t ts-num-d" xmlns="http://www.w3.org/2000/svg">
  <title id="ts-num-t">Задержка и цена: фронтирные LLM против Jev</title>
  <desc id="ts-num-d">Две панели. Задержка end-to-end: у фронтирных LLM от 3 до 329 секунд, у Jev от 70 до 500 миллисекунд. Цена входных токенов: у LLM от 0,20 до 10 долларов за миллион, у Jev 0,042 доллара за миллион, выходные токены бесплатны.</desc>
  <rect width="960" height="316" fill="#f8fafc"/>
  <text x="40" y="44" font-family="'PT Mono', Menlo, monospace" font-size="12" fill="rgba(30,30,30,.6)" letter-spacing="0.1em">ЗАДЕРЖКА END-TO-END · СХЕМАТИЧНО</text>
  <text x="40" y="86" font-family="'PT Mono', Menlo, monospace" font-size="12" fill="#1e1e1e">фронтирные LLM</text>
  <rect x="40" y="98" width="380" height="36" fill="rgba(30,30,30,.8)"/>
  <text x="408" y="121" font-family="'PT Mono', Menlo, monospace" font-size="14" fill="#fefefe" text-anchor="end">3–329 с</text>
  <text x="40" y="176" font-family="'PT Mono', Menlo, monospace" font-size="12" fill="#1e1e1e">TypeSafe Jev</text>
  <rect x="40" y="188" width="12" height="36" fill="#03aa5c"/>
  <text x="64" y="211" font-family="'PT Mono', Menlo, monospace" font-size="14" fill="#1e1e1e">70–500 мс</text>
  <text x="40" y="262" font-family="'PT Mono', Menlo, monospace" font-size="11" fill="rgba(30,30,30,.55)">полосы не в масштабе: разница до трёх порядков</text>
  <line x1="480" y1="30" x2="480" y2="286" stroke="rgba(30,30,30,.15)" stroke-width="1"/>
  <text x="520" y="44" font-family="'PT Mono', Menlo, monospace" font-size="12" fill="rgba(30,30,30,.6)" letter-spacing="0.1em">ЦЕНА · ВХОДНЫЕ ТОКЕНЫ, $ / MTOK</text>
  <text x="520" y="86" font-family="'PT Mono', Menlo, monospace" font-size="12" fill="#1e1e1e">LLM</text>
  <rect x="520" y="98" width="360" height="36" fill="rgba(30,30,30,.8)"/>
  <text x="868" y="121" font-family="'PT Mono', Menlo, monospace" font-size="14" fill="#fefefe" text-anchor="end">$0,20–10</text>
  <text x="520" y="176" font-family="'PT Mono', Menlo, monospace" font-size="12" fill="#1e1e1e">TypeSafe Jev</text>
  <rect x="520" y="188" width="8" height="36" fill="#03aa5c"/>
  <text x="540" y="211" font-family="'PT Mono', Menlo, monospace" font-size="14" fill="#1e1e1e">$0,042</text>
  <text x="520" y="262" font-family="'PT Mono', Menlo, monospace" font-size="11" fill="rgba(30,30,30,.55)">выходные токены: у LLM примерно в 5 раз дороже входа, у Jev бесплатно</text>
</svg>
<figcaption class="ts-cap">Диапазоны из анонса TypeSafe. Полосы нарисованы схематично: в реальном масштабе полоса Jev была бы толщиной с линию.</figcaption>
</figure>

К этим цифрам есть вопросы, и TypeSafe сама их называет. Воркфлоу готовила их же команда model capabilities, так что систематическая ошибка возможна. Референс считается по среднему двух моделей OpenAI и Anthropic, что занижает результат самой TypeSafe и DeepSeek. Прогоны делались с ноутбуков на западном побережье США, где сейчас живёт их сервис. Заявленные множители они называют верхней границей реального выигрыша.

Даже с поправками порядок разумный. Задача, на которую фронтирная LLM тратит полминуты, у Jev занимает доли секунды. На потоке в тысячи решений в час это граница между «проверить руками» и «встроить в продакшн».

## Где такие модели нужны

Самое полезное в анонсе: список мест в коде, где вероятностное решение заменяет хрупкую логику. Я собрал их в одну схему.

<figure class="ts-fig">
<svg viewBox="0 0 960 560" role="img" aria-labelledby="ts-diag-t ts-diag-d" xmlns="http://www.w3.org/2000/svg">
  <title id="ts-diag-t">Вызов Jev внутри обычного кода</title>
  <desc id="ts-diag-d">Состояние программы поступает в Jev, модель параллельно возвращает типизированные вероятностные решения. Ниже четыре точки применения: выбор следующего инструмента в агентском цикле, развилка выполнения, оценка срочности и риска до действия, проверка выходов модели и ограждения.</desc>
  <defs>
    <marker id="ts-d-ink" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0, 8 3, 0 6" fill="#1e1e1e"/></marker>
    <marker id="ts-d-green" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0, 8 3, 0 6" fill="#03aa5c"/></marker>
  </defs>
  <rect width="960" height="504" fill="#f8fafc"/>
  <rect x="40" y="64" width="210" height="96" rx="6" fill="#ffffff" stroke="#1e1e1e" stroke-width="1"/>
  <rect x="48" y="72" width="52" height="14" rx="2" fill="rgba(30,30,30,.07)" stroke="rgba(30,30,30,.35)" stroke-width="0.8"/>
  <text x="74" y="83" fill="#1e1e1e" font-size="9" font-family="'PT Mono', Menlo, monospace" text-anchor="middle" letter-spacing="0.08em">ВХОД</text>
  <text x="145" y="120" fill="#1e1e1e" font-size="14" font-weight="600" font-family="'Host Grotesk', system-ui, sans-serif" text-anchor="middle">Состояние программы</text>
  <text x="145" y="140" fill="#64748b" font-size="10" font-family="'PT Mono', Menlo, monospace" text-anchor="middle">неструктурированный текст</text>
  <path d="M 250,112 H 352" fill="none" stroke="#1e1e1e" stroke-width="1.2" marker-end="url(#ts-d-ink)"/>
  <rect x="273" y="97" width="56" height="13" rx="2" fill="#f8fafc"/>
  <text x="301" y="107" fill="#64748b" font-size="9" font-family="'PT Mono', Menlo, monospace" text-anchor="middle" letter-spacing="0.08em">STATE</text>
  <rect x="360" y="52" width="240" height="120" rx="6" fill="#ffffff" stroke="#03aa5c" stroke-width="1.4"/>
  <rect x="372" y="60" width="116" height="14" rx="2" fill="rgba(3,170,92,0.09)" stroke="rgba(3,170,92,0.45)" stroke-width="0.8"/>
  <text x="430" y="71" fill="#03aa5c" font-size="9" font-family="'PT Mono', Menlo, monospace" text-anchor="middle" letter-spacing="0.08em">SYSTEM ONE · RLCD</text>
  <text x="480" y="102" fill="#1e1e1e" font-size="17" font-weight="600" font-family="'Host Grotesk', system-ui, sans-serif" text-anchor="middle">Jev</text>
  <text x="480" y="124" fill="#475569" font-size="10" font-family="'PT Mono', Menlo, monospace" text-anchor="middle">типизированные вероятностные решения</text>
  <rect x="376" y="136" width="104" height="17" rx="3" fill="rgba(3,170,92,0.09)" stroke="rgba(3,170,92,0.45)" stroke-width="0.8"/>
  <text x="428" y="148" fill="#03aa5c" font-size="9" font-family="'PT Mono', Menlo, monospace" text-anchor="middle">193,6× быстрее</text>
  <rect x="488" y="136" width="104" height="17" rx="3" fill="rgba(3,170,92,0.09)" stroke="rgba(3,170,92,0.45)" stroke-width="0.8"/>
  <text x="540" y="148" fill="#03aa5c" font-size="9" font-family="'PT Mono', Menlo, monospace" text-anchor="middle">444,6× дешевле</text>
  <path d="M 600,112 H 702" fill="none" stroke="#1e1e1e" stroke-width="1.2" marker-end="url(#ts-d-ink)"/>
  <rect x="625" y="97" width="52" height="13" rx="2" fill="#f8fafc"/>
  <text x="651" y="107" fill="#64748b" font-size="9" font-family="'PT Mono', Menlo, monospace" text-anchor="middle" letter-spacing="0.08em">DECISION</text>
  <rect x="710" y="64" width="210" height="96" rx="6" fill="#ffffff" stroke="#1e1e1e" stroke-width="1"/>
  <rect x="718" y="72" width="58" height="14" rx="2" fill="rgba(30,30,30,.07)" stroke="rgba(30,30,30,.35)" stroke-width="0.8"/>
  <text x="747" y="83" fill="#1e1e1e" font-size="9" font-family="'PT Mono', Menlo, monospace" text-anchor="middle" letter-spacing="0.08em">ВЫХОД</text>
  <text x="815" y="120" fill="#1e1e1e" font-size="14" font-weight="600" font-family="'Host Grotesk', system-ui, sans-serif" text-anchor="middle">Решение и вероятность</text>
  <text x="815" y="140" fill="#64748b" font-size="10" font-family="'PT Mono', Menlo, monospace" text-anchor="middle">структурированный выход, conf</text>
  <path d="M 480,172 V 202" fill="none" stroke="#03aa5c" stroke-width="1.2"/>
  <path d="M 480,202 H 168 Q 160,202 160,210 V 264" fill="none" stroke="#03aa5c" stroke-width="1.2" marker-end="url(#ts-d-green)"/>
  <path d="M 480,202 H 381 Q 373,202 373,210 V 264" fill="none" stroke="#03aa5c" stroke-width="1.2" marker-end="url(#ts-d-green)"/>
  <path d="M 480,202 H 578 Q 586,202 586,210 V 264" fill="none" stroke="#03aa5c" stroke-width="1.2" marker-end="url(#ts-d-green)"/>
  <path d="M 480,202 H 791 Q 799,202 799,210 V 264" fill="none" stroke="#03aa5c" stroke-width="1.2" marker-end="url(#ts-d-green)"/>
  <rect x="40" y="232" width="880" height="228" rx="8" fill="rgba(30,30,30,0.025)" stroke="rgba(30,30,30,0.12)" stroke-width="0.8"/>
  <rect x="52" y="225" width="196" height="14" rx="2" fill="#f8fafc"/>
  <text x="60" y="236" fill="rgba(30,30,30,0.5)" font-size="9" font-family="'PT Mono', Menlo, monospace" text-anchor="start" letter-spacing="0.12em">ТОЧКИ РЕШЕНИЙ В ОБЫЧНОМ КОДЕ</text>
  <rect x="62" y="272" width="196" height="150" rx="6" fill="#ffffff" stroke="#1e1e1e" stroke-width="1"/>
  <rect x="74" y="284" width="28" height="14" rx="2" fill="rgba(3,170,92,0.09)" stroke="rgba(3,170,92,0.45)" stroke-width="0.8"/>
  <text x="88" y="295" fill="#03aa5c" font-size="9" font-family="'PT Mono', Menlo, monospace" text-anchor="middle">01</text>
  <text x="78" y="326" fill="#1e1e1e" font-size="13" font-weight="600" font-family="'Host Grotesk', system-ui, sans-serif">Следующий инструмент</text>
  <text x="78" y="350" fill="#475569" font-size="10" font-family="'PT Mono', Menlo, monospace">какой тул или субагент</text>
  <text x="78" y="366" fill="#475569" font-size="10" font-family="'PT Mono', Menlo, monospace">взять в цикле агента</text>
  <rect x="275" y="272" width="196" height="150" rx="6" fill="#ffffff" stroke="#1e1e1e" stroke-width="1"/>
  <rect x="287" y="284" width="28" height="14" rx="2" fill="rgba(3,170,92,0.09)" stroke="rgba(3,170,92,0.45)" stroke-width="0.8"/>
  <text x="301" y="295" fill="#03aa5c" font-size="9" font-family="'PT Mono', Menlo, monospace" text-anchor="middle">02</text>
  <text x="291" y="326" fill="#1e1e1e" font-size="13" font-weight="600" font-family="'Host Grotesk', system-ui, sans-serif">Развилка выполнения</text>
  <text x="291" y="350" fill="#475569" font-size="10" font-family="'PT Mono', Menlo, monospace">продолжить, повторить,</text>
  <text x="291" y="366" fill="#475569" font-size="10" font-family="'PT Mono', Menlo, monospace">спросить человека, стоп</text>
  <rect x="488" y="272" width="196" height="150" rx="6" fill="#ffffff" stroke="#1e1e1e" stroke-width="1"/>
  <rect x="500" y="284" width="28" height="14" rx="2" fill="rgba(3,170,92,0.09)" stroke="rgba(3,170,92,0.45)" stroke-width="0.8"/>
  <text x="514" y="295" fill="#03aa5c" font-size="9" font-family="'PT Mono', Menlo, monospace" text-anchor="middle">03</text>
  <text x="504" y="326" fill="#1e1e1e" font-size="13" font-weight="600" font-family="'Host Grotesk', system-ui, sans-serif">Оценка до действия</text>
  <text x="504" y="350" fill="#475569" font-size="10" font-family="'PT Mono', Menlo, monospace">срочность и риск шага</text>
  <text x="504" y="366" fill="#475569" font-size="10" font-family="'PT Mono', Menlo, monospace">до его выполнения</text>
  <rect x="701" y="272" width="196" height="150" rx="6" fill="#ffffff" stroke="#1e1e1e" stroke-width="1"/>
  <rect x="713" y="284" width="28" height="14" rx="2" fill="rgba(3,170,92,0.09)" stroke="rgba(3,170,92,0.45)" stroke-width="0.8"/>
  <text x="727" y="295" fill="#03aa5c" font-size="9" font-family="'PT Mono', Menlo, monospace" text-anchor="middle">04</text>
  <text x="717" y="326" fill="#1e1e1e" font-size="13" font-weight="600" font-family="'Host Grotesk', system-ui, sans-serif">Проверка выходов</text>
  <text x="717" y="350" fill="#475569" font-size="10" font-family="'PT Mono', Menlo, monospace">скоринг и ограждения для</text>
  <text x="717" y="366" fill="#475569" font-size="10" font-family="'PT Mono', Menlo, monospace">ответов и промптов модели</text>
  <text x="40" y="540" fill="#475569" font-size="9" font-family="'PT Mono', Menlo, monospace" letter-spacing="0.12em">ЛЕГЕНДА</text>
  <rect x="116" y="530" width="14" height="12" rx="2" fill="#ffffff" stroke="#03aa5c" stroke-width="1"/>
  <text x="138" y="540" fill="#475569" font-size="9" font-family="'PT Mono', Menlo, monospace">модель Jev</text>
  <rect x="234" y="530" width="14" height="12" rx="2" fill="#ffffff" stroke="#1e1e1e" stroke-width="1"/>
  <text x="256" y="540" fill="#475569" font-size="9" font-family="'PT Mono', Menlo, monospace">точка решения в коде</text>
  <rect x="412" y="530" width="14" height="12" rx="2" fill="rgba(3,170,92,0.09)" stroke="rgba(3,170,92,0.45)" stroke-width="0.8"/>
  <text x="434" y="540" fill="#475569" font-size="9" font-family="'PT Mono', Menlo, monospace">заявленный выигрыш из workflow evals</text>
  <path d="M 668,536 H 682" fill="none" stroke="#1e1e1e" stroke-width="1.2" marker-end="url(#ts-d-ink)"/>
  <text x="696" y="540" fill="#475569" font-size="9" font-family="'PT Mono', Menlo, monospace">поток данных</text>
  <path d="M 812,536 H 826" fill="none" stroke="#03aa5c" stroke-width="1.2" marker-end="url(#ts-d-green)"/>
  <text x="840" y="540" fill="#475569" font-size="9" font-family="'PT Mono', Menlo, monospace">развилки решений</text>
</svg>
<figcaption class="ts-cap">Вызов Jev внутри обычного кода: состояние на входе, решения с вероятностями на выходе. Четыре развилки внизу TypeSafe называет типовыми сценариями; полный список с примерами лежит в их документации.</figcaption>
</figure>

Экономика здесь ключевая. В их демо Doom бот делает десять запросов в секунду, и это обходится примерно в семь долларов в час. Когда каждое решение стоит копейки, модель можно вызывать на каждом шаге программы, а не в двух местах ради экономии.

## Что уже показали сторонние проверки

За первые дни модель обкатывали не только авторы, и результаты совпадают с их обещаниями. В тесте проверки команд для fx Jev отвечала медианно за 312 мс против 1458 мс у GPT-5.6 Luna и ошибалась реже: 207 верных решений из 210 против 203. Выборка скромная, 70 команд по три повтора, но направление то же.

Browser Use собрали [Jev Ultrafast](https://github.com/browser-use/jev-ultrafast): страница разбита на короткие решения, Jev выбирает действие, генерация текста остаётся за обычной моделью. В показанном прогоне агент нашёл рейсы из Цюриха в Лондон за 7,1 секунды. Ранние проекты с открытым кодом собирают в каталоге [awesome-jev](https://github.com/AnotiaWang/awesome-jev): проверка кода, поиск по смыслу, детект секретов, роутинг моделей. Гильермо Рауч рассматривает Jev как нового кандидата на проверку команд по умолчанию в Vercel.

Подключить модель можно уже сейчас: она лежит в [Vercel AI Gateway](https://vercel.com/ai-gateway/models/jev) под именем `typesafe-ai/jev`, плюс собственный API TypeSafe.

## Что остаётся открытым

Выборки сторонних тестов пока маленькие: 70 команд у fx, один сценарий у Browser Use с опубликованной методикой и ограничениями.

Гарантия «без галлюцинаций» покрывает схему и типы: модель не может выдать значение не того типа или поле вне схемы. Смысловая ошибка с идеальным форматом остаётся возможной, поэтому калиброванные вероятности рядом с каждым ответом важнее самого запрета. TypeSafe сами перечисляют слабые места: вычисления, даты, косвенные указания, задачи из нескольких зависимых шагов.

Стандартной публичной бенчмарк-таблицы у TypeSafe нет принципиально: они считают, что публичные таблицы ломают стимулы, и обещают разовые оценки к каждому обновлению. Сторонние замеры вроде fx-теста это компенсируют, но проверять на своих задачах всё равно придётся самим.

Цена вызывает вопросы у них же самих. $0,042 за миллион входных токенов и бесплатные выходные, с прямой оговоркой: доказать, что это не субсидия, они пока не могут.

## Что с этим делать

В [разборе голосового браузера на Jev](/blog/jev-voice-browser/) показан полный путь решения: состояние страницы, варианты действий, вероятности и проверки перед кликом. Там есть открытая реализация, схемы и скриншоты собственных проверок.

Если в твоём коде решения принимаются хрупкими if-ами поверх текста LLM, это ровно их кейс. Выпиши такие места, выбери то, где решение повторяется много раз в час, и проверь Jev на своём воркфлоу. Документация с картой сценариев открыта, workflow evals показывают примеры и расхождения моделей между собой.

Я сверстал реплику их анонса и понял главный тезис не из текста, а из таблицы: это ставка, что следующий шаг автоматизации делается через другой интерфейс ответа. Не через более умный текст, а через решения с типами и вероятностями. Похоже на правду; проверяется цифрами на твоих задачах.
