#!/usr/bin/env python3
# fetch_cloudflare_ips.py
# Fetches ONLY IP ranges (IPv4 + IPv6 CIDRs) from Cloudflare's official pages.
# Sources: https://www.cloudflare.com/ips-v4 and https://www.cloudflare.com/ips-v6
# Output: cloudflare-ips.txt (clean list of IPs/CIDRs only, one per line)

import requests
import re
from datetime import datetime

# Official Cloudflare URLs (public, no login needed)
urls = [
    "https://www.cloudflare.com/ips-v4",  # IPv4 CIDRs
    "https://www.cloudflare.com/ips-v6"   # IPv6 CIDRs
]

print(f"[{datetime.now()}] Fetching Cloudflare IP ranges from official pages...")

all_cidrs = set()

for url in urls:
    response = requests.get(url)
    response.raise_for_status()
    content = response.text
    
    # Strict regex: Matches ONLY valid IPv4 or IPv6 CIDRs
    # IPv4: e.g., 103.21.244.0/22
    # IPv6: e.g., 2400:cb00::/32
    cidr_pattern = re.compile(
        r'\b(?:\d{1,3}\.){3}\d{1,3}/\d{1,2}\b|'  # IPv4 CIDR
        r'\b(?:[0-9a-fA-F]{0,4}:){1,7}(?::[0-9a-fA-F]{0,4}){0,7}(?:/\d{1,3})?\b',  # IPv6 CIDR (handles :: shorthand)
        re.IGNORECASE
    )
    
    matches = re.findall(cidr_pattern, content)
    all_cidrs.update(matches)

# Sort: IPv4 first (by IP), then IPv6 (by hex)
def sort_key(cidr):
    if ':' in cidr:  # IPv6
        return ('2', cidr.lower())
    else:  # IPv4
        ip, prefix = cidr.rsplit('/', 1)
        ip_parts = [int(x) for x in ip.split('.')]
        return ('1', tuple(ip_parts) + (int(prefix),))

sorted_cidrs = sorted(all_cidrs, key=sort_key)

# Save to clean TXT file (IPs only, one per line)
output_filename = "cloudflare-ips.txt"
with open(output_filename, "w", encoding="utf-8") as f:
    f.write(f"# Cloudflare IP Ranges (IPv4 + IPv6)\n")
    f.write(f"# Sources: https://www.cloudflare.com/ips-v4 and https://www.cloudflare.com/ips-v6\n")
    f.write(f"# Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(f"# Total: {len(sorted_cidrs)} CIDRs\n\n")
    f.write("# IPv4 Ranges\n")
    for cidr in [c for c in sorted_cidrs if ':' not in c]:
        f.write(cidr + "\n")
    f.write("\n# IPv6 Ranges\n")
    for cidr in [c for c in sorted_cidrs if ':' in c]:
        f.write(cidr + "\n")

print(f"Success! {len(sorted_cidrs)} IP ranges extracted and saved to '{output_filename}'.")
print("\nSample IPv4 (first 5):")
for cidr in [c for c in sorted_cidrs if ':' not in c][:5]:
    print(f"  - {cidr}")
print("\nSample IPv6 (first 3):")
for cidr in [c for c in sorted_cidrs if ':' in c][:3]:
    print(f"  - {cidr}")
print(f"\nFull list ready for firewall import (ESXi, pfSense, etc.). Run anytime for updates.")
