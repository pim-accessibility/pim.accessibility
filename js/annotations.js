/* PIM Accessibility — accessibility annotations, drawn like the Figma layer
   "Anotações (aria-hidden) — v2.2 B" (node 60:1290) and the mobile frame 57:1576.

   - Everything is drawn in ONE layer with aria-hidden="true": screen readers get
     the real semantics of the page, never the labels (same as in Figma).
   - Desktop (≥ 80em / 1280px): labels in the page margins, dashed 2px lines (3/4)
     ending in a 12px dot, 2.5px brackets for landmarks — geometry measured in Figma.
   - Below 80em: labels in rows above the element, no lines (Figma mobile frame).
   - The spec (which element, which label) lives in <script type="application/json"
     id="anno-spec"> so labels can be translated per page. */
(function () {
  'use strict';
  var specEl = document.getElementById('anno-spec');
  if (!specEl) return;
  var spec;
  try { spec = JSON.parse(specEl.textContent); } catch (e) { return; }
  var root = document.documentElement;
  var DESKTOP = window.matchMedia('(min-width: 80em)');

  /* Figma line colours per annotation type */
  var LINE = { link: '#6FA0F0', landmark: '#E07AB4', heading: '#5FC8C8', image: '#7BD69B',
               list: '#8F96F0', button: '#A8D46A', note: '#C49BEA' };

  function chip(label, type) {
    var c = document.createElement('span');
    c.className = 'a11y-chip';
    c.setAttribute('data-t', type);
    var i = document.createElement('span');
    i.className = 'a11y-chip-i';
    c.appendChild(i);
    c.appendChild(document.createTextNode(label));
    return c;
  }

  /* ---------------- Mobile / tablet: rows of labels above elements ---------------- */
  function buildInline() {
    (spec.mobile || []).forEach(function (row) {
      var el = document.querySelector(row.sel);
      if (!el) return;
      var r = document.createElement('div');
      r.className = 'a11y-inline' + (row.cls ? ' ' + row.cls : '');
      r.setAttribute('aria-hidden', 'true');
      row.chips.forEach(function (c) { r.appendChild(chip(c[0], c[1])); });
      if (row.where === 'prepend') el.insertBefore(r, el.firstChild);
      else el.parentNode.insertBefore(r, el);
    });
  }

  /* ---------------- Desktop: overlay layer ---------------- */
  var layer = document.createElement('div');
  layer.className = 'a11y-layer';
  layer.setAttribute('aria-hidden', 'true');

  function box(x, y, w, h, cls, color) {
    var d = document.createElement('span');
    d.className = cls;
    d.style.left = x + 'px'; d.style.top = y + 'px';
    if (w != null) d.style.width = w + 'px';
    if (h != null) d.style.height = h + 'px';
    if (color) d.style.setProperty('--c', color);
    layer.appendChild(d);
    return d;
  }
  function hline(x0, x1, y, c) { var a = Math.min(x0, x1); box(a, y - 1, Math.abs(x1 - x0), 2, 'a11y-dash-h', c); }
  function vline(x, y0, y1, c) { var a = Math.min(y0, y1); box(x - 1, a, 2, Math.abs(y1 - y0), 'a11y-dash-v', c); }
  function solidH(x0, x1, y, c) { box(Math.min(x0, x1), y - 1.25, Math.abs(x1 - x0), 2.5, 'a11y-solid', c); }
  function solidV(x, y0, y1, c) { box(x - 1.25, Math.min(y0, y1), 2.5, Math.abs(y1 - y0), 'a11y-solid', c); }
  function dot(x, y, c) { box(x - 7, y - 7, 14, 14, 'a11y-dot', c); }
  function place(label, type, x, y) {
    var c = chip(label, type);
    c.style.left = x + 'px'; c.style.top = y + 'px';
    layer.appendChild(c);
    return c;
  }

  function rect(el) {
    var r = el.getBoundingClientRect();
    var sx = window.scrollX, sy = window.scrollY;
    return { l: r.left + sx, r: r.right + sx, t: r.top + sy, b: r.bottom + sy, w: r.width, h: r.height,
             cx: r.left + sx + r.width / 2, cy: r.top + sy + r.height / 2 };
  }
  /* Vertical centre of an element's first line of text (Figma anchors headings there) */
  function firstLineY(el) {
    var r = rect(el);
    var lh = parseFloat(getComputedStyle(el).lineHeight);
    if (isNaN(lh)) lh = parseFloat(getComputedStyle(el).fontSize) * 1.2;
    return r.t + Math.min(lh, r.h) / 2;
  }

  function drawDesktop() {
    layer.textContent = '';
    var header = document.querySelector('.site-header');
    if (!header) return;
    var hs = getComputedStyle(header), hr = rect(header);
    var cL = hr.l + parseFloat(hs.paddingLeft);          // content left edge  (Figma x = 192)
    var cR = hr.r - parseFloat(hs.paddingRight);         // content right edge (Figma x = 1248)
    var vw = document.documentElement.clientWidth;

    (spec.desktop || []).forEach(function (a) {
      var el = document.querySelector(a.sel);
      if (!el || !el.getClientRects().length) return;
      var r = rect(el), c = LINE[a.t] || LINE.note, ch, w, y, dx, x;
      var anchor = a.ysel ? (el.querySelector(a.ysel) || el) : el;
      var ay = a.y === 'line' ? firstLineY(anchor) : rect(anchor).cy;

      switch (a.m) {
        case 'left': {          // label in the left margin, ends 16px before the content edge
          dx = a.dx != null ? a.dx : -10;
          x = r.l + dx;
          ch = place(a.l, a.t, 0, ay - 14);
          w = ch.offsetWidth;
          ch.style.left = Math.max(2, cL - 16 - w) + 'px';
          hline(cL - 16, x, ay, c); dot(x, ay, c);
          break;
        }
        case 'right': {         // label in the right margin, starts 28px after the content edge
          x = r.r + (a.dx != null ? a.dx : -6);
          ch = place(a.l, a.t, 0, ay - 14);
          w = ch.offsetWidth;
          ch.style.left = Math.min(cR + 28, vw - w - 2) + 'px';
          hline(x, cR + 28, ay, c); dot(x, ay, c);
          break;
        }
        case 'top': {           // label above the element, dashed line down to a dot on its top edge
          var len = a.len || 24, dy = r.t + 6, cx = a.xsel ? rect(el.querySelector(a.xsel) || el).cx : r.cx;
          ch = place(a.l, a.t, 0, dy - len - 28);
          w = ch.offsetWidth;
          ch.style.left = (cx - w / 2) + 'px';
          vline(cx, dy - len, dy, c); dot(cx, dy, c);
          break;
        }
        case 'near-left': {     // label inside the content, line of fixed length to the element
          x = r.l - 6;
          ch = place(a.l, a.t, 0, ay - 14);
          w = ch.offsetWidth;
          ch.style.left = (x - (a.len || 65) - w) + 'px';
          hline(x - (a.len || 65), x, ay, c); dot(x, ay, c);
          break;
        }
        case 'dot': {           // a dot only (Figma: decorative cursor)
          dot(r.l + (a.fx || 0), r.t + (a.fy || 0), c);
          break;
        }
        case 'hb-top': {        // horizontal bracket above (Figma <nav>)
          y = r.t - 8;
          solidH(r.l, r.r, y, c); solidV(r.l, y, y + 6, c); solidV(r.r, y, y + 6, c);
          ch = place(a.l, a.t, 0, y - 48 - 28);
          w = ch.offsetWidth;
          ch.style.left = (r.cx - w / 2) + 'px';
          vline(r.cx, y - 48, y, c);
          break;
        }
        case 'hb-bottom': {     // horizontal bracket below (Figma <ul>)
          y = r.b + 10;
          solidH(r.l, r.r, y, c); solidV(r.l, y - 6, y, c); solidV(r.r, y - 6, y, c);
          ch = place(a.l, a.t, 0, y + 14);
          w = ch.offsetWidth;
          ch.style.left = (r.cx - w / 2) + 'px';
          vline(r.cx, y, y + 14, c);
          break;
        }
        case 'bracket': {       // landmark bracket in the right margin (x = content + 4 … + 14)
          var top = a.tsel ? rect(document.querySelector(a.tsel)).t + (a.toff || 0) : r.t + (a.it || 6);
          var bot = r.b - (a.ib != null ? a.ib : 6);
          var stub = a.ssel ? firstLineY(document.querySelector(a.ssel))
                   : (a.stub != null ? top + a.stub : (top + bot) / 2);
          var x0 = cR + 4, x1 = cR + 14;
          solidH(x0, x1, top, c); solidH(x0, x1, bot, c); solidV(x1, top, bot, c);
          solidH(x1, cR + 28, stub, c);
          ch = place(a.l, a.t, 0, stub - 14);
          w = ch.offsetWidth;
          ch.style.left = Math.min(cR + 28, vw - w - 2) + 'px';
          break;
        }
      }
    });
    layer.style.height = document.documentElement.scrollHeight + 'px';
  }

  var raf = 0;
  function update() {
    cancelAnimationFrame(raf);
    raf = requestAnimationFrame(function () {
      if (root.classList.contains('anno-on') && DESKTOP.matches) {
        if (!layer.parentNode) document.body.appendChild(layer);
        drawDesktop();
      } else if (layer.parentNode) {
        layer.parentNode.removeChild(layer);
      }
    });
  }

  buildInline();
  update();
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(update);
  window.addEventListener('load', update);
  window.addEventListener('resize', update);
  if (DESKTOP.addEventListener) DESKTOP.addEventListener('change', update);
  if (window.ResizeObserver) new ResizeObserver(update).observe(document.body);
  /* site.js toggles .anno-on on <html> */
  new MutationObserver(update).observe(root, { attributes: true, attributeFilter: ['class'] });
})();
