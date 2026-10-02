#!/usr/bin/env python3
"""
Builder for Variant 2: Плотный журнал (Dense Magazine Strip)
Outputs:
  - content/blog/claude-fable-5-1-v2.html (Hugo post with frontmatter)
  - static/design-review/variant-2.html (Standalone static preview)
"""

import os
import re

with open('content/blog/claude-fable-5-1.html', 'r', encoding='utf-8') as f:
    base = f.read()

with open('content/blog/claude-fable-5-1-v1.html', 'r', encoding='utf-8') as f:
    v1 = f.read()

# Frontmatter for Hugo post
hugo_frontmatter = """---
title: "Обзор Claude Fable 5.1 [Вариант 2: Плотный журнал]"
date: 2026-09-02
description: "Обзор Claude Fable 5.1: бенчмарки против Fable 5, 22 кейса партнёров, системная карта по главам, первые отзывы в X и 14 промптов из гайда Anthropic."
tags: ["anthropic", "claude-code", "claude-fable-5-1"]
keywords: ["Claude Fable 5.1", "Fable 5.1 обзор", "Fable 5.1 бенчмарки", "системная карта Fable 5.1", "промпты для Fable 5.1", "Mythos 5.1"]
section: "AI"
image: /images/blog/fable51/og.png
layout: paper
faq:
  - q: "Чем Claude Fable 5.1 отличается от Fable 5?"
    a: "Контекстное окно 1M токенов, срез знаний июнь 2026, режим extended thinking auto. В API вход $10 и выход $50 за миллион токенов, чтение кэша подешевело на 75% до $0.25 за миллион. На уровнях усилия Low и Medium модель даёт результат уровня Fable 5 дешевле."
  - q: "Где доступна Claude Fable 5.1?"
    a: "В Claude Code, Claude Cowork, claude.ai и приложениях Claude, в Cursor. Для разработчиков: Claude API, Amazon Bedrock, Google Cloud, Microsoft Foundry. Тарифы claude.ai: Pro, Max, Team, Enterprise."
  - q: "Что такое Mythos 5.1 и чем она отличается от Fable 5.1?"
    a: "У моделей одни веса и разные ограничения. Fable 5.1 доступна всем, Mythos 5.1 выдаётся проверенным организациям по программам доступа для кибербезопасности и наук о жизни, пока только в США."
  - q: "Что случилось с лимитами подписок Claude после релиза?"
    a: "Недельные лимиты подписок сбросили, до 13 сентября 2026 недельный лимит Claude Code выше обычного на 50%. Это видно на экране Usage в аккаунте Max, в анонсе этого нет. Скидка на чтение кэша действует только в API, в подписках Pro и Max лимиты считаются как раньше."
  - q: "Как промптить Fable 5.1?"
    a: "Вместе с моделью Anthropic выпустила официальный гайд по промптингу. В статье 14 промптов из гайда в оригинале, для каждого указано, куда его класть."
slug: "claude-fable-5-1-v2"
sitemap_exclude: true
robots: "noindex, nofollow"
---
<button class="theme-btn" id="themeBtn" aria-label="Переключить тему">☾</button>
"""

# Variant Switcher Navigation Bar
top_bar = """
<nav class="article-variant-switcher" aria-label="Сравнение вариантов статьи">
  <div class="avs-group">
    <span class="avs-label">Вариант:</span>
    <a href="/blog/claude-fable-5-1-v1/" class="avs-link">1. Сетка пеликанов</a>
    <a href="/blog/claude-fable-5-1-v2/" class="avs-link is-active" aria-current="page">2. Плотный журнал</a>
    <a href="/blog/claude-fable-5-1-v3/" class="avs-link">3. Бегущая стена</a>
    <a href="/blog/claude-fable-5-1/" class="avs-link" style="opacity:0.65">Было (слайдеры)</a>
  </div>
  <span class="avs-hint">Концепт 2: Плотный журнал (гравюра Anthropic и полоса пеликанов)</span>
</nav>

<div class="page"><header class="masthead">
<p class="kicker">Fable 5.1 · Релиз 1 сентября 2026</p>
<h1>Разбираю Claude Fable 5.1: бенчмарки, отзывы, системная карта и промптинг</h1>
<p class="lede">Пересказ анонса Anthropic и 22 отзыва партнёров, разложенные по типу использования модели.</p>
<p class="meta">Источники: страница релиза и системная карта Anthropic, пост Simon Willison, 33 поста в X, экран usage founder · снято <time datetime="2026-09-02">2 сентября 2026</time> · независимой проверки нет</p>
</header>
</div>
"""

# Hero Section: Two-level editorial layout
hero_magazine_html = """
<section class="mag-hero-section" aria-label="Первое впечатление: официальный арт и шкала мышления">
  <div class="mag-hero-wrap">
    
    <!-- Верхний ярус: ботаническая гравюра Anthropic -->
    <figure class="mag-hero-art">
      <div class="mag-hero-art-frame">
        <img width="671" height="672" src="/images/blog/fable51/anthropic-birds-clean.png" alt="Официальный арт релиза Claude Fable 5.1 и Claude Mythos 5.1" class="mag-hero-art-img">
      </div>
      <figcaption class="mag-hero-art-caption">
        Официальный арт релиза Claude Fable 5.1 и Claude Mythos 5.1
      </figcaption>
    </figure>

    <!-- Нижний ярус: чистая горизонтальная полоса 5 стадий пеликана Simon Willison -->
    <div class="mag-pelican-strip">
      <div class="mag-strip-header">
        <div class="mag-strip-title">Шкала мышления: тест Simon Willison «a pelican on a bicycle»</div>
        <div class="mag-strip-meta">От 23 секунд ($0.10) до 13м 54с ($3.30)</div>
      </div>
      
      <div class="mag-pelican-grid">
        <!-- Low -->
        <article class="mag-pelican-card">
          <div class="mag-card-head">
            <span class="mag-card-level">Низкий (Low)</span>
            <span class="mag-card-stat">24с · $0.10</span>
          </div>
          <div class="mag-card-media">
            <img width="914" height="686" src="/images/blog/fable51/pelikan-low.png" alt="Пеликан на велосипеде: уровень Low (24с, $0.10)" loading="lazy">
          </div>
          <div class="mag-card-body">
            <p>Контурный рисунок без глубоких рассуждений. Базовые пропорции рамы и птицы.</p>
          </div>
        </article>

        <!-- Medium -->
        <article class="mag-pelican-card">
          <div class="mag-card-head">
            <span class="mag-card-level">Средний (Medium)</span>
            <span class="mag-card-stat">23с · $0.10</span>
          </div>
          <div class="mag-card-media">
            <img width="914" height="686" src="/images/blog/fable51/pelikan-medium.png" alt="Пеликан на велосипеде: уровень Medium (23с, $0.10)" loading="lazy">
          </div>
          <div class="mag-card-body">
            <p>Чуть чётче геометрия крыла и клюва, минимальные детали пера. Стоимость та же.</p>
          </div>
        </article>

        <!-- High -->
        <article class="mag-pelican-card">
          <div class="mag-card-head">
            <span class="mag-card-level">Высокий (High)</span>
            <span class="mag-card-stat">30с · $0.13</span>
          </div>
          <div class="mag-card-media">
            <img width="914" height="686" src="/images/blog/fable51/pelikan-high.png" alt="Пеликан на велосипеде: уровень High (30с, $0.13)" loading="lazy">
          </div>
          <div class="mag-card-body">
            <p>Включаются рассуждения. Появляется штриховка, форма тела становится анатомичнее.</p>
          </div>
        </article>

        <!-- XHigh -->
        <article class="mag-pelican-card">
          <div class="mag-card-head">
            <span class="mag-card-level">Очень высокий (XHigh)</span>
            <span class="mag-card-stat">7м 51с · $1.83</span>
          </div>
          <div class="mag-card-media">
            <img width="914" height="686" src="/images/blog/fable51/pelikan-xhigh.png" alt="Пеликан на велосипеде: уровень XHigh (7м 51с, $1.83)" loading="lazy">
          </div>
          <div class="mag-card-body">
            <p>15-кратный рост по времени. Тщательная прорисовка оперения, перьев, спиц и светотени.</p>
          </div>
        </article>

        <!-- Max -->
        <article class="mag-pelican-card mag-pelican-max">
          <div class="mag-card-head">
            <span class="mag-card-level">Максимальный (Max)</span>
            <span class="mag-card-stat highlight">13м 54с · $3.30</span>
          </div>
          <div class="mag-card-media">
            <img width="914" height="686" src="/images/blog/fable51/pelikan-max.webp" alt="Пеликан на велосипеде: уровень Max (13м 54с, $3.30)" loading="lazy">
          </div>
          <div class="mag-card-body">
            <p>14 минут непрерывного мышления. Появились шлем, корзина с рыбой, ноги по обе стороны рамы.</p>
          </div>
        </article>
      </div>

      <p class="mag-strip-caption">
        <strong>Наблюдение Simon Willison:</strong> на Low и Medium модель почти не тратит время на рассуждения ($0.10), а на Max уходит в 14-минутный поиск сюжета и деталей.
      </p>
    </div>

  </div>
</section>
"""

# Table of contents
toc_html = """
<div class="page">
<nav class="toc" aria-label="Содержание"><ul><li><a href="#model">Claude Fable 5.1</a></li><li><a href="#reliz">Что вышло</a></li><li><a href="#usilie">Бенчмарки по уровням усилия</a></li><li><a href="#nauka">Три научных результата</a></li><li><a href="#oblasti">Кейсы партнёров по областям работы</a></li><li><a href="#coding">1. Агентный кодинг и долгие автономные прогоны</a></li><li><a href="#debug">2. Отладка и разбор инцидентов</a></li><li><a href="#research">3. Исследовательские задачи</a></li><li><a href="#finance">4. Финансы и документы</a></li><li><a href="#writing">5. Письмо и знаниевая работа</a></li><li><a href="#agents">6. Агенты с инструментами</a></li><li><a href="#price">7. Цена и скорость</a></li><li><a href="#syscard">Системная карта: риски, взломы и лимиты</a></li><li><a href="#prompting">Как промптить Fable 5.1</a></li><li><a href="#otzyvy">Пеликаны Simon Willison</a></li><li><a href="#video-zhir">Стена видео и боевые прогоны</a></li><li><a href="#otzyvy-x">Первые отзывы в X</a></li><li><a href="#istochniki">Первоисточник</a></li></ul></nav>
"""

# Extract Bento grid from v1 (between bentoApp start and syscard start)
bento_start = v1.find('<div class="bento-container" id="bentoApp">')
bento_end = v1.find('<div class="page"><section id="syscard">')
bento_html = v1[bento_start:bento_end]

# Verify NO search box is present in Bento
search_row_start = bento_html.find('<div class="bento-search-row">')
if search_row_start != -1:
    search_row_end = bento_html.find('</div>\n      <div class="bento-pills-row"')
    bento_html = bento_html[:search_row_start] + bento_html[search_row_end + 6:]

no_results_start = bento_html.find('<div class="bento-no-results"')
if no_results_start != -1:
    bento_html = bento_html[:no_results_start] + '</div>\n'

# Extract model to nauka from base
idx_model = base.find('<section id="model"')
idx_oblasti_head = base.find('<section id="oblasti">')
idx_oblasti_svg_end = base.find('</section>\n</div>', idx_oblasti_head) + len('</section>\n</div>')
model_to_nauka_svg = base[idx_model:idx_oblasti_svg_end]

# Extract syscard through otzyvy (Simon Willison) from base
idx_syscard = base.find('<div class="page"><section id="syscard">')
idx_video_zhir = base.find('<section id="video-zhir"')
syscard_to_otzyvy = base[idx_syscard:idx_video_zhir]

# Custom Clean Video Section (#video-zhir)
video_wall_html = """
<section id="video-zhir" class="mag-video-section" aria-label="Стена видео и боевые прогоны">
  <!-- Ненавязчивый затемнённый мозаичный фон из обложек видеосообщества X -->
  <div class="mag-video-backdrop" aria-hidden="true">
    <div class="mag-mosaic-grid">
      <div class="mag-mosaic-item"><img src="/images/blog/fable51/superalesha-poster.jpg" alt="" loading="lazy"></div>
      <div class="mag-mosaic-item"><img src="/images/blog/fable51/bridgemindai-poster.jpg" alt="" loading="lazy"></div>
      <div class="mag-mosaic-item"><img src="/images/blog/fable51/spicey_lemonade-poster.jpg" alt="" loading="lazy"></div>
      <div class="mag-mosaic-item"><img src="/images/blog/fable51/knowixbuilds-poster.jpg" alt="" loading="lazy"></div>
      <div class="mag-mosaic-item"><img src="/images/blog/fable51/llmjunky-poster.jpg" alt="" loading="lazy"></div>
      <div class="mag-mosaic-item"><img src="/images/blog/fable51/techartist_-poster.jpg" alt="" loading="lazy"></div>
      <div class="mag-mosaic-item"><img src="/images/blog/fable51/bijanbowen-poster.jpg" alt="" loading="lazy"></div>
      <div class="mag-mosaic-item"><img src="/images/blog/fable51/harshithlucky3-poster.jpg" alt="" loading="lazy"></div>
      <div class="mag-mosaic-item"><img src="/images/blog/fable51/holytrinity-poster.jpg" alt="" loading="lazy"></div>
      <div class="mag-mosaic-item"><img src="/images/blog/fable51/omedvibecodes-arena-poster.jpg" alt="" loading="lazy"></div>
    </div>
    <div class="mag-backdrop-overlay"></div>
  </div>

  <!-- Передний план: два сфокусированных просторных видеоплеера -->
  <div class="mag-video-foreground">
    <div class="page">
      <div class="mag-video-header">
        <p class="kicker">Боевые тесты</p>
        <h2>Стена видео и боевые прогоны</h2>
        <p class="mag-video-intro">Два ключевых теста первых суток релиза: проверка автономного расхода квоты от Райли Брауна и сравнительный прогон против GPT-5.6 Sol в Blender 3D на реальном плане квартиры.</p>
      </div>
    </div>

    <div class="mag-video-grid">
      <!-- Riley Brown $218 Burn -->
      <article class="mag-video-card">
        <div class="mag-vc-header">
          <div class="mag-vc-tag">Тест расхода</div>
          <h3 class="mag-vc-title">Тестирование агентного расхода: $218 за 3 промпта</h3>
          <div class="mag-vc-author"><a href="https://x.com/rileybrown/status/2095005898095653302" target="_blank" rel="noopener">Райли Браун (@rileybrown)</a> · 1 сентября 2026</div>
        </div>
        <div class="mag-vc-player">
          <video width="900" height="582" controls preload="none" poster="/images/blog/fable51/rileybrown-218-poster.jpg" src="https://pub-e4f33e98bfb544e39053056c8bb8940a.r2.dev/fable51/rileybrown-218.mp4"></video>
        </div>
        <div class="mag-vc-body">
          <p>Три сложных промпта на Fable 5.1 с глубокими рассуждениями и параллельными вызовами субагентов обошлись в $218. Модель запускает многократные агентные циклы и активно читает кэш, что при максимальной нагрузке приводит к резкому росту счета.</p>
          <div class="mag-vc-metrics">
            <div class="mag-metric-box">
              <span class="mag-metric-val">$218.00</span>
              <span class="mag-metric-lbl">Итоговый расход</span>
            </div>
            <div class="mag-metric-box">
              <span class="mag-metric-val">3</span>
              <span class="mag-metric-lbl">Промпта</span>
            </div>
            <div class="mag-metric-box">
              <span class="mag-metric-val">High</span>
              <span class="mag-metric-lbl">Уровень усилия</span>
            </div>
            <div class="mag-metric-box">
              <span class="mag-metric-val">~$72.60</span>
              <span class="mag-metric-lbl">Средняя цена запроса</span>
            </div>
          </div>
        </div>
      </article>

      <!-- ctgptlb 3D Blender Shootout -->
      <article class="mag-video-card">
        <div class="mag-vc-header">
          <div class="mag-vc-tag">Сравнение моделей</div>
          <h3 class="mag-vc-title">Fable 5.1 против GPT-5.6 Sol в Blender 3D</h3>
          <div class="mag-vc-author"><a href="https://x.com/ctgptlb/status/2094925117344428232" target="_blank" rel="noopener">@ctgptlb</a> · 1 сентября 2026</div>
        </div>
        <div class="mag-vc-player">
          <video width="900" height="506" controls preload="none" poster="/images/blog/fable51/ctgptlb-blender-poster.jpg" src="https://pub-e4f33e98bfb544e39053056c8bb8940a.r2.dev/fable51/ctgptlb-blender.mp4"></video>
        </div>
        <div class="mag-vc-body">
          <p>Одна задача обеим моделям: из плана квартиры собрать 3D в Blender, отрендерить изометрические ракурсы комнат и сгенерировать видео облёта с камеры. Sol справилась за 30 минут (6 ракурсов), Fable 5.1 потратила 111 минут, но выдала 14 детализированных ракурсов.</p>
          <div class="mag-vc-metrics">
            <div class="mag-metric-box">
              <span class="mag-metric-val">111 мин vs 30</span>
              <span class="mag-metric-lbl">Время генерации</span>
            </div>
            <div class="mag-metric-box">
              <span class="mag-metric-val">14 vs 6</span>
              <span class="mag-metric-lbl">3D-ракурсов</span>
            </div>
            <div class="mag-metric-box">
              <span class="mag-metric-val">44с vs 36с</span>
              <span class="mag-metric-lbl">Длина видеотура</span>
            </div>
            <div class="mag-metric-box">
              <span class="mag-metric-val">Fable 5.1</span>
              <span class="mag-metric-lbl">Качество текстур</span>
            </div>
          </div>
        </div>
      </article>
    </div>
  </div>
</section>
"""

# Extract otzyvy-x to istochniki end from base
idx_otzyvy_x = base.find('<section id="otzyvy-x">')
idx_liquid_dock = base.find('<!-- Liquid Glass Floating Navigation Dock -->')
otzyvy_x_to_istochniki = base[idx_otzyvy_x:idx_liquid_dock]

# Custom CSS for Variant 2
custom_css = """
<style>
/* ==========================================================================
   VARIANT 2: Плотный журнал (Dense Magazine Strip)
   Swiss editorial typography, paper theme, clean layouts.
   No sci-fi, no crosshairs, no HUDs, no scanlines, no neon.
   ========================================================================== */

/* Article Variant Switcher Bar */
.article-variant-switcher {
  position: sticky;
  top: 0;
  z-index: 100;
  background: var(--paper);
  border-bottom: 1px solid var(--hairline);
  padding: 10px 18px;
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
  font-family: 'PT Mono', monospace;
  font-size: 12px;
}
.avs-group {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}
.avs-label {
  font-weight: 700;
  color: var(--muted);
  text-transform: uppercase;
  font-size: 11px;
  letter-spacing: .06em;
}
.avs-link {
  color: var(--muted);
  text-decoration: none;
  padding: 4px 10px;
  border-radius: 6px;
  border: 1px solid transparent;
  transition: all .15s ease;
  white-space: nowrap;
}
.avs-link:hover {
  color: var(--ink);
  background: var(--card);
  border-color: var(--hairline);
}
.avs-link.is-active {
  color: var(--ink);
  background: var(--card);
  border-color: var(--ink);
  font-weight: 700;
}
.avs-hint {
  font-size: 11.5px;
  color: var(--muted);
}
@media (max-width: 768px) {
  .avs-hint { display: none; }
}

/* --- HERO SECTION: TWO-LEVEL EDITORIAL LAYOUT --- */
.mag-hero-section {
  max-width: min(1140px, calc(100vw - 36px));
  margin: 16px auto 44px;
  padding: 0 16px;
}
@media (max-width: 640px) {
  .mag-hero-section {
    padding: 0 8px;
    margin: 8px auto 32px;
  }
}
.mag-hero-wrap {
  display: flex;
  flex-direction: column;
  gap: 28px;
}

/* Top Level: Botanical Art */
.mag-hero-art {
  margin: 0 auto;
  width: 100%;
  text-align: center;
}
.mag-hero-art-frame {
  display: inline-block;
  background: #020202;
  border: 1px solid var(--hairline);
  border-radius: 6px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  max-width: 580px;
  width: 100%;
}
.mag-hero-art-img {
  width: 100%;
  height: auto;
  display: block;
  margin: 0 auto;
}
.mag-hero-art-caption {
  font: 400 12px/1.5 'PT Mono', monospace;
  color: var(--muted);
  text-align: center;
  margin-top: 10px;
  letter-spacing: .02em;
}

/* Immediately Below: Pelican 5-stage Strip */
.mag-pelican-strip {
  background: var(--card);
  border: 1px solid var(--hairline);
  border-radius: 6px;
  padding: 20px 22px;
}
.mag-strip-header {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  gap: 12px;
  padding-bottom: 12px;
  margin-bottom: 16px;
  border-bottom: 1px solid var(--hairline);
  flex-wrap: wrap;
}
.mag-strip-title {
  font: 700 13px/1.4 'PT Mono', monospace;
  text-transform: uppercase;
  letter-spacing: .05em;
  color: var(--ink);
}
.mag-strip-meta {
  font: 400 12px/1.4 'PT Mono', monospace;
  color: var(--muted);
}
.mag-pelican-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 14px;
}
@media (max-width: 1024px) {
  .mag-pelican-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}
@media (max-width: 680px) {
  .mag-pelican-grid {
    display: flex;
    overflow-x: auto;
    scroll-snap-type: x mandatory;
    gap: 12px;
    padding-bottom: 8px;
    scrollbar-width: thin;
  }
  .mag-pelican-card {
    flex: 0 0 240px;
    scroll-snap-align: start;
  }
}
.mag-pelican-card {
  background: var(--paper);
  border: 1px solid var(--hairline);
  border-radius: 4px;
  padding: 12px;
  display: flex;
  flex-direction: column;
  transition: transform .18s ease, border-color .18s ease;
}
.mag-pelican-card:hover {
  transform: translateY(-2px);
  border-color: var(--rule);
}
.mag-pelican-card.mag-pelican-max {
  border-color: var(--ink);
}
.mag-card-head {
  display: flex;
  flex-direction: column;
  gap: 3px;
  margin-bottom: 10px;
  padding-bottom: 8px;
  border-bottom: 1px solid var(--hairline);
}
.mag-card-level {
  font: 700 11.5px/1.3 'PT Mono', monospace;
  text-transform: uppercase;
  letter-spacing: .04em;
  color: var(--ink);
}
.mag-card-stat {
  font: 400 11px/1.3 'PT Mono', monospace;
  color: var(--muted);
}
.mag-card-stat.highlight {
  font-weight: 700;
  color: var(--ink);
}
.mag-card-media {
  background: var(--card);
  border: 1px solid var(--hairline);
  border-radius: 3px;
  overflow: hidden;
  margin-bottom: 10px;
  line-height: 0;
}
.mag-card-media img {
  width: 100%;
  height: auto;
  display: block;
}
.mag-card-body p {
  margin: 0;
  font-size: 13px;
  line-height: 1.45;
  color: var(--ink);
}
.mag-strip-caption {
  margin: 16px 0 0;
  padding-top: 12px;
  border-top: 1px dashed var(--hairline);
  font-size: 13px;
  line-height: 1.5;
  color: var(--muted);
}

/* --- VIDEO SECTION: DENSE EDITORIAL MAGAZINE VIDEO WALL --- */
.mag-video-section {
  position: relative;
  background: #0e1117;
  color: #f1f5f9;
  padding: 64px 0 72px;
  margin: 48px 0;
  overflow: hidden;
}
.mag-video-backdrop {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
  overflow: hidden;
}
.mag-mosaic-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 8px;
  width: 110%;
  margin-left: -5%;
  opacity: 0.16;
  filter: grayscale(30%);
}
@media (max-width: 800px) {
  .mag-mosaic-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}
.mag-mosaic-item {
  background: #000;
  aspect-ratio: 16/10;
  overflow: hidden;
}
.mag-mosaic-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}
.mag-backdrop-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(circle at 50% 30%, rgba(14, 17, 23, 0.72) 0%, rgba(14, 17, 23, 0.96) 85%);
}
.mag-video-foreground {
  position: relative;
  z-index: 2;
}
.mag-video-header {
  margin-bottom: 36px;
}
.mag-video-header .kicker {
  color: #94a3b8;
}
.mag-video-header h2 {
  color: #fff;
  font-size: 1.6em;
  margin: 0 0 10px;
}
.mag-video-intro {
  color: #94a3b8;
  font-size: 1.05em;
  line-height: 1.55;
  margin: 0;
}
.mag-video-grid {
  max-width: min(1140px, calc(100vw - 36px));
  margin: 0 auto;
  padding: 0 18px;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 28px;
}
@media (max-width: 900px) {
  .mag-video-grid {
    grid-template-columns: 1fr;
    gap: 24px;
    padding: 0 12px;
  }
}
.mag-video-card {
  background: rgba(22, 27, 36, 0.94);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 8px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.35);
  transition: border-color .2s ease;
}
.mag-video-card:hover {
  border-color: rgba(255, 255, 255, 0.28);
}
.mag-vc-header {
  padding: 18px 20px 14px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}
.mag-vc-tag {
  display: inline-block;
  font: 700 11px/1.3 'PT Mono', monospace;
  text-transform: uppercase;
  letter-spacing: .06em;
  color: #94a3b8;
  background: rgba(255, 255, 255, 0.06);
  padding: 3px 8px;
  border-radius: 4px;
  margin-bottom: 8px;
}
.mag-vc-title {
  font-size: 1.2em;
  font-weight: 700;
  margin: 0 0 6px;
  line-height: 1.35;
  color: #f8fafc;
}
.mag-vc-author {
  font: 400 12px/1.4 'PT Mono', monospace;
  color: #94a3b8;
}
.mag-vc-author a {
  color: #cbd5e1;
  text-decoration: underline;
  text-underline-offset: 3px;
}
.mag-vc-player {
  background: #000;
  position: relative;
  line-height: 0;
  width: 100%;
}
.mag-vc-player video {
  width: 100%;
  height: auto;
  display: block;
  max-height: 380px;
  object-fit: contain;
}
.mag-vc-body {
  padding: 18px 20px 20px;
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}
.mag-vc-body p {
  margin: 0 0 16px;
  font-size: 14.5px;
  line-height: 1.55;
  color: #cbd5e1;
}
.mag-vc-metrics {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 8px;
  padding-top: 14px;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
}
@media (max-width: 540px) {
  .mag-vc-metrics {
    grid-template-columns: repeat(2, 1fr);
  }
}
.mag-metric-box {
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 4px;
  padding: 8px 10px;
  text-align: center;
}
.mag-metric-val {
  display: block;
  font: 700 13px/1.3 'PT Mono', monospace;
  color: #f8fafc;
  margin-bottom: 2px;
}
.mag-metric-lbl {
  display: block;
  font: 400 10.5px/1.2 'PT Mono', monospace;
  color: #94a3b8;
}

/* Subtle refinements for Liquid Dock */
.liquid-dock {
  position: fixed;
  bottom: 24px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 120;
  font-family: 'PT Mono', monospace;
}
.liquid-dock-bar {
  display: flex;
  align-items: center;
  background: var(--card);
  border: 1px solid var(--hairline);
  box-shadow: 0 6px 24px rgba(0, 0, 0, 0.12);
  border-radius: 30px;
  padding: 5px 8px;
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
}
.liquid-dock-trigger {
  display: flex;
  align-items: center;
  gap: 8px;
  background: none;
  border: none;
  padding: 6px 12px;
  font: 400 12px/1 'PT Mono', monospace;
  color: var(--ink);
  cursor: pointer;
}
.liquid-dock-pulse {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--ink);
}
.liquid-dock-cur-num {
  font-weight: 700;
  color: var(--muted);
}
.liquid-dock-cur-title {
  font-weight: 700;
  color: var(--ink);
}
.liquid-dock-chevron {
  color: var(--muted);
  transition: transform .2s ease;
}
.liquid-dock.is-open .liquid-dock-chevron {
  transform: rotate(180deg);
}
.liquid-dock-sep {
  width: 1px;
  height: 16px;
  background: var(--hairline);
  margin: 0 4px;
}
.liquid-dock-top {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: none;
  border: none;
  color: var(--ink);
  cursor: pointer;
  transition: background .15s ease;
}
.liquid-dock-top:hover {
  background: var(--paper);
}
.liquid-dock-drawer {
  position: absolute;
  bottom: calc(100% + 12px);
  left: 50%;
  transform: translateX(-50%) translateY(8px);
  width: 320px;
  max-height: 420px;
  overflow-y: auto;
  background: var(--paper);
  border: 1px solid var(--hairline);
  box-shadow: 0 12px 36px rgba(0, 0, 0, 0.18);
  border-radius: 12px;
  padding: 14px;
  opacity: 0;
  pointer-events: none;
  transition: opacity .2s ease, transform .2s ease;
}
.liquid-dock.is-open .liquid-dock-drawer {
  opacity: 1;
  pointer-events: auto;
  transform: translateX(-50%) translateY(0);
}
.liquid-dock-drawer-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 8px;
  margin-bottom: 8px;
  border-bottom: 1px solid var(--hairline);
  font-size: 11px;
  color: var(--muted);
  text-transform: uppercase;
  letter-spacing: .06em;
}
.liquid-dock-list {
  list-style: none;
  margin: 0;
  padding: 0;
}
.liquid-dock-list li {
  margin-bottom: 4px;
}
.liquid-dock-link {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 6px 8px;
  border-radius: 6px;
  text-decoration: none;
  color: var(--ink);
  font-size: 12px;
  transition: background .15s ease;
}
.liquid-dock-link:hover {
  background: var(--card);
}
.liquid-dock-link.is-active {
  background: var(--card);
  font-weight: 700;
}
.liquid-num {
  font-size: 11px;
  color: var(--muted);
}
</style>
"""

# Liquid dock HTML & Scripts
liquid_dock_html_and_js = base[idx_liquid_dock:]

# Combine everything
hugo_body = (
    top_bar +
    hero_magazine_html +
    toc_html + "\n" +
    model_to_nauka_svg + "\n" +
    bento_html + "\n" +
    syscard_to_otzyvy + "\n" +
    video_wall_html + "\n" +
    otzyvy_x_to_istochniki + "\n" +
    custom_css + "\n" +
    liquid_dock_html_and_js
)

# Write to content/blog/claude-fable-5-1-v2.html
with open('content/blog/claude-fable-5-1-v2.html', 'w', encoding='utf-8') as f:
    f.write(hugo_frontmatter + "\n" + hugo_body)
print("Successfully generated content/blog/claude-fable-5-1-v2.html")

# Generate standalone static HTML file for static/design-review/variant-2.html
static_html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Обзор Claude Fable 5.1 [Вариант 2: Плотный журнал] | sereja.tech</title>
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=PT+Serif:ital,wght@0,400;0,700;1,400&family=PT+Mono&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/css/paper.css">
  <script>try{{var t=localStorage.getItem("theme");if(t)document.documentElement.setAttribute("data-theme",t)}}catch(e){{}}</script>
</head>
<body class="paper">
  <nav class="site-top" aria-label="Основная навигация">
    <a class="wordmark" href="/">Сережа Рис</a>
    <span class="site-links">
      <a href="/blog/">Блог</a>
      <a href="/about/">Обо мне</a>
      <a href="https://t.me/ris_ai?utm_source=sereja_tech&utm_medium=link&utm_campaign=article_nav" target="_blank" rel="noopener">Телеграм</a>
    </span>
  </nav>

  <main>
{hugo_body}
  </main>

  <footer class="site-bottom">
    <span>© 2026 Сережа Рис · sereja.tech</span>
    <span class="site-links">
      <a href="https://t.me/ris_ai?utm_source=sereja_tech&utm_medium=link&utm_campaign=footer" target="_blank" rel="noopener">Телеграм</a>
      <a href="https://www.youtube.com/@serejaris?utm_source=sereja_tech&utm_medium=link&utm_campaign=footer" target="_blank" rel="noopener">YouTube</a>
      <a href="https://t.me/vibecod3rs?utm_source=sereja_tech&utm_medium=link&utm_campaign=footer" target="_blank" rel="noopener">Вайбкодеры</a>
      <a href="https://github.com/serejaris" target="_blank" rel="noopener">GitHub</a>
    </span>
  </footer>
</body>
</html>
"""

os.makedirs('static/design-review', exist_ok=True)
with open('static/design-review/variant-2.html', 'w', encoding='utf-8') as f:
    f.write(static_html)
print("Successfully generated static/design-review/variant-2.html")
