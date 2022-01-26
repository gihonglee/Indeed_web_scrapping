import pandas as pd
import requests

from bs4 import BeautifulSoup
# reference from https://www.youtube.com/watch?v=PPcgtx0sI2E

def extract(page):
	headers = {"User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'}
	url = f'https://www.indeed.com/jobs?q=data%20scientist&l=Washington%2C%20DC&start={page}&vjk=a2fb13319444e5be'
	r = requests.get(url, headers)
	soup = BeautifulSoup(r.content, 'html.parser')
	return soup
def containsNumber(value):
    for character in value:
        if character.isdigit():
            return True
    return False

def transform(soup):
	
	divs = soup.find_all('div', class_ = "job_seen_beacon") #jobCard_mainContent big6_visualChanges
	for item in divs:
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
		salary = item.find('div', class_ = "attribute_snippet").text if item.find('div', class_ = "attribute_snippet") else None
		if salary == None:
			salary = item.find('span',class_ = "estimated-salary").text if item.find('span',class_ = "estimated-salary") else None
		description = item.find('div', class_ = "job-snippet").text.replace('\n', '') if item.find('div', class_ = "job-snippet") else None
		daysago = item.find('span', class_ = "date").text if item.find('span', class_ = "visually-hidden") else None
		data_jk = item.find('a', class_ = "data-jk").text if item.find('a', class_ = "data-jk") else None
		
		job = {
		'title': title,
		'company': company,
		'salary': salary,
		'location' : location,
		'company_rating' : rating,
		'description' : description,
		'daysago' : daysago         }
		jobList.append(job)
		print(data_jk)
	return jobList

jobList = []

i = 0
while i < 10:
	print(f'Getting page, {i/10 + 1}')
	try:
		c = extract(i)
	except:
		break
	transform(c)
	i += 10


df = pd.DataFrame(jobList)

print(df.head())
df.to_csv('jobs.csv')