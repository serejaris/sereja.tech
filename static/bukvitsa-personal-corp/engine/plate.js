/* Сборка таблицы: буквы раскладываются по листу, в штрихи кладутся ячейки
   со сценами, вокруг каждой буквы рисуется орнамент. */
(function () {
  var PC = (window.PC = window.PC || {});
  var NS = 'http://www.w3.org/2000/svg';
  var G = function () { return PC.glyphs; };
  var GAP = 10;

  function el(tag, attrs, parent) {
    var e = document.createElementNS(NS, tag);
    if (attrs) for (var k in attrs) e.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(e);
    return e;
  }
  function f(n) { return Math.round(n * 10) / 10; }
  function pathD(pts, closed) {
    return 'M' + pts.map(function (p) { return f(p[0]) + ' ' + f(p[1]); }).join('L') + (closed ? 'Z' : '');
  }

  /* раскладка букв: row — в строку, grid — по две в ряд, col — столбиком */
  function arrange(boxes, name) {
    var pos = [], W = 0, H = 0, i;
    if (name === 'row') {
      var x = 0; H = Math.max.apply(null, boxes.map(function (b) { return b.h; }));
      boxes.forEach(function (b, k) { pos.push({ x: x, y: (H - b.h) / 2 }); x += b.w + GAP; });
      W = x - GAP;
    } else if (name === 'col') {
      W = Math.max.apply(null, boxes.map(function (b) { return b.w; }));
      var y = 0;
      boxes.forEach(function (b) { pos.push({ x: (W - b.w) / 2, y: y }); y += b.h + GAP; });
      H = y - GAP;
    } else { // grid: 2 колонки
      var rows = [];
      for (i = 0; i < boxes.length; i += 2) rows.push(boxes.slice(i, i + 2));
      var cw = [0, 0];
      rows.forEach(function (r) { r.forEach(function (b, k) { cw[k] = Math.max(cw[k], b.w); }); });
      var yy = 0;
      rows.forEach(function (r, ri) {
        var rh = Math.max.apply(null, r.map(function (b) { return b.h; }));
        r.forEach(function (b, k) {
          var xx = k === 0 ? 0 : cw[0] + GAP;
          if (r.length === 1) xx = (cw[0] + GAP + cw[1] - b.w) / 2;
          else xx += (cw[k] - b.w) / 2;
          pos.push({ x: xx, y: yy + (rh - b.h) / 2 });
        });
        yy += rh + GAP;
      });
      W = cw[0] + GAP + cw[1]; H = yy - GAP;
      if (boxes.length === 1) { W = boxes[0].w; }
    }
    return { pos: pos, W: W, H: H };
  }

  /* выбор раскладки по ширине контейнера и высоте окна: берём ту, что
     окажется крупнее всего, когда вся таблица влезает и в ширину, и в высоту */
  function chooseLayout(boxes, widthPx, maxHeightPx) {
    if (boxes.length === 1) return 'single';
    var best = null;
    // при почти равном масштабе берём сетку: слово читается целиком и не уходит лентой вниз
    ['grid', 'row', 'col'].forEach(function (name) {
      var a = arrange(boxes, name), sc = Math.min(widthPx / a.W, maxHeightPx / a.H);
      if (!best || sc > best.sc * 1.12) best = { name: name, sc: sc };
    });
    return best.name;
  }

  function makeDefs(svg) {
    var defs = el('defs', null, svg);
    var c1 = el('clipPath', { id: 'cp-rect' }, defs);
    el('rect', { x: -71, y: -46, width: 142, height: 92, rx: 2 }, c1);
    var c2 = el('clipPath', { id: 'cp-med' }, defs);
    el('circle', { r: 56 }, c2);
    return defs;
  }

  /* Подписи лент по настоящей ширине текста (нужен документ и шрифт).
     Медальон: шрифт подгоняется под хорду круга на высоте нижнего края строки;
     если меньше MIN1 — две строки на ленте пошире, номер опускается ниже. */
  var MED_R = 56, MED_RIB1 = 'M-60 19Q0 16 60 19L60 31Q0 28 -60 31Z', MED_RIB2 = 'M-60 19Q0 16 60 19L60 39Q0 36 -60 39Z';
  function chord(y) { return 2 * Math.sqrt(Math.max(0, MED_R * MED_R - y * y)) - 7; }
  function measure(t, text, size) {
    t.textContent = text; t.removeAttribute('textLength'); t.removeAttribute('lengthAdjust');
    t.setAttribute('font-size', f(size));
    var w = 0;
    try { w = t.getComputedTextLength(); } catch (e) { w = 0; }
    return w || text.length * size * 0.62;
  }
  function squeeze(t, w, avail) {   // крайний случай: шрифт уже на минимуме
    if (w > avail) { t.setAttribute('textLength', f(avail)); t.setAttribute('lengthAdjust', 'spacingAndGlyphs'); }
  }
  function fitCaptions(svg) {
    Array.prototype.forEach.call(svg.querySelectorAll('.cell'), function (cell) {
      var t = cell.querySelector('text.cap'), text = t && t.getAttribute('data-text');
      if (!text) return;
      var med = cell.classList.contains('cell-med'), w, size;
      if (!med) {                          // планка: прямая лента шириной 114
        w = measure(t, text, 7.4);
        size = Math.max(6, Math.floor(Math.min(7.4, 7.4 * 112 / w) * 10) / 10);
        squeeze(t, measure(t, text, size), 112);
        return;
      }
      var rib = cell.querySelector('.ribbon path'), badge = cell.querySelector('.badge');
      t.setAttribute('y', 26.3);
      w = measure(t, text, 6.6);
      size = Math.min(6.6, 6.6 * chord(26.3 + 1.4) / w);
      var words = text.split(' ');
      if (size >= 5.4 || words.length < 2) {
        rib.setAttribute('d', MED_RIB1);
        badge.setAttribute('transform', 'translate(0 42)');
        size = Math.max(5, Math.floor(size * 10) / 10);
        squeeze(t, measure(t, text, size), chord(26.3 + 1.4));
        return;
      }
      // две строки: разрез, при котором длинная строка короче всего
      var best = null;
      for (var k = 1; k < words.length; k++) {
        var a = words.slice(0, k).join(' '), b = words.slice(k).join(' ');
        var wa = measure(t, a, 6.6), wb = measure(t, b, 6.6);
        var sz = Math.min(6.2, 6.6 * chord(24.6 + 1.3) / wa, 6.6 * chord(32.2 + 1.3) / wb);
        if (!best || sz > best.sz) best = { a: a, b: b, sz: sz };
      }
      size = Math.max(4.6, Math.floor(best.sz * 10) / 10);
      rib.setAttribute('d', MED_RIB2);
      badge.setAttribute('transform', 'translate(0 46)');
      t.textContent = ''; t.removeAttribute('textLength'); t.removeAttribute('lengthAdjust');
      t.setAttribute('font-size', f(size));
      [[best.a, 24.6], [best.b, 32.2]].forEach(function (ln) {
        var sp = document.createElementNS(NS, 'tspan');
        sp.setAttribute('x', 0); sp.setAttribute('y', ln[1]); sp.textContent = ln[0];
        t.appendChild(sp);
        var lw = sp.getComputedTextLength ? sp.getComputedTextLength() : 0, av = chord(ln[1] + 0.25 * size);
        if (lw > av) { sp.setAttribute('textLength', f(av)); sp.setAttribute('lengthAdjust', 'spacingAndGlyphs'); }
      });
    });
  }

  function fitText(t, text, avail, size) {
    t.textContent = text;
    var est = text.length * size * 0.58;
    if (est > avail) { t.setAttribute('textLength', f(avail)); t.setAttribute('lengthAdjust', 'spacingAndGlyphs'); }
  }

  function buildCell(c, scene, art) {
    var isRect = c.kind === 'rect';
    var g = el('g', {
      class: 'cell ' + (isRect ? 'cell-rect' : 'cell-med'),
      'data-id': scene.id, tabindex: 0, role: 'button',
      transform: 'translate(' + f(c.x) + ' ' + f(c.y) + ')',
      'aria-label': scene.numeral + '. ' + scene.caption
    });
    var bg, ring, clip = el('g', { 'clip-path': isRect ? 'url(#cp-rect)' : 'url(#cp-med)' }, g);
    if (isRect) {
      bg = el('rect', { class: 'cell-bg', x: -75, y: -50, width: 150, height: 100, rx: 3 }, g);
      g.insertBefore(bg, clip);
    } else {
      bg = el('circle', { class: 'cell-bg', r: 60 }, g);
      g.insertBefore(bg, clip);
    }
    el(isRect ? 'rect' : 'circle', isRect ? { class: 'cell-paper', x: -71, y: -46, width: 142, height: 92 } : { class: 'cell-paper', r: 56 }, clip);
    var sc = el('g', { class: 'sc', transform: isRect ? 'translate(-69 -46) scale(0.575)' : 'translate(-91 -60.5) scale(0.7576)' }, clip);
    art(sc, scene.id);
    // золотая рамка освещения
    el(isRect ? 'rect' : 'circle', isRect ? { class: 'cell-gold', x: -71, y: -46, width: 142, height: 92, rx: 2 } : { class: 'cell-gold', r: 56 }, g);

    // подпись-лента
    var rib = el('g', { class: 'ribbon' }, clip), t;
    if (isRect) {
      el('rect', { x: -52, y: -46, width: 122, height: 13.5 }, rib);
      t = el('text', { class: 'cap', x: 9, y: -36.2, 'text-anchor': 'middle', 'font-size': 7.4 }, rib);
      fitText(t, scene.caption, 114, 7.4);
      t.setAttribute('data-text', scene.caption);
    } else {
      // лента ниже окна смысла: верхний край не выше y=17.5 ячейки, это y≈103 холста 240×160
      el('path', { d: MED_RIB1 }, rib);
      t = el('text', { class: 'cap', x: 0, y: 26.3, 'text-anchor': 'middle', 'font-size': 6.6 }, rib);
      fitText(t, scene.caption, 90, 6.6);
      t.setAttribute('data-text', scene.caption);
    }
    // номер сцены: у планки — в левом верхнем углу, у медальона — плашкой под лентой,
    // целиком внутри круга и ниже окна смысла (y≈125–145 холста), не на рисунке
    var badge, nt;
    if (isRect) {
      badge = el('g', { class: 'badge', transform: 'translate(-62 -39.5)' }, g);
      el('circle', { r: 11.5 }, badge);
      nt = el('text', { class: 'num', y: 3.7, 'text-anchor': 'middle', 'font-size': 10.5 }, badge);
      nt.textContent = scene.numeral;
      if (scene.numeral.length > 3) { nt.setAttribute('textLength', 18); nt.setAttribute('lengthAdjust', 'spacingAndGlyphs'); }
    } else {
      var bw = Math.max(16, 5 + scene.numeral.length * 5.4);
      badge = el('g', { class: 'badge', transform: 'translate(0 42)' }, g);
      el('rect', { x: f(-bw / 2), y: -7, width: f(bw), height: 14, rx: 7 }, badge);
      nt = el('text', { class: 'num', y: 3.1, 'text-anchor': 'middle', 'font-size': 9 }, badge);
      nt.textContent = scene.numeral;
      if (scene.numeral.length > 4) { nt.setAttribute('textLength', f(bw - 7)); nt.setAttribute('lengthAdjust', 'spacingAndGlyphs'); }
    }
    return g;
  }

  /* spec: { letters:[{letter, scenes:[...]}], widthPx, maxHeightPx, art(g,id) } */
  function render(spec) {
    var svg = el('svg', { class: 'plate', xmlns: NS, role: 'group', 'aria-label': 'Буквица' });
    makeDefs(svg);
    var built = spec.letters.map(function (L) {
      var gl = G().build(L.letter, L.scenes.length);
      var orn = PC.ornament.build(gl, L.letter + L.scenes.length + (L.salt || ''));
      var F = orn.frame;
      var pad = 12;
      return { L: L, g: gl, orn: orn, box: { w: F.x1 - F.x0 + 2 * pad, h: F.y1 - F.y0 + 2 * pad, ox: F.x0 - pad, oy: F.y0 - pad } };
    });
    var layout = spec.forceLayout || chooseLayout(built.map(function (b) { return b.box; }), spec.widthPx, spec.maxHeightPx);
    var arr = arrange(built.map(function (b) { return b.box; }), layout === 'single' ? 'grid' : layout);
    svg.setAttribute('viewBox', '0 0 ' + f(arr.W) + ' ' + f(arr.H));
    svg.setAttribute('data-w', arr.W); svg.setAttribute('data-h', arr.H);

    var cells = [];
    built.forEach(function (b, bi) {
      var p = arr.pos[bi];
      var lg = el('g', { class: 'letter', 'data-letter': b.L.letter, transform: 'translate(' + f(p.x - b.box.ox) + ' ' + f(p.y - b.box.oy) + ')' }, svg);
      lg.appendChild(b.orn.group);
      var band = el('g', { class: 'band' }, lg);
      [['band-edge', 5], ['band-fill', 0], ['band-tick', -20]].forEach(function (layer) {
        b.g.paths.forEach(function (pp) {
          el('path', { class: layer[0], d: pathD(pp.pts, pp.closed), 'stroke-width': pp.w + layer[1], 'stroke-linecap': pp.cap }, band);
        });
      });
      b.g.cells.forEach(function (c, ci) {
        var sc = b.L.scenes[ci];
        if (!sc) return;
        var cg = buildCell(c, sc, spec.art);
        lg.appendChild(cg);
        cells.push({ scene: sc, el: cg, kind: c.kind, letter: b.L.letter, w: c.w || c.r * 2, h: c.h || c.r * 2 });
      });
      // связь орнамента с ячейками: data-cell → номер сцены
      b.orn.group.querySelectorAll('[data-cell]').forEach(function (e) {
        var sc = b.L.scenes[+e.getAttribute('data-cell')];
        if (sc) e.setAttribute('data-scene', sc.id); else e.removeAttribute('data-cell');
      });
    });
    return { svg: svg, cells: cells, layout: layout, W: arr.W, H: arr.H };
  }

  PC.plate = { render: render, chooseLayout: chooseLayout, fitCaptions: fitCaptions };
})();
