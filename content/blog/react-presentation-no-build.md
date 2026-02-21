---
title: "React-презентация без сборки: Editorial Brutalism на CDN"
date: 2026-01-13
description: "Как сделать презентацию для курса на React без webpack и npm. Editorial Brutalism, grain-текстуры через SVG, анимации skew. Архитектура и примеры кода."
tags: ["react", "презентация"]
section: Вайбкодинг
---

Презентация для первого урока. 8й поток курса по вайбкодингу.

19 человек — дизайнеры, юристы, психолог, директор парков развлечений. PowerPoint не годился.

За вечер собрал React-презентацию с grain-текстурой и пульсирующей картой мира. Без npm.

## Почему не PowerPoint

Курс про создание вещей с помощью AI. Показывать скучные слайды — странно. Студенты сразу видят: преподаватель сам не пользуется тем, чему учит.

Хотелось grain-текстуру поверх всего. Skew при смене слайдов. Пульсирующие точки на карте — участники из 9 городов. В PowerPoint такое не соберёшь. В Keynote тоже. А в Claude Code — за час.

## React без сборки

Весь setup — три CDN-ссылки в HTML:

```html
<script src="https://unpkg.com/react@18/umd/react.development.js"></script>
<script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>
<script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
```

Babel компилирует JSX прямо в браузере. Да, это медленнее. Для презентации на 11 слайдов — без разницы.

{{< callout insight >}}
Прототипы. Демо для клиента. Презентации. Когда нужно показать через 10 минут, а не через 10 коммитов.
{{< /callout >}}

Компоненты лежат в отдельных JSX-файлах и подключаются через `type="text/babel"`:

```html
<script type="text/babel" src="components/layouts/TitleSlide.jsx"></script>
<script type="text/babel" src="components/layouts/StatsSlide.jsx"></script>
<script type="text/babel" src="components/App.jsx"></script>
```

## Архитектура: данные отдельно

Контент слайдов живёт в JS-файлах, не в компонентах. Это позволяет менять тексты без правки кода.

| Файл | Что хранит |
|------|------------|
| `data/cohort.js` | Данные о потоке: участники, города, статистика |
| `data/slides.js` | Массив слайдов с типами и контентом |
| `components/layouts/` | Компоненты для каждого типа слайда |

App.jsx — диспетчер. Смотрит на тип слайда, рендерит нужный компонент:

```javascript
const SLIDE_COMPONENTS = {
    title: TitleSlide,
    stats: StatsSlide,
    profiles: ProfilesSlide,
    list: ListSlide,
    // ...
};

const SlideComponent = SLIDE_COMPONENTS[slideConfig.type];
return <SlideComponent num={slideNum} data={slideConfig.data} />;
```

## Editorial Brutalism: что это

Не путать с обычным брутализмом — тот про сырой HTML и Comic Sans ради шока. Editorial Brutalism берёт типографику из журналов и добавляет бруталистские акценты. Вдохновлялся сайтами Bloomberg и The Outline (RIP).

Три шрифта. **Unbounded** — жирный display для заголовков, геометричный. **Cormorant Garamond** — элегантный serif для текста. И **Space Mono** для всего технического: меток, кода, счётчика слайдов.

Цвета — тёмная база с яркими акцентами:

```css
:root {
    --bg-primary: #0d0d0d;
    --text-primary: #f5f5f0;
    --accent: #ff3d00;        /* оранжевый */
    --highlight: #e8ff00;     /* жёлтый */
}
```

## Grain-текстура через SVG

Плёночный шум. Обычно для этого тащат PNG-файл. Но есть способ лучше — SVG с feTurbulence генерирует шум прямо в браузере:

```css
body::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 400 400' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
    opacity: 0.03;
    pointer-events: none;
    z-index: 9999;
}
```

`opacity: 0.03` — почти невидимо. Но убери — и сразу чувствуется, что чего-то не хватает.

## Анимация skew при переходах

Слайды появляются с перекосом в 2 градуса и выпрямляются. Мелочь, но без неё переходы кажутся плоскими:

```css
@keyframes slideIn {
    0% {
        opacity: 0;
        transform: translateY(60px) skewY(2deg);
    }
    100% {
        opacity: 1;
        transform: translateY(0) skewY(0);
    }
}
```

Секрет — `cubic-bezier(0.16, 1, 0.3, 1)`. Быстрый старт, плавное торможение.

## Карта с пульсирующими маркерами

19 участников из 9 городов — от Буэнос-Айреса до Екатеринбурга. Просто список городов — скучно. Карта — сразу понятно.

SVG с упрощёнными континентами. Города — круги с pulse-анимацией:

```javascript
const CITY_COORDS = [
    { name: 'Москва', x: 62, y: 28, count: 8 },
    { name: 'Берлин', x: 46, y: 31, count: 1 },
    { name: 'Буэнос-Айрес', x: 24, y: 82, count: 1 },
    // ...
];
```

Каждый маркер пульсирует со своей задержкой. Москва с 8 участниками — крупнее остальных:

```css
.city-marker:nth-child(1) .pulse-ring { animation-delay: 0s; }
.city-marker:nth-child(2) .pulse-ring { animation-delay: 0.15s; }
.city-marker:nth-child(3) .pulse-ring { animation-delay: 0.3s; }
/* ... */
```

## Навигация с клавиатуры

Стрелки, Space, Home/End. Без этого — не презентация:

```javascript
useEffect(() => {
    const handleKeyDown = (e) => {
        switch (e.key) {
            case 'ArrowRight':
            case ' ':
                goNext();
                break;
            case 'ArrowLeft':
                goPrev();
                break;
            case 'Home':
                goToSlide(0);
                break;
        }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
}, [goNext, goPrev]);
```

## Что получилось

11 слайдов. Запускается через `npx serve .` или любой локальный сервер. Работает в любом браузере.

Структура папок:

```
presentation/
├── index.html
├── styles/main.css
├── data/
│   ├── cohort.js
│   └── slides.js
└── components/
    ├── App.jsx
    ├── Controls.jsx
    └── layouts/
        ├── TitleSlide.jsx
        ├── StatsSlide.jsx
        └── ...
```

{{< callout warning "Ограничения" >}}
Требует локальный сервер — браузер не загрузит JSX напрямую из файловой системы. Нет hot reload. Для production нужна сборка.
{{< /callout >}}

Для курсовой презентации — хватает. Сел в 8 вечера, к 9 уже прогонял слайды.

## Источники

- [Neobrutalism: Definition and Best Practices — NN/G](https://www.nngroup.com/articles/neobrutalism/)
- [Neubrutalism — UI Design Trend — Bejamas](https://bejamas.com/blog/neubrutalism-web-design-trend)
- [@babel/standalone — Babel Documentation](https://babeljs.io/docs/babel-standalone)
- [React Without Build Tools — Jim Nielsen](https://blog.jim-nielsen.com/2020/react-without-build-tools/)
- [React via CDN: Fast, Simple, and Perfect for Prototypes](https://mediusware.com/blog/using-react-via-cdn)
