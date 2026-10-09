/* Буквица: состояние страницы, панель чтения, заметки на полях, освещение. */
(function () {
  var PC = (window.PC = window.PC || {});
  var NS = 'http://www.w3.org/2000/svg';
  var STORE = 'bukvitsa-pc3-v1';
  var BUKVA = ['CORP', 'C', 'O', 'R', 'P'];
  var P = window.PC_PROGRAM;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  if (!P || !P.scenes || !P.scenes.length) {
    document.body.insertAdjacentHTML('afterbegin', '<p class="noscript">Не нашлось содержания буквицы (data/program.js).</p>');
    return;
  }

  var app = $('#app'), wrap = $('#plate-wrap'), panel = $('#panel'), overlay = $('#overlay'), layout = $('#layout');
  var notesL = $('#notes-l'), notesR = $('#notes-r');
  var scenes = P.scenes, byId = {}, partById = {};
  scenes.forEach(function (s, i) { byId[s.id] = s; s._i = i; });
  (P.parts || []).forEach(function (p) { partById[p.id] = p; });

  var state = { bukva: 'CORP', mode: 'read', view: 'plate', sel: scenes[0].id, tab: 'pic', lit: {} };
  var plate = null, noteEls = {}, leaderEls = {}, ringEl = null, srcCache = {}, lastW = 0, lastH = 0, activePh = 0;
  var routes = {};      // id сцены → как идёт выносная линия: сторона, рельс, высота строки в заметке
  var picked = false;   // в «Смотреть» выбор не выделяем, пока читатель сам не нажал на сцену

  /* ---------- хранилище ---------- */
  function load() {
    try {
      var raw = localStorage.getItem(STORE);
      if (raw) {
        var d = JSON.parse(raw);
        (d.lit || []).forEach(function (id) { if (byId[id]) state.lit[id] = 1; });
        if (d.mode === 'look' || d.mode === 'read') state.mode = d.mode;
        if (d.view === 'folio' || d.view === 'plate') state.view = d.view;
      }
    } catch (e) {}
  }
  function save() {
    try {
      localStorage.setItem(STORE, JSON.stringify({ lit: Object.keys(state.lit), mode: state.mode, view: state.view }));
    } catch (e) {}
  }
  function readUrl() {
    var q = new URLSearchParams(location.search);
    var b = (q.get('bukva') || '').toUpperCase();
    if (BUKVA.indexOf(b) >= 0) state.bukva = b;
    if (q.get('mode') === 'look' || q.get('mode') === 'read') state.mode = q.get('mode');
    if (q.get('view') === 'folio' || q.get('view') === 'plate') state.view = q.get('view');
    var h = location.hash.replace('#', '');
    if (byId[h]) state.sel = h;
  }
  function writeUrl() {
    try {
      var q = new URLSearchParams(location.search);
      q.set('bukva', state.bukva);
      q.set('mode', state.mode);
      q.set('view', state.view);
      history.replaceState(null, '', '?' + q.toString() + '#' + state.sel);
    } catch (e) {}
  }

  /* ---------- сцены ---------- */
  var FALLBACK = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 160"><rect class="ln" x="40" y="30" width="160" height="100" stroke-dasharray="4 4"/><text class="rub" x="120" y="84" text-anchor="middle" font-size="12">РИСУНОК В РАБОТЕ</text></svg>';
  function parseSvg(text) {
    if (!text || text.indexOf('<svg') < 0) return null;
    var doc = new DOMParser().parseFromString(text, 'image/svg+xml');
    if (doc.querySelector('parsererror')) return null;
    var root = doc.documentElement;
    $$('script,style,foreignObject,image', root).forEach(function (n) { n.parentNode.removeChild(n); });
    $$('*', root).forEach(function (n) {
      Array.prototype.slice.call(n.attributes).forEach(function (a) { if (/^on/i.test(a.name)) n.removeAttribute(a.name); });
    });
    return root;
  }
  function fetchSvg(url) {
    return fetch(url).then(function (r) { if (!r.ok) throw new Error(r.status); return r.text(); }).then(parseSvg);
  }
  function loadAll() {
    var ph = fetchSvg('scenes/_placeholder.svg').catch(function () { return null; }).then(function (r) { return r || parseSvg(FALLBACK); });
    return ph.then(function (placeholder) {
      return Promise.all(scenes.map(function (s) {
        return fetchSvg('scenes/' + s.id + '.svg').catch(function () { return null; }).then(function (root) {
          srcCache[s.id] = root ? { root: root, real: true } : { root: placeholder, real: false };
        });
      }));
    });
  }
  function cloneInto(target, id) {
    var src = (srcCache[id] || {}).root;
    if (!src) return;
    Array.prototype.forEach.call(src.childNodes, function (n) { target.appendChild(document.importNode(n, true)); });
  }
  function sceneSvg(id, cls) {
    var svg = document.createElementNS(NS, 'svg');
    svg.setAttribute('viewBox', '0 0 240 160');
    svg.setAttribute('class', 'sc' + (cls ? ' ' + cls : ''));
    svg.setAttribute('role', 'img');
    svg.setAttribute('aria-label', byId[id].caption);
    var bg = document.createElementNS(NS, 'rect');
    bg.setAttribute('class', 'sc-bg'); bg.setAttribute('width', 240); bg.setAttribute('height', 160);
    svg.appendChild(bg);
    var fr = document.createElementNS(NS, 'rect');
    fr.setAttribute('class', 'sc-frame'); fr.setAttribute('x', 4); fr.setAttribute('y', 4); fr.setAttribute('width', 232); fr.setAttribute('height', 152);
    svg.appendChild(fr);
    cloneInto(svg, id);
    return svg;
  }

  /* ---------- буквы по режиму ---------- */
  function lettersFor(b) {
    if (b === 'CORP') {
      var out = [];
      ['C', 'O', 'R', 'P'].forEach(function (L) {
        var list = scenes.filter(function (s) { return s.part === L; });
        if (list.length) out.push({ letter: L, scenes: list });
      });
      return out;
    }
    return [{ letter: b, scenes: scenes.slice() }];
  }

  /* ---------- сборка таблицы и полей ---------- */
  function narrow() { return window.innerWidth <= 860; }

  /* в «Читать» буква целиком помещается в окно рядом с текстом: и раскладка
     слова CORP, и ширина таблицы выбираются по высоте окна */
  function fitHeight() {
    var top = $('.topbar');
    return Math.max(320, window.innerHeight - (top ? top.offsetHeight : 0) - 24);
  }
  function renderPlate() {
    wrap.style.maxWidth = '';
    var wpx = wrap.clientWidth || 760;
    var fit = state.mode === 'read';
    var availH = fit ? fitHeight() : 1e6;
    plate = PC.plate.render({
      letters: lettersFor(state.bukva), widthPx: wpx,
      maxHeightPx: availH,
      art: function (g, id) { cloneInto(g, id); }
    });
    if (fit) {
      var w = Math.min(wpx, availH * plate.W / plate.H);
      if (w < wpx - 2) wrap.style.maxWidth = Math.floor(w) + 'px';
    }
    app.setAttribute('data-single', plate.layout === 'single' ? '1' : '0');
    plate.byId = {};
    plate.cells.forEach(function (c) {
      plate.byId[c.scene.id] = c;
      c.el.addEventListener('click', function () { onCell(c.scene.id); });
      c.el.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); onCell(c.scene.id); }
      });
      c.el.addEventListener('mouseenter', function () { setHover(c.scene.id, true); });
      c.el.addEventListener('mouseleave', function () { setHover(c.scene.id, false); });
    });
    ringEl = null;
    buildNotes();
    // освещение ставим до вставки в страницу: иначе при каждой перезагрузке
    // освещённые ячейки заново «разгораются» из туши за секунду
    applyLit();
    wrap.textContent = '';
    wrap.appendChild(plate.svg);
    PC.plate.fitCaptions(plate.svg);
    lastW = wrap.parentNode.clientWidth;
    lastH = window.innerHeight;
    applySel();
    layoutNotes();
    syncPanelLit();       // панель и окно сцены всегда в том же состоянии, что и ячейка
  }
  function refitCaptions() { if (plate) { PC.plate.fitCaptions(plate.svg); layoutNotes(); } }

  /* Заметка на полях: номер, заголовок, текст. Название части пишется один раз,
     над первой сценой части; дополнения «на полях» уходят в окно сцены. */
  function buildNotes() {
    notesL.textContent = ''; notesR.textContent = ''; noteEls = {};
    var seen = {};
    scenes.forEach(function (s) {
      var first = !seen[s.part];
      seen[s.part] = 1;
      if (!plate.byId[s.id]) return;
      var d = document.createElement('div');
      d.className = 'note';
      d.setAttribute('data-id', s.id);
      var part = partById[s.part];
      if (first && part) {
        var k = document.createElement('span'); k.className = 'kick';
        var kb = document.createElement('b'); kb.textContent = part.id;
        k.appendChild(kb); k.appendChild(document.createTextNode(part.title));
        d.appendChild(k);
      }
      var tx = document.createElement('div'); tx.className = 'tx';
      var nm = document.createElement('span'); nm.className = 'nm'; nm.textContent = s.numeral;
      var b = document.createElement('b'); b.textContent = (s.note && s.note.title ? s.note.title : s.caption) + '. ';
      tx.appendChild(nm); tx.appendChild(document.createTextNode(' '));
      tx.appendChild(b); tx.appendChild(document.createTextNode(s.note ? s.note.text : ''));
      d.appendChild(tx);
      d.addEventListener('click', function () { onCell(s.id); });
      d.addEventListener('mouseenter', function () { setHover(s.id, true); });
      d.addEventListener('mouseleave', function () { setHover(s.id, false); });
      noteEls[s.id] = d;
    });
  }
  function setHover(id, on) {
    if (leaderEls[id]) {
      leaderEls[id].classList.toggle('hov', on);
      if (on) leaderEls[id].parentNode.appendChild(leaderEls[id]);
    }
    if (noteEls[id]) noteEls[id].classList.toggle('hov', on);
    var c = plate && plate.byId[id];
    if (c) c.el.classList.toggle('hov', on);
  }

  function notesVisible() { return getComputedStyle(notesL).display !== 'none'; }

  function cellBox(c, ref) {
    var r = c.el.querySelector('.cell-bg').getBoundingClientRect();
    return {
      x0: r.left - ref.left, x1: r.right - ref.left, y0: r.top - ref.top, y1: r.bottom - ref.top,
      cx: (r.left + r.right) / 2 - ref.left, cy: (r.top + r.bottom) / 2 - ref.top,
      w: r.width, h: r.height, k: r.width / (c.kind === 'rect' ? 150 : 120)
    };
  }

  /* Раскладка заметок по полям.
     1. Сторона: ячейку, к которой слева мешает подойти соседка, подписываем справа,
        и наоборот. Ячейку в середине длинной планки подписываем через «рельс»:
        линия идёт над буквой (или под ней) и опускается к ячейке сверху (снизу).
     2. Высота: каждая заметка стремится встать строкой заголовка ровно напротив
        своей ячейки, чтобы выносная линия была горизонтальной; где заметки
        не помещаются, столбец раздвигается вверх и вниз поровну (изотонная регрессия). */
  function layoutNotes() {
    var vis = notesVisible();
    notesL.textContent = ''; notesR.textContent = '';
    notesL.style.height = ''; notesR.style.height = '';
    wrap.style.marginTop = '';
    routes = {};
    // «Смотреть» на узком экране: полей нет, заметки идут сеткой под буквой по порядку сцен
    if (state.mode === 'look' && window.innerWidth <= 1180) {
      scenes.forEach(function (s) { var n = noteEls[s.id]; if (n) { n.style.top = ''; notesR.appendChild(n); } });
      drawLeaders();
      return;
    }
    if (!vis) { drawLeaders(); return; }
    var pr = wrap.getBoundingClientRect(), mid = pr.width / 2, G = 8;
    var items = [];
    plate.cells.forEach(function (c) {
      var n = noteEls[c.scene.id];
      if (!n) return;
      var b = cellBox(c, pr);
      b.id = c.scene.id; b.n = n; b.ord = c.scene._i; b.kind = c.kind;
      items.push(b);
    });
    // высоты заметок и высота строки заголовка внутри заметки
    items.forEach(function (it) {
      notesL.appendChild(it.n);
      it.h = it.n.offsetHeight;
      var t = it.n.querySelector('.tx');
      it.a = (t ? t.offsetTop : 0) + 9;
    });
    notesL.textContent = '';
    // кто загораживает ячейку слева и справа по её средней линии
    items.forEach(function (it) {
      it.bl = it.br = false;
      items.forEach(function (o) {
        if (o === it || !(o.y0 < it.cy && o.y1 > it.cy)) return;
        if (o.cx < it.cx) it.bl = true; else it.br = true;
      });
    });
    function railTopOk(it) {   // над ячейкой и правее неё нет других ячеек
      return !items.some(function (o) { return o !== it && o.y1 <= it.y0 + 2 && o.x1 > it.x0; });
    }
    function railBotOk(it) {   // под ячейкой и левее неё нет других ячеек
      return !items.some(function (o) { return o !== it && o.y0 >= it.y1 - 2 && o.x0 < it.x1; });
    }
    items.forEach(function (it) {
      it.rail = ''; it.free = false;
      if (it.bl && it.br) {
        if (railTopOk(it)) { it.side = 'r'; it.rail = 't'; }
        else if (railBotOk(it)) { it.side = 'l'; it.rail = 'b'; }
        else it.side = it.cx < mid ? 'l' : 'r';
      } else if (it.bl) it.side = 'r';
      else if (it.br) it.side = 'l';
      else { it.side = it.cx < mid ? 'l' : 'r'; it.free = true; }
    });
    // выравниваем столбцы: свободные ячейки переходят на более короткую сторону
    function total(side) { return items.reduce(function (s, it) { return s + (it.side === side ? it.h + G : 0); }, 0); }
    for (var guard = 0; guard < items.length; guard++) {
      var hl = total('l'), hr = total('r'), heavy = hl > hr ? 'l' : 'r', diff = Math.abs(hl - hr);
      var cand = items.filter(function (it) { return it.free && it.side === heavy && diff > it.h + G; })
        .sort(function (a, b) { return heavy === 'l' ? b.cx - a.cx : a.cx - b.cx; })[0];
      if (!cand) break;
      cand.side = heavy === 'l' ? 'r' : 'l';
    }
    // желаемая высота строки заголовка; у рельса это граница. Верхний рельс держим
    // у самой границы (иначе он уплывает вверх и сталкивает букву вниз, за край окна),
    // нижний отпускаем: ниже уйти ему не вредно
    items.forEach(function (it) {
      var band = (it.kind === 'rect' ? 18 : 6) * it.k + 8;
      if (it.rail === 't') { it.lim = it.y0 - band; it.pref = it.lim; it.w = 3; }
      else if (it.rail === 'b') { it.lim = it.y1 + band; it.pref = it.lim; it.w = 0.05; }
      else { it.pref = it.cy; it.w = 1; }
    });
    function stack(side) {
      var col = items.filter(function (it) { return it.side === side; })
        .sort(function (a, b) { return Math.abs(a.pref - b.pref) > 2 ? a.pref - b.pref : a.ord - b.ord; });
      var i;
      // рельсы одной планки — лесенкой, чтобы линии не пересекались
      for (i = col.length - 2; i >= 0; i--) {
        if (col[i].rail === 't' && col[i + 1].rail === 't') col[i].pref = Math.min(col[i].pref, col[i + 1].pref - (col[i].h + G + col[i + 1].a - col[i].a));
      }
      for (i = 1; i < col.length; i++) {
        if (col[i].rail === 'b' && col[i - 1].rail === 'b') col[i].pref = Math.max(col[i].pref, col[i - 1].pref + (col[i - 1].h + G + col[i].a - col[i - 1].a));
      }
      var cum = 0, blocks = [];
      col.forEach(function (it) {
        it.cum = cum; cum += it.h + G;
        blocks.push({ s: (it.pref - it.a - it.cum) * it.w, w: it.w, n: 1 });
        while (blocks.length > 1) {
          var B = blocks[blocks.length - 1], A = blocks[blocks.length - 2];
          if (A.s / A.w <= B.s / B.w) break;
          A.s += B.s; A.w += B.w; A.n += B.n; blocks.pop();
        }
      });
      i = 0;
      blocks.forEach(function (B) {
        var m = B.s / B.w;
        for (var k = 0; k < B.n; k++, i++) col[i].top = m + col[i].cum;
      });
      // верхние рельсы не ниже своей границы: поднимаем их и всё, что над ними
      for (i = col.length - 1; i >= 0; i--) {
        if (col[i].rail === 't') col[i].top = Math.min(col[i].top, col[i].lim - col[i].a);
        if (i < col.length - 1) col[i].top = Math.min(col[i].top, col[i + 1].top - col[i].h - G);
      }
      // нижние рельсы не выше своей границы: опускаем их и всё, что под ними
      for (i = 0; i < col.length; i++) {
        if (col[i].rail === 'b') col[i].top = Math.max(col[i].top, col[i].lim - col[i].a);
        if (i > 0) col[i].top = Math.max(col[i].top, col[i - 1].top + col[i - 1].h + G);
      }
      return col;
    }
    var cols = { l: stack('l'), r: stack('r') };
    var minTop = 0;
    items.forEach(function (it) { minTop = Math.min(minTop, it.top); });
    var D = Math.ceil(-minTop);              // заметки выше буквы: опускаем букву
    if (D > 0) wrap.style.marginTop = D + 'px';
    ['l', 'r'].forEach(function (side) {
      var cont = side === 'l' ? notesL : notesR, bottom = 0;
      var off = cont.getBoundingClientRect().top - pr.top;
      cols[side].forEach(function (it) {
        cont.appendChild(it.n);
        it.n.style.top = Math.round(it.top + D - off) + 'px';
        bottom = Math.max(bottom, it.top + D - off + it.h);
        routes[it.id] = { side: side, rail: it.rail, a: it.a };
      });
      cont.style.height = Math.max(0, Math.round(bottom)) + 'px';
    });
    drawLeaders();
  }

  function f1(n) { return Math.round(n * 10) / 10; }

  /* Выносные линии никогда не ложатся на рисунок: маска вырезает их над каждой ячейкой,
     линия доходит до края ячейки и уходит «под» соседние, если путь через них. */
  function leaderLayer(L) {
    var defs = document.createElementNS(NS, 'defs');
    var mask = document.createElementNS(NS, 'mask');
    mask.setAttribute('id', 'leader-mask');
    mask.setAttribute('maskUnits', 'userSpaceOnUse');
    var W = Math.max(L.width, 1) + 4000, H = Math.max(L.height, 1) + 4000;
    [['x', -2000], ['y', -2000], ['width', W], ['height', H]].forEach(function (a) { mask.setAttribute(a[0], a[1]); });
    var bg = document.createElementNS(NS, 'rect');
    [['x', -2000], ['y', -2000], ['width', W], ['height', H], ['fill', '#fff']].forEach(function (a) { bg.setAttribute(a[0], a[1]); });
    mask.appendChild(bg);
    if (plate) plate.cells.forEach(function (c) {
      var b = cellBox(c, L), hole;
      if (c.kind === 'med') {
        hole = document.createElementNS(NS, 'circle');
        hole.setAttribute('cx', f1(b.cx)); hole.setAttribute('cy', f1(b.cy)); hole.setAttribute('r', f1(b.w / 2));
      } else {
        hole = document.createElementNS(NS, 'rect');
        hole.setAttribute('x', f1(b.x0)); hole.setAttribute('y', f1(b.y0));
        hole.setAttribute('width', f1(b.w)); hole.setAttribute('height', f1(b.h));
      }
      hole.setAttribute('fill', '#000');
      mask.appendChild(hole);
    });
    defs.appendChild(mask);
    overlay.appendChild(defs);
    var g = document.createElementNS(NS, 'g');
    g.setAttribute('mask', 'url(#leader-mask)');
    overlay.appendChild(g);
    return g;
  }

  function drawLeaders() {
    overlay.textContent = '';
    leaderEls = {};
    var L = layout.getBoundingClientRect();
    var showSel = picked || state.mode === 'read';
    var lines = null;
    function mk(d, ex, ey, id) {
      if (!lines) lines = leaderLayer(L);
      var on = showSel && id === state.sel;
      var path = document.createElementNS(NS, 'path');
      path.setAttribute('d', d);
      path.setAttribute('class', 'leader' + (on ? ' sel' : ''));
      lines.appendChild(path);
      var dot = document.createElementNS(NS, 'circle');
      dot.setAttribute('cx', f1(ex)); dot.setAttribute('cy', f1(ey)); dot.setAttribute('r', on ? 3.2 : 2.2);
      dot.setAttribute('class', 'leader-dot' + (on ? ' sel' : ''));
      overlay.appendChild(dot);
      leaderEls[id] = path;
    }
    if (notesVisible() && plate) {
      scenes.forEach(function (s) {
        var n = noteEls[s.id], c = plate.byId[s.id], rt = routes[s.id];
        if (!n || !c || !n.parentNode || !rt) return;
        var nr = n.getBoundingClientRect(), b = cellBox(c, L);
        var left = rt.side === 'l';
        var x1 = (left ? nr.right : nr.left) - L.left, y1 = nr.top - L.top + rt.a;
        var d, ex, ey;
        if (rt.rail) {
          // рельс: вдоль поля над (под) буквой, затем отвесно к краю ячейки
          ex = b.cx; ey = rt.rail === 't' ? b.y0 : b.y1;
          d = 'M' + f1(x1) + ' ' + f1(y1) + 'H' + f1(ex) + 'V' + f1(ey);
        } else {
          var hh = b.h / 2, hw = b.w / 2;
          var dy = Math.max(-hh * 0.55, Math.min(hh * 0.55, y1 - b.cy));
          ey = b.cy + dy;
          var dx = c.kind === 'med' ? Math.sqrt(Math.max(0, hw * hw - dy * dy)) : hw;
          ex = left ? b.cx - dx : b.cx + dx;
          if (Math.abs(ey - y1) < 0.6) d = 'M' + f1(x1) + ' ' + f1(y1) + 'H' + f1(ex);
          else d = 'M' + f1(x1) + ' ' + f1(y1) + 'H' + f1(x1 + (left ? 12 : -12)) + 'L' + f1(ex) + ' ' + f1(ey);
        }
        mk(d, ex, ey, s.id);
      });
      // выбранная — поверх остальных
      var sel = leaderEls[state.sel];
      if (sel && showSel) sel.parentNode.appendChild(sel);
    } else if (app.getAttribute('data-mode') === 'read' && !narrow() && plate) {
      var folio = app.getAttribute('data-view') === 'folio';
      var src = folio ? $('.pane-pic .pic', panel) : null, c = plate.byId[state.sel];
      if (src && c && src.offsetParent) {
        var pr = src.getBoundingClientRect(), cb = cellBox(c, L);
        var panelRight = pr.left - L.left > cb.cx;      // панель справа от буквы
        var x1b = (panelRight ? pr.left : pr.right) - L.left, y1b = pr.top + Math.min(pr.height / 2, 40) - L.top;
        var x2b = panelRight ? cb.x1 : cb.x0, y2b = cb.cy;   // до края ячейки, не на рисунок
        var kx = x1b + (panelRight ? -14 : 14);
        mk('M' + f1(x1b) + ' ' + f1(y1b) + 'L' + f1(kx) + ' ' + f1(y1b) + 'L' + f1(x2b) + ' ' + f1(y2b), x2b, y2b, state.sel);
      }
    }
  }

  /* ---------- выбор и освещение ---------- */
  function applySel() {
    $$('.cell.sel', plate.svg).forEach(function (e) { e.classList.remove('sel'); });
    $$('.note.sel').forEach(function (e) { e.classList.remove('sel'); });
    var c = plate.byId[state.sel];
    if (ringEl && ringEl.parentNode) ringEl.parentNode.removeChild(ringEl);
    ringEl = null;
    if (c) {
      c.el.classList.add('sel');
      var shape = c.el.querySelector('.cell-bg').cloneNode(false);
      shape.setAttribute('class', 'sel-ring');
      shape.setAttribute('transform', c.el.getAttribute('transform'));
      c.el.parentNode.appendChild(shape);
      ringEl = shape;
    }
    if (noteEls[state.sel]) noteEls[state.sel].classList.add('sel');
  }

  function applyLit() {
    scenes.forEach(function (s) {
      var on = !!state.lit[s.id], c = plate.byId[s.id];
      if (c) c.el.classList.toggle('lit', on);
      if (noteEls[s.id]) noteEls[s.id].classList.toggle('lit', on);
    });
    $$('[data-scene]', plate.svg).forEach(function (e) {
      e.classList.toggle('lit', !!state.lit[e.getAttribute('data-scene')]);
    });
    updateCount();
  }

  function litCount() { return scenes.filter(function (s) { return state.lit[s.id]; }).length; }

  function onCell(id) {
    var look = state.mode === 'look';
    if (!picked) { picked = true; app.setAttribute('data-picked', '1'); }
    select(id, { scroll: !look && narrow() });
    if (look) openLightbox(id);
  }

  function select(id, opt) {
    opt = opt || {};
    if (!byId[id]) return;
    state.sel = id;
    applySel();
    renderScene();
    $$('.sbtn', panel).forEach(function (b) { b.classList.toggle('sel', b.getAttribute('data-id') === id); });
    drawLeaders();
    writeUrl();
    if (opt.scroll) {
      var t = $('.p-scene', panel);
      if (t) t.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }

  function step(d) {
    if (!picked) { picked = true; app.setAttribute('data-picked', '1'); }
    var i = byId[state.sel]._i + d;
    if (i < 0 || i >= scenes.length) return;
    select(scenes[i].id, {});
  }

  function toggleLit(id, force) {
    var on = force === undefined ? !state.lit[id] : force;
    if (on) state.lit[id] = 1; else delete state.lit[id];
    save();
    var c = plate.byId[id];
    if (c) {
      c.el.classList.toggle('lit', on);
      if (on) flash(c);
    }
    if (noteEls[id]) noteEls[id].classList.toggle('lit', on);
    $$('[data-scene="' + id + '"]', plate.svg).forEach(function (e) { e.classList.toggle('lit', on); });
    syncPanelLit();
    updateCount();
    var lb = $('#lightbox');
    if (lb.open) fillLightbox(lb.getAttribute('data-id'));
  }
  function flash(c) {
    var shape = c.el.querySelector('.cell-bg').cloneNode(false);
    shape.setAttribute('class', 'flash');
    c.el.appendChild(shape);
    setTimeout(function () { if (shape.parentNode) shape.parentNode.removeChild(shape); }, 1200);
  }
  function setAll(on) {
    scenes.forEach(function (s) {
      if (on) state.lit[s.id] = 1; else delete state.lit[s.id];
    });
    save();
    applyLit();
    syncPanelLit();
    if (on) plate.cells.forEach(function (c, i) { setTimeout(function () { flash(c); }, i * 45); });
  }

  /* ---------- панель ---------- */
  function buildPanel() {
    panel.textContent = '';
    var inn = document.createElement('div');
    inn.className = 'p-in';
    inn.innerHTML =
      '<div class="p-head"><h1 class="p-title"></h1><p class="p-sub"></p><p class="p-by"></p></div>' +
      '<div class="p-count"><div class="ct"><span class="ct-n"></span><em class="ct-l">освещено</em></div><div class="bar"><i></i></div></div>' +
      '<nav class="p-parts" aria-label="Сцены по частям"></nav>' +
      '<section class="p-scene" aria-live="polite">' +
        '<div class="sc-head"><span class="sc-num"></span><h2 class="sc-title"></h2></div>' +
        '<p class="sc-cap"></p>' +
        '<div class="tabs" role="tablist">' +
          '<button type="button" role="tab" data-tab="pic">Картинка</button>' +
          '<button type="button" role="tab" data-tab="sum">Пересказ</button>' +
          '<button type="button" role="tab" data-tab="orig">Оригинал</button>' +
        '</div>' +
        '<div class="pane pane-pic" data-pane="pic"><div class="pic"></div></div>' +
        '<div class="pane pane-sum" data-pane="sum"><div class="pic pic-s"></div><p class="sum"></p></div>' +
        '<div class="pane pane-orig" data-pane="orig"></div>' +
        '<div class="p-note-narrow"></div>' +
      '</section>' +
      '<div class="p-actions"><button type="button" class="nav prev">← Назад</button>' +
        '<button type="button" class="seal" aria-pressed="false"></button>' +
        '<button type="button" class="nav next">Дальше →</button></div>' +
      '<div class="p-done">Буква освещена вся: поток от установки до третьей недели лежит в красках.</div>' +
      '<div class="p-tools"><button type="button" class="linkbtn all">Осветить всё</button>' +
        '<button type="button" class="linkbtn none">Вернуть в тушь</button>' +
        '<button type="button" class="linkbtn to-letter">К букве ↑</button></div>' +
      '<p class="p-foot"></p>';
    panel.appendChild(inn);
    $('.p-title', panel).textContent = P.title || '';
    $('.p-sub', panel).textContent = P.subtitle || '';
    $('.p-by', panel).textContent = P.byline || '';
    // кнопки сцен по частям
    var nav = $('.p-parts', panel);
    (P.parts || []).forEach(function (part) {
      var list = scenes.filter(function (s) { return s.part === part.id; });
      if (!list.length) return;
      var d = document.createElement('div'); d.className = 'part';
      var t = document.createElement('div'); t.className = 'part-t';
      var b = document.createElement('b'); b.textContent = part.id;
      t.appendChild(b); t.appendChild(document.createTextNode(part.title + (part.dates ? ' · ' + part.dates : '')));
      var bs = document.createElement('div'); bs.className = 'part-btns';
      list.forEach(function (s) {
        var bt = document.createElement('button');
        bt.type = 'button'; bt.className = 'sbtn'; bt.setAttribute('data-id', s.id);
        bt.textContent = s.numeral; bt.title = s.caption; bt.setAttribute('aria-label', 'Сцена ' + s.numeral + ': ' + s.caption);
        bt.addEventListener('click', function () { select(s.id, {}); });
        bs.appendChild(bt);
      });
      d.appendChild(t); d.appendChild(bs); nav.appendChild(d);
    });
    $$('.tabs button', panel).forEach(function (b) {
      b.addEventListener('click', function () { state.tab = b.getAttribute('data-tab'); showTab(); drawLeaders(); });
    });
    $('.prev', panel).addEventListener('click', function () { step(-1); });
    $('.next', panel).addEventListener('click', function () { step(1); });
    $('.seal', panel).addEventListener('click', function () { toggleLit(state.sel); });
    $('.all', panel).addEventListener('click', function () { setAll(true); });
    $('.none', panel).addEventListener('click', function () { setAll(false); });
    $('.to-letter', panel).addEventListener('click', function () { $('#stage').scrollIntoView({ behavior: 'smooth', block: 'start' }); });
    $('.p-foot', panel).textContent = P.footnote || 'Страница собрана по записям потока; студентов здесь нет, везде «участник». Слова Риса приведены дословно, с местом и временем в записи.';
  }

  function showTab() {
    $$('.tabs button', panel).forEach(function (b) { b.setAttribute('aria-selected', b.getAttribute('data-tab') === state.tab ? 'true' : 'false'); });
    $$('.pane', panel).forEach(function (p) { p.hidden = app.getAttribute('data-view') === 'folio' ? false : p.getAttribute('data-pane') !== state.tab; });
  }

  function summaryNodes(parts) {
    var frag = document.createDocumentFragment(), k = 0;
    var text = (parts || []).join(' ');
    text.split(/(\[\[[\s\S]*?\]\])/).forEach(function (seg) {
      var m = seg.match(/^\[\[([\s\S]*?)\]\]$/);
      if (m) {
        k++;
        var sp = document.createElement('span');
        sp.className = 'ph'; sp.tabIndex = 0; sp.setAttribute('data-ph', k); sp.textContent = m[1];
        sp.addEventListener('mouseenter', function () { setPh(+sp.getAttribute('data-ph'), sp); });
        sp.addEventListener('mouseleave', function () { setPh(0); });
        sp.addEventListener('focus', function () { setPh(+sp.getAttribute('data-ph'), sp); });
        sp.addEventListener('blur', function () { setPh(0); });
        sp.addEventListener('click', function () { setPh(activePh === +sp.getAttribute('data-ph') ? 0 : +sp.getAttribute('data-ph'), sp); });
        frag.appendChild(sp);
      } else if (seg) frag.appendChild(document.createTextNode(seg));
    });
    return frag;
  }
  function setPh(k, from) {
    activePh = k;
    $$('.ph', panel).forEach(function (e) { e.classList.toggle('on', k && +e.getAttribute('data-ph') === k); });
    var targets = [];
    $$('.pic .sc', panel).forEach(function (e) { targets.push(e); });
    var c = plate && plate.byId[state.sel];
    if (c) { var cs = $('.sc', c.el); if (cs) targets.push(cs); }
    targets.forEach(function (t) {
      var has = k && t.querySelector('[data-ph="' + k + '"]');
      if (has) t.setAttribute('data-active-ph', k); else t.removeAttribute('data-active-ph');
    });
    $$('.pane-sum .pic', panel).forEach(function (p) {
      var any = k && !p.querySelector('[data-ph="' + k + '"]');
      p.classList.toggle('ph-glow', !!any);
    });
  }

  function renderScene() {
    var s = byId[state.sel], part = partById[s.part] || {};
    activePh = 0;
    $('.sc-num', panel).textContent = s.numeral;
    $('.sc-title', panel).textContent = (s.note && s.note.title) || s.caption;
    $('.sc-cap', panel).textContent = s.caption + (part.title ? ' · ' + part.id + ' · ' + part.title : '');
    var pic = $('.pane-pic .pic', panel), pic2 = $('.pane-sum .pic', panel);
    pic.textContent = ''; pic2.textContent = '';
    pic.appendChild(sceneSvg(s.id)); pic2.appendChild(sceneSvg(s.id));
    $('.sum', panel).textContent = '';
    $('.sum', panel).appendChild(summaryNodes(s.summary));
    var o = s.original || {}, op = $('.pane-orig', panel);
    op.textContent = '';
    if (o.quote) {
      var q = document.createElement('blockquote'); q.className = 'q'; q.textContent = '«' + o.quote + '»'; op.appendChild(q);
      var src = document.createElement('p'); src.className = 'q-src';
      var who = document.createElement('b'); who.textContent = o.who || 'Рис';
      src.appendChild(who);
      src.appendChild(document.createTextNode([o.where, o.time ? 'запись ' + o.time : ''].filter(Boolean).length ? ' · ' + [o.where, o.time ? 'запись ' + o.time : ''].filter(Boolean).join(' · ') : ''));
      op.appendChild(src);
    }
    var ul = document.createElement('ul'); ul.className = 'links';
    (o.links || []).forEach(function (l) {
      var li = document.createElement('li'), a = document.createElement('a');
      a.href = l.url; a.textContent = l.label || l.url; a.target = '_blank'; a.rel = 'noopener noreferrer';
      li.appendChild(a); ul.appendChild(li);
    });
    if (!(o.links || []).length) { var li = document.createElement('li'); li.className = 'no'; li.textContent = 'Публичных ссылок к этой сцене нет.'; ul.appendChild(li); }
    op.appendChild(ul);
    // заметка и «на полях» в панели для узких экранов
    var nn = $('.p-note-narrow', panel);
    nn.textContent = '';
    if (s.note) {
      var nm = document.createElement('span'); nm.className = 'nm'; nm.textContent = 'На полях';
      var tx = document.createElement('div'); var b = document.createElement('b'); b.textContent = s.note.title + '. ';
      tx.appendChild(b); tx.appendChild(document.createTextNode(s.note.text));
      nn.appendChild(nm); nn.appendChild(tx);
      if (s.margin && s.margin.length) {
        var mg = document.createElement('div'); mg.className = 'mg';
        s.margin.forEach(function (m) { var sp = document.createElement('span'); sp.textContent = '· ' + m; mg.appendChild(sp); });
        nn.appendChild(mg);
      }
    }
    $('.prev', panel).disabled = s._i === 0;
    $('.next', panel).disabled = s._i === scenes.length - 1;
    showTab();
    syncPanelLit();
  }

  function syncPanelLit() {
    var on = !!state.lit[state.sel];
    $$('.pane .pic', panel).forEach(function (p) { p.classList.toggle('lit', on); });
    var seal = $('.seal', panel);
    seal.setAttribute('aria-pressed', on ? 'true' : 'false');
    seal.textContent = on ? 'Освещено' : 'Осветить';
    seal.title = on ? 'Вернуть сцену в тушь' : 'Раскрасить сцену, ячейку и орнамент рядом';
    $$('.sbtn', panel).forEach(function (b) { b.classList.toggle('lit', !!state.lit[b.getAttribute('data-id')]); });
  }

  function updateCount() {
    var n = litCount(), t = scenes.length;
    $('.ct-n', panel).textContent = n + ' / ' + t;
    $('.bar i', panel).style.width = (100 * n / t) + '%';
    app.setAttribute('data-all', n === t ? '1' : '0');
    $$('.sbtn', panel).forEach(function (b) { b.classList.toggle('lit', !!state.lit[b.getAttribute('data-id')]); });
  }

  /* ---------- окно сцены (режим «Смотреть») ---------- */
  var lb = $('#lightbox');
  function fillLightbox(id) {
    var s = byId[id];
    lb.setAttribute('data-id', id);
    lb.textContent = '';
    var f = document.createElement('div'); f.className = 'lb-in';
    var h = document.createElement('div'); h.className = 'lb-h';
    var t = document.createElement('span'); t.className = 'lb-t'; t.textContent = s.numeral + ' · ' + ((s.note && s.note.title) || s.caption);
    var x = document.createElement('button'); x.type = 'button'; x.className = 'nav'; x.textContent = '✕'; x.setAttribute('aria-label', 'Закрыть');
    x.addEventListener('click', function () { lb.close(); });
    h.appendChild(t); h.appendChild(x);
    var pic = document.createElement('div'); pic.className = 'pic' + (state.lit[id] ? ' lit' : '');
    pic.appendChild(sceneSvg(id));
    var p = document.createElement('p'); p.className = 'lb-s';
    p.textContent = (s.summary || []).join(' ').replace(/\[\[|\]\]/g, '');
    // дополнения «на полях»: на самих полях их нет, чтобы заметки стояли рядом со своими ячейками
    var mg = null;
    if (s.margin && s.margin.length) {
      mg = document.createElement('div'); mg.className = 'lb-mg';
      var mh = document.createElement('span'); mh.className = 'nm'; mh.textContent = 'На полях';
      mg.appendChild(mh);
      s.margin.forEach(function (m) { var sp = document.createElement('span'); sp.textContent = '· ' + m; mg.appendChild(sp); });
    }
    var row = document.createElement('div'); row.className = 'p-actions';
    var seal = document.createElement('button'); seal.type = 'button'; seal.className = 'seal';
    seal.setAttribute('aria-pressed', state.lit[id] ? 'true' : 'false'); seal.textContent = state.lit[id] ? 'Освещено' : 'Осветить';
    seal.addEventListener('click', function () { toggleLit(id); });
    var rd = document.createElement('button'); rd.type = 'button'; rd.className = 'nav'; rd.textContent = 'Читать →';
    rd.addEventListener('click', function () { lb.close(); setMode('read'); select(id, { scroll: narrow() }); });
    row.appendChild(seal); row.appendChild(rd);
    f.appendChild(h); f.appendChild(pic); f.appendChild(p);
    if (mg) f.appendChild(mg);
    f.appendChild(row);
    lb.appendChild(f);
  }
  function openLightbox(id) {
    if (typeof lb.showModal !== 'function') { setMode('read'); return; }
    fillLightbox(id);
    if (!lb.open) lb.showModal();
  }
  lb.addEventListener('click', function (e) { if (e.target === lb) lb.close(); });

  /* ---------- режимы ---------- */
  function syncSegs() {
    $$('#seg-letters button').forEach(function (b) { b.setAttribute('aria-pressed', b.getAttribute('data-bukva') === state.bukva ? 'true' : 'false'); });
    $$('#seg-view button').forEach(function (b) { b.setAttribute('aria-pressed', b.getAttribute('data-view') === state.view ? 'true' : 'false'); });
    $$('#seg-mode button').forEach(function (b) { b.setAttribute('aria-pressed', b.getAttribute('data-mode') === state.mode ? 'true' : 'false'); });
    app.setAttribute('data-mode', state.mode);
    app.setAttribute('data-view', state.view);
    $('#seg-view').style.display = state.mode === 'look' ? 'none' : '';
  }
  function setMode(m) { state.mode = m; syncSegs(); save(); writeUrl(); relayout(true); }
  function setView(v) { state.view = v; syncSegs(); save(); writeUrl(); showTab(); relayout(true); }
  function setBukva(b) { state.bukva = b; syncSegs(); writeUrl(); relayout(true); }

  var raf = 0;
  function relayout(force) {
    cancelAnimationFrame(raf);
    raf = requestAnimationFrame(function () {
      var w = wrap.parentNode.clientWidth;
      // высота окна важна только в «Читать» на широком экране: там буква вписана в окно
      var hChanged = state.mode === 'read' && !narrow() && Math.abs(window.innerHeight - lastH) > 40;
      if (force || !plate || Math.abs(w - lastW) > 3 || hChanged) renderPlate();
      else layoutNotes();
    });
  }

  /* ---------- запуск ---------- */
  function init() {
    load(); readUrl();
    $('#foot').textContent = P.foot || '';
    document.title = (P.title || 'Буквица') + ' · Personal Corp 3';
    buildPanel();
    syncSegs();
    app.setAttribute('data-picked', '0');
    $$('#seg-letters button').forEach(function (b) { b.addEventListener('click', function () { setBukva(b.getAttribute('data-bukva')); }); });
    $$('#seg-view button').forEach(function (b) { b.addEventListener('click', function () { setView(b.getAttribute('data-view')); }); });
    $$('#seg-mode button').forEach(function (b) { b.addEventListener('click', function () { setMode(b.getAttribute('data-mode')); }); });
    window.addEventListener('resize', function () { relayout(false); });
    var sraf = 0;
    function onScroll() {
      if (app.getAttribute('data-view') !== 'folio' || app.getAttribute('data-mode') !== 'read') return;
      cancelAnimationFrame(sraf); sraf = requestAnimationFrame(drawLeaders);
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    panel.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('keydown', function (e) {
      if (e.target && /INPUT|TEXTAREA|SELECT/.test(e.target.tagName)) return;
      if (e.altKey || e.metaKey || e.ctrlKey) return;
      if (e.key === 'ArrowRight') step(1);
      if (e.key === 'ArrowLeft') step(-1);
    });
    window.addEventListener('hashchange', function () {
      var h = location.hash.replace('#', '');
      if (byId[h] && h !== state.sel) select(h, {});
    });
    if (window.ResizeObserver) new ResizeObserver(function () { relayout(false); }).observe(wrap);
    // подписи лент меряются шрифтом; когда он догрузится, подгоняем заново
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(refitCaptions);
    if (document.fonts && document.fonts.load) document.fonts.load('700 10px "Cormorant Garamond"').then(refitCaptions, function () {});
    loadAll().then(function () {
      renderPlate();
      renderScene();
      select(state.sel, {});
      updateCount();
      document.documentElement.setAttribute('data-ready', '1');
    });
  }
  PC.app = { state: state, select: select, toggleLit: toggleLit, setAll: setAll, setMode: setMode, setView: setView, setBukva: setBukva };
  init();
})();
