/**
 * KB Download Utilities
 * Print and Markdown download for knowledge base document pages.
 * CSP safe — no inline onclick, no innerHTML for buttons, pure addEventListener.
 */

(function () {
  'use strict';

  // ── Helpers ────────────────────────────────────────────────────────────

  function getMetaValue(label) {
    var bars = document.querySelectorAll('.meta-bar, .sop-meta-bar, .wi-meta-bar');
    for (var i = 0; i < bars.length; i++) {
      var items = bars[i].querySelectorAll('.meta-item, .sop-meta-item, .wi-meta-item');
      for (var j = 0; j < items.length; j++) {
        var text = items[j].textContent || '';
        if (text.toLowerCase().indexOf(label.toLowerCase()) !== -1) {
          var strong = items[j].querySelector('strong');
          if (strong) return text.replace(strong.textContent, '').trim();
        }
      }
    }
    return '';
  }

  function getDocId() {
    var bc = document.querySelectorAll('.breadcrumb span');
    if (bc.length) return bc[bc.length - 1].textContent.trim();
    var title = document.title || '';
    var match = title.match(/^([A-Z0-9][A-Z0-9-]+)\s*[:]/);
    if (match) return match[1];
    return 'KB-DOC';
  }

  function getDocTitle() {
    var h1 = document.querySelector(
      '.kb-page-hero h1, .grc-page-hero h1, .grc-hero h1, .t1-hero h2, .cc-hero h1'
    );
    if (h1) return h1.textContent.trim().replace(/^[A-Z0-9-]+\s*[:]\s*/, '');
    return document.title.replace(' — Cyber Security Knowledge Base', '').trim();
  }

  function getSection() {
    var bc = document.querySelectorAll('.breadcrumb a');
    if (bc.length >= 2) return bc[1].textContent.trim();
    return '';
  }

  function getStatus() {
    var el = document.querySelector('.sop-badge-approved, .badge-approved, .doc-badge.approved');
    if (el) return el.textContent.trim();
    var el2 = document.querySelector('.sop-badge-draft, .wi-badge-draft, .doc-badge.wip');
    if (el2) return el2.textContent.trim();
    return '';
  }

  // ── Markdown extraction ────────────────────────────────────────────────

  function elemToMd(el) {
    if (!el) return '';
    var tag = el.tagName ? el.tagName.toLowerCase() : '';
    var text = (el.textContent || '').trim();

    if (el.classList) {
      var skipList = [
        'kb-topnav','doc-toolbar','breadcrumb','kb-footer',
        'sop-nav','wi-nav','pol-nav','frm-nav','grc-nav',
        'asm-nav','t1-nav','live-dot','kb-page-hero-meta',
        'grc-page-hero-pills','grc-hero-pills','grc-hero-ey'
      ];
      for (var s = 0; s < skipList.length; s++) {
        if (el.classList.contains(skipList[s])) return '';
      }
    }

    if (el.classList && (
      el.classList.contains('kb-page-hero') || el.classList.contains('grc-page-hero') ||
      el.classList.contains('grc-hero') || el.classList.contains('t1-hero') ||
      el.classList.contains('cc-hero') || el.classList.contains('asm-page-hero')
    )) {
      var heroH = el.querySelector('h1, h2');
      var heroP = el.querySelector('p');
      var out = '';
      if (heroH) out += '# ' + heroH.textContent.trim() + '\n\n';
      if (heroP) out += '> ' + heroP.textContent.trim() + '\n\n';
      return out;
    }

    if (el.classList && (
      el.classList.contains('meta-bar') || el.classList.contains('sop-meta-bar') ||
      el.classList.contains('wi-meta-bar')
    )) {
      var items = el.querySelectorAll('.meta-item, .sop-meta-item, .wi-meta-item');
      var metaOut = '';
      items.forEach(function(item) {
        var strong = item.querySelector('strong');
        if (strong) {
          var lbl = strong.textContent.trim().replace(':', '');
          var val = item.textContent.replace(strong.textContent, '').trim();
          if (val && lbl) metaOut += '**' + lbl + ':** ' + val + '  \n';
        }
      });
      return metaOut ? metaOut + '\n' : '';
    }

    if (el.classList && (
      el.classList.contains('sop-section-num') || el.classList.contains('wi-section-label') ||
      el.classList.contains('pol-section-num') || el.classList.contains('grc-section-num') ||
      el.classList.contains('cc-section-eyebrow') || el.classList.contains('wi-section-num')
    )) return '';

    if (el.classList && (
      el.classList.contains('sop-section-title') || el.classList.contains('pol-section-title') ||
      el.classList.contains('grc-section-title') || el.classList.contains('cc-section-title') ||
      el.classList.contains('wi-section-title')
    )) return '\n## ' + text + '\n\n';

    if (el.classList && el.classList.contains('frm-section-header')) {
      var h3 = el.querySelector('h3');
      return '\n## ' + (h3 ? h3.textContent.trim() : text) + '\n\n';
    }

    if (tag === 'h1') return '\n# '   + text + '\n\n';
    if (tag === 'h2') return '\n## '  + text + '\n\n';
    if (tag === 'h3') return '\n## '  + text + '\n\n';
    if (tag === 'h4') return '\n### ' + text + '\n\n';
    if (tag === 'p')  return text + '\n\n';

    if (tag === 'table') {
      var rows = el.querySelectorAll('tr');
      if (!rows.length) return '';
      var tOut = '';
      var hDone = false;
      rows.forEach(function(row) {
        var cells = row.querySelectorAll('th, td');
        if (!cells.length) return;
        var line = '| ';
        cells.forEach(function(c) { line += c.textContent.trim().replace(/\n+/g, ' ') + ' | '; });
        tOut += line + '\n';
        if (!hDone && row.querySelector('th')) {
          var sep = '| ';
          cells.forEach(function() { sep += '--- | '; });
          tOut += sep + '\n';
          hDone = true;
        }
      });
      return tOut + '\n';
    }

    if (el.classList && (
      el.classList.contains('sop-step') || el.classList.contains('proc-step') ||
      el.classList.contains('pm-step') || el.classList.contains('h-step') ||
      el.classList.contains('vm-phase') || el.classList.contains('process-step')
    )) {
      var sNum   = el.querySelector('.sop-step-num, .proc-step-num, .pm-step-num, .h-step-num, .vm-phase-num, .step-num');
      var sTitle = el.querySelector('.sop-step-title, .proc-step-title, .pm-step-title, .vm-phase-title, .step-body h4');
      var sDesc  = el.querySelector('.sop-step-desc, .proc-step-desc, .pm-step-desc, .vm-phase-steps, .step-body p');
      var num    = sNum   ? sNum.textContent.trim()   : '';
      var stitle = sTitle ? sTitle.textContent.trim() : '';
      var sdesc  = sDesc  ? sDesc.textContent.trim()  : '';
      return (num ? num + '. ' : '- ') +
        (stitle ? '**' + stitle + '**' : '') +
        (sdesc  ? ' — ' + sdesc : '') + '\n';
    }

    if (el.classList && (
      el.classList.contains('h-check') || el.classList.contains('ev-item') ||
      el.classList.contains('esc-item') || el.classList.contains('evidence-item') ||
      el.classList.contains('gap-item') || el.classList.contains('pitfall-item') ||
      el.classList.contains('q-item')   || el.classList.contains('comp-item') ||
      el.classList.contains('h-rollback-item') || el.classList.contains('h-tip') ||
      el.classList.contains('gov-item')
    )) return '- ' + text + '\n';

    if (el.classList && (
      el.classList.contains('sop-principle') || el.classList.contains('outcome-card') ||
      el.classList.contains('review-card')   || el.classList.contains('threshold-card') ||
      el.classList.contains('sla-card')      || el.classList.contains('supplier-card') ||
      el.classList.contains('focus-card')    || el.classList.contains('tier-card') ||
      el.classList.contains('acct-card')     || el.classList.contains('comp-card') ||
      el.classList.contains('example-card')  || el.classList.contains('principle-card')
    )) {
      var cH = el.querySelector('h4, h3');
      var cP = el.querySelector('p');
      var cOut = '';
      if (cH) cOut += '**' + cH.textContent.trim() + '**';
      if (cP) cOut += ' — ' + cP.textContent.trim();
      return cOut ? '- ' + cOut + '\n' : '';
    }

    if (el.classList && (
      el.classList.contains('callout-warn') || el.classList.contains('callout-info') ||
      el.classList.contains('sop-callout-warn') || el.classList.contains('sop-callout-info') ||
      el.classList.contains('instr-box')    || el.classList.contains('redirect-box') ||
      el.classList.contains('req-banner')   || el.classList.contains('grc-important') ||
      el.classList.contains('how-box')      || el.classList.contains('decl-box')
    )) {
      var cP2 = el.querySelector('p');
      return cP2 ? '> ' + cP2.textContent.trim() + '\n\n' : '';
    }

    if (el.classList && el.classList.contains('rel-link')) {
      var href = el.getAttribute('href') || '';
      return '- [' + text + '](' + href + ')\n';
    }

    if (tag === 'li') return '- ' + text + '\n';
    if (tag === 'ul' || tag === 'ol') {
      var lOut = '';
      var lis = el.querySelectorAll(':scope > li');
      lis.forEach(function(li) { lOut += '- ' + li.textContent.trim() + '\n'; });
      return lOut + '\n';
    }

    if (el.children && el.children.length) {
      var childOut = '';
      for (var k = 0; k < el.children.length; k++) {
        childOut += elemToMd(el.children[k]);
      }
      return childOut;
    }

    return '';
  }

  function buildMarkdown() {
    var docId   = getDocId();
    var title   = getDocTitle();
    var section = getSection();
    var status  = getStatus();
    var author  = getMetaValue('Author') || 'Paulo Ferreira';
    var version = getMetaValue('Version') || 'v1.0';
    var date    = new Date().toLocaleDateString('en-GB', {
      day: '2-digit', month: 'long', year: 'numeric'
    });
    var url = window.location.href.split('?')[0].split('#')[0];

    var header =
      '# ' + docId + ': ' + title + '\n\n' +
      '| Field | Value |\n' +
      '|-------|-------|\n' +
      '| **Document ID** | ' + docId + ' |\n' +
      '| **Section** | ' + section + ' |\n' +
      (status  ? '| **Status** | '  + status  + ' |\n' : '') +
      (author  ? '| **Author** | '  + author  + ' |\n' : '') +
      (version ? '| **Version** | ' + version + ' |\n' : '') +
      '| **Downloaded** | ' + date + ' |\n' +
      '| **Source** | ' + url + ' |\n' +
      '\n---\n\n';

    var wrapper = document.querySelector('.page-wrapper');
    if (!wrapper) return header + '*Content could not be extracted.*';

    var contentMd = '';
    for (var i = 0; i < wrapper.children.length; i++) {
      var child = wrapper.children[i];
      if (child.classList.contains('doc-toolbar')) continue;
      if (child.classList.contains('breadcrumb'))  continue;
      if (child.classList.contains('kb-footer'))   continue;
      if (child.tagName && child.tagName.toLowerCase() === 'nav') continue;
      contentMd += elemToMd(child);
    }

    contentMd = contentMd.replace(/\n{4,}/g, '\n\n\n');

    return header + contentMd.trim() +
      '\n\n---\n*Downloaded from the Cyber Security Knowledge Base — soc-it-kb.github.io*\n';
  }

  // ── Download ───────────────────────────────────────────────────────────

  function doDownloadMd() {
    var md       = buildMarkdown();
    var docId    = getDocId();
    var filename = docId.toLowerCase()
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/-+/g, '-')
      .replace(/^-|-$/g, '') + '.md';

    var blob = new Blob([md], { type: 'text/markdown;charset=utf-8' });
    var blobUrl = URL.createObjectURL(blob);
    var a = document.createElement('a');
    a.href = blobUrl;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(blobUrl);
  }

  // ── Toolbar injection ──────────────────────────────────────────────────

  function injectToolbar() {
    var wrapper = document.querySelector('.page-wrapper');
    if (!wrapper) return;

    // Prevent double injection
    if (wrapper.querySelector('.doc-toolbar')) return;

    var hasMeta = wrapper.querySelector('.meta-bar, .sop-meta-bar, .wi-meta-bar');
    var hasHero = wrapper.querySelector(
      '.kb-page-hero, .grc-page-hero, .grc-hero, .t1-hero, .cc-hero, .asm-page-hero'
    );
    if (!hasMeta && !hasHero) return;

    var path = window.location.pathname;
    var skipList = [
      'grc-register-', 'grc.html', 'grc-governance', 'grc-risk', 'grc-compliance',
      'asm.html', 'asm-security', 'asm-vulnerability', 'asm-patch', 'asm-threat',
      'index.html', 'playbooks.html', 'runbooks.html', 'sops.html',
      'work-instructions.html', 'governance.html', 'search.html', 'tools-references'
    ];
    for (var i = 0; i < skipList.length; i++) {
      if (path.indexOf(skipList[i]) !== -1) return;
    }

    // Build toolbar — DOM methods only, no innerHTML, no onclick (CSP safe)
    var toolbar = document.createElement('div');
    toolbar.className = 'doc-toolbar';

    var printBtn = document.createElement('button');
    printBtn.className = 'doc-toolbar-btn btn-print';
    printBtn.title = 'Print or save as PDF';
    printBtn.textContent = 'Print / Save as PDF';
    printBtn.addEventListener('click', function () { window.print(); });

    var mdBtn = document.createElement('button');
    mdBtn.className = 'doc-toolbar-btn btn-md';
    mdBtn.title = 'Download as Markdown';
    mdBtn.textContent = 'Download as Markdown';
    mdBtn.addEventListener('click', doDownloadMd);

    toolbar.appendChild(printBtn);
    toolbar.appendChild(mdBtn);

    var bc = wrapper.querySelector('.breadcrumb');
    if (bc && bc.nextSibling) {
      wrapper.insertBefore(toolbar, bc.nextSibling);
    } else {
      wrapper.insertBefore(toolbar, wrapper.firstChild);
    }
  }

  // Run immediately if DOM ready, otherwise wait
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', injectToolbar);
  } else {
    injectToolbar();
  }

})();
