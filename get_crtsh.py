import urllib.request, urllib.parse, urllib.error
import json
import ssl
import argparse

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

    dns_list = list()

    for count in range(len(js)):                                #get dns_names json and print
        dns_name = js[count]['name_value']
        dns_list.append(dns_name)

    dns_list = sorted(set(dns_list))
    for dns in dns_list:
        print(dns)

def service_url(address):
    print()
    print('Retrieving subdomains for:', address)
    print()
    serviceurl = 'https://crt.sh/?q=%25.'+address+'&output=json'
    dns_list(serviceurl)

def file_input(fname):
    fh = open(fname)
    for line in fh:
        address = line.rstrip()
        service_url(address)


def menu():
    parser = argparse.ArgumentParser(description='Find subdomains using certspotter')
    parser.add_argument("-i", '--input', type=str,
                        help="single target input")
    parser.add_argument("-f", "--file", type=str,
                        help="file list of targets")
    #parser.add_argument("-o", "--output", type=str,
    #                   help="output the results to a .txt file")
    args = parser.parse_args()

    if args.input:
        service_url(args.input)
    if args.file:
        file_input(args.file)

menu()
