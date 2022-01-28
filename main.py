import pandas as pd
import requests
import time

from bs4 import BeautifulSoup
# reference from https://www.youtube.com/watch?v=PPcgtx0sI2E

api_url = "https://www.indeed.com/viewjob?viewtype=embedded&jk={job_id}"
#headers = {"User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'}
headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'}
def extract(page):
	#headers = {"User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'}
	
	url = f'https://www.indeed.com/jobs?q=data%20scientist&l=United%20States&start={page}&vjk=9be962d3b5516567'
	r = requests.get(url, headers = headers)
	soup = BeautifulSoup(r.content, 'html.parser')
	return soup

def transform(soup):
	
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
			requests.get(api_url.format(job_id=job_id), headers=headers).content,
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
while i < 30:
	start = time.process_time()
	
	try:
		c = extract(i)
	except:
		break
	transform(c)
	time_taken = time.process_time() - start
	print(f'Page, {i/10 + 1} done' , time_taken)
	i += 10


df = pd.DataFrame(jobList)

print(df.head(10))
df.to_csv('jobs.csv')