# Test Matrix

Two separate kinds of evidence. Do not mix them up on your resume or in interviews.

## 1. Policy model (automated, done)

`python3 tools/verify_policy.py` parses the ACLs in `configs/core-sw1-security.txt` and checks all 20 cases, including return traffic. Result: **20/20 match the access policy.** Mutation check: deleting the guest isolation rule makes it report 16/20, so the script does detect broken rules.

| # | Case | Expected | Model result | Matched rule |
|---|---|---|---|---|
| 1 | Clinical -> APP-SRV TCP 443 | Allow | Allow (PASS) | `SRV-IN: permit tcp 10.10.50.0 0.0.0.255 any established` |
| 2 | Clinical -> DNS UDP 53 | Allow | Allow (PASS) | `SRV-IN: permit udp host 10.10.50.11 eq 53 any` |
| 3 | Clinical DHCP lease via relay | Allow | Allow (PASS) | `SRV-IN: permit udp host 10.10.50.11 eq 67 any eq 67` |
| 4 | Admin -> APP-SRV TCP 443 | Allow | Allow (PASS) | `SRV-IN: permit tcp 10.10.50.0 0.0.0.255 any established` |
| 5 | Admin -> mgmt switch SSH 22 | Allow | Allow (PASS) | `MGMT-IN: permit tcp 10.10.99.0 0.0.0.255 10.10.20.0 0.0.0.255 established` |
| 6 | Admin -> SYSLOG-AAA ICMP | Allow | Allow (PASS) | `SRV-IN: permit icmp 10.10.50.0 0.0.0.255 any echo-reply` |
| 7 | IoT -> APP-SRV TCP 443 | Allow | Allow (PASS) | `SRV-IN: permit tcp 10.10.50.0 0.0.0.255 any established` |
| 8 | Guest -> Internet ICMP | Allow | Allow (PASS) | `(no ACL on this path)` |
| 9 | Mgmt switch -> SYSLOG UDP 514 | Allow | Allow (PASS) | `MGMT-IN: permit udp 10.10.99.0 0.0.0.255 host 10.10.50.12 eq 514` |
| 10 | APP-SRV reply -> Clinical (established) | Allow | Allow (PASS) | `SRV-IN: permit tcp 10.10.50.0 0.0.0.255 any established` |
| 11 | Guest -> Clinical | Deny | Deny (PASS) | `GUEST-IN: deny ip 10.10.30.0 0.0.0.255 10.10.0.0 0.0.255.255` |
| 12 | Guest -> APP-SRV TCP 443 | Deny | Deny (PASS) | `GUEST-IN: deny ip 10.10.30.0 0.0.0.255 10.10.0.0 0.0.255.255` |
| 13 | Guest -> mgmt switch SSH | Deny | Deny (PASS) | `GUEST-IN: deny ip 10.10.30.0 0.0.0.255 10.10.0.0 0.0.255.255` |
| 14 | Guest -> IoT | Deny | Deny (PASS) | `GUEST-IN: deny ip 10.10.30.0 0.0.0.255 10.10.0.0 0.0.255.255` |
| 15 | Clinical -> IoT | Deny | Deny (PASS) | `CLIN-IN: deny ip any any` |
| 16 | Clinical -> mgmt switch SSH | Deny | Deny (PASS) | `CLIN-IN: deny ip any any` |
| 17 | Admin -> IoT | Deny | Deny (PASS) | `ADMIN-IN: deny ip any any` |
| 18 | IoT -> Clinical | Deny | Deny (PASS) | `IOT-IN: deny ip any any` |
| 19 | IoT -> mgmt switch SSH | Deny | Deny (PASS) | `IOT-IN: deny ip any any` |
| 20 | Clinical -> Internet ICMP | Deny | Deny (PASS) | `CLIN-IN: deny ip any any` |

This shows the written ACLs implement the written policy. It does not prove Packet Tracer behaves the same.

## 2. Packet Tracer run (manual, your results)

Run every case once before applying `core-sw1-security.txt` and once after. Use ping (ICMP cases), Desktop > Web Browser or Telnet/SSH to the port (TCP cases), and simulation mode if a result surprises you.

| # | Before ACLs (expected: Allow) | After ACLs (Expected per table above) | Matches? | Notes / screenshot |
|---|---|---|---|---|
| 1 | | | |
| 2 | | | |
| 3 | | | |
| 4 | | | |
| 5 | | | |
| 6 | | | |
| 7 | | | |
| 8 | | | |
| 9 | | | |
| 10 | | | |
| 11 | | | |
| 12 | | | |
| 13 | | | |
| 14 | | | |
| 15 | | | |
| 16 | | | |
| 17 | | | |
| 18 | | | |
| 19 | | | |
| 20 | | | |

Only quote "20 of 20 passing in Packet Tracer" on your resume after this table is filled in with real results.
