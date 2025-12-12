#!/usr/bin/env python
import json

# URL https://www.gstatic.com/ipranges/cloud.json
# URL https://www.gstatic.com/ipranges/goog.json

def process_json_file(filename):
    # Load JSON data from file
    with open(filename, 'r') as file:
        data = json.load(file)

    # Extract IPv4 and IPv6 addresses with subnet
    ip_subnets = []
    for prefix in data['prefixes']:
        if 'ipv4Prefix' in prefix:
            ip_subnets.append(prefix['ipv4Prefix'])
        elif 'ipv6Prefix' in prefix:
            ip_subnets.append(prefix['ipv6Prefix'])

    return ip_subnets

# Process first input file
ip_subnets1 = process_json_file('goog.json')

# Process second input file
ip_subnets2 = process_json_file('cloud.json')

# Combine IP addresses from both files
all_ip_subnets = ip_subnets1 + ip_subnets2

# Write all IP addresses to text file
with open('ips_google.txt', 'w') as output_file:
    for subnet in all_ip_subnets:
        output_file.write(subnet + '\n')
