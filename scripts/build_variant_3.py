#!/usr/bin/env python3
"""
Builder for Variant 3: Фокусная инфографика (Pure Visual Progression)
Purges decorative nonsense, fake CAD crosshairs, sci-fi HUDs, and English buzzwords.
Applies pure Swiss editorial typography ('PT Serif' text, 'PT Mono' meta/numbers, paper theme).

Outputs:
  - content/blog/claude-fable-5-1-v3.html (Hugo post with frontmatter)
  - static/design-review/variant-3.html (Standalone static preview)
"""

import os
import re

# Read base and v1 files
with open('content/blog/claude-fable-5-1.html', 'r', encoding='utf-8') as f:
    base = f.read()

with open('content/blog/claude-fable-5-1-v1.html', 'r', encoding='utf-8') as f:
    v1 = f.read()

# 1. Extract Bento Grid from v1 (between bentoApp start and syscard start)
bento_start = v1.find('<div class="bento-container" id="bentoApp">')
bento_end = v1.find('<div class="page"><section id="syscard">')
bento_html = v1[bento_start:bento_end]

# 2. Extract sections from base:
#    model_to_nauka: #model, #reliz, #usilie, #nauka (up to oblasti)
idx_model = base.find('<section id="model"')
idx_oblasti_head = base.find('<section id="oblasti">')
idx_oblasti_svg_end = base.find('</section>\n</div>', idx_oblasti_head) + len('</section>\n</div>')
model_to_nauka = base[idx_model:idx_oblasti_svg_end]

# Add quiet editorial figure of official artwork to reliz
birds_figure = """
<figure class="hero-art" style="max-width:540px;margin:24px auto;">
  <img width="671" height="672" src="/images/blog/fable51/anthropic-birds-clean.png" alt="Официальная гравюра релиза Claude Fable 5.1 и Claude Mythos 5.1 · Anthropic">
  <figcaption>Официальная гравюра Anthropic: символ двух конфигураций единых весов модели</figcaption>
</figure>
"""
if '<figure class="hero-art"' not in model_to_nauka:
    needle = 'по программам доступа для кибербезопасности и наук о жизни.</p>'
    pos = model_to_nauka.find(needle)
    if pos != -1:
        model_to_nauka = model_to_nauka[:pos + len(needle)] + "\n" + birds_figure + model_to_nauka[pos + len(needle):]

# 3. Extract syscard and prompting from base:
#    syscard_to_prompting: from syscard start up to otzyvy
idx_syscard = base.find('<div class="page"><section id="syscard">')
idx_otzyvy = base.find('<div class="page"><section id="otzyvy">')
syscard_to_prompting = base[idx_syscard:idx_otzyvy]

# 4. Clean Simon Willison section in #otzyvy:
#    Refers to the top progression hero without repeating the rough carousel
otzyvy_html = """
<div class="page"><section id="otzyvy"><h2>Пеликаны и первые отзывы</h2>
<h3>Simon Willison: пеликан на велосипеде по пяти уровням усилия</h3>
<p><a href="https://simonwillison.net/2026/Sep/1/claude-fable-5-1/" target="_blank" rel="noopener">Simon Willison</a> прогнал один и тот же промпт на всех пяти уровнях усилия и заметил, что на low и medium в ответе нет следов extended thinking, а с xhigh вычисления раскручиваются в десятки раз по токенам и цене.</p>
<p>Визуальный разбор всех пяти генераций с точными метриками времени и стоимости вынесен в <a href="#visualProgression">инфографику в начале статьи</a>. На максимальном уровне модель за 14 минут непрерывных размышлений самостоятельно добавила шлем, корзину с рыбой и ноги по обе стороны рамы на педалях.</p>
<p>Анимацию он попросил следующим промптом "animate this" на уровне high за $1.37. Сравнения с прошлыми моделями в посте нет, есть одна оговорка: до размаха Gemini 3.7 Flash пеликан не дотягивает. Картинки из его теста.</p>
</section></div>
"""

# 5. Extract otzyvy-x and istochniki from base:
idx_otzyvy_x = base.find('<section id="otzyvy-x">')
idx_liquid_dock = base.find('<!-- Liquid Glass Floating Navigation Dock -->')
otzyvy_x_to_istochniki = base[idx_otzyvy_x:idx_liquid_dock]

# 6. Extract liquid dock HTML and JS from base
liquid_dock_html_and_js = base[idx_liquid_dock:]

# 7. Hero section HTML: Pure Visual Progression (The 5 Pelicans)
hero_progression_html = """
<div class="pvp-hero-container" id="visualProgression">
  <div class="pvp-intro-block">
    <span class="pvp-intro-kicker">Стресс-тест Саймона Уиллисона · Запрос: «Пеликан на велосипеде в SVG»</span>
    <h2 class="pvp-intro-title">Визуальная прогрессия мышления: от скетча до полной автономии</h2>
    <p class="pvp-intro-text">Один и тот же запрос на пяти уровнях усилия (effort). Наглядно виден резкий перелом: первые три режима укладываются в полминуты без глубоких рассуждений, а на XHigh и Max начинается многоминутная автономная прорисовка деталей.</p>
  </div>

  <!-- Compute Progression Summary Strip -->
  <div class="pvp-summary-strip" role="region" aria-label="Сводка вычислительной прогрессии">
    <div class="pvp-summary-grid">
      <div class="pvp-summary-item">
        <span class="psi-label">Рост времени</span>
        <strong class="psi-val">23 с ➔ 13 мин 54 с</strong>
        <span class="psi-sub">+3 526% времени</span>
      </div>
      <div class="pvp-summary-item">
        <span class="psi-label">Рост стоимости</span>
        <strong class="psi-val">$0.10 ➔ $3.30</strong>
        <span class="psi-sub">в 33 раза дороже</span>
      </div>
      <div class="pvp-summary-item">
        <span class="psi-label">Токены рассуждений</span>
        <strong class="psi-val">0 ➔ 32 000 токенов</strong>
        <span class="psi-sub">от скетча до корзины и шлема</span>
      </div>
      <div class="pvp-summary-item">
        <span class="psi-label">Вердикт теста</span>
        <strong class="psi-val">Лучший SVG Anthropic</strong>
        <span class="psi-sub">но Gemini 3.7 шире</span>
      </div>
    </div>

    <!-- Proportional Timeline Scale illustrating the 15x compute jump -->
    <div class="pvp-scale-bar" aria-hidden="true">
      <div class="pvp-scale-labels">
        <span>Быстрый диапазон (23–30 с)</span>
        <span>Скачок в 15 раз (7 мин 51 с)</span>
        <span>Пик автономии (13 мин 54 с)</span>
      </div>
      <div class="pvp-scale-track">
        <div class="pvp-scale-seg fast-range" title="Быстрый диапазон: 23–30 с"></div>
        <div class="pvp-scale-seg jump-range" title="Глубокие вычисления: от 8 до 14 минут"></div>
      </div>
    </div>
  </div>

  <!-- 5 Pelicans Cards Grid -->
  <div class="pvp-cards-grid" role="region" aria-label="Сетка пяти уровней усилия мышления">
    
    <!-- 01: Low -->
    <article class="pvp-card" data-effort="low">
      <div class="pvp-card-head">
        <div class="pvp-card-top-row">
          <div class="pvp-card-title-group">
            <span class="pvp-card-num">01</span>
            <h3 class="pvp-card-level">Low</h3>
          </div>
          <span class="pvp-card-micro-stat">24 с · $0.10</span>
        </div>
        <span class="pvp-tag quiet">без рассуждений</span>
      </div>
      <div class="pvp-card-media">
        <img width="914" height="686" src="/images/blog/fable51/pelikan-low.png" alt="Пеликан на велосипеде, Low (24 с, $0.10)" loading="eager">
        <div class="pvp-media-meta">24 с · $0.10</div>
      </div>
      <div class="pvp-card-body">
        <div class="pvp-stats-row">
          <div class="pvp-stat"><span class="pvp-stat-val">24 с</span><span class="pvp-stat-lbl">время</span></div>
          <div class="pvp-stat"><span class="pvp-stat-val">$0.10</span><span class="pvp-stat-lbl">цена</span></div>
          <div class="pvp-stat"><span class="pvp-stat-val">0</span><span class="pvp-stat-lbl">токенов</span></div>
        </div>
        <div class="pvp-meter" aria-hidden="true">
          <div class="pvp-meter-fill" style="width: 2.9%"></div>
        </div>
        <p class="pvp-card-text">Без рассуждений. Схематичный набросок за секунды. Контур птицы оторван от рамы, колёса без спиц, цепи и педалей нет.</p>
      </div>
    </article>

    <!-- 02: Medium -->
    <article class="pvp-card" data-effort="medium">
      <div class="pvp-card-head">
        <div class="pvp-card-top-row">
          <div class="pvp-card-title-group">
            <span class="pvp-card-num">02</span>
            <h3 class="pvp-card-level">Medium</h3>
          </div>
          <span class="pvp-card-micro-stat">23 с · $0.10</span>
        </div>
        <span class="pvp-tag quiet">без рассуждений</span>
      </div>
      <div class="pvp-card-media">
        <img width="914" height="686" src="/images/blog/fable51/pelikan-medium.png" alt="Пеликан на велосипеде, Medium (23 с, $0.10)" loading="eager">
        <div class="pvp-media-meta">23 с · $0.10</div>
      </div>
      <div class="pvp-card-body">
        <div class="pvp-stats-row">
          <div class="pvp-stat"><span class="pvp-stat-val">23 с</span><span class="pvp-stat-lbl">время</span></div>
          <div class="pvp-stat"><span class="pvp-stat-val">$0.10</span><span class="pvp-stat-lbl">цена</span></div>
          <div class="pvp-stat"><span class="pvp-stat-val">0</span><span class="pvp-stat-lbl">токенов</span></div>
        </div>
        <div class="pvp-meter" aria-hidden="true">
          <div class="pvp-meter-fill" style="width: 2.8%"></div>
        </div>
        <p class="pvp-card-text">Без рассуждений. Мгновенный ответ: птица сдвинута ближе к рулю, но признаков extended thinking нет. Геометрия на уровне Fable 5.</p>
      </div>
    </article>

    <!-- 03: High -->
    <article class="pvp-card" data-effort="high">
      <div class="pvp-card-head">
        <div class="pvp-card-top-row">
          <div class="pvp-card-title-group">
            <span class="pvp-card-num">03</span>
            <h3 class="pvp-card-level">High</h3>
          </div>
          <span class="pvp-card-micro-stat">30 с · $0.13</span>
        </div>
        <span class="pvp-tag standard">стандартный режим</span>
      </div>
      <div class="pvp-card-media">
        <img width="914" height="686" src="/images/blog/fable51/pelikan-high.png" alt="Пеликан на велосипеде, High (30 с, $0.13)" loading="eager">
        <div class="pvp-media-meta">30 с · $0.13</div>
      </div>
      <div class="pvp-card-body">
        <div class="pvp-stats-row">
          <div class="pvp-stat"><span class="pvp-stat-val">30 с</span><span class="pvp-stat-lbl">время</span></div>
          <div class="pvp-stat"><span class="pvp-stat-val">$0.13</span><span class="pvp-stat-lbl">цена</span></div>
          <div class="pvp-stat"><span class="pvp-stat-val">~850</span><span class="pvp-stat-lbl">токенов</span></div>
        </div>
        <div class="pvp-meter" aria-hidden="true">
          <div class="pvp-meter-fill" style="width: 3.6%"></div>
        </div>
        <p class="pvp-card-text">Стандартный режим Claude Code. Первые циклы рассуждений: появляются спицы, рама, седло и узнаваемый силуэт клюва.</p>
      </div>
    </article>

    <!-- 04: XHigh -->
    <article class="pvp-card is-jump" data-effort="xhigh">
      <div class="pvp-card-head">
        <div class="pvp-card-top-row">
          <div class="pvp-card-title-group">
            <span class="pvp-card-num">04</span>
            <h3 class="pvp-card-level">XHigh</h3>
          </div>
          <span class="pvp-card-micro-stat highlight">7м 51с · $1.83</span>
        </div>
        <span class="pvp-tag jump">скачок в 15 раз</span>
      </div>
      <div class="pvp-card-media">
        <img width="914" height="686" src="/images/blog/fable51/pelikan-xhigh.png" alt="Пеликан на велосипеде, XHigh (7 мин 51 с, $1.83)" loading="lazy">
        <div class="pvp-media-meta highlight">7 мин 51 с · $1.83</div>
      </div>
      <div class="pvp-card-body">
        <div class="pvp-stats-row">
          <div class="pvp-stat"><span class="pvp-stat-val">7м 51с</span><span class="pvp-stat-lbl">время</span></div>
          <div class="pvp-stat"><span class="pvp-stat-val">$1.83</span><span class="pvp-stat-lbl">цена</span></div>
          <div class="pvp-stat"><span class="pvp-stat-val">~16k</span><span class="pvp-stat-lbl">токенов</span></div>
        </div>
        <div class="pvp-meter" aria-hidden="true">
          <div class="pvp-meter-fill is-jump-fill" style="width: 56.5%"></div>
        </div>
        <p class="pvp-card-text">Скачок в 15 раз. Почти 8 минут рассуждений: многослойные перья, анатомия клюва, тормозные тросы и объёмные трубы велосипеда.</p>
      </div>
    </article>

    <!-- 05: Max -->
    <article class="pvp-card is-peak" data-effort="max">
      <div class="pvp-card-head">
        <div class="pvp-card-top-row">
          <div class="pvp-card-title-group">
            <span class="pvp-card-num">05</span>
            <h3 class="pvp-card-level">Max</h3>
          </div>
          <span class="pvp-card-micro-stat peak-text">13м 54с · $3.30</span>
        </div>
        <span class="pvp-tag peak">пик автономии: шлем, корзина, педали</span>
      </div>
      <div class="pvp-card-media">
        <img width="914" height="686" src="/images/blog/fable51/pelikan-max.webp" alt="Пеликан на велосипеде, Max (13 мин 54 с, $3.30)" loading="lazy">
        <div class="pvp-media-meta peak-meta">13 мин 54 с · $3.30</div>
      </div>
      <div class="pvp-card-body">
        <div class="pvp-stats-row">
          <div class="pvp-stat"><span class="pvp-stat-val">13м 54с</span><span class="pvp-stat-lbl">время</span></div>
          <div class="pvp-stat"><span class="pvp-stat-val">$3.30</span><span class="pvp-stat-lbl">цена</span></div>
          <div class="pvp-stat"><span class="pvp-stat-val">32 000</span><span class="pvp-stat-lbl">токенов</span></div>
        </div>
        <div class="pvp-meter" aria-hidden="true">
          <div class="pvp-meter-fill is-peak-fill" style="width: 100%"></div>
        </div>
        <p class="pvp-card-text">Пик автономии: 14 минут размышлений. Модель сама дополнила сюжет: надела защитный шлем, повесила спереди корзину со свежей рыбой и поставила ноги на педали.</p>
      </div>
    </article>

  </div>
</div>
"""

# 8. Video section HTML: Quiet Background Video Wall + 2 Honest Foreground Video Blocks
video_wall_html = """
<section id="video-zhir" class="quiet-video-wall-section">
  <!-- Quiet Background Video Wall Backdrop (Tiled real community experiments from X) -->
  <div class="ambient-video-track-wrap" aria-hidden="true">
    <div class="ambient-marquee-row row-left" id="ambientRowLeft">
      <div class="ambient-tile"><img src="/images/blog/fable51/bridgemindai-poster.jpg" alt="" loading="lazy"><span class="ambient-tile-label">@bridgemindai · Mario Kart</span></div>
      <div class="ambient-tile"><img src="/images/blog/fable51/knowixbuilds-poster.jpg" alt="" loading="lazy"><span class="ambient-tile-label">@knowixbuilds · 2.4M Voxels</span></div>
      <div class="ambient-tile"><img src="/images/blog/fable51/spicey_lemonade-poster.jpg" alt="" loading="lazy"><span class="ambient-tile-label">@spicey_lemonade · Minecraft</span></div>
      <div class="ambient-tile"><img src="/images/blog/fable51/superalesha-poster.jpg" alt="" loading="lazy"><span class="ambient-tile-label">@superalesha · Three.js FPS</span></div>
      <div class="ambient-tile"><img src="/images/blog/fable51/llmjunky-poster.jpg" alt="" loading="lazy"><span class="ambient-tile-label">@LLMJunky · Rocket League</span></div>
      <div class="ambient-tile"><img src="/images/blog/fable51/techartist_-poster.jpg" alt="" loading="lazy"><span class="ambient-tile-label">@techartist_ · Mount Fuji 3D</span></div>
      <div class="ambient-tile"><img src="/images/blog/fable51/omedvibecodes-arena-poster.jpg" alt="" loading="lazy"><span class="ambient-tile-label">@OmedVibeCodes · Hardcore Arena</span></div>
      <div class="ambient-tile"><img src="/images/blog/fable51/bijanbowen-poster.jpg" alt="" loading="lazy"><span class="ambient-tile-label">@bijanbowen · Subway FPS</span></div>
      <!-- Duplicate for seamless continuous movement -->
      <div class="ambient-tile"><img src="/images/blog/fable51/bridgemindai-poster.jpg" alt="" loading="lazy"><span class="ambient-tile-label">@bridgemindai · Mario Kart</span></div>
      <div class="ambient-tile"><img src="/images/blog/fable51/knowixbuilds-poster.jpg" alt="" loading="lazy"><span class="ambient-tile-label">@knowixbuilds · 2.4M Voxels</span></div>
      <div class="ambient-tile"><img src="/images/blog/fable51/spicey_lemonade-poster.jpg" alt="" loading="lazy"><span class="ambient-tile-label">@spicey_lemonade · Minecraft</span></div>
      <div class="ambient-tile"><img src="/images/blog/fable51/superalesha-poster.jpg" alt="" loading="lazy"><span class="ambient-tile-label">@superalesha · Three.js FPS</span></div>
      <div class="ambient-tile"><img src="/images/blog/fable51/llmjunky-poster.jpg" alt="" loading="lazy"><span class="ambient-tile-label">@LLMJunky · Rocket League</span></div>
      <div class="ambient-tile"><img src="/images/blog/fable51/techartist_-poster.jpg" alt="" loading="lazy"><span class="ambient-tile-label">@techartist_ · Mount Fuji 3D</span></div>
      <div class="ambient-tile"><img src="/images/blog/fable51/omedvibecodes-arena-poster.jpg" alt="" loading="lazy"><span class="ambient-tile-label">@OmedVibeCodes · Hardcore Arena</span></div>
      <div class="ambient-tile"><img src="/images/blog/fable51/bijanbowen-poster.jpg" alt="" loading="lazy"><span class="ambient-tile-label">@bijanbowen · Subway FPS</span></div>
    </div>

    <div class="ambient-marquee-row row-right" id="ambientRowRight">
      <div class="ambient-tile"><img src="/images/blog/fable51/harshithlucky3-poster.jpg" alt="" loading="lazy"><span class="ambient-tile-label">@HarshithLucky3 · Airbus H145</span></div>
      <div class="ambient-tile"><img src="/images/blog/fable51/holytrinity-poster.jpg" alt="" loading="lazy"><span class="ambient-tile-label">@holytrinity · Корабль в бутылке</span></div>
      <div class="ambient-tile"><img src="/images/blog/fable51/skrinshot-iz-posta-tuanaiseo.jpg" alt="" loading="lazy"><span class="ambient-tile-label">@tuanaiseo · Cities: Skylines</span></div>
      <div class="ambient-tile"><img src="/images/blog/fable51/skrinshot-iz-posta-demosthenes2010.jpg" alt="" loading="lazy"><span class="ambient-tile-label">@demosthenes2010 · 99 агентов</span></div>
      <div class="ambient-tile"><img src="/images/blog/fable51/skrinshot-iz-posta-claudiudp.jpg" alt="" loading="lazy"><span class="ambient-tile-label">@ClaudiuDP · 10 субагентов</span></div>
      <div class="ambient-tile"><img src="/images/blog/fable51/skrinshot-iz-posta-lakr233.jpg" alt="" loading="lazy"><span class="ambient-tile-label">@Lakr233 · Отладка iGhostVT</span></div>
      <div class="ambient-tile"><img src="/images/blog/fable51/skrinshot-iz-posta-dotey.jpg" alt="" loading="lazy"><span class="ambient-tile-label">@dotey · 1M контекст</span></div>
      <div class="ambient-tile"><img src="/images/blog/fable51/skrinshot-iz-posta-kenn.jpg" alt="" loading="lazy"><span class="ambient-tile-label">@kenn · Кэш 80x дешевле</span></div>
      <!-- Duplicate for seamless continuous movement -->
      <div class="ambient-tile"><img src="/images/blog/fable51/harshithlucky3-poster.jpg" alt="" loading="lazy"><span class="ambient-tile-label">@HarshithLucky3 · Airbus H145</span></div>
      <div class="ambient-tile"><img src="/images/blog/fable51/holytrinity-poster.jpg" alt="" loading="lazy"><span class="ambient-tile-label">@holytrinity · Корабль в бутылке</span></div>
      <div class="ambient-tile"><img src="/images/blog/fable51/skrinshot-iz-posta-tuanaiseo.jpg" alt="" loading="lazy"><span class="ambient-tile-label">@tuanaiseo · Cities: Skylines</span></div>
      <div class="ambient-tile"><img src="/images/blog/fable51/skrinshot-iz-posta-demosthenes2010.jpg" alt="" loading="lazy"><span class="ambient-tile-label">@demosthenes2010 · 99 агентов</span></div>
      <div class="ambient-tile"><img src="/images/blog/fable51/skrinshot-iz-posta-claudiudp.jpg" alt="" loading="lazy"><span class="ambient-tile-label">@ClaudiuDP · 10 субагентов</span></div>
      <div class="ambient-tile"><img src="/images/blog/fable51/skrinshot-iz-posta-lakr233.jpg" alt="" loading="lazy"><span class="ambient-tile-label">@Lakr233 · Отладка iGhostVT</span></div>
      <div class="ambient-tile"><img src="/images/blog/fable51/skrinshot-iz-posta-dotey.jpg" alt="" loading="lazy"><span class="ambient-tile-label">@dotey · 1M контекст</span></div>
      <div class="ambient-tile"><img src="/images/blog/fable51/skrinshot-iz-posta-kenn.jpg" alt="" loading="lazy"><span class="ambient-tile-label">@kenn · Кэш 80x дешевле</span></div>
    </div>
  </div>

  <!-- Frosted Glass Veil to maintain pure paper editorial readability -->
  <div class="quiet-wall-veil" aria-hidden="true"></div>

  <!-- Foreground Content: Honest Video Analysis -->
  <div class="quiet-wall-foreground">
    <div class="page" style="padding-bottom:0">
      <p class="kicker">Боевые тесты сообщества</p>
      <h2>Боевые видео: расход лимитов и сложные задачи</h2>
      <p class="intro">Два самых показательных видео первых суток: как Fable 5.1 израсходовала $218 за три запроса и честный баттл против GPT-5.6 Sol в Blender 3D на плане реальной квартиры.</p>
    </div>

    <div class="honest-video-grid">
      
      <!-- Video 1: Riley Brown -->
      <article class="honest-video-card">
        <div class="hvc-header">
          <span class="hvc-badge danger">$218 за 3 промпта</span>
          <h3 class="hvc-title">Расход API: тестирование длинного контекста</h3>
          <div class="hvc-author">
            <a href="https://x.com/rileybrown/status/2095005898095653302" target="_blank" rel="noopener">@rileybrown</a> · 1 сентября 2026
          </div>
        </div>
        <div class="hvc-player-wrap">
          <video width="900" height="582" controls preload="metadata" poster="/images/blog/fable51/rileybrown-218-poster.jpg" src="https://pub-e4f33e98bfb544e39053056c8bb8940a.r2.dev/fable51/rileybrown-218.mp4"></video>
        </div>
        <div class="hvc-body">
          <p>Три промпта на Fable 5.1 обошлись в $218. Модель поднимает глубокие автономные цепочки рассуждений и сжигает квоты с рекордной скоростью.</p>
          <div class="hvc-stats-grid">
            <div class="hvc-stat-box"><span class="hvc-stat-val">$218</span><span class="hvc-stat-lbl">Расход API</span></div>
            <div class="hvc-stat-box"><span class="hvc-stat-val">3</span><span class="hvc-stat-lbl">Промпта</span></div>
            <div class="hvc-stat-box"><span class="hvc-stat-val">High</span><span class="hvc-stat-lbl">Усилие</span></div>
            <div class="hvc-stat-box"><span class="hvc-stat-val">$72.66</span><span class="hvc-stat-lbl">За 1 запрос</span></div>
          </div>
          <div class="hvc-callout">
            <strong>Факт расхода:</strong> сессия израсходовала 70% пятичасового лимита тарифа Max 20x всего за 15 минут автоматических проверок.
          </div>
        </div>
      </article>

      <!-- Video 2: Blender Shootout -->
      <article class="honest-video-card">
        <div class="hvc-header">
          <span class="hvc-badge battle">Fable 5.1 против GPT-5.6 Sol</span>
          <h3 class="hvc-title">3D в Blender: сборка сцены по плану квартиры</h3>
          <div class="hvc-author">
            <a href="https://x.com/ctgptlb/status/2094925117344428232" target="_blank" rel="noopener">@ctgptlb</a> · 1 сентября 2026
          </div>
        </div>
        <div class="hvc-player-wrap">
          <video width="900" height="506" controls preload="metadata" poster="/images/blog/fable51/ctgptlb-blender-poster.jpg" src="https://pub-e4f33e98bfb544e39053056c8bb8940a.r2.dev/fable51/ctgptlb-blender.mp4"></video>
        </div>
        <div class="hvc-body">
          <p>Одна задача обеим моделям: по 2D-плану квартиры собрать 3D-сцену в Blender, отрендерить ракурсы и сделать прогулочное видео. Sol справилась за 30 минут, Fable 5.1 — за 111 минут.</p>
          <div class="hvc-stats-grid">
            <div class="hvc-stat-box"><span class="hvc-stat-val">111 мин</span><span class="hvc-stat-lbl">Fable 5.1</span></div>
            <div class="hvc-stat-box"><span class="hvc-stat-val">30 мин</span><span class="hvc-stat-lbl">GPT-5.6 Sol</span></div>
            <div class="hvc-stat-box"><span class="hvc-stat-val">14 vs 6</span><span class="hvc-stat-lbl">3D кадров</span></div>
            <div class="hvc-stat-box"><span class="hvc-stat-val">44 vs 36 с</span><span class="hvc-stat-lbl">Видеооблёт</span></div>
          </div>
          <div class="hvc-callout">
            <strong>Итог сравнения:</strong> Fable 5.1 работала в 3.7 раза дольше, но сгенерировала полные текстурированные материалы и интерьерные ракурсы с естественным светом.
          </div>
        </div>
      </article>

    </div>

    <!-- Wall Interactive Pause/Play Toggle -->
    <div class="quiet-wall-control-bar">
      <span>Фон: 16 проектов и тестов сообщества из X</span>
      <button type="button" class="quiet-wall-toggle" id="wallToggleBtn" aria-label="Приостановить движение фона">⏸ Пауза фона</button>
    </div>
  </div>
</section>
"""

# 9. Custom CSS for Variant 3
custom_css = """
<style>
/* ==========================================================================
   Article Variant Switcher Bar
   ========================================================================== */
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
  border-radius: 4px;
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
  color: var(--bar-text);
  background: var(--bar);
  border-color: var(--bar);
  font-weight: 700;
}
.avs-hint {
  font-size: 11.5px;
  color: var(--muted);
}
@media (max-width: 768px) {
  .avs-hint { display: none; }
}

/* ==========================================================================
   VARIANT 3: Фокусная инфографика (Pure Visual Progression)
   ========================================================================== */
.pvp-hero-container {
  max-width: min(1200px, calc(100vw - 40px));
  margin: 24px auto 48px;
  padding: 0 16px;
}
@media (max-width: 640px) {
  .pvp-hero-container {
    padding: 0 4px;
    margin: 16px auto 36px;
  }
}

.pvp-intro-block {
  margin-bottom: 24px;
  padding-bottom: 20px;
  border-bottom: 1px solid var(--hairline);
}
.pvp-intro-kicker {
  font: 400 11.5px/1.4 'PT Mono', monospace;
  letter-spacing: .08em;
  text-transform: uppercase;
  color: var(--muted);
  display: block;
  margin-bottom: 8px;
}
.pvp-intro-title {
  font-size: 1.4em;
  font-weight: 400;
  line-height: 1.3;
  color: var(--ink);
  margin: 0 0 10px;
}
.pvp-intro-text {
  font-size: 1em;
  line-height: 1.55;
  color: var(--muted);
  max-width: 860px;
  margin: 0;
}

/* Compute Progression Summary Strip */
.pvp-summary-strip {
  background: var(--card);
  border: 1px solid var(--hairline);
  border-radius: 6px;
  padding: 16px 20px;
  margin-bottom: 24px;
}
.pvp-summary-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
}
@media (max-width: 860px) {
  .pvp-summary-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
@media (max-width: 480px) {
  .pvp-summary-grid {
    grid-template-columns: 1fr;
  }
}
.pvp-summary-item {
  display: flex;
  flex-direction: column;
  gap: 3px;
  background: var(--paper);
  border: 1px solid var(--hairline);
  border-radius: 4px;
  padding: 10px 12px;
}
.psi-label {
  font: 400 10.5px/1.2 'PT Mono', monospace;
  color: var(--muted);
  text-transform: uppercase;
  letter-spacing: .06em;
}
.psi-val {
  font: 700 13.5px/1.3 'PT Mono', monospace;
  color: var(--ink);
}
.psi-sub {
  font: 400 11.5px/1.3 'PT Serif', Georgia, serif;
  color: var(--muted);
}

/* Visual timeline bar showing the 15x jump */
.pvp-scale-bar {
  margin-top: 14px;
  padding-top: 12px;
  border-top: 1px dashed var(--hairline);
}
.pvp-scale-labels {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font: 400 11px/1.3 'PT Mono', monospace;
  color: var(--muted);
  margin-bottom: 6px;
}
.pvp-scale-track {
  height: 6px;
  background: var(--hairline);
  border-radius: 3px;
  overflow: hidden;
  display: flex;
  gap: 2px;
}
.pvp-scale-seg {
  height: 100%;
}
.pvp-scale-seg.fast-range {
  background: var(--muted);
  width: 9.3%;
}
.pvp-scale-seg.jump-range {
  background: var(--ink);
  width: 90.7%;
}

/* 5 Pelicans Cards Grid */
.pvp-cards-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 14px;
}
@media (max-width: 1060px) {
  .pvp-cards-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}
@media (max-width: 640px) {
  .pvp-cards-grid {
    grid-template-columns: 1fr;
  }
}

.pvp-card {
  background: var(--card);
  border: 1px solid var(--hairline);
  border-radius: 6px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  transition: transform .18s ease, border-color .18s ease, box-shadow .18s ease;
}
.pvp-card:hover {
  transform: translateY(-3px);
  border-color: var(--ink);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
}
.pvp-card.is-jump {
  border-color: var(--hairline);
}
.pvp-card.is-peak {
  border-color: var(--ink);
}

.pvp-card-head {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 6px;
  padding: 10px 12px;
  background: var(--paper);
  border-bottom: 1px solid var(--hairline);
}
.pvp-card-top-row {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  width: 100%;
}
.pvp-card-title-group {
  display: flex;
  align-items: baseline;
  gap: 6px;
}
.pvp-card-num {
  font: 700 11px/1 'PT Mono', monospace;
  color: var(--muted);
}
.pvp-card-level {
  font: 700 13.5px/1 'PT Mono', monospace;
  margin: 0;
  color: var(--ink);
}
.pvp-card-micro-stat {
  font: 400 10.5px/1 'PT Mono', monospace;
  color: var(--muted);
  white-space: nowrap;
}
.pvp-card-micro-stat.highlight {
  font-weight: 700;
  color: var(--ink);
}
.pvp-card-micro-stat.peak-text {
  font-weight: 700;
  color: var(--ink);
}

.pvp-tag {
  font: 400 10px/1.3 'PT Mono', monospace;
  padding: 2px 6px;
  border-radius: 3px;
  border: 1px solid var(--hairline);
  display: inline-block;
  line-height: 1.35;
}
.pvp-tag.quiet {
  background: var(--card);
  color: var(--muted);
}
.pvp-tag.standard {
  background: var(--card);
  color: var(--ink);
}
.pvp-tag.jump {
  background: var(--card);
  color: var(--ink);
  font-weight: 700;
  border-color: var(--ink);
}
.pvp-tag.peak {
  background: var(--bar);
  color: var(--bar-text);
  font-weight: 700;
  border-color: var(--bar);
}

.pvp-card-media {
  position: relative;
  background: #000;
  line-height: 0;
}
.pvp-card-media img {
  width: 100%;
  height: auto;
  display: block;
}
.pvp-media-meta {
  position: absolute;
  bottom: 8px;
  right: 8px;
  background: rgba(0, 0, 0, 0.82);
  color: #fff;
  font: 700 11px/1.3 'PT Mono', monospace;
  padding: 2px 7px;
  border-radius: 3px;
  border: 1px solid rgba(255, 255, 255, 0.2);
}
.pvp-media-meta.peak-meta {
  background: var(--ink);
  color: var(--paper);
}

.pvp-card-body {
  padding: 12px 14px 14px;
  display: flex;
  flex-direction: column;
  flex: 1;
}
.pvp-stats-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 4px;
  margin-bottom: 8px;
  font: 400 10.5px/1.2 'PT Mono', monospace;
  text-align: center;
}
.pvp-stat {
  background: var(--paper);
  border: 1px solid var(--hairline);
  border-radius: 3px;
  padding: 4px 2px;
  display: flex;
  flex-direction: column;
  gap: 1px;
}
.pvp-stat-val {
  font-weight: 700;
  color: var(--ink);
}
.pvp-stat-lbl {
  font-size: 9.5px;
  color: var(--muted);
}
.pvp-meter {
  height: 3px;
  background: var(--hairline);
  border-radius: 2px;
  margin-bottom: 10px;
  overflow: hidden;
}
.pvp-meter-fill {
  height: 100%;
  background: var(--muted);
}
.pvp-meter-fill.is-jump-fill {
  background: var(--ink);
}
.pvp-meter-fill.is-peak-fill {
  background: var(--ink);
}
.pvp-card-text {
  font-size: 13px;
  line-height: 1.45;
  color: var(--muted);
  margin: 0;
  flex: 1;
}

/* ==========================================================================
   Quiet Video Wall Section (#video-zhir)
   ========================================================================== */
.quiet-video-wall-section {
  position: relative;
  overflow: hidden;
  padding: 72px 0 54px;
  margin: 48px 0;
  border-radius: 8px;
  border: 1px solid var(--hairline);
  background: var(--card);
  scroll-margin-top: 80px;
}

/* Ambient Wall Track */
.ambient-video-track-wrap {
  position: absolute;
  inset: 0;
  pointer-events: none;
  opacity: 0.55;
  filter: contrast(1.02) brightness(0.94);
  display: flex;
  flex-direction: column;
  gap: 14px;
  justify-content: center;
  z-index: 1;
  overflow: hidden;
}
.ambient-marquee-row {
  display: flex;
  gap: 14px;
  width: max-content;
  will-change: transform;
}
.ambient-marquee-row.row-left {
  animation: ambientScrollLeft 52s linear infinite;
}
.ambient-marquee-row.row-right {
  animation: ambientScrollRight 58s linear infinite;
}
.ambient-marquee-row.is-paused {
  animation-play-state: paused !important;
}
@keyframes ambientScrollLeft {
  0% { transform: translateX(0); }
  100% { transform: translateX(-50%); }
}
@keyframes ambientScrollRight {
  0% { transform: translateX(-50%); }
  100% { transform: translateX(0); }
}

.ambient-tile {
  width: 240px;
  height: 138px;
  border-radius: 6px;
  overflow: hidden;
  position: relative;
  border: 1px solid var(--hairline);
  flex-shrink: 0;
  background: #000;
}
.ambient-tile img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.ambient-tile-label {
  position: absolute;
  bottom: 6px;
  left: 6px;
  font: 400 10px/1.2 'PT Mono', monospace;
  background: rgba(0, 0, 0, 0.78);
  color: #fff;
  padding: 2px 6px;
  border-radius: 3px;
  white-space: nowrap;
}

/* Frosted veil to ensure text contrast */
.quiet-wall-veil {
  position: absolute;
  inset: 0;
  z-index: 2;
  pointer-events: none;
  backdrop-filter: blur(5px);
  -webkit-backdrop-filter: blur(5px);
  background: linear-gradient(180deg, rgba(255, 254, 249, 0.72) 0%, rgba(255, 254, 249, 0.84) 100%);
}
:root[data-theme="dark"] .quiet-wall-veil {
  background: linear-gradient(180deg, rgba(20, 20, 20, 0.72) 0%, rgba(20, 20, 20, 0.84) 100%);
}

/* Foreground Container */
.quiet-wall-foreground {
  position: relative;
  z-index: 3;
  max-width: 1140px;
  margin: 0 auto;
  padding: 0 22px;
}
@media (max-width: 640px) {
  .quiet-wall-foreground {
    padding: 0 14px;
  }
}

.honest-video-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
  margin-top: 24px;
}
@media (max-width: 860px) {
  .honest-video-grid {
    grid-template-columns: 1fr;
  }
}

.honest-video-card {
  background: var(--paper);
  border: 1px solid var(--hairline);
  border-radius: 8px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  box-shadow: 0 14px 36px rgba(0, 0, 0, 0.10);
  transition: transform .18s ease, border-color .18s ease, box-shadow .18s ease;
}
:root[data-theme="dark"] .honest-video-card {
  box-shadow: 0 16px 40px rgba(0, 0, 0, 0.35);
}
.honest-video-card:hover {
  transform: translateY(-2px);
  border-color: var(--ink);
  box-shadow: 0 18px 44px rgba(0, 0, 0, 0.16);
}
.hvc-header {
  padding: 16px 18px 12px;
  border-bottom: 1px solid var(--hairline);
  background: var(--card);
}
.hvc-badge {
  display: inline-block;
  font: 700 11px/1.3 'PT Mono', monospace;
  text-transform: uppercase;
  letter-spacing: .06em;
  padding: 3px 8px;
  border-radius: 4px;
  margin-bottom: 8px;
}
.hvc-badge.danger {
  background: #ebcece;
  color: #7a1d1d;
}
:root[data-theme="dark"] .hvc-badge.danger {
  background: #441c1c;
  color: #fca5a5;
}
.hvc-badge.battle {
  background: #ced6bf;
  color: #2b4515;
}
:root[data-theme="dark"] .hvc-badge.battle {
  background: #253820;
  color: #bef264;
}

.hvc-title {
  font-size: 1.18em;
  font-weight: 700;
  margin: 0 0 4px;
  color: var(--ink);
}
.hvc-author {
  font: 400 12px 'PT Mono', monospace;
  color: var(--muted);
}
.hvc-author a {
  color: var(--ink);
  text-decoration: underline;
  text-underline-offset: 3px;
}

.hvc-player-wrap {
  background: #000;
  line-height: 0;
  position: relative;
}
.hvc-player-wrap video {
  width: 100%;
  height: auto;
  display: block;
  max-height: 380px;
  object-fit: contain;
}

.hvc-body {
  padding: 16px 18px 18px;
  display: flex;
  flex-direction: column;
  flex: 1;
}
.hvc-body p {
  margin: 0 0 14px;
  font-size: .95em;
  line-height: 1.52;
  color: var(--ink);
}
.hvc-stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 6px;
  margin-bottom: 14px;
  font: 400 11px/1.3 'PT Mono', monospace;
}
@media (max-width: 520px) {
  .hvc-stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
.hvc-stat-box {
  background: var(--card);
  border: 1px solid var(--hairline);
  padding: 6px 8px;
  border-radius: 4px;
}
.hvc-stat-val {
  font-weight: 700;
  font-size: 12.5px;
  color: var(--ink);
  display: block;
  margin-bottom: 2px;
}
.hvc-stat-lbl {
  font-size: 10px;
  color: var(--muted);
  display: block;
}
.hvc-callout {
  padding: 10px 12px;
  border-radius: 4px;
  font-size: 12px;
  line-height: 1.45;
  margin-top: auto;
  border: 1px solid var(--hairline);
  background: var(--card);
  color: var(--ink);
}

.quiet-wall-control-bar {
  margin-top: 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 8px 14px;
  background: var(--paper);
  border: 1px solid var(--hairline);
  border-radius: 6px;
  font-family: 'PT Mono', monospace;
  font-size: 11.5px;
  color: var(--muted);
  flex-wrap: wrap;
}
.quiet-wall-toggle {
  background: var(--card);
  border: 1px solid var(--hairline);
  border-radius: 4px;
  padding: 4px 10px;
  color: var(--ink);
  font: 400 11px 'PT Mono', monospace;
  cursor: pointer;
  transition: all .15s ease;
}
.quiet-wall-toggle:hover {
  background: var(--ink);
  color: var(--paper);
  border-color: var(--ink);
}
</style>
"""

# 10. Client-side scripts
custom_scripts = """
<!-- Bento Filter Without Search Script -->
<script>
(function(){
  const pills = document.querySelectorAll('.bento-pill');
  const sections = document.querySelectorAll('.bento-category-section');
  if (!pills.length || !sections.length) return;

  pills.forEach(pill => {
    pill.addEventListener('click', () => {
      const filter = pill.getAttribute('data-filter');
      pills.forEach(p => {
        const isActive = (p === pill);
        p.classList.toggle('active', isActive);
        p.setAttribute('aria-selected', isActive ? 'true' : 'false');
      });

      sections.forEach(sec => {
        const cat = sec.getAttribute('data-category');
        if (filter === 'all' || filter === cat) {
          sec.style.display = '';
        } else {
          sec.style.display = 'none';
        }
      });
    });
  });
})();
</script>

<!-- Quiet Video Wall Toggle Script -->
<script>
(function(){
  const btn = document.getElementById('wallToggleBtn');
  const rowLeft = document.getElementById('ambientRowLeft');
  const rowRight = document.getElementById('ambientRowRight');
  if (!btn || !rowLeft || !rowRight) return;

  let isPaused = false;
  btn.addEventListener('click', () => {
    isPaused = !isPaused;
    rowLeft.classList.toggle('is-paused', isPaused);
    rowRight.classList.toggle('is-paused', isPaused);
    btn.textContent = isPaused ? '▶ Движение фона' : '⏸ Пауза фона';
  });
})();
</script>

<!-- Copy Prompt Buttons Script -->
<script>
document.querySelectorAll('.copy-btn').forEach(b => {
  b.addEventListener('click', async () => {
    const code = b.closest('.prompt').querySelector('code').innerText;
    try {
      await navigator.clipboard.writeText(code);
      b.textContent = 'Скопировано';
      setTimeout(() => b.textContent = 'Скопировать', 1500);
    } catch(e) {
      b.textContent = 'Не вышло';
    }
  });
});
</script>
"""

# 11. TOC HTML
toc_html = """
<nav class="toc" aria-label="Содержание"><ul><li><a href="#model">Claude Fable 5.1</a></li><li><a href="#reliz">Что вышло</a></li><li><a href="#usilie">Бенчмарки по уровням усилия</a></li><li><a href="#nauka">Три научных результата</a></li><li><a href="#bentoApp">Кейсы партнёров по областям (22 кейса)</a></li><li><a href="#syscard">Системная карта: риски, взломы и лимиты</a></li><li><a href="#prompting">Как промптить Fable 5.1</a></li><li><a href="#otzyvy">Пеликаны Simon Willison</a></li><li><a href="#video-zhir">Боевые видео: расход лимитов и сложные задачи</a></li><li><a href="#otzyvy-x">Первые отзывы в X</a></li><li><a href="#istochniki">Первоисточник</a></li></ul></nav>
"""

# 12. Top Bar & Frontmatter
hugo_frontmatter = """---
title: "Обзор Claude Fable 5.1 [Вариант 3: Фокусная инфографика]"
slug: "claude-fable-5-1-v3"
sitemap_exclude: true
robots: "noindex, nofollow"
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
---
"""

top_bar = """
<button class="theme-btn" id="themeBtn" aria-label="Переключить тему">☾</button>

<nav class="article-variant-switcher" aria-label="Сравнение вариантов статьи">
  <div class="avs-group">
    <span class="avs-label">Вариант:</span>
    <a href="/blog/claude-fable-5-1-v1/" class="avs-link">1. Bento Grid (Каталог)</a>
    <a href="/blog/claude-fable-5-1-v2/" class="avs-link">2. Master-Detail (Досье)</a>
    <a href="/blog/claude-fable-5-1-v3/" class="avs-link is-active" aria-current="page">3. Фокусная инфографика</a>
    <a href="/blog/claude-fable-5-1/" class="avs-link" style="opacity:0.65">Было (7 слайдеров)</a>
  </div>
  <span class="avs-hint">Вариант 3: Чистая визуальная прогрессия пеликанов + Видео сообщества</span>
</nav>

<div class="page"><header class="masthead">
<p class="kicker">Fable 5.1 · Релиз 1 сентября 2026</p>
<h1>Разбираю Claude Fable 5.1: бенчмарки, отзывы, системная карта и промптинг</h1>
<p class="lede">Пересказ анонса Anthropic и 22 отзыва партнёров, разложенные по типу использования модели.</p>
<p class="meta">Источники: страница релиза и системная карта Anthropic, пост Simon Willison, 33 поста в X, экран usage founder · снято <time datetime="2026-09-02">2 сентября 2026</time> · независимой проверки нет</p>
</header>
</div>
"""

hugo_body = (
    top_bar + "\n" +
    hero_progression_html + "\n" +
    '<div class="page">\n' +
    toc_html + "\n" +
    model_to_nauka + "\n" +
    bento_html + "\n" +
    syscard_to_prompting + "\n" +
    otzyvy_html + "\n" +
    video_wall_html + "\n" +
    otzyvy_x_to_istochniki + "\n" +
    custom_scripts + "\n" +
    custom_css + "\n" +
    liquid_dock_html_and_js
)

# Write to content/blog/claude-fable-5-1-v3.html
with open('content/blog/claude-fable-5-1-v3.html', 'w', encoding='utf-8') as f:
    f.write(hugo_frontmatter + "\n" + hugo_body)
print("Successfully generated content/blog/claude-fable-5-1-v3.html")

# Standalone static HTML file for static/design-review/variant-3.html
static_html = f"""<!DOCTYPE html>
<html lang="ru" data-theme="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Обзор Claude Fable 5.1 [Вариант 3: Фокусная инфографика] | sereja.tech</title>
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
with open('static/design-review/variant-3.html', 'w', encoding='utf-8') as f:
    f.write(static_html)
print("Successfully generated static/design-review/variant-3.html")
