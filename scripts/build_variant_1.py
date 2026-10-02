#!/usr/bin/env python3
"""
Builder for Variant 1: Редакционная классика (Swiss Editorial)
Outputs:
  - content/blog/claude-fable-5-1-v1.html (Hugo post with frontmatter)
  - static/design-review/variant-1.html (Standalone static preview)
"""

import os
import re

def build_variant_1():
    base_file = 'content/blog/claude-fable-5-1.html'
    with open(base_file, 'r', encoding='utf-8') as f:
        base = f.read()

    # Frontmatter for Hugo post
    frontmatter = """---
title: "Обзор Claude Fable 5.1 [Вариант 1: Редакционная классика]"
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
slug: "claude-fable-5-1-v1"
sitemap_exclude: true
robots: "noindex, nofollow"
---
"""

    # Variant Switcher & Theme Button
    header_nav = """<button class="theme-btn" id="themeBtn" aria-label="Переключить тему">☾</button>

<nav class="article-variant-switcher" aria-label="Сравнение вариантов статьи">
  <div class="avs-group">
    <span class="avs-label">Вариант:</span>
    <a href="/blog/claude-fable-5-1-v1/" class="avs-link is-active" aria-current="page">1. Редакционная классика</a>
    <a href="/blog/claude-fable-5-1-v2/" class="avs-link">2. Master-Detail (Досье)</a>
    <a href="/blog/claude-fable-5-1-v3/" class="avs-link">3. Unified Rail (Один слайдер)</a>
    <a href="/blog/claude-fable-5-1/" class="avs-link" style="opacity:0.65">Было (7 слайдеров)</a>
  </div>
  <span class="avs-hint">Вариант 1: чистая швейцарская типографика, сетка пеликанов и видеостена</span>
</nav>

<div class="page"><header class="masthead">
<p class="kicker">Fable 5.1 · Релиз 1 сентября 2026</p>
<h1>Разбираю Claude Fable 5.1: бенчмарки, отзывы, системная карта и промптинг</h1>
<p class="lede">Пересказ анонса Anthropic и 22 отзыва партнёров, разложенные по типу использования модели.</p>
<p class="meta">Источники: страница релиза и системная карта Anthropic, пост Simon Willison, 33 поста в X, экран usage founder · снято <time datetime="2026-09-02">2 сентября 2026</time> · независимой проверки нет</p>
</header>
</div> <!-- close .page from masthead -->
"""

    # 1. Hero Section: Clean 5-card grid of Simon Willison's pelicans
    pelican_hero = """<!-- Hero section: Clean 5-card grid of Simon Willison's pelicans -->
<div class="pelican-hero-container">
  <div class="pelican-hero-box" id="thinkingGrid">
    <div class="pelican-hero-header">
      <p class="pelican-kicker">Тест Саймона Уиллисона · Уровни рассуждений</p>
      <h2 class="pelican-hero-title">Пять уровней усилия: «Пеликан на велосипеде»</h2>
      <p class="pelican-hero-lead">Один и тот же промпт на пяти уровнях extended thinking: от базового SVG за 10 центов до 14 минут размышлений со шлемом и корзиной рыбы.</p>
    </div>

    <div class="pelican-grid">
      <!-- Card 1: Low -->
      <article class="pelican-card">
        <div class="pelican-card-head">
          <span class="pelican-level">Low</span>
          <span class="pelican-tag">Без рассуждений</span>
        </div>
        <div class="pelican-media">
          <img width="914" height="686" src="/images/blog/fable51/pelikan-low.png" alt="Пеликан на велосипеде: уровень Low (24 с, $0.10)" loading="eager">
        </div>
        <div class="pelican-stats">
          <span class="pelican-stat-time">24 с</span>
          <span class="pelican-stat-sep">·</span>
          <span class="pelican-stat-cost">$0.10</span>
        </div>
        <p class="pelican-desc">Без рассуждений, базовые контуры. Примитивные круги колёс, тело птицы оторвано от рамы.</p>
      </article>

      <!-- Card 2: Medium -->
      <article class="pelican-card">
        <div class="pelican-card-head">
          <span class="pelican-level">Medium</span>
          <span class="pelican-tag">Без рассуждений</span>
        </div>
        <div class="pelican-media">
          <img width="914" height="686" src="/images/blog/fable51/pelikan-medium.png" alt="Пеликан на велосипеде: уровень Medium (23 с, $0.10)" loading="lazy">
        </div>
        <div class="pelican-stats">
          <span class="pelican-stat-time">23 с</span>
          <span class="pelican-stat-sep">·</span>
          <span class="pelican-stat-cost">$0.10</span>
        </div>
        <p class="pelican-desc">Без рассуждений, идентичный результат. Та же цена и скорость, простейшие векторные контуры.</p>
      </article>

      <!-- Card 3: High -->
      <article class="pelican-card is-highlight">
        <div class="pelican-card-head">
          <span class="pelican-level">High</span>
          <span class="pelican-tag tag-code">Дефолт Claude Code</span>
        </div>
        <div class="pelican-media">
          <img width="914" height="686" src="/images/blog/fable51/pelikan-high.png" alt="Пеликан на велосипеде: уровень High (30 с, $0.13)" loading="lazy">
        </div>
        <div class="pelican-stats">
          <span class="pelican-stat-time">30 с</span>
          <span class="pelican-stat-sep">·</span>
          <span class="pelican-stat-cost">$0.13</span>
        </div>
        <p class="pelican-desc">Дефолт Claude Code, посадка на раму. Включается рассуждение: собран узнаваемый силуэт птицы.</p>
      </article>

      <!-- Card 4: XHigh -->
      <article class="pelican-card">
        <div class="pelican-card-head">
          <span class="pelican-level">XHigh</span>
          <span class="pelican-tag">Глубокий цикл</span>
        </div>
        <div class="pelican-media">
          <img width="914" height="686" src="/images/blog/fable51/pelikan-xhigh.png" alt="Пеликан на велосипеде: уровень XHigh (7 мин 51 с, $1.83)" loading="lazy">
        </div>
        <div class="pelican-stats">
          <span class="pelican-stat-time">7 мин 51 с</span>
          <span class="pelican-stat-sep">·</span>
          <span class="pelican-stat-cost">$1.83</span>
        </div>
        <p class="pelican-desc">Скачок времени в 15 раз, проработка спиц и перьев. Глубокий механический цикл мышления.</p>
      </article>

      <!-- Card 5: Max -->
      <article class="pelican-card is-max">
        <div class="pelican-card-head">
          <span class="pelican-level">Max</span>
          <span class="pelican-tag tag-max">14 мин мышления</span>
        </div>
        <div class="pelican-media">
          <img width="914" height="686" src="/images/blog/fable51/pelikan-max.webp" alt="Пеликан на велосипеде: уровень Max (13 мин 54 с, $3.30)" loading="lazy">
        </div>
        <div class="pelican-stats">
          <span class="pelican-stat-time">13 мин 54 с</span>
          <span class="pelican-stat-sep">·</span>
          <span class="pelican-stat-cost">$3.30</span>
        </div>
        <p class="pelican-desc">14 минут мышления, шлем, корзина с рыбой, педали с двух сторон. Завершённая иллюстрация.</p>
      </article>
    </div>

    <div class="pelican-caption">
      <p><strong>Вывод Саймона Уиллисона:</strong> на Low и Medium модель не использует рассуждения и возвращает базовый SVG за 10 центов. Рассуждения начинаются с High (дефолт Claude Code), а на Max уходят в 14-минутный цикл, механически прорисовывая детали и сюжет.</p>
    </div>
  </div>
</div>
"""

    # TOC and sections from base
    toc = """<div class="page">

<nav class="toc" aria-label="Содержание"><ul><li><a href="#model">Claude Fable 5.1</a></li><li><a href="#reliz">Что вышло</a></li><li><a href="#usilie">Бенчмарки по уровням усилия</a></li><li><a href="#nauka">Три научных результата</a></li><li><a href="#oblasti">Кейсы партнёров по областям работы</a></li><li><a href="#coding">1. Агентный кодинг и долгие автономные прогоны</a></li><li><a href="#debug">2. Отладка и разбор инцидентов</a></li><li><a href="#research">3. Исследовательские задачи</a></li><li><a href="#finance">4. Финансы и документы</a></li><li><a href="#writing">5. Письмо и знаниевая работа</a></li><li><a href="#agents">6. Агенты с инструментами</a></li><li><a href="#price">7. Цена и скорость</a></li><li><a href="#syscard">Системная карта: риски, взломы и лимиты</a></li><li><a href="#prompting">Как промптить Fable 5.1</a></li><li><a href="#otzyvy">Пеликаны Simon Willison</a></li><li><a href="#video-zhir">Боевые видео и расход лимитов</a></li><li><a href="#otzyvy-x">Первые отзывы в X</a></li><li><a href="#istochniki">Первоисточник</a></li></ul></nav>
"""

    # Extract model to oblasti from base
    idx_model = base.find('<section id="model"')
    idx_oblasti_head = base.find('<section id="oblasti">')
    idx_oblasti_svg_end = base.find('</section>\n</div>', idx_oblasti_head) + len('</section>\n</div>')
    model_to_oblasti = base[idx_model:idx_oblasti_svg_end]

    # Extract clean Bento Grid from existing v1
    with open('content/blog/claude-fable-5-1-v1.html', 'r', encoding='utf-8') as f:
        v1_existing = f.read()

    bento_start = v1_existing.find('<!-- Bento Grid 22 Partner Cases')
    bento_end = v1_existing.find('<div class="page"><section id="syscard">')
    bento_html = v1_existing[bento_start:bento_end]

    # Extract syscard through prompting from base
    idx_syscard = base.find('<div class="page"><section id="syscard">')
    idx_otzyvy = base.find('<div class="page"><section id="otzyvy">')
    syscard_to_prompting = base[idx_syscard:idx_otzyvy]

    # Clean Simon Willison otzyvy section (without duplicate pelican gallery)
    otzyvy_section = """<div class="page"><section id="otzyvy"><h2>Пеликаны Simon Willison</h2>
<p><a href="https://simonwillison.net/2026/Sep/1/claude-fable-5-1/" target="_blank" rel="noopener">Simon Willison</a> прогнал один и тот же промпт на всех пяти уровнях усилия и заметил, что на low и medium в ответе нет следов extended thinking, а с xhigh рассуждение раскручивается в десятки раз по токенам и цене. Подробное визуальное сравнение иллюстраций вынесено в начало статьи.</p>
<p>На max появились шлем, корзина с рыбой и ноги по обе стороны рамы. Анимацию он попросил следующим промптом "animate this" на уровне high за $1.37. Сравнения с прошлыми моделями в посте нет, есть одна оговорка: до размаха Gemini 3.7 Flash пеликан не дотягивает.</p>
</section></div>
"""

    # 2. Video Section (#video-zhir): "Боевые видео и расход лимитов"
    video_zhir_section = """<section id="video-zhir" class="video-zhir-section">
  <!-- Приглушённая сетка из 12 скриншотов комьюнити из X на фоне -->
  <div class="vwall-ambient-backdrop" aria-hidden="true">
    <div class="vwall-mosaic-grid">
      <div class="vwall-ambient-tile"><img src="/images/blog/fable51/superalesha-poster.jpg" alt="" loading="lazy"></div>
      <div class="vwall-ambient-tile"><img src="/images/blog/fable51/bridgemindai-poster.jpg" alt="" loading="lazy"></div>
      <div class="vwall-ambient-tile"><img src="/images/blog/fable51/spicey_lemonade-poster.jpg" alt="" loading="lazy"></div>
      <div class="vwall-ambient-tile"><img src="/images/blog/fable51/knowixbuilds-poster.jpg" alt="" loading="lazy"></div>
      <div class="vwall-ambient-tile"><img src="/images/blog/fable51/llmjunky-poster.jpg" alt="" loading="lazy"></div>
      <div class="vwall-ambient-tile"><img src="/images/blog/fable51/techartist_-poster.jpg" alt="" loading="lazy"></div>
      <div class="vwall-ambient-tile"><img src="/images/blog/fable51/bijanbowen-poster.jpg" alt="" loading="lazy"></div>
      <div class="vwall-ambient-tile"><img src="/images/blog/fable51/harshithlucky3-poster.jpg" alt="" loading="lazy"></div>
      <div class="vwall-ambient-tile"><img src="/images/blog/fable51/holytrinity-poster.jpg" alt="" loading="lazy"></div>
      <div class="vwall-ambient-tile"><img src="/images/blog/fable51/omedvibecodes-arena-poster.jpg" alt="" loading="lazy"></div>
      <div class="vwall-ambient-tile"><img src="/images/blog/fable51/rileybrown-218-poster.jpg" alt="" loading="lazy"></div>
      <div class="vwall-ambient-tile"><img src="/images/blog/fable51/ctgptlb-blender-poster.jpg" alt="" loading="lazy"></div>
    </div>
    <div class="vwall-backdrop-overlay"></div>
  </div>

  <div class="vwall-content-wrap">
    <div class="vwall-head-box">
      <p class="vwall-kicker">Боевые тесты релиза</p>
      <h2 class="vwall-title">Боевые видео и расход лимитов</h2>
      <p class="vwall-intro">Два главных боевых видео первых суток: замер агентного расхода $218 от Райли Брауна и 111-минутный баттл с GPT-5.6 Sol в Blender 3D по реальному плану квартиры.</p>
    </div>

    <!-- 2 больших чистых плеера -->
    <div class="vwall-cards-row">
      <!-- Card 1: Riley Brown -->
      <article class="vwall-card">
        <div class="vwall-card-header">
          <h3 class="vwall-card-title">Райли Браун: $218 за 3 промпта</h3>
          <div class="vwall-card-author"><a href="https://x.com/rileybrown/status/2095005898095653302" target="_blank" rel="noopener">@rileybrown</a> · 1 сентября 2026</div>
        </div>
        <div class="vwall-video-wrap">
          <video width="900" height="582" controls preload="none" poster="/images/blog/fable51/rileybrown-218-poster.jpg" src="https://pub-e4f33e98bfb544e39053056c8bb8940a.r2.dev/fable51/rileybrown-218.mp4"></video>
        </div>
        <div class="vwall-card-body">
          <p>Три промпта на Fable 5.1 обошлись в $218. Модель поднимает глубокие циклы рассуждений и быстро расходует лимиты при решении комплексных задач.</p>
          <div class="vwall-metrics">
            <div class="vwall-metric-item">
              <span class="vwall-metric-val">$218</span>
              <span class="vwall-metric-lbl">Расход</span>
            </div>
            <div class="vwall-metric-item">
              <span class="vwall-metric-val">3</span>
              <span class="vwall-metric-lbl">Промпта</span>
            </div>
            <div class="vwall-metric-item">
              <span class="vwall-metric-val">High</span>
              <span class="vwall-metric-lbl">Усилие</span>
            </div>
          </div>
        </div>
      </article>

      <!-- Card 2: ctgptlb -->
      <article class="vwall-card">
        <div class="vwall-card-header">
          <h3 class="vwall-card-title">ctgptlb: Fable 5.1 против Sol в 3D Blender</h3>
          <div class="vwall-card-author"><a href="https://x.com/ctgptlb/status/2094925117344428232" target="_blank" rel="noopener">@ctgptlb</a> · 1 сентября 2026</div>
        </div>
        <div class="vwall-video-wrap">
          <video width="900" height="506" controls preload="none" poster="/images/blog/fable51/ctgptlb-blender-poster.jpg" src="https://pub-e4f33e98bfb544e39053056c8bb8940a.r2.dev/fable51/ctgptlb-blender.mp4"></video>
        </div>
        <div class="vwall-card-body">
          <p>Одна задача обеим моделям: из плана квартиры собрать 3D в Blender, отрендерить кадры и видео. Sol справился за 30 минут (6 кадров), Fable 5.1 работала 111 минут, но выдала 14 кадров.</p>
          <div class="vwall-metrics">
            <div class="vwall-metric-item">
              <span class="vwall-metric-val">111 мин vs 30 мин</span>
              <span class="vwall-metric-lbl">Время работы</span>
            </div>
            <div class="vwall-metric-item">
              <span class="vwall-metric-val">14 vs 6</span>
              <span class="vwall-metric-lbl">3D-кадров</span>
            </div>
            <div class="vwall-metric-item">
              <span class="vwall-metric-val">44 с vs 36 с</span>
              <span class="vwall-metric-lbl">Видео</span>
            </div>
          </div>
        </div>
      </article>
    </div>
  </div>
</section>
"""

    # Extract otzyvy-x through istochniki from base
    idx_otzyvy_x = base.find('<section id="otzyvy-x">')
    idx_post_sources = base.find('</section></div>\n\n<nav class="liquid-dock"')
    if idx_post_sources == -1:
        idx_post_sources = base.find('<!-- Liquid Glass Floating Navigation Dock -->')
    otzyvy_x_to_sources = base[idx_otzyvy_x:idx_post_sources] + '</section></div>\n\n'

    # Liquid Glass dock nav (clean, minimal)
    liquid_dock_html = """<!-- Liquid Glass Floating Navigation Dock -->
<nav class="liquid-dock" id="liquidDock" aria-label="Быстрая навигация по статье">
  <div class="liquid-dock-drawer" id="liquidDockDrawer" role="region" aria-label="Содержание статьи">
    <div class="liquid-dock-drawer-head">
      <span class="liquid-dock-drawer-title">Содержание</span>
      <span class="liquid-dock-drawer-hint">9 разделов</span>
    </div>
    <ul class="liquid-dock-list">
      <li><a href="#model" class="liquid-dock-link is-active" data-section="model"><span class="liquid-num">01</span><span class="liquid-text">Модель Fable 5.1</span></a></li>
      <li><a href="#usilie" class="liquid-dock-link" data-section="usilie"><span class="liquid-num">02</span><span class="liquid-text">Бенчмарки</span></a></li>
      <li><a href="#nauka" class="liquid-dock-link" data-section="nauka"><span class="liquid-num">03</span><span class="liquid-text">Научные открытия</span></a></li>
      <li><a href="#oblasti" class="liquid-dock-link" data-section="oblasti"><span class="liquid-num">04</span><span class="liquid-text">Кейсы партнёров</span></a></li>
      <li><a href="#video-zhir" class="liquid-dock-link" data-section="video-zhir"><span class="liquid-num">05</span><span class="liquid-text">Боевые видео</span></a></li>
      <li><a href="#syscard" class="liquid-dock-link" data-section="syscard"><span class="liquid-num">06</span><span class="liquid-text">Системная карта</span></a></li>
      <li><a href="#prompting" class="liquid-dock-link" data-section="prompting"><span class="liquid-num">07</span><span class="liquid-text">Промптинг</span></a></li>
      <li><a href="#otzyvy" class="liquid-dock-link" data-section="otzyvy"><span class="liquid-num">08</span><span class="liquid-text">Пеликаны Willison</span></a></li>
      <li><a href="#otzyvy-x" class="liquid-dock-link" data-section="otzyvy-x"><span class="liquid-num">09</span><span class="liquid-text">Отзывы в X</span></a></li>
    </ul>
  </div>

  <div class="liquid-dock-bar">
    <button class="liquid-dock-trigger" id="liquidDockTrigger" aria-expanded="false" aria-controls="liquidDockDrawer" aria-label="Открыть оглавление">
      <span class="liquid-dock-pulse" aria-hidden="true"></span>
      <span class="liquid-dock-cur-num" id="liquidDockCurNum">01</span>
      <span class="liquid-dock-cur-title" id="liquidDockCurTitle">Модель Fable 5.1</span>
      <svg class="liquid-dock-chevron" viewBox="0 0 16 16" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
        <path d="M4 6l4 4 4-4"/>
      </svg>
    </button>
    <div class="liquid-dock-sep" aria-hidden="true"></div>
    <button class="liquid-dock-top" id="liquidDockTop" aria-label="Наверх" title="Наверх">
      <svg viewBox="0 0 16 16" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
        <path d="M8 12V4M4 8l4-4 4 4"/>
      </svg>
    </button>
  </div>
</nav>
"""

    # Swiss Editorial CSS Styles
    custom_css = """<style>
/* ==========================================================================
   VARIANT 1: РЕДАКЦИОННАЯ КЛАССИКА (SWISS EDITORIAL)
   - Чистая типографика: PT Serif для текста, PT Mono для чисел и метрик
   - Бумажная тема, строгие линии 1px, спокойные акценты
   - Без псевдотехнологичных рамок, перекрестий и англоязычного мусора
   ========================================================================== */

/* --- 1. ПЯТЬ УРОВНЕЙ УСИЛИЯ (ПЕЛИКАНЫ SIMON WILLISON) --- */
.pelican-hero-container {
  max-width: 1220px;
  margin: 24px auto 48px;
  padding: 0 20px;
}

.pelican-hero-box {
  background: var(--card);
  border: 1px solid var(--rule);
  border-radius: 6px;
  padding: 28px 24px 24px;
}

.pelican-hero-header {
  margin-bottom: 24px;
  border-bottom: 1px solid var(--hairline);
  padding-bottom: 18px;
}

.pelican-kicker {
  font: 400 12px/1.4 'PT Mono', monospace;
  color: var(--muted);
  text-transform: uppercase;
  letter-spacing: .06em;
  margin: 0 0 6px;
}

.pelican-hero-title {
  font-family: 'PT Serif', Georgia, serif;
  font-size: 1.8em;
  font-weight: 700;
  line-height: 1.25;
  color: var(--ink);
  margin: 0 0 8px;
  letter-spacing: -.01em;
}

.pelican-hero-lead {
  font-size: 1.05em;
  line-height: 1.55;
  color: var(--muted);
  margin: 0;
  max-width: 860px;
}

.pelican-grid {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: 16px;
  margin-bottom: 20px;
}

.pelican-card {
  background: var(--paper);
  border: 1px solid var(--hairline);
  border-radius: 5px;
  padding: 14px;
  display: flex;
  flex-direction: column;
  transition: border-color .18s ease, transform .18s ease;
}

.pelican-card:hover {
  border-color: var(--rule);
  transform: translateY(-2px);
}

.pelican-card.is-highlight {
  border-color: var(--ink);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.04);
}

.pelican-card.is-max {
  border-color: var(--accent);
}

.pelican-card-head {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  gap: 6px;
  margin-bottom: 10px;
}

.pelican-level {
  font-family: 'PT Serif', Georgia, serif;
  font-size: 1.2em;
  font-weight: 700;
  color: var(--ink);
  line-height: 1;
}

.pelican-tag {
  font: 400 10px/1.3 'PT Mono', monospace;
  color: var(--muted);
  background: var(--card);
  padding: 2px 6px;
  border-radius: 3px;
  border: 1px solid var(--hairline);
  white-space: nowrap;
}

.pelican-tag.tag-code {
  color: var(--bar-text);
  background: var(--bar);
  border-color: var(--bar);
  font-weight: 700;
}

.pelican-tag.tag-max {
  color: var(--accent);
  background: var(--card);
  border-color: var(--accent);
  font-weight: 700;
}

.pelican-media {
  aspect-ratio: 4/3;
  width: 100%;
  border-radius: 4px;
  overflow: hidden;
  background: var(--card);
  border: 1px solid var(--hairline);
  margin-bottom: 12px;
}

.pelican-media img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  display: block;
}

.pelican-stats {
  font: 700 13px/1.4 'PT Mono', monospace;
  color: var(--ink);
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 8px;
  padding-bottom: 8px;
  border-bottom: 1px solid var(--hairline);
}

.pelican-stat-sep {
  color: var(--muted);
  font-weight: 400;
}

.pelican-desc {
  font-size: 12.5px;
  line-height: 1.45;
  color: var(--muted);
  margin: 0;
  flex: 1;
}

.pelican-desc strong {
  color: var(--ink);
}

.pelican-caption {
  padding-top: 16px;
  border-top: 1px solid var(--hairline);
  font-size: 13.5px;
  line-height: 1.55;
  color: var(--muted);
}

.pelican-caption strong {
  color: var(--ink);
}

@media (max-width: 1080px) {
  .pelican-grid {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}

@media (max-width: 640px) {
  .pelican-grid {
    grid-template-columns: 1fr;
  }
  .pelican-hero-box {
    padding: 18px 14px;
  }
}

/* --- 2. СЕКЦИЯ БОЕВЫХ ВИДЕО (#video-zhir) --- */
.video-zhir-section {
  position: relative;
  overflow: hidden;
  padding: 68px 0 74px;
  margin: 56px 0 64px;
  background: #111214;
  border-top: 1px solid var(--rule);
  border-bottom: 1px solid var(--rule);
  color: #f4f4f5;
  scroll-margin-top: 80px;
}

/* Приглушённая сетка из 12 скриншотов на фоне */
.vwall-ambient-backdrop {
  position: absolute;
  inset: -10px;
  z-index: 1;
  pointer-events: none;
  overflow: hidden;
}

.vwall-mosaic-grid {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 12px;
  width: 104%;
  height: 104%;
  margin-left: -2%;
  opacity: 0.25;
  filter: blur(2px);
}

.vwall-ambient-tile {
  position: relative;
  border-radius: 4px;
  overflow: hidden;
  background: #1c1d21;
  aspect-ratio: 16/10;
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.vwall-ambient-tile img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.vwall-backdrop-overlay {
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at center, rgba(17, 18, 20, 0.6) 0%, rgba(17, 18, 20, 0.9) 85%);
}

/* Контент поверх видеостены */
.vwall-content-wrap {
  position: relative;
  z-index: 2;
  max-width: 1100px;
  margin: 0 auto;
  padding: 0 20px;
}

.vwall-head-box {
  text-align: center;
  max-width: 760px;
  margin: 0 auto 36px;
}

.vwall-kicker {
  font: 400 12px/1.4 'PT Mono', monospace;
  color: #a1a1aa;
  text-transform: uppercase;
  letter-spacing: .08em;
  margin: 0 0 8px;
}

.vwall-title {
  font-family: 'PT Serif', Georgia, serif;
  font-size: 2.1em;
  font-weight: 700;
  color: #ffffff !important;
  margin: 0 0 12px;
  line-height: 1.25;
  letter-spacing: -.01em;
}

.vwall-intro {
  font-size: 1.05em;
  line-height: 1.55;
  color: #d4d4d8;
  margin: 0;
}

/* 2 больших чистых плеера */
.vwall-cards-row {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
}

@media (max-width: 860px) {
  .vwall-cards-row {
    grid-template-columns: 1fr;
  }
}

.vwall-card {
  background: #18191c;
  border: 1px solid rgba(255, 255, 255, 0.14);
  border-radius: 8px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.vwall-card-header {
  padding: 16px 18px 12px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.vwall-card-title {
  font-family: 'PT Serif', Georgia, serif;
  font-size: 1.25em;
  font-weight: 700;
  color: #ffffff;
  margin: 0 0 4px;
}

.vwall-card-author {
  font: 400 12px/1.4 'PT Mono', monospace;
  color: #a1a1aa;
}

.vwall-card-author a {
  color: #f4f4f5;
  text-decoration: underline;
  text-underline-offset: 2px;
}

.vwall-video-wrap {
  position: relative;
  background: #000;
  width: 100%;
}

.vwall-video-wrap video {
  width: 100%;
  height: auto;
  display: block;
}

.vwall-card-body {
  padding: 16px 18px 18px;
  display: flex;
  flex-direction: column;
  flex: 1;
}

.vwall-card-body p {
  font-size: 14.5px;
  line-height: 1.5;
  color: #d4d4d8;
  margin: 0 0 16px;
  flex: 1;
}

.vwall-metrics {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
  background: #202226;
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 6px;
  padding: 10px 12px;
}

.vwall-metric-item {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.vwall-metric-val {
  font: 700 13.5px/1.2 'PT Mono', monospace;
  color: #ffffff;
}

.vwall-metric-lbl {
  font: 400 10px/1.2 'PT Mono', monospace;
  color: #a1a1aa;
  text-transform: uppercase;
  letter-spacing: .04em;
}
</style>
"""

    # JavaScript block
    scripts = """<script>
(function(){
  const dock = document.getElementById('liquidDock');
  if (!dock) return;

  const trigger = document.getElementById('liquidDockTrigger');
  const topBtn = document.getElementById('liquidDockTop');
  const curNum = document.getElementById('liquidDockCurNum');
  const curTitle = document.getElementById('liquidDockCurTitle');
  const links = dock.querySelectorAll('.liquid-dock-link');
  const toc = document.querySelector('nav.toc');

  const sectionMeta = {
    'model': { num: '01', title: 'Модель Fable 5.1', linkId: 'model' },
    'reliz': { num: '01', title: 'Что вышло', linkId: 'model' },
    'usilie': { num: '02', title: 'Бенчмарки', linkId: 'usilie' },
    'nauka': { num: '03', title: 'Научные открытия', linkId: 'nauka' },
    'oblasti': { num: '04', title: 'Кейсы партнёров', linkId: 'oblasti' },
    'coding': { num: '04', title: 'Кейсы: Кодинг', linkId: 'oblasti' },
    'debug': { num: '04', title: 'Кейсы: Отладка', linkId: 'oblasti' },
    'research': { num: '04', title: 'Кейсы: Исследования', linkId: 'oblasti' },
    'finance': { num: '04', title: 'Кейсы: Финансы', linkId: 'oblasti' },
    'writing': { num: '04', title: 'Кейсы: Письмо', linkId: 'oblasti' },
    'agents': { num: '04', title: 'Кейсы: Агенты', linkId: 'oblasti' },
    'price': { num: '04', title: 'Кейсы: Экономика', linkId: 'oblasti' },
    'video-zhir': { num: '05', title: 'Боевые видео', linkId: 'video-zhir' },
    'syscard': { num: '06', title: 'Системная карта', linkId: 'syscard' },
    'prompting': { num: '07', title: 'Промптинг', linkId: 'prompting' },
    'otzyvy': { num: '08', title: 'Пеликаны Willison', linkId: 'otzyvy' },
    'otzyvy-x': { num: '09', title: 'Отзывы в X', linkId: 'otzyvy-x' },
    'istochniki': { num: '09', title: 'Первоисточник', linkId: 'otzyvy-x' }
  };

  function setActiveSection(id) {
    const meta = sectionMeta[id];
    if (!meta) return;
    if (curNum) curNum.textContent = meta.num;
    if (curTitle) curTitle.textContent = meta.title;
    links.forEach(l => {
      if (l.getAttribute('data-section') === meta.linkId) {
        l.classList.add('is-active');
      } else {
        l.classList.remove('is-active');
      }
    });
  }

  function checkVisibility() {
    if (!toc) return;
    const rect = toc.getBoundingClientRect();
    if (rect.bottom < 40) {
      dock.classList.add('is-visible');
    } else {
      dock.classList.remove('is-visible');
      dock.classList.remove('is-open');
      if (trigger) trigger.setAttribute('aria-expanded', 'false');
    }
  }

  window.addEventListener('scroll', checkVisibility, { passive: true });
  window.addEventListener('resize', checkVisibility, { passive: true });
  checkVisibility();

  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          setActiveSection(entry.target.id);
        }
      });
    }, {
      rootMargin: '-10% 0px -75% 0px',
      threshold: 0
    });

    Object.keys(sectionMeta).forEach(id => {
      const el = document.getElementById(id);
      if (el) observer.observe(el);
    });
  }

  if (trigger) {
    trigger.addEventListener('click', (e) => {
      e.stopPropagation();
      const isOpen = dock.classList.toggle('is-open');
      trigger.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    });
  }

  document.addEventListener('click', (e) => {
    if (!dock.contains(e.target) && dock.classList.contains('is-open')) {
      dock.classList.remove('is-open');
      if (trigger) trigger.setAttribute('aria-expanded', 'false');
    }
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && dock.classList.contains('is-open')) {
      dock.classList.remove('is-open');
      if (trigger) {
        trigger.setAttribute('aria-expanded', 'false');
        trigger.focus();
      }
    }
  });

  if (topBtn) {
    topBtn.addEventListener('click', () => {
      dock.classList.remove('is-open');
      if (trigger) trigger.setAttribute('aria-expanded', 'false');
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  links.forEach(link => {
    link.addEventListener('click', () => {
      dock.classList.remove('is-open');
      if (trigger) trigger.setAttribute('aria-expanded', 'false');
    });
  });
})();
</script>

<script>
document.querySelectorAll('.carousel').forEach(c=>{const t=c.querySelector('.track');const cards=()=>t.querySelectorAll('.card');const w=()=>cards()[0].getBoundingClientRect().width+14;
const ctr=document.createElement('div');ctr.className='counter';t.after(ctr);c.tabIndex=0;
const upd=()=>{const n=cards().length;const i=Math.min(n,Math.round(t.scrollLeft/w())+1);ctr.textContent=i+' из '+n};upd();t.addEventListener('scroll',upd,{passive:true});window.addEventListener('resize',upd);
const go=d=>t.scrollBy({left:d*w()});c.querySelector('.prev').onclick=()=>go(-1);c.querySelector('.next').onclick=()=>go(1);
let hover=false;c.addEventListener('mouseenter',()=>hover=true);c.addEventListener('mouseleave',()=>hover=false);
const key=e=>{if(!(hover||c.contains(document.activeElement)))return;if(e.key==='ArrowLeft'){e.preventDefault();go(-1)}else if(e.key==='ArrowRight'){e.preventDefault();go(1)}};
document.addEventListener('keydown',key);});
(()=>{const b=document.getElementById('themeBtn');const h=document.documentElement;const cur=()=>h.getAttribute('data-theme')||(matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light');
const paint=()=>{b.textContent=cur()==='dark'?'☀':'☾'};paint();
b.onclick=()=>{const n=cur()==='dark'?'light':'dark';h.setAttribute('data-theme',n);try{localStorage.setItem('theme',n)}catch(e){}paint()};
matchMedia('(prefers-color-scheme: dark)').addEventListener('change',paint);})();
</script>

<script>
(function(){
  function fit(c){
    const t=c.querySelector('.track'); if(!t) return;
    const r=t.getBoundingClientRect(); let h=0;
    t.querySelectorAll('.card').forEach(k=>{
      const b=k.getBoundingClientRect();
      if(b.right>r.left+8 && b.left<r.right-8) {
        h=Math.max(h, k.scrollHeight || k.offsetHeight);
      }
    });
    if(h) t.style.height=(h+24)+'px';
  }
  const all=[...document.querySelectorAll('.carousel')];
  all.forEach(c=>{
    const t=c.querySelector('.track');
    let raf;
    t.addEventListener('scroll',()=>{cancelAnimationFrame(raf); raf=requestAnimationFrame(()=>fit(c));}, {passive:true});
    c.querySelectorAll('img').forEach(m=>m.addEventListener('load',()=>fit(c)));
    c.querySelectorAll('video').forEach(v=>{
      v.addEventListener('loadedmetadata',()=>fit(c));
      v.addEventListener('loadeddata',()=>fit(c));
    });
    if(window.ResizeObserver){
      new ResizeObserver(()=>fit(c)).observe(t);
    }
  });
  const fitAll=()=>all.forEach(fit);
  window.addEventListener('resize',fitAll);
  window.addEventListener('load',fitAll);
  if(document.fonts && document.fonts.ready){
    document.fonts.ready.then(fitAll);
  }
  fitAll();
  setTimeout(fitAll,300);
  setTimeout(fitAll,1000);
  setTimeout(fitAll,2500);
})();
</script>
<script>
document.querySelectorAll('.copy-btn').forEach(b=>b.addEventListener('click',async()=>{const code=b.closest('.prompt').querySelector('code').innerText;try{await navigator.clipboard.writeText(code);b.textContent='Скопировано';setTimeout(()=>b.textContent='Скопировать',1500);}catch(e){b.textContent='Не вышло';}}));
</script>

<script>
// Bento Grid Interactive Pill Filter
(function() {
  const pills = document.querySelectorAll('.bento-pill');
  const sections = document.querySelectorAll('.bento-category-section');
  if (!pills.length || !sections.length) return;

  function applyFilter(cat, updateHash) {
    pills.forEach(p => {
      const active = p.dataset.filter === cat;
      p.classList.toggle('active', active);
      p.setAttribute('aria-selected', active ? 'true' : 'false');
    });

    sections.forEach(sec => {
      if (cat === 'all') {
        sec.style.display = '';
      } else {
        sec.style.display = (sec.dataset.category === cat) ? '' : 'none';
      }
    });

    if (updateHash && cat !== 'all') {
      history.replaceState(null, '', '#' + cat);
    } else if (updateHash && cat === 'all') {
      history.replaceState(null, '', window.location.pathname);
    }
  }

  pills.forEach(p => {
    p.addEventListener('click', () => {
      const cat = p.dataset.filter;
      applyFilter(cat, true);
    });
  });

  function checkHash() {
    const hash = window.location.hash.replace('#', '');
    const validCats = ['coding', 'debug', 'research', 'finance', 'writing', 'agents', 'price'];
    if (validCats.includes(hash)) {
      applyFilter(hash, false);
      const targetSec = document.getElementById(hash);
      if (targetSec) {
        setTimeout(() => targetSec.scrollIntoView({ behavior: 'smooth', block: 'start' }), 100);
      }
    }
  }

  window.addEventListener('hashchange', checkHash);
  if (window.location.hash) checkHash();
})();
</script>
"""

    # Assemble Hugo post
    hugo_post = (
        frontmatter +
        header_nav +
        pelican_hero +
        toc +
        model_to_oblasti +
        bento_html +
        syscard_to_prompting +
        otzyvy_section +
        video_zhir_section +
        otzyvy_x_to_sources +
        liquid_dock_html +
        custom_css +
        scripts
    )

    with open('content/blog/claude-fable-5-1-v1.html', 'w', encoding='utf-8') as f:
        f.write(hugo_post)
    print("Successfully wrote content/blog/claude-fable-5-1-v1.html")

    # Assemble standalone preview for static/design-review/variant-1.html
    standalone_prefix = """<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Обзор Claude Fable 5.1 [Вариант 1: Редакционная классика] | sereja.tech</title>
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <meta name="theme-color" content="#141414" media="(prefers-color-scheme: dark)">
  <meta name="theme-color" content="#fffef9" media="(prefers-color-scheme: light)">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=PT+Serif:ital,wght@0,400;0,700;1,400&family=PT+Mono&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/css/paper.css">
  <script>try{var t=localStorage.getItem("theme");if(t)document.documentElement.setAttribute("data-theme",t)}catch(e){}</script>
</head>
<body class="kind-page section-blog paper">
  <nav class="site-top" aria-label="Основная навигация">
    <a class="wordmark" href="/">Сережа Рис</a>
    <span class="site-links">
      <a href="/blog/">Блог</a>
      <a href="/about/">Обо мне</a>
      <a href="https://t.me/ris_ai" target="_blank" rel="noopener">Телеграм</a>
    </span>
  </nav>

  <main>
"""

    standalone_suffix = """  </main>

  <footer class="site-bottom">
    <span>© 2026 Сережа Рис · sereja.tech</span>
    <span class="site-links">
      <a href="https://t.me/ris_ai?utm_source=sereja_tech&utm_medium=link&utm_campaign=footer" target="_blank" rel="noopener">Телеграм</a>
      <a href="https://www.youtube.com/@serejaris?utm_source=sereja_tech&utm_medium=link&utm_campaign=footer" target="_blank" rel="noopener">YouTube</a>
      <a href="https://t.me/vibecod3rs?utm_source=sereja_tech&utm_medium=link&utm_campaign=footer" target="_blank" rel="noopener">Вайбкодеры</a>
      <a href="https://github.com/serejaris" target="_blank" rel="noopener">GitHub</a>
      <a href="/index.xml">RSS</a>
    </span>
  </footer>
</body>
</html>
"""

    standalone_preview = (
        standalone_prefix +
        header_nav +
        pelican_hero +
        toc +
        model_to_oblasti +
        bento_html +
        syscard_to_prompting +
        otzyvy_section +
        video_zhir_section +
        otzyvy_x_to_sources +
        liquid_dock_html +
        custom_css +
        scripts +
        standalone_suffix
    )

    with open('static/design-review/variant-1.html', 'w', encoding='utf-8') as f:
        f.write(standalone_preview)
    print("Successfully wrote static/design-review/variant-1.html")

if __name__ == '__main__':
    build_variant_1()
