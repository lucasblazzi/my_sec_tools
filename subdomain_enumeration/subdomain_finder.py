import urllib.request, urllib.parse, urllib.error
import json
import ssl
import argparse
import itertools

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


def dns_list(address):
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0'
    services = [
        {'api': 'crtsh', 'url': 'https://crt.sh/?q=%25.{}&output=json' .format(address)},
        {'api': 'certspotter', 'url': 'https://api.certspotter.com/v1/issuances?domain={}&include_subdomains=true&expand=dns_names&expand=issuer&expand=cert' .format(address)}
    ]

    subdomains = []
    for api in services:
        serviceurl = api['url']
        request = urllib.request.Request(serviceurl, headers={'User-Agent': user_agent})
        try:
            handler = urllib.request.urlopen(request)
        except urllib.error.HTTPError as e:  # manipulando erros HTTP
            print("CODE:", e.code, " -->", e.reason.upper())
            exit()
        except urllib.error.URLError:  # manipulando erros na URL
            print("Server down or incorrect domain")
            exit()

        data = handler.read().decode()
        try:  # loads json
            js = json.loads(data)
        except:
            js = None

        if api['api'] == 'certspotter':
            for count in range(len(js)):  # get dns_names json and print
                dns_name = js[count]['dns_names']
                for dns in dns_name:
                    subdomains.append(dns)
        elif api['api'] == 'crtsh':
            for count in range(len(js)):  # get dns_names json and print
                dns_name = js[count]['name_value']
                subdomains.append(dns_name)

    all_subdomains = []
    for dns in subdomains:
        dns = dns.split('\n')
        all_subdomains.append(dns)

    subdomains = list(itertools.chain.from_iterable(all_subdomains))
    print_subdomains(subdomains)


def print_subdomains(subdomains):
    subdomains = sorted(set(subdomains))
    for dns in subdomains:
        print(dns)


def menu():
    parser = argparse.ArgumentParser(description='Find subdomains using certspotter and crtsh')
    parser.add_argument("-u", '--url', type=str,
                        help="single target input")
    args = parser.parse_args()
    if args.url:
        dns_list(args.url)


menu()