# Build Guide (about 8 hours)

## 0. Place devices and cable

| Device | Packet Tracer model | Name |
|---|---|---|
| Core multilayer switch | 3650-24PS | CORE-SW1 |
| Access switches | 2960-24TT x3 | SW-A1, SW-A2, SW-S1 |
| Routers | 2911 x2 | R1, ISP |
| PCs | PC x5 | PC-Clin1, PC-Clin2, PC-Admin1, Guest1, IoT1 |
| Servers | Server-PT x3 | APP-SRV, DHCP-DNS, SYSLOG-AAA |

| From | To |
|---|---|
| CORE g1/0/1 | SW-A1 g0/1 |
| CORE g1/0/2 | SW-A2 g0/1 |
| CORE g1/0/3 | SW-S1 g0/1 |
| CORE g1/0/24 | R1 g0/0 |
| R1 g0/1 | ISP g0/0 |
| SW-A1 f0/1, f0/2, f0/3 | PC-Clin1, PC-Clin2, PC-Admin1 |
| SW-A2 f0/1, f0/2 | Guest1, IoT1 |
| SW-S1 f0/1, f0/2, f0/3 | APP-SRV, DHCP-DNS, SYSLOG-AAA |

If a port name differs on your model, adjust the config to match.

## 1. Base configuration
Paste in this order: `core-sw1.txt`, `sw-a1.txt`, `sw-a2.txt`, `sw-s1.txt`, `r1.txt`, `isp.txt`. Then follow `servers.md` for server IPs and DHCP pools. Set PCs to DHCP.

## 2. Baseline checks (before ACLs)
`show vlan brief`, `show interfaces trunk`, `show ip route` on CORE-SW1. Every PC gets an address in its VLAN. Run the whole test matrix and record the "before" column. Take screenshots. Save as `healthnet.pkt`.

## 3. Services on SYSLOG-AAA
Turn on Services > SYSLOG and Services > NTP. Add a local note of the IP (10.10.50.12).

## 4. Apply security
1. Paste `core-sw1-security.txt` on CORE-SW1.
2. Paste the matching blocks from `access-switch-hardening.txt` on each access switch.
3. Add the NAT lines already in `r1.txt` (re-paste the file if you used the old one).

## 5. After-ACL checks
Run the matrix again and record the "after" column. If a result differs from the model, find out why. A mismatch you diagnose is good material for a ticket. Then confirm:
- `show access-lists` hit counters increase as you test
- SSH from PC-Admin1 to 10.10.99.11 works, from PC-Clin1 it does not
- Syslog entries appear on SYSLOG-AAA after you shut and re-enable a port
- `show port-security interface f0/1` on an access switch
- Guest1 can ping 8.8.8.8, PC-Clin1 cannot

## 6. Break/fix tickets
Do the four in `troubleshooting/`. For each, inject the fault, diagnose with commands only, fix, verify, and fill in the ticket with what you really observed.

## 7. Wrap up
Screenshots into `screenshots/`, copy running configs into `configs/` if they changed, fill in `docs/compliance-map.md` evidence column, update README status, push.

## Known Packet Tracer limits
Some versions lack `aaa`, `ntp`, sticky MAC, or `privilege exec` on certain models. If a command errors, skip it and write the limitation in the README. Do not list a control as implemented if you could not enable it.
