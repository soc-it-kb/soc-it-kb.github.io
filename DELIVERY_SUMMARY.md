# Security Infrastructure Baselines — Delivery Summary

**Date:** 11 May 2026
**Owner:** Paulo Ferreira
**Domain:** ASM — Security Infrastructure Baselines (sixth ASM domain)

## What's delivered

A complete new ASM sub-domain covering Web Application Firewalls, load balancers, and Privileged Access Management platforms — the three classes of high-value security-infrastructure that the Network Device Baselines domain explicitly deferred. Six new content files + five maintenance files.

### New content files (6)

| File | Type | Purpose |
|---|---|---|
| `asm-security-infrastructure-baselines.html` | Domain hub | Peer to the five existing ASM domain hubs; scope, device-type overview, framework alignment, roles, metrics, exception handling |
| `it-si-sop-01.html` | SOP | 7-section policy-level baseline with 4 device-type req-domains and 7 baseline principles |
| `it-si-wi-01.html` | WI | **Common Management Plane & Logging** — 10 steps; shared foundation referenced by WI-02/03/04 |
| `it-si-wi-02.html` | WI | **WAF Hardening** — 8 steps; OWASP Top 10 + CRS coverage, monitor-then-block, FP triage SLA |
| `it-si-wi-03.html` | WI | **Load Balancer Hardening** — 8 steps; TLS, cert lifecycle, HSTS, source-IP preservation, HA |
| `it-si-wi-04.html` | WI | **PAM Platform Hardening** — 10 steps; vault encryption, session recording integrity, JIT access, **vault-independent break-glass procedure** |

### Maintenance files (5)

| File | Change |
|---|---|
| `search-index.json` | 199 → 205 entries (+6 SI entries) |
| `index.html` | Total pages 199→205; WIs 65→69; SOPs 29→30; ASM 74→80; ASM Highlight description and ASM card updated; sixth ASM domain link (`.si` amber palette); footer 9→11 May |
| `search.html` | Page count 199 → 205 |
| `asm.html` | Stats 5→6 domains, 13+→14+ SOPs, 13→17 WIs; sixth domain card with amber palette (`.security-infra`); missing `.network .domain-card-footer` colour rule fixed in same pass |
| `governance.html` | Inventory date 9→11 May; total 206→212; ASM domain pages 7→8; ASM SOPs 16→17; ASM WIs 48→52; breakdown table consolidated (added Network row that was missing + new SI row); new 11 May 2026 changelog entry; meta-pill date 4→11 May; footer 6→11 May |

## Design decisions

The three earlier ask_user_input_v0 choices shaped the domain:

1. **WAF scope: vendor-agnostic for both on-prem and cloud-managed**, with callout that cloud-WAF tenant-platform integration specifics defer to the future Cloud Baselines domain. Same vendor-agnostic discipline as the network domain — controls in vendor-neutral terms, no per-vendor steps.

2. **PAM included in this domain** (not deferred to a future Identity domain). Rationale: PAM platform hardening is genuinely security-infrastructure work and shares much of its baseline with WAF/LB. Identity *governance* aspects (rotation cadences, JIT approval workflows, recording retention policy) explicitly deferred to the future Identity domain SOP — boundary documented in scope notes.

3. **Reverse proxies and API gateways deferred** to a future Application Delivery sub-domain, with a scope-notes callout. Avoided the temptation to force-fit them into the LB WI; the operational reality is different enough to warrant separate treatment when the time comes.

## Structural shape

Unlike the network domain — where switches/routers/firewalls/wireless APs share a common control-domain structure (management/control/data/etc.) — WAF/LB/PAM have distinct architectures. The domain is therefore organised by **device type** with a **shared common-management-plane WI** (IT-SI-WI-01) that the other three reference, rather than by control domain. Each device-type WI covers what's genuinely unique to that platform class.

The shared-WI approach means:
- The common controls (AAA, MFA, syslog, NTP, change control) live in one place, not three near-identical copies
- A change to the shared controls updates one document
- Each device-type WI stays focused on what's actually unique

## Framework alignment

Lighter on vendor-specific CIS benchmarks than the network domain, since CIS coverage of WAFs and PAM is partial. The baselines lean more on:

- **OWASP** for WAFs (Top 10, ASVS v4 L2 minimum, CRS v4.x paranoia 2+)
- **NIST 800-63B** for PAM (AAL2 minimum; **AAL3 for Tier 0 PAM admin access** — explicit step-up requirement)
- **NIST 800-52 r2** for TLS configuration on load balancers
- **CIS F5 BIG-IP** Level 1 where the platform is F5
- **NIST CSF 2.0**, NIST 800-53 r5, ISO 27001:2022, PCI DSS v4.0 cross-domain

For non-F5 platforms, the vendor's published hardening guide combined with the NIST 800-53 control families substitutes for the missing CIS-equivalent benchmark.

## The one control that's worth emphasising

The SOP and WI-04 both call this out with a `callout-warn`: **the single most common failure pattern in PAM deployment is a non-existent or untested break-glass procedure.** When the PAM platform is unreachable and the only documented credentials are stored in it, recovery is a vendor support case at best and a major incident at worst. WI-04 Step 7 specifies the procedure: documented, vault-independent storage, named approvers with documented escalation, annual test under controlled conditions, post-test credential rotation, with explicit anti-patterns (break-glass credentials that themselves get auto-rotated; storage that depends on PAM; single-person break-glass).

## Vendor-agnostic discipline

The estate spans CyberArk, BeyondTrust, Delinea, HashiCorp Vault for PAM; F5, Citrix, HAProxy, NGINX Plus, A10, AVI for load balancers; F5 ASM, Imperva, FortiWeb, Cloudflare, Azure Front Door, AWS WAF for WAFs. Vendor-specific WIs would force false standardisation across 30+ countries. The baselines describe controls in vendor-neutral terms (what the control achieves, what feature implements it, acceptance criteria, vendor-doc pointer); the operating units apply the platform-specific steps using their vendor's hardening guide as reference.

## Validation

All 6 new files structurally balanced:

| File | Lines | div | tr | table |
|---|---|---|---|---|
| `asm-security-infrastructure-baselines.html` | 288 | 94/94 | 10/10 | 1/1 |
| `it-si-sop-01.html` | 359 | 66/66 | 11/11 | 1/1 |
| `it-si-wi-01.html` | 406 | 111/111 | 14/14 | 1/1 |
| `it-si-wi-02.html` | 371 | 94/94 | 11/11 | 1/1 |
| `it-si-wi-03.html` | 369 | 94/94 | 12/12 | 1/1 |
| `it-si-wi-04.html` | 443 | 112/112 | 13/13 | 1/1 |

All 5 maintenance files structurally balanced; all counter values internally consistent.

## Deployment

Replace these 11 files in the `soc-it-kb.github.io` repository root:

```
asm-security-infrastructure-baselines.html   (new)
it-si-sop-01.html                            (new)
it-si-wi-01.html                             (new)
it-si-wi-02.html                             (new)
it-si-wi-03.html                             (new)
it-si-wi-04.html                             (new)
search-index.json                            (replace, 205 entries)
index.html                                   (replace)
search.html                                  (replace)
asm.html                                     (replace)
governance.html                              (replace)
```

Flat repo structure — all files at root, same as previous deliveries.

## Follow-ups (not for this session)

- **Cloud Baselines domain** (M365 + Azure CIS Foundations) — next priority. Will pick up the cloud-WAF tenant-platform integration aspects this domain deferred.
- **Application Delivery sub-domain** — reverse proxies (NGINX as RP, standalone HAProxy), API gateways (Kong, Apigee, Azure APIM, AWS API Gateway). Lower priority than Cloud Baselines.
- **Identity domain SOP** — will absorb the PAM identity-governance aspects this domain explicitly deferred (rotation cadences, JIT approval policy, recording-retention policy).
- Six broken link targets from the earlier sweep.
- Tabletop exercise scenarios pack, BCP/DRP plans, the FRM-12-model migrations, Asset Onboarding Form (pending FRM-12-or-not lock).
- Azure Static Web Apps migration (Phase 1) / GRC app on Azure (Phase 2).
