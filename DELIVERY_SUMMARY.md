# Network Device Security Baselines — Delivery Summary

**Date:** 9 May 2026
**Owner:** Paulo Ferreira
**Domain:** ASM (Attack Surface Management)
**Status:** Approved · Live

---

## What this delivery is

A complete vendor-agnostic baseline methodology for network devices across all operating units — switches, routers, firewalls, wireless access points and controllers — published as a new ASM domain sitting as a full peer alongside Patch Management, Vulnerability Management, Threat Intelligence, and the existing endpoint/server Security Baselines.

This closes the longest-standing gap in the ASM domain coverage. Until today there were no organisation-level security baselines for network devices.

## Why vendor-agnostic

The agencies' estate is mixed: different vendors (Cisco IOS XE, NX-OS, Juniper Junos, Palo Alto, Check Point, various wireless platforms), different generations, different operating units making different choices. Vendor-specific work instructions would force a false standardisation; engineers in a Juniper-heavy site would have nothing useful to follow if all the documents used Cisco syntax, and vice versa.

The discipline applied throughout: **describe the control, not the syntax**. Each step specifies what the control achieves, what feature implements it (in vendor-neutral terms), the acceptance criteria, and a pointer to vendor documentation or the relevant CIS benchmark. An engineer with their vendor's hardening guide and this WI can apply the control without ambiguity.

## Why organised by control domain

The baseline is split into six control domains rather than by device type. The rationale: a managed switch, router, firewall, and wireless AP all have a management plane. They all forward or filter traffic. They all need configuration management. Organising the baseline by *what is being protected* rather than by *which vendor's syntax to use* keeps the controls portable across the mixed estate and gives engineers a stable conceptual map regardless of vendor.

This is also closer to how CIS structures its benchmarks internally — by control category, not just by section number.

## Files in this delivery

### New files (8)

| File | Lines | Purpose |
|---|---|---|
| `asm-network-baselines.html` | 311 | Network domain hub page, peer to other ASM domains |
| `it-net-sop-01.html` | 392 | Network Device Security Baseline — the policy-level SOP |
| `it-net-wi-01.html` | 370 | Management Plane Hardening WI (8 steps) |
| `it-net-wi-02.html` | 352 | Control Plane Hardening WI (8 steps) |
| `it-net-wi-03.html` | 353 | Data Plane Hardening WI (8 steps) |
| `it-net-wi-04.html` | 394 | Wireless Hardening WI (10 steps) |
| `it-net-wi-05.html` | 400 | Firewall Hardening WI (10 steps) |
| `it-net-wi-06.html` | 352 | Configuration Management & Change Control WI (8 steps) |

**Total new content:** ~2,924 lines of authored HTML; 8 documents; 52 prescriptive procedural steps across the six WIs.

### Maintenance updates (5)

| File | Change |
|---|---|
| `search-index.json` | 191 → 199 entries (+8 for new files) |
| `index.html` | Counters bumped: Total pages 191→199; Work Instructions 59→65; SOPs 28→29; ASM pages 66→74 |
| `search.html` | "Search across N pages" 191→199 |
| `asm.html` | New "Network Device Baselines" domain card added (5th domain); ASM stats updated: 4→5 domains, 12+→13+ SOPs, 7→13 WIs; new `.domain-card.network` CSS variant (teal/cyan palette to differentiate from existing four) |
| `governance.html` | Inventory date 8→9 May; counters bumped (Total 198→206, ASM domain pages 6→7, ASM SOPs 15→16, ASM WIs 42→48); new 9 May 2026 changelog entry with full delivery description |

---

## Structure summary

### IT-NET-SOP-01: Network Device Security Baseline

Seven sections:

1. **Purpose** — why this baseline exists; the unique impact of network-device weaknesses.
2. **Scope** — in: switches, routers, firewalls, wireless, OOB management. Out: WAFs/LBs (future Security Infrastructure domain), endpoints (other ASM domain), servers (other ASM domain).
3. **Baseline Principles** — seven principles: defence in depth; least privilege; strong authentication; secure protocols only; segmentation by purpose; configuration as documented state; comprehensive centralised logging.
4. **Minimum Security Requirements** — six control-domain requirement boxes (Management / Control / Data / Wireless / Firewall / Config Management), each operationalised by a dedicated WI. Ends with a "default-deny is not a discussion" callout.
5. **Roles & Responsibilities** — IT Operations Lead, Network Engineering, SOC, GRC, Local IT, Architecture/Technical Authority; separation-of-duties callout.
6. **Framework Alignment** — full table mapping the baseline to 7 CIS benchmarks + NIST CSF 2.0 + NIST 800-53 r5 + ISO 27001:2022 + BCP 38.
7. **Governance & Review** — ownership, review cadence, exception handling, compliance & audit, related documents.

### The six Work Instructions

Each WI follows the same proven pattern (consistent with earlier WI work in the KB):

- **Prerequisites** — what must be in place before starting; includes a `callout-warn` for the highest-risk gotcha
- **Step-by-step instructions** — numbered step boxes with title, objective, body, verification, and CIS reference tag
- **Validation & verification** — functional validation list + configuration review table
- **Rollback & troubleshooting** — common scenarios with root cause + fix; rollback procedure
- **Common errors & tips** — bulleted reality-check on the most common mistakes

#### WI step counts and key coverage:

- **WI-01 Management Plane (8 steps):** disable plaintext (Telnet/HTTP/SNMPv1v2/FTP); enable secure protocols (SSHv2, TLS 1.2+, SNMPv3 authPriv); AAA with MFA; management ACL; timeouts/banners; NTP with authentication; centralised syslog; console hardening.
- **WI-02 Control Plane (8 steps):** routing-protocol authentication (OSPF/EIGRP/BGP/IS-IS); CoPP; spanning-tree protection (BPDU Guard, Root Guard, Loop Guard); storm control; uRPF/BCP38; DAI + IPv6 RA Guard; unused-protocol disable; route filtering at boundaries.
- **WI-03 Data Plane (8 steps):** unused-port discipline; port security; VLAN hygiene (native VLAN non-default, trunk allow-list); DHCP snooping; inter-VLAN filtering; segment isolation (guest/IoT/OT); L2 service hygiene (CDP/LLDP/VTP); private VLANs.
- **WI-04 Wireless (10 steps):** disable WEP/TKIP/WPS; WPA3/WPA2-Enterprise with 802.1X; PMF (802.11w); guest isolation; rogue-AP detection; WIDS/WIPS; RF management; SSID hygiene; dynamic VLAN assignment; logging to SIEM.
- **WI-05 Firewall (10 steps):** default-deny; rule documentation & ownership; egress filtering; stale-rule lifecycle (90/180 day); geo-blocking; IPS/AV; TLS inspection policy; Layer-7 controls; anti-evasion; HA with annual failover test.
- **WI-06 Configuration Management (8 steps):** golden config per device class; automated backups (daily T0/T1, weekly T2/T3; 90/30-day retention; annual restore test); change control workflow (standard/normal/emergency); drift detection; firmware/OS lifecycle; secure decommissioning per GRC-SOP-05 §12; lab isolation; OOB infrastructure in scope.

---

## Framework alignment

| Framework / benchmark | Reference | Coverage |
|---|---|---|
| CIS Cisco IOS XE Benchmark | Level 1 | Catalyst switches & routers |
| CIS Cisco NX-OS Benchmark | Level 1 | Nexus data-centre switches |
| CIS Cisco IOS XR Benchmark | Level 1 | Service-provider routers |
| CIS Juniper Junos OS Benchmark | Level 1 | Junos switches, routers, firewalls |
| CIS Palo Alto Firewall Benchmark | Level 1 | PAN-OS firewalls |
| CIS Check Point Firewall Benchmark | Level 1 | Check Point Gaia firewalls |
| CIS Wireless LAN Benchmark | Level 1 | Wireless controllers & APs |
| NIST CSF 2.0 | PR.AC, PR.DS, PR.PT, DE.CM | Identity & access, data security, protective tech, monitoring |
| NIST SP 800-53 r5 | AC, AU, CM, IA, SC families | Cross-domain reference |
| ISO/IEC 27001:2022 | A.5.15, A.8.16, A.8.20, A.8.21, A.8.22, A.8.23 | Access control, networks security, segregation, web filtering, monitoring |
| BCP 38 / RFC 2827 | Anti-spoofing | Control plane (WI-02) |

### CIS attribution choice

The CIS attribution is **lighter** than the previous endpoint/server work — per-control-domain references in the SOP framework section, paraphrased in WIs (not per-step CIS IDs).

This was a deliberate choice: vendor-specific CIS IDs (e.g. "Cisco IOS XE 1.1.1") would not portably apply across the mixed estate. A control mapped to Cisco's §1.1.1 may map to Juniper's §2.4.3 for the same concept. Forcing per-step IDs would either fix the document to one vendor (defeating vendor-agnosticism) or create attribution that's accurate for some readers and misleading for others.

The chosen pattern names the relevant CIS control category in each WI step (e.g. "Mgmt-plane disable insecure services") which an auditor can find in any vendor's CIS benchmark for the same concept.

---

## What's deferred to future deliveries

### Security Infrastructure baselines (future domain)

Web Application Firewalls (WAFs), load balancers, and Privileged Access Management (PAM) appliances are network-adjacent but distinct enough to deserve their own sub-domain rather than being shoe-horned into the network baselines:

- WAFs are an application-security tool, not a network tool; their baseline is closer to that of an application gateway than a perimeter firewall.
- Load balancers (whether F5, Citrix, or HAProxy) have a distinct control profile.
- PAM appliances (CyberArk, BeyondTrust, etc.) have a distinct identity and credential-vault control profile.

The network-baselines hub explicitly notes this scope boundary so readers know where to expect the missing controls.

### Cloud Baselines (future domain)

Microsoft 365 and Azure each have their own CIS Foundations Benchmarks and benefit from their own dedicated baseline domain. The network baselines hub notes this as out-of-scope and a follow-up.

### Vendor-specific WIs (optional follow-up if needed)

The vendor-agnostic baseline can be supplemented later with vendor-specific WIs (e.g. "IT-NET-WI-CISCO-IOSXE-01: applying WI-01 on Cisco IOS XE devices") if the operating units want CLI-level specificity. This wasn't done in this delivery because the framework would be premature without operational feedback on the vendor-agnostic baseline first.

---

## Quality / structural validation

All 12 HTML files in the delivery were validated for HTML balance:

| File | Lines | `<div>` | `<tr>` | `<table>` |
|---|---|---|---|---|
| asm-network-baselines.html | 311 | 105/105 ✓ | 11/11 ✓ | 1/1 ✓ |
| it-net-sop-01.html | 392 | 70/70 ✓ | 12/12 ✓ | 1/1 ✓ |
| it-net-wi-01.html | 370 | 95/95 ✓ | 13/13 ✓ | 1/1 ✓ |
| it-net-wi-02.html | 352 | 94/94 ✓ | 9/9 ✓ | 1/1 ✓ |
| it-net-wi-03.html | 353 | 93/93 ✓ | 11/11 ✓ | 1/1 ✓ |
| it-net-wi-04.html | 394 | 110/110 ✓ | 11/11 ✓ | 1/1 ✓ |
| it-net-wi-05.html | 400 | 110/110 ✓ | 11/11 ✓ | 1/1 ✓ |
| it-net-wi-06.html | 352 | 94/94 ✓ | 11/11 ✓ | 1/1 ✓ |
| asm.html (updated) | 268 | 95/95 ✓ | — | — |
| index.html (updated) | 266 | 78/78 ✓ | — | — |
| search.html (updated) | 225 | 42/42 ✓ | — | — |
| governance.html (updated) | 338 | 168/168 ✓ | 35/35 ✓ | 2/2 ✓ |

`search-index.json`: 199 entries, valid JSON.

---

## Deployment

1. Replace existing files at the soc-it-kb.github.io repo root with the versions in this delivery:
   - `asm.html`, `index.html`, `search.html`, `search-index.json`, `governance.html`
2. Add the new files at the repo root:
   - `asm-network-baselines.html`
   - `it-net-sop-01.html`
   - `it-net-wi-01.html` through `it-net-wi-06.html`
3. Commit; GitHub Pages will deploy on push.
4. No other files in the repo need to change as part of this delivery (no broken-link sweep was triggered).

---

## Next sessions (in priority order)

1. **Security Infrastructure baselines** — WAF, load balancers, PAM. Likely similar shape: hub + SOP + WIs by device-type rather than control-domain (smaller scope, more vendor-specific).
2. **Cloud Baselines** — M365 Foundations + Azure Foundations. Larger scope; potentially split into two sub-domains.
3. Tabletop exercise scenarios pack (GRC-TTX-01..NN).
4. BCP / DRP plans.
5. Vendor-specific network WIs (only if operational feedback indicates a need).
