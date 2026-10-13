# TS-004: Wrong default gateway

Status: **prepared, not yet run in Packet Tracer.** Everything below "Planned" is the test plan. Fill the "Observed" fields from your real run before publishing this as a finished ticket.

## Planned: fault injection
On PC-Clin2 set a static gateway of 10.10.10.254 instead of 10.10.10.1 (or edit the CLINICAL DHCP pool gateway).

## Planned: expected symptom
PC-Clin2 reaches PCs in its own VLAN but not APP-SRV or the gateway chain.

## Planned: diagnosis steps
ipconfig on the PC, ping own VLAN then gateway, compare the gateway with the SVI address from show ip interface brief on CORE-SW1.

## Planned: fix
Correct the gateway to 10.10.10.1 (fix the DHCP pool if that was the source) and renew.

## Planned: prevention
Use DHCP for client addressing and validate pool options against the IP plan.

## Observed (fill in)
| Field | Detail |
|---|---|
| Symptom seen | |
| Commands run and key output | |
| Root cause confirmed | |
| Fix applied | |
| Verification | |
| Date | |
