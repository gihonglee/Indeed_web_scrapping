import pandas as pd
import numpy as np
#git checkout -b data_cleaning

df = pd.read_csv("jobs14:03:24.csv")
print(df.head())
print(df.shape)
print(df.describe)
print(df.columns)
print(df['column name'].isna().sum())
print(df.groupby(['salary']).count())
print()
# let's get the salary right






# # salary parsing
# df['hourly'] = df['Salary Estimate'].apply(lambda x: 1 if 'per hour' in x.lower() else 0)
# df['employe'] = df['Salary Estimate'].apply(lambda x: 1 if 'employer provided' in x.lower else 0)

# # salary
# # 1.get rid of salaray -1
# df = df[df['Salary Estimate'] != '-1'] # this will only return result that is not -1
# # remove (Glassdoor est.)
# salary = df['Salary Estimate'].apply(lambda x: x.split('(')[0])
# minus_kd = salary.apply(lambda x: x.remove('K').remove('$'))
# min_hr = minus_kd.apply(lambda x: x.lower().replace('per hour','').replace('employer provided salary:',''))

# df['min_salary'] = min_hr.apply(lambda x: int(x.split('-')[0]))
# df['max_salary'] = min_hr.apply(lambda x: int(x.split('-')[1]))
# df['avg_salary'] = (df['min_salary']+ df['max_salary']) /2

# # state field
# # parsing of job description (python ,etc)


