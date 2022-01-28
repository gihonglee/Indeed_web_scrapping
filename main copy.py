import requests
from bs4 import BeautifulSoup

headers = {"User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'}

url = "https://www.indeed.com/jobs?q=data+engineer&l=United+States"
api_url = "https://www.indeed.com/viewjob?viewtype=embedded&jk={job_id}"

soup = BeautifulSoup(requests.get(url, headers=headers).content, "html.parser")

for job in soup.select('a[id^="job_"]'):
	job_id = job["id"].split("_")[-1]
	item = soup.find(id = "job_" + job_id)
	salary = None
	salary = item.find('div', class_ = "metadata salary-snippet-container").text if item.find('div', class_ = "metadata salary-snippet-container") else None
	if salary == None:
		salary = item.find('div',class_ = "metadata estimated-salary-container").text if item.find('div',class_ = "metadata estimated-salary-container") else None
	print(salary)
	
	# s = BeautifulSoup(

	# 	requests.get(api_url.format(job_id=job_id), headers=headers).content,
	# 	"html.parser",
	# )

	# print(s.title.get_text(strip=True))
	# print()
	# print(s.select_one("#jobDescriptionText").get_text(strip=True, separator="\n"))
	# print("#" * 80)