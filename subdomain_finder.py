import urllib.request, urllib.parse, urllib.error
import json
import ssl
import argparse
import itertools

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


def dns_list(address):
    print('\n[*] Searching for {} subdomains\n\n'.format(address))
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0'
    services = [
        {'api': 'crtsh', 'url': 'https://crt.sh/?q=%25.{}&output=json'.format(address)},
        {'api': 'certspotter',
         'url': 'https://api.certspotter.com/v1/issuances?domain={}&include_subdomains=true&expand=dns_names&expand=issuer&expand=cert'.format(
             address)}
    ]

    subdomains = []
    for api in services:
        serviceurl = api['url']
        request = urllib.request.Request(serviceurl, headers={'User-Agent': user_agent})
        try:
            handler = urllib.request.urlopen(request)
        except urllib.error.HTTPError as e:  # manipulando erros HTTP
            print("CODE:", e.code, " -->", e.reason.upper())
            print("Certspotter may have blocked this request, try again later or get an API Key")
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


def file_search(file):
    file = open(file, 'r').read().split('\n')
    for line in file:
        dns_list(line)
    print('\n\n\n')


def print_subdomains(subdomains):
    subdomains = sorted(set(subdomains))
    print('[*] {} subdomains found\n'.format(len(subdomains)))
    for dns in subdomains:
        print(dns)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Find subdomains using certspotter and crtsh')
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-u", '--url', type=str,
                        help="single target - simple input")
    group.add_argument("-f", '--file', type=str,
                        help="multiple targets - input from file")
    args = parser.parse_args()
    if args.url:
        dns_list(args.url)
    if args.file:
        file_search(args.file)
