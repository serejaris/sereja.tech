/* Форма букв буквицы: C, O, R, P из толстых штрихов-полос.
   В штрихах лежат прямоугольные ячейки (150x100, в горизонтальных планках)
   и круглые медальоны (диаметр 120, в стойках и на ноге буквы R).
   Когда сцен много (одна буква на все сцены), стойки удваиваются:
   два столбца медальонов, как в тяжёлой романской буквице.
   Число ячеек подстраивается: перебираем варианты размеров и берём тот,
   у которого пропорции буквы ближе всего к идеальным. */
(function () {
  var PC = (window.PC = window.PC || {});

  var RW = 150, RH = 100;        // прямоугольная ячейка
  var MR = 60, MP = 124;         // радиус и шаг медальонов
  var EX = 119, EY = 94;         // «локоть»: смещение от планки к стойке
  var BAND = 136;                // толщина полосы-штриха
  var WIDE = BAND + MP;          // толщина двойной стойки

  function rect(x, y) { return { kind: 'rect', x: x, y: y, w: RW, h: RH }; }
  function med(x, y) { return { kind: 'med', x: x, y: y, r: MR }; }
  function seg(pts, closed, w, cap) { return { pts: pts, closed: !!closed, w: w || BAND, cap: cap || 'round' }; }

  /* стойка из m рядов: внутренний столбец на x, внешний на x + dir*124 */
  function stem(cells, x, y0, m, sw, dir) {
    for (var j = 0; j < m; j++) {
      cells.push(med(x, y0 + MP * j));
      if (sw === 2) cells.push(med(x + dir * MP, y0 + MP * j));
    }
  }
  function stemBand(paths, x, y0, m, dir) { // широкая полоса под двойной стойкой
    paths.push(seg([[x + dir * MP / 2, y0 - 40], [x + dir * MP / 2, y0 + MP * (m - 1) + 40]], false, WIDE, 'butt'));
  }

  /* ---------- построители букв ---------- */

  function buildC(p) {
    var cells = [], paths = [], i;
    var yb = MP * p.m + 64;
    for (i = 0; i < p.at; i++) cells.push(rect(EX + RW * i, 0));
    stem(cells, 0, EY, p.m, p.sw, -1);
    for (i = 0; i < p.ab; i++) cells.push(rect(EX + RW * i, yb));
    var path = [
      [EX + RW * (p.at - 1) + 75, 0], [EX, 0], [0, EY],
      [0, EY + MP * (p.m - 1)], [EX, yb], [EX + RW * (p.ab - 1) + 75, yb]
    ];
    paths.push(seg(path, false));
    if (p.sw === 2) stemBand(paths, 0, EY, p.m, -1);
    var sx = p.sw === 2 ? -MP / 2 : 0;
    return {
      cells: cells, paths: paths, counters: [],
      ends: [{ x: path[0][0], y: path[0][1], dx: 1, dy: 0 }, { x: path[5][0], y: path[5][1], dx: 1, dy: 0 }],
      rosettes: [], mouth: { x: EX + RW * Math.max(p.at, p.ab) + 20, y: yb / 2 }, sx: sx
    };
  }

  function buildO(p) {
    var cells = [], paths = [], i, m = p.m, sw = p.sw;
    var yb = m > 0 ? MP * m + 64 : 188;
    var hw = Math.max(p.at, p.ab);
    var xr = RW * (hw - 1) / 2 + EX;
    for (i = 0; i < p.at; i++) cells.push(rect(RW * (i - (p.at - 1) / 2), 0));
    stem(cells, xr, EY, m, sw, 1);
    stem(cells, -xr, EY, m, sw, -1);
    for (i = 0; i < p.ab; i++) cells.push(rect(RW * (i - (p.ab - 1) / 2), yb));
    var tw = RW * (p.at - 1) / 2, bw = RW * (p.ab - 1) / 2;
    var y1 = m > 0 ? EY + MP * (m - 1) : EY;
    paths.push(seg([[-tw, 0], [tw, 0], [xr, EY], [xr, y1], [bw, yb], [-bw, yb], [-xr, y1], [-xr, EY]], true));
    if (sw === 2 && m > 0) { stemBand(paths, xr, EY, m, 1); stemBand(paths, -xr, EY, m, -1); }
    var inner = 2 * xr - 120;
    return {
      cells: cells, paths: paths,
      counters: [{ x: 0, y: yb / 2, w: inner, h: yb - 100 }],
      ends: [], rosettes: m === 0 ? [{ x: xr, y: EY }, { x: -xr, y: EY }] : []
    };
  }

  function buildPR(p, withLeg) {
    var cells = [], paths = [], i, j;
    var a = p.a, mb = p.mb, ms = p.ms, k = withLeg ? p.k : 0, sw = p.sw;
    var X0 = 150;                               // первая планка (правее стойки)
    var xr = X0 + RW * (a - 1) + EX;            // x стойки чаши
    var ym = mb > 0 ? MP * mb + 64 : 188;       // y средней планки
    for (i = 0; i < a; i++) cells.push(rect(X0 + RW * i, 0));
    stem(cells, 0, EY, ms, sw, -1);
    for (j = 0; j < mb; j++) cells.push(med(xr, EY + MP * j));
    for (i = 0; i < a; i++) cells.push(rect(X0 + RW * i, ym));
    var legPts = [];
    for (j = 0; j < k; j++) { cells.push(med(xr + 38 * j, ym + EY + MP * j)); legPts.push([xr + 38 * j, ym + EY + MP * j]); }
    var endX = X0 + RW * (a - 1);
    var stemEnd = EY + MP * (ms - 1);
    paths.push(seg([[0, stemEnd], [0, EY], [X0, 0], [endX + 75, 0]], false));
    paths.push(seg([[endX + 75, 0], [xr, EY], [xr, mb > 0 ? EY + MP * (mb - 1) : EY], [endX, ym], [X0, ym], [0, ym]], false));
    if (k > 0) paths.push(seg([[endX, ym], [xr, ym + EY]].concat(legPts.slice(1)), false));
    if (sw === 2) stemBand(paths, 0, EY, ms, -1);
    var ends = [{ x: sw === 2 ? -MP / 2 : 0, y: stemEnd + (sw === 2 ? 40 : 0), dx: 0, dy: 1 }];
    if (k > 0) { var l = legPts[legPts.length - 1]; ends.push({ x: l[0], y: l[1], dx: 0.3, dy: 1 }); }
    return {
      cells: cells, paths: paths,
      counters: [{ x: xr / 2, y: ym / 2, w: xr - 120, h: ym - 100 }],
      ends: ends, rosettes: mb === 0 ? [{ x: xr, y: EY }] : []
    };
  }

  /* ---------- перебор вариантов ---------- */

  function bbox(g) {
    var x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9;
    g.cells.forEach(function (c) {
      var hw = c.kind === 'rect' ? c.w / 2 : c.r, hh = c.kind === 'rect' ? c.h / 2 : c.r;
      x0 = Math.min(x0, c.x - hw); x1 = Math.max(x1, c.x + hw);
      y0 = Math.min(y0, c.y - hh); y1 = Math.max(y1, c.y + hh);
    });
    g.paths.forEach(function (p) {
      var h = p.w / 2;
      p.pts.forEach(function (q) {
        var capv = p.cap === 'butt' ? 0 : h;
        x0 = Math.min(x0, q[0] - h); x1 = Math.max(x1, q[0] + h);
        y0 = Math.min(y0, q[1] - capv); y1 = Math.max(y1, q[1] + capv);
      });
    });
    return { x0: x0, y0: y0, x1: x1, y1: y1, w: x1 - x0, h: y1 - y0 };
  }

  function weightPen(n, sw) {
    if (sw === 2) return n < 11 ? 2 : 0;
    return n >= 14 ? 0.5 : (n >= 11 ? 0.15 : 0);
  }

  function options(letter, n) {
    var out = [], at, ab, m, a, mb, ms, k, sw, p;
    for (sw = 1; sw <= 2; sw++) {
      if (letter === 'C') {
        for (at = 1; at <= 12; at++) for (ab = Math.max(1, at - 1); ab <= at + 1; ab++) {
          m = (n - at - ab) / sw; if (m < 1 || m !== Math.floor(m)) continue;
          out.push({ p: { at: at, ab: ab, m: m, sw: sw }, ideal: 1.12, pen: weightPen(n, sw) + Math.abs(at - ab) * 0.06 + (at < ab ? 0.05 : 0) + (m === 1 && n > 6 ? 0.2 : 0) });
        }
      } else if (letter === 'O') {
        for (at = 1; at <= 12; at++) for (ab = Math.max(1, at - 1); ab <= at; ab++) {
          m = (n - at - ab) / (2 * sw); if (m < 0 || m !== Math.floor(m)) continue;
          if (sw === 2 && m < 1) continue;
          out.push({ p: { at: at, ab: ab, m: m, sw: sw }, ideal: 1.2, pen: weightPen(n, sw) + (at - ab) * 0.05 + (m === 0 ? 0.25 : 0) + (at + ab === 2 ? 0.4 : 0) });
        }
      } else if (letter === 'P') {
        for (a = 1; a <= 9; a++) for (mb = 0; mb <= 9; mb++) for (ms = mb + 1; ms <= mb + 5; ms++) {
          if (sw * ms + 2 * a + mb !== n) continue;
          out.push({ p: { a: a, mb: mb, ms: ms, sw: sw }, ideal: 1.4, pen: weightPen(n, sw) + (mb === 0 ? 0.3 : 0) + (ms - mb - 1) * 0.04 + (a === 1 && n > 7 ? 0.3 : 0) });
        }
      } else if (letter === 'R') {
        for (a = 1; a <= 9; a++) for (mb = 0; mb <= 9; mb++) for (k = 1; k <= 9; k++) for (ms = mb + k - 1; ms <= mb + k + 1; ms++) {
          if (ms < mb + 1 || sw * ms + 2 * a + mb + k !== n) continue;
          out.push({ p: { a: a, mb: mb, ms: ms, k: k, sw: sw }, ideal: 1.4, pen: weightPen(n, sw) + (mb === 0 ? 0.3 : 0) + Math.abs(ms - mb - k) * 0.05 + (a === 1 && n > 7 ? 0.3 : 0) + (k > mb + 2 ? 0.2 : 0) });
        }
      }
    }
    return out;
  }

  function make(letter, p) {
    if (letter === 'C') return buildC(p);
    if (letter === 'O') return buildO(p);
    if (letter === 'P') return buildPR(p, false);
    return buildPR(p, true);
  }

  /* порядок чтения: сверху вниз, внутри ряда слева направо */
  function sortReading(cells) {
    var arr = cells.slice().sort(function (a, b) { return a.y - b.y || a.x - b.x; });
    var rows = [], cur = [arr[0]];
    for (var i = 1; i < arr.length; i++) {
      if (arr[i].y - cur[cur.length - 1].y < 45) cur.push(arr[i]); else { rows.push(cur); cur = [arr[i]]; }
    }
    rows.push(cur);
    var res = [];
    rows.forEach(function (r) { r.sort(function (a, b) { return a.x - b.x; }); res = res.concat(r); });
    return res;
  }

  /* главный вход: буква и число ячеек */
  function build(letter, n) {
    n = Math.max(3, n | 0);
    var opts = options(letter, n), best = null, bestScore = 1e9, dn;
    for (dn = 1; dn < 5 && !opts.length; dn++) opts = options(letter, n + dn);
    opts.forEach(function (o) {
      var g = make(letter, o.p), b = bbox(g);
      var s = Math.abs(b.h / b.w - o.ideal) + o.pen;
      if (s < bestScore) { bestScore = s; best = { g: g, p: o.p }; }
    });
    var g = best.g;
    g.cells = sortReading(g.cells);
    g.cells.forEach(function (c, i) { c.idx = i; });
    g.bbox = bbox(g);
    g.letter = letter;
    g.params = best.p;
    return g;
  }

  PC.glyphs = { build: build, BAND: BAND, RW: RW, RH: RH, MR: MR };
})();
