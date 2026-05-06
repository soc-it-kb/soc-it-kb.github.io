/**
 * KB Download Utilities
 * Handles print and markdown download for knowledge base document pages.
 * Loaded on document pages via <script src="download-utils.js"></script>
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
          if (strong) {
            var val = text.replace(strong.textContent, '').trim();
            return val || '';
          }
        }
      }
    }
    return '';
  }

  function getDocId() {
    // Try breadcrumb last item
    var bc = document.querySelectorAll('.breadcrumb span');
    if (bc.length) return bc[bc.length - 1].textContent.trim();
    // Try page title prefix
    var title = document.title || '';
    var match = title.match(/^([A-Z0-9-]+(?:-\d+)?(?:-[A-Za-z]+)?(?:-\d+)?)\s*[:—]/);
    if (match) return match[1];
    return 'KB-DOC';
  }

  function getDocTitle() {
    var h1 = document.querySelector('.kb-page-hero h1, .grc-page-hero h1, .grc-hero h1, .t1-hero h2, .cc-hero h1');
    if (h1) {
      var text = h1.textContent.trim();
      // Remove leading ID prefix if present (e.g. "IT-SRV-SOP-Win-01: ")
      text = text.replace(/^[A-Z0-9-]+(?:-\d+)?\s*[:—]\s*/,'');
      return text;
    }
    return document.title.replace(' — Cyber Security Knowledge Base','').trim();
  }

  function getSection() {
    var bc = document.querySelectorAll('.breadcrumb a');
    if (bc.length >= 2) return bc[1].textContent.trim();
    return '';
  }

  function getStatus() {
    var badge = document.querySelector('.sop-badge-approved, .badge-approved, .doc-badge.approved');
    if (badge) return badge.textContent.trim();
    var draftBadge = document.querySelector('.sop-badge-draft, .wi-badge-draft, .doc-badge.wip');
    if (draftBadge) return draftBadge.textContent.trim();
    return '';
  }

  function getAuthor() {
    return getMetaValue('Author') || getMetaValue('author') || 'Paulo Ferreira';
  }

  function getVersion() {
    return getMetaValue('Version') || getMetaValue('version') || 'v1.0';
  }

  // ── Text extraction helpers ────────────────────────────────────────────

  function elemToMd(el, depth) {
    if (!el) return '';
    depth = depth || 0;
    var tag = el.tagName ? el.tagName.toLowerCase() : '';
    var text = (el.textContent || '').trim();

    // Skip hidden/toolbar elements
    if (el.classList) {
      var skip = ['kb-topnav','doc-toolbar','breadcrumb','kb-footer',
                  'sop-nav','wi-nav','pol-nav','frm-nav','grc-nav',
                  'asm-nav','t1-nav','live-dot'];
      for (var i = 0; i < skip.length; i++) {
        if (el.classList.contains(skip[i])) return '';
      }
    }

    // Hero section — extract heading and description
    if (el.classList && (el.classList.contains('kb-page-hero') || el.classList.contains('grc-page-hero') ||
        el.classList.contains('grc-hero') || el.classList.contains('t1-hero') || el.classList.contains('cc-hero'))) {
      var heroH = el.querySelector('h1, h2');
      var heroP = el.querySelector('p');
      var out = '';
      if (heroH) out += '# ' + heroH.textContent.trim() + '\n\n';
      if (heroP)  out += '> ' + heroP.textContent.trim() + '\n\n';
      return out;
    }

    // Meta bar — render as a definition list style
    if (el.classList && (el.classList.contains('meta-bar') || el.classList.contains('sop-meta-bar') || el.classList.contains('wi-meta-bar'))) {
      var items = el.querySelectorAll('.meta-item, .sop-meta-item, .wi-meta-item');
      var metaOut = '';
      items.forEach(function(item) {
        var strong = item.querySelector('strong');
        if (strong) {
          var label = strong.textContent.trim().replace(':','');
          var val = item.textContent.replace(strong.textContent, '').trim();
          if (val && label) metaOut += '**' + label + ':** ' + val + '  \n';
        }
      });
      return metaOut ? metaOut + '\n' : '';
    }

    // Section labels / eyebrow text → H2
    if (el.classList && (el.classList.contains('sop-section-num') || el.classList.contains('wi-section-label') ||
        el.classList.contains('pol-section-num') || el.classList.contains('grc-section-num') ||
        el.classList.contains('cc-section-eyebrow') || el.classList.contains('wi-section-num'))) {
      return ''; // skip — title follows immediately
    }

    // Section titles → H2
    if (el.classList && (el.classList.contains('sop-section-title') || el.classList.contains('pol-section-title') ||
        el.classList.contains('grc-section-title') || el.classList.contains('cc-section-title') ||
        el.classList.contains('wi-section-title'))) {
      return '\n## ' + text + '\n\n';
    }

    // Card headings → H3
    if (tag === 'h4') return '\n### ' + text + '\n\n';
    if (tag === 'h3') return '\n## ' + text + '\n\n';
    if (tag === 'h2') return '\n## ' + text + '\n\n';
    if (tag === 'h1') return '\n# ' + text + '\n\n';

    // Paragraphs
    if (tag === 'p') return text + '\n\n';

    // Bullet/list items
    if (tag === 'li') return '- ' + text + '\n';
    if (tag === 'ul' || tag === 'ol') {
      var listOut = '';
      var listItems = el.querySelectorAll(':scope > li');
      listItems.forEach(function(li) { listOut += '- ' + li.textContent.trim() + '\n'; });
      return listOut + '\n';
    }

    // Tables
    if (tag === 'table') {
      var rows = el.querySelectorAll('tr');
      if (!rows.length) return '';
      var tableOut = '';
      var headerDone = false;
      rows.forEach(function(row, ri) {
        var cells = row.querySelectorAll('th, td');
        if (!cells.length) return;
        var line = '| ';
        cells.forEach(function(c) { line += c.textContent.trim().replace(/\n/g,' ') + ' | '; });
        tableOut += line + '\n';
        if (!headerDone && row.querySelector('th')) {
          var sep = '| ';
          cells.forEach(function() { sep += '--- | '; });
          tableOut += sep + '\n';
          headerDone = true;
        }
      });
      return tableOut + '\n';
    }

    // Step/process items
    if (el.classList && (el.classList.contains('sop-step') || el.classList.contains('proc-step') ||
        el.classList.contains('pm-step') || el.classList.contains('h-step') || el.classList.contains('vm-phase'))) {
      var stepTitle = el.querySelector('.sop-step-title, .proc-step-title, .pm-step-title, .h-step-text, .vm-phase-title');
      var stepDesc  = el.querySelector('.sop-step-desc, .proc-step-desc, .pm-step-desc, .vm-phase-steps');
      var stepNum   = el.querySelector('.sop-step-num, .proc-step-num, .pm-step-num, .h-step-num, .vm-phase-num');
      var num = stepNum ? stepNum.textContent.trim() : '';
      var title2 = stepTitle ? stepTitle.textContent.trim() : '';
      var desc2  = stepDesc  ? stepDesc.textContent.trim()  : '';
      return (num ? num + '. ' : '- ') + (title2 ? '**' + title2 + '**' : '') + (desc2 ? ' — ' + desc2 : '') + '\n';
    }

    // Bullet items (custom)
    if (el.classList && (el.classList.contains('sop-bullet') || el.classList.contains('wi-bullet') ||
        el.classList.contains('pol-bullet') || el.classList.contains('h-checks') ||
        el.classList.contains('h-rollback') || el.classList.contains('h-tips') ||
        el.classList.contains('esc-list') || el.classList.contains('ev-list') ||
        el.classList.contains('evidence-list') || el.classList.contains('gap-list') ||
        el.classList.contains('pitfall-list') || el.classList.contains('q-list') ||
        el.classList.contains('comp-list') || el.classList.contains('proc-steps') ||
        el.classList.contains('pm-steps') || el.classList.contains('h-steps') ||
        el.classList.contains('vm-phases'))) {
      var children = el.children;
      var bulkOut = '';
      for (var ci = 0; ci < children.length; ci++) {
        bulkOut += elemToMd(children[ci], depth + 1);
      }
      return bulkOut + '\n';
    }

    // Check/validation items
    if (el.classList && (el.classList.contains('h-check') || el.classList.contains('ev-item') ||
        el.classList.contains('esc-item') || el.classList.contains('evidence-item') ||
        el.classList.contains('gap-item') || el.classList.contains('pitfall-item') ||
        el.classList.contains('q-item') || el.classList.contains('comp-item'))) {
      return '- ' + text + '\n';
    }

    // Principle / card / tier content — recurse children
    if (el.classList && (el.classList.contains('sop-principle') || el.classList.contains('tier-card') ||
        el.classList.contains('acct-card') || el.classList.contains('comp-card') ||
        el.classList.contains('focus-card') || el.classList.contains('outcome-card') ||
        el.classList.contains('review-card') || el.classList.contains('threshold-card') ||
        el.classList.contains('supplier-card') || el.classList.contains('example-card'))) {
      var cardH = el.querySelector('h4');
      var cardP = el.querySelector('p');
      var cardOut = '';
      if (cardH) cardOut += '**' + cardH.textContent.trim() + '**';
      if (cardP)  cardOut += ' — ' + cardP.textContent.trim();
      return cardOut ? '- ' + cardOut + '\n' : '';
    }

    // Callout boxes
    if (el.classList && (el.classList.contains('callout-warn') || el.classList.contains('callout-info') ||
        el.classList.contains('sop-callout-warn') || el.classList.contains('sop-callout-info') ||
        el.classList.contains('instr-box') || el.classList.contains('redirect-box') ||
        el.classList.contains('req-banner') || el.classList.contains('grc-important'))) {
      var calloutP = el.querySelector('p');
      return calloutP ? '> ' + calloutP.textContent.trim() + '\n\n' : '';
    }

    // SLA / review frequency cards
    if (el.classList && (el.classList.contains('sla-card') || el.classList.contains('review-card'))) {
      var slah = el.querySelector('h4');
      var slap = el.querySelector('p');
      return (slah ? '**' + slah.textContent.trim() + '**' : '') + (slap ? ' — ' + slap.textContent.trim() : '') + '\n';
    }

    // Related links
    if (el.classList && el.classList.contains('rel-link')) {
      var href = el.getAttribute('href') || '';
      return '- [' + text + '](' + href + ')\n';
    }

    // Default — recurse children
    if (el.children && el.children.length > 0) {
      var childOut = '';
      for (var k = 0; k < el.children.length; k++) {
        childOut += elemToMd(el.children[k], depth + 1);
      }
      return childOut;
    }

    return '';
  }

  function buildMarkdown() {
    var docId    = getDocId();
    var docTitle = getDocTitle();
    var section  = getSection();
    var status   = getStatus();
    var author   = getAuthor();
    var version  = getVersion();
    var date     = new Date().toLocaleDateString('en-GB', {day:'2-digit', month:'long', year:'numeric'});
    var url      = window.location.href.replace(window.location.search,'').replace(window.location.hash,'');

    // Build header block
    var header = '# ' + docId + ': ' + docTitle + '\n\n'
      + '| Field | Value |\n'
      + '|-------|-------|\n'
      + '| **Document ID** | ' + docId + ' |\n'
      + '| **Section** | ' + section + ' |\n'
      + (status  ? '| **Status** | ' + status + ' |\n' : '')
      + (author  ? '| **Author** | ' + author + ' |\n' : '')
      + (version ? '| **Version** | ' + version + ' |\n' : '')
      + '| **Downloaded** | ' + date + ' |\n'
      + '| **Source** | ' + url + ' |\n'
      + '\n---\n\n';

    // Extract page content
    var wrapper = document.querySelector('.page-wrapper');
    if (!wrapper) return header + '*Content could not be extracted.*';

    var contentMd = '';
    var children = wrapper.children;
    for (var i = 0; i < children.length; i++) {
      var child = children[i];
      // Skip toolbar, breadcrumb, nav, footer
      if (child.classList.contains('doc-toolbar')) continue;
      if (child.classList.contains('breadcrumb')) continue;
      if (child.classList.contains('kb-footer')) continue;
      if (child.tagName && child.tagName.toLowerCase() === 'nav') continue;
      contentMd += elemToMd(child);
    }

    // Clean up excessive blank lines
    contentMd = contentMd.replace(/\n{4,}/g, '\n\n\n');

    return header + contentMd.trim() + '\n\n---\n*Downloaded from the Cyber Security Knowledge Base — soc-it-kb.github.io*\n';
  }

  // ── Public functions ───────────────────────────────────────────────────

  window.kbPrint = function() {
    window.print();
  };

  window.kbDownloadMd = function() {
    var md = buildMarkdown();
    var docId = getDocId();
    var filename = docId.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/-+/g,'-').replace(/^-|-$/g,'') + '.md';

    var blob = new Blob([md], {type: 'text/markdown;charset=utf-8'});
    var url  = URL.createObjectURL(blob);
    var a    = document.createElement('a');
    a.href     = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  // ── Toolbar injection ──────────────────────────────────────────────────
  // Automatically inject the toolbar after the breadcrumb on page load

  document.addEventListener('DOMContentLoaded', function() {
    var wrapper = document.querySelector('.page-wrapper');
    if (!wrapper) return;

    // Only inject on document pages (pages with a meta-bar or hero)
    var hasMeta = wrapper.querySelector('.meta-bar, .sop-meta-bar, .wi-meta-bar');
    var hasHero = wrapper.querySelector('.kb-page-hero, .grc-page-hero, .grc-hero, .t1-hero, .cc-hero');
    if (!hasMeta && !hasHero) return;

    // Don't inject on register pages or hub/index pages
    var url = window.location.pathname;
    var skipPatterns = ['grc-register-', 'grc.html', 'grc-governance', 'grc-risk', 'grc-compliance',
                        'asm.html', 'asm-security', 'asm-vulnerability', 'asm-patch', 'asm-threat',
                        'index.html', 'playbooks.html', 'runbooks.html', 'sops.html',
                        'work-instructions.html', 'governance.html', 'search.html'];
    for (var i = 0; i < skipPatterns.length; i++) {
      if (url.indexOf(skipPatterns[i]) !== -1) return;
    }

    var toolbar = document.createElement('div');
    toolbar.className = 'doc-toolbar';
    toolbar.innerHTML =
      '<button class="doc-toolbar-btn btn-print" onclick="kbPrint()" title="Print or save as PDF">' +
        '🖨️ Print / Save as PDF' +
      '</button>' +
      '<button class="doc-toolbar-btn btn-md" onclick="kbDownloadMd()" title="Download as Markdown">' +
        '⬇️ Download as Markdown' +
      '</button>';

    // Insert after breadcrumb if present, otherwise at start of wrapper
    var bc = wrapper.querySelector('.breadcrumb');
    if (bc && bc.nextSibling) {
      wrapper.insertBefore(toolbar, bc.nextSibling);
    } else {
      wrapper.insertBefore(toolbar, wrapper.firstChild);
    }
  });

})();
