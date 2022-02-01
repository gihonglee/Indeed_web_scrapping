import re
import requests
import csv
import concurrent.futures

proxylist = []

with open('proxylist.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        proxylist.append(row[1])

def extract(proxy):
    try:
        r = requests.get('https://httpbin.org/ip', proxies= {'http:' : proxy, 'https:' : proxy}, timeout = 2)
        print(r.json(), '- woring')
    except:
        pass
    return proxy

with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(extract, proxylist)

# for proxy in proxylist:
#     print(proxy)
#     extract(proxy)