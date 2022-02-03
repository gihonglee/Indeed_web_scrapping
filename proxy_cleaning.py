import re
import requests
import csv
import concurrent.futures
import proxy_scrapping


good_list = []
def get_list():
    proxylist = []
    with open('proxylist.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            proxylist.append(row[1] +  ":" + row[2])
    return proxylist[1:]

def extract(proxy,url):
    count = 0
    try:
        r =requests.get(url, proxies = {'http': proxy, 'https': proxy}, timeout = 2)
        count += 1
        good_list.append(proxy)
        return proxy
    except:
        pass
    

def working_list(url):
    proxy_scrapping.update_csv()
    print(f"data update completed! We have {len(get_list())} proxies")
    url_list = [url for i in range(len(get_list()))]
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(extract, get_list(),url_list)
    return good_list

