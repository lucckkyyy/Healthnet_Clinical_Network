# Access Policy (least privilege)

Written before configuration, the way a change request would be.

| Source | Allowed | Denied |
|---|---|---|
| Clinical (10) | APP-SRV on 443, DNS and DHCP | Guest, Medical-IoT, Management, direct internet |
| Admin (20) | Servers (443, syslog/AAA), Management (SSH) | Medical-IoT |
| Guest (30) | Internet only | All internal VLANs |
| Medical-IoT (40) | APP-SRV on 443 | Anything initiated into this VLAN |
| Management (99) | Syslog/NTP/AAA to server segment | Reachable from Admin only |

Status: policy defined. ACLs are written and verified against `test-matrix.md` in the build phase.
