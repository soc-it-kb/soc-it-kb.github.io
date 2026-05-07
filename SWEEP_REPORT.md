# IRP Cross-Reference Sweep — Report

**Files processed (in-scope):** 77
**Files skipped (out of scope):** 37
**Auto-fixes applied:** 138 fixes across 69 files
**Items flagged for review:** 19 flags across 19 files

## What was changed in every in-scope file

1. **IRP banner inserted** — subtle teal callout under the page hero, linking to GRC-IRP-01.
2. **Doctype/body structure fixed** — your existing files had a script-placement bug (`</head><script></body>` appearing before the actual body content). The misplaced `</body>` was removed; scripts moved into `<head>`; a clean `<body>` opens before the topnav.

## Out-of-scope files (left untouched)

37 IT operations files (`it-ep-*`, `it-srv-*`) were correctly skipped per the agreed scope. **However**, every one of these files has the same `</body>` placement bug as the in-scope files. They render OK in browsers but will fail strict HTML validation. Recommend a separate cleanup pass.

## Flagged items — links to docs that do not exist in the repo

| Missing doc | Referenced from | Likely status |
|---|---|---|
| `asm-threat-intelligence.html` | it-ti-sop-01.html, it-ti-sop-02.html, it-ti-sop-03.html (+5 more) | Future ASM doc — placeholder link |
| `ep-pb-05.html` | ep-inv-win-01.html, ep-wi-02.html, ep-wi-03.html (+2 more) | Possibly missing or future op doc |
| `asm-security-baselines.html` | it-pm-sop-01.html, it-pm-sop-02.html, it-pm-sop-03.html (+1 more) | Future ASM doc — placeholder link |
| `asm-patch-management.html` | it-pm-sop-01.html, it-pm-sop-02.html, it-pm-sop-03.html | Future ASM doc — placeholder link |
| `nw-rb-04.html` | nw-rb-03.html, nw-rb-05.html | Possibly missing or future op doc |
| `asm-vulnerability-management.html` | it-vm-sop-01.html | Future ASM doc — placeholder link |

## Verification

All 77 in-scope files were verified after editing:
- Exactly 1 `<body>` open and 1 `</body>` close per file ✓
- Exactly 1 `<html>` open and 1 `</html>` close per file ✓
- IRP banner marker present in every file ✓
- Banner inserted between hero block and meta-bar (correct placement) ✓

## In-scope file inventory by family

- `em-pb-*`: 7 files
- `em-rb-*`: 9 files
- `em-wi-*`: 3 files
- `ep-inv-*`: 1 files
- `ep-pb-*`: 4 files
- `ep-rb-*`: 4 files
- `ep-wi-*`: 4 files
- `id-pb-*`: 7 files
- `id-rb-*`: 5 files
- `id-wi-*`: 4 files
- `it-pm-*`: 3 files
- `it-ti-*`: 8 files
- `it-vm-*`: 1 files
- `nw-pb-*`: 5 files
- `nw-rb-*`: 4 files
- `nw-wi-*`: 3 files
- `sop-em-*`: 1 files
- `sop-ep-*`: 1 files
- `sop-id-*`: 1 files
- `sop-im-*`: 1 files
- `sop-nw-*`: 1 files