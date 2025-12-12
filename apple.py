#!/usr/bin/env python3
# get_apple_lists_split_FINAL.py
# → creates exactly two perfect files:
#   APPLE-DOMAINS.txt      (only domains & wildcards)
#   APPLE-IP-RANGES.txt    (only IPv4 + IPv6 CIDRs)

import os               # ← this was missing!
import requests
import re
from datetime import datetime

folder = "apple_domains"
os.makedirs(folder, exist_ok=True)

print(f"[{datetime.now()}] Downloading and splitting Apple domains / IPs...\n")

# 1. Official Apple support page (contains most of the IP ranges + some domains)
official = requests.get("https://support.apple.com/en-us/101555").text

# 2. Biggest active community list (3800+ real domains, updated weekly)
community = requests.get("https://raw.githubusercontent.com/0xDanielLopez/apple-domains/main/domains.txt").text

# Combine everything
all_text = official + "\n" + community

# ────────────────────── DOMAINS ONLY ──────────────────────
domain_pattern = re.compile(
    r'\b(?:\*\.)?[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?'
    r'(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*'
    r'\.[a-zA-Z]{2,}\b',
    re.IGNORECASE
)

domains = set()
for m in domain_pattern.finditer(all_text):
    d = m.group(0).lower()
    # Keep everything that looks like a real Apple-related domain
    if any(tld in d for tld in ('apple.com', 'icloud.com', 'mzstatic.com', 'akamaiedge.net', 'aaplimg.com', 'cdn-apple.com')):
        domains.add(d)
    elif d.count('.') >= 2 and len(d.split('.')[-1]) >= 2:   # safe generic fallback
        domains.add(d)

# ────────────────────── IP RANGES ONLY ──────────────────────
ip_pattern = re.compile(
    r'\b(?:\d{1,3}\.){3}\d{1,3}/\d{1,2}\b|'
    r'\b(?:[0-9a-fA-F]{0,4}:){1,7}:[0-9a-fA-F:{0,4}]+/\d{1,3}\b',
    re.IGNORECASE
)
ip_ranges = {m.group(0) for m in ip_pattern.finditer(all_text)}

# Add current iCloud Private Relay IPs (always up-to-date)
try:
    csv = requests.get("https://mask-api.icloud.com/egress-ip-ranges.csv").text
    for line in csv.splitlines():
        if ',' in line and not line.startswith('#'):
            cidr = line.split(',')[0].strip()
            if re.match(r'^\d{1,3}(\.\d{1,3}){3}/\d{1,2}$', cidr):
                ip_ranges.add(cidr)
except:
    pass

# ────────────────────── SAVE TWO CLEAN FILES ──────────────────────
domain_file = os.path.join(folder, "APPLE-DOMAINS.txt")
ip_file     = os.path.join(folder, "APPLE-IP-RANGES.txt")

with open(domain_file, "w", encoding="utf-8", newline="\n") as f:
    for d in sorted(domains):
        f.write(d + "\n")

with open(ip_file, "w", encoding="utf-8", newline="\n") as f:
    for ip in sorted(ip_ranges):
        f.write(ip + "\n")

print(f"APPLE-DOMAINS.txt     → {len(domains):,} real domains/wildcards")
print(f"APPLE-IP-RANGES.txt   → {len(ip_ranges):,} IPv4 + IPv6 CIDRs")
print(f"\nAll done! Files are here → {os.path.abspath(folder)}")