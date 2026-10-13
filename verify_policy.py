#!/usr/bin/env python3
"""Policy verifier for HealthNet.

Parses the ACLs and their interface bindings from configs/core-sw1-security.txt
and runs the 20-case test matrix against them, using first-match-wins and an
implicit deny, like IOS. Each allow case also checks the return leg through the
ingress ACL of the destination VLAN.

What this proves: the written ACL text implements the written access policy.
What it does not prove: that Packet Tracer behaves the same. Run the matrix in
Packet Tracer too and record the real results in docs/test-matrix.md.

Usage:  python3 tools/verify_policy.py [--markdown]
"""
import ipaddress as ip
import os
import sys
from dataclasses import dataclass
from typing import Optional

CONFIG = os.path.join(os.path.dirname(__file__), "..", "configs", "core-sw1-security.txt")
ANY = ip.ip_network("0.0.0.0/0")


@dataclass
class Rule:
    action: str
    proto: str
    src: ip.IPv4Network
    sport: Optional[int]
    dst: ip.IPv4Network
    dport: Optional[int]
    flag: Optional[str]
    text: str


@dataclass
class Pkt:
    proto: str
    src: str
    dst: str
    sport: Optional[int] = None
    dport: Optional[int] = None
    est: bool = False
    icmp: Optional[str] = None  # "echo" or "echo-reply"


def _addr(tok, i):
    if tok[i] == "any":
        return ANY, i + 1
    if tok[i] == "host":
        return ip.ip_network(tok[i + 1] + "/32"), i + 2
    inv = ".".join(str(255 - int(o)) for o in tok[i + 1].split("."))
    return ip.ip_network(f"{tok[i]}/{inv}", strict=False), i + 2


def _port(tok, i):
    if i < len(tok) and tok[i] == "eq":
        return int(tok[i + 1]), i + 2
    return None, i


def parse(path):
    acls, binding, cur_acl, cur_if = {}, {}, None, None
    for raw in open(path):
        line = raw.strip()
        if not line or line.startswith("!"):
            continue
        tok = line.split()
        if line.startswith("ip access-list extended"):
            cur_acl, cur_if = tok[-1], None
            acls[cur_acl] = []
        elif line.startswith("interface vlan"):
            cur_if, cur_acl = int(tok[-1]), None
        elif line.startswith("ip access-group") and cur_if is not None:
            binding[cur_if] = tok[2]
        elif cur_acl and tok[0] in ("permit", "deny"):
            src, i = _addr(tok, 2)
            sport, i = _port(tok, i)
            dst, i = _addr(tok, i)
            dport, i = _port(tok, i)
            flag = tok[i] if i < len(tok) and tok[i] in ("established", "echo", "echo-reply") else None
            acls[cur_acl].append(Rule(tok[0], tok[1], src, sport, dst, dport, flag, line))
        elif tok[0] == "exit":
            cur_acl = None
    return acls, binding


def matches(r: Rule, p: Pkt):
    if r.proto != "ip" and r.proto != p.proto:
        return False
    if ip.ip_address(p.src) not in r.src or ip.ip_address(p.dst) not in r.dst:
        return False
    if r.sport is not None and p.sport != r.sport:
        return False
    if r.dport is not None and p.dport != r.dport:
        return False
    if r.flag == "established" and not p.est:
        return False
    if r.flag in ("echo", "echo-reply") and p.icmp != r.flag:
        return False
    return True


def evaluate(acls, binding, vlan, p: Pkt):
    """Return (allowed, matched rule text). vlan=None means no ACL (uplink/internet)."""
    if vlan is None:
        return True, "(no ACL on this path)"
    for r in acls[binding[vlan]]:
        if matches(r, p):
            return r.action == "permit", f"{binding[vlan]}: {r.text}"
    return False, f"{binding[vlan]}: implicit deny"


CLIN, ADM, GST, IOT = "10.10.10.50", "10.10.20.50", "10.10.30.50", "10.10.40.50"
APP, DNS, LOG, SWA1, NET = "10.10.50.10", "10.10.50.11", "10.10.50.12", "10.10.99.11", "8.8.8.8"


def tcp(s, d, dp, sp=40000, est=False):
    return Pkt("tcp", s, d, sp, dp, est)


def echo(s, d):
    return Pkt("icmp", s, d, icmp="echo")


def reply_echo(s, d):
    return Pkt("icmp", s, d, icmp="echo-reply")


# (id, description, expected, [(ingress_vlan, packet), ...legs...])
CASES = [
    (1, "Clinical -> APP-SRV TCP 443", "Allow", [(10, tcp(CLIN, APP, 443)), (50, tcp(APP, CLIN, 40000, 443, True))]),
    (2, "Clinical -> DNS UDP 53", "Allow", [(10, Pkt("udp", CLIN, DNS, 40000, 53)), (50, Pkt("udp", DNS, CLIN, 53, 40000))]),
    (3, "Clinical DHCP lease via relay", "Allow", [(10, Pkt("udp", "0.0.0.0", "255.255.255.255", 68, 67)), (50, Pkt("udp", DNS, "10.10.10.1", 67, 67))]),
    (4, "Admin -> APP-SRV TCP 443", "Allow", [(20, tcp(ADM, APP, 443)), (50, tcp(APP, ADM, 40000, 443, True))]),
    (5, "Admin -> mgmt switch SSH 22", "Allow", [(20, tcp(ADM, SWA1, 22)), (99, tcp(SWA1, ADM, 40000, 22, True))]),
    (6, "Admin -> SYSLOG-AAA ICMP", "Allow", [(20, echo(ADM, LOG)), (50, reply_echo(LOG, ADM))]),
    (7, "IoT -> APP-SRV TCP 443", "Allow", [(40, tcp(IOT, APP, 443)), (50, tcp(APP, IOT, 40000, 443, True))]),
    (8, "Guest -> Internet ICMP", "Allow", [(30, echo(GST, NET)), (None, reply_echo(NET, GST))]),
    (9, "Mgmt switch -> SYSLOG UDP 514", "Allow", [(99, Pkt("udp", SWA1, LOG, 50000, 514))]),
    (10, "APP-SRV reply -> Clinical (established)", "Allow", [(50, tcp(APP, CLIN, 40000, 443, True))]),
    (11, "Guest -> Clinical", "Deny", [(30, echo(GST, CLIN))]),
    (12, "Guest -> APP-SRV TCP 443", "Deny", [(30, tcp(GST, APP, 443))]),
    (13, "Guest -> mgmt switch SSH", "Deny", [(30, tcp(GST, SWA1, 22))]),
    (14, "Guest -> IoT", "Deny", [(30, echo(GST, IOT))]),
    (15, "Clinical -> IoT", "Deny", [(10, echo(CLIN, IOT))]),
    (16, "Clinical -> mgmt switch SSH", "Deny", [(10, tcp(CLIN, SWA1, 22))]),
    (17, "Admin -> IoT", "Deny", [(20, echo(ADM, IOT))]),
    (18, "IoT -> Clinical", "Deny", [(40, echo(IOT, CLIN))]),
    (19, "IoT -> mgmt switch SSH", "Deny", [(40, tcp(IOT, SWA1, 22))]),
    (20, "Clinical -> Internet ICMP", "Deny", [(10, echo(CLIN, NET))]),
]


def main():
    acls, binding = parse(CONFIG)
    md = "--markdown" in sys.argv
    failures = 0
    rows = []
    for cid, desc, expected, legs in CASES:
        allowed, why = True, ""
        for vlan, pkt in legs:
            ok, rule = evaluate(acls, binding, vlan, pkt)
            if not ok:
                allowed, why = False, rule
                break
            why = rule
        got = "Allow" if allowed else "Deny"
        status = "PASS" if got == expected else "FAIL"
        failures += status == "FAIL"
        rows.append((cid, desc, expected, got, status, why))
    if md:
        print("| # | Case | Expected | Model result | Matched rule |")
        print("|---|---|---|---|---|")
        for cid, desc, exp, got, st, why in rows:
            print(f"| {cid} | {desc} | {exp} | {got} ({st}) | `{why}` |")
    else:
        for cid, desc, exp, got, st, why in rows:
            print(f"{cid:>2}  {st}  expected {exp:<5} got {got:<5}  {desc}\n      {why}")
    total = len(rows)
    print(f"\n{total - failures}/{total} cases match the access policy")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
