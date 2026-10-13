# TS-003: ACL rules in the wrong order

Status: **prepared, not yet run in Packet Tracer.** Everything below "Planned" is the test plan. Fill the "Observed" fields from your real run before publishing this as a finished ticket.

## Planned: fault injection
Edit GUEST-IN so the broad permit ip 10.10.30.0 0.0.0.255 any comes BEFORE the deny to 10.10.0.0/16 (remove and re-add the rules in that order).

## Planned: expected symptom
Guest1 can now reach internal hosts such as APP-SRV, which test cases 11 to 14 should block.

## Planned: diagnosis steps
show access-lists (look at rule order and hit counts), re-run test cases 11 to 14, trace in simulation mode to see which rule matched.

## Planned: fix
Delete and recreate the ACL with the deny before the final permit, or use sequence numbers (ip access-list resequence).

## Planned: prevention
Review ACLs top to bottom before applying, run the policy verifier (tools/verify_policy.py) after every ACL edit.

## Observed (fill in)
| Field | Detail |
|---|---|
| Symptom seen | |
| Commands run and key output | |
| Root cause confirmed | |
| Fix applied | |
| Verification | |
| Date | |
