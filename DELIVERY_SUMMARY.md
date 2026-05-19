# TTX (Tabletop Exercise) Library — Delivery Summary

**Session date:** 15 May 2026  
**Author:** Paulo Ferreira  
**Scope locked via three decisions:**
1. Combined library covering BCDR + cyber scenarios under one TTX domain
2. Reusable template (GRC-FRM-TTX-01) plus 5 worked-example scenarios alongside it
3. Mixed pack — some executive, some technical, clearly labelled by audience
4. New bronze accent palette for visual distinctness as exercise / rehearsal content
5. Full retro-fit of grc-bcdr-wi-02 with a "Pre-built scenarios" section linking to the library

---

## Files in this delivery (13 total)

### 7 new TTX files

| File | Code | Type | Lines | Chars |
|---|---|---|---:|---:|
| `grc-frm-ttx-01.html` | GRC-FRM-TTX-01 | Scenario authoring template | 361 | 23,565 |
| `grc-ttx-01.html` | GRC-TTX-01 | Scenario — Ransomware affecting clinical systems | 381 | 28,317 |
| `grc-ttx-02.html` | GRC-TTX-02 | Scenario — Entra tenant compromise | 352 | 27,485 |
| `grc-ttx-03.html` | GRC-TTX-03 | Scenario — Regional disaster: sustained site evacuation | 346 | 25,856 |
| `grc-ttx-04.html` | GRC-TTX-04 | Scenario — Critical SaaS provider sustained failure | 323 | 24,127 |
| `grc-ttx-05.html` | GRC-TTX-05 | Scenario — Azure region failure during business-critical period | 340 | 25,316 |
| `grc-ttx.html` | (hub) | TTX library hub | 257 | 18,051 |

### 1 modified file (retro-fit)

| File | Change |
|---|---|
| `grc-bcdr-wi-02.html` | New "Pre-built scenarios available" section before Related documents; library + template added to Related documents |

### 5 maintenance files

| File | Change |
|---|---|
| `search-index.json` | 233 → 240 entries (7 new); new "Tabletop Scenarios" sub-category for the 5 scenarios |
| `index.html` | Total pages 233 → 240; GRC pages 50 → 57 |
| `grc.html` | Forms 11 → 12; new "Tabletop scenarios 5" stat; Domains 5 → 6; new bronze TTX domain card with bronze palette; new "Rehearse a scenario" use-case card |
| `governance.html` | GRC Hub Domain pages 6 → 7 (Tabletop Exercises named); GRC Forms 11 → 12 (FRM-TTX-01 named); new "GRC Tabletop Scenarios" row with all 5 TTX codes; Total pages 212 → 240, GRC pages 37 → 57 (stale-baseline drift from prior deliveries corrected as a bonus); new TTX change-log entry as most recent |
| `search.html` | Page count 233 → 240 |

---

## Audience distribution

| Audience | Count | Scenarios |
|---|---:|---|
| Mixed | 2 | TTX-01 (Ransomware clinical), TTX-04 (SaaS provider failure) |
| Technical | 2 | TTX-02 (Entra tenant compromise), TTX-05 (Azure region failure) |
| Executive | 1 | TTX-03 (Regional disaster) |

Audience badges colour-coded across the library: amber for executive, blue for technical, purple for mixed.

---

## Category distribution

| Category | Count | Scenarios |
|---|---:|---|
| Cyber + BCDR (hybrid) | 2 | TTX-01, TTX-04 |
| Cyber | 1 | TTX-02 (identity) |
| BCDR | 1 | TTX-03 (natural disaster) |
| Cloud DR | 1 | TTX-05 |

---

## Palette decision

Bronze accent (Option C) chosen for the TTX series:
- Main: `#A0612A`
- Light: `#F5E8DD`
- Border: `#E0BB99`
- Dark: `#6B3F15`
- Hero gradient: `#2D1808 → #6B3F15 → #A0612A`

This is the 9th visual palette in the KB, distinct from existing 8:
1. GRC teal (`#0E5C5C`) — governance / policy / compliance core
2. BCP forest-green warm (`#2D6B3F`) — business continuity
3. DR forest-green cool / teal (`#1F5A4A`) — IT disaster recovery
4. ASM purple (`#5B2D8E`) — attack surface management family
5. Network teal-blue — network device baselines
6. Security Infrastructure amber/orange — WAF / LB / PAM
7. Cloud slate-blue (`#2E5C8A`) — cloud baselines
8. Identity rose-pink (`#8B2D5C`) — identity governance
9. **TTX bronze (`#A0612A`)** — exercise / rehearsal content (this delivery)

The bronze signals "rehearsal / exercise" content distinct from policy, methodology, and operations — supporting the audience-level scanning of the KB.

---

## Boundaries explicitly preserved

The TTX delivery does NOT duplicate:
- `grc-bcdr-wi-02` exercise methodology — TTX provides scenarios; WI provides how to scope, sequence, and run exercises
- `grc-irp-01` + IRP suite — cyber incident response; TTX scenarios test it but do not re-author it
- `SOP-ID-01` + SOC suite — identity threat ops; TTX-02 references these
- `DR-WI-02` cloud DR — TTX-02 / 04 / 05 exercise specific scenarios from that WI
- `grc-frm-14` IR communication templates — referenced where applicable

---

## Suggested rotation guidance (from the hub page)

The BCDR Exercise programme (per GRC-BCDR-WI-02) requires Tier-1 services and processes to be exercised annually. The 5 scenarios above are not all run every year — a healthy rotation:

- **Annually rotate** across scenario types (cyber, BCDR, hybrid) so the portfolio is exercised over a 2-3 year window
- **After any major change** to a relevant document or capability, re-run the relevant scenario to validate the change
- **After a near-miss or real event**, use the relevant scenario to extract additional learning beyond the AAR
- **Combine scenarios occasionally** — e.g. TTX-03 + TTX-04 for a regional-disaster-that-causes-supplier-disruption multi-day exercise; this is realistic and tests sustained capability

---

## Bonus correction in this delivery

Discovered that `governance.html` inventory stats had drifted: Total pages was at 212 (stale from May 12) and GRC pages at 37 (stale from May 8) despite intervening Identity Governance, BCDR-1, BCDR-2, and Glossary deliveries. Corrected to current accurate values (240 and 57 respectively) as part of this maintenance pass. The earlier inventory-grid cards in governance.html are a separate stats surface from the change-log entries below them and were not being updated by individual deliveries — flag for ongoing discipline.

---

## Pending follow-ups (carried, NOT in this delivery)

1. MITRE mapping for BCDR impact-class techniques on `tools-references.html` — T1485 Data Destruction, T1486 Data Encrypted for Impact, T1490 Inhibit System Recovery; mitigation M1053 Data Backup. Natural next pass.
2. Two separate "Forms" and "Forms & Templates" subs in `search-index.json` under GRC — candidate for consolidation
3. The earlier glossary trim option from 140 → ~123 (drop document-class prefixes, 800-53 family abbreviations, agency codes) if user requests
4. Optional: a tabletop "facilitator pack" — printable / PDF version of selected scenarios — has been mentioned as future possibility

---

## Structural validation

All 12 HTML files plus the JSON pass tag-balance and JSON-validity checks. No structural issues introduced.

---

## What the library gives agencies

Before this delivery, agencies had the methodology to run tabletop exercises (per GRC-BCDR-WI-02) but no starting scenarios — they had to author from scratch. With this delivery they have:

- **Run as-is**: 5 worked examples covering the most realistic scenarios for AKDN agencies (ransomware on clinical, identity compromise, regional disaster, supplier breach, Azure region loss). Each is populated with realistic injects, discussion prompts, expected decisions, evaluation criteria, and AAR framework.
- **Adapt**: change inject content, swap named SaaS / region / process, or extend with additional injects using the same structure.
- **Author new**: use GRC-FRM-TTX-01 template for scenarios specific to the agency's estate.

The Exercise Programme can now begin executing immediately without bottlenecking on scenario authoring.
