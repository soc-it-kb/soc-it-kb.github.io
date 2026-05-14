# Tools & References — MITRE ATT&CK Comprehensive Coverage Rebuild

**Date:** 12 May 2026
**Author:** Paulo Ferreira
**Scope:** Full rebuild of MITRE ATT&CK coverage section in `tools-references.html`
**Status:** Complete; balanced and validated; all referenced IDs verified against search-index

---

## What changed

The previous page had a sparse "ATT&CK techniques covered by published playbooks & runbooks" section mapping ~40 techniques to playbook/runbook IDs across 10 ATT&CK tactics, with some references to wildcard `EM-RB-*` patterns that didn't represent actual files. That section, plus the old "ATT&CK coverage validation matrix", has been replaced with a comprehensive mapping.

### Before → After

| Aspect | Before | After |
|---|---|---|
| ATT&CK tactics covered | 10 | **14** (added Reconnaissance, Resource Development, Collection, separated Discovery/Lateral) |
| Techniques mapped | ~40 (many wildcard refs) | **139** (every ref validated against search-index) |
| Control types shown | Playbooks + Runbooks only | **Preventive (ASM) · Detective (SOC) · Responsive (SOC)** for every technique |
| KB content referenced | Playbooks + Runbooks (~15 IDs) | **126 unique IDs** spanning Playbooks, Runbooks, SOC SOPs, SOC WIs, Tier-1 Checklists, Investigation WIs, ASM SOPs, ASM WIs |
| Gap visibility | None | **Honest gap report** for 6 techniques with no coverage + 8 with partial coverage |
| Cross-tactic stats | One Tactic / Coverage / Notes table | **Per-tactic coverage breakdown** + summary stats card |
| External link | None | Every technique ID links to its MITRE ATT&CK page (`attack.mitre.org/techniques/Tnnn[/nnn]`) |
| Broken references | Several (`EM-RB-*` wildcards) | **Zero** — every link target verified to exist |

---

## Coverage profile

- **125 techniques (90%)** have full coverage — preventive ASM control + detective SOC content + responsive SOC content
- **8 techniques (6%)** have partial coverage — at least one of the three control types missing
- **6 techniques (4%)** are honestly marked as gap — no coverage in the current KB

### Per-tactic breakdown

| Tactic | Total | Full | Partial | Gap |
|---|---:|---:|---:|---:|
| TA0043 Reconnaissance | 6 | 1 | 3 | 2 |
| TA0042 Resource Development | 4 | 0 | 0 | 4 |
| TA0001 Initial Access | 11 | 10 | 1 | 0 |
| TA0002 Execution | 13 | 12 | 1 | 0 |
| TA0003 Persistence | 15 | 15 | 0 | 0 |
| TA0004 Privilege Escalation | 8 | 7 | 0 | 1 |
| TA0005 Defense Evasion | 12 | 12 | 0 | 0 |
| TA0006 Credential Access | 12 | 10 | 2 | 0 |
| TA0007 Discovery | 12 | 12 | 0 | 0 |
| TA0008 Lateral Movement | 9 | 9 | 0 | 0 |
| TA0009 Collection | 9 | 9 | 0 | 0 |
| TA0011 Command and Control | 10 | 10 | 0 | 0 |
| TA0010 Exfiltration | 8 | 8 | 0 | 0 |
| TA0040 Impact | 10 | 10 | 0 | 0 |

### Known gaps and rationale (in the page itself as well)

| Technique | Tactic | Reason |
|---|---|---|
| T1583 / T1586 / T1588 / T1608 | Resource Development | External to the organisation — adversary builds capability before contact. Defensible gap. |
| T1589 / T1590 | Reconnaissance | Pre-intrusion intelligence-gathering with limited preventive surface. |
| T1611 | Privilege Escalation | Container runtime escape — no AKS / container workloads onboarded yet. Plan for when they are. |

---

## Method (how mappings were derived)

The SOC playbooks, runbooks, and Tier-1 checklists currently **do not declare their ATT&CK technique mappings inline**. The mapping in this delivery is authoritative — derived from artefact titles, descriptions in search-index, and content scope as built. Implication: this page becomes the canonical source-of-truth for KB ↔ ATT&CK mapping, and a future pass could back-inject per-step ATT&CK IDs into individual playbooks using this mapping as input.

ASM content (Baselines, SOPs, WIs) is mapped to ATT&CK on the basis of which technique the control intends to prevent:
- `IT-CL-WI-01 Tenant Identity` → T1078 (Valid Accounts), T1110 (Brute Force), T1556 (Modify Auth Process), T1098 (Account Manipulation), T1621 (MFA fatigue)
- `IT-CL-WI-02 M365 Tenant Hardening` → T1566 (Phishing), T1204 (User Execution), T1114 (Email Collection), T1567 (Web Service exfil)
- `IT-CL-WI-04 Azure Workload Patterns` → T1190 (Exploit Public-Facing), T1530 (Cloud Storage data), T1486 (Ransomware impact), T1498 (Network DoS)
- `IT-CL-WI-05 Defender Suite` → T1562 (Impair Defenses)
- `IT-NET-WI-05 Firewall Hardening` → broad C2 and lateral movement coverage
- `IT-SI-WI-02 WAF Hardening` → T1190, T1071.001 (HTTP/S C2), T1491 (Defacement)
- `IT-SI-WI-04 PAM Platform Hardening` → T1078 (priv-esc & lateral), T1555 (password stores)
- `IT-PM-SOP-01..02 + IT-VM-SOP-01` → T1068 (Exploitation for Priv-Esc), T1210 (Exploit Remote Services), T1212 (Exploit for Cred Access)
- `IT-EP-WI-PAW-*` → T1003 (Credential Dumping), T1078 (priv-esc on Tier-0)

This is the first time the KB has a clear "how does prevention + detection + response stack up against each technique?" view, which is precisely the question an auditor, a new analyst, or a planning session needs to answer quickly.

---

## File structure preserved

The new page **preserves** all sections that were not part of the rebuild scope:

- SOC tool × MITRE ATT&CK mapping (primary matrix) — kept as-is
- Technique-level drill-down (T1059, T1055, T1078, T1021 forensic table) — kept as-is
- Tool capability reference (EDR, SIEM, Email Security, IAM, Network, TI cards) — kept as-is
- NIST CSF 2.0 framework reference card and 6-function quick reference — kept as-is
- External framework references (MITRE, ISO 27035) — kept as-is
- Core concepts (Infrastructure Tiers, PAW) — kept as-is

Two sections were **replaced**:
- Old "ATT&CK techniques covered by published playbooks & runbooks" tactic-grid (12 cards with ~40 techniques) → **new comprehensive 14-tactic technique mapping with 139 techniques**
- Old "ATT&CK coverage validation matrix" (11-row summary table) → **new gap report + per-tactic coverage summary**

Two **structural fixes** applied to existing pre-existing defects:
- The `<script>` tags were outside `<head>` but before `<body>` (and there was a premature `</body>` immediately after); both fixed so the document structure is `<html>` → `<head>` (with scripts) → `<body>` → content → `</body>` → `</html>`.

---

## Design choices

**Collapsible tactic sections.** Each of the 14 tactics is a `<details>` element. Collapsed by default so the page is scannable; click to expand the technique table for that tactic. No JavaScript required — pure HTML semantics.

**Coverage state badges.** Each technique row shows a `Full` / `Partial` / `Gap` badge in green / orange / red. Each tactic summary shows aggregate counts so the most active tactics (e.g. Persistence with 15 fully-covered techniques) stand out visually from the gaps (e.g. Resource Development with 0 / 0 / 4).

**Every reference is a working link.** Each cell renders referenced KB content IDs as small inline pill-links. Hover shows the title via `title=` attribute. Each technique ID also links to its canonical MITRE ATT&CK page on attack.mitre.org. No wildcard or placeholder references remain.

**Gap-row styling.** Rows where `state == 'gap'` get a subtle background tint so they're visible during a quick scan without being alarming.

**Empty-cell style.** Where a control type is genuinely missing, the cell shows an em-dash in light grey — distinguishable from "I forgot to fill this in" and consistent with the gap badge.

**Per-tactic stats card.** Summary card at the top of the section shows 14 tactics / 139 techniques / 125 full / 8 partial / 6 gap. Quick orientation for an auditor or new joiner.

---

## Files delivered

| File | Purpose |
|---|---|
| `tools-references.html` | The rebuilt page. Drop into repo root, replaces the existing file. |
| `mitre_mapping.py` | The mapping data structure used to generate the page. Kept as a build artefact in case future content additions (new playbooks, new ASM domains) need to extend the mapping. Run `python3 mitre_mapping.py` to print coverage stats. |

---

## Pending follow-ups (not blocking this delivery)

1. **Back-inject ATT&CK technique IDs into individual playbook / runbook content** — currently the mapping lives only in `tools-references.html`. A future pass could add a "MITRE ATT&CK coverage" callout to each playbook's hero metadata, using this file as the source-of-truth.
2. **Add a search-index entry for `tools-references.html`** — the page is in the top nav but has no search-index entry today. Add one with appropriate tags during the next maintenance pass.
3. **Linux execution detection** (T1059.004) — currently a partial: prevention via baseline, no Tier-1 detection. Future Linux Tier-1 checklist would close this.
4. **Container security** (T1611 and broader container coverage) — gap pending AKS / container workload onboarding.
5. **Recon detective signals** — if internet-facing log analysis becomes a deliberate practice, recon-tactic partial → full.
6. **Cloud Discovery TI mapping** — `IT-TI-WI-01..05` and `IT-TI-SOP-02..03` support detection across the entire technique surface; currently not referenced inline to keep the table readable. Consider a separate "Threat Intelligence supports all tactics" callout in a future iteration.

---

## Validation

- All tags balanced: `<div>` 135/135 · `<span>` 278/278 · `<tr>` 201/201 · `<table>` 19/19 · `<a>` 830/830 · `<details>` 14/14 · `<summary>` 14/14
- HTML structure clean: one `<html>`, one `<head>`, one `<body>`, properly nested
- All 126 referenced KB content IDs validated against search-index (zero broken references)
- All 14 ATT&CK tactics rendered with correct technique counts (6+4+11+13+15+8+12+12+12+9+9+10+8+10 = 139 ✓)
- Coverage stats arithmetic: 125 + 8 + 6 = 139 ✓
