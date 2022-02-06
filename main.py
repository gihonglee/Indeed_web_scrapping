from email import header
from matplotlib.cbook import ls_mapper
import pandas as pd
import requests
import time
from datetime import datetime
from bs4 import BeautifulSoup
import proxy_cleaning
# reference from https://www.youtube.com/watch?v=PPcgtx0sI2E



api_url = "https://www.indeed.com/viewjob?viewtype=embedded&jk={job_id}"
headers_list = [{"User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'},
{"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'},
{"User-Agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36'},
{"User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'},
 {"User-Agent": 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1'},
 {"User-Agent" : 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36'}]


def extract(page,proxy_list,proxy_i):
    url = f'https://www.indeed.com/jobs?q=data%20scientist&l=United%20States&start={page}&vjk=9be962d3b5516567'
    r = requests.get(url, headers = headers_list[(page//10)%6], proxies = {'http': proxy_list[proxy_i], 'https': proxy_list[proxy_i]})
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup

def transform(soup,i,jobList):
	# divs = soup.find_all('div', class_ = "job_seen_beacon")
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

		job_result = {
		'title': title,
		'company': company,
		'salary': salary,
		'location' : location,
		'company_rating' : rating,
		'description' : description}
		jobList.append(job_result)

	return jobList # result of a jobinfo in a page

def main():
	#Variable Declaration and prepare for the 
	page = 0
	proxy_list = proxy_cleaning.working_list('https://www.indeed.com/jobs?q=data%20scientist&l=United%20States&start=0&vjk=9be962d3b5516567')
	proxy_i = 0
	jobList = []
	print("start to scrapping")
	print(f"we have {len(proxy_list)} wokring proxy list")

	# iterate the pages and proxies to scrap
	while page < 1000:
		start = time.process_time()
		soup = None
		while soup is None:
			try: # need to iterate the proxies
				soup = extract(page,proxy_list,proxy_i)	
			except:
				proxy_i = proxy_i + 1
				print(f"{proxy_i}th proxy out of {len(proxy_list)} | Soup iteration, move to next proxy")
				if proxy_i > len(proxy_list) -2:          
					proxy_list = proxy_cleaning.working_list('https://www.indeed.com/jobs?q=data%20scientist&l=United%20States&start=0&vjk=9be962d3b5516567')# need to reset proxy_list 
					print(f"we have {len(proxy_list)} wokring proxy list")           
					proxy_i = 0
					print(f"{proxy_i}th proxy out of {len(proxy_list)} | Soup iteration, resetting the proxylist")
		jobList = transform(soup,page,jobList)
		
		if page % 10 == 0:
			df = pd.DataFrame(jobList)
			now = datetime.now()
			current_time = now.strftime("%H")
			df.to_csv('jobs' + str(current_time) + '.csv')

		time_taken = time.process_time() - start
		
		if time_taken <0.7:
			proxy_i = proxy_i+1
			print(f"{proxy_i}th proxy out of {len(proxy_list)} | Time took very short")
			if proxy_i > len(proxy_list) -2:          
				proxy_list = proxy_cleaning.working_list('https://www.indeed.com/jobs?q=data%20scientist&l=United%20States&start=0&vjk=9be962d3b5516567')# need to reset proxy_list    
				print(f"we have {len(proxy_list)} wokring proxy list")        
				proxy_i = 0
				print(f"{proxy_i}th proxy out of {len(proxy_list)} | Time took very short")

		print(f'Page, {page/10 + 1} done' , time_taken)
		page += 10

	df = pd.DataFrame(jobList)
	now = datetime.now()
	current_time = now.strftime("%H")
	df.to_csv('jobs' + str(current_time) + '.csv')

if __name__ == "__main__":
    main()
