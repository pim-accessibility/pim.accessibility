/* PIM Accessibility — theme selector + annotations control. No dependencies. */
(function () {
  'use strict';
  var root = document.documentElement;
  var store = {
    get: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) { /* storage blocked: keep in memory */ } }
  };

  /* ---------- Theme: Light / Dark radio group (fieldset + legend) ---------- */
  var radios = document.querySelectorAll('input[name="theme"]');
  function applyTheme(t) {
    root.setAttribute('data-theme', t);
    for (var i = 0; i < radios.length; i++) radios[i].checked = radios[i].value === t;
  }
  applyTheme(root.getAttribute('data-theme') || 'light');
  for (var i = 0; i < radios.length; i++) {
    radios[i].addEventListener('change', function (e) {
      if (!e.target.checked) return;
      applyTheme(e.target.value);
      store.set('pim-theme', e.target.value);
    });
  }
  // Until the person chooses, follow the system setting live.
  var mq = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)');
  if (mq && mq.addEventListener) {
    mq.addEventListener('change', function (e) {
      if (!store.get('pim-theme')) applyTheme(e.matches ? 'dark' : 'light');
    });
  }

  /* ---------- Annotations: one button whose label says the action ----------
     The visible label changes (Hide ↔ Show), so aria-pressed is NOT used
     (APG button pattern: a toggle's label must not change with its state). */
  var btn = document.getElementById('anno-toggle');
  var status = document.getElementById('anno-status');
  if (!btn || !status) return;
  var verb = btn.querySelector('.anno-verb');
  var t = {
    on: status.getAttribute('data-on'),
    off: status.getAttribute('data-off'),
    hide: btn.getAttribute('data-hide'),
    show: btn.getAttribute('data-show')
  };
  function applyAnno(on, announce) {
    root.classList.toggle('anno-on', on);
    verb.textContent = on ? t.hide : t.show;
    if (announce) status.textContent = on ? t.on : t.off;
  }
  applyAnno(root.classList.contains('anno-on'), false);
  status.textContent = root.classList.contains('anno-on') ? t.on : t.off;
  btn.addEventListener('click', function () {
    var on = !root.classList.contains('anno-on');
    applyAnno(on, true);
    store.set('pim-annotations', on ? 'on' : 'off');
  });
})();
