import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
def extract():
	header = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"}
	url = f'https://free-proxy-list.net/'
	r = requests.get(url, headers = header)
	soup = BeautifulSoup(r.content, 'html.parser')
	return soup

def transform(soup):
    datas = []
    table = soup.find('table', class_ = "table table-striped table-bordered")
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data_temp = [ele for ele in cols if ele]
        data = {
		'IP': data_temp[0],
		'Port': data_temp[1],
		'Https': data_temp[6]
		}
        datas.append(data)
    return datas

def update_csv():
    c = extract()	
    datas = transform(c)
    df = pd.DataFrame(datas)
    df.to_csv('proxylist.csv')

