---
title: "TypeSafe выпустила Jev: модель ИИ для выбора действий"
date: 2026-09-17
description: "TypeSafe выпустила Jev. Как модель помогает распределять обращения, управлять действиями помощника и проверять результат. Попробовать можно в Telegram."
tags: ["ИИ", "автоматизация", "агенты"]
image: /images/blog/typesafe-system-one-jev-general-reader.png
intro: "TypeSafe выпустила Jev: модель ИИ, которая выбирает действие из заданных вариантов и оценивает ситуацию. Она помогает распределять обращения и выбирать следующие шаги в играх и помощниках."
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
  .ts-fig.ts-story svg { min-width: 0; }
}
</style>

15 сентября 2026 года [TypeSafe представила Jev](https://typesafe.ai/blog/introducing-system-one-models-and-jev), модель искусственного интеллекта для выбора действий и оценки ситуаций. Она может определить, кому передать обращение клиента, какое действие предложить помощнику или когда нужна проверка человеком. Модель выбирает из заданных вариантов и может учитывать относящуюся к вопросу историю.

Для компаний смысл такого подхода в [повторяющихся решениях](https://docs.typesafe.ai/concepts/use-case-map): распределении запросов, оценке срочности, проверке работы автоматических помощников. Попробовать Jev можно в нашем [Telegram-боте @jev_robot](https://t.me/jev_robot), без установки программ и собственного ключа доступа.

<span id="jev-получает-состояние-программы-и-вопросы"></span>
## Как Jev разбирается с обращением клиента

Представь сообщение: «Платёж не проходит третий день». Компания может поручить [Jev распределение обращений](https://docs.typesafe.ai/concepts/use-case-map). Команда сервиса заранее задаёт три отдела: поддержка, продажи, платежи. Сообщение клиента становится входом для модели; вопрос звучит так: кому его передать?

[Jev сравнивает текст с заданными вариантами](https://docs.typesafe.ai/primitives/choice) и возвращает выбранный отдел вместе с вероятностями вариантов. После этого приложение может направить обращение соответствующему сотруднику. Сотрудник проверяет проблему и занимается её решением. Цель и правила задаёт команда компании, выбор предлагает модель, передачу выполняет программа.

Принцип распространяется на [другие вопросы](https://docs.typesafe.ai/api). Можно оценить срочность обращения по заданной шкале или спросить, сообщает ли человек о серьёзной проблеме. Для решения могут понадобиться история переписки, сведения о заказе и действующие правила. Объём и состав информации зависят от задачи; нужные связи и доказательства должны сохраниться.

<figure class="ts-fig ts-story">
<svg viewBox="0 0 640 620" role="img" aria-labelledby="ts-diag-t ts-diag-d" xmlns="http://www.w3.org/2000/svg">
<title id="ts-diag-t">Как обращение клиента проходит от Jev к сотруднику</title>
<desc id="ts-diag-d">Текст обращения поступает в Jev. Модель сравнивает три заданных отдела, возвращает выбор и вероятности. Приложение передаёт обращение, сотрудник проверяет вопрос. Отделы и правила задаёт команда сервиса.</desc>
<defs><marker id="ts-d-ink" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0, 8 3, 0 6" fill="#1e1e1e"/></marker></defs>
<rect width="640" height="620" fill="#f8fafc"/>
<rect x="80" y="20" width="480" height="90" rx="8" fill="#fff" stroke="#1e1e1e"/>
<text x="320" y="55" font-family="system-ui, sans-serif" text-anchor="middle" fill="#1e1e1e" font-size="28" font-weight="600">Обращение</text>
<text x="320" y="86" font-family="system-ui, sans-serif" text-anchor="middle" fill="#475569" font-size="25">«Платёж не проходит»</text>
<path d="M320 110V134" stroke="#1e1e1e" stroke-width="2" marker-end="url(#ts-d-ink)"/>
<rect x="80" y="140" width="480" height="90" rx="8" fill="#fff" stroke="#1e1e1e"/>
<text x="320" y="175" font-family="system-ui, sans-serif" text-anchor="middle" fill="#1e1e1e" font-size="28" font-weight="600">Jev сравнивает</text>
<text x="320" y="206" font-family="system-ui, sans-serif" text-anchor="middle" fill="#475569" font-size="25">три заданных отдела</text>
<path d="M320 230V254" stroke="#1e1e1e" stroke-width="2" marker-end="url(#ts-d-ink)"/>
<rect x="80" y="260" width="480" height="90" rx="8" fill="#fff" stroke="#1e1e1e"/>
<text x="320" y="295" font-family="system-ui, sans-serif" text-anchor="middle" fill="#1e1e1e" font-size="28" font-weight="600">Выбор отдела</text>
<text x="320" y="326" font-family="system-ui, sans-serif" text-anchor="middle" fill="#475569" font-size="25">с вероятностями вариантов</text>
<path d="M320 350V374" stroke="#1e1e1e" stroke-width="2" marker-end="url(#ts-d-ink)"/>
<rect x="80" y="380" width="480" height="90" rx="8" fill="#fff" stroke="#1e1e1e"/>
<text x="320" y="415" font-family="system-ui, sans-serif" text-anchor="middle" fill="#1e1e1e" font-size="28" font-weight="600">Приложение</text>
<text x="320" y="446" font-family="system-ui, sans-serif" text-anchor="middle" fill="#475569" font-size="25">передаёт обращение</text>
<path d="M320 470V494" stroke="#1e1e1e" stroke-width="2" marker-end="url(#ts-d-ink)"/>
<rect x="80" y="500" width="480" height="90" rx="8" fill="#fff" stroke="#1e1e1e"/>
<text x="320" y="535" font-family="system-ui, sans-serif" text-anchor="middle" fill="#1e1e1e" font-size="28" font-weight="600">Сотрудник</text>
<text x="320" y="566" font-family="system-ui, sans-serif" text-anchor="middle" fill="#475569" font-size="25">проверяет вопрос</text>
</svg>
<figcaption class="ts-cap">В <a href="https://docs.typesafe.ai/concepts/use-case-map">распределении обращений</a> команда сервиса задаёт отделы и правила. Jev предлагает выбор, приложение передаёт обращение, сотрудник проверяет вопрос.</figcaption>
</figure>

<span id="заданный-тип-ответа-помогает-коду-правильность-проверяется-отдельно"></span>
## Выбор из списка тоже бывает ошибочным

[TypeSafe гарантирует ответ в заданной форме](https://typesafe.ai/blog/introducing-system-one-models-and-jev): например, один из разрешённых отделов. При этом сообщение о неудачном платеже может попасть в продажи. Сотрудник получит обращение, которое ему не предназначалось, и помощь задержится. Правильность выбора требуется проверять отдельно.

[Вероятности показывают оценку модели](https://docs.typesafe.ai/confidence). Высокая уверенность не освобождает от проверки: [TypeSafe прямо предупреждает](https://docs.typesafe.ai/concepts/system-one), что оценка надёжности на группе примеров не гарантирует отдельного ответа. Важны реальные ошибки на тех обращениях, с которыми работает сервис.

[Для рискованных действий](https://docs.typesafe.ai/confidence) можно предусмотреть подтверждение человеком: например, перед отправкой письма или необратимым изменением данных. Если сведений мало, их нужно получить; сложный случай приложение может передать другой модели или человеку. Такой порядок задают создатели приложения.

<span id="почему-проверке-агента-нужен-контекст-всей-работы"></span>
## Как проверить, что помощник действительно выполнил просьбу

ИИ-помощник может выполнять действия в программах: искать информацию, готовить сообщения, пользоваться браузером. [TypeSafe предлагает проверять результаты такой работы](https://evals.typesafe.ai/agent_trace_observability). Обещание «письмо отправлено» само по себе ещё не подтверждает отправку.

Допустим, человек попросил отправить письмо. Для [проверки этого действия](https://raw.githubusercontent.com/typesafe-ai/skills/main/skills/typesafe-ai/SKILL.md) нужны просьба, разрешение на отправку, адресат и ответ почтовой программы. Помощник готовит текст и предлагает действие; почтовая программа выполняет отправку по правилам приложения. Jev может оценить собранные сведения, а программа решит, закрыть задачу или передать её человеку.

В [проверке TypeSafe](https://evals.typesafe.ai/agent_trace_observability) отдельно оцениваются разрешения, выполнение задачи и удовлетворённость пользователя. Это разные вещи: действие может состояться, а человек остаться недоволен. Программе нужна относящаяся к вопросу история работы. Когда необходимой информации нет, успешный результат считать подтверждённым нельзя.

<span id="применение-начинается-с-повторяющегося-выбора"></span>
## Что уже показали в играх и браузере

В [демонстрации Doom команды TypeSafe](https://x.com/CompleteSkeptic/status/2099925687465570372) Jev выбирает, что делать дальше в игре. Программа передаёт описание происходящего текстом, модель выбирает действие, игровая программа его исполняет. Изменившаяся ситуация становится следующим входом. Работа с изображением игрового экрана этим демо не показана.

<figure>
<video controls playsinline preload="metadata" style="display:block;width:100%;height:auto" aria-label="Оригинальная демонстрация Jev в Doom от TypeSafe">
<source src="/images/blog/typesafe-system-one-jev/doom-original.mp4" type="video/mp4">
<a href="https://x.com/CompleteSkeptic/status/2099925687465570372">Видео Jev в Doom от TypeSafe</a>
</video>
<figcaption class="ts-cap"><a href="https://x.com/CompleteSkeptic/status/2099925687465570372">TypeSafe / Diogo Almeida, 15 сентября</a>: Jev выбирает действия по текстовому описанию происходящего в Doom. Полная исходная запись.</figcaption>
</figure>

[Авторы Doom-демо](https://x.com/CompleteSkeptic/status/2099925687465570372) оценивают темп в десять обращений к модели в секунду и расходы примерно в семь долларов в час. Это оценка их сценария: размер отправляемого текста, частота действий и дополнительные расходы меняют стоимость.

В [Wikiracing команды TypeSafe](https://x.com/CompleteSkeptic/status/2099925688925184171) задача состоит в переходе от одной статьи Wikipedia к другой по ссылкам. Jev выбирает следующую ссылку, программа открывает страницу, затем выбор повторяется. Самый короткий маршрут не гарантирован; опубликованный таймер исключает загрузку страниц.

В [демо Browser Use](https://github.com/browser-use/jev-ultrafast/blob/main/docs/performance.md) программа искала рейсы Цюрих → Лондон. Jev выбирала действие и элемент страницы. Названия городов для заполнения полей генерировала другая модель, Mercury; действия в браузере выполняла программа. Авторы сообщают о 7,073 секунды, но таймер начинается после первого наблюдения страницы. Начальная навигация и независимая проверка результата не входят в это время; билеты не покупались.

В [голосовом браузере](/blog/jev-voice-browser/) Jev выбирает действие по распознанной команде и подписям элементов страницы.

<span id="первые-проверки-имеют-собственные-условия"></span>
## Насколько убедительны первые результаты

В [одном из первых опубликованных тестов](https://x.com/fazxes/status/2100300097695232164) команда сервиса fx сравнивала, как Jev и GPT-5.6 Luna оценивают безопасность команд автоматического помощника перед выполнением. Типичный ответ Jev занимал около 0,3 секунды, Luna отвечала примерно за 1,5 секунды. Jev в этом сравнении ошибалась реже; ошибки были у обеих моделей. Результат относится к этим примерам и условиям проверки.

[TypeSafe также публикует собственные тесты](https://evals.typesafe.ai/) обработки счетов, поддержки клиентов и других процессов. Ориентир для правильных ответов получен с помощью двух сильных ИИ-моделей. Их согласие не заменяет независимую проверку человеком. Подробности сравнения важны при оценке рекламируемых показателей скорости и цены.

[Документация Jev](https://docs.typesafe.ai/model-jaggedness/jev-1.13) перечисляет ошибки с математикой, датами, косвенными связями и противоречивыми условиями. Лишние сведения тоже могут мешать. Если несколько решений зависят друг от друга, проверять нужно весь путь и последствия неверного шага.

<span id="у-модели-есть-ограничения-у-цены-есть-дата"></span>
## Сколько стоит использование

[Цена TypeSafe](https://docs.typesafe.ai/models) на 17 сентября: $0,042 за миллион входных токенов, выход бесплатный. Токеном называют фрагмент текста, иногда часть слова. Поэтому расход зависит от объёма информации, переданной модели, и количества обращений. Из этого тарифа нельзя вывести цену одной произвольной проверки.

Для подключения через посредника Vercel [карточка Gateway](https://vercel.com/ai-gateway/models/jev) показывает $0,04 за миллион входных токенов; цена выхода там не указана. Другие модели в приложении оплачиваются отдельно. [TypeSafe](https://typesafe.ai/blog/introducing-system-one-models-and-jev) допускает субсидирование своего тарифа; его устойчивость не установлена.

<span id="попробовать-в-telegram-без-установки"></span>
## Как попробовать самому

Открой [наш @jev_robot в Telegram](https://t.me/jev_robot) и нажми Start → «Разобрать пример». Сначала бот показывает задачу, условия и иллюстрацию. Кнопка «Проверить пример · 1 запрос» отправляет вопрос модели.

В карточке «Какую кнопку выбрать?» [бот](https://t.me/jev_robot) предлагает команду «открой документацию» и три элемента страницы: «Документация», «Войти», «Поиск». Команде соответствует ссылка «Документация». Модель возвращает свой выбор и вероятности вариантов; сравни ответ с этой целью. Бот показывает решение, браузерную кнопку он не нажимает.

Через [«Проверить мою задачу»](https://t.me/jev_robot) можно заменить исходный текст и посмотреть новый ответ при тех же условиях. «Все примеры» содержит пять учебных карточек: выбор кнопки, проверку команды помощника, режим модели, поиск функции по смыслу и риск изменения кода. Для собственного вопроса доступны выбор вариантов, оценка по шкале и да/нет. Эти проверки работают с текстовыми описаниями; бот не исполняет команды и не переключает модели.

На 17 сентября [проба в боте](https://t.me/jev_robot) бесплатная в пределах 20 запросов в сутки по UTC, со сбросом в 03:00 по Москве. Собственный ключ доступа не нужен. Просмотр карточек и сохранённого ответа квоту не расходует; обращение к модели списывает один запрос. Между запросами нужны десять секунд, текст ограничен 3000 символами. Доступ зависит от бюджета сервиса и доступности модели. Введённый текст и условия передаются через Vercel в TypeSafe; не отправляй секреты и личные данные.

Jev позволяет [добавить осмысленный выбор в программу](https://docs.typesafe.ai/concepts/use-case-map). Для пользователя важно, какие сведения получила модель, кто исполняет её решение и кто отвечает за ошибку. Начать знакомство можно с понятного примера в боте: задать цель, увидеть выбор и самостоятельно проверить, подходит ли он.

<span id="множители-typesafe-относятся-к-четырём-собственным-тестам"></span>
<details>
<summary>Подробности первых тестов и рекламируемых показателей</summary>

[Команда fx](https://x.com/fazxes/status/2100300097695232164) проверяла 70 размеченных случаев по три раза. Jev дала 207 верных решений из 210, GPT-5.6 Luna дала 203. Медиана задержки составила 312 мс против 1458 мс, около 4,7×. Повторы зависимы; маркетинговые 193,6× и 444,6× здесь не воспроизводятся.

В [анонсе TypeSafe](https://typesafe.ai/blog/introducing-system-one-models-and-jev) заявлены 193,6× ускорения и 444,6× снижения стоимости в проверках целых процессов. Знаменатель и расчёт не раскрыты. Эти результаты не устанавливают выигрыш на других задачах. Диапазон 70-500 мс также является заявлением компании о задержке вызова.

[Четыре теста](https://evals.typesafe.ai/) включают инцидент безопасности, проверку агента поддержки, обработку счёта и обслуживание клиента. График усредняет их точность, цену и время с равным весом. Ориентир для ответов получен усреднением GPT-6 Astra и Fable 5.1 с высоким уровнем размышления. Другие модели используют настройки провайдера по умолчанию и обёртку для структурированных вероятностей. Этот ориентир не задаёт базу множителей скорости и цены. TypeSafe отмечает возможное смещение собственных тестов и запуск с ноутбуков на западном побережье США.

В [Agent Trace Observability](https://evals.typesafe.ai/agent_trace_observability) есть пример, в котором все три модели расходятся с эталоном. Независимая человеческая проверка эталона требуется отдельно. [Browser Use](https://github.com/browser-use/jev-ultrafast/blob/main/docs/performance.md) ограничивает статистические выводы тремя парами прогонов. В [Wikiracing](https://x.com/CompleteSkeptic/status/2099925688925184171) более 255 ссылок требуют двухэтапного выбора.

</details>

<details>
<summary>Устройство ответов и оценка надёжности</summary>

<div class="ts-hero">
<svg viewBox="0 0 960 280" role="img" aria-labelledby="ts-hero-t ts-hero-d" xmlns="http://www.w3.org/2000/svg">
  <title id="ts-hero-t">Jev получает ситуацию и возвращает выбор</title>
  <desc id="ts-hero-d">Описание ситуации поступает в Jev. Модель возвращает выбор из заданных вариантов и вероятности.</desc>
  <defs>
    <marker id="ts-a-ink" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0, 8 3, 0 6" fill="#1e1e1e"/></marker>
  </defs>
  <rect width="960" height="280" fill="#abbab9"/>
  <g stroke="rgba(30,30,30,.75)" stroke-width="1"><path d="M 26,38 V 26 H 38" fill="none"/><path d="M 922,26 H 934 V 38" fill="none"/></g>
  <rect x="330" y="30" width="300" height="22" fill="#1e1e1e"/>
  <a href="https://typesafe.ai/blog/introducing-system-one-models-and-jev"><text x="480" y="45" font-family="'PT Mono', Menlo, monospace" font-size="18" fill="#fefefe" text-anchor="middle">АНОНС TYPESAFE · 15.09.2026</text></a>
  <path d="M 60,158 H 240" fill="none" stroke="#1e1e1e" stroke-width="1.4" marker-end="url(#ts-a-ink)"/>
  <text x="150" y="146" font-family="'PT Mono', Menlo, monospace" font-size="18" fill="rgba(30,30,30,.8)" text-anchor="middle">ситуация</text>
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

[Интерфейс TypeSafe](https://docs.typesafe.ai/api) называет входную информацию `state`, вопросы `questions`, ответы `answers`. Choice выбирает из заданных вариантов и возвращает их вероятности; Noul возвращает вероятность «да» от 0 до 1; Score вычисляет оценку по вероятностям упорядоченных уровней.

[Confidence](https://docs.typesafe.ai/confidence) у Choice и Score характеризует распределение вероятностей; Noul отдельного confidence не возвращает. [Калибровка](https://docs.typesafe.ai/concepts/system-one) проверяется на группе ответов и не гарантирует отдельного решения. Другие языковые модели тоже поддерживают заданные схемы; сравнивать нужно одинаковые задачи и настройки.

[TypeSafe](https://typesafe.ai/blog/introducing-system-one-models-and-jev) называет подход System One, а обучение RLCD: обучение с подкреплением для калиброванных решений. Опубликованный интерфейс не доказывает внутреннюю архитектуру модели.

</details>

<span id="как-попробовать-через-официальный-skill"></span>
<span id="попробовать-jev-через-ai-cli"></span>
<details>
<summary>Для создателей приложений: официальный skill и ai-cli</summary>

[TypeSafe skill](https://docs.typesafe.ai/agent-skill) даёт агенту для работы с проектом инструкции для чтения документации, постановки типизированных вопросов и интеграции Jev. В [Claude Code](https://docs.typesafe.ai/agent-skill) установка выполняется двумя командами:

```bash
claude plugin marketplace add typesafe-ai/skills
claude plugin install typesafe@typesafe-ai
```

Для [Codex и других поддерживаемых агентов](https://docs.typesafe.ai/agent-skill), с Node.js и `npx`:

```bash
npx skills add typesafe-ai/skills --skill typesafe-ai
```

Команда предлагает выбрать агента; установка по умолчанию относится к текущему проекту. В Claude Code skill вызывается `/typesafe:typesafe-ai`, в другом агенте по имени. [README](https://github.com/typesafe-ai/skills) предлагает маршрутизацию поддержки по отделам с передачей неоднозначных случаев человеку. Можно попросить агента подготовить такой сценарий на безопасном тестовом обращении. [Skill](https://raw.githubusercontent.com/typesafe-ai/skills/main/skills/typesafe-ai/SKILL.md) не запускает автоматический контроль всех действий: порядок, пороги и исполнение остаются в приложении.

Для [playground TypeSafe](https://console.typesafe.ai/playground) требуется вход. [Прямой API](https://docs.typesafe.ai/introduction/quickstart) использует ключ из [настроек](https://console.typesafe.ai/settings/keys); доступ зависит от аккаунта. [Vercel Gateway](https://vercel.com/changelog/typesafe-ai-jev-now-available-on-ai-gateway) использует свой ключ или Vercel OIDC. Установка skill не выдаёт доступ к модели; ключи этих сервисов различаются и не должны попадать в публичные промпты или код.

[Chris Tate 17 сентября](https://x.com/ctatedev/status/2100584917092409479) предложил ai-cli для обращения к Jev из терминала. [ai-cli 0.5.1](https://registry.npmjs.org/ai-cli/0.5.1) требует Node.js 22+:

```bash
npm install -g ai-cli
```

[Оценка через CLI](https://ai-cli.dev/docs/evaluate) требует `AI_GATEWAY_API_KEY`, доступа к Jev и средств Gateway; модель по умолчанию `typesafe-ai/jev`. Исходный [пример Tate](https://x.com/ctatedev/status/2100584917092409479):

```text
git diff --cached |
  ai evaluate \
    --boolean "api=Breaks the API?"
```

Команда передаёт подготовленные к коммиту изменения на Boolean-вопрос. [JSON-ответ](https://ai-cli.dev/docs/evaluate) `answers.api.probability` означает P(true). Человек или следующий код принимает дальнейшее решение; успешное завершение команды не означает безопасный коммит. Для оценки нужны достаточный API-контракт и контекст потребителей, а также тесты совместимости. Перед отправкой проверь текст на секреты и личные данные. CLI принимает также Choice и Score; стоимость зависит от входа, вопросов и [условий Gateway](https://vercel.com/ai-gateway/models/jev).

<figure>
<a href="/images/blog/typesafe-system-one-jev/ai-cli-ctatedev-original.jpg"><img src="/images/blog/typesafe-system-one-jev/ai-cli-ctatedev-original.jpg" alt="Примеры команд Chris Tate для проверки изменений программы, плана инфраструктуры и подозрительного текста" width="1080" height="1080" loading="lazy"></a>
<figcaption><a href="https://x.com/ctatedev/status/2100584917092409479">Chris Tate</a>: примеры вопросов к изменению программы, плану инфраструктуры и тексту из буфера обмена.</figcaption>
</figure>

</details>

<span id="проверка-на-своей-задаче-даёт-основание-для-внедрения"></span>
