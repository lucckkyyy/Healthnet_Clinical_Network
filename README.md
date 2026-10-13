# 🏥 HealthNet - Segmented Clinical Network Lab

## 📘 Modeling a Hospital Network Where Zones Are Kept Apart on Purpose

I work on the IT side of a hospital network, so I built this to model the part of that environment that matters most: keeping clinical workstations, admin systems, guest Wi-Fi, medical devices, and servers in separate zones, and allowing only the traffic each zone actually needs. A flat network is the easy thing to build. The interesting part is deciding what *shouldn't* be allowed and proving it.

The lab is a scaled-down model in Cisco Packet Tracer: six VLANs, a multilayer core switch doing inter-VLAN routing, centralized DHCP, least-privilege ACLs, SSH-only management, port security, and centralized logging. It is a lab project, not a production design, and it doesn't claim to match the size of a real hospital network.

The part I care about most is the access policy. I wrote it as a table first, the way a change request would be written, then wrote the ACLs from it, then built a script that parses the ACL text and checks it against the policy, so a typo in a rule shows up as a failing test.

---

## ✅ Verification

| Check | Result |
|---|---|
| Access policy (6 VLANs, least privilege) | Documented in `docs/access-policy.md` |
| Device configs: base, security, hardening, NAT | Complete in `configs/` |
| ACL policy check, 20 cases (10 allow / 10 deny) | **20/20 pass** (`python3 tools/verify_policy.py`) |
| Break/fix tickets (trunk, DHCP, ACL order, gateway) | Written in `troubleshooting/` |
| Cisco Packet Tracer run | Results go in `docs/test-matrix.md` |

The script checks the ACL text against the policy. It does not emulate a network.

---|---|
| Topology, IP plan, access policy | Done |
| Base and security device configs | Written |
| ACL policy check (20 cases, 10 allow / 10 deny) | **20/20 pass** (`tools/verify_policy.py`) |
| Fault tickets (trunk, DHCP, ACL order, gateway) | Prepared, not yet run |
| Built and tested in Cisco Packet Tracer | In progress |

The script checks the ACL text against the policy. It does not emulate a network, so the Packet Tracer results are recorded separately in `docs/test-matrix.md` as I run them.

---

## 🧠 Skills I Developed

### **Network Segmentation & Routing**
- Designing a six-VLAN layout (clinical, admin, guest, medical/IoT, servers, management) plus an unused blackhole native VLAN
- Configuring trunks that carry only the VLANs each switch needs
- Inter-VLAN routing on a multilayer switch, DHCP relay with `ip helper-address`, and NAT at the edge router

### **Least-Privilege Access Control**
- Writing the policy as a table first, then turning it into one extended ACL per VLAN
- Understanding why ACL order matters, why return traffic needs `established` or `echo-reply` rules, and how DHCP relay replies interact with an inbound ACL
- Restricting SSH to the admin VLAN and using local admin and helpdesk accounts with different privilege levels

### **Device Hardening**
- SSH-only access, port security, BPDU guard, shutting unused ports into a dead VLAN
- Syslog and NTP to a central server so events line up in time

### **Testing & Verification**
- Building a 20-case test matrix, including return paths, instead of only testing the happy path
- Writing a Python verifier that parses the real ACL config, then breaking a rule on purpose to confirm the script catches it (20/20 dropped to 16/20)

### **Troubleshooting & Documentation**
- Four fault scenarios prepared as ticket-style write-ups: symptom, diagnosis steps, root cause, fix, prevention
- Mapping configuration choices to eight NIST 800-53 controls, only for features I can actually enable

---

## ⚡ What I Built

- Six VLANs and three trunk links, with inter-VLAN routing on a multilayer core switch
- Centralized DHCP and DNS server segment with relay on every client VLAN
- Six inbound ACLs implementing the access policy
- SSH-only management, admin and helpdesk roles, port security, syslog, NTP, and NAT
- A policy verifier (`tools/verify_policy.py`) that runs 20 cases against the real config
- A step-by-step build guide and four prepared break/fix tickets

### Addressing at a glance

| VLAN | Name | Subnet |
|---|---|---|
| 10 | CLINICAL | 10.10.10.0/24 |
| 20 | ADMIN | 10.10.20.0/24 |
| 30 | GUEST | 10.10.30.0/24 |
| 40 | MEDICAL-IOT | 10.10.40.0/24 |
| 50 | SERVERS | 10.10.50.0/24 |
| 99 | MGMT | 10.10.99.0/24 |
| 999 | BLACKHOLE (unused native VLAN) | none |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Simulation | Cisco Packet Tracer |
| Switching & routing | VLANs, 802.1Q trunks, SVIs, DHCP relay, static routes, NAT/PAT |
| Security | Extended ACLs, SSH, local AAA, port security, BPDU guard |
| Monitoring | Syslog, NTP |
| Verification | Python 3 (ACL parser and policy checker) |
| Frameworks | NIST 800-53 control mapping |

---

## 🚀 Run It

```bash
git clone https://github.com/lucckkyyy/healthnet-clinical-network.git
cd healthnet-clinical-network

# Check the ACL policy (20 cases)
python3 tools/verify_policy.py
```

To build the network, follow `docs/build-guide.md`. Paste the files in `configs/` into the devices in Cisco Packet Tracer, then fill in the Packet Tracer results in `docs/test-matrix.md`.

```
healthnet-clinical-network/
  docs/               ip-plan, access-policy, test-matrix, compliance-map, build-guide
  configs/            base configs, core-sw1-security.txt, access-switch-hardening.txt
  tools/              verify_policy.py
  troubleshooting/    four fault tickets
  screenshots/
```

---

## 🚀 The Learning Outcome

The biggest lesson was that a security policy is only as good as its tests. Writing the ACLs was the easy part. The real work was thinking through everything around them: return traffic, DHCP relay replies, rule order, and what happens when the broad "permit" rule lands above the "deny". Building a script that reads the actual config, and then breaking a rule on purpose to see it fail, made the policy something I could check instead of something I hoped was right.

It also connected a lot of what I do at work, from segmentation and access reviews to troubleshooting, to something I can show and explain step by step.

---

*Author: Aryan Rajguru*
