/*
 * Полка каталога в шапке статьи: восемь коробок, по одной на крупную тему
 * раздела по тегам INDEX.md в corp-research (origin/main, 6 октября 2026 года).
 * Толщина коробки это число отчётов по теме. На фасаде каждой коробки
 * надпись темы, как на корешке; это сознательное исключение из правила
 * Hairline «в рисунке нет текста» по слову Риса 06.10.2026.
 *
 * Движение идёт от прокрутки страницы, курсор не нужен. Доля прокрутки,
 * пока полка в кадре, сглаживается пружиной и прогоняет по полке волну:
 * коробки по очереди выдвигаются к читателю и встают обратно, как будто
 * листаешь полку слева направо. В покое коробки стоят чуть вразнобой,
 * claude-code выдвинута и выделена. При prefers-reduced-motion полка
 * остаётся в позе покоя.
 *
 * Рисует движок Hairline (hairline-kernel.js, MIT, Lucas Marques): фигура
 * сделана по образцу shelf из набора, без страницы-стенда, ползунка и темы.
 */
(function () {
  var host = document.getElementById("hl-shelf");
  if (!host || !window.HL) return;
  var stage = host.querySelector(".hl-stage");
  var readEl = host.querySelector(".hl-read");
  var Cam = HL.Cam, facing = HL.facing, fit = HL.fit, prism = HL.prism,
    proj = HL.proj, rings = HL.rings, mk = HL.mk, put = HL.put, solid = HL.solid,
    spring = HL.spring, stepS = HL.stepS, register = HL.register;

  /* надпись на корешке, тег каталога, число отчётов, слово к числу
     (слово Риса 06.10.2026: «здесь нужны подписи типа рилсы, законы, агенты») */
  var TOPICS = [
    ["агенты", "agent", 118, "отчётов"], ["Claude Code", "claude-code", 100, "отчётов"],
    ["видео и рилсы", "video", 55, "отчётов"], ["Telegram", "telegram", 54, "отчёта"],
    ["обучение", "education", 48, "отчётов"], ["дизайн", "design", 47, "отчётов"],
    ["цены", "pricing", 35, "отчётов"], ["законы", "legal", 5, "отчётов"]
  ];
  var N = TOPICS.length;
  var K = 0.24, GAP = 2.6, D = 40, H = 52, R = 2.4, B = 1;
  /* MINW: коробка не тоньше строки надписи; у «законов» 5 отчётов дали бы
     1,2 единицы, поэтому она толще пропорции, но остаётся самой тонкой */
  var FS = 4.2, MINW = 7.4, TXT0 = 5;
  var REST = [3, 9, 0.5, 1.5, 0, 4, 1, 2.5], STAR = 1, PULL = 16, WAVE = 1.25;
  var PLANK = 5, POST = 6, BACK = 3, TOPZ = H + 14;

  var x = GAP;
  var spans = TOPICS.map(function (t) { var w = Math.max(MINW, t[2] * K), s = [x, x + w]; x += w + GAP; return s; });
  var L = x;

  var C = Cam(16, 0.5, 1.6);
  fit(C, [[-POST, -BACK, -PLANK], [L + POST, D + 6 + PULL, TOPZ]], 200, 160);
  var P = proj(C), front = facing(C);

  /* рамка рисунка: углы полки и передние углы коробок при наибольшем выдвижении */
  var pts = [];
  [-POST, L + POST].forEach(function (px) {
    [-BACK, D + 6].forEach(function (py) {
      [-PLANK, TOPZ].forEach(function (pz) { pts.push(P(px, py, pz)); });
    });
  });
  spans.forEach(function (s) {
    [s[0], s[1]].forEach(function (px) { pts.push(P(px, D + PULL, 0), P(px, D + PULL, H)); });
  });
  var PAD = 4;
  var x0 = Math.min.apply(null, pts.map(function (q) { return q[0]; })) - PAD;
  var y0 = Math.min.apply(null, pts.map(function (q) { return q[1]; })) - PAD;
  var x1 = Math.max.apply(null, pts.map(function (q) { return q[0]; })) + PAD;
  var y1 = Math.max.apply(null, pts.map(function (q) { return q[1]; })) + PAD;
  var vw = x1 - x0, vh = y1 - y0;

  HL.inject(document);
  stage.setAttribute("data-hairline", "shelf");
  stage.style.aspectRatio = vw.toFixed(1) + " / " + vh.toFixed(1);
  var svg = mk("svg", { viewBox: [x0, y0, vw, vh].map(function (n) { return n.toFixed(1); }).join(" "), "aria-hidden": "true" }, stage);
  var g = mk("g", {}, svg);

  /* сзади вперёд: задняя стенка, левая стойка, полка, коробки слева направо, правая стойка */
  function block(ax, ay, bx, by, z0, z1, r, b) {
    var rr = rings(ax, ay, bx, by, r, b);
    put(solid(g), prism(P, front, rr[0], rr[1], z0, z1));
  }
  block(-POST, -BACK, L + POST, 0, -PLANK, TOPZ, 1.2, 0.6);
  block(-POST, 0, 0, D + 6, -PLANK, TOPZ, 1.6, 0.8);
  block(0, 0, L, D + 6, -PLANK, 0, 1.6, 0.8);

  /* надпись лежит на фасаде коробки (плоскость y = D + выдвижение) и идёт
     снизу вверх, как на корешке: ось строки это +z, низ букв смотрит в +x */
  var O3 = P(0, 0, 0), EZ = P(0, 0, 1), EX = P(1, 0, 0);
  var MA = EZ[0] - O3[0], MB = EZ[1] - O3[1], MC = EX[0] - O3[0], MD = EX[1] - O3[1];
  function spineMatrix(cx, y) {
    var o = P(cx, y, TXT0);
    return "matrix(" + [MA, MB, MC, MD, o[0], o[1]].map(function (n) { return n.toFixed(3); }).join(" ") + ")";
  }
  var boxes = spans.map(function (s, i) {
    var el = solid(g);
    var label = mk("text", {
      "class": "hl-spine", "font-size": FS, "dominant-baseline": "central",
      style: "fill:var(--ink,var(--hl-edge));stroke:none;font-family:'PT Mono',ui-monospace,monospace;font-weight:400;letter-spacing:.02em"
    }, el.g);
    label.textContent = TOPICS[i][0];
    return { x0: s[0], x1: s[1], el: el, label: label, drawn: NaN };
  });
  block(L, 0, L + POST, D + 6, -PLANK, TOPZ, 1.6, 0.8);

  function draw(bx, off) {
    off = Math.round(off * 100) / 100;
    if (off === bx.drawn) return;
    bx.drawn = off;
    var rr = rings(bx.x0, off, bx.x1, D + off, R, B);
    put(bx.el, prism(P, front, rr[0], rr[1], 0, H));
    bx.label.setAttribute("transform", spineMatrix((bx.x0 + bx.x1) / 2, D + off));
  }

  function smooth(t) { t = Math.max(0, Math.min(1, t)); return t * t * (3 - 2 * t); }

  /* поза полки при доле прокрутки p от 0 до 1 */
  var shown = -2;
  function pose(p) {
    var s = smooth(p / 0.12);
    var c = -WAVE + p * (N - 1 + 2 * WAVE);
    var best = -1, top = 0.35;
    boxes.forEach(function (bx, i) {
      var bell = smooth(1 - Math.abs(i - c) / WAVE) * s;
      if (bell > top) { top = bell; best = i; }
      draw(bx, REST[i] * (1 - s) + PULL * bell);
    });
    var act = best >= 0 ? best : (s < 0.5 ? STAR : -1);
    if (act !== shown) {
      boxes.forEach(function (bx, i) { bx.el.sil.classList.toggle("hi", i === act); });
      if (readEl) readEl.textContent = best >= 0 ? TOPICS[best][0] + " · " + TOPICS[best][2] + " " + TOPICS[best][3] : "";
      shown = act;
    }
  }

  var still = null; // движение от прокрутки всегда (слово Риса 06.10.2026)
  var sp = spring(0, { k: 90, c: 19, eps: 0.0005 });

  /* доля прокрутки: 0, пока полка целиком видна в первом экране, 1, когда
     три четверти полки ушли за верх окна */
  function target() {
    if (still && still.matches) return 0;
    var r = stage.getBoundingClientRect();
    var top = r.top + window.scrollY, h = r.height, vh = window.innerHeight;
    var start = 0, end = Math.max(400, top + h * 1.2);
    return Math.max(0, Math.min(1, (window.scrollY - start) / (end - start)));
  }

  var loop = register(stage, function (dt) {
    var moving = stepS(sp, dt);
    pose(still && still.matches ? 0 : sp.x);
    return moving;
  });

  function onScroll() { sp.t = target(); loop.wake(); }
  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", onScroll);
  if (still && still.addEventListener) still.addEventListener("change", function () { sp.x = sp.t = target(); sp.v = 0; loop.wake(); });
  sp.x = sp.t = target();
  pose(still && still.matches ? 0 : sp.x);
})();
