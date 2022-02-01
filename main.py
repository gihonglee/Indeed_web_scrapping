from email import header
from matplotlib.cbook import ls_mapper
import pandas as pd
import requests
import time
from datetime import datetime
from bs4 import BeautifulSoup
# reference from https://www.youtube.com/watch?v=PPcgtx0sI2E

api_url = "https://www.indeed.com/viewjob?viewtype=embedded&jk={job_id}"
headers_list = [{"User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'},
{"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'},
{"User-Agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36'},
{"User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'},
 {"User-Agent": 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1'},
 {"User-Agent" : 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36'}]

def extract(page):
	
	url = f'https://www.indeed.com/jobs?q=data%20scientist&l=United%20States&start={page}&vjk=9be962d3b5516567'
	r = requests.get(url, headers = headers_list[(page//10)%6])
	soup = BeautifulSoup(r.content, 'html.parser')
	return soup

def transform(soup,i):
	
	divs = soup.find_all('div', class_ = "job_seen_beacon")
	
	for job in soup.select('a[id^="job_"]'):
		job_id = job["id"].split("_")[-1]
		item = soup.find(id = "job_" + job_id)
		title = ""
		title1 = item.find('span').text
		title2 = item.find_next('span').find_next('span').text
		if title1 == "new":
			title = title2
		else:
			title = title1
		company = item.find('span', class_ = "companyName").text
		rating = item.find('span', class_ = "ratingNumber").find('span').text if item.find('span', class_ = "ratingNumber") else None
		location = item.find('div', class_ = "companyLocation").text
		salary = None
		salary = item.find('div', class_ = "metadata salary-snippet-container").text if item.find('div', class_ = "metadata salary-snippet-container") else None
		if salary == None:
			salary = item.find('div',class_ = "metadata estimated-salary-container").text if item.find('div',class_ = "metadata estimated-salary-container") else None
		s = BeautifulSoup(
			requests.get(api_url.format(job_id=job_id), headers=headers_list[(i//10)%6]).content,
			"html.parser",
		)
		description = s.select_one("#jobDescriptionText").get_text(strip=True, separator="\n") if s.select_one("#jobDescriptionText") else None

		job = {
		'title': title,
		'company': company,
		'salary': salary,
		'location' : location,
		'company_rating' : rating,
		'description' : description}
		jobList.append(job)
	return jobList

jobList = []

i = 0
print(headers_list[(i//10)%6])
while i < 30000:
	start = time.process_time()
	
	try:
		c = extract(i)	
	except:
		break
	transform(c,i)
	time_taken = time.process_time() - start
	if time_taken <0.05:
		break
	
	print(f'Page, {i/10 + 1} done' , time_taken)
	i += 10
	time.sleep(5)

df = pd.DataFrame(jobList)

print(df.head(10))

now = datetime.now()
current_time = now.strftime("%H:%M:%S")
df.to_csv('jobs.csv' + current_time)
