# TS-002: DHCP helper removed

Status: **prepared, not yet run in Packet Tracer.** Everything below "Planned" is the test plan. Fill the "Observed" fields from your real run before publishing this as a finished ticket.

## Planned: fault injection
On CORE-SW1 interface vlan 30 run: no ip helper-address 10.10.50.11.

## Planned: expected symptom
Guest1 gets a 169.254.x.x address after a DHCP renew while other VLANs are fine.

## Planned: diagnosis steps
ipconfig /renew on the PC, show running-config interface vlan 30, compare with a working VLAN interface.

## Planned: fix
Restore: ip helper-address 10.10.50.11 on interface vlan 30

## Planned: prevention
Include the helper line in a per-VLAN interface template and check it in the post-change review.

## Observed (fill in)
| Field | Detail |
|---|---|
| Symptom seen | |
| Commands run and key output | |
| Root cause confirmed | |
| Fix applied | |
| Verification | |
| Date | |
