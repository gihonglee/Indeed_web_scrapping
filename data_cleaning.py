import pandas as pd
import numpy as np
#git checkout -b data_cleaning

df = pd.read_csv("jobs13:31:55.csv")

# salary parsing
# state field
# parsing of job description (python ,etc)

#salary
#1.get rid of salaray -1
df = df[df['Salary Estimate'] != '-1'] # this will only return result that is not -1
# remove (Glassdoor est.)
salary = df['Salary Estimate'].apply(lambda x: x.split('(')[0])
minus_kd = salary.apply(lambda x: x.remove('K$'))

