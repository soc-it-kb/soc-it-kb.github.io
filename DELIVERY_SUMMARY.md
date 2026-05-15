# Identity Governance & Lifecycle — Domain Delivery

**Date:** 15 May 2026
**Author:** Paulo Ferreira
**Domain:** ASM-ID — 8th ASM sub-domain
**Closes off:** ASM section completeness — final ASM domain in the planned set

---

## Scope locked

Per the in-conversation Q&A:

- **Shape:** Option A — single SOP + 5 WIs (JML, recert, role design, non-human, privileged identity governance). Tight scope; finishes in one delivery.
- **Placement:** Standalone Identity domain — new ASM sub-domain alongside Cloud, Security Infrastructure, Network.
- **Coverage:** Hybrid + non-human — Entra ID + on-prem AD; humans + service accounts/principals/managed identities/certs.

Delivery shape ended up at 7 files (hub + SOP + 5 WIs) matching the Cloud delivery shape, for structural consistency with the other ASM sub-domains which all have hub pages. The hub is lightweight; the SOP carries the substantive policy content.

---

## 7 new files

| File | Purpose | Lines |
|------|---------|-------|
| `asm-identity-governance.html` | Domain hub — 5-class identity scope, framework alignment, roles, metrics, related domains | 309 |
| `it-id-sop-01.html` | Policy-level SOP — 7 principles, 5 requirement domains (53 items total), 8 roles, framework alignment | 402 |
| `it-id-wi-01.html` | JML Lifecycle — 7 steps, joiner / mover / leaver / student / guest / reconciliation. SLA dashboard table. | 362 |
| `it-id-wi-02.html` | Access Recertification — 8 steps, cadence per tier, named reviewers, non-response default, evidence retention | 395 |
| `it-id-wi-03.html` | Role Design & Entitlement — 9 steps, role catalogue, naming convention, SoD, drift check | 392 |
| `it-id-wi-04.html` | Non-Human Identity Governance — 10 steps, inventory, ownership, rotation, OAuth review, decommissioning | 438 |
| `it-id-wi-05.html` | Privileged Identity Governance — 10 steps, eligibility layer above PIM activation, T0 two-person approval, PAW correlation | 423 |

All 7 files HTML-validated (div / span / tr / table tag balance).

---

## 6 maintenance files updated

| File | Change |
|------|--------|
| `search-index.json` | 212 → 219 entries (7 identity entries with full `desc` and `tags`) |
| `asm.html` | Added `.domain-card.identity` rose-pink CSS variant. 8th domain card (ASM-ID). Stats 7→8 domains, 18→19 SOPs, 57→62 WIs. |
| `index.html` | Added `.asm-domain-link.id` CSS. 8th ASM link 🔑 Identity Governance. Stats 212→219 pages, 74→79 WIs, 31→32 SOPs, 87→94 ASM pages. ASM Highlight + WI descriptions updated. |
| `governance.html` | Date pill + inventory date 12→15 May 2026. Inventory cards 9→10 / 18→19 / 57→62. ASM domain pages + ASM SOPs rows updated. New Identity Governance WIs row in breakdown. New 15 May 2026 changelog entry with 31 tags. Footer date updated. |
| `search.html` | Page count 212 → 219. |
| `sops.html` | Identity governance sub-group added under ASM & IT Operations with IT-ID-SOP-01. SOPs-total counter 28→29 (ASM/IT/SOC sub-total; site-wide is 32 including GRC). |

---

## Design choices worth flagging

### 1. Boundary discipline against adjacent domains

This domain governs **identity itself**; it does NOT duplicate:

- `IT-CL-WI-01` covers tenant-platform identity config (CA, PIM activation, MFA, break-glass) — the *how*
- `IT-SI-WI-04` covers PAM platform mechanics (vault, session recording, credential rotation)
- `IT-EP-SOP-PAW-01` covers PAW build and lifecycle
- `IT-SRV-WI-DC-01` covers Tier-0 AD administrative access enforcement
- SOC `SOP-ID-01` + ID-PB / ID-RB cover identity incident response (compromise, MFA bypass, OAuth abuse)

The most important boundary: **WI-05 is the eligibility governance layer; IT-CL-WI-01 §7 is the activation mechanism**. Activation = how someone temporarily elevates. Eligibility = whether they should be allowed to. The two cooperate; this delivery is the second.

### 2. Five identity classes, not one

The domain treats identities in five operational classes — employees/contractors, students/alumni, guests, on-prem service accounts, non-human cloud identities — each with its own lifecycle pattern, governance owner, and cadence. This matters because student JML is calendar-driven and bulk; staff JML is event-driven; service accounts have no JML at all in the traditional sense; guests need sponsors not managers.

### 3. Non-human as first-class

WI-04 exists because in most estates non-human identities outnumber humans 5-30x and are the largest under-governed surface. Treating service accounts and service principals as an afterthought is the dominant industry failure mode. The WI gives them dedicated inventory, ownership, rotation, OAuth review, and decommissioning processes equivalent in rigour to human-identity governance.

### 4. Privileged eligibility, not activation

WI-05 is deliberately distinct from PIM activation. PIM activation is the mechanism — request, MFA, justification, time-window — and lives in IT-CL-WI-01 because it's tenant-platform configuration. WI-05 is the governance layer: who's *eligible* to activate, why, for how long, reviewed by whom, with two-person approval at T0 and cross-domain SoD enforcement. Standing privilege is the failure mode; eligibility-not-assignment is the principle.

### 5. Hybrid scope

The estate has on-prem AD in most agencies plus Entra. Cloud-only treatment would create real gaps. The WIs explicitly cover both: AD-driven sync, Entra-only identities, AD-only identities, and the propagation discipline between them.

### 6. Bullet-wrap discipline

Same approach as Cloud / SI WIs: outer flex containers from the start, inner `.step-body ul` lists using `<li><strong>...</strong>` pattern. False-positive count from naive grep matches Cloud/SI baselines.

---

## Palette

Identity rose / pink — distinctive across all existing domain palettes:

- Primary: `#8B2D5C` deep rose
- Light: `#FAEBF2`
- Border: `#E2B3C8`
- Dark: `#5C1A3A`
- Hero gradient: `#3A1530` → `#5C1A3A` → `#8B2D5C`

Existing domain palettes for reference:
- ASM hub: `#5B2D8E` purple
- Network: `#145570` teal
- Security Infrastructure: `#8F500C` amber
- Cloud: `#2E5C8A` slate blue
- **Identity: `#8B2D5C` rose** ← this delivery
- GRC: `#0E5C5C` teal

---

## File counts (post-delivery)

| Category | Before | After | Delta |
|----------|--------|-------|-------|
| Total pages | 212 | 219 | +7 |
| ASM domain pages | 9 | 10 | +1 |
| ASM SOPs | 18 | 19 | +1 |
| ASM WIs | 57 | 62 | +5 |
| All SOPs | 31 | 32 | +1 |
| All WIs | 74 | 79 | +5 |
| All ASM pages | 87 | 94 | +7 |
| search-index entries | 212 | 219 | +7 |

---

## Pending future follow-ups (not in this delivery)

Carried forward for future sessions, not blocking this delivery:

1. Future Application Delivery sub-domain (reverse proxies, API gateways)
2. Future multi-cloud extension (AWS + GCP baselines)
3. Future Cloud Architecture document (landing zone reference design)
4. Future vendor-specific cloud-WAF extension (Cloudflare, AWS WAF, Akamai)
5. Tabletop exercise scenarios pack (GRC-TTX-01..NN)
6. BCP / DRP plans
7. FRM-06/08/10 + IRP Annex Template migration to FRM-12 model
8. Asset Onboarding Form (pending FRM-12-or-not maturation)
9. `mailto:` submit pattern on GRC-FRM-13
10. Azure Static Web Apps migration with Entra ID (Phase 1)
11. GRC app on Azure (Functions + Cosmos/SQL) Phase 2
12. 6 broken link targets from earlier sweep
13. `td.code` misuse sweep across other GRC/ASM pages
14. Retro-fix bullet-wrap pattern across other ASM hubs if formatting issues found
15. Back-inject ATT&CK technique IDs into individual playbook/runbook content
16. Add search-index entry for tools-references.html
17. **Update MITRE mapping to include identity WIs (T1136 Create Account, T1078 Valid Accounts, T1098 Account Manipulation, T1078.004 Cloud Accounts, T1098.001 Add Cloud Credentials, T1484 Domain/Tenant Policy Modification, T1078.002 Domain Accounts, T1098.003 Add Privileged Role)** — natural next pass given the new WIs cover several mitigation patterns

---

## How to deploy

1. Drop the 7 new files (`asm-identity-governance.html`, `it-id-sop-01.html`, `it-id-wi-01.html` through `it-id-wi-05.html`) into the soc-it-kb.github.io repo root.
2. Replace the 5 modified HTML files (`asm.html`, `index.html`, `governance.html`, `search.html`, `sops.html`).
3. Replace `search-index.json`.
4. Commit and push to GitHub Pages.

No new shared CSS or JS — the identity rose-pink palette is scoped to the new pages via inline `:root` CSS variables; the `.domain-card.identity` and `.asm-domain-link.id` variants are added inline to `asm.html` and `index.html` respectively.

---

## Closing note

This delivery rounds out the ASM section as originally planned: 8 domains covering the full preventive control surface across endpoint / server / network / security-infrastructure / cloud / identity, each with policy SOP and operational WIs, vendor-agnostic where the estate is mixed, framework-aligned throughout, with deliberate boundaries against adjacent SOC and GRC content.

The next natural enhancement is the MITRE mapping pass (item 17 above) to thread the new identity WIs into the existing T-code coverage on `tools-references.html` — but that's optional and not blocking.
