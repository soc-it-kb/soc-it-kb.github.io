# Asset Management Methodology — Delivery Summary

**Date:** 8 May 2026
**Files in this delivery:** 9 (4 new + 5 maintenance)

## What was built

### New documents (4)

| ID | Title | Lines | Type |
|---|---|---|---|
| **GRC-SOP-05** | Asset Management & Naming Convention Standard | 853 | Authoritative SOP — replaces TDA-NCS approach |
| **GRC-REG-CODES** | Naming Convention Codes Register | 253 | Controlled-vocabulary register (codes seeded with starter values) |
| **GRC-REG-ASSET** | Asset Register | 657 | Live register with 9 representative entries (one per asset type) |
| **GRC-WI-05** | Asset Submission Reviewer Work Instruction | 476 | Reviewer-side mechanics for processing submissions |

### Maintenance updates (5)

| File | Changes |
|---|---|
| `search-index.json` | 187 → 191 entries (added 4 new) |
| `index.html` | Total 187→191; GRC 33→37; SOPs 27→28; WIs 58→59 |
| `search.html` | "Search across 191 pages" |
| `grc.html` | Stats: SOPs 4→5; Registers 10→12; WIs 2→3. Quick-access grid: Asset Register + Codes Register cards added |
| `governance.html` | Inventory totals 194→198, GRC 33→37; SOP/WI/Register inventory rows updated; new 8 May 2026 changelog entry prepended |

## Key methodology decisions captured

**Authority** — GRC-SOP-05 is the *authoritative* source of truth for asset naming and management. Supersedes any earlier TDA Naming Convention Standard. The TDA no longer exists; codes live in GRC-REG-CODES rather than embedded in a separate convention document.

**Framework alignment** — ITIL 4 ITAM and SCM, ISO/IEC 19770-1, ISO 27001:2022 A.5.9, NIST CSF 2.0 ID.AM, NIST 800-53 CM-8, CIS Controls 1+2.

**Naming convention** — `AGENCY+COUNTRY+CITY+TYPE+SEQ` with three identifier patterns:
- Pattern A — hostname-as-Asset-ID for physical/located assets (e.g. `AKDNPTLISSRV0001`)
- Pattern B — synthetic ID for non-host assets (e.g. `ASSET-AKDN-APP-0001`)
- Pattern C — CENTRAL prefix for cross-agency centrally-managed (e.g. `ASSET-CENTRAL-SAAS-0001`)

**Schema** — 34 fields across 8 groups (28 SCM mandatory; 6 ITAM extension optional). 3-level maturity ladder so agencies don't need full ITAM on day one.

**Lifecycle** — 7 states (Proposed/Onboarding/Live/Under-review/Decommissioning/Decommissioned/Archived) with documented transitions and authorisers per state.

**Federation** — assets belong to one operating unit (agency code) or to CENTRAL. Schema is ready for backend filtering once Azure GRC app exists.

**Review cadence** — annual T0/T1, 18m T2, 24m T3 — matches existing tier model.

## What was NOT built (deferred)

- **Asset Onboarding Form** — the FRM-12-or-not decision is being matured separately. Once locked, the form will be authored to match the chosen model and integrate with this SOP.
- **Mailto:submit pattern** for Approach B — separate session.
- **Azure migration prep** — purely static documentation methodology built today; no backend hooks.

## Verification

- All 4 new files: HTML balanced (every `<div>`, `<tr>`, `<table>`, `<ul>`, `<ol>` opens and closes)
- Asset Register: 9/9 entries verified present, schema applied uniformly
- Codes Register: starter codes seeded (5 agencies + CENTRAL, 8 cities IATA-aligned, 14 asset types, 11 function tags)
- search-index.json: 191 entries, all 4 new entries with correct section/sub assignments
- governance.html inventory totals reconcile: 198 = 23+22+20+5+14+6+15+42+37+14
- grc.html stats reconcile: 33 items + 4 nav pages = 37 GRC pages
- All hyperlinks between new documents are bi-directional (SOP↔Register, SOP↔WI, WI↔Register)

## Outstanding items still queued

1. Asset Onboarding Form (pending FRM-12-or-not decision)
2. Mailto: submit pattern on GRC-FRM-13
3. FRM-06/08/10 + IRP Annex Template migration to FRM-12 model
4. Tabletop exercise scenarios pack
5. Azure Static Web Apps migration (Phase 1 — Entra ID auth, static)
6. Azure GRC app (Phase 2 — Functions + Cosmos/SQL for live registers)
7. 6 broken link targets from earlier sweep
