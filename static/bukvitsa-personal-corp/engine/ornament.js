/* Орнамент вокруг буквы: шнур-рамка, побеги с листьями и ягодами,
   завитки на концах штрихов, цветок в просвете буквы.
   Всё рисуется тушью; элементы с data-cell окрашиваются, когда
   освещена их ячейка (листья зеленеют, ягоды краснеют, шарики золотятся). */
(function () {
  var PC = (window.PC = window.PC || {});
  var NS = 'http://www.w3.org/2000/svg';
  var PAD = 84;

  function rngFor(seed) {
    var a = 0;
    for (var i = 0; i < seed.length; i++) a = (a * 31 + seed.charCodeAt(i)) >>> 0;
    return function () {
      a |= 0; a = (a + 0x6d2b79f5) | 0;
      var t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  function el(tag, attrs, parent) {
    var e = document.createElementNS(NS, tag);
    for (var k in attrs) e.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(e);
    return e;
  }
  function f(n) { return Math.round(n * 10) / 10; }

  function distSeg(px, py, ax, ay, bx, by) {
    var dx = bx - ax, dy = by - ay, l2 = dx * dx + dy * dy;
    var t = l2 ? ((px - ax) * dx + (py - ay) * dy) / l2 : 0;
    t = Math.max(0, Math.min(1, t));
    var qx = ax + t * dx, qy = ay + t * dy;
    return Math.hypot(px - qx, py - qy);
  }
  function clearance(g, x, y) {            // расстояние до ближайшего края полосы
    var d = 1e9;
    g.paths.forEach(function (p) {
      var n = p.pts.length;
      for (var i = 0; i < n - (p.closed ? 0 : 1); i++) {
        var a = p.pts[i], b = p.pts[(i + 1) % n];
        d = Math.min(d, distSeg(x, y, a[0], a[1], b[0], b[1]) - p.w / 2);
      }
    });
    return d;
  }

  /* шнур: две пряди по скруглённому прямоугольнику */
  function roundedPoints(x0, y0, x1, y1, r, step) {
    var pts = [], i, n;
    function arc(cx, cy, a0) {
      n = Math.max(4, Math.round((Math.PI / 2) * r / step));
      for (i = 0; i <= n; i++) {
        var a = a0 + (Math.PI / 2) * (i / n);
        pts.push([cx + r * Math.cos(a), cy + r * Math.sin(a)]);
      }
    }
    function line(ax, ay, bx, by) {
      var l = Math.hypot(bx - ax, by - ay), m = Math.max(1, Math.round(l / step));
      for (i = 1; i < m; i++) pts.push([ax + (bx - ax) * i / m, ay + (by - ay) * i / m]);
    }
    arc(x1 - r, y0 + r, -Math.PI / 2);
    line(x1, y0 + r, x1, y1 - r);
    arc(x1 - r, y1 - r, 0);
    line(x1 - r, y1, x0 + r, y1);
    arc(x0 + r, y1 - r, Math.PI / 2);
    line(x0, y1 - r, x0, y0 + r);
    arc(x0 + r, y0 + r, Math.PI);
    line(x0 + r, y0, x1 - r, y0);
    return pts;
  }

  function strand(pts, amp, wl, phase) {
    var d = '', s = 0, n = pts.length;
    for (var i = 0; i < n; i++) {
      var p = pts[i], q = pts[(i + 1) % n], o = pts[(i + n - 1) % n];
      var tx = q[0] - o[0], ty = q[1] - o[1], tl = Math.hypot(tx, ty) || 1;
      var nx = -ty / tl, ny = tx / tl;
      if (i) s += Math.hypot(p[0] - o[0], p[1] - o[1]);
      var w = amp * Math.sin((2 * Math.PI * s) / wl + phase);
      d += (i ? 'L' : 'M') + f(p[0] + nx * w) + ' ' + f(p[1] + ny * w);
    }
    return d + 'Z';
  }

  function leafPath(s) {
    return 'M0 0C' + f(s * 0.3) + ' ' + f(-s * 0.46) + ' ' + f(s * 0.78) + ' ' + f(-s * 0.46) + ' ' + f(s) + ' 0C' +
      f(s * 0.78) + ' ' + f(s * 0.46) + ' ' + f(s * 0.3) + ' ' + f(s * 0.46) + ' 0 0Z';
  }

  function build(g, key) {
    var rnd = rngFor(key || g.letter + g.cells.length);
    var b = g.bbox;
    var F = { x0: b.x0 - PAD, y0: b.y0 - PAD, x1: b.x1 + PAD, y1: b.y1 + PAD };
    var root = el('g', { class: 'orn' });

    function nearest(x, y) {
      var bi = 0, bd = 1e9;
      g.cells.forEach(function (c, i) {
        var d = Math.hypot(c.x - x, c.y - y);
        if (d < bd) { bd = d; bi = i; }
      });
      return bi;
    }
    function tag(e, x, y) { e.setAttribute('data-cell', nearest(x, y)); return e; }

    /* шнур */
    var cord = roundedPoints(F.x0, F.y0, F.x1, F.y1, 30, 3);
    el('path', { class: 'orn-ln', d: strand(cord, 3.6, 22, 0) }, root);
    el('path', { class: 'orn-ln', d: strand(cord, 3.6, 22, Math.PI) }, root);
    var o1 = roundedPoints(F.x0 - 9, F.y0 - 9, F.x1 + 9, F.y1 + 9, 38, 8);
    el('path', { class: 'orn-hair', d: 'M' + o1.map(function (q) { return f(q[0]) + ' ' + f(q[1]); }).join('L') + 'Z' }, root);

    /* узлы в углах рамки */
    [[F.x0, F.y0], [F.x1, F.y0], [F.x1, F.y1], [F.x0, F.y1]].forEach(function (c) {
      var kn = el('g', {}, root);
      el('circle', { class: 'orn-ln', cx: c[0], cy: c[1], r: 11 }, kn);
      tag(el('circle', { class: 'orn-gold', cx: c[0], cy: c[1], r: 6.4 }, kn), c[0], c[1]);
      el('circle', { class: 'orn-ink', cx: c[0], cy: c[1], r: 1.6 }, kn);
    });

    function leaf(x, y, ang, s, cell) {
      var gl = el('g', { transform: 'translate(' + f(x) + ' ' + f(y) + ') rotate(' + f(ang) + ')' }, root);
      var l = el('path', { class: 'orn-leaf', d: leafPath(s) }, gl);
      l.setAttribute('data-cell', cell);
      el('path', { class: 'orn-ln', d: 'M0 0L' + f(s * 0.82) + ' 0' }, gl);
    }
    function berry(x, y, r, cell) {
      var c = el('circle', { class: 'orn-berry', cx: f(x), cy: f(y), r: r }, root);
      c.setAttribute('data-cell', cell);
    }

    /* побег: стебель по кривой, листья по сторонам, ягода или завиток на конце */
    function sprig(bx, by, dx, dy, len, cell) {
      var nx = -dy, ny = dx, bend = (rnd() - 0.5) * len * 0.5;
      var ex = bx + dx * len + nx * bend, ey = by + dy * len + ny * bend;
      var cx = bx + dx * len * 0.5 + nx * bend * 1.6, cy = by + dy * len * 0.5 + ny * bend * 1.6;
      el('path', { class: 'orn-ln', d: 'M' + f(bx) + ' ' + f(by) + 'Q' + f(cx) + ' ' + f(cy) + ' ' + f(ex) + ' ' + f(ey) }, root);
      function at(t) {
        var u = 1 - t;
        return [u * u * bx + 2 * u * t * cx + t * t * ex, u * u * by + 2 * u * t * cy + t * t * ey,
          Math.atan2(2 * u * (cy - by) + 2 * t * (ey - cy), 2 * u * (cx - bx) + 2 * t * (ex - cx)) * 180 / Math.PI];
      }
      var side = rnd() < 0.5 ? 1 : -1, ts = len > 52 ? [0.38, 0.7] : [0.6];
      ts.forEach(function (t, i) {
        var q = at(t), s = 17 + rnd() * 6;
        leaf(q[0], q[1], q[2] + side * (38 + rnd() * 14), s, cell);
        side = -side;
      });
      var q = at(1);
      if (rnd() < 0.55) berry(q[0], q[1], 5.2 + rnd() * 1.8, cell);
      else leaf(q[0], q[1], q[2] + (rnd() - 0.5) * 30, 17, cell);
    }

    /* кандидаты на побеги вдоль штрихов */
    var count = 0, maxSprigs = Math.max(4, Math.round(g.cells.length * 0.9));
    g.paths.forEach(function (p) {
      var n = p.pts.length, half = p.w / 2;
      for (var i = 0; i < n - (p.closed ? 0 : 1); i++) {
        var a = p.pts[i], c = p.pts[(i + 1) % n];
        var sl = Math.hypot(c[0] - a[0], c[1] - a[1]);
        if (sl < 20) continue;
        var ux = (c[0] - a[0]) / sl, uy = (c[1] - a[1]) / sl;
        var steps = Math.max(1, Math.floor(sl / 140));
        for (var s = 0; s < steps; s++) {
          if (count >= maxSprigs) return;
          var t = (s + 0.5 + (rnd() - 0.5) * 0.4) / steps;
          var px = a[0] + (c[0] - a[0]) * t, py = a[1] + (c[1] - a[1]) * t;
          var sides = rnd() < 0.5 ? [1, -1] : [-1, 1];
          for (var k = 0; k < 2; k++) {
            var nx = -uy * sides[k], ny = ux * sides[k];
            // свободная длина наружу от края полосы
            var free = 0, st;
            if (clearance(g, px + nx * (half + 3), py + ny * (half + 3)) < 1) continue;
            for (st = half + 4; st < half + 130; st += 6) {
              var qx = px + nx * st, qy = py + ny * st;
              if (qx < F.x0 + 18 || qx > F.x1 - 18 || qy < F.y0 + 18 || qy > F.y1 - 18) break;
              if (clearance(g, qx, qy) < (st - half) - 4) break;
              free = st - half;
            }
            if (free >= 34 && rnd() < 0.7) {
              var len = Math.min(free - 8, 54 + rnd() * 26);
              var bx = px + nx * (half - 4), by = py + ny * (half - 4);
              sprig(bx, by, nx, ny, len, nearest(px, py));
              count++;
              break;
            }
          }
        }
      }
    });

    /* завитки на свободных концах штрихов */
    (g.ends || []).forEach(function (e) {
      var l = Math.hypot(e.dx, e.dy) || 1, dx = e.dx / l, dy = e.dy / l;
      var sx = e.x + dx * ((PC.glyphs.BAND / 2) - 8), sy = e.y + dy * ((PC.glyphs.BAND / 2) - 8);
      var cell = nearest(e.x, e.y);
      var r0 = 30, turns = 1.3, hd = Math.atan2(dy, dx), ch = Math.cos(hd), sh = Math.sin(hd);
      var pts = [];
      for (var i = 0; i <= 44; i++) {
        var t = i / 44, th = -Math.PI / 2 + Math.PI * 2 * turns * t, r = r0 * (1 - 0.8 * t);
        var lx = r * Math.cos(th), ly = r0 + r * Math.sin(th);
        pts.push([sx + lx * ch - ly * sh, sy + lx * sh + ly * ch]);
      }
      var shift = [0, 0];
      var d = pts.map(function (q, i) { return (i ? 'L' : 'M') + f(q[0]) + ' ' + f(q[1]); }).join('');
      el('path', { class: 'orn-ln', d: d }, root);
      var tip = pts[pts.length - 1];
      berry(tip[0] + shift[0], tip[1] + shift[1], 5.4, cell);
      leaf(sx + dx * 14, sy + dy * 14, Math.atan2(dy, dx) * 180 / Math.PI + 70, 20, cell);
    });

    /* цветок в просвете буквы */
    function flower(cx, cy, R, cell) {
      var gl = el('g', { transform: 'translate(' + f(cx) + ' ' + f(cy) + ')' }, root);
      for (var k = 0; k < 4; k++) {
        var pe = el('path', { class: 'orn-petal', d: 'M0 0C' + f(R * 0.5) + ' ' + f(-R * 0.55) + ' ' + f(R * 0.9) + ' ' + f(-R * 0.3) + ' 0 ' + f(-R) + 'C' + f(-R * 0.9) + ' ' + f(-R * 0.3) + ' ' + f(-R * 0.5) + ' ' + f(-R * 0.55) + ' 0 0Z', transform: 'rotate(' + (k * 90 + 45) + ')' }, gl);
        pe.setAttribute('data-cell', cell);
      }
      var c = el('circle', { class: 'orn-gold', cx: 0, cy: 0, r: R * 0.2 }, gl);
      c.setAttribute('data-cell', cell);
      el('circle', { class: 'orn-ink', cx: 0, cy: 0, r: R * 0.05 }, gl);
    }
    (g.counters || []).forEach(function (c) {
      var m = Math.min(c.w, c.h);
      if (m >= 70) flower(c.x, c.y, Math.min(34, m * 0.36), nearest(c.x, c.y));
    });
    (g.rosettes || []).forEach(function (r) { flower(r.x, r.y, 20, nearest(r.x, r.y)); });

    return { group: root, frame: F };
  }

  PC.ornament = { build: build, PAD: PAD };
})();
