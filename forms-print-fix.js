/**
 * KB Forms Print Fix
 * Mirrors form-input values into static print-only DOM nodes so that
 * "Print" and "Save as PDF" preserve the user-entered values.
 *
 * Problem: browsers do not reliably render the typed value of <input>,
 * <textarea>, or <select> elements when printing. Multi-line <textarea>
 * values are clipped to the rendered single-row height. Radio / select
 * selection state is generally lost.
 *
 * Solution: on `beforeprint`, walk every form-input element in the page,
 * create a sibling element with the value rendered as static text, and
 * make the original invisible in print. On `afterprint`, remove all
 * mirror nodes so the editable form is restored exactly as it was.
 *
 * CSP-safe: no inline event handlers, no innerHTML for user-controlled
 * content (textContent only), pure addEventListener.
 *
 * Applies to any KB page that includes this script. No markup change
 * required on the form itself beyond the <script src="..."></script>.
 */

(function () {
  'use strict';

  var MIRROR_CLASS = 'frm-print-mirror';
  var MIRROR_EMPTY_CLASS = 'frm-print-mirror-empty';
  var HIDE_FOR_PRINT_CLASS = 'frm-print-hide';
  var LABEL_CHECKED_CLASS = 'frm-print-radio-checked';
  var LABEL_UNCHECKED_CLASS = 'frm-print-radio-unchecked';
  var INJECTED_STYLE_ID = 'frm-print-fix-style';

  // Inject the print stylesheet exactly once.
  function ensureStyle() {
    if (document.getElementById(INJECTED_STYLE_ID)) return;
    var style = document.createElement('style');
    style.id = INJECTED_STYLE_ID;
    style.textContent = [
      '/* KB Forms Print Fix — screen styles */',
      '.' + MIRROR_CLASS + ' { display:none; }',
      '@media print {',
      '  /* Hide originals; show mirrors */',
      '  .' + HIDE_FOR_PRINT_CLASS + ' { display:none !important; }',
      '  .' + MIRROR_CLASS + ' {',
      '    display:block;',
      '    font-family:inherit;',
      '    font-size:11pt;',
      '    color:#000;',
      '    line-height:1.4;',
      '    white-space:pre-wrap;',
      '    word-break:break-word;',
      '    min-height:1.2em;',
      '    padding:2pt 4pt;',
      '    border-bottom:0.5pt solid #999;',
      '    background:transparent;',
      '  }',
      '  .' + MIRROR_CLASS + '.frm-print-mirror-inline { display:inline; border-bottom:0.5pt solid #999; padding:0 2pt; }',
      '  .' + MIRROR_EMPTY_CLASS + ' { color:#bbb; }',
      '  /* Radio: change visual style of label */',
      '  .' + LABEL_CHECKED_CLASS + ' { font-weight:700; }',
      '  .' + LABEL_CHECKED_CLASS + '::before { content:"\\2611  "; font-weight:700; }',  /* ☑ */
      '  .' + LABEL_UNCHECKED_CLASS + '::before { content:"\\2610  "; }',  /* ☐ */
      '  .' + LABEL_CHECKED_CLASS + ' input[type="radio"], .' + LABEL_UNCHECKED_CLASS + ' input[type="radio"] { display:none; }',
      '  /* Checkboxes (less common): same treatment */',
      '  input[type="checkbox"] { -webkit-appearance:none; appearance:none; width:10pt; height:10pt; border:0.5pt solid #333; display:inline-block; vertical-align:middle; }',
      '  input[type="checkbox"]:checked::after { content:"\\2713"; display:block; text-align:center; font-size:9pt; line-height:9pt; }',
      '  /* Tighter padding on form table cells so mirrors fit well */',
      '  .frm-table td .' + MIRROR_CLASS + ' { font-size:10pt; min-height:1em; }',
      '}',
    ].join('\n');
    document.head.appendChild(style);
  }

  // Determine whether an element should be inlined (e.g. single-line input
  // in a one-cell label/value row) or block (textarea in a multi-cell row).
  function shouldInline(el) {
    if (el.tagName === 'TEXTAREA') return false;
    if (el.tagName === 'SELECT') return false;
    // type="text", "date", etc — inline if inside a details-table row.
    var parent = el.parentElement;
    while (parent && parent !== document.body) {
      if (parent.classList && (
        parent.classList.contains('details-table') ||
        parent.classList.contains('field-input-wrap') ||
        parent.classList.contains('decl-box')
      )) return true;
      parent = parent.parentElement;
    }
    return false;
  }

  // Build a mirror node for an input/textarea/select.
  function buildMirror(el) {
    var span = document.createElement('span');
    span.className = MIRROR_CLASS;
    if (shouldInline(el)) span.classList.add('frm-print-mirror-inline');

    var val = '';
    if (el.tagName === 'SELECT') {
      var opt = el.options[el.selectedIndex];
      if (opt && opt.value !== '' && opt.text) val = opt.text;
    } else {
      val = el.value || '';
    }

    if (val === '' || val == null) {
      span.classList.add(MIRROR_EMPTY_CLASS);
      span.textContent = '\u00a0'; // non-breaking space — keeps the underline visible
    } else {
      span.textContent = val;
    }
    return span;
  }

  var alreadyApplied = false;

  function applyMirrors() {
    if (alreadyApplied) return;
    alreadyApplied = true;
    ensureStyle();

    // Standard inputs / textareas / selects: mirror with sibling node.
    var nodes = document.querySelectorAll(
      'textarea, input[type="text"], input[type="date"], input[type="email"], ' +
      'input[type="tel"], input[type="number"], input[type="url"], select'
    );
    for (var i = 0; i < nodes.length; i++) {
      var el = nodes[i];
      if (!el.parentNode) continue;
      var mirror = buildMirror(el);
      el.classList.add(HIDE_FOR_PRINT_CLASS);
      el.parentNode.insertBefore(mirror, el.nextSibling);
    }

    // Radios: mark the containing label as checked/unchecked.
    var radios = document.querySelectorAll('input[type="radio"]');
    for (var r = 0; r < radios.length; r++) {
      var radio = radios[r];
      var label = radio.closest('label');
      if (!label) continue;
      if (radio.checked) label.classList.add(LABEL_CHECKED_CLASS);
      else label.classList.add(LABEL_UNCHECKED_CLASS);
    }
  }

  function removeMirrors() {
    if (!alreadyApplied) return;
    alreadyApplied = false;
    var mirrors = document.querySelectorAll('.' + MIRROR_CLASS);
    for (var i = 0; i < mirrors.length; i++) {
      if (mirrors[i].parentNode) mirrors[i].parentNode.removeChild(mirrors[i]);
    }
    var hidden = document.querySelectorAll('.' + HIDE_FOR_PRINT_CLASS);
    for (var j = 0; j < hidden.length; j++) {
      hidden[j].classList.remove(HIDE_FOR_PRINT_CLASS);
    }
    var checked = document.querySelectorAll('.' + LABEL_CHECKED_CLASS);
    for (var c = 0; c < checked.length; c++) {
      checked[c].classList.remove(LABEL_CHECKED_CLASS);
    }
    var unchecked = document.querySelectorAll('.' + LABEL_UNCHECKED_CLASS);
    for (var u = 0; u < unchecked.length; u++) {
      unchecked[u].classList.remove(LABEL_UNCHECKED_CLASS);
    }
  }

  // Inject style early so screen rendering is correct from first paint.
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', ensureStyle);
  } else {
    ensureStyle();
  }

  // Browsers: `beforeprint` / `afterprint` events are the cleanest hook,
  // supported in modern Chrome/Edge/Firefox/Safari for both print and
  // "Save as PDF" flows (which use the print pipeline).
  window.addEventListener('beforeprint', applyMirrors);
  window.addEventListener('afterprint', removeMirrors);

  // Safari has historically had quirks with these events; matchMedia
  // print listener gives a second hook for reliability.
  if (window.matchMedia) {
    var mql = window.matchMedia('print');
    var mqlHandler = function (e) {
      if (e.matches) applyMirrors();
      else removeMirrors();
    };
    if (mql.addEventListener) mql.addEventListener('change', mqlHandler);
    else if (mql.addListener) mql.addListener(mqlHandler);
  }
})();
