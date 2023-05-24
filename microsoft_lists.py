#!/usr/bin/env python
import argparse
import sys
import requests
import json

# URL https://us1.proofpointessentials.com/api/v1/orgs/mycompany.com/users/
# API Documentation https://eu1.proofpointessentials.com/api/v1/docs/index.php


def main():
    ips = []
    urls = []

    with open("worldwide.json") as file:
        scopes = json.load(file)
    for scope in scopes:
        if 'ips' in scope:
            ips += (scope['ips'])
        if 'urls' in scope:
            urls += (scope['urls'])

    print(ips)
    print(urls)

    with open("ips.txt", 'a') as file_ip:
        for ip in ips:
            file_ip.write(ip+"\n")

    with open("urls.txt", 'a') as file_urls:
        for url in urls:
            file_urls.write(url+"\n")


if __name__ == '__main__':
	main()