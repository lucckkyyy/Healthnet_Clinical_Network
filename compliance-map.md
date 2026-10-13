# NIST 800-53 Control Mapping (planned)

Only controls that map to a configuration actually built in this lab.

| Control | Name | Implemented by | Evidence |
|---|---|---|---|
| AC-2 | Account management | Local helpdesk and admin accounts | configs/ |
| AC-3 | Access enforcement | Per-VLAN ACLs | configs/, test-matrix.md |
| AC-4 | Information flow enforcement | Inter-VLAN ACL policy | test-matrix.md |
| AC-6 | Least privilege | Restricted trunks, role-based CLI access | configs/ |
| AU-2 | Event logging | Syslog from all devices | screenshots/ |
| AU-8 | Time stamps | NTP | screenshots/ |
| CM-7 | Least functionality | Unused ports shut down, blackhole native VLAN | configs/ |
| SC-7 | Boundary protection | Edge router, NAT, guest isolation | test-matrix.md |

Status: configs for every control are written. Mark a control as evidenced only after you apply it in Packet Tracer and capture a screenshot or `show` output. Controls that Packet Tracer cannot run (for example `aaa` or `ntp` on some models) must be listed as design only.
