# Cloud Baselines Domain — Delivery Summary

**Date:** 12 May 2026
**Author:** Paulo Ferreira
**Scope:** 7th ASM domain — Microsoft 365 and Microsoft Azure tenant baselines
**Status:** Complete; all files balanced and validated

---

## What's in this delivery (13 files)

### New (7 files — drop into repo root)

| File | Lines | Purpose |
|---|---|---|
| `asm-cloud-baselines.html` | 308 | Cloud domain hub. 5 platform-cards (Tenant Identity / M365 / Azure Subscription / Azure Workloads / Defender Suite). Framework alignment table with 10 entries (CIS M365, CIS Azure, MS Secure Score, NIST CSF 2.0, 800-53 r5, 800-63B, ISO 27001, 27017, 27018, MCSB v1). Tier-aware metrics. Day-1 SIEM-gap callout. |
| `it-cl-sop-01.html` | 394 | 7-section SOP. 5 requirement-domains (Tenant Identity 9 items, M365 11, Azure Subscription 10, Azure Workloads 10, Defender Suite 9) each tier-tagged. 8 roles. Secure Score targets per tier (M365 A3/E3 ≥70%, E5 ≥80%; Azure T0/1 ≥75%, T2/3 ≥60%). SIEM-under-transition callout in §3.7. |
| `it-cl-wi-01.html` | 415 | Tenant Identity & CA. 9 steps cross-cutting M365 and Azure. Break-glass first (cloud-only, vaulted off-tenant, excluded from every CA, SOC-monitored — flagged as single most important). Eliminate legacy auth → MFA → CA-001..007 → named locations → Identity Protection (E5) → PIM (E5) → guest access → SSPR. |
| `it-cl-wi-02.html` | 460 | M365 Tenant Hardening. 10 tier-aware steps. Exchange anti-phishing → SPF/DKIM/DMARC progression to `p=reject` → SharePoint/OneDrive sharing → Teams federation → Unified Audit Log (tiered retention) → Purview labels (A3/E3+; auto-labelling E5) → DLP → Defender for Office 365 P2 (E5) → IRM/CC (E5) → Customer Lockbox (E5). |
| `it-cl-wi-03.html` | 456 | Azure Subscription Baseline. 10 steps. Management group hierarchy → Defender for Cloud plans per subscription tier → Azure Policy at MG scope (MCSB + custom deny set) → diagnostic settings via DeployIfNotExists → Activity Log forwarding → Defender continuous export → RBAC least-privilege → resource locks → cost-anomaly alerting (cryptomining/egress) → tagging enforcement. |
| `it-cl-wi-04.html` | 475 | Azure Workload Patterns. 10 steps. Storage (CMK + soft-delete + immutable for T0/1) → Key Vault (purge protection mandatory) → VNet/NSG → Private Endpoints → **Azure WAF on App Gateway/Front Door** (absorbs cloud-WAF scope deferred from IT-SI-WI-02) → SQL/Cosmos → VMs → App Service/Functions → backup with MUA → DDoS Protection Standard. |
| `it-cl-wi-05.html` | 437 | Defender Suite Configuration. 9 tier-aware steps. Tenant-side config only; SOC operational use boundary explicit. Defender for Endpoint (A3/E3+) → Defender for Office 365 (E5, x-ref WI-02 §8) → Defender for Identity (DC sensors) → Defender for Cloud Apps (E5) → Defender for Cloud (x-ref WI-03 §2) → TVM to central VM → SIEM ingestion with severity mapping → boundary maintained → suite-level metrics. |

### Maintenance (6 files — replace in repo root)

| File | Change |
|---|---|
| `search-index.json` | 205 → 212 entries (7 cloud entries added with full desc/tags fields) |
| `index.html` | Stats: 205→212 total pages, 69→74 WIs, 30→31 SOPs, 80→87 ASM pages. Added 7th ASM domain link with cloud slate-blue palette (`.cl`). ASM Highlight description and Work Instructions description updated. |
| `asm.html` | Added 7th domain card "Cloud Baselines" (☁️ ASM-CL) with slate-blue palette (gradient `#E8F0F8`→`#C5DAEB`, border `#A8C5DE`, accent `#2E5C8A`). Stats reconciled to honest counts: 6→7 domains, 14+→18 SOPs, **17→57 WIs** (the previous 17 was stale; the search-index has 57 ASM WIs spanning 7 sub-domains). |
| `governance.html` | Inventory date 11→12 May. ASM domain pages 8→9. ASM SOPs 17→18. ASM WIs 52→57. Added "ASM WIs — Cloud Baselines" inventory table row. Full 12 May 2026 changelog entry describing the cloud delivery, all 7 deferrals, the 7 baseline principles, the 5 WIs, framework alignment (10 entries), and the maintenance footprint. Footer date 11→12 May. |
| `search.html` | Page count 205 → 212. |
| `sops.html` | 27 → 28 SOPs total; ASM & IT Ops 17 → 18; added "Cloud baselines" sub-group with IT-CL-SOP-01 entry under ASM & IT Operations section, dated 12 May 2026. |

---

## Design decisions (locked via interactive Q&A earlier in session)

- **Scope:** M365 + Azure primary; AWS/GCP deferred (recorded in GRC-REG-ASSET; future multi-cloud extension)
- **Entra ID:** tenant-level controls here (CA, PIM, break-glass, sign-in risk); identity governance (JML, recertification) deferred to future Identity domain SOP
- **Defender suite:** tenant-side config here (WI-05); SOC operational use under SOC SOPs — boundary documented in WI-05 Step 8
- **Cloud-WAF:** Azure-native here (WI-04 Step 5, absorbing the scope deferred from IT-SI-WI-02); third-party (Cloudflare, AWS WAF, Akamai) deferred to future vendor extension
- **Azure landing zone:** Azure Policy as enforcement here (WI-03 Step 3); broader architecture (hub-spoke, management group reference design) deferred to future Cloud Architecture document
- **SIEM treatment:** vendor-neutral "central SIEM" terminology throughout; current 1-tenant state is recorded as time-bounded exceptions vs the 12–18-month migration roadmap. The baseline crystallises the gap.

## Licensing-tier-aware throughout

- `.tier-tag.all` (green) — required at every tier
- `.tier-tag.e3` (orange) — required at A3 / E3 and above
- `.tier-tag.e5` (purple) — requires E5 licensing

Each WI step indicates which tiers it applies to. Conformance is reported per tier so deviations are visible against achievable expectations rather than against an aspirational universal standard.

---

## Bullet-wrap discipline

Applied to outer flex containers from the start. The SI hub Scope/Metrics bug (flex with `align-items:flex-start` splitting `<li><strong>` patterns to separate rows) did not recur in the cloud hub. Inner `step-body ul` lists use the same `<li><strong>` pattern that SI WIs use and that renders correctly — different CSS context, no bug.

## Validation

All 7 cloud files + 5 maintenance HTML files + 1 JSON have balanced tags:

- `<div>`/`</div>` pairs match
- `<span>`/`</span>` pairs match  
- `<tr>`/`</tr>` pairs match
- `<a>`/`</a>` pairs match
- `<table>`/`</table>` pairs match
- 0 unwrapped outer `<li><strong>` patterns in flex containers

Search index post-cloud: **212 entries** (7 cloud + 205 prior).

## Estate counts post-cloud (honest, from search-index)

- **ASM Domain hubs:** 9 (in search index: 3 dedicated hubs + 6 pre-search-index domain pages tracked in governance inventory)
- **ASM SOPs:** 18 (added IT-CL-SOP-01)
- **ASM WIs:** 57 (added 5 cloud WIs to existing 52)
  - IT-EP-WI: 12 · IT-SRV-WI: 19 · IT-GOV-WI: 6 · IT-NET-WI: 6 · IT-TI-WI: 5 · IT-SI-WI: 4 · IT-CL-WI: 5

---

## Pending follow-ups (not blocking this delivery)

1. Future Identity domain SOP (JML / recertification / eligibility curation; cloud-WI-01 covers tenant-level controls only)
2. Future Application Delivery sub-domain (reverse proxies, API gateways)
3. Future multi-cloud extension (AWS + GCP baselines)
4. Future Cloud Architecture document (landing zone reference design)
5. Future vendor-specific cloud-WAF extension (Cloudflare, AWS WAF, Akamai)
6. Tabletop exercise scenarios pack (GRC-TTX-01..NN)
7. BCP / DRP plans
8. FRM-06/08/10 + IRP Annex Template migration to FRM-12 model
9. Asset Onboarding Form (pending FRM-12-or-not maturation)
10. mailto: submit pattern on GRC-FRM-13
11. Azure Static Web Apps migration with Entra ID (Phase 1)
12. GRC app on Azure (Functions + Cosmos/SQL) Phase 2
13. 6 broken link targets from earlier sweep
14. `td.code` misuse sweep across other GRC/ASM pages
15. Retro-fix bullet-wrap pattern across other ASM hubs if formatting issues found
