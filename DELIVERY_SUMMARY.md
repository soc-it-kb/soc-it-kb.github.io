# MITRE ATT&CK Refresh — Delivery Summary

**Session date:** 15 May 2026
**Author:** Paulo Ferreira
**Scope locked via two decisions:**
1. Deferred set only — BCDR (T1485, T1486, T1490, M1053) + Identity (T1136, T1078, T1098, T1484)
2. tools-references.html only; back-injection of technique IDs into individual PB/RB/WI content remains a separate follow-up pass

---

## Files in this delivery (5 total)

| File | Change |
|---|---|
| `tools-references.html` | Section title broadened; tactic cards augmented for TA0001 / TA0003 / TA0004 / TA0008 / TA0040; new Mitigations section; coverage validation matrix updated; technique drill-down table extended; `+MIT` tag style introduced |
| `search-index.json` | 240 → 241 entries (new entry for tools-references.html itself — closes pending follow-up #14) |
| `index.html` | Total pages 240 → 241 |
| `search.html` | Page count 240 → 241 |
| `governance.html` | Total pages 240 → 241; new change-log entry as most recent |

---

## What was added — by tactic

### TA0001 Initial Access
| Technique | Change |
|---|---|
| T1078 Valid Accounts | **Augmented:** IT-ID-WI-01, IT-ID-WI-02, IT-ID-WI-05 added as governance refs |

### TA0003 Persistence
| Technique | Change |
|---|---|
| T1136 Create Account | **Augmented:** IT-ID-WI-01 (JML Lifecycle) added |
| T1136.003 Cloud Account | **New entry:** linked to IT-ID-WI-01, IT-CL-WI-01 |
| T1098 Account Manipulation | **New entry:** linked to ID-PB-03 + IT-ID-WI-02, IT-ID-WI-05 |
| T1098.001 Additional Cloud Credentials | **New entry:** linked to ID-PB-03 + IT-ID-WI-04, IT-ID-WI-05, IT-CL-WI-01 |
| T1098.003 Additional Cloud Roles | **New entry:** linked to ID-PB-03 + IT-ID-WI-02, IT-ID-WI-05, IT-CL-WI-01 |

### TA0004 Privilege Escalation
| Technique | Change |
|---|---|
| T1078 Valid Accounts | **Augmented:** IT-ID-WI-05, IT-ID-WI-02 added |
| T1078.004 Valid Accounts: Cloud | **New entry:** linked to ID-PB-02 + IT-ID-WI-05, IT-CL-WI-01 |
| T1484 Domain or Tenant Policy Modification | **New entry:** linked to ID-PB-03 + IT-ID-WI-05, IT-CL-WI-01, IT-SRV-WI-DC-01 |

### TA0008 Lateral Movement
| Technique | Change |
|---|---|
| T1078 Valid Accounts | **Augmented:** IT-ID-WI-02, IT-ID-WI-05 added |
| T1078.002 Valid Accounts: Domain | **New entry:** linked to ID-PB-02 + IT-ID-WI-02, IT-ID-WI-05, IT-SRV-WI-DC-01 |

### TA0040 Impact
| Technique | Change |
|---|---|
| T1485 Data Destruction | **New entry:** linked to EP-PB-05 + GRC-DR-SOP-01, GRC-DR-WI-01 |
| T1486 Data Encrypted for Impact | **Augmented:** GRC-DR-SOP-01, GRC-DR-WI-01, GRC-FRM-DR-01 added |
| T1490 Inhibit System Recovery | **Augmented:** GRC-DR-SOP-01 (immutable + isolated), GRC-BCDR-WI-02 added |

---

## New section — ATT&CK Mitigations

Six mitigations now table-mapped to their authoritative implementing content:

| Mitigation | Name | Source |
|---|---|---|
| M1018 | User Account Management | IT-ID-SOP-01, IT-ID-WI-01, IT-ID-WI-02 |
| M1026 | Privileged Account Management | IT-ID-WI-05, IT-SI-WI-04, IT-EP-SOP-PAW-01 |
| M1027 | Password Policies | IT-CL-WI-01, IT-SRV-WI-DC-01 |
| M1032 | Multi-factor Authentication | IT-CL-WI-01, IT-ID-WI-05 |
| M1036 | Account Use Policies | IT-ID-WI-04, IT-ID-WI-05 |
| **M1053** | **Data Backup** | **GRC-DR-SOP-01, GRC-DR-WI-01, GRC-FRM-DR-01** |

M1053 is the BCDR-flagged mitigation deferred across two preceding deliveries. The other 5 were natural additions arising from the same audit — the Identity Governance and Cloud Baseline domains had been publishing M1018/M1026/M1027/M1032/M1036 content for weeks without it being visible on the matrix surface.

---

## Architecture decision: `+MIT` tag

Existing tactic cards mixed detection content (PB/RB) and governance content (WIs) without distinction. The refresh introduces a small `+MIT` chip on entries where the listed reference is **preventive / governance** rather than **detective / responsive**.

- **No tag (default):** detection / response content (playbooks, runbooks, IR SOPs)
- **`+MIT` chip (green):** preventive / governance content (WIs, baselines, BCDR SOPs)

Section title broadened from "ATT&CK techniques covered by published playbooks & runbooks" to "ATT&CK techniques covered by published content" to reflect inclusion of preventive material.

---

## Coverage matrix updates

| Tactic | Before | After | Reason |
|---|---|---|---|
| Persistence | Partial | **Covered** | Identity governance T1136 sub-techs + T1098 + T1098.001 + T1098.003 mapped |
| Privilege Escalation | Partial | **Covered** | T1078 + T1078.004 + T1484 mapped |
| Lateral Movement | Covered | Covered (note refined) | T1078.002 governance refs added |
| Impact | Covered | Covered (note refined) | M1053 via GRC-DR-SOP-01 now named |

---

## Technique-level drill-down — new rows

| ID | Name | Tool | Evidence |
|---|---|---|---|
| T1098 | Account Manipulation | IAM, SIEM | Directory audit logs; unsanctioned role/credential grant |
| T1485 | Data Destruction | EDR/XDR, Backup | File/backup logs; mass deletion, shadow-copy removal |
| T1486 | Data Encrypted for Impact | EDR/XDR, Backup | File I/O, backup; ransomware encryption pattern |

---

## Bonus correction

The **search-index entry for tools-references.html** has been a pending follow-up since the page was rebuilt in late April. With this refresh adding new content to the page, it was the natural moment to fix that gap — entry now exists with full tag coverage of every T-code and M-code referenced on the page. Readers searching for "T1486" or "M1053" now land on tools-references.html directly.

---

## Pending follow-ups (carried, NOT in this delivery)

1. **Back-injection of ATT&CK technique IDs** into individual playbook / runbook / WI content — remains a separate discipline pass since it requires per-file analytical work distinct from the matrix update. (Standing item.)
2. **Broader MITRE coverage review** for cloud / network / security-infrastructure baselines — many other techniques addressed by these domains aren't currently in the matrix.
3. **`td.code` misuse sweep** across other GRC/ASM pages
4. **6 broken link targets** from the earlier sweep
5. **FRM-06/08/10 + IRP Annex Template migration** to FRM-12 model
6. **Duplicate "Forms" / "Forms & Templates" subs** in search-index consolidation
7. **Future cloud / network domain extensions** (Application Delivery, multi-cloud, vendor-specific cloud-WAF, Cloud Architecture)

---

## Structural validation

All 4 HTML files plus the JSON pass tag-balance and JSON-validity checks. No structural issues introduced.

---

## What this gives readers

Before this delivery: someone searching the ATT&CK matrix for "what addresses tenant compromise" or "what mitigates ransomware impact" would have found incomplete entries pointing at detection (EDR/XDR via EP-PB-05) without seeing the structural defences in place. The Identity Governance domain (8 weeks old at this point) and the BCDR domain (5 weeks old) had been publishing the actual mitigations without being visible on the canonical surface.

After: the matrix surface reflects what's actually in place. M1053 has a named source. T1485 has a named source. T1098.001 (the technique behind Entra app-registration abuse used as the seed event in TTX-02) has a named source. The matrix now matches the content.
