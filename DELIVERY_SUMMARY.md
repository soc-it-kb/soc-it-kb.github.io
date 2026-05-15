# BCDR Domain — First-Pass Delivery

**Date:** 15 May 2026
**Author:** Paulo Ferreira
**Scope:** Business Continuity & Disaster Recovery domain — first of two passes.

## Decisions locked before authoring

| Question | Decision |
|---|---|
| Document shape | **Option B** — Two parallel suites: GRC-BCP-* (business-audience) and GRC-DR-* (IT-audience). Mirrors industry practice; clean separation. |
| Scope breadth | **Framework + templates** — central authorship of policy/methodology/templates; agencies populate their own plans. Centre-of-excellence model. |
| Cloud DR | **First-class concern** — Azure region failure, M365 outage, Entra tenant lockout/compromise treated as named designed-for scenarios. |
| Methodology placement | **B1** — three SOPs: shared methodology (`GRC-BCDR-SOP-01`) + BCP policy + DR policy. Avoids drift from authoring shared concepts twice. |
| Palette | **Two variants of forest green** — BCP warmer (`#2D6B3F`), DR cooler/teal (`#1F5A4A`). Family identity with audience differentiation. |
| Delivery cadence | **Split into two passes** — this is pass 1 (7 files); pass 2 will deliver 3 DR-specific WIs + 3 templates. |

## Files in this delivery (7 new + 6 maintenance = 13)

### New BCDR content

| File | Code | Type | Audience | Lines |
|---|---|---|---|---|
| `grc-bcp.html` | GRC-BCP | Domain hub | Business | 284 |
| `grc-dr.html` | GRC-DR | Domain hub | IT | 304 |
| `grc-bcdr-sop-01.html` | GRC-BCDR-SOP-01 | SOP (methodology, shared) | Shared | 291 |
| `grc-bcp-sop-01.html` | GRC-BCP-SOP-01 | SOP (policy) | Business | 272 |
| `grc-dr-sop-01.html` | GRC-DR-SOP-01 | SOP (policy) | IT | 255 |
| `grc-bcdr-wi-01.html` | GRC-BCDR-WI-01 | WI (BIA, shared) | Shared | 284 |
| `grc-bcdr-wi-02.html` | GRC-BCDR-WI-02 | WI (Exercise, shared) | Shared | 296 |

### Maintenance updates

| File | Change |
|---|---|
| `search-index.json` | 219 → 226 entries (7 BCDR entries with full `desc` and `tags`) |
| `grc.html` | Domain grid layout `1fr 1fr 1fr` → `auto-fit minmax(280px,1fr)` (5 cards wrap naturally 3+2); added BCP + DR domain cards with new `.bcp` and `.dr` CSS variants; stats SOPs 5→8, WIs 3→5, Domains 3→5; added Continuity / Recovery use case cards; Plans & response section gained the 3 BCDR SOPs |
| `index.html` | Stats: total 219→226, SOPs 32→35, WIs 79→81, GRC pages 37→44; GRC card description mentions business continuity & disaster recovery and ISO 22301:2019; intro paragraph adds BCDR within GRC enumeration; footer date 11→15 May |
| `governance.html` | New change-log entry (15 May 2026); inventory: GRC Hub domain pages 4→6, GRC SOPs 5→8 (all three BCDR codes named), GRC WIs 3→5 (both BCDR WI codes named) |
| `sops.html` | GRC SOPs section gained 3 BCDR entries; stats SOPs total 29→32, GRC 5→8; footer date 11→15 May |
| `search.html` | Page count 219 → 226 |

## Content highlights

### `grc-bcp.html` — Business Continuity hub
- Operating model section frames the centre-of-excellence approach
- 6 disruption-type categories (Cyber, Technology, Supplier, Physical, People, Regional) with primary-owner mapping
- Boundary table making explicit what is in scope vs what lives elsewhere (IRP, DR, GRC-REG-RISK)
- 7-role accountability at domain level
- 6 portfolio metrics for tracking

### `grc-dr.html` — IT Disaster Recovery hub
- Recovery tier glance: T1 ≤4h/15m, T2 ≤24h/4h, T3 ≤72h/24h, T4 ≤7d/7d
- Cloud DR first-class section enumerating 5 scenarios with named recovery paths
- Boundary table making explicit what is in scope vs what lives in Cloud Baselines (IT-CL-WI-03/04), Identity Governance, IRP, SOC SOP-ID-01
- 8-role accountability
- 8 portfolio metrics including cloud tenant break-glass health

### `grc-bcdr-sop-01.html` — Shared methodology
- 13 defined terms (RTO, RPO, MTPD, MBCO, BIA, recovery tier, business process, IT service, etc.)
- 6 BIA methodology principles (process-first not system-first, beneficiary-safety-trump, time-graduated impact, dependencies-bridge-to-DR)
- Standard RTO/RPO classification bands with IT tier mapping
- Exercise framework: 4 types with cadence per tier
- BCDR Steering Committee composition, cadence, reserved decisions
- 8-artefact review cadence table
- Framework alignment: ISO 22301, ISO 27001 A.5.29/A.5.30/A.8.13/A.8.14, NIST 800-34, NIST CSF 2.0 RC.*, NIST 800-53 CP family, CIS 11, SOC 2 A1.2/A1.3, MITRE M1053

### `grc-bcp-sop-01.html` — Business Continuity Policy
- 11 policy statements (named ownership, BIA cadence 24m, exercise cadence Tier-1 annual / Tier-2 24m, plan currency, exception handling, plan-accessible-offline for Tier-1, framework alignment)
- 10 roles & responsibilities
- 6 invocation principles including documented decision, lower bar for Tier-1, parallel BCP+IRP for cyber-triggered continuity, formal stand-down with AAR
- Plan currency & assurance: 7 mechanisms

### `grc-dr-sop-01.html` — IT Disaster Recovery Policy
- 13 policy statements (tier assignment, tier minima, runbook currency for T1/T2, immutable backup for cyber resilience, cloud DR first-class, break-glass quarterly testing, recovery does not introduce vulnerabilities, post-recovery baseline validation)
- Tier framework summary table
- 7 backup/replication principles (3-2-1 baseline, immutability, restore-tests-not-backup-tests, replication-for-RTO-backup-for-RPO, third-party SaaS shared responsibility)
- 6 cloud platform DR principles (paired-region default, tenant-lockout-as-designed-scenario, tenant-compromise-recovery-path, M365-sustained-outage-communications-fallback)
- 10 roles & responsibilities

### `grc-bcdr-wi-01.html` — Conducting a BIA
- 9-step procedure from team establishment through Steering Committee submission
- Impact assessment across 5 dimensions × 6 time horizons with 5-point rubric
- Dependency mapping covering IT services, data, suppliers, sites, people, upstream processes
- 6 common pitfalls

### `grc-bcdr-wi-02.html` — Exercise & Testing Programme
- 10-step procedure from annual scheduling through lessons-learned feedback
- "EXERCISE" tagging discipline on all communications; pause-for-real-events rule
- Hot-wash within 30 minutes; formal AAR within 14 days; plan update within 90 days
- Findings severity classification; overdue escalation to Steering Committee
- 7 common pitfalls

## Boundaries explicitly documented (non-duplication)

This delivery does **not** duplicate:

- **`grc-irp-01.html`** + IRP suite — cyber incident response. BCDR engages alongside when continuity is invoked.
- **`SOP-ID-01`** / SOC suite — identity threat response. Tenant lockout *response* stays in SOC; recovery-to-operations after tenant compromise lives in `GRC-DR-WI-02` (second pass).
- **`it-cl-wi-03.html` / `it-cl-wi-04.html`** — cloud resilience design (paired regions, AZs, GZRS). DR uses those patterns; doesn't re-author them.
- **`IT-SRV-WI-*`** — server backup configuration.
- **`grc-register-risk.html`** — BCDR risks captured in the existing risk register; no new register.

## Structural validation

- All 7 new files pass div/span/tr/td/a balance checks (clean).
- Maintenance files: div/span/tr/td/a tag balances preserved; 4 of 5 HTML maintenance files have the inherited duplicate-`</body>` quirk that pre-exists in the baseline (noted in the 11 May 2026 change-log entry) — not introduced by these edits.
- `search-index.json` validates as JSON; 226 entries; no duplicate IDs.

## Pending in second-pass delivery (6 files, separate request)

| File | Code | Purpose |
|---|---|---|
| `grc-dr-wi-01.html` | GRC-DR-WI-01 | Recovery Tier Classification — assigning services to T1-4, backup/replication minima per tier |
| `grc-dr-wi-02.html` | GRC-DR-WI-02 | Cloud Platform DR — Azure region failure, M365 outage, Entra tenant lockout/compromise |
| `grc-dr-wi-03.html` | GRC-DR-WI-03 | Worked Example — populated DR plan for identity/email/file/network/EDR |
| `grc-frm-bcp-01.html` | GRC-FRM-BCP-01 | Business Process Continuity Plan template |
| `grc-frm-bcdr-01.html` | GRC-FRM-BCDR-01 | BIA worksheet template |
| `grc-frm-dr-01.html` | GRC-FRM-DR-01 | DR Runbook template |

## Future follow-up after second pass

- **MITRE mapping update** in `tools-references.html` to include the impact-class techniques BCDR principally mitigates: T1485 (Data Destruction), T1486 (Data Encrypted for Impact), T1490 (Inhibit System Recovery); mitigation M1053 (Data Backup).

## Upload

Upload all 13 files to the GitHub Pages repository root (or replace existing files at the root for maintenance updates). The 7 new files have no dependencies beyond the existing shared CSS / JS files already present.
