# BCDR Second-Pass Delivery

**Date:** 15 May 2026
**Author:** Paulo Ferreira
**Domain:** Business Continuity & Disaster Recovery (second pass — domain now complete)

---

## What this delivery adds

The BCDR domain is now functionally complete. First pass (delivered earlier today) established the hubs, the three SOPs, and the two shared work instructions (BIA conduct, exercise programme). This second pass adds the DR-specific work instructions and the three fillable templates agencies populate per process and per IT service.

### 6 new BCDR files

| File | Code | Suite | Lines | Purpose |
|------|------|-------|-------|---------|
| `grc-dr-wi-01.html` | GRC-DR-WI-01 | DR | 307 | Recovery Tier Classification — assigning IT services to Tier 1–4 |
| `grc-dr-wi-02.html` | GRC-DR-WI-02 | DR | 484 | Cloud Platform DR — Azure region failure, M365 outage, Entra tenant lockout/compromise, SaaS disruption |
| `grc-dr-wi-03.html` | GRC-DR-WI-03 | DR | 483 | Worked Example — populated DR plan for 5 core IT services |
| `grc-frm-bcdr-01.html` | GRC-FRM-BCDR-01 | Shared | 480 | BIA Worksheet Template |
| `grc-frm-bcp-01.html` | GRC-FRM-BCP-01 | BCP | 389 | Business Process Continuity Plan Template |
| `grc-frm-dr-01.html` | GRC-FRM-DR-01 | DR | 440 | DR Runbook Template |

### 5 maintenance files

| File | Change |
|------|--------|
| `search-index.json` | 226 → 232 entries (6 new entries with full `desc` and `tags`) |
| `grc.html` | Stats: Forms 8 → 11, Work Instructions 5 → 8 |
| `index.html` | Stats: Total 226 → 232, WIs 81 → 84, GRC pages 44 → 50 |
| `governance.html` | Inventory: GRC WIs 5 → 8 (with all three GRC-DR-WI codes named), GRC Forms 8 → 11 (with all three GRC-FRM-* codes named); new change-log entry |
| `search.html` | Page count 226 → 232 |

`sops.html` is **not** changed in this pass — no new SOPs in second pass.

---

## What the second pass establishes

### Domain completeness

Across both passes, the BCDR domain delivers:

- **2 hubs**: `grc-bcp.html` (business-audience), `grc-dr.html` (IT-audience)
- **3 SOPs**: `grc-bcdr-sop-01` (shared methodology), `grc-bcp-sop-01` (BCP policy), `grc-dr-sop-01` (DR policy)
- **5 work instructions**: `grc-bcdr-wi-01` (BIA conduct, shared), `grc-bcdr-wi-02` (exercise programme, shared), `grc-dr-wi-01` (tier classification), `grc-dr-wi-02` (cloud DR), `grc-dr-wi-03` (worked example)
- **3 templates**: `grc-frm-bcdr-01` (BIA worksheet), `grc-frm-bcp-01` (BCP plan), `grc-frm-dr-01` (DR runbook)

13 files total. Agencies now have everything required to scope critical processes (BIA), classify the IT services that support them (tier), plan continuity (BCP plan) and recovery (DR runbook), exercise both, and report at portfolio level.

### Operating model — centre-of-excellence

The central GRC team authors the framework, methodology, terminology, exercise standards, and templates. Agencies populate their own BCP plans and DR runbooks using these templates and methodology. Reviewed and reported at portfolio level. The 13 files in this domain are not the plans themselves; they are the framework for producing and operating the plans.

This reflects the scale of the estate — 30+ countries, multiple agencies with materially different mandates (AKHS clinical, AKES/AKA education, IIS research, AKDN development), 96,000 employees — where central plan authorship would not be feasible.

### Worked example as a learning tool

`grc-dr-wi-03.html` documents the 5 most common core IT services (identity, email, file services, network, EDR) at the level of detail expected for a real Tier-1 or Tier-2 runbook. Agency IT teams populating their own runbooks via `grc-frm-dr-01` now have a concrete model showing what completeness and depth look like — tier inheritance applied, RTO/RPO traced to BIA, dependencies named, backup with immutability, validation explicit, cross-references to baseline documents (cloud, network, identity).

---

## Design choices in this pass

### Templates with fillable placeholders, not narrative

`grc-frm-bcdr-01`, `grc-frm-bcp-01`, and `grc-frm-dr-01` are structured forms with `[Fill]` placeholders the agency replaces. They are usable as-is for content authoring. Each ends with a "completeness checklist" so the named owner (BPO or IT Service Owner) can self-validate before sign-off.

### Cloud DR as named scenarios, not generic

`grc-dr-wi-02` operationalises five named scenarios with step-by-step procedures rather than generic guidance. Tenant compromise in particular gets explicit clean-up-vs-clean-tenant decision criteria, the irreversibility caveat, and a clean-tenant migration outline. This reflects the estate's hybrid posture and the genuine credible failure modes — Azure region failure, M365 outage, Entra lockout/compromise, SaaS disruption — rather than treating cloud as "the hosting choice" with implicit resilience.

### Boundary discipline maintained

The second pass does not duplicate existing content:
- Resilience design lives in `it-cl-wi-03` / `it-cl-wi-04`; DR uses those designs, doesn't re-author
- Break-glass governance lives in `it-id-wi-05`; DR-WI-02 describes break-glass *use* during recovery
- SOC incident response stays in `sop-id-01` and identity playbooks/runbooks; DR-WI-02 Scenario 4 describes recovery-to-operations running in parallel
- Risk management lives in `grc-sop-04` and `grc-register-risk`; BCDR risks flow there, no new register

---

## Pending follow-ups

- **MITRE mapping update** in `tools-references.html` to include T1485 (Data Destruction), T1486 (Data Encrypted for Impact), T1490 (Inhibit System Recovery), and M1053 (Data Backup) — deferred from first pass, natural pass after the domain is fully published
- **Tabletop exercise scenarios pack** (potential GRC-TTX-* series) — only if agencies request ready-made scenarios beyond the Exercise WI's framework guidance

---

## Validation

All 6 new files and 4 maintenance HTML files structurally validated (balanced div/span/tr/td/a/table/ul/li). `search-index.json` validates as JSON with 232 entries.

---

## Files

**New (6):**
- `grc-dr-wi-01.html` — Recovery Tier Classification
- `grc-dr-wi-02.html` — Cloud Platform Disaster Recovery
- `grc-dr-wi-03.html` — Worked Example
- `grc-frm-bcdr-01.html` — BIA Worksheet Template
- `grc-frm-bcp-01.html` — Business Process Continuity Plan Template
- `grc-frm-dr-01.html` — DR Runbook Template

**Maintenance (5):**
- `search-index.json` (226 → 232)
- `grc.html` (stats: Forms 8→11, WIs 5→8)
- `index.html` (stats: Total 226→232, WIs 81→84, GRC 44→50)
- `governance.html` (inventory + new change-log entry)
- `search.html` (page count 226 → 232)
