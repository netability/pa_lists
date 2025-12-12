#!/usr/bin/env python3
# fetch_proofpoint_ips_correct_url.py
# Fetches ONLY IP ranges (CIDRs) from the CORRECT Proofpoint webpage source.
# Note: Page requires authentication. To use:
# 1. Log in to https://help.proofpoint.com in your browser.
# 2. Navigate to: https://help.proofpoint.com/Essentials/Product_Documentation/Email_Security/Mail_Services/01_Connection_Details
# 3. View page source (Ctrl+U), copy ALL HTML.
# 4. Paste into a file named 'proofpoint_page.html' in the same folder as this script.
# 5. Run: python fetch_proofpoint_ips_correct_url.py
# Output: proofpoint-ips-fetched.txt (clean list of IPs/CIDRs only)

import re
from datetime import datetime

# Load the HTML from the local file (paste the page source here)
html_filename = "proofpoint_page.html"  # ← Create this file with copied HTML
output_filename = "proofpoint-ips-fetched.txt"

print(f"[{datetime.now()}] Fetching IPs from local Proofpoint page source (correct URL)...")

try:
    with open(html_filename, "r", encoding="utf-8", errors="ignore") as f:
        html_content = f.read()
except FileNotFoundError:
    print(f"Error: Please create '{html_filename}' with the page source (Ctrl+U after logging in).")
    print("Steps: 1. Log in to Proofpoint Help. 2. Go to the correct URL. 3. Copy full source. 4. Paste & save as '{html_filename}'.")
    exit(1)

# Strict regex: Matches ONLY valid IPv4 CIDR ranges (e.g., 67.216.175.0/20)
# Proofpoint uses only IPv4 CIDRs for SMTP/DKIM—no IPv6.
cidr_pattern = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}/[0-9]{1,2}\b')

# Find all matches
cidrs = set(re.findall(cidr_pattern, html_content))

# Sort them logically (by IP, then prefix length)
def sort_key(cidr):
    ip, prefix = cidr.rsplit('/', 1)
    ip_parts = [int(x) for x in ip.split('.')]
    return tuple(ip_parts) + (int(prefix),)

sorted_cidrs = sorted(cidrs, key=sort_key)

# Save to clean TXT file (IPs only, one per line)
with open(output_filename, "w", encoding="utf-8") as f:
    f.write(f"# Proofpoint Essentials IP Ranges (Fetched from correct webpage)\n")
    f.write(f"# URL: https://help.proofpoint.com/Essentials/Product_Documentation/Email_Security/Mail_Services/01_Connection_Details\n")
    f.write(f"# Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(f"# Total: {len(sorted_cidrs)} CIDRs\n\n")
    for cidr in sorted_cidrs:
        f.write(cidr + "\n")

print(f"Success! {len(sorted_cidrs)} IP ranges extracted and saved to '{output_filename}'.")
print("\nSample (first 5):")
for cidr in sorted_cidrs[:5]:
    print(f"  - {cidr}")
print(f"\nFull list ready for firewall import (ESXi, pfSense, etc.).")
if len(sorted_cidrs) < 5:
    print("Warning: Low count—ensure you copied the full page source including tables. Search HTML for '67.216' to verify.")