# TS-001: Trunk missing a VLAN

Status: **prepared, not yet run in Packet Tracer.** Everything below "Planned" is the test plan. Fill the "Observed" fields from your real run before publishing this as a finished ticket.

## Planned: fault injection
On CORE-SW1 g1/0/1 run: switchport trunk allowed vlan 10,99 (removes VLAN 20).

## Planned: expected symptom
Admin PC loses its gateway and DHCP lease renewal fails while Clinical keeps working.

## Planned: diagnosis steps
show interfaces trunk (compare allowed and active VLANs on both ends), show vlan brief, ping the gateway from the Admin PC.

## Planned: fix
Restore: switchport trunk allowed vlan 10,20,99

## Planned: prevention
Standardize trunk configs from a template and diff before change; keep the allowed-VLAN list in docs/ip-plan.md.

## Observed (fill in)
| Field | Detail |
|---|---|
| Symptom seen | |
| Commands run and key output | |
| Root cause confirmed | |
| Fix applied | |
| Verification | |
| Date | |
