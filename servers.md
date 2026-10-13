# Server configuration (set in the Packet Tracer GUI)

## Static IPs (Desktop > IP Configuration)

| Server | IP | Mask | Gateway | DNS |
|---|---|---|---|---|
| APP-SRV | 10.10.50.10 | 255.255.255.0 | 10.10.50.1 | 10.10.50.11 |
| DHCP-DNS | 10.10.50.11 | 255.255.255.0 | 10.10.50.1 | 10.10.50.11 |
| SYSLOG-AAA | 10.10.50.12 | 255.255.255.0 | 10.10.50.1 | 10.10.50.11 |

## DHCP pools on DHCP-DNS (Services > DHCP, delete the default pool first)

| Pool | Gateway | DNS | Start IP | Mask | Max users |
|---|---|---|---|---|---|
| CLINICAL | 10.10.10.1 | 10.10.50.11 | 10.10.10.50 | 255.255.255.0 | 50 |
| ADMIN | 10.10.20.1 | 10.10.50.11 | 10.10.20.50 | 255.255.255.0 | 50 |
| GUEST | 10.10.30.1 | 10.10.50.11 | 10.10.30.50 | 255.255.255.0 | 50 |
| IOT | 10.10.40.1 | 10.10.50.11 | 10.10.40.50 | 255.255.255.0 | 50 |

DHCP requests reach this server through `ip helper-address 10.10.50.11` on each VLAN interface of CORE-SW1.
