/**
 * KB Language Switcher
 * Injects a PT | FR language switcher into the nav.
 * Opens the current page via Google Translate — no external scripts,
 * no inline handlers, fully CSP safe.
 */

(function () {
  'use strict';

  var BASE_URL = 'https://translate.google.com/translate';
  var SITE_ORIGIN = 'https://soc-it-kb.github.io';

  var LANGS = [
    { code: 'pt', label: 'PT', title: 'Traduzir para Português' },
    { code: 'fr', label: 'FR', title: 'Traduire en Français'   },
  ];

  function getTranslateUrl(targetLang) {
    var pageUrl = window.location.href;
    // If already on a translated page, extract the original URL
    if (pageUrl.indexOf('translate.google') !== -1) {
      var match = pageUrl.match(/[?&]u=([^&]+)/);
      if (match) pageUrl = decodeURIComponent(match[1]);
    }
    return BASE_URL +
      '?sl=en' +
      '&tl=' + targetLang +
      '&hl=' + targetLang +
      '&u=' + encodeURIComponent(pageUrl) +
      '&anno=2';
  }

  function isTranslatedPage() {
    return window.location.href.indexOf('translate.google') !== -1;
  }

  function injectSwitcher() {
    var nav = document.querySelector('.kb-topnav');
    if (!nav) return;
    if (nav.querySelector('.kb-topnav-lang')) return;

    var lang = document.createElement('div');
    lang.className = 'kb-topnav-lang';

    // EN link — goes back to original if on translated page
    var enLink = document.createElement('a');
    enLink.title = 'View in English';
    enLink.textContent = 'EN';
    if (isTranslatedPage()) {
      // Extract original URL from translate.google parameters
      var match = window.location.href.match(/[?&]u=([^&]+)/);
      enLink.href = match ? decodeURIComponent(match[1]) : SITE_ORIGIN;
    } else {
      enLink.href = window.location.href;
      enLink.className = 'lang-active';
    }
    lang.appendChild(enLink);

    // Separators and PT/FR links
    LANGS.forEach(function (l, i) {
      var sep = document.createElement('span');
      sep.className = 'lang-sep';
      sep.textContent = '|';
      lang.appendChild(sep);

      var a = document.createElement('a');
      a.href = getTranslateUrl(l.code);
      a.title = l.title;
      a.textContent = l.label;
      a.target = '_blank';
      a.rel = 'noopener noreferrer';
      lang.appendChild(a);
    });

    // Insert before search or at end of nav
    var search = nav.querySelector('.kb-topnav-search');
    if (search) {
      nav.insertBefore(lang, search);
    } else {
      nav.appendChild(lang);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', injectSwitcher);
  } else {
    injectSwitcher();
  }

})();
