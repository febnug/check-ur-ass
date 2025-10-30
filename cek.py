#!/usr/bin/env python3

# cara pake : python3 cek.py <domain>

import socket
import requests
import sys
import dns.resolver

def check_dns(domain):
    print(f"🔎 DNS Lookup for {domain}")
    try:
        answers = dns.resolver.resolve(domain, 'A')
        for rdata in answers:
            print(f"  ➜ A record: {rdata.to_text()}")
    except Exception as e:
        print(f"  ✗ DNS A record error: {e}")

    try:
        answers = dns.resolver.resolve(domain, 'MX')
        for rdata in answers:
            print(f"  ➜ MX record: {rdata.exchange} (priority {rdata.preference})")
    except Exception:
        pass

    try:
        answers = dns.resolver.resolve(domain, 'NS')
        print(f"  ➜ NS records: {[r.to_text() for r in answers]}")
    except Exception:
        pass

def check_http(domain):
    print(f"\n🌐 HTTP Status Check for {domain}")
    urls = [f"http://{domain}", f"https://{domain}"]
    for url in urls:
        try:
            resp = requests.get(url, timeout=5)
            print(f"  ➜ {url} → {resp.status_code} {resp.reason}")
            if resp.status_code == 503:
                print("     ⚠️  Service Temporarily Unavailable (server overload/maintenance?)")
        except requests.exceptions.SSLError:
            print(f"  ✗ SSL error on {url}")
        except requests.exceptions.ConnectionError as e:
            print(f"  ✗ Connection error: {e}")
        except requests.exceptions.Timeout:
            print(f"  ✗ Timeout connecting to {url}")

def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <domain>")
        sys.exit(1)

    domain = sys.argv[1]
    check_dns(domain)
    check_http(domain)

if __name__ == "__main__":
    main()
