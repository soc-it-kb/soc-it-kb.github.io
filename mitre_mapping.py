"""
MITRE ATT&CK technique-to-KB mapping.
Each technique is mapped to:
  - prevent: ASM SOPs/WIs that prevent the technique (preventive controls)
  - detect:  Tier-1 checklists, SOC WIs, Investigation WIs (detective controls)
  - respond: SOC Playbooks, SOC Runbooks, SOC SOPs (responsive controls)

Coverage state per technique:
  - 'full'    = prevent + detect + respond
  - 'partial' = at least one of (prevent, detect, respond) but not all
  - 'gap'     = none

Tactics covered per ATT&CK Enterprise v15 (current):
  TA0043 Reconnaissance, TA0042 Resource Development, TA0001 Initial Access,
  TA0002 Execution, TA0003 Persistence, TA0004 Privilege Escalation,
  TA0005 Defense Evasion, TA0006 Credential Access, TA0007 Discovery,
  TA0008 Lateral Movement, TA0009 Collection, TA0011 Command and Control,
  TA0010 Exfiltration, TA0040 Impact

ASM-WI shortcuts: only the most direct preventive mappings; full ASM-WI list omitted to keep
the rows readable.
"""

TACTICS = [
    ('TA0043', 'Reconnaissance',         'Adversary gathers information about the target before attempting intrusion'),
    ('TA0042', 'Resource Development',   'Adversary establishes resources to support operations (mostly external to the org)'),
    ('TA0001', 'Initial Access',         'Adversary attempts to gain initial foothold in the environment'),
    ('TA0002', 'Execution',              'Adversary runs malicious code on local or remote system'),
    ('TA0003', 'Persistence',            'Adversary maintains access across reboots, password changes, and other interruptions'),
    ('TA0004', 'Privilege Escalation',   'Adversary gains higher-level permissions on a system or network'),
    ('TA0005', 'Defense Evasion',        'Adversary avoids detection by security controls'),
    ('TA0006', 'Credential Access',      'Adversary steals account names and passwords'),
    ('TA0007', 'Discovery',              'Adversary learns about the environment after initial compromise'),
    ('TA0008', 'Lateral Movement',       'Adversary moves through the environment to reach the objective'),
    ('TA0009', 'Collection',             'Adversary gathers information relevant to the objective'),
    ('TA0011', 'Command and Control',    'Adversary communicates with compromised systems to control them'),
    ('TA0010', 'Exfiltration',           'Adversary steals data from the environment'),
    ('TA0040', 'Impact',                 'Adversary disrupts availability or compromises integrity of systems and data'),
]

# Mapping: { 'TA0001': [ (tech_id, tech_name, prevent_list, detect_list, respond_list), ... ], ... }
MAPPING = {

    # ============================================================
    # TA0043 Reconnaissance — adversary gathers info BEFORE intrusion
    # ============================================================
    'TA0043': [
        ('T1595',     'Active Scanning',
            ['IT-NET-WI-05', 'IT-SI-WI-02', 'IT-CL-WI-04'],  # firewall hardening, WAF, Azure WAF
            ['NW-T1-04'],                                      # firewall/IDS alert checklist
            []),  # No dedicated response playbook — typically too low-signal to warrant a runbook
        ('T1595.001', 'Scanning IP Blocks',
            ['IT-NET-WI-05', 'IT-CL-WI-04'],
            ['NW-T1-04'],
            []),
        ('T1595.002', 'Vulnerability Scanning (by adversary)',
            ['IT-NET-WI-05', 'IT-SI-WI-02'],
            ['NW-T1-04'],
            []),
        ('T1589',     'Gather Victim Identity Information',
            [],  # External — no preventive control on the org side
            [],
            []),
        ('T1590',     'Gather Victim Network Information',
            [],
            [],
            []),
        ('T1598',     'Phishing for Information',
            ['IT-CL-WI-02'],                                  # M365 anti-phishing baselines
            ['EM-T1-01', 'EM-T1-04'],
            ['EM-PB-01', 'EM-PB-04']),  # phishing & BEC playbooks include recon-phase phishing
    ],

    # ============================================================
    # TA0042 Resource Development — adversary builds capability
    # Almost entirely external to the organisation — gap is expected
    # ============================================================
    'TA0042': [
        ('T1583', 'Acquire Infrastructure',     [], [], []),
        ('T1586', 'Compromise Accounts (external)',[], [], []),
        ('T1588', 'Obtain Capabilities (tooling)', [], [], []),
        ('T1608', 'Stage Capabilities',         [], [], []),
    ],

    # ============================================================
    # TA0001 Initial Access
    # ============================================================
    'TA0001': [
        ('T1566',     'Phishing',
            ['IT-CL-WI-02'],                                      # M365 anti-phish, Safe Links, DKIM/DMARC
            ['EM-T1-01', 'EM-T1-03', 'EM-T1-04', 'EM-T1-05', 'EM-WI-01'],
            ['SOP-EM-01', 'EM-PB-01', 'EM-PB-02', 'EM-PB-03', 'EM-PB-06', 'EM-RB-04', 'EM-RB-05']),
        ('T1566.001', 'Spearphishing Attachment',
            ['IT-CL-WI-02'],
            ['EM-T1-03', 'EM-WI-01'],
            ['EM-PB-01', 'EM-PB-02', 'EM-RB-03', 'EM-RB-04', 'EM-RB-06']),
        ('T1566.002', 'Spearphishing Link',
            ['IT-CL-WI-02'],
            ['EM-T1-01', 'EM-WI-01'],
            ['EM-PB-01', 'EM-PB-03', 'EM-RB-04', 'EM-RB-05']),
        ('T1566.003', 'Spearphishing via Service',
            ['IT-CL-WI-02'],
            ['EM-T1-01'],
            ['EM-PB-04']),
        ('T1190',     'Exploit Public-Facing Application',
            ['IT-SI-SOP-01', 'IT-SI-WI-02', 'IT-CL-SOP-01', 'IT-CL-WI-04', 'IT-VM-SOP-01', 'IT-PM-SOP-02'],  # WAF, Azure WAF, VM, emergency patch
            ['NW-T1-01', 'NW-T1-04', 'NW-WI-01'],
            ['SOP-NW-01', 'NW-PB-01', 'NW-RB-01', 'NW-RB-02']),
        ('T1133',     'External Remote Services',
            ['IT-NET-WI-05', 'IT-SI-WI-04', 'IT-CL-WI-01'],  # firewall, PAM, tenant identity
            ['ID-T1-01', 'NW-T1-04'],
            ['ID-PB-01', 'ID-PB-06', 'NW-PB-01']),
        ('T1078',     'Valid Accounts',
            ['IT-CL-WI-01', 'IT-SRV-WI-DC-01', 'IT-EP-WI-Win-01', 'IT-SI-WI-04'],  # CA/MFA/PIM, Tier-0 access, PAM
            ['ID-T1-01', 'ID-T1-04', 'ID-WI-01'],
            ['SOP-ID-01', 'ID-PB-01', 'ID-PB-05', 'ID-PB-06', 'ID-RB-01', 'ID-RB-03']),
        ('T1078.004', 'Cloud Accounts',
            ['IT-CL-SOP-01', 'IT-CL-WI-01', 'IT-CL-WI-05'],
            ['ID-T1-01', 'ID-T1-04'],
            ['ID-PB-01', 'ID-PB-05', 'ID-RB-01']),
        ('T1195',     'Supply Chain Compromise',
            ['IT-VM-SOP-01', 'IT-TI-SOP-01'],
            [],
            []),  # No dedicated playbook — handled via IRP
        ('T1199',     'Trusted Relationship',
            ['IT-CL-WI-01', 'IT-CL-WI-02'],                       # guest access governance, cross-tenant
            ['ID-T1-05'],
            ['ID-PB-06']),
        ('T1200',     'Hardware Additions',
            ['IT-EP-WI-Win-05', 'IT-EP-WI-PAW-05'],               # USB/device control
            ['EP-T1-05'],
            ['EP-WI-USB']),
    ],

    # ============================================================
    # TA0002 Execution
    # ============================================================
    'TA0002': [
        ('T1059',     'Command and Scripting Interpreter',
            ['IT-EP-WI-Win-03', 'IT-SRV-WI-Win-03', 'IT-EP-WI-PAW-04'],  # ASR rules, EDR
            ['EP-T1-04', 'EP-INV-Win-01'],
            ['SOP-EP-01', 'EP-PB-01', 'EP-PB-02', 'EP-RB-01']),
        ('T1059.001', 'PowerShell',
            ['IT-EP-WI-Win-03', 'IT-SRV-WI-Win-03'],              # ASR + constrained language mode in baselines
            ['EP-T1-04', 'EP-INV-Win-01'],
            ['EP-PB-01', 'EP-RB-01']),
        ('T1059.003', 'Windows Command Shell',
            ['IT-EP-WI-Win-03'],
            ['EP-T1-04'],
            ['EP-PB-01', 'EP-RB-01']),
        ('T1059.004', 'Unix Shell',
            ['IT-SRV-WI-LNX-02', 'IT-SRV-WI-LNX-03'],
            [],                                                    # No Tier-1 for Linux execution today — gap
            []),
        ('T1059.005', 'Visual Basic',
            ['IT-EP-WI-Win-03'],
            ['EP-T1-02', 'EP-T1-04'],
            ['EP-PB-01']),
        ('T1059.007', 'JavaScript',
            ['IT-EP-WI-Win-03'],
            ['EP-T1-04'],
            ['EP-PB-01']),
        ('T1106',     'Native API',
            ['IT-EP-WI-Win-03', 'IT-SRV-WI-Win-03'],
            ['EP-T1-02', 'EP-INV-Win-01'],
            ['EP-PB-02']),
        ('T1204',     'User Execution',
            ['IT-CL-WI-02', 'IT-EP-WI-Win-03'],                   # Safe Links/Attachments + ASR
            ['EM-T1-03', 'EP-T1-02'],
            ['EM-PB-01', 'EM-PB-02', 'EP-PB-01']),
        ('T1204.001', 'Malicious Link',
            ['IT-CL-WI-02'],                                       # Safe Links
            ['EM-T1-01', 'EM-T1-03'],
            ['EM-PB-01', 'EM-PB-03']),
        ('T1204.002', 'Malicious File',
            ['IT-CL-WI-02', 'IT-EP-WI-Win-03'],                   # Safe Attachments + ASR
            ['EM-T1-03', 'EP-T1-02'],
            ['EM-PB-01', 'EM-PB-02', 'EP-PB-01', 'EM-RB-03']),
        ('T1053',     'Scheduled Task/Job',
            ['IT-EP-WI-Win-04', 'IT-SRV-WI-Win-04'],              # logging
            ['EP-T1-01', 'EP-INV-Win-01'],
            ['EP-PB-03', 'EP-PB-04']),
        ('T1053.005', 'Scheduled Task (Windows)',
            ['IT-EP-WI-Win-04', 'IT-SRV-WI-Win-04'],
            ['EP-T1-01', 'EP-INV-Win-01'],
            ['EP-PB-03', 'EP-PB-04']),
        ('T1569',     'System Services',
            ['IT-EP-WI-Win-01', 'IT-SRV-WI-Win-02'],
            ['EP-T1-04'],
            ['EP-PB-02', 'EP-PB-04']),
    ],

    # ============================================================
    # TA0003 Persistence
    # ============================================================
    'TA0003': [
        ('T1547',     'Boot or Logon Autostart',
            ['IT-EP-WI-Win-04', 'IT-SRV-WI-Win-04', 'IT-EP-WI-PAW-06'],
            ['EP-T1-01', 'EP-INV-Win-01'],
            ['EP-PB-04', 'EP-RB-03', 'EP-WI-04']),
        ('T1547.001', 'Registry Run Keys / Startup Folder',
            ['IT-EP-WI-Win-04', 'IT-SRV-WI-Win-04'],
            ['EP-INV-Win-01'],
            ['EP-PB-04', 'EP-RB-03']),
        ('T1543',     'Create or Modify System Process',
            ['IT-EP-WI-Win-01', 'IT-SRV-WI-Win-01', 'IT-SRV-WI-LNX-02'],
            ['EP-T1-04', 'EP-INV-Win-01'],
            ['EP-PB-04', 'EP-RB-03']),
        ('T1543.003', 'Windows Service',
            ['IT-EP-WI-Win-01', 'IT-SRV-WI-Win-01'],
            ['EP-INV-Win-01'],
            ['EP-PB-04', 'EP-RB-03']),
        ('T1136',     'Create Account',
            ['IT-CL-WI-01', 'IT-SRV-WI-DC-01'],                   # Conditional Access, Tier-0 AD admin discipline
            ['ID-T1-04', 'ID-WI-01'],
            ['ID-PB-05', 'ID-RB-03']),
        ('T1136.003', 'Cloud Account',
            ['IT-CL-WI-01'],
            ['ID-T1-04'],
            ['ID-PB-05']),
        ('T1098',     'Account Manipulation',
            ['IT-CL-WI-01', 'IT-SRV-WI-DC-02', 'IT-EP-WI-PAW-02'],                   # Entra PIM, AD credential protection
            ['ID-T1-04'],
            ['ID-PB-05', 'ID-RB-01', 'ID-RB-03']),
        ('T1098.001', 'Add Cloud Credentials',
            ['IT-CL-WI-01'],
            ['ID-T1-04'],
            ['ID-PB-05', 'ID-PB-04']),
        ('T1078',     'Valid Accounts (persistence)',
            ['IT-CL-WI-01', 'IT-SI-WI-04'],
            ['ID-T1-01', 'ID-T1-04'],
            ['SOP-ID-01', 'ID-PB-01', 'ID-PB-05']),
        ('T1505.003', 'Web Shell',
            ['IT-SI-WI-02', 'IT-CL-WI-04', 'IT-SRV-WI-Win-03', 'IT-SRV-WI-LNX-04'],
            ['NW-T1-01', 'EP-T1-01'],
            ['NW-PB-01', 'NW-PB-02', 'EP-PB-04']),
        ('T1546',     'Event Triggered Execution',
            ['IT-EP-WI-Win-04', 'IT-SRV-WI-Win-04'],
            ['EP-INV-Win-01'],
            ['EP-PB-04']),
        ('T1574',     'Hijack Execution Flow',
            ['IT-EP-WI-Win-03'],
            ['EP-T1-04', 'EP-INV-Win-01'],
            ['EP-PB-04']),
        ('T1556',     'Modify Authentication Process',
            ['IT-CL-WI-01', 'IT-SRV-WI-DC-02'],
            ['ID-T1-04'],
            ['ID-PB-02', 'ID-PB-03', 'ID-PB-05']),
        ('T1137',     'Office Application Startup',
            ['IT-EP-WI-Win-03', 'IT-CL-WI-02'],                   # ASR + Office security baseline
            ['EP-T1-02'],
            ['EP-PB-04']),
        ('T1078.004', 'Valid Cloud Accounts (persistence)',
            ['IT-CL-WI-01'],
            ['ID-T1-01'],
            ['ID-PB-01', 'ID-PB-05']),
    ],

    # ============================================================
    # TA0004 Privilege Escalation
    # ============================================================
    'TA0004': [
        ('T1068',     'Exploitation for Privilege Escalation',
            ['IT-PM-SOP-01', 'IT-PM-SOP-02', 'IT-VM-SOP-01', 'IT-GOV-WI-PM-01', 'IT-GOV-WI-PM-02', 'IT-GOV-WI-VM-01', 'IT-GOV-WI-VM-02'],
            ['EP-T1-02', 'EP-INV-Win-01'],
            ['EP-PB-02']),
        ('T1078',     'Valid Accounts (priv-esc)',
            ['IT-CL-WI-01', 'IT-SI-WI-04', 'IT-SRV-WI-DC-01'],   # PIM, PAM, Tier-0
            ['ID-T1-04'],
            ['ID-PB-05', 'ID-RB-01']),
        ('T1548',     'Abuse Elevation Control Mechanism',
            ['IT-EP-WI-Win-01', 'IT-SRV-WI-Win-01'],              # local admin / UAC
            ['EP-T1-04'],
            ['EP-PB-02']),
        ('T1548.002', 'Bypass User Account Control',
            ['IT-EP-WI-Win-01'],
            ['EP-T1-04', 'EP-INV-Win-01'],
            ['EP-PB-02']),
        ('T1134',     'Access Token Manipulation',
            ['IT-EP-WI-Win-03', 'IT-SRV-WI-Win-03'],
            ['EP-T1-04', 'EP-INV-Win-01'],
            ['EP-PB-02']),
        ('T1484',     'Domain or Tenant Policy Modification',
            ['IT-SRV-WI-DC-01', 'IT-CL-WI-01'],
            ['ID-T1-04'],
            ['ID-PB-05', 'ID-PB-07']),
        ('T1484.002', 'Trust Modification (Cloud)',
            ['IT-CL-WI-01', 'IT-CL-WI-03'],                       # CA + Azure subscription baseline
            ['ID-T1-04'],
            ['ID-PB-05']),
        ('T1611',     'Escape to Host (containers)',
            ['IT-CL-WI-04'],                                       # workload patterns
            [],
            []),  # Gap: no container-runtime detection content yet
    ],

    # ============================================================
    # TA0005 Defense Evasion
    # ============================================================
    'TA0005': [
        ('T1562',     'Impair Defenses',
            ['IT-EP-WI-Win-03', 'IT-SRV-WI-Win-03', 'IT-CL-WI-05'],
            ['EP-T1-02', 'EP-INV-Win-01'],
            ['EP-PB-02', 'EP-PB-04']),
        ('T1562.001', 'Disable or Modify Tools',
            ['IT-EP-WI-Win-03', 'IT-CL-WI-05'],                   # tamper protection, Defender baseline
            ['EP-T1-02'],
            ['EP-PB-02', 'EP-PB-04']),
        ('T1027',     'Obfuscated Files or Information',
            ['IT-EP-WI-Win-03'],
            ['EP-T1-02', 'EM-T1-03'],
            ['EM-PB-03', 'EP-PB-01']),
        ('T1036',     'Masquerading',
            ['IT-EP-WI-Win-03'],
            ['EM-T1-04', 'EP-T1-04'],
            ['EM-PB-02', 'EP-PB-01']),
        ('T1070',     'Indicator Removal',
            ['IT-EP-WI-Win-04', 'IT-SRV-WI-Win-04', 'IT-SRV-WI-LNX-05'],
            ['EP-INV-Win-01'],
            ['EP-PB-04']),
        ('T1070.004', 'File Deletion',
            ['IT-EP-WI-Win-04'],
            ['EP-INV-Win-01'],
            ['EP-PB-04']),
        ('T1140',     'Deobfuscate/Decode Files',
            ['IT-EP-WI-Win-03'],
            ['EP-T1-02'],
            ['EP-PB-01']),
        ('T1218',     'System Binary Proxy Execution (LOLBin)',
            ['IT-EP-WI-Win-03'],
            ['EP-T1-04', 'EP-INV-Win-01'],
            ['EP-PB-01', 'EP-PB-02']),
        ('T1550',     'Use Alternate Authentication Material',
            ['IT-CL-WI-01', 'IT-SRV-WI-DC-02'],
            ['ID-T1-04'],
            ['ID-PB-05']),
        ('T1550.001', 'Application Access Token',
            ['IT-CL-WI-01'],
            ['ID-T1-04'],
            ['ID-PB-04']),
        ('T1564',     'Hide Artifacts',
            ['IT-EP-WI-Win-04'],
            ['EP-INV-Win-01'],
            ['EP-PB-04']),
        ('T1112',     'Modify Registry',
            ['IT-EP-WI-Win-04'],
            ['EP-INV-Win-01'],
            ['EP-PB-04']),
    ],

    # ============================================================
    # TA0006 Credential Access
    # ============================================================
    'TA0006': [
        ('T1003',     'OS Credential Dumping',
            ['IT-EP-WI-Win-01', 'IT-SRV-WI-DC-02', 'IT-EP-WI-PAW-03', 'IT-EP-WI-PAW-02', 'IT-EP-WI-PAW-01'],  # local admin, AD cred protection, PAW
            ['EP-T1-02', 'EP-T1-04'],
            ['EP-PB-02']),
        ('T1003.001', 'LSASS Memory',
            ['IT-EP-WI-Win-01', 'IT-SRV-WI-DC-02'],               # Credential Guard, RunAsPPL
            ['EP-T1-02'],
            ['EP-PB-02']),
        ('T1003.002', 'Security Account Manager (SAM)',
            ['IT-EP-WI-Win-01'],
            ['EP-INV-Win-01'],
            ['EP-PB-02']),
        ('T1110',     'Brute Force',
            ['IT-CL-WI-01', 'IT-SI-WI-02'],                       # CA lockout + WAF rate limit
            ['ID-T1-01', 'ID-T1-03'],
            ['ID-PB-07', 'ID-RB-03']),
        ('T1110.003', 'Password Spraying',
            ['IT-CL-WI-01'],                                       # CA, sign-in risk policies
            ['ID-T1-01'],
            ['ID-PB-07']),
        ('T1110.004', 'Credential Stuffing',
            ['IT-CL-WI-01'],
            ['ID-T1-01'],
            ['ID-PB-07']),
        ('T1556',     'Modify Authentication Process',
            ['IT-CL-WI-01', 'IT-SRV-WI-DC-02'],
            ['ID-T1-04'],
            ['ID-PB-02', 'ID-PB-03', 'ID-RB-05']),
        ('T1621',     'Multi-Factor Authentication Request Generation (MFA fatigue)',
            ['IT-CL-WI-01'],                                       # number matching, CA
            ['ID-T1-02'],
            ['ID-PB-03']),
        ('T1555',     'Credentials from Password Stores',
            ['IT-EP-WI-Win-01', 'IT-SI-WI-04'],                   # local admin, PAM vault
            ['EP-T1-04'],
            ['EP-PB-02']),
        ('T1212',     'Exploitation for Credential Access',
            ['IT-PM-SOP-01', 'IT-PM-SOP-02', 'IT-VM-SOP-01', 'IT-GOV-WI-PM-01', 'IT-GOV-WI-PM-02'],
            [],
            []),
        ('T1187',     'Forced Authentication',
            ['IT-SRV-WI-DC-02', 'IT-NET-WI-03'],                  # NTLM hardening, data plane
            [],
            []),
        ('T1606',     'Forge Web Credentials',
            ['IT-CL-WI-01', 'IT-SI-WI-04'],
            ['ID-T1-04'],
            ['ID-PB-04', 'ID-PB-05']),
    ],

    # ============================================================
    # TA0007 Discovery
    # ============================================================
    'TA0007': [
        ('T1087',     'Account Discovery',
            ['IT-SRV-WI-DC-04'],                                   # logging
            ['EP-T1-04', 'EP-INV-Win-01'],
            ['EP-PB-01', 'EP-PB-03']),
        ('T1087.002', 'Domain Account Discovery',
            ['IT-SRV-WI-DC-04'],
            ['EP-INV-Win-01'],
            ['EP-PB-03', 'ID-PB-05']),
        ('T1018',     'Remote System Discovery',
            ['IT-NET-WI-03'],
            ['NW-T1-02'],
            ['NW-PB-03', 'NW-RB-03', 'NW-WI-03']),
        ('T1046',     'Network Service Discovery',
            ['IT-NET-WI-05'],
            ['NW-T1-02', 'NW-T1-04'],
            ['NW-PB-03', 'NW-RB-03']),
        ('T1057',     'Process Discovery',
            ['IT-EP-WI-Win-04'],
            ['EP-T1-04', 'EP-INV-Win-01'],
            ['EP-PB-01']),
        ('T1083',     'File and Directory Discovery',
            ['IT-EP-WI-Win-04'],
            ['EP-INV-Win-01'],
            ['EP-PB-01']),
        ('T1135',     'Network Share Discovery',
            ['IT-NET-WI-03', 'IT-SRV-WI-Win-02'],
            ['NW-T1-02'],
            ['NW-PB-03']),
        ('T1069',     'Permission Groups Discovery',
            ['IT-SRV-WI-DC-04'],
            ['EP-INV-Win-01'],
            ['EP-PB-03', 'ID-PB-05']),
        ('T1482',     'Domain Trust Discovery',
            ['IT-SRV-WI-DC-04'],
            ['EP-INV-Win-01'],
            ['EP-PB-03']),
        ('T1538',     'Cloud Service Dashboard',
            ['IT-CL-WI-01', 'IT-CL-WI-03'],
            ['ID-T1-01'],
            ['ID-PB-01']),
        ('T1526',     'Cloud Service Discovery',
            ['IT-CL-WI-03'],
            ['ID-T1-01'],
            ['ID-PB-01']),
        ('T1518',     'Software Discovery',
            ['IT-EP-WI-Win-04'],
            ['EP-INV-Win-01'],
            ['EP-PB-01']),
    ],

    # ============================================================
    # TA0008 Lateral Movement
    # ============================================================
    'TA0008': [
        ('T1021',     'Remote Services',
            ['IT-NET-WI-03', 'IT-NET-WI-05', 'IT-SRV-WI-DC-05'],
            ['NW-T1-02', 'NW-WI-03'],
            ['NW-PB-03', 'NW-RB-03', 'EP-PB-03', 'EP-RB-04']),
        ('T1021.001', 'Remote Desktop Protocol',
            ['IT-NET-WI-05', 'IT-SRV-WI-Win-05', 'IT-CL-WI-04'],  # firewall, server firewall, JIT
            ['NW-T1-02'],
            ['NW-PB-03', 'EP-PB-03']),
        ('T1021.002', 'SMB / Windows Admin Shares',
            ['IT-NET-WI-03', 'IT-SRV-WI-Win-02'],
            ['NW-T1-02'],
            ['NW-PB-03', 'EP-PB-03']),
        ('T1021.004', 'SSH',
            ['IT-SRV-WI-LNX-02', 'IT-NET-WI-05'],
            ['NW-T1-02'],
            ['NW-PB-03']),
        ('T1021.006', 'Windows Remote Management',
            ['IT-SRV-WI-Win-02'],
            ['NW-T1-02'],
            ['NW-PB-03', 'EP-PB-03']),
        ('T1570',     'Lateral Tool Transfer',
            ['IT-NET-WI-03', 'IT-SRV-WI-Win-05'],
            ['EP-T1-01', 'NW-T1-02'],
            ['EP-PB-03', 'EP-RB-04']),
        ('T1078',     'Valid Accounts (lateral)',
            ['IT-CL-WI-01', 'IT-SI-WI-04'],
            ['ID-T1-01', 'ID-T1-04'],
            ['ID-PB-01', 'ID-PB-05', 'EP-PB-03']),
        ('T1550',     'Use Alternate Auth Material (lateral)',
            ['IT-SRV-WI-DC-02', 'IT-CL-WI-01'],                   # Credential Guard + CA
            ['ID-T1-04'],
            ['ID-PB-05']),
        ('T1210',     'Exploitation of Remote Services',
            ['IT-PM-SOP-01', 'IT-PM-SOP-02', 'IT-VM-SOP-01', 'IT-GOV-WI-PM-02', 'IT-GOV-WI-VM-03'],
            ['NW-T1-04'],
            ['NW-PB-01']),
    ],

    # ============================================================
    # TA0009 Collection
    # ============================================================
    'TA0009': [
        ('T1005',     'Data from Local System',
            ['IT-EP-WI-Win-02', 'IT-EP-WI-Win-04', 'IT-SRV-WI-LNX-07'],  # BitLocker, monitoring, Linux backups
            ['EP-INV-Win-01'],
            ['EP-PB-01']),
        ('T1039',     'Data from Network Shared Drive',
            ['IT-SRV-WI-Win-04', 'IT-SRV-WI-LNX-05'],
            ['NW-T1-05'],
            ['NW-PB-04']),
        ('T1213',     'Data from Information Repositories',
            ['IT-CL-WI-02'],                                       # SharePoint sharing + DLP
            ['EM-T1-02'],
            ['EM-PB-06']),
        ('T1114',     'Email Collection',
            ['IT-CL-WI-02'],                                       # M365 audit + Defender for Office
            ['EM-T1-02', 'ID-T1-01', 'ID-WI-05'],
            ['EM-PB-04', 'EM-PB-06', 'EM-PB-07', 'EM-RB-07', 'ID-PB-02', 'ID-RB-02', 'ID-WI-02']),
        ('T1114.003', 'Email Forwarding Rule',
            ['IT-CL-WI-02'],
            ['EM-T1-02'],
            ['EM-PB-04', 'EM-PB-06', 'EM-PB-07', 'EM-RB-07', 'ID-PB-02', 'ID-RB-02', 'ID-RB-04']),
        ('T1119',     'Automated Collection',
            ['IT-EP-WI-Win-04'],
            ['EP-INV-Win-01'],
            ['EP-PB-01']),
        ('T1530',     'Data from Cloud Storage',
            ['IT-CL-WI-04', 'IT-CL-WI-02'],                       # storage hardening + DLP
            ['NW-T1-05'],
            ['NW-PB-04']),
        ('T1074',     'Data Staged',
            ['IT-EP-WI-Win-04'],
            ['EP-INV-Win-01', 'NW-T1-05'],
            ['EP-PB-01', 'NW-PB-04']),
        ('T1056',     'Input Capture (keylogging)',
            ['IT-EP-WI-Win-03'],
            ['EP-T1-04'],
            ['EP-PB-01']),
    ],

    # ============================================================
    # TA0011 Command and Control
    # ============================================================
    'TA0011': [
        ('T1071',     'Application Layer Protocol',
            ['IT-NET-SOP-01', 'IT-NET-WI-05', 'IT-SI-WI-01'],
            ['NW-T1-01', 'NW-WI-01'],
            ['SOP-NW-01', 'NW-PB-02', 'NW-RB-01', 'NW-RB-02', 'NW-WI-02']),
        ('T1071.001', 'Web Protocols (HTTP/S C2)',
            ['IT-NET-WI-05', 'IT-SI-WI-02'],
            ['NW-T1-01'],
            ['NW-PB-02', 'NW-RB-01', 'NW-RB-02']),
        ('T1071.004', 'DNS C2',
            ['IT-NET-WI-05'],
            ['NW-T1-03'],
            ['NW-PB-02', 'NW-RB-02']),
        ('T1095',     'Non-Application Layer Protocol',
            ['IT-NET-WI-05'],
            ['NW-T1-01'],
            ['NW-PB-02', 'NW-RB-02']),
        ('T1572',     'Protocol Tunneling',
            ['IT-NET-WI-05'],
            ['NW-T1-01', 'NW-T1-03'],
            ['NW-PB-02', 'NW-RB-02']),
        ('T1090',     'Proxy',
            ['IT-NET-WI-05'],
            ['NW-T1-01'],
            ['NW-PB-02', 'NW-RB-02']),
        ('T1568',     'Dynamic Resolution',
            ['IT-NET-WI-05'],
            ['NW-T1-03'],
            ['NW-PB-02', 'NW-RB-02']),
        ('T1102',     'Web Service (C2 over legitimate platforms)',
            ['IT-NET-WI-05'],
            ['NW-T1-01'],
            ['NW-PB-02']),
        ('T1573',     'Encrypted Channel',
            ['IT-NET-WI-05', 'IT-SI-WI-02'],                      # TLS inspection
            ['NW-T1-01'],
            ['NW-PB-02']),
        ('T1105',     'Ingress Tool Transfer',
            ['IT-NET-WI-05', 'IT-EP-WI-Win-03'],
            ['NW-T1-01', 'EP-T1-04'],
            ['NW-PB-02', 'EP-PB-01']),
    ],

    # ============================================================
    # TA0010 Exfiltration
    # ============================================================
    'TA0010': [
        ('T1041',     'Exfiltration Over C2 Channel',
            ['IT-NET-WI-05'],
            ['NW-T1-05'],
            ['NW-PB-04', 'NW-RB-02']),
        ('T1048',     'Exfiltration Over Alternative Protocol',
            ['IT-NET-WI-05'],
            ['NW-T1-05'],
            ['NW-PB-04', 'NW-RB-02']),
        ('T1048.003', 'Unencrypted Non-C2 Protocol Exfil',
            ['IT-NET-WI-05'],
            ['NW-T1-05'],
            ['NW-PB-04']),
        ('T1567',     'Exfiltration Over Web Service',
            ['IT-CL-WI-02', 'IT-NET-WI-05'],                      # DLP + egress filtering
            ['NW-T1-05'],
            ['NW-PB-04', 'EM-PB-06']),
        ('T1567.002', 'Exfiltration to Cloud Storage',
            ['IT-CL-WI-02', 'IT-CL-WI-04'],                       # DLP + storage controls
            ['NW-T1-05'],
            ['NW-PB-04', 'EM-PB-06']),
        ('T1052',     'Exfiltration Over Physical Medium (USB)',
            ['IT-EP-WI-Win-05', 'IT-EP-WI-PAW-05'],               # USB control
            ['EP-T1-05'],
            ['EP-WI-USB']),
        ('T1029',     'Scheduled Transfer',
            ['IT-NET-WI-05'],
            ['NW-T1-05'],
            ['NW-PB-04']),
        ('T1030',     'Data Transfer Size Limits',
            ['IT-NET-WI-05'],
            ['NW-T1-05'],
            ['NW-PB-04']),
    ],

    # ============================================================
    # TA0040 Impact
    # ============================================================
    'TA0040': [
        ('T1486',     'Data Encrypted for Impact (Ransomware)',
            ['IT-EP-WI-Win-03', 'IT-SRV-WI-Win-03', 'IT-SRV-WI-LNX-04', 'IT-CL-WI-04'],  # EDR + backups
            ['EP-T1-03', 'EP-INV-Win-01'],
            ['EM-PB-05', 'EP-PB-01', 'EP-WI-02', 'EP-WI-03']),
        ('T1490',     'Inhibit System Recovery',
            ['IT-EP-WI-Win-04', 'IT-SRV-WI-Win-06', 'IT-SRV-WI-LNX-07', 'IT-SRV-WI-DC-06', 'IT-CL-WI-04'],
            ['EP-T1-03'],
            ['EM-PB-05']),
        ('T1489',     'Service Stop',
            ['IT-EP-WI-Win-04'],
            ['EP-T1-04'],
            ['EP-PB-04']),
        ('T1485',     'Data Destruction',
            ['IT-SRV-WI-Win-06', 'IT-SRV-WI-LNX-07', 'IT-SRV-WI-DC-06'],
            ['EP-T1-03'],
            ['EM-PB-05', 'EP-PB-01']),
        ('T1565',     'Data Manipulation',
            ['IT-EP-WI-Win-02', 'IT-SRV-WI-Win-06'],
            ['EP-INV-Win-01'],
            ['EP-PB-01']),
        ('T1491',     'Defacement',
            ['IT-SI-WI-02', 'IT-CL-WI-04'],                       # WAF
            ['NW-T1-04'],
            ['NW-PB-01']),
        ('T1499',     'Endpoint Denial of Service',
            ['IT-NET-WI-05', 'IT-SI-WI-02', 'IT-CL-WI-04'],
            ['NW-T1-04'],
            ['NW-PB-05', 'NW-RB-05']),
        ('T1498',     'Network Denial of Service',
            ['IT-NET-WI-05', 'IT-SI-WI-03', 'IT-CL-WI-04'],       # network + LB + Azure DDoS Std
            ['NW-T1-04'],
            ['NW-PB-05', 'NW-RB-05']),
        ('T1531',     'Account Access Removal',
            ['IT-CL-WI-01', 'IT-SRV-WI-DC-01'],                   # break-glass, Tier-0 discipline
            ['ID-T1-04'],
            ['ID-PB-05', 'ID-RB-01']),
        ('T1561',     'Disk Wipe',
            ['IT-EP-WI-Win-02', 'IT-SRV-WI-Win-06'],
            ['EP-T1-03'],
            ['EM-PB-05']),
    ],
}

def coverage_state(prevent, detect, respond):
    """Return 'full' | 'partial' | 'gap' based on which control types exist."""
    n = sum(1 for x in (prevent, detect, respond) if x)
    if n == 3: return 'full'
    if n == 0: return 'gap'
    return 'partial'

def get_stats():
    """Compute summary statistics."""
    total_tech = 0
    full = 0
    partial = 0
    gap = 0
    by_tactic = {}
    for tac_id, techs in MAPPING.items():
        f = p = g = 0
        for _, _, prevent, detect, respond in techs:
            state = coverage_state(prevent, detect, respond)
            total_tech += 1
            if state == 'full': full += 1; f += 1
            elif state == 'partial': partial += 1; p += 1
            else: gap += 1; g += 1
        by_tactic[tac_id] = (f, p, g, len(techs))
    return {
        'total_techniques': total_tech,
        'full': full,
        'partial': partial,
        'gap': gap,
        'by_tactic': by_tactic,
    }

if __name__ == '__main__':
    stats = get_stats()
    print(f"Total techniques mapped: {stats['total_techniques']}")
    print(f"  Full coverage:    {stats['full']}")
    print(f"  Partial coverage: {stats['partial']}")
    print(f"  Gap:              {stats['gap']}")
    print()
    print('Per tactic (full/partial/gap of total):')
    for tac_id, tac_name, _ in TACTICS:
        f, p, g, n = stats['by_tactic'].get(tac_id, (0,0,0,0))
        print(f'  {tac_id} {tac_name:25s}: {f}/{p}/{g} of {n}')
