from urllib.request import Request, urlopen
from fake_useragent import UserAgent
import random
from bs4 import BeautifulSoup
from IPython.core.display import clear_output

# Here I provide some proxies for not getting caught while scraping
ua = UserAgent() # From here we generate a random user agent
proxies = [] # Will contain proxies [ip, port]

# Main function
def main():
  # Retrieve latest proxies
  proxies_req = Request('https://www.sslproxies.org/')
  proxies_req.add_header('User-Agent', ua.random)
  proxies_doc = urlopen(proxies_req).read().decode('utf8')

  soup = BeautifulSoup(proxies_doc, 'html.parser')
  proxies_table = soup.find(id='proxylisttable')

  # Save proxies in the array
  for row in proxies_table.tbody.find_all('tr'):
    proxies.append({
      'ip':   row.find_all('td')[0].string,
      'port': row.find_all('td')[1].string
    })

  # Choose a random proxy
  proxy_index = random_proxy()
  proxy = proxies[proxy_index]

  for n in range(1, 20):
    req = Request('http://icanhazip.com')
    req.set_proxy(proxy['ip'] + ':' + proxy['port'], 'http')

    # Every 10 requests, generate a new proxy
    if n % 10 == 0:
      proxy_index = random_proxy()
      proxy = proxies[proxy_index]

    # Make the call
    try:
      my_ip = urlopen(req).read().decode('utf8')
      print('#' + str(n) + ': ' + my_ip)
      clear_output(wait = True)
    except: # If error, delete this proxy and find another one
      del proxies[proxy_index]
      print('Proxy ' + proxy['ip'] + ':' + proxy['port'] + ' deleted.')
      proxy_index = random_proxy()
      proxy = proxies[proxy_index]

# Retrieve a random index proxy (we need the index to delete it if not working)
def random_proxy():
  return random.randint(0, len(proxies) - 1)

if __name__ == '__main__':
  main()

user_agent_list = (
   #Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    #Firefox
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
)

 # Make a get request
user_agent = random.choice(user_agent_list)
headers= {'User-Agent': user_agent, "Accept-Language": "en-US, en;q=0.5"}
proxy = random.choice(proxies)
response = get("your url", headers=headers, proxies=proxy)


a = 49.128.185.109:8181
72.80.242.101:8080
204.13.155.165:14999
47.243.225.209:8080
85.25.93.136:5566
200.37.140.34:10101
95.216.247.69:40042
150.129.171.35:30093
117.121.202.62:8080
181.129.70.82:46752
81.214.138.123:3128
181.196.205.250:38178
169.57.1.84:8123
110.74.195.65:55443
43.155.105.144:59394
202.154.180.53:46717
103.86.187.242:23500
211.237.5.86:8899
5.189.184.6:80
34.138.225.120:8888
45.79.230.234:80
200.37.140.36:10101
14.161.31.192:53281
54.37.160.93:1080
54.36.250.193:80
103.250.153.242:31382
54.37.160.92:1080
202.62.84.210:53281
54.37.160.91:1080
185.177.125.108:8081
133.167.121.133:1976
54.37.160.90:1080
43.228.125.189:8080
163.116.159.237:8081
92.42.109.189:1080
43.155.92.192:59394
187.87.189.252:55443
117.121.204.9:9797
47.243.135.104:8080
92.42.109.188:1080
194.44.20.25:8282
119.81.189.194:80
43.134.208.11:59394
213.163.2.206:3128
103.87.170.123:58248
200.114.79.27:999
84.237.254.131:53281
14.102.44.1:44047
109.86.182.203:3128
202.40.188.94:40486
113.130.126.2:31932
119.235.17.105:55443
92.118.92.107:8181
140.227.238.217:3128
103.105.212.106:53281
190.145.200.126:53281
212.225.137.109:8080
210.14.104.230:8080
187.216.93.20:55443
41.77.13.186:53281
41.190.147.158:54018
178.88.185.2:3128
103.92.114.2:80
134.19.254.2:21231
70.44.24.245:8888
118.174.196.112:36314
27.79.210.17:14208
202.77.120.38:57965
182.253.232.58:44922
144.91.104.118:7777
95.216.247.71:40086
94.200.240.102:8080
103.215.72.115:55443
162.155.10.150:55443
140.227.213.98:3128
170.254.224.7:55443
201.184.145.62:999
134.119.206.108:1080
185.94.218.57:43403
103.240.168.138:6666
43.155.92.79:59394
194.233.69.38:443
103.152.100.155:8080
20.105.253.176:8080
194.233.69.41:443
85.195.120.157:1080
139.255.129.161:8080
110.74.199.16:63141
158.69.53.132:9300
123.231.221.243:6969
5.183.101.101:14999
88.132.34.230:53281
103.107.92.1:52827
111.92.164.242:50249
200.25.254.193:54240
62.240.163.2:8080
118.70.109.148:55443
190.63.169.34:53281
2.32.168.174:80
103.239.147.250:54623
