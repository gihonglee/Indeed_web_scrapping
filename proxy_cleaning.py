import re
import requests
import csv
import concurrent.futures
import proxy_scrapping

url = 'https://www.indeed.com/jobs?q=data%20scientist&l=United%20States&start=10&vjk=9be962d3b5516567'
header = {"User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'}

def get_list():
    proxylist = []
    with open('proxylist.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            proxylist.append(row[1] +  ":" + row[2])
    return proxylist[1:]

def extract(proxy):
    count = 0
    try:
        r =requests.get(url, proxies = {'http': proxy, 'https': proxy}, timeout = 2)
        count += 1
        print(proxy)
        print(r.status_code)
        print(count)
        return proxy
    except:
        pass
    

def working_list(url):
    proxy_scrapping.update_csv()
    print(f"data update completed! We have {len(get_list())} proxies")
    # good_list = []
    # url_list = [url for i in range(len(get_list()))]
    with concurrent.futures.ThreadPoolExecutor() as executor:
        lista = executor.map(extract, get_list())
    # proxy_list = get_list()
    # for proxy in proxy_list:
    #     good_list.append(extract(proxy,url))
    return lista

lista = working_list(url)
count = 0
for i in lista:
    count +=1
print(count)
