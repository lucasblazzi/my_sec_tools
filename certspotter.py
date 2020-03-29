import urllib.request, urllib.parse, urllib.error
import json
import ssl


# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def dns_list(serviceurl):                                       #handle webpage (urllib)      
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0'
    request = urllib.request.Request(serviceurl,headers={'User-Agent': user_agent})
    try:
        handler = urllib.request.urlopen(request)
    except urllib.error.HTTPError as e:                        # manipulando erros HTTP
        print("CODE:", e.code, " -->", e.reason.upper())       
        exit()
    except urllib.error.URLError:                              # manipulando erros na URL
        print("Server down or incorrect domain")
        exit()

    data = handler.read().decode()

    try:                                                        #loads json
        js = json.loads(data)
    except:
        js = None

    for count in range(len(js)):                                #get dns_names json and print
        dns_name = js[count]['dns_names']
        for dns in dns_name:
            print(dns)

def service_url(address):
    print()
    print('Retrieving subdomains for:', address)
    print()
    serviceurl = 'https://api.certspotter.com/v1/issuances?domain=' + address + '&include_subdomains=true&expand=dns_names&expand=issuer&expand=cert'
    dns_list(serviceurl)

def man_input(address):                                         #manual input of domains
    while True:
        address = input('Enter domain: ')
        if len(address) < 1: break
        service_url(address)

def file_input():
    fname = input("file name:")
    fh = open(fname)
    for line in fh:
        address = line.rstrip()
        service_url(address)

def menu():
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
    elif menu == 2:
        file_input()
        
        
menu()

