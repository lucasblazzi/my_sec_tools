import urllib.request, urllib.parse, urllib.error
import json
import ssl


# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def dns_list(serviceurl):
    uh = urllib.request.urlopen(serviceurl, context=ctx)
    data = uh.read().decode()

    try:
        js = json.loads(data)
    except:
        js = None

    for count in range(len(js)):
        dns_name = js[count]['dns_names']
        for dns in dns_name:
            print(dns)

def man_input(address):
    while True:
        address = input('Enter domain: ')
        print()
        print('Retrieving subdomains for:', address)
        print()
        serviceurl = 'https://api.certspotter.com/v1/issuances?domain=' + address + '&include_subdomains=true&expand=dns_names&expand=issuer&expand=cert'
        if len(address) < 1: break
        dns_list(serviceurl)
        

print("------------------------------------")
print("-------CERTSPOTTER SUBDOMAINS-------")
print("------------------------------------")
print()
print("1 - manual input")
print("2 - file list input")

menu = int(input("--->"))
if menu == 1:
    address = None
    man_input(address)
else:
    quit()

