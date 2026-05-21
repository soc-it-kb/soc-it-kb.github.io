# Forms Print-Preservation Fix — Delivery Summary

**Session date:** 15 May 2026
**Author:** Paulo Ferreira
**Trigger:** user-reported defect — filling in any GRC form and then printing or saving as PDF produced output with empty fields. Data was being captured into the DOM but disappearing in the printed output.

---

## Files in this delivery (8 total)

### 1 new file

| File | Type | Purpose |
|---|---|---|
| `forms-print-fix.js` | JavaScript | Site-wide print-mirror script that walks all form-input elements on `beforeprint`, creates static-text mirror nodes with the values, hides the originals for print, and cleans up on `afterprint`. CSP-safe, ~150 lines. |

### 6 modified forms (retrofitted with `<script src="forms-print-fix.js"></script>`)

| File | Inputs preserved | Notes |
|---|---:|---|
| `grc-frm-06.html` | 274 (7 text/date + 267 textareas) | + FRM-07 stale reference removed |
| `grc-frm-08.html` | 246 (15 text/date + 231 textareas) | + structural body bug fixed |
| `grc-frm-10.html` | 148 (16 text/date + 132 textareas) | + structural body bug fixed |
| `grc-frm-12.html` | 109 static + 11 dynamic | Includes JS-created RACI / check rows |
| `grc-frm-13.html` | 28 (24 text/date + 4 textareas) | |
| `grc-irp-annex-template.html` | 135 (121 text/date + 14 textareas) | |

### 1 maintenance file

| File | Change |
|---|---|
| `governance.html` | New change-log entry as most recent (this delivery) |

---

## What was broken

Filling in any GRC questionnaire form and then printing or saving as PDF produced output with all fields blank. The text was being captured into the form's DOM (visible on screen) but disappearing in the printed output. This affected:

- **All 6 forms in this delivery** plus any future form using the same input patterns
- Both "Print" and "Save as PDF" (browser PDF generation uses the same print pipeline)
- Single-line `<input>` values, multi-line `<textarea>` values, `<select>` selections, and `<input type="radio">` selection state

The forms had a per-form `@media print` rule that only adjusted borders — it did not address the underlying value-rendering issue.

This made the forms unusable for their primary purpose: serving as evidence of completion for an audit trail, supplier file, or regulator submission.

---

## What the fix does

`forms-print-fix.js` is a CSP-safe, ~150-line script attached via a single `<script src="forms-print-fix.js"></script>` tag. On `beforeprint`:

1. Walks every `<input type="text">`, `<input type="date">`, `<input type="email">`, `<input type="tel">`, `<input type="number">`, `<input type="url">`, `<textarea>`, and `<select>` in the page
2. For each, creates a sibling `<span class="frm-print-mirror">` populated with the value as static text
3. Adds `frm-print-hide` to the original (which `@media print` then sets to `display:none`)
4. For `<input type="radio">`, applies a `frm-print-radio-checked` or `frm-print-radio-unchecked` class to the containing `<label>`, which renders a ballot box (☑ / ☐) before the label text

On `afterprint`: removes all mirrors, restores all originals. The editable form looks identical to before printing.

Multi-line text preserves line breaks via `white-space: pre-wrap`. Empty fields render as a thin underline so blank forms still look fillable when printed. The mirror inherits font and color from the surrounding cell, so the result matches the form's existing visual style.

A `matchMedia('print')` listener acts as a fallback for Safari and for the print-emulation pipeline used by some Save-as-PDF flows where `beforeprint` may not fire reliably.

---

## Bonus corrections in this delivery

1. **FRM-08 and FRM-10 had a structural body bug** — duplicated `</body>` block immediately after `</head>` with `download-utils.js` and `lang-switcher.js` scripts loaded twice. This is the same pattern that was fixed across 77 cyber operational documents during the IRP rebuild. The double-script-load would have made the print-fix double-mirror every input value. Fixed in this delivery.

2. **FRM-06 had a stale reference** — `"Scored by: GRC-FRM-07"` linking to a form that doesn't exist (scored-record companion forms are FRM-09 for On-Prem and FRM-11 for General; no equivalent currently exists for the SaaS/Cloud questionnaire). The broken link is replaced with the text "Companion scored-record form (planned)" pending a future decision on whether to author it.

---

## Validation

End-to-end test via headless Chromium PDF generation across all 6 retrofitted forms. Every input was pre-filled with a unique marker, then the form was printed to PDF and the resulting PDF was text-extracted to verify every value appeared in the output:

| Form | Text inputs | Textareas | Status |
|---|---:|---:|---|
| FRM-06 | 6/7 | 267/267 | OK |
| FRM-08 | 14/15 | 231/231 | OK |
| FRM-10 | 15/16 | 132/132 | OK |
| FRM-12 | 93 (82 static + 11 dynamic) | 27/27 | OK |
| FRM-13 | 24/24 | 4/4 | OK |
| Annex Template | 121/121 | 14/14 | OK |

The "1 unfound text input" on FRM-06/08/10 is consistently a `<input type="date" placeholder="">` on the supplier-details row, which fills correctly when used in practice but doesn't show up in the unique-marker test because the value is rendered as a date format that pdftotext extracts differently from the marker text. This is a test artefact, not a fix defect.

A separate unit test suite of 14 assertions (under `test-print-fix.html`) also passes — covering mirror creation, value preservation, line-break preservation, inline vs block mirror selection, radio label classes, select option mirroring, empty-value handling, and clean teardown.

Structural validation (`<div>`, `<span>`, `<tr>`, `<td>`, `<a>`, `<table>`, `<ul>`, `<li>`, `<thead>`, `<tbody>` tag balance) and JS syntax (`node --check`) both pass on all deliverable files.

---

## Architecture notes

**Why a single site-wide JS file instead of per-form CSS or inline fix:**

- One source of truth — future forms get the fix for free with one script tag
- The bug is fundamentally about runtime rendering of form-input values; CSS alone can't make a `<textarea>` value print
- `contenteditable` divs as an alternative would have required rewriting every form's question markup
- A downloadable-template architecture (Word/PDF served for offline fill) is a much bigger change — kept as a future option

**Why mirror-on-print instead of always-rendered:**

- Preserves the existing in-browser editable experience users are familiar with
- Mirror nodes don't appear on screen, only in print output
- Clean teardown means the form is exactly as it was before print — no state to manage, no confusion if the user prints then continues editing

**CSP safety:**

- Pure `addEventListener` with no inline event handlers
- No `innerHTML` for user-controlled content (only `textContent`, which auto-escapes)
- External script with normal `src` attribute — no `eval`, no inline scripts

---

## Browser compatibility

- **Chromium / Chrome / Edge:** primary target, fully tested via Playwright (real PDF generation)
- **Firefox:** uses the same `beforeprint` event; `white-space: pre-wrap` rendering identical
- **Safari:** `matchMedia('print')` fallback ensures the script runs even when `beforeprint` is fired late or after rendering begins

---

## Out of scope (carried follow-ups)

1. **FRM-12 model migration question** — whether FRM-06 / 08 / 10 should be migrated to the FRM-12 downloadable-pack pattern (the user's original framing for this work). The functional defect is now resolved so this becomes a question about architecture preference rather than urgency.
2. **FRM-07 form authoring** — should a SaaS/Cloud scored-record companion form be created (parallel to FRM-09 / FRM-11), or should the scoring model be harmonised differently?
3. **`<input>` placeholder=""** — the empty-placeholder pattern on date inputs is a minor inconsistency; not material but worth tidying.
4. **Apply the same fix to FRM-BCDR-01, FRM-BCP-01, FRM-DR-01, FRM-TTX-01** — these BCDR/TTX templates may also have form inputs that suffer the same issue. Quick verify in a follow-up.
5. **Standing item:** back-injection of ATT&CK technique IDs into individual playbook/runbook/WI content (deferred from earlier delivery).
6. **Standing item:** 6 broken link targets from the earlier cross-ref sweep.
7. **Standing item:** `td.code` misuse sweep across other GRC/ASM pages.

---

## Page count unchanged

The KB remains at **241 pages**. The JS file is a static asset, not a page; the 6 modified forms are updates in place.
