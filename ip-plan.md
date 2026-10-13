# IP and VLAN Plan

| VLAN | Name | Subnet | Gateway (SVI on CORE-SW1) |
|---|---|---|---|
| 10 | CLINICAL | 10.10.10.0/24 | 10.10.10.1 |
| 20 | ADMIN | 10.10.20.0/24 | 10.10.20.1 |
| 30 | GUEST | 10.10.30.0/24 | 10.10.30.1 |
| 40 | MEDICAL-IOT | 10.10.40.0/24 | 10.10.40.1 |
| 50 | SERVERS | 10.10.50.0/24 | 10.10.50.1 |
| 99 | MGMT | 10.10.99.0/24 | 10.10.99.1 |
| 999 | BLACKHOLE (unused native VLAN) | none | none |

## Static addresses

| Device | IP |
|---|---|
| APP-SRV | 10.10.50.10 |
| DHCP-DNS | 10.10.50.11 |
| SYSLOG-AAA | 10.10.50.12 |
| SW-A1 (VLAN 99) | 10.10.99.11 |
| SW-A2 (VLAN 99) | 10.10.99.12 |
| SW-S1 (VLAN 99) | 10.10.99.13 |
| CORE-SW1 to R1 link | 10.10.0.2 (core) / 10.10.0.1 (R1), /30 |
| R1 to ISP link | 203.0.113.2 (R1) / 203.0.113.1 (ISP), /30 |

## Trunks

| Link | Allowed VLANs | Native VLAN |
|---|---|---|
| CORE g1/0/1 to SW-A1 g0/1 | 10, 20, 99 | 999 |
| CORE g1/0/2 to SW-A2 g0/1 | 30, 40, 99 | 999 |
| CORE g1/0/3 to SW-S1 g0/1 | 50, 99 | 999 |
