import dns.resolver
import argparse

def dns_brute(domain, wordlist):
    try:
        file = open(wordlist)
        subdomains = file.read().splitlines()
        for sub in subdomains:
            site = sub + '.' + domain
            try:
                results = dns.resolver.resolve(site, 'A')
                for result in results:
                    print('[*]FOUND - {} --> IP: {}' .format(site, result))
            except:
                pass
    except FileNotFoundError:
        print('\nFile not found\n')
        pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Bruteforce subdomains using a wordlist')
    parser.add_argument("-u", "--url", type=str,
                        help="target domain")
    parser.add_argument("-w", "--wordlist", type=str,
                        help="subdomain wordlist")
    args = parser.parse_args()
    if args.url and args.wordlist:
        dns_brute(args.url, args.wordlist)